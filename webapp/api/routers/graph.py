"""Graph metrics API router -- communities, influence, bridge concepts, export, path, theme DAG."""

from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException, Query

from reading_app import db

router = APIRouter(prefix="/api/graph", tags=["graph"])


def _get_metrics(metric_type: str, entity_type: str, limit: int = 20) -> list[dict]:
    """Read pre-computed graph metrics from the graph_metrics table."""
    with db.get_conn() as conn:
        rows = conn.execute(
            """SELECT * FROM graph_metrics
               WHERE metric_type = %s AND entity_type = %s
               ORDER BY score DESC
               LIMIT %s""",
            (metric_type, entity_type, limit),
        ).fetchall()
    return rows


def _parse_metric_metadata(value) -> dict[str, object]:
    """Normalize graph metric metadata from DB rows."""
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return {}
        if isinstance(parsed, dict):
            return parsed
    return {}


def _normalize_community_id(metadata_value, score_value) -> int | None:
    """Resolve a stable integer community id from metadata or score."""
    metadata = _parse_metric_metadata(metadata_value)
    raw_value = metadata.get("community_id", score_value)
    if raw_value in (None, ""):
        return None

    try:
        return int(float(raw_value))
    except (TypeError, ValueError):
        return None


@router.get("/communities")
def communities(limit: int = Query(20, ge=1, le=100)):
    """Source communities with resolved titles and theme labels."""
    metrics = _get_metrics("community", "source", limit)
    if not metrics:
        return metrics

    entity_ids = [m["entity_id"] for m in metrics]
    with db.get_conn() as conn:
        # Resolve source titles
        srows = conn.execute(
            "SELECT id, title FROM sources WHERE id = ANY(%s)",
            (entity_ids,),
        ).fetchall()
        title_lookup = {r["id"]: r["title"] for r in srows}

        # Get most common theme per community
        theme_rows = conn.execute(
            """SELECT st.source_id, t.name AS theme_name
               FROM source_themes st
               JOIN themes t ON st.theme_id = t.id
               WHERE st.source_id = ANY(%s)""",
            (entity_ids,),
        ).fetchall()
        source_themes: dict[str, list[str]] = {}
        for r in theme_rows:
            source_themes.setdefault(r["source_id"], []).append(r["theme_name"])

    for m in metrics:
        m["title"] = title_lookup.get(m["entity_id"], m["entity_id"])
    return metrics


@router.get("/influential-sources")
def influential_sources(limit: int = Query(20, ge=1, le=100)):
    """Top sources ranked by PageRank with resolved titles."""
    metrics = _get_metrics("pagerank", "source", limit)
    if not metrics:
        return metrics

    entity_ids = [m["entity_id"] for m in metrics]
    with db.get_conn() as conn:
        srows = conn.execute(
            "SELECT id, title FROM sources WHERE id = ANY(%s)",
            (entity_ids,),
        ).fetchall()
        title_lookup = {r["id"]: r["title"] for r in srows}

    for m in metrics:
        m["title"] = title_lookup.get(m["entity_id"], m["entity_id"])
    return metrics


@router.get("/bridge-concepts")
def bridge_concepts(limit: int = Query(20, ge=1, le=100)):
    """Concepts that bridge disparate parts of the knowledge graph, with resolved names."""
    metrics = _get_metrics("betweenness", "concept", limit)
    if not metrics:
        return metrics

    entity_ids = [m["entity_id"] for m in metrics]
    with db.get_conn() as conn:
        crows = conn.execute(
            "SELECT id, canonical_name FROM concepts WHERE id = ANY(%s)",
            (entity_ids,),
        ).fetchall()
        name_lookup = {r["id"]: r["canonical_name"] for r in crows}

    for m in metrics:
        m["canonical_name"] = name_lookup.get(m["entity_id"], m["entity_id"])
    return metrics


@router.get("/theme-influence")
def theme_influence(limit: int = Query(20, ge=1, le=100)):
    """Theme-level influence scores with resolved names."""
    metrics = _get_metrics("theme_influence", "theme", limit)
    if not metrics:
        return metrics

    entity_ids = [m["entity_id"] for m in metrics]
    with db.get_conn() as conn:
        trows = conn.execute(
            "SELECT id, name FROM themes WHERE id = ANY(%s)",
            (entity_ids,),
        ).fetchall()
        name_lookup = {r["id"]: r["name"] for r in trows}

    for m in metrics:
        m["name"] = name_lookup.get(m["entity_id"], m["entity_id"])
    return metrics


@router.get("/export")
def export_graph(limit: int = Query(50, ge=1, le=500)):
    """Export top sources by PageRank with their edges, for Cytoscape or similar."""
    with db.get_conn() as conn:
        # Top sources by pagerank
        node_rows = conn.execute(
            """SELECT pr.entity_id AS id, s.title, pr.score AS pagerank,
                      s.published_at, s.source_type,
                      community.score AS community_score,
                      community.metadata AS community_metadata,
                      (SELECT count(*) FROM claims c WHERE c.source_id = s.id) AS claim_count
               FROM graph_metrics pr
               JOIN sources s ON pr.entity_id = s.id
               LEFT JOIN graph_metrics community
                 ON community.entity_id = pr.entity_id
                AND community.metric_type = 'community'
                AND community.entity_type = 'source'
               WHERE pr.metric_type = 'pagerank' AND pr.entity_type = 'source'
               ORDER BY pr.score DESC
               LIMIT %s""",
            (limit,),
        ).fetchall()

        nodes = []
        for row in node_rows:
            node = dict(row)
            node["community"] = _normalize_community_id(
                node.pop("community_metadata", None),
                node.pop("community_score", None),
            )
            # Serialize published_at for JSON
            if node.get("published_at") is not None:
                node["published_at"] = str(node["published_at"])
            nodes.append(node)

        node_ids = [n["id"] for n in nodes]
        if not node_ids:
            return {"nodes": [], "edges": []}

        # Edges between these nodes
        edge_rows = conn.execute(
            """SELECT source_a, source_b, edge_type, explanation, confidence
               FROM source_edges
               WHERE source_a = ANY(%s) AND source_b = ANY(%s)""",
            (node_ids, node_ids),
        ).fetchall()

    edges = [dict(edge) for edge in edge_rows]
    return {"nodes": nodes, "edges": edges}


@router.get("/theme-dag")
def theme_dag():
    """Export theme DAG for visualization: themes as nodes, theme_edges + cross-theme implications as edges."""
    with db.get_conn() as conn:
        themes = conn.execute(
            "SELECT id, name, velocity FROM themes ORDER BY velocity DESC NULLS LAST"
        ).fetchall()

        hierarchy_edges = conn.execute(
            "SELECT parent_id, child_id, relationship, strength FROM theme_edges"
        ).fetchall()

        implication_edges = conn.execute(
            """SELECT source_theme_id, target_theme_id, implication, confidence
               FROM cross_theme_implications
               ORDER BY confidence DESC NULLS LAST
               LIMIT 100"""
        ).fetchall()

    return {
        "themes": themes,
        "hierarchy_edges": hierarchy_edges,
        "implication_edges": implication_edges,
    }


@router.get("/themes/{theme_id}/context")
def theme_context(theme_id: str):
    """Summarize how a theme sits inside the theme graph."""
    with db.get_conn() as conn:
        theme = conn.execute(
            "SELECT id, name FROM themes WHERE id = %s",
            (theme_id,),
        ).fetchone()
        if not theme:
            raise HTTPException(status_code=404, detail=f"Theme '{theme_id}' not found")

        influence = conn.execute(
            """SELECT score, rank
               FROM (
                   SELECT entity_id, score, RANK() OVER (ORDER BY score DESC) AS rank
                   FROM graph_metrics
                   WHERE metric_type = 'theme_influence' AND entity_type = 'theme'
               ) ranked
               WHERE entity_id = %s""",
            (theme_id,),
        ).fetchone()

        parents = conn.execute(
            """SELECT p.id, p.name, te.relationship
               FROM theme_edges te
               JOIN themes p ON te.parent_id = p.id
               WHERE te.child_id = %s
               ORDER BY p.name""",
            (theme_id,),
        ).fetchall()
        children = conn.execute(
            """SELECT c.id, c.name, te.relationship
               FROM theme_edges te
               JOIN themes c ON te.child_id = c.id
               WHERE te.parent_id = %s
               ORDER BY c.name""",
            (theme_id,),
        ).fetchall()

        outgoing = conn.execute(
            """SELECT cti.id, cti.implication, cti.confidence,
                      cti.source_theme_id, cti.target_theme_id,
                      tt.name AS target_theme
               FROM cross_theme_implications cti
               JOIN themes tt ON cti.target_theme_id = tt.id
               WHERE cti.source_theme_id = %s
               ORDER BY cti.confidence DESC NULLS LAST
               LIMIT 4""",
            (theme_id,),
        ).fetchall()
        incoming = conn.execute(
            """SELECT cti.id, cti.implication, cti.confidence,
                      cti.source_theme_id, cti.target_theme_id,
                      st.name AS source_theme
               FROM cross_theme_implications cti
               JOIN themes st ON cti.source_theme_id = st.id
               WHERE cti.target_theme_id = %s
               ORDER BY cti.confidence DESC NULLS LAST
               LIMIT 4""",
            (theme_id,),
        ).fetchall()

    return {
        "theme": theme,
        "influence": {
            "score": influence["score"] if influence else None,
            "rank": influence["rank"] if influence else None,
        },
        "parents": parents,
        "children": children,
        "outgoing_implications": outgoing,
        "incoming_implications": incoming,
    }


# ---------------------------------------------------------------------------
# Path between two sources
# ---------------------------------------------------------------------------

def _resolve_source_ref(ref: str) -> dict | None:
    """Resolve a source by ID (exact or prefix) or partial title match."""
    import re
    _ID_RE = re.compile(r"[0-9A-Z]{26}")

    with db.get_conn() as conn:
        # Exact ID
        if _ID_RE.fullmatch(ref):
            row = conn.execute(
                "SELECT id, title FROM sources WHERE id = %s", (ref,)
            ).fetchone()
            if row:
                return dict(row)

        # Prefix match (at least 6 chars)
        if len(ref) >= 6 and ref.replace("-", "").isalnum():
            row = conn.execute(
                "SELECT id, title FROM sources WHERE id LIKE %s LIMIT 1",
                (f"{ref}%",),
            ).fetchone()
            if row:
                return dict(row)

        # Partial title match
        row = conn.execute(
            "SELECT id, title FROM sources WHERE title ILIKE %s LIMIT 1",
            (f"%{ref}%",),
        ).fetchone()
        if row:
            return dict(row)

    return None


@router.get("/path")
def graph_path(
    from_id: str = Query(..., alias="from", description="Source A: ID, ID prefix, or partial title"),
    to_id: str = Query(..., alias="to", description="Source B: ID, ID prefix, or partial title"),
    max_hops: int = Query(3, ge=1, le=5, description="Maximum path depth"),
):
    """Find and explain connection paths between two sources.

    Returns edge paths (via source_edges), shared concepts, and claim
    relationships linking the two sources.
    """
    # Resolve source references
    source_a = _resolve_source_ref(from_id)
    if not source_a:
        raise HTTPException(status_code=404, detail=f"Source not found: {from_id}")

    source_b = _resolve_source_ref(to_id)
    if not source_b:
        raise HTTPException(status_code=404, detail=f"Source not found: {to_id}")

    id_a = source_a["id"]
    id_b = source_b["id"]

    if id_a == id_b:
        raise HTTPException(
            status_code=400,
            detail=f"Both references resolve to the same source: {source_a['title']} ({id_a})",
        )

    # --- Edge paths via recursive CTE ---
    from retrieval.graph import GraphRetriever

    edge_paths = []
    with db.get_conn() as conn:
        retriever = GraphRetriever(lambda: conn)
        raw_paths = retriever.explain_path(id_a, id_b, max_hops=max_hops)

        if raw_paths:
            # Collect all IDs and edge pairs for batch resolution
            all_ids: set[str] = set()
            all_edge_pairs: set[tuple[str, str]] = set()
            for row in raw_paths:
                path_ids = list(row.get("path", []))
                all_ids.update(path_ids)
                for i in range(len(path_ids) - 1):
                    all_edge_pairs.add((path_ids[i], path_ids[i + 1]))

            # Resolve titles
            if all_ids:
                placeholders = ",".join(["%s"] * len(all_ids))
                title_rows = conn.execute(
                    f"SELECT id, title FROM sources WHERE id IN ({placeholders})",
                    tuple(all_ids),
                ).fetchall()
                titles = {r["id"]: r["title"] for r in title_rows}
            else:
                titles = {}

            # Resolve edge metadata
            edges_lookup: dict[tuple[str, str], dict] = {}
            for a, b in all_edge_pairs:
                edge_row = conn.execute(
                    """SELECT edge_type, explanation, confidence
                       FROM source_edges
                       WHERE (source_a = %s AND source_b = %s)
                          OR (source_a = %s AND source_b = %s)
                       LIMIT 1""",
                    (a, b, b, a),
                ).fetchone()
                if edge_row:
                    edges_lookup[(a, b)] = dict(edge_row)

            # Build enriched paths
            for row in raw_paths:
                path_ids = list(row.get("path", []))
                hops = []
                for i in range(len(path_ids) - 1):
                    edge_info = edges_lookup.get((path_ids[i], path_ids[i + 1]), {})
                    hops.append({
                        "from_id": path_ids[i],
                        "from_title": titles.get(path_ids[i], path_ids[i]),
                        "to_id": path_ids[i + 1],
                        "to_title": titles.get(path_ids[i + 1], path_ids[i + 1]),
                        "edge_type": edge_info.get("edge_type", "unknown"),
                        "explanation": edge_info.get("explanation"),
                        "confidence": edge_info.get("confidence"),
                    })
                edge_paths.append({
                    "path_ids": path_ids,
                    "depth": row.get("depth", len(hops)),
                    "hops": hops,
                })

    # --- Shared concepts ---
    with db.get_conn() as conn:
        shared_concepts_rows = conn.execute("""
            SELECT c.id, c.canonical_name, c.concept_type,
                   sc1.relationship AS rel_a, sc2.relationship AS rel_b
            FROM source_concepts sc1
            JOIN source_concepts sc2 ON sc1.concept_id = sc2.concept_id
            JOIN concepts c ON sc1.concept_id = c.id
            WHERE sc1.source_id = %s AND sc2.source_id = %s
            ORDER BY c.canonical_name
        """, (id_a, id_b)).fetchall()

    shared_concepts = [dict(r) for r in shared_concepts_rows]

    connected = bool(edge_paths or shared_concepts)

    return {
        "source_a": {"id": id_a, "title": source_a["title"]},
        "source_b": {"id": id_b, "title": source_b["title"]},
        "connected": connected,
        "edge_paths": edge_paths,
        "shared_concepts": shared_concepts,
    }


# ---------------------------------------------------------------------------
# Rich node detail (Phase 4: Graph Detail Drawer)
# ---------------------------------------------------------------------------

@router.get("/node/{source_id}/detail")
def node_detail(source_id: str):
    """Return rich detail payload for a source node in the graph.

    Fetched lazily on node selection. Includes evidence snippets,
    temporal metadata, confidence, source type counts, and implications.
    """
    with db.get_conn() as conn:
        # Verify source exists
        source = conn.execute(
            "SELECT id, title, source_type, url, published_at, ingested_at FROM sources WHERE id = %s",
            (source_id,),
        ).fetchone()
        if not source:
            raise HTTPException(status_code=404, detail=f"Source '{source_id}' not found")

        # Evidence count + top snippets
        claim_rows = conn.execute(
            """SELECT claim_text, evidence_snippet, confidence, section
               FROM claims
               WHERE source_id = %s
               ORDER BY confidence DESC NULLS LAST
               LIMIT 5""",
            (source_id,),
        ).fetchall()
        evidence_count_row = conn.execute(
            "SELECT COUNT(*) AS cnt FROM claims WHERE source_id = %s",
            (source_id,),
        ).fetchone()
        evidence_count = evidence_count_row["cnt"] if evidence_count_row else 0

        supporting_snippets = [
            {
                "claim_text": r["claim_text"][:200] if r["claim_text"] else "",
                "evidence_snippet": r["evidence_snippet"][:300] if r["evidence_snippet"] else "",
                "confidence": r["confidence"],
                "section": r["section"],
            }
            for r in claim_rows
        ]

        # Temporal metadata: first and last seen via connected sources
        temporal = conn.execute(
            """SELECT
                  MIN(s2.published_at) AS first_seen,
                  MAX(s2.published_at) AS last_seen
               FROM source_edges se
               JOIN sources s2 ON s2.id = CASE
                   WHEN se.source_a = %s THEN se.source_b
                   ELSE se.source_a
               END
               WHERE se.source_a = %s OR se.source_b = %s""",
            (source_id, source_id, source_id),
        ).fetchone()

        first_seen = source["published_at"]
        last_seen = source["published_at"]
        if temporal:
            if temporal["first_seen"] and (not first_seen or temporal["first_seen"] < first_seen):
                first_seen = temporal["first_seen"]
            if temporal["last_seen"] and (not last_seen or temporal["last_seen"] > last_seen):
                last_seen = temporal["last_seen"]

        # Aggregated confidence from edges
        edge_conf = conn.execute(
            """SELECT AVG(confidence) AS avg_conf, COUNT(*) AS edge_count
               FROM source_edges
               WHERE (source_a = %s OR source_b = %s) AND confidence IS NOT NULL""",
            (source_id, source_id),
        ).fetchone()

        # Source type counts of connected sources
        type_counts = conn.execute(
            """SELECT s2.source_type, COUNT(*) AS cnt
               FROM source_edges se
               JOIN sources s2 ON s2.id = CASE
                   WHEN se.source_a = %s THEN se.source_b
                   ELSE se.source_a
               END
               WHERE se.source_a = %s OR se.source_b = %s
               GROUP BY s2.source_type""",
            (source_id, source_id, source_id),
        ).fetchall()
        source_type_counts = {r["source_type"]: r["cnt"] for r in type_counts}

        # Themes for this source
        themes = conn.execute(
            """SELECT t.id, t.name
               FROM source_themes st
               JOIN themes t ON st.theme_id = t.id
               WHERE st.source_id = %s""",
            (source_id,),
        ).fetchall()
        theme_ids = [t["id"] for t in themes]

        # Cross-theme implications involving this source's themes
        implication_summaries = []
        if theme_ids:
            impl_rows = conn.execute(
                """SELECT cti.implication, cti.confidence,
                          st.name AS source_theme, tt.name AS target_theme
                   FROM cross_theme_implications cti
                   JOIN themes st ON cti.source_theme_id = st.id
                   JOIN themes tt ON cti.target_theme_id = tt.id
                   WHERE cti.source_theme_id = ANY(%s) OR cti.target_theme_id = ANY(%s)
                   ORDER BY cti.confidence DESC NULLS LAST
                   LIMIT 5""",
                (theme_ids, theme_ids),
            ).fetchall()
            implication_summaries = [
                {
                    "source_theme": r["source_theme"],
                    "target_theme": r["target_theme"],
                    "implication": r["implication"][:200] if r["implication"] else "",
                    "confidence": r["confidence"],
                }
                for r in impl_rows
            ]

        # Bridge scores from graph_metrics
        bridge_rows = conn.execute(
            """SELECT gm.score, gm.metadata
               FROM graph_metrics gm
               WHERE gm.entity_id = %s AND gm.metric_type = 'betweenness'
               LIMIT 1""",
            (source_id,),
        ).fetchall()
        bridge_score = bridge_rows[0]["score"] if bridge_rows else None

    return {
        "source_id": source_id,
        "title": source["title"],
        "source_type": source["source_type"],
        "url": source["url"],
        "evidence_count": evidence_count,
        "supporting_snippets": supporting_snippets,
        "first_seen": first_seen.isoformat() if hasattr(first_seen, "isoformat") else str(first_seen) if first_seen else None,
        "last_seen": last_seen.isoformat() if hasattr(last_seen, "isoformat") else str(last_seen) if last_seen else None,
        "confidence": round(edge_conf["avg_conf"], 3) if edge_conf and edge_conf["avg_conf"] else None,
        "edge_count": edge_conf["edge_count"] if edge_conf else 0,
        "source_type_counts": source_type_counts,
        "themes": [{"id": t["id"], "name": t["name"]} for t in themes],
        "implication_summaries": implication_summaries,
        "bridge_score": bridge_score,
    }
