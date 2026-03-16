"""Shared HTTP retry utility with exponential backoff."""

from __future__ import annotations

import logging
import time
from typing import Callable, TypeVar

import httpx

logger = logging.getLogger(__name__)

T = TypeVar("T")

# Exceptions that are worth retrying
RETRYABLE_EXCEPTIONS = (
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.PoolTimeout,
)

# HTTP status codes that are worth retrying
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def with_retry(
    fn: Callable[[], T],
    *,
    max_attempts: int = 3,
    base_delay: float = 2.0,
    max_delay: float = 30.0,
    label: str = "",
    retryable_exceptions: tuple[type[Exception], ...] | None = None,
) -> T:
    """Call ``fn()`` with exponential backoff on retryable errors.

    Retries on connection errors, timeouts, and HTTP 429/5xx responses.
    Pass ``retryable_exceptions`` to also retry on additional exception types
    (e.g. ``(RuntimeError,)`` for CLI-based callers).
    Respects ``Retry-After`` header when present.

    Raises the last exception after all attempts are exhausted.
    """
    all_retryable = RETRYABLE_EXCEPTIONS + (retryable_exceptions or ())
    last_exc: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except all_retryable as exc:
            last_exc = exc
            if attempt == max_attempts:
                break
            delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            logger.warning(
                "%s: %s on attempt %d/%d, retrying in %.1fs",
                label or "with_retry", exc, attempt, max_attempts, delay,
            )
            time.sleep(delay)
        except httpx.HTTPStatusError as exc:
            last_exc = exc
            if exc.response.status_code not in RETRYABLE_STATUS_CODES:
                raise
            if attempt == max_attempts:
                break
            # Respect Retry-After header
            retry_after = exc.response.headers.get("Retry-After")
            if retry_after:
                try:
                    delay = min(float(retry_after), max_delay)
                except ValueError:
                    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            else:
                delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
            logger.warning(
                "%s: HTTP %d on attempt %d/%d, retrying in %.1fs",
                label or "with_retry", exc.response.status_code,
                attempt, max_attempts, delay,
            )
            time.sleep(delay)

    raise last_exc  # type: ignore[misc]
