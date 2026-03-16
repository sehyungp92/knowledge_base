"""Optional PinchTab fallback for JS-rendered pages.

PinchTab is a local browser automation service that can render JS-heavy pages
and extract their text content. This module provides a thin wrapper around
its HTTP API, following the same pattern as stealth_fetch.py.

If PinchTab is not running, all functions degrade gracefully.
"""

from __future__ import annotations

import logging
import os
import time

import httpx

logger = logging.getLogger(__name__)

PINCHTAB_BASE = os.environ.get("PINCHTAB_BASE_URL", "http://localhost:9867")

_available_cache: tuple[bool, float] | None = None
_CACHE_TTL = 60.0


class PinchTabUnavailable(Exception):
    """Raised when PinchTab service is not running."""


def is_pinchtab_available() -> bool:
    """Check if PinchTab is running. Result cached for 60s."""
    global _available_cache
    now = time.monotonic()
    if _available_cache is not None:
        cached_result, cached_at = _available_cache
        if now - cached_at < _CACHE_TTL:
            return cached_result

    try:
        resp = httpx.get(f"{PINCHTAB_BASE}/health", timeout=5)
        available = resp.status_code == 200
    except Exception:
        available = False

    _available_cache = (available, now)
    return available


def fetch_text_pinchtab(url: str, timeout: int = 60) -> tuple[str, str]:
    """Fetch page text via PinchTab browser automation.

    Args:
        url: The URL to fetch and extract text from.
        timeout: Navigation timeout in seconds.

    Returns:
        Tuple of (text, title).

    Raises:
        PinchTabUnavailable: If PinchTab is not running.
        ValueError: If no text could be extracted.
        httpx.HTTPStatusError: On HTTP errors from PinchTab API.
    """
    if not is_pinchtab_available():
        raise PinchTabUnavailable("PinchTab service is not running")

    # Navigate to the URL
    nav_resp = httpx.post(
        f"{PINCHTAB_BASE}/navigate",
        json={"url": url, "blockAds": True, "timeout": timeout},
        timeout=timeout + 10,
    )
    nav_resp.raise_for_status()
    nav_data = nav_resp.json()
    title = nav_data.get("title", "")

    # Extract text content
    text_resp = httpx.get(f"{PINCHTAB_BASE}/text", timeout=30)
    text_resp.raise_for_status()
    text_data = text_resp.json()

    text = text_data.get("text", "")
    if not title:
        title = text_data.get("title", "")

    if not text:
        raise ValueError(f"PinchTab returned empty text for {url}")

    return text, title
