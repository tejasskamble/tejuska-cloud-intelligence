"""
api_client.py
=============
TEJUSKA Cloud Intelligence
Thin HTTP client for communicating with the FastAPI backend.
"""

import requests
from typing import Any, Dict, Optional


class TejuskaAPIClient:
    """Synchronous HTTP client wrapping the TEJUSKA FastAPI backend."""

    def __init__(self, base_url: str, timeout: int = 60) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout  = timeout

    def health(self) -> Dict[str, Any]:
        """Check backend health."""
        response = requests.get(f"{self._base_url}/health", timeout=self._timeout)
        response.raise_for_status()
        return response.json()

    def nlp_query(self, tenant_id: str, query: str) -> Dict[str, Any]:
        """Submit a natural-language cost query to OPTIC."""
        response = requests.post(
            f"{self._base_url}/api/v1/query",
            json={"tenant_id": tenant_id, "query": query},
            timeout=self._timeout,
        )
        response.raise_for_status()
        return response.json()

    def auto_terminate(
        self, tenant_id: str, resource_id: str, dry_run: bool = True
    ) -> Dict[str, Any]:
        """Trigger ABACUS evaluation for a cloud resource."""
        response = requests.post(
            f"{self._base_url}/api/v1/auto-terminate",
            json={
                "tenant_id":   tenant_id,
                "resource_id": resource_id,
                "dry_run":     dry_run,
            },
            timeout=self._timeout,
        )
        response.raise_for_status()
        return response.json()

    def send_notification(
        self,
        tenant_id: str,
        channel: str,
        recipient: str,
        body: str,
        subject: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Dispatch a notification via the backend service."""
        response = requests.post(
            f"{self._base_url}/api/v1/notify",
            json={
                "tenant_id": tenant_id,
                "channel":   channel,
                "recipient": recipient,
                "subject":   subject,
                "body":      body,
            },
            timeout=self._timeout,
        )
        response.raise_for_status()
        return response.json()
