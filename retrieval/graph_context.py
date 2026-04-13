"""Shared graph context: compact, structured graph intelligence for LLM context.

Composable functions that any handler can call alongside gather_wiki_context()
to inject graph-structural signals (bridge concepts, cross-theme implications,
cluster membership, suggested questions) into LLM prompts.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class GraphContext:
    """Compact graph intelligence for LLM context injection."""
    bridge_concepts: list[dict] = field(default_factory=list)
    concept_edges: list[dict] = field(default_factory=list)
    cross_theme_implications: list[dict] = field(default_factory=list)
    cluster_info: list[dict] = field(default_factory=list)
    contradictions: list[dict] = field(default_factory=list)
    suggested_questions: list[str] = field(default_factory=list)
    stats: dict = field(default_factory=dict)


def query_graph_context(
    query: str | None = None,
    theme_ids: list[str] | None = None,
    source_ids: list[str] | None = None,
    get_conn_fn=None,
    budget_items: int = 20,
) -> GraphContext:
    """Build a compact graph context block for LLM injection.

    Combines bridge concept discovery, cross-theme implications,
    contradiction detection, and graph-topology suggested questions.
    All queries are best-effort — failures degrade gracefully.
    """
    if get_conn_fn is None:
        from reading_app.db import get_conn
        get_conn_fn = get_conn

    gctx = GraphContext()

    # Resolve theme_ids from query if not provided
    if not theme_ids and query:
        try:
            from retrieval.lenses import _find_themes_for_query
            theme_ids = _find_themes_for_query(query, get_conn_fn)
        except Exception:
            logger.debug("graph_context_theme_discovery_failed", exc_info=True)

    # 1. Bridge concepts — high betweenness centrality concepts in relevant themes
    try:
        gctx.bridge_concepts = _get_bridge_concepts(
            get_conn_fn, theme_ids=theme_ids, limit=min(budget_items, 10),
        )
    except Exception:
        logger.debug("graph_context_bridge_failed", exc_info=True)

    # 1b. Concept-level edges
    try:
        gctx.concept_edges = get_concept_edges(
            get_conn_fn, theme_ids=theme_ids, limit=min(budget_items, 10),
        )
    except Exception:
        logger.debug("graph_context_concept_edges_failed", exc_info=True)

    # 2. Cross-theme implications
    if theme_ids:
        try:
            gctx.cross_theme_implications = _get_implications(
                get_conn_fn, theme_ids, limit=min(budget_items, 10),
            )
        except Exception:
            logger.debug("graph_context_implications_failed", exc_info=True)

    # 3. Contradictions (if query provided)
    if query:
        try:
            from retrieval.graph import GraphRetriever
            gr = GraphRetriever(get_conn_fn)
            raw = gr.find_contradictions(topic=query, threshold=0.83)
            for c in raw[:5]:
                gctx.contradictions.append({
                    "claim_a": c.get("claim_a_text", "")[:150],
                    "claim_b": c.get("claim_b_text", "")[:150],
                    "source_a_title": c.get("source_a_title", ""),
                    "source_b_title": c.get("source_b_title", ""),
                    "similarity": c.get("similarity", 0),
                })
        except Exception:
            logger.debug("graph_context_contradictions_failed", exc_info=True)

    # 4. Cluster info for source_ids
    if source_ids:
        try:
            gctx.cluster_info = _get_cluster_info(get_conn_fn, source_ids)
        except Exception:
            logger.debug("graph_context_cluster_failed", exc_info=True)

    # 5. Suggested questions from graph topology
    try:
        gctx.suggested_questions = _suggest_questions(
            gctx, theme_ids=theme_ids, query=query,
        )
    except Exception:
        logger.debug("graph_context_questions_failed", exc_info=True)

    # Stats for logging
    gctx.stats = {
        "bridges": len(gctx.bridge_concepts),
        "concept_edges": len(gctx.concept_edges),
        "implications": len(gctx.cross_theme_implications),
        "contradictions": len(gctx.contradictions),
        "questions": len(gctx.suggested_questions),
    }

    return gctx


# ---------------------------------------------------------------------------
# Component queries
# ---------------------------------------------------------------------------


def _get_bridge_concepts(
    get_conn_fn,
    theme_ids: list[str] | None = None,
    limit: int = 10,
) -> list[dict]:
    """Get high-betweenness concepts, optionally filtered to themes."""
    with get_conn_fn() as conn:
        if theme_ids:
            rows = conn.execute(
                """SELECT c.id, c.canonical_name,
                          gm.score AS betweenness,
                          array_agg(DISTINCT st.theme_id) FILTER (WHERE st.theme_id IS NOT NULL) AS themes,
                          COUNT(DISTINCT sc.source_id) AS source_count
                   FROM graph_metrics gm
                   JOIN concepts c ON gm.entity_id = c.id::text
                   JOIN source_concepts sc ON sc.concept_id = c.id
                   JOIN source_themes st ON st.source_id = sc.source_id
                   WHERE gm.metric_type = 'betweenness'
                     AND gm.entity_type = 'concept'
                     AND st.theme_id = ANY(%s)
                   GROUP BY c.id, c.canonical_name, gm.score
                   ORDER BY gm.score DESC
                   LIMIT %s""",
                (theme_ids, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT c.id, c.canonical_name,
                          gm.score AS betweenness,
                          COUNT(DISTINCT sc.source_id) AS source_count
                   FROM graph_metrics gm
                   JOIN concepts c ON gm.entity_id = c.id::text
                   JOIN source_concepts sc ON sc.concept_id = c.id
                   WHERE gm.metric_type = 'betweenness'
                     AND gm.entity_type = 'concept'
                   GROUP BY c.id, c.canonical_name, gm.score
                   ORDER BY gm.score DESC
                   LIMIT %s""",
                (limit,),
            ).fetchall()

    return [
        {
            "name": r["canonical_name"],
            "betweenness": round(r["betweenness"], 4),
            "source_count": r["source_count"],
            "themes": r.get("themes", []),
        }
        for r in rows
    ]


def _get_implications(
    get_conn_fn,
    theme_ids: list[str],
    limit: int = 10,
) -> list[dict]:
    """Get cross-theme implications involving the given themes."""
    with get_conn_fn() as conn:
        rows = conn.execute(
            """SELECT cti.implication, cti.confidence,
                      st.name AS source_theme, tt.name AS target_theme,
                      st.id AS source_theme_id, tt.id AS target_theme_id
               FROM cross_theme_implications cti
               LEFT JOIN themes st ON cti.source_theme_id = st.id
               LEFT JOIN themes tt ON cti.target_theme_id = tt.id
               WHERE cti.source_theme_id = ANY(%s) OR cti.target_theme_id = ANY(%s)
               ORDER BY cti.confidence DESC NULLS LAST
               LIMIT %s""",
            (theme_ids, theme_ids, limit),
        ).fetchall()

    return [
        {
            "source_theme": r["source_theme"] or r["source_theme_id"],
            "target_theme": r["target_theme"] or r["target_theme_id"],
            "source_theme_id": r["source_theme_id"],
            "target_theme_id": r["target_theme_id"],
            "implication": r["implication"][:200] if r["implication"] else "",
            "confidence": r["confidence"],
        }
        for r in rows
    ]


def get_concept_edges(
    get_conn_fn,
    concept_names: list[str] | None = None,
    theme_ids: list[str] | None = None,
    limit: int = 15,
) -> list[dict]:
    """Get typed concept-level relationships, optionally filtered."""
    with get_conn_fn() as conn:
        if concept_names:
            rows = conn.execute(
                """SELECT ca.canonical_name AS concept_a, cb.canonical_name AS concept_b,
                          ce.edge_type, ce.confidence
                   FROM concept_edges ce
                   JOIN concepts ca ON ce.concept_a_id = ca.id
                   JOIN concepts cb ON ce.concept_b_id = cb.id
                   WHERE ca.canonical_name = ANY(%s) OR cb.canonical_name = ANY(%s)
                   ORDER BY ce.confidence DESC
                   LIMIT %s""",
                (concept_names, concept_names, limit),
            ).fetchall()
        elif theme_ids:
            rows = conn.execute(
                """SELECT DISTINCT ca.canonical_name AS concept_a, cb.canonical_name AS concept_b,
                          ce.edge_type, ce.confidence
                   FROM concept_edges ce
                   JOIN concepts ca ON ce.concept_a_id = ca.id
                   JOIN concepts cb ON ce.concept_b_id = cb.id
                   JOIN source_concepts sca ON sca.concept_id = ca.id
                   JOIN source_themes sta ON sta.source_id = sca.source_id
                   WHERE sta.theme_id = ANY(%s)
                   ORDER BY ce.confidence DESC
                   LIMIT %s""",
                (theme_ids, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT ca.canonical_name AS concept_a, cb.canonical_name AS concept_b,
                          ce.edge_type, ce.confidence
                   FROM concept_edges ce
                   JOIN concepts ca ON ce.concept_a_id = ca.id
                   JOIN concepts cb ON ce.concept_b_id = cb.id
                   ORDER BY ce.confidence DESC
                   LIMIT %s""",
                (limit,),
            ).fetchall()

    return [
        {
            "concept_a": r["concept_a"],
            "concept_b": r["concept_b"],
            "edge_type": r["edge_type"],
            "confidence": r["confidence"],
        }
        for r in rows
    ]


def _get_cluster_info(
    get_conn_fn,
    source_ids: list[str],
) -> list[dict]:
    """Get community membership for the given sources."""
    with get_conn_fn() as conn:
        rows = conn.execute(
            """SELECT gm.entity_id AS source_id, s.title,
                      gm.score AS community_id
               FROM graph_metrics gm
               JOIN sources s ON gm.entity_id = s.id
               WHERE gm.metric_type = 'community'
                 AND gm.entity_type = 'source'
                 AND gm.entity_id = ANY(%s)""",
            (source_ids,),
        ).fetchall()

    return [
        {
            "source_id": r["source_id"],
            "title": r["title"],
            "community": int(r["community_id"]),
        }
        for r in rows
    ]


def _suggest_questions(
    gctx: GraphContext,
    theme_ids: list[str] | None = None,
    query: str | None = None,
) -> list[str]:
    """Generate structural questions from graph topology."""
    questions = []

    # Questions from bridge concepts
    for b in gctx.bridge_concepts[:3]:
        themes = b.get("themes") or []
        if themes and len(themes) >= 2:
            # themes may be IDs — use cross_theme_implications for readable names
            t1, t2 = themes[0], themes[1]
            # Try to find readable theme names from implications
            name_map = {}
            for imp in gctx.cross_theme_implications:
                if imp.get("source_theme"):
                    name_map[imp.get("source_theme_id", "")] = imp["source_theme"]
                    name_map[imp.get("target_theme_id", "")] = imp["target_theme"]
            t1_display = name_map.get(t1, t1)
            t2_display = name_map.get(t2, t2)
            questions.append(
                f"Why does '{b['name']}' bridge {t1_display} and {t2_display}? "
                f"What structural role does it play?"
            )
        elif b["source_count"] >= 5:
            questions.append(
                f"'{b['name']}' appears in {b['source_count']} sources with high centrality. "
                f"What makes it a conceptual hub?"
            )

    # Questions from contradictions
    for c in gctx.contradictions[:2]:
        questions.append(
            f"How to reconcile: \"{c['claim_a'][:80]}\" vs \"{c['claim_b'][:80]}\"?"
        )

    # Questions from cross-theme implications
    for imp in gctx.cross_theme_implications[:2]:
        if imp["source_theme"] != imp["target_theme"]:
            questions.append(
                f"What are the second-order effects of {imp['source_theme']} "
                f"developments on {imp['target_theme']}?"
            )

    return questions[:5]


# ---------------------------------------------------------------------------
# Epistemic status vocabulary
# ---------------------------------------------------------------------------


def confidence_tier(
    confidence: float | None,
    provenance_type: str | None = None,
) -> str:
    """Map numeric confidence + provenance to a human-readable epistemic tier.

    Returns one of: EXTRACTED, INFERRED, AMBIGUOUS, SPECULATIVE, ESTABLISHED.
    """
    if confidence is None:
        return "AMBIGUOUS"

    # Provenance overrides for specific types
    if provenance_type == "user_enrichment":
        return "ESTABLISHED" if confidence >= 0.6 else "INFERRED"
    if provenance_type == "synthesis":
        return "INFERRED" if confidence >= 0.5 else "SPECULATIVE"

    # Numeric tiers
    if confidence >= 0.85:
        return "EXTRACTED"
    if confidence >= 0.65:
        return "INFERRED"
    if confidence >= 0.4:
        return "AMBIGUOUS"
    return "SPECULATIVE"


def format_confidence_display(
    confidence: float | None,
    provenance_type: str | None = None,
) -> str:
    """Format confidence as 'TIER (0.XX)' for display."""
    tier = confidence_tier(confidence, provenance_type)
    if confidence is not None:
        return f"{tier} ({confidence:.2f})"
    return tier


def format_graph_context_block(
    gctx: GraphContext,
    header: str = "Graph Intelligence",
    max_chars: int = 3000,
) -> str:
    """Format GraphContext as a prompt-ready markdown block."""
    if not any([
        gctx.bridge_concepts,
        gctx.concept_edges,
        gctx.cross_theme_implications,
        gctx.contradictions,
        gctx.suggested_questions,
    ]):
        return ""

    parts = [f"## {header}\n"]
    chars = len(parts[0])

    def _budget_ok() -> bool:
        return chars < max_chars

    if gctx.bridge_concepts:
        parts.append("### Bridge Concepts (high centrality)")
        for b in gctx.bridge_concepts[:5]:
            line = f"- **{b['name']}** (betweenness: {b['betweenness']}, {b['source_count']} sources)"
            parts.append(line)
            chars += len(line) + 1

    if gctx.concept_edges and _budget_ok():
        parts.append("\n### Concept Relationships")
        for ce in gctx.concept_edges[:5]:
            etype = ce["edge_type"].replace("_", " ")
            line = f"- **{ce['concept_a']}** {etype} **{ce['concept_b']}** ({ce['confidence']:.2f})"
            parts.append(line)
            chars += len(line) + 1

    if gctx.cross_theme_implications and _budget_ok():
        parts.append("\n### Cross-Theme Implications")
        for imp in gctx.cross_theme_implications[:5]:
            conf = f" [{imp['confidence']:.2f}]" if imp.get("confidence") else ""
            line = f"- {imp['source_theme']} → {imp['target_theme']}: {imp['implication']}{conf}"
            parts.append(line)
            chars += len(line) + 1
            if not _budget_ok():
                break

    if gctx.contradictions and _budget_ok():
        parts.append("\n### Potential Contradictions")
        for c in gctx.contradictions[:3]:
            line = (
                f"- \"{c['claim_a']}\" vs \"{c['claim_b']}\" "
                f"({c.get('source_a_title', '?')} vs {c.get('source_b_title', '?')})"
            )
            parts.append(line)
            chars += len(line) + 1

    if gctx.suggested_questions and _budget_ok():
        parts.append("\n### Structural Questions")
        for q in gctx.suggested_questions:
            parts.append(f"- {q}")

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Graph report artifact
# ---------------------------------------------------------------------------


def generate_graph_report(get_conn_fn=None) -> str:
    """Generate a compact structural briefing: what's interesting in the graph right now.

    Designed for /map or /gaps. Cached externally; callers should invalidate
    when source count changes.
    """
    if get_conn_fn is None:
        from reading_app.db import get_conn
        get_conn_fn = get_conn

    parts = ["# Knowledge Graph Report\n"]

    # 1. Corpus stats
    try:
        with get_conn_fn() as conn:
            counts = conn.execute(
                """SELECT
                       (SELECT COUNT(*) FROM sources WHERE processing_status = 'complete') AS sources,
                       (SELECT COUNT(*) FROM claims) AS claims,
                       (SELECT COUNT(*) FROM concepts) AS concepts,
                       (SELECT COUNT(*) FROM source_edges) AS source_edges,
                       (SELECT COUNT(*) FROM themes) AS themes"""
            ).fetchone()
            concept_edge_count = 0
            try:
                concept_edge_count = conn.execute(
                    "SELECT COUNT(*) AS c FROM concept_edges"
                ).fetchone()["c"]
            except Exception:
                pass

        parts.append("## Corpus Overview")
        parts.append(f"- **{counts['sources']}** sources, **{counts['claims']}** claims")
        parts.append(f"- **{counts['concepts']}** concepts, **{counts['themes']}** themes")
        parts.append(f"- **{counts['source_edges']}** source edges, **{concept_edge_count}** concept edges")
        parts.append("")
    except Exception:
        logger.debug("graph_report_stats_failed", exc_info=True)

    # 2. Top bridge concepts
    try:
        bridges = _get_bridge_concepts(get_conn_fn, limit=10)
        if bridges:
            parts.append("## Bridge Concepts (highest betweenness centrality)")
            for i, b in enumerate(bridges, 1):
                parts.append(
                    f"{i}. **{b['name']}** — betweenness: {b['betweenness']}, "
                    f"{b['source_count']} sources"
                )
            parts.append("")
    except Exception:
        logger.debug("graph_report_bridges_failed", exc_info=True)

    # 3. Theme influence (PageRank on theme DAG)
    try:
        with get_conn_fn() as conn:
            themes = conn.execute(
                """SELECT gm.entity_id, t.name, gm.score
                   FROM graph_metrics gm
                   JOIN themes t ON gm.entity_id = t.id
                   WHERE gm.metric_type = 'theme_influence'
                   ORDER BY gm.score DESC
                   LIMIT 10"""
            ).fetchall()
        if themes:
            parts.append("## Most Influential Themes (PageRank)")
            for t in themes:
                parts.append(f"- **{t['name']}** (influence: {t['score']:.4f})")
            parts.append("")
    except Exception:
        logger.debug("graph_report_themes_failed", exc_info=True)

    # 4. Community summary
    try:
        with get_conn_fn() as conn:
            communities = conn.execute(
                """SELECT gm.score AS community_id, COUNT(*) AS member_count,
                          array_agg(s.title ORDER BY gm.entity_id) AS titles
                   FROM graph_metrics gm
                   JOIN sources s ON gm.entity_id = s.id
                   WHERE gm.metric_type = 'community'
                   GROUP BY gm.score
                   HAVING COUNT(*) >= 3
                   ORDER BY COUNT(*) DESC
                   LIMIT 8"""
            ).fetchall()
        if communities:
            parts.append(f"## Source Communities ({len(communities)} clusters with 3+ members)")
            for c in communities:
                sample = [t[:50] for t in (c["titles"] or [])[:3]]
                parts.append(
                    f"- Cluster {int(c['community_id'])}: "
                    f"{c['member_count']} sources — {', '.join(sample)}"
                )
            parts.append("")
    except Exception:
        logger.debug("graph_report_communities_failed", exc_info=True)

    # 5. Coverage gaps
    try:
        from retrieval.lenses import scan_coverage_gaps
        gaps = scan_coverage_gaps(get_conn_fn)
        if gaps:
            parts.append(f"## Coverage Gaps ({len(gaps)} detected)")
            for g in gaps[:10]:
                parts.append(f"- [{g['gap_type']}] **{g['theme']}**: {g['detail']}")
            parts.append("")
    except Exception:
        logger.debug("graph_report_gaps_failed", exc_info=True)

    # 6. Concept edges summary
    try:
        edges = get_concept_edges(get_conn_fn, limit=10)
        if edges:
            parts.append("## Top Concept Relationships")
            for e in edges:
                etype = e["edge_type"].replace("_", " ")
                parts.append(
                    f"- **{e['concept_a']}** {etype} **{e['concept_b']}** "
                    f"(conf: {e['confidence']:.2f})"
                )
            parts.append("")
    except Exception:
        logger.debug("graph_report_concept_edges_failed", exc_info=True)

    # 7. Wiki health snapshot
    try:
        from pathlib import Path
        wiki_dir = Path(__file__).resolve().parent.parent / "wiki"
        page_counts = {}
        for subdir in ("themes", "entities", "sources", "syntheses", "beliefs", "questions"):
            d = wiki_dir / subdir
            if d.is_dir():
                page_counts[subdir] = len(list(d.glob("*.md")))
            else:
                page_counts[subdir] = 0

        parts.append("## Wiki Health")
        for subdir, count in page_counts.items():
            parts.append(f"- **{subdir}**: {count} pages")
        parts.append("")
    except Exception:
        logger.debug("graph_report_wiki_health_failed", exc_info=True)

    return "\n".join(parts)
