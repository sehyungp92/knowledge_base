"""Notifications API router -- list, mark-read, SSE stream."""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from reading_app import db

router = APIRouter(prefix="/api/notifications", tags=["notifications"])


@router.get("/")
def list_notifications(
    unread: bool | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List notifications with optional unread filter."""
    conditions: list[str] = []
    params: list = []

    if unread is True:
        conditions.append("read = FALSE")
    elif unread is False:
        conditions.append("read = TRUE")

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    params.extend([limit, offset])

    with db.get_conn() as conn:
        rows = conn.execute(
            f"""SELECT * FROM notifications
                {where}
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s""",
            params,
        ).fetchall()

    return rows


@router.patch("/{notification_id}")
def mark_read(notification_id: int):
    """Mark a notification as read."""
    with db.get_conn() as conn:
        row = conn.execute(
            """UPDATE notifications
               SET read = TRUE
               WHERE id = %s
               RETURNING *""",
            (notification_id,),
        ).fetchone()
        conn.commit()

    if not row:
        raise HTTPException(status_code=404, detail=f"Notification {notification_id} not found")
    return row


@router.get("/stream")
async def notification_stream():
    """SSE endpoint -- poll for new notifications every 5 seconds."""
    try:
        from sse_starlette.sse import EventSourceResponse
    except ImportError:
        raise HTTPException(
            status_code=501,
            detail="sse_starlette is not installed; SSE streaming unavailable",
        )

    async def event_generator():
        last_check = datetime.now(timezone.utc)
        while True:
            await asyncio.sleep(5)
            try:
                with db.get_conn() as conn:
                    rows = conn.execute(
                        """SELECT * FROM notifications
                           WHERE created_at > %s AND read = FALSE
                           ORDER BY created_at ASC""",
                        (last_check,),
                    ).fetchall()
                if rows:
                    last_check = datetime.now(timezone.utc)
                    for row in rows:
                        yield {
                            "event": "notification",
                            "data": json.dumps(row, default=str),
                        }
            except Exception:
                yield {"event": "error", "data": "poll_failed"}

    return EventSourceResponse(event_generator())
