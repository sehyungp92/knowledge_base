"""Concepts API router -- browse and explore extracted concepts."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from reading_app import db

router = APIRouter(prefix="/api/concepts", tags=["concepts"])


@router.get("/")
def list_concepts(
    concept_type: str | None = Query(None),
    q: str | None = Query(None, description="Search by name"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List concepts with source counts, optionally filtered by type or name."""
    conditions: list[str] = []
    params: list = []

    if concept_type:
        conditions.append("c.concept_type = %s")
        params.append(concept_type)

    if q:
        conditions.append("(c.canonical_name ILIKE %s OR c.description ILIKE %s)")
        escaped = q.replace("%", r"\%").replace("_", r"\_")
        pattern = f"%{escaped}%"
        params.extend([pattern, pattern])

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    params.extend([limit, offset])

    with db.get_conn() as conn:
        rows = conn.execute(
            f"""SELECT c.id, c.canonical_name, c.concept_type, c.description, c.aliases,
                       COUNT(sc.source_id) AS source_count
                FROM concepts c
                LEFT JOIN source_concepts sc ON sc.concept_id = c.id
                {where}
                GROUP BY c.id
                ORDER BY source_count DESC, c.canonical_name
                LIMIT %s OFFSET %s""",
            params,
        ).fetchall()

        total = conn.execute(
            f"SELECT COUNT(*) AS cnt FROM concepts c {where}",
            params[:-2],  # exclude limit/offset
        ).fetchone()["cnt"]

        types = conn.execute(
            """SELECT concept_type, COUNT(*) AS count
               FROM concepts
               WHERE concept_type IS NOT NULL
               GROUP BY concept_type
               ORDER BY count DESC"""
        ).fetchall()

    return {
        "items": rows,
        "total": total,
        "types": types,
    }


@router.get("/{concept_id}")
def get_concept(concept_id: str):
    """Get a single concept with its linked sources."""
    with db.get_conn() as conn:
        concept = conn.execute(
            "SELECT * FROM concepts WHERE id = %s",
            (concept_id,),
        ).fetchone()

        if not concept:
            raise HTTPException(status_code=404, detail=f"Concept '{concept_id}' not found")

        sources = conn.execute(
            """SELECT s.id, s.title, s.source_type, s.ingested_at, sc.relationship, sc.confidence
               FROM source_concepts sc
               JOIN sources s ON s.id = sc.source_id
               WHERE sc.concept_id = %s
               ORDER BY sc.confidence DESC NULLS LAST, s.ingested_at DESC
               LIMIT 50""",
            (concept_id,),
        ).fetchall()

        # Find related concepts (shared sources)
        related = conn.execute(
            """SELECT c2.id, c2.canonical_name, c2.concept_type,
                      COUNT(*) AS shared_sources
               FROM source_concepts sc1
               JOIN source_concepts sc2 ON sc1.source_id = sc2.source_id
               JOIN concepts c2 ON c2.id = sc2.concept_id
               WHERE sc1.concept_id = %s AND sc2.concept_id != %s
               GROUP BY c2.id, c2.canonical_name, c2.concept_type
               ORDER BY shared_sources DESC
               LIMIT 20""",
            (concept_id, concept_id),
        ).fetchall()

    return {
        "concept": concept,
        "sources": sources,
        "related": related,
    }
