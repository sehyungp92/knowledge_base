"""Library API router -- sources, ideas, contradictions."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from reading_app import db
from ingest.source_quality import read_source_artifact_text, resolve_source_dir
from retrieval.graph import GraphRetriever

router = APIRouter(prefix="/api/library", tags=["library"])


def _get_source_or_404(source_id: str) -> dict:
    """Load a source row or raise a 404."""
    source = db.get_source(source_id)
    if not source:
        raise HTTPException(status_code=404, detail=f"Source '{source_id}' not found")
    return source


def _artifact_flags(source: dict) -> dict[str, bool]:
    """Return lightweight availability flags for source markdown artifacts."""
    source_dir = resolve_source_dir(source.get("library_path"), source["id"])
    if source_dir is None:
        return {"has_summary": False, "has_reflection": False}
    return {
        "has_summary": (source_dir / "deep_summary.md").is_file(),
        "has_reflection": (source_dir / "reflection.md").is_file(),
    }


@router.get("/sources")
def list_sources(
    source_type: str | None = Query(None),
    status: str | None = Query(None),
    sort: str | None = Query(None, description="Sort by: date (default) or influence"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List sources with optional filters. sort=influence uses PageRank from graph_metrics."""
    # Build common claim_count subquery
    claim_count_sql = "(SELECT count(*) FROM claims WHERE source_id = s.id) AS claim_count"

    if sort == "influence":
        conditions: list[str] = []
        params: list = []
        if source_type:
            conditions.append("s.source_type = %s")
            params.append(source_type)
        if status:
            conditions.append("s.processing_status = %s")
            params.append(status)
        where = "WHERE " + " AND ".join(conditions) if conditions else ""
        params.extend([limit, offset])
        with db.get_conn() as conn:
            rows = conn.execute(
                f"""SELECT s.*, COALESCE(gm.score, 0) AS influence_score,
                           {claim_count_sql}
                    FROM sources s
                    LEFT JOIN graph_metrics gm
                      ON gm.entity_id = s.id
                      AND gm.metric_type = 'pagerank'
                      AND gm.entity_type = 'source'
                    {where}
                    ORDER BY COALESCE(gm.score, 0) DESC, s.ingested_at DESC
                    LIMIT %s OFFSET %s""",
                params,
            ).fetchall()
        return rows

    # Default sort by date, with claim_count
    conditions2: list[str] = []
    params2: list = []
    if source_type:
        conditions2.append("s.source_type = %s")
        params2.append(source_type)
    if status:
        conditions2.append("s.processing_status = %s")
        params2.append(status)
    where2 = "WHERE " + " AND ".join(conditions2) if conditions2 else ""
    params2.extend([limit, offset])
    with db.get_conn() as conn:
        rows = conn.execute(
            f"""SELECT s.*, {claim_count_sql}
                FROM sources s
                {where2}
                ORDER BY s.ingested_at DESC
                LIMIT %s OFFSET %s""",
            params2,
        ).fetchall()
    return rows


@router.get("/sources/{source_id}")
def get_source(source_id: str):
    """Get a compact source overview for the detail page header."""
    source = _get_source_or_404(source_id)
    like_pattern = f"%{source_id}%"
    with db.get_conn() as conn:
        themes = conn.execute(
            """SELECT t.id, t.name FROM themes t
               JOIN source_themes st ON t.id = st.theme_id
               WHERE st.source_id = %s""",
            (source_id,),
        ).fetchall()

        concepts = conn.execute(
            """SELECT c.id, c.canonical_name, c.concept_type, sc.relationship
               FROM source_concepts sc
               JOIN concepts c ON sc.concept_id = c.id
               WHERE sc.source_id = %s""",
            (source_id,),
        ).fetchall()
        count_row = conn.execute(
            """SELECT
                   (SELECT COUNT(*) FROM claims WHERE source_id = %s) AS claim_count,
                   (SELECT COUNT(*) FROM source_edges
                      WHERE source_a = %s OR source_b = %s) AS related_count,
                   (SELECT COUNT(*) FROM capabilities
                      WHERE evidence_sources::text LIKE %s) AS capability_count,
                   (SELECT COUNT(*) FROM limitations
                      WHERE evidence_sources::text LIKE %s) AS limitation_count,
                   (SELECT COUNT(*) FROM bottlenecks
                      WHERE evidence_sources::text LIKE %s) AS bottleneck_count,
                   (SELECT COUNT(*) FROM breakthroughs
                      WHERE primary_source_id = %s
                         OR corroborating_sources::text LIKE %s) AS breakthrough_count""",
            (
                source_id,
                source_id,
                source_id,
                like_pattern,
                like_pattern,
                like_pattern,
                source_id,
                like_pattern,
            ),
        ).fetchone()

    return {
        "source": source,
        "themes": themes,
        "concepts": concepts,
        "counts": {
            "claims": count_row["claim_count"] if count_row else 0,
            "related_sources": count_row["related_count"] if count_row else 0,
            "landscape_signals": {
                "capabilities": count_row["capability_count"] if count_row else 0,
                "limitations": count_row["limitation_count"] if count_row else 0,
                "bottlenecks": count_row["bottleneck_count"] if count_row else 0,
                "breakthroughs": count_row["breakthrough_count"] if count_row else 0,
            },
        },
        "artifacts": _artifact_flags(source),
    }


@router.get("/sources/{source_id}/claims")
def get_source_claims(
    source_id: str,
    limit: int = Query(25, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Paginated claims for a source detail page."""
    _get_source_or_404(source_id)
    with db.get_conn() as conn:
        total = conn.execute(
            "SELECT COUNT(*) AS cnt FROM claims WHERE source_id = %s",
            (source_id,),
        ).fetchone()["cnt"]
        items = conn.execute(
            """SELECT id, claim_text, evidence_snippet, claim_type, section, confidence
               FROM claims
               WHERE source_id = %s
               ORDER BY confidence DESC NULLS LAST, section ASC
               LIMIT %s OFFSET %s""",
            (source_id, limit, offset),
        ).fetchall()

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + len(items) < total,
    }


@router.get("/sources/{source_id}/related")
def get_source_related(
    source_id: str,
    limit: int = Query(12, ge=1, le=50),
    offset: int = Query(0, ge=0),
):
    """Paginated one-hop source relationships."""
    _get_source_or_404(source_id)
    graph = GraphRetriever(db.get_conn)
    neighbours = graph.one_hop(source_id)
    total = len(neighbours)
    items = neighbours[offset: offset + limit]
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + len(items) < total,
    }


@router.get("/sources/{source_id}/landscape-signals")
def get_source_landscape_signals(
    source_id: str,
    limit_per_group: int = Query(6, ge=1, le=20),
):
    """Grouped landscape signals tied to a source, loaded on demand."""
    _get_source_or_404(source_id)
    like_pattern = f"%{source_id}%"

    with db.get_conn() as conn:
        capability_total = conn.execute(
            "SELECT COUNT(*) AS cnt FROM capabilities WHERE evidence_sources::text LIKE %s",
            (like_pattern,),
        ).fetchone()["cnt"]
        limitation_total = conn.execute(
            "SELECT COUNT(*) AS cnt FROM limitations WHERE evidence_sources::text LIKE %s",
            (like_pattern,),
        ).fetchone()["cnt"]
        bottleneck_total = conn.execute(
            "SELECT COUNT(*) AS cnt FROM bottlenecks WHERE evidence_sources::text LIKE %s",
            (like_pattern,),
        ).fetchone()["cnt"]
        breakthrough_total = conn.execute(
            """SELECT COUNT(*) AS cnt FROM breakthroughs
               WHERE primary_source_id = %s
                  OR corroborating_sources::text LIKE %s""",
            (source_id, like_pattern),
        ).fetchone()["cnt"]

        capabilities = conn.execute(
            """SELECT c.id, c.theme_id, t.name AS theme_name, c.description, c.maturity, c.confidence
               FROM capabilities c
               LEFT JOIN themes t ON c.theme_id = t.id
               WHERE c.evidence_sources::text LIKE %s
               ORDER BY c.confidence DESC NULLS LAST, c.last_updated DESC NULLS LAST
               LIMIT %s""",
            (like_pattern, limit_per_group),
        ).fetchall()
        limitations = conn.execute(
            """SELECT l.id, l.theme_id, t.name AS theme_name, l.description, l.limitation_type, l.severity
               FROM limitations l
               LEFT JOIN themes t ON l.theme_id = t.id
               WHERE l.evidence_sources::text LIKE %s
               ORDER BY l.confidence DESC NULLS LAST, l.last_updated DESC NULLS LAST
               LIMIT %s""",
            (like_pattern, limit_per_group),
        ).fetchall()
        bottlenecks = conn.execute(
            """SELECT b.id, b.theme_id, t.name AS theme_name, b.description, b.bottleneck_type, b.resolution_horizon
               FROM bottlenecks b
               LEFT JOIN themes t ON b.theme_id = t.id
               WHERE b.evidence_sources::text LIKE %s
               ORDER BY b.confidence DESC NULLS LAST, b.last_updated DESC NULLS LAST
               LIMIT %s""",
            (like_pattern, limit_per_group),
        ).fetchall()
        breakthroughs = conn.execute(
            """SELECT br.id, br.theme_id, t.name AS theme_name, br.description, br.significance
               FROM breakthroughs br
               LEFT JOIN themes t ON br.theme_id = t.id
               WHERE br.primary_source_id = %s
                  OR br.corroborating_sources::text LIKE %s
               ORDER BY br.detected_at DESC
               LIMIT %s""",
            (source_id, like_pattern, limit_per_group),
        ).fetchall()

    return {
        "limit_per_group": limit_per_group,
        "capabilities": {
            "items": capabilities,
            "total": capability_total,
            "has_more": len(capabilities) < capability_total,
        },
        "limitations": {
            "items": limitations,
            "total": limitation_total,
            "has_more": len(limitations) < limitation_total,
        },
        "bottlenecks": {
            "items": bottlenecks,
            "total": bottleneck_total,
            "has_more": len(bottlenecks) < bottleneck_total,
        },
        "breakthroughs": {
            "items": breakthroughs,
            "total": breakthrough_total,
            "has_more": len(breakthroughs) < breakthrough_total,
        },
    }


@router.get("/sources/{source_id}/graph-context")
def get_source_graph_context(source_id: str):
    """Return graph-derived context that explains why a source matters."""
    _get_source_or_404(source_id)
    graph = GraphRetriever(db.get_conn)

    with db.get_conn() as conn:
        metric_row = conn.execute(
            """SELECT pr.score AS influence_score,
                      community.metadata->>'community_id' AS community_id
               FROM graph_metrics pr
               LEFT JOIN graph_metrics community
                 ON community.entity_id = pr.entity_id
                AND community.metric_type = 'community'
                AND community.entity_type = 'source'
               WHERE pr.metric_type = 'pagerank'
                 AND pr.entity_type = 'source'
                 AND pr.entity_id = %s""",
            (source_id,),
        ).fetchone()

        community_id = metric_row["community_id"] if metric_row else None

        peers = []
        cluster_size = 0
        if community_id is not None:
            cluster_size = conn.execute(
                """SELECT COUNT(*) AS cnt
                   FROM graph_metrics gm
                   WHERE gm.metric_type = 'community'
                     AND gm.entity_type = 'source'
                     AND gm.metadata->>'community_id' = %s""",
                (str(community_id),),
            ).fetchone()["cnt"]
            peers = conn.execute(
                """SELECT gm.entity_id AS id, s.title, COALESCE(pr.score, 0) AS influence_score
                   FROM graph_metrics gm
                   JOIN sources s ON gm.entity_id = s.id
                   LEFT JOIN graph_metrics pr
                     ON pr.entity_id = gm.entity_id
                    AND pr.metric_type = 'pagerank'
                    AND pr.entity_type = 'source'
                   WHERE gm.metric_type = 'community'
                     AND gm.entity_type = 'source'
                     AND gm.metadata->>'community_id' = %s
                     AND gm.entity_id != %s
                   ORDER BY COALESCE(pr.score, 0) DESC, s.ingested_at DESC
                   LIMIT 5""",
                (str(community_id), source_id),
            ).fetchall()

    implications = graph.get_source_implications(source_id)[:4]

    return {
        "influence_score": metric_row["influence_score"] if metric_row else None,
        "community_id": int(community_id) if community_id not in (None, "") else None,
        "community_size": cluster_size,
        "cluster_peers": peers,
        "implications": implications,
    }


@router.get("/sources/{source_id}/summary")
def get_source_summary(source_id: str):
    """Return the deep summary markdown for a source."""
    source = _get_source_or_404(source_id)

    library_path = source.get("library_path")
    if not library_path:
        raise HTTPException(status_code=404, detail="No library path for this source")

    summary_text = read_source_artifact_text(library_path, source_id, "deep_summary.md")
    if summary_text is None:
        raise HTTPException(status_code=404, detail="No deep summary available")

    return {"markdown": summary_text}


@router.get("/sources/{source_id}/reflection")
def get_source_reflection(source_id: str):
    """Return the reflection markdown for a source."""
    source = _get_source_or_404(source_id)

    library_path = source.get("library_path")
    if not library_path:
        raise HTTPException(status_code=404, detail="No library path for this source")

    reflection_text = read_source_artifact_text(library_path, source_id, "reflection.md")
    if reflection_text is None:
        raise HTTPException(status_code=404, detail="No reflection available")

    return {"markdown": reflection_text}


@router.get("/ideas")
def list_ideas(
    idea_type: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """List ideas that passed the novelty gate, optionally filtered by type."""
    conditions: list[str] = ["novelty_check_passed = TRUE"]
    params: list = []

    if idea_type:
        conditions.append("idea_type = %s")
        params.append(idea_type)

    where = "WHERE " + " AND ".join(conditions)
    params.extend([limit, offset])

    with db.get_conn() as conn:
        rows = conn.execute(
            f"""SELECT * FROM ideas
                {where}
                ORDER BY overall_score DESC NULLS LAST
                LIMIT %s OFFSET %s""",
            params,
        ).fetchall()

    return rows


@router.get("/contradictions")
def list_contradictions(
    topic: str = Query("", description="Topic filter for contradiction search"),
    limit: int = Query(20, ge=1, le=100),
    threshold: float = Query(0.85, ge=0.7, le=0.99),
):
    """Find potential claim contradictions via embedding similarity."""
    if not topic:
        return []

    escaped = topic.replace("%", r"\%").replace("_", r"\_")
    pattern = f"%{escaped}%"

    with db.get_conn() as conn:
        rows = conn.execute(
            """SELECT c1.id AS claim_a, c2.id AS claim_b,
                      c1.claim_text AS claim_a_text, c1.source_id AS source_a_id,
                      c2.claim_text AS claim_b_text, c2.source_id AS source_b_id,
                      1 - (c1.embedding <=> c2.embedding) AS similarity
               FROM claims c1
               JOIN claims c2 ON c1.id < c2.id
               WHERE c1.embedding IS NOT NULL AND c2.embedding IS NOT NULL
                 AND c1.source_id != c2.source_id
                 AND (c1.claim_text ILIKE %s OR c2.claim_text ILIKE %s)
                 AND 1 - (c1.embedding <=> c2.embedding) > %s
               ORDER BY similarity DESC
               LIMIT %s""",
            (pattern, pattern, threshold, limit),
        ).fetchall()

    return rows
