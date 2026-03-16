"""Shared helpers for tracking pipeline and post-processing step status."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


def _serialize_result(result: Any) -> str:
    return json.dumps(result or {}, default=str)


def ensure_step_rows(source_id: str, steps: list[str], get_conn_fn) -> bool:
    """Ensure status rows exist for each tracked step."""
    try:
        with get_conn_fn() as conn:
            for step in steps:
                conn.execute(
                    """INSERT INTO post_processing_status (source_id, step, status)
                       VALUES (%s, %s, 'pending')
                       ON CONFLICT (source_id, step) DO NOTHING""",
                    (source_id, step),
                )
            conn.commit()
        return True
    except Exception:
        logger.debug("Failed to ensure step rows for %s", source_id, exc_info=True)
        return False


def load_step_status(source_id: str, get_conn_fn) -> dict[str, dict]:
    """Load step status rows for a source."""
    try:
        with get_conn_fn() as conn:
            rows = conn.execute(
                """SELECT step, status, started_at, completed_at, error, result, attempt_count
                   FROM post_processing_status
                   WHERE source_id = %s""",
                (source_id,),
            ).fetchall()
        return {row["step"]: dict(row) for row in rows}
    except Exception:
        logger.debug("Failed to load step status for %s", source_id, exc_info=True)
        return {}


def mark_step_running(source_id: str, step: str, get_conn_fn) -> None:
    """Mark a step as running and increment its attempt count."""
    now = datetime.now(timezone.utc)
    try:
        with get_conn_fn() as conn:
            conn.execute(
                """INSERT INTO post_processing_status
                       (source_id, step, status, started_at, completed_at, result, error, attempt_count)
                   VALUES (%s, %s, 'running', %s, NULL, '{}'::jsonb, NULL, 1)
                   ON CONFLICT (source_id, step) DO UPDATE SET
                       status = 'running',
                       started_at = EXCLUDED.started_at,
                       completed_at = NULL,
                       result = '{}'::jsonb,
                       error = NULL,
                       attempt_count = post_processing_status.attempt_count + 1""",
                (source_id, step, now),
            )
            conn.commit()
    except Exception:
        logger.debug("Failed to mark %s/%s running", source_id, step, exc_info=True)


def mark_step_completed(
    source_id: str,
    step: str,
    get_conn_fn,
    *,
    result: Any | None = None,
) -> None:
    """Mark a step as completed with structured result details."""
    now = datetime.now(timezone.utc)
    try:
        with get_conn_fn() as conn:
            conn.execute(
                """INSERT INTO post_processing_status
                       (source_id, step, status, completed_at, result, error)
                   VALUES (%s, %s, 'completed', %s, %s, NULL)
                   ON CONFLICT (source_id, step) DO UPDATE SET
                       status = 'completed',
                       completed_at = EXCLUDED.completed_at,
                       result = EXCLUDED.result,
                       error = NULL""",
                (source_id, step, now, _serialize_result(result)),
            )
            conn.commit()
    except Exception:
        logger.debug("Failed to mark %s/%s completed", source_id, step, exc_info=True)


def mark_step_failed(
    source_id: str,
    step: str,
    error: str,
    get_conn_fn,
    *,
    result: Any | None = None,
) -> None:
    """Mark a step as failed with a short error message."""
    now = datetime.now(timezone.utc)
    error_message = (error or "unknown error")[:500]
    try:
        with get_conn_fn() as conn:
            conn.execute(
                """INSERT INTO post_processing_status
                       (source_id, step, status, completed_at, result, error)
                   VALUES (%s, %s, 'failed', %s, %s, %s)
                   ON CONFLICT (source_id, step) DO UPDATE SET
                       status = 'failed',
                       completed_at = EXCLUDED.completed_at,
                       result = EXCLUDED.result,
                       error = EXCLUDED.error""",
                (source_id, step, now, _serialize_result(result), error_message),
            )
            conn.commit()
    except Exception:
        logger.debug("Failed to mark %s/%s failed", source_id, step, exc_info=True)
