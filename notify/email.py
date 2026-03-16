"""Email sender for monitor notifications via AgentMail API."""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def send_email(
    inbox_id: str,
    to: str,
    subject: str,
    body_text: str,
    body_html: str | None = None,
    *,
    api_key: str,
) -> bool:
    """Send an email via AgentMail.

    Best-effort: returns False on failure, never raises.
    """
    try:
        from agentmail import AgentMail

        client = AgentMail(api_key=api_key)
        kwargs = {
            "to": [to],
            "subject": subject,
            "text": body_text,
        }
        if body_html:
            kwargs["html"] = body_html

        client.inboxes.messages.send(inbox_id=inbox_id, **kwargs)
        logger.info("Email sent to %s: %s", to, subject)
        return True
    except Exception:
        logger.error("Failed to send email to %s: %s", to, subject, exc_info=True)
        return False


def send_summary_email(
    title: str,
    channel: str,
    url: str,
    summary_markdown: str,
    source_id: str,
    theme_names: list[str] | None = None,
) -> bool:
    """Send a YouTube monitor summary email.

    Loads AgentMail config from environment via Config. Returns False on failure.
    """
    from reading_app.config import Config

    config = Config()

    to = config.monitor_email_to
    if not to:
        logger.warning("MONITOR_EMAIL_TO not configured; skipping email")
        return False

    api_key = config.agentmail_api_key
    inbox_id = config.agentmail_inbox_id
    if not api_key or not inbox_id:
        logger.warning("AgentMail credentials not configured; skipping email")
        return False

    subject = f"[KB Monitor] Preview: {channel}: {title}"

    theme_line = ""
    if theme_names:
        theme_line = f"Themes: {', '.join(theme_names)}\n"

    body_text = (
        f"{title}\n"
        f"Channel: {channel}\n"
        f"URL: {url}\n"
        f"Source ID: {source_id}\n"
        f"{theme_line}"
        f"\n{'=' * 60}\n\n"
        f"{summary_markdown}\n"
        f"\n{'=' * 60}\n\n"
        f"To continue ingestion, run:\n"
        f"  /save_confirmed {source_id}\n"
    )

    return send_email(
        inbox_id=inbox_id,
        to=to,
        subject=subject,
        body_text=body_text,
        api_key=api_key,
    )


def send_digest_email(
    date: str,
    digest_markdown: str,
    digest_type: str = "daily",
) -> bool:
    """Send a daily or weekly digest email.

    Args:
        date: YYYY-MM-DD (daily) or YYYY-WNN (weekly).
        digest_markdown: Full markdown content.
        digest_type: "daily" or "weekly".

    Returns False on failure, never raises.
    """
    from reading_app.config import Config

    config = Config()
    to = config.monitor_email_to
    if not to:
        logger.warning("MONITOR_EMAIL_TO not configured; skipping digest email")
        return False

    api_key = config.agentmail_api_key
    inbox_id = config.agentmail_inbox_id
    if not api_key or not inbox_id:
        logger.warning("AgentMail credentials not configured; skipping digest email")
        return False

    if digest_type == "weekly":
        subject = f"[KB Digest] Weekly Roundup — {date}"
    else:
        subject = f"[KB Digest] Daily — {date}"

    return send_email(
        inbox_id=inbox_id,
        to=to,
        subject=subject,
        body_text=digest_markdown,
        api_key=api_key,
    )
