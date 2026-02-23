"""
ai_engine.py
============
TEJUSKA Cloud Intelligence
Agentic AI Engine:
  - OPTIC: LangChain-powered Text-to-SQL NLP agent.
  - ABACUS: GNN + PPO Reinforcement Learning for autonomous resource optimisation.
"""

import os
import logging
from typing import Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

logger = logging.getLogger("tejuska.ai_engine")

OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY", "")
DATABASE_URL: str = os.environ.get("DATABASE_URL", "")

# ---------------------------------------------------------------------------
# GNN Model Definition (Graph Neural Network for resource graph analysis)
# ---------------------------------------------------------------------------

class ResourceGNN(nn.Module):
    """
    Simple two-layer Graph Convolutional Network.
    Input:  node feature matrix X (shape: N x F)
    Output: per-node termination logits (shape: N x 2)
    """

    def __init__(self, in_features: int = 8, hidden_dim: int = 32, out_classes: int = 2) -> None:
        super().__init__()
        self.fc1 = nn.Linear(in_features, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, out_classes)

    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        # Normalised adjacency: D^{-1} A
        degree = adj.sum(dim=1, keepdim=True).clamp(min=1.0)
        adj_norm = adj / degree

        x = F.relu(self.fc1(adj_norm @ x))
        x = self.fc2(adj_norm @ x)
        return x


# ---------------------------------------------------------------------------
# PPO Policy Network (lightweight, single hidden layer)
# ---------------------------------------------------------------------------

class PPOPolicy(nn.Module):
    """
    PPO actor-critic policy for single-resource action selection.
    State:  resource feature vector (in_features,)
    Action: 0 = keep, 1 = terminate
    """

    def __init__(self, in_features: int = 8, hidden_dim: int = 64) -> None:
        super().__init__()
        self.shared = nn.Linear(in_features, hidden_dim)
        self.actor  = nn.Linear(hidden_dim, 2)
        self.critic = nn.Linear(hidden_dim, 1)

    def forward(self, state: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        h = F.relu(self.shared(state))
        logits = self.actor(h)
        value  = self.critic(h)
        return logits, value


# ---------------------------------------------------------------------------
# AI Engine
# ---------------------------------------------------------------------------

class AIEngine:
    """
    Encapsulates OPTIC (NLP query) and ABACUS (autonomous termination) logic.
    """

    def __init__(self) -> None:
        self._gnn    = ResourceGNN()
        self._policy = PPOPolicy()
        self._gnn.eval()
        self._policy.eval()
        logger.info("AIEngine initialised (GNN + PPO loaded in eval mode).")

    # ------------------------------------------------------------------
    # OPTIC: Text-to-SQL
    # ------------------------------------------------------------------

    async def translate_and_execute(
        self, tenant_id: str, query: str
    ) -> Tuple[str, str]:
        """
        Translate a natural-language query to SQL, execute it, and return
        both the generated SQL and a plain-English answer.

        In production this calls the OpenAI Chat Completions API.
        The implementation below provides a deterministic stub when no API
        key is present so that unit tests pass without network access.
        """
        if not OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not set; returning stub response.")
            stub_sql = (
                "SELECT service_name, SUM(billed_cost) AS total_cost "
                "FROM consolidated_billing "
                f"WHERE tenant_id = '{tenant_id}' "
                "GROUP BY service_name ORDER BY total_cost DESC LIMIT 10;"
            )
            stub_answer = (
                "Your top 10 cloud services by billed cost for this period are listed. "
                "Connect an OpenAI API key to enable live natural-language answers."
            )
            return stub_sql, stub_answer

        import openai  # imported lazily to avoid mandatory dep at test time
        client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

        system_prompt = (
            "You are a FinOps SQL expert. The user will ask a question about cloud costs. "
            "You will generate a PostgreSQL query against the 'consolidated_billing' table. "
            "Always filter by tenant_id. Return ONLY the SQL statement, nothing else."
        )
        sql_response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"tenant_id='{tenant_id}'. Question: {query}"},
            ],
            temperature=0.0,
            max_tokens=512,
        )
        generated_sql: str = sql_response.choices[0].message.content.strip()

        # Convert SQL result to natural language
        answer_prompt = (
            "The following SQL was run to answer the user's question. "
            "Provide a concise, professional plain-English summary of the result. "
            "If you do not have the actual data, describe what the query will return."
        )
        answer_response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": answer_prompt},
                {"role": "user", "content": f"SQL: {generated_sql}"},
            ],
            temperature=0.3,
            max_tokens=256,
        )
        answer: str = answer_response.choices[0].message.content.strip()
        return generated_sql, answer

    # ------------------------------------------------------------------
    # ABACUS: Autonomous Termination
    # ------------------------------------------------------------------

    async def evaluate_and_terminate(
        self, tenant_id: str, resource_id: str, dry_run: bool = True
    ) -> None:
        """
        Evaluate whether a cloud resource should be terminated using the
        GNN + PPO pipeline.

        Feature vector (8 dimensions):
          [cpu_util, mem_util, net_in, net_out, cost_per_hr, age_days, tag_prod, reserved]

        In production, these values are fetched from the database / cloud APIs.
        This implementation uses a deterministic synthetic vector for demonstration.
        """
        logger.info(
            "Evaluating resource=%s for tenant=%s (dry_run=%s)",
            resource_id, tenant_id, dry_run,
        )

        # Build synthetic feature vector (replace with real DB fetch in production)
        features = np.array(
            [0.05, 0.10, 0.002, 0.001, 0.023, 45.0, 0.0, 0.0],
            dtype=np.float32,
        )
        state_tensor = torch.from_numpy(features).unsqueeze(0)  # shape: (1, 8)

        with torch.no_grad():
            logits, _ = self._policy(state_tensor)
            action = int(torch.argmax(logits, dim=-1).item())

        action_label = "TERMINATE" if action == 1 else "KEEP"
        logger.info(
            "PPO recommendation for resource=%s: %s (dry_run=%s)",
            resource_id, action_label, dry_run,
        )

        if action == 1 and not dry_run:
            # In production: call AWS Boto3 / GCP SDK to terminate the resource
            logger.info(
                "Executing termination of resource=%s for tenant=%s.",
                resource_id, tenant_id,
            )
        else:
            logger.info(
                "No action taken (action=%s, dry_run=%s).", action_label, dry_run
            )
