"""Search API router -- fan-out full-text and trigram search + semantic vector search."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Query

from reading_app import db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("/")
def search(
    q: str = Query(..., min_length=1, description="Search query"),
    types: str | None = Query(None, description="Comma-separated entity types to search"),
):
    """Fan-out search across sources, claims, capabilities, limitations,
    bottlenecks, beliefs, anticipations, and ideas.  Uses pg_trgm similarity
    where FTS is unavailable."""
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty")

    allowed_types = {"sources", "claims", "capabilities", "limitations",
                     "bottlenecks", "beliefs", "anticipations", "ideas"}
    if types:
        requested = {t.strip() for t in types.split(",")}
        search_types = requested & allowed_types
    else:
        search_types = allowed_types

    results: dict[str, list] = {}
    counts: dict[str, int] = {}

    with db.get_conn() as conn:
        if "sources" in search_types:
            rows = conn.execute(
                """SELECT id, title, source_type, url, abstract,
                          similarity(title, %s) AS sim
                   FROM sources
                   WHERE title %% %s
                   ORDER BY sim DESC
                   LIMIT 20""",
                (q, q),
            ).fetchall()
            results["sources"] = rows
            counts["sources"] = len(rows)

        if "claims" in search_types:
            rows = conn.execute(
                """SELECT id, source_id, claim_text, claim_type, confidence,
                          evidence_snippet,
                          ts_rank(fts_vector, plainto_tsquery('english', %s)) AS rank
                   FROM claims
                   WHERE fts_vector @@ plainto_tsquery('english', %s)
                   ORDER BY rank DESC
                   LIMIT 20""",
                (q, q),
            ).fetchall()
            results["claims"] = rows
            counts["claims"] = len(rows)

        if "capabilities" in search_types:
            rows = conn.execute(
                """SELECT c.id, c.theme_id, c.description, c.maturity, c.confidence,
                          t.name AS theme_name,
                          similarity(c.description, %s) AS sim
                   FROM capabilities c
                   LEFT JOIN themes t ON c.theme_id = t.id
                   WHERE c.description %% %s
                   ORDER BY sim DESC
                   LIMIT 20""",
                (q, q),
            ).fetchall()
            results["capabilities"] = rows
            counts["capabilities"] = len(rows)

        if "limitations" in search_types:
            rows = conn.execute(
                """SELECT l.id, l.theme_id, l.description, l.limitation_type, l.severity,
                          t.name AS theme_name,
                          similarity(l.description, %s) AS sim
                   FROM limitations l
                   LEFT JOIN themes t ON l.theme_id = t.id
                   WHERE l.description %% %s
                   ORDER BY sim DESC
                   LIMIT 20""",
                (q, q),
            ).fetchall()
            results["limitations"] = rows
            counts["limitations"] = len(rows)

        if "bottlenecks" in search_types:
            rows = conn.execute(
                """SELECT b.id, b.theme_id, b.description, b.bottleneck_type,
                          b.resolution_horizon, b.confidence,
                          t.name AS theme_name,
                          similarity(b.description, %s) AS sim
                   FROM bottlenecks b
                   LEFT JOIN themes t ON b.theme_id = t.id
                   WHERE b.description %% %s
                   ORDER BY sim DESC
                   LIMIT 20""",
                (q, q),
            ).fetchall()
            results["bottlenecks"] = rows
            counts["bottlenecks"] = len(rows)

        if "beliefs" in search_types:
            rows = conn.execute(
                """SELECT id, claim, confidence, status, belief_type,
                          domain_theme_id,
                          similarity(claim, %s) AS sim
                   FROM beliefs
                   WHERE claim %% %s
                   ORDER BY sim DESC
                   LIMIT 20""",
                (q, q),
            ).fetchall()
            results["beliefs"] = rows
            counts["beliefs"] = len(rows)

        if "anticipations" in search_types:
            rows = conn.execute(
                """SELECT id, theme_id, prediction, confidence, timeline, status,
                          similarity(prediction, %s) AS sim
                   FROM anticipations
                   WHERE prediction %% %s
                   ORDER BY sim DESC
                   LIMIT 20""",
                (q, q),
            ).fetchall()
            results["anticipations"] = rows
            counts["anticipations"] = len(rows)

        if "ideas" in search_types:
            rows = conn.execute(
                """SELECT id, idea_text, idea_type, novelty_score, overall_score,
                          novelty_check_passed,
                          similarity(idea_text, %s) AS sim
                   FROM ideas
                   WHERE idea_text %% %s
                   ORDER BY sim DESC
                   LIMIT 20""",
                (q, q),
            ).fetchall()
            results["ideas"] = rows
            counts["ideas"] = len(rows)

    return {"query": q, "counts": counts, "results": results}


@router.get("/semantic")
def semantic_search(
    q: str = Query(..., min_length=2, description="Search query"),
    k: int = Query(20, ge=1, le=50, description="Number of results"),
    recent_bias: bool = Query(False, description="Apply temporal decay to favor recent sources"),
):
    """Semantic search using vector embeddings + keyword hybrid retrieval with RRF fusion."""
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty")

    from reading_app.embeddings import embed_sync
    from retrieval.hybrid import hybrid_retrieve, DECAY_DEFAULT

    embedding = embed_sync(q)
    if embedding is None:
        logger.warning("Embedding generation failed for query: %s — falling back to keyword-only", q[:80])

    results = hybrid_retrieve(
        query=q,
        get_conn_fn=db.get_conn,
        embedding=embedding,
        k=k,
        mmr=True,
        temporal_decay=recent_bias,
        half_life_days=DECAY_DEFAULT,
    )

    # Group by source for better presentation
    sources_seen: dict[str, dict] = {}
    claims = []
    for r in results:
        claim = {
            "id": r["id"],
            "claim_text": r["claim_text"],
            "source_id": r["source_id"],
            "source_title": r.get("source_title", ""),
            "evidence_snippet": r.get("evidence_snippet", ""),
            "score": round(r.get("rrf_score", 0), 4),
        }
        claims.append(claim)

        sid = r["source_id"]
        if sid not in sources_seen:
            sources_seen[sid] = {
                "id": sid,
                "title": r.get("source_title", ""),
                "claim_count": 0,
                "top_score": 0,
            }
        sources_seen[sid]["claim_count"] += 1
        sources_seen[sid]["top_score"] = max(sources_seen[sid]["top_score"], claim["score"])

    sources = sorted(sources_seen.values(), key=lambda s: -s["top_score"])

    return {
        "query": q,
        "total": len(claims),
        "claims": claims,
        "sources": sources[:10],
        "embedding_available": embedding is not None,
    }
