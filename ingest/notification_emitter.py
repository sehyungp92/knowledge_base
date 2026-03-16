"""Lightweight notification emitter — inserts into notifications table."""

from __future__ import annotations

import json
import logging

from reading_app import db

logger = logging.getLogger(__name__)


def emit_notification(
    type: str,
    entity_type: str,
    entity_id: str,
    title: str,
    detail: dict | None = None,
    source_id: str | None = None,
):
    """Insert a notification into the notifications table.

    Silently swallows errors — notifications are best-effort and must
    never abort the ingest pipeline.
    """
    try:
        with db.get_conn() as conn:
            conn.execute(
                """INSERT INTO notifications (type, entity_type, entity_id, title, detail, source_id)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (type, entity_type, entity_id, title,
                 json.dumps(detail or {}), source_id),
            )
            conn.commit()
        logger.info("Notification emitted: %s for %s/%s", type, entity_type, entity_id)
    except Exception:
        logger.exception("Failed to emit notification")


def emit_coverage_gap_notifications() -> list[dict]:
    """Run coverage gap scan and emit notifications for each gap found.

    Called from the heartbeat skill handler. Returns the list of gaps
    for inclusion in the heartbeat report.
    """
    try:
        from retrieval.lenses import scan_coverage_gaps

        db.ensure_pool()
        gaps = scan_coverage_gaps(db.get_conn)

        for gap in gaps:
            gap_type = gap.get("gap_type", "unknown")
            theme = gap.get("theme", "?")
            theme_id = gap.get("theme_id", "")
            detail_text = gap.get("detail", "")

            if gap_type == "over_optimistic":
                title = f"Over-optimistic coverage: {theme}"
            elif gap_type == "blind_spot_bottleneck":
                title = f"Blind-spot bottleneck: {theme}"
            else:
                title = f"Coverage gap: {theme}"

            emit_notification(
                type="coverage_gap",
                entity_type="theme",
                entity_id=theme_id,
                title=title,
                detail={"gap_type": gap_type, "detail": detail_text, "theme": theme},
            )

        if gaps:
            logger.info("Emitted %d coverage gap notifications", len(gaps))
        return gaps
    except Exception:
        logger.exception("Coverage gap scan failed")
        return []
