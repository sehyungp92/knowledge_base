"""Predictions (anticipations) API router -- tracking, calibration, pressure."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from reading_app import db
from retrieval import landscape

router = APIRouter(prefix="/api/predictions", tags=["predictions"])


@router.get("/")
def list_predictions(
    sort: str = Query("evidence", description="Sort by: evidence, confidence, timeline"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List anticipations with evidence counts."""
    order_map = {
        "evidence": "evidence_count DESC",
        "confidence": "a.confidence DESC",
        "timeline": "a.timeline ASC NULLS LAST",
    }
    order_clause = order_map.get(sort, "evidence_count DESC")

    with db.get_conn() as conn:
        rows = conn.execute(
            f"""SELECT a.*, t.name AS theme_name,
                   jsonb_array_length(COALESCE(a.status_evidence, '[]'::jsonb)) AS evidence_count
               FROM anticipations a
               JOIN themes t ON a.theme_id = t.id
               ORDER BY {order_clause}
               LIMIT %s OFFSET %s""",
            (limit, offset),
        ).fetchall()

    # Resolve source titles from based_on and status_evidence
    all_source_ids: set[str] = set()
    for row in rows:
        based_on = row.get("based_on")
        if isinstance(based_on, list):
            for item in based_on:
                sid = item.get("source_id") if isinstance(item, dict) else item if isinstance(item, str) else None
                if sid:
                    all_source_ids.add(sid)
        evidence = row.get("status_evidence")
        if isinstance(evidence, list):
            for item in evidence:
                if isinstance(item, dict) and item.get("source_id"):
                    all_source_ids.add(item["source_id"])

    source_lookup: dict[str, str] = {}
    if all_source_ids:
        with db.get_conn() as conn:
            srows = conn.execute(
                "SELECT id, title FROM sources WHERE id = ANY(%s)",
                (list(all_source_ids),),
            ).fetchall()
            source_lookup = {r["id"]: r["title"] for r in srows}

    # Inject resolved titles
    for row in rows:
        row["source_lookup"] = source_lookup

    return rows


class StatusUpdate(BaseModel):
    status: str


VALID_STATUSES = {"open", "partially_confirmed", "confirmed", "disconfirmed", "invalidated", "expired"}


@router.patch("/{anticipation_id}/status")
def update_status(anticipation_id: str, body: StatusUpdate):
    """Manually update an anticipation's status."""
    if body.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {', '.join(sorted(VALID_STATUSES))}")
    result = db.update_anticipation_status(anticipation_id, body.status)
    if not result:
        raise HTTPException(status_code=404, detail="Anticipation not found")
    return result


@router.get("/calibration")
def calibration():
    """Group anticipations by confidence bucket, count confirmed vs invalidated."""
    with db.get_conn() as conn:
        rows = conn.execute(
            """SELECT
                  FLOOR(confidence * 10) / 10 AS bucket,
                  COUNT(*) AS total,
                  COUNT(*) FILTER (WHERE status = 'confirmed') AS confirmed,
                  COUNT(*) FILTER (WHERE status = 'invalidated') AS invalidated,
                  COUNT(*) FILTER (WHERE status = 'open') AS open
               FROM anticipations
               GROUP BY bucket
               ORDER BY bucket"""
        ).fetchall()

    return rows


@router.get("/pressure")
def pressure():
    """Anticipations with accumulated evidence -- signals that need attention."""
    return landscape.get_anticipations_with_evidence()


@router.get("/expired")
def expired(min_age_days: int = Query(60, ge=1)):
    """Untested anticipations older than min_age_days."""
    return landscape.get_untested_anticipations(min_age_days)
