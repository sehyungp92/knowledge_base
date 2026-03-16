"""Beliefs API router -- tracked positions with confidence and history."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from reading_app import db

router = APIRouter(prefix="/api/beliefs", tags=["beliefs"])


@router.get("/")
def list_beliefs(
    status: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List beliefs with optional status filter, enriched with theme name."""
    conditions: list[str] = []
    params: list = []

    if status:
        conditions.append("b.status = %s")
        params.append(status)

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    params.extend([limit, offset])

    with db.get_conn() as conn:
        rows = conn.execute(
            f"""SELECT b.*, t.name AS theme_name
                FROM beliefs b
                LEFT JOIN themes t ON b.domain_theme_id = t.id
                {where}
                ORDER BY b.last_updated DESC
                LIMIT %s OFFSET %s""",
            params,
        ).fetchall()

    return rows


# ── Analytics endpoints (MUST be before /{belief_id} catch-all) ──────


@router.get("/analytics/stale")
def stale_beliefs(velocity_threshold: float = Query(0.3)):
    """Beliefs needing review based on theme velocity."""
    return db.get_stale_beliefs(velocity_threshold)


@router.get("/analytics/unchallenged")
def unchallenged_beliefs(min_confidence: float = Query(0.8)):
    """High-confidence beliefs that have never been challenged."""
    return db.get_unchallenged_beliefs(min_confidence)


@router.get("/analytics/low-confidence")
def low_confidence_beliefs(threshold: float = Query(0.5)):
    """Beliefs with confidence below the threshold."""
    return db.get_low_confidence_beliefs(threshold)


@router.get("/analytics/consistency")
def consistency_check(theme_id: str | None = Query(None)):
    """Potentially contradicting belief pairs within themes."""
    return db.get_belief_pairs_for_consistency(theme_id)


# ── Individual belief endpoints ──────────────────────────────────────


@router.get("/{belief_id}")
def get_belief(belief_id: str):
    """Get a single belief with theme name."""
    with db.get_conn() as conn:
        row = conn.execute(
            """SELECT b.*, t.name AS theme_name
               FROM beliefs b
               LEFT JOIN themes t ON b.domain_theme_id = t.id
               WHERE b.id = %s""",
            (belief_id,),
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail=f"Belief '{belief_id}' not found")
    return row


@router.get("/{belief_id}/timeline")
def belief_timeline(belief_id: str):
    """Get a belief together with its challenge log entries."""
    with db.get_conn() as conn:
        belief = conn.execute(
            """SELECT b.*, t.name AS theme_name
               FROM beliefs b
               LEFT JOIN themes t ON b.domain_theme_id = t.id
               WHERE b.id = %s""",
            (belief_id,),
        ).fetchone()

        if not belief:
            raise HTTPException(status_code=404, detail=f"Belief '{belief_id}' not found")

        challenges = conn.execute(
            """SELECT * FROM challenge_log
               WHERE belief_id = %s
               ORDER BY created_at DESC""",
            (belief_id,),
        ).fetchall()

    return {"belief": belief, "challenges": challenges}
