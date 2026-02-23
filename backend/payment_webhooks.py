"""
payment_webhooks.py
===================
TEJUSKA Cloud Intelligence
Stripe and Razorpay payment webhook handlers.
"""

import os
import logging

import stripe
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse

logger = logging.getLogger("tejuska.payments")

router = APIRouter()

STRIPE_SECRET_KEY: str     = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET: str = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
RAZORPAY_KEY_ID: str       = os.environ.get("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET: str   = os.environ.get("RAZORPAY_KEY_SECRET", "")

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY


# ---------------------------------------------------------------------------
# Stripe Webhook
# ---------------------------------------------------------------------------

@router.post("/stripe", tags=["Payments"])
async def stripe_webhook(request: Request) -> JSONResponse:
    """
    Handle Stripe lifecycle events:
      - checkout.session.completed
      - customer.subscription.updated
      - customer.subscription.deleted
    """
    payload: bytes = await request.body()
    sig_header: str = request.headers.get("stripe-signature", "")

    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="STRIPE_WEBHOOK_SECRET is not configured.",
        )

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=STRIPE_WEBHOOK_SECRET,
        )
    except stripe.error.SignatureVerificationError as exc:
        logger.warning("Stripe signature verification failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Stripe signature.",
        )

    event_type: str = event["type"]
    data_object = event["data"]["object"]

    if event_type == "checkout.session.completed":
        tenant_id = data_object.get("metadata", {}).get("tenant_id")
        logger.info("Checkout completed for tenant=%s", tenant_id)
        # TODO: Update subscriptions table to plan='enterprise'

    elif event_type == "customer.subscription.updated":
        subscription_id = data_object.get("id")
        new_status      = data_object.get("status")
        logger.info(
            "Subscription %s updated. New status: %s", subscription_id, new_status
        )
        # TODO: Reflect subscription status change in DB

    elif event_type == "customer.subscription.deleted":
        subscription_id = data_object.get("id")
        logger.info("Subscription %s cancelled.", subscription_id)
        # TODO: Downgrade tenant to free plan in DB

    else:
        logger.debug("Unhandled Stripe event type: %s", event_type)

    return JSONResponse(content={"received": True})


# ---------------------------------------------------------------------------
# Razorpay Webhook
# ---------------------------------------------------------------------------

@router.post("/razorpay", tags=["Payments"])
async def razorpay_webhook(request: Request) -> JSONResponse:
    """
    Handle Razorpay payment events:
      - payment.captured
      - subscription.cancelled
    """
    import hmac
    import hashlib

    payload: bytes = await request.body()
    received_signature: str = request.headers.get("x-razorpay-signature", "")

    if not RAZORPAY_KEY_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="RAZORPAY_KEY_SECRET is not configured.",
        )

    expected_signature = hmac.new(
        key=RAZORPAY_KEY_SECRET.encode("utf-8"),
        msg=payload,
        digestmod=hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, received_signature):
        logger.warning("Razorpay signature verification failed.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Razorpay signature.",
        )

    import json
    body = json.loads(payload)
    event_type: str = body.get("event", "")

    if event_type == "payment.captured":
        payment_id = body.get("payload", {}).get("payment", {}).get("entity", {}).get("id")
        logger.info("Razorpay payment captured. Payment ID: %s", payment_id)
        # TODO: Update subscription plan in DB

    elif event_type == "subscription.cancelled":
        subscription_id = (
            body.get("payload", {})
            .get("subscription", {})
            .get("entity", {})
            .get("id")
        )
        logger.info("Razorpay subscription cancelled. ID: %s", subscription_id)
        # TODO: Downgrade tenant to free plan in DB

    else:
        logger.debug("Unhandled Razorpay event: %s", event_type)

    return JSONResponse(content={"received": True})
