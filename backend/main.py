"""
main.py
=======
TEJUSKA Cloud Intelligence - FastAPI Backend
Entry point for all API routes.
"""

import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional

from notifications import NotificationService
from ai_engine import AIEngine
from payment_webhooks import router as payments_router

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("tejuska.main")

# ---------------------------------------------------------------------------
# Application lifespan
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("TEJUSKA Cloud Intelligence backend starting.")
    yield
    logger.info("TEJUSKA Cloud Intelligence backend shutting down.")


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------
app = FastAPI(
    title="TEJUSKA Cloud Intelligence API",
    version="1.0.0",
    description="Enterprise FinOps Agentic AI Backend",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payments_router, prefix="/webhooks", tags=["Payments"])

# ---------------------------------------------------------------------------
# Shared service instances
# ---------------------------------------------------------------------------
notification_service = NotificationService()
ai_engine = AIEngine()

# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------

class HealthResponse(BaseModel):
    status: str
    version: str


class NLPQueryRequest(BaseModel):
    tenant_id: str = Field(..., description="Unique tenant identifier.")
    query: str = Field(..., min_length=1, max_length=2000, description="Natural-language cost query.")


class NLPQueryResponse(BaseModel):
    tenant_id: str
    query: str
    sql: str
    answer: str


class AutoTerminationRequest(BaseModel):
    tenant_id: str = Field(..., description="Unique tenant identifier.")
    resource_id: str = Field(..., description="Cloud resource ID to evaluate.")
    dry_run: bool = Field(True, description="If True, simulate without executing.")


class NotificationRequest(BaseModel):
    tenant_id: str
    channel: str = Field(..., pattern="^(slack|email|sms)$")
    recipient: str
    subject: Optional[str] = None
    body: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check() -> HealthResponse:
    """Return service health status."""
    return HealthResponse(status="healthy", version="1.0.0")


@app.post("/api/v1/query", response_model=NLPQueryResponse, tags=["OPTIC - NLP"])
async def natural_language_query(request: NLPQueryRequest) -> NLPQueryResponse:
    """
    Accept a natural-language cloud cost question, translate it to SQL via
    the OPTIC LLM agent, execute the query, and return a plain-English answer.
    """
    logger.info("NLP query received for tenant=%s", request.tenant_id)
    try:
        sql, answer = await ai_engine.translate_and_execute(
            tenant_id=request.tenant_id,
            query=request.query,
        )
        return NLPQueryResponse(
            tenant_id=request.tenant_id,
            query=request.query,
            sql=sql,
            answer=answer,
        )
    except Exception as exc:
        logger.exception("NLP query failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Query processing failed. Please try again.",
        )


@app.post("/api/v1/auto-terminate", tags=["ABACUS - Automation"])
async def auto_terminate(
    request: AutoTerminationRequest,
    background_tasks: BackgroundTasks,
) -> JSONResponse:
    """
    Evaluate a cloud resource using GNN + PPO RL and, if the model recommends
    termination, schedule the action as a background task.
    """
    logger.info(
        "Auto-termination request: tenant=%s resource=%s dry_run=%s",
        request.tenant_id, request.resource_id, request.dry_run,
    )
    background_tasks.add_task(
        ai_engine.evaluate_and_terminate,
        tenant_id=request.tenant_id,
        resource_id=request.resource_id,
        dry_run=request.dry_run,
    )
    return JSONResponse(
        content={
            "message": "Evaluation scheduled.",
            "tenant_id": request.tenant_id,
            "resource_id": request.resource_id,
            "dry_run": request.dry_run,
        },
        status_code=status.HTTP_202_ACCEPTED,
    )


@app.post("/api/v1/notify", tags=["Notifications"])
async def send_notification(request: NotificationRequest) -> JSONResponse:
    """Send a notification via the requested channel (Slack, Email, or SMS)."""
    try:
        result = await notification_service.send(
            channel=request.channel,
            recipient=request.recipient,
            subject=request.subject,
            body=request.body,
        )
        return JSONResponse(content={"success": True, "detail": result})
    except Exception as exc:
        logger.exception("Notification failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Notification delivery failed: {exc}",
        )
