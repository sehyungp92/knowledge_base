"""Discord DM sender for monitor notifications."""

from __future__ import annotations

import logging

import httpx

from notify.text import split_text_chunks

logger = logging.getLogger(__name__)

_DISCORD_API_BASE = "https://discord.com/api/v10"
_MAX_DISCORD_LENGTH = 2000


def send_discord_message(text: str) -> bool:
    """Send a text message to the configured Discord DM recipient."""
    from reading_app.config import Config

    config = Config()
    token = config.discord_bot_token
    user_id = config.discord_allowed_user_id

    if not token or not user_id:
        logger.debug("Discord not configured; skipping message")
        return False

    chunks = split_text_chunks(text, _MAX_DISCORD_LENGTH)
    if not chunks:
        return False

    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
    }

    try:
        dm_resp = httpx.post(
            f"{_DISCORD_API_BASE}/users/@me/channels",
            headers=headers,
            json={"recipient_id": user_id},
            timeout=15,
        )
        if dm_resp.status_code not in (200, 201):
            logger.warning("Discord DM open returned %d: %s", dm_resp.status_code, dm_resp.text[:200])
            return False

        channel_id = dm_resp.json().get("id")
        if not channel_id:
            logger.warning("Discord DM open returned no channel id")
            return False

        for chunk in chunks:
            msg_resp = httpx.post(
                f"{_DISCORD_API_BASE}/channels/{channel_id}/messages",
                headers=headers,
                json={"content": chunk},
                timeout=15,
            )
            if msg_resp.status_code not in (200, 201):
                logger.warning(
                    "Discord send returned %d: %s",
                    msg_resp.status_code,
                    msg_resp.text[:200],
                )
                return False

        return True
    except Exception:
        logger.error("Failed to send Discord message", exc_info=True)
        return False
