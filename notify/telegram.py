"""Telegram message sender for digest notifications."""

from __future__ import annotations

import logging

import httpx

from notify.text import split_text_chunks

logger = logging.getLogger(__name__)

_MAX_TELEGRAM_LENGTH = 4096


def send_telegram_messages(messages: list[str], *, parse_mode: str | None = "Markdown") -> bool:
    """Send one or more messages to the configured Telegram chat.

    Best-effort: returns False on failure, never raises.
    """
    from reading_app.config import Config

    config = Config()
    token = config.telegram_bot_token
    chat_id = config.telegram_allowed_chat_id

    if not token or not chat_id:
        logger.debug("Telegram not configured; skipping message")
        return False

    if not messages:
        return False

    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        for message in messages:
            payload = {"chat_id": chat_id, "text": message}
            if parse_mode:
                payload["parse_mode"] = parse_mode
            resp = httpx.post(url, json=payload, timeout=15)
            if resp.status_code != 200:
                logger.warning("Telegram send returned %d: %s", resp.status_code, resp.text[:200])
                return False
        return True
    except Exception:
        logger.error("Failed to send Telegram message", exc_info=True)
        return False


def send_telegram_message(text: str, *, parse_mode: str | None = "Markdown") -> bool:
    """Send a message to the configured Telegram chat.

    Best-effort: returns False on failure, never raises.
    """
    return send_telegram_messages(
        split_text_chunks(text, _MAX_TELEGRAM_LENGTH),
        parse_mode=parse_mode,
    )
