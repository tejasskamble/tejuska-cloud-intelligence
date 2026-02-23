"""
notifications.py
================
TEJUSKA Cloud Intelligence
Unified notification service: Slack, Email (SMTP), and Twilio SMS.
All configuration is loaded from environment variables.
"""

import os
import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from slack_sdk.webhook import WebhookClient
from slack_sdk.errors import SlackApiError
from twilio.rest import Client as TwilioClient

logger = logging.getLogger("tejuska.notifications")


class NotificationService:
    """
    Provides send() as a single dispatch point.
    Channel must be one of: 'slack', 'email', 'sms'.
    """

    def __init__(self) -> None:
        # Slack
        self._slack_webhook_url: str = os.environ.get("SLACK_WEBHOOK_URL", "")

        # SMTP / Email
        self._smtp_host: str = os.environ.get("SMTP_HOST", "smtp.gmail.com")
        self._smtp_port: int = int(os.environ.get("SMTP_PORT", "587"))
        self._smtp_user: str = os.environ.get("SMTP_USER", "")
        self._smtp_password: str = os.environ.get("SMTP_PASSWORD", "")

        # Twilio SMS
        self._twilio_account_sid: str = os.environ.get("TWILIO_ACCOUNT_SID", "")
        self._twilio_auth_token: str = os.environ.get("TWILIO_AUTH_TOKEN", "")
        self._twilio_from_number: str = os.environ.get("TWILIO_FROM_NUMBER", "")

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    async def send(
        self,
        channel: str,
        recipient: str,
        body: str,
        subject: Optional[str] = None,
    ) -> str:
        """
        Dispatch a notification to the specified channel.

        Parameters
        ----------
        channel   : 'slack' | 'email' | 'sms'
        recipient : Slack webhook URL override, email address, or phone number.
        body      : Notification body text.
        subject   : Subject line (required for email; ignored for Slack/SMS).

        Returns
        -------
        str: Confirmation message.
        """
        channel = channel.lower().strip()
        if channel == "slack":
            return self._send_slack(body=body)
        if channel == "email":
            return self._send_email(
                to_address=recipient,
                subject=subject or "TEJUSKA Cloud Intelligence Alert",
                body=body,
            )
        if channel == "sms":
            return self._send_sms(to_number=recipient, body=body)
        raise ValueError(f"Unsupported notification channel: '{channel}'")

    # ------------------------------------------------------------------
    # Slack
    # ------------------------------------------------------------------

    def _send_slack(self, body: str) -> str:
        """Post a message to the configured Slack webhook."""
        if not self._slack_webhook_url:
            raise EnvironmentError("SLACK_WEBHOOK_URL environment variable is not set.")
        client = WebhookClient(url=self._slack_webhook_url)
        response = client.send(text=body)
        if response.status_code != 200:
            raise RuntimeError(
                f"Slack webhook returned HTTP {response.status_code}: {response.body}"
            )
        logger.info("Slack notification delivered successfully.")
        return "Slack notification delivered."

    # ------------------------------------------------------------------
    # Email via SMTP
    # ------------------------------------------------------------------

    def _send_email(self, to_address: str, subject: str, body: str) -> str:
        """Send a plain-text email via STARTTLS SMTP."""
        if not self._smtp_user or not self._smtp_password:
            raise EnvironmentError("SMTP_USER or SMTP_PASSWORD environment variable is not set.")

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self._smtp_user
        message["To"] = to_address
        message.attach(MIMEText(body, "plain", "utf-8"))

        context = ssl.create_default_context()
        with smtplib.SMTP(self._smtp_host, self._smtp_port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.login(self._smtp_user, self._smtp_password)
            server.sendmail(self._smtp_user, to_address, message.as_string())

        logger.info("Email notification delivered to %s.", to_address)
        return f"Email delivered to {to_address}."

    # ------------------------------------------------------------------
    # SMS via Twilio
    # ------------------------------------------------------------------

    def _send_sms(self, to_number: str, body: str) -> str:
        """Send an SMS using the Twilio REST API."""
        if not self._twilio_account_sid or not self._twilio_auth_token:
            raise EnvironmentError("Twilio credentials are not set in environment variables.")
        if not self._twilio_from_number:
            raise EnvironmentError("TWILIO_FROM_NUMBER environment variable is not set.")

        client = TwilioClient(self._twilio_account_sid, self._twilio_auth_token)
        msg = client.messages.create(
            body=body,
            from_=self._twilio_from_number,
            to=to_number,
        )
        logger.info("SMS delivered to %s. SID: %s", to_number, msg.sid)
        return f"SMS delivered to {to_number}. SID: {msg.sid}"
