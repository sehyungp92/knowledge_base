"""Analytical lenses: structured multi-perspective retrieval.

Four lenses provide different views on a query:
- Evidence: Direct claim and snippet retrieval
- Theme Panorama: Landscape state across themes
- Bridge / Implication: Cross-theme and cross-source connections
- Contradiction / Coverage Gap: Conflicting claims and thin areas
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class LensResult:
    """Structured result from an analytical lens."""
    lens_id: str          # "evidence" | "theme_panorama" | "bridge" | "contradiction"
    query: str            # input that drove the lens
    summary: str          # narrative summary of findings
    confidence: float     # lens-level confidence (0-1)
    citations: list[str] = field(default_factory=list)   # source IDs cited
    evidence_items: list[dict] = field(default_factory=list)  # structured evidence


# ---------------------------------------------------------------------------
# Evidence Lens
# ---------------------------------------------------------------------------

def evidence_lens(
    query: str,
    get_conn_fn,
    embedding: list[float] | None = None,
    k: int = 15,
) -> LensResult:
    """Direct claim and snippet retrieval for a question.

    Runs hybrid_retrieve, formats top claims with snippets, generates
    a brief narrative summary from the results.
    """
    from retrieval.hybrid import hybrid_retrieve

    try:
        claims = hybrid_retrieve(
            query=query,
            get_conn_fn=get_conn_fn,
            embedding=embedding,
            k=k,
            mmr=True,
            mmr_lambda=0.7,
        )
    except Exception:
        logger.warning("evidence_lens retrieval failed", exc_info=True)
        return LensResult(
            lens_id="evidence", query=query, summary="Retrieval failed.",
            confidence=0.0,
        )

    if not claims:
        return LensResult(
            lens_id="evidence", query=query,
            summary="No relevant claims found in the knowledge base.",
            confidence=0.0,
        )

    # Build structured evidence items
    evidence_items = []
    citations = set()
    for c in claims:
        sid = c.get("source_id", "")
        citations.add(sid)
        evidence_items.append({
            "claim_text": c.get("claim_text", c.get("claim", "")),
            "evidence_snippet": c.get("evidence_snippet", ""),
            "source_id": sid,
            "source_title": c.get("source_title", ""),
            "confidence": c.get("claim_confidence", c.get("confidence")),
            "rrf_score": c.get("rrf_score", 0),
        })

    # Build narrative summary from top claims (no LLM, just structured)
    top_sources = {}
    for item in evidence_items[:10]:
        sid = item["source_id"]
        if sid not in top_sources:
            top_sources[sid] = {
                "title": item["source_title"],
                "claims": [],
            }
        top_sources[sid]["claims"].append(item["claim_text"][:150])

    summary_parts = [f"Found {len(claims)} relevant claims across {len(citations)} sources."]
    for sid, info in list(top_sources.items())[:5]:
        title = info["title"] or sid[:12]
        claim_preview = info["claims"][0][:120] if info["claims"] else ""
        summary_parts.append(f"- [{sid[:12]}] {title}: {claim_preview}")

    avg_score = sum(c.get("rrf_score", 0) for c in claims) / len(claims) if claims else 0
    confidence = min(1.0, avg_score * 30)  # Normalize RRF scores to 0-1

    return LensResult(
        lens_id="evidence",
        query=query,
        summary="\n".join(summary_parts),
        confidence=confidence,
        citations=list(citations),
        evidence_items=evidence_items,
    )


# ---------------------------------------------------------------------------
# Theme Panorama Lens
# ---------------------------------------------------------------------------

def panorama_lens(
    query: str,
    get_conn_fn,
    theme_ids: list[str] | None = None,
) -> LensResult:
    """Landscape state across themes for a topic.

    Fetches theme states (capabilities, limitations, bottlenecks, breakthroughs,
    anticipations), generates cross-theme narrative.
    """
    # If no theme_ids provided, search for matching themes
    if not theme_ids:
        theme_ids = _find_themes_for_query(query, get_conn_fn)

    if not theme_ids:
        return LensResult(
            lens_id="theme_panorama", query=query,
            summary="No matching themes found for this query.",
            confidence=0.0,
        )

    from retrieval.wiki_retrieval import gather_wiki_context
    wiki_ctx = gather_wiki_context(theme_ids=theme_ids[:5])

    # Build summary from wiki narratives
    summary_parts = [f"Landscape across {min(len(theme_ids), 5)} themes:"]
    for tid, narrative in wiki_ctx.theme_narratives.items():
        first_para = narrative.split("\n\n")[0] if narrative else ""
        summary_parts.append(f"\n**{tid}:** {first_para[:500]}")

    # Minimal evidence_items for citation tracking
    evidence_items = [
        {"type": "theme_narrative", "theme_id": tid, "content": narrative[:200]}
        for tid, narrative in wiki_ctx.theme_narratives.items()
    ]

    has_data = bool(wiki_ctx.theme_narratives)
    confidence = 0.7 if has_data else 0.2

    return LensResult(
        lens_id="theme_panorama",
        query=query,
        summary="\n".join(summary_parts),
        confidence=confidence,
        citations=[],
        evidence_items=evidence_items,
    )


# ---------------------------------------------------------------------------
# Bridge / Implication Lens
# ---------------------------------------------------------------------------

def bridge_lens(
    query: str,
    get_conn_fn,
    embedding: list[float] | None = None,
) -> LensResult:
    """Cross-theme and cross-source connections.

    Runs two_hop_via_concepts and checks cross_theme_implications
    to find unexpected connections relevant to the query.
    """
    from retrieval.graph import GraphRetriever
    from retrieval.hybrid import hybrid_retrieve

    # First find relevant sources via hybrid search
    try:
        claims = hybrid_retrieve(
            query=query, get_conn_fn=get_conn_fn,
            embedding=embedding, k=5,
        )
    except Exception:
        claims = []

    source_ids = list(dict.fromkeys(c.get("source_id") for c in claims if c.get("source_id")))

    evidence_items = []
    citations = set()

    # Get 2-hop connections for top sources
    if source_ids:
        try:
            gr = GraphRetriever(get_conn_fn)
            for sid in source_ids[:3]:
                two_hop = gr.two_hop_via_concepts(sid)
                for conn_info in two_hop[:5]:
                    citations.add(sid)
                    connected_id = conn_info.get("id", "")
                    citations.add(connected_id)
                    evidence_items.append({
                        "type": "concept_bridge",
                        "source_a": sid,
                        "source_b": connected_id,
                        "title": conn_info.get("title", ""),
                        "shared_concepts": conn_info.get("shared_concepts", []),
                        "overlap_count": conn_info.get("overlap_count", 0),
                    })
        except Exception:
            logger.debug("bridge_lens: graph retrieval failed", exc_info=True)

    # Get cross-theme implications
    theme_ids = _find_themes_for_query(query, get_conn_fn)
    if theme_ids:
        try:
            with get_conn_fn() as conn:
                impl_rows = conn.execute(
                    """SELECT cti.implication, cti.confidence,
                              st.name AS source_theme, tt.name AS target_theme,
                              cti.evidence_sources
                       FROM cross_theme_implications cti
                       LEFT JOIN themes st ON cti.source_theme_id = st.id
                       LEFT JOIN themes tt ON cti.target_theme_id = tt.id
                       WHERE cti.source_theme_id = ANY(%s) OR cti.target_theme_id = ANY(%s)
                       ORDER BY cti.confidence DESC NULLS LAST
                       LIMIT 10""",
                    (theme_ids, theme_ids),
                ).fetchall()

                for r in impl_rows:
                    evidence_items.append({
                        "type": "cross_theme_implication",
                        "source_theme": r.get("source_theme", "?"),
                        "target_theme": r.get("target_theme", "?"),
                        "implication": r.get("implication", ""),
                        "confidence": r.get("confidence"),
                    })
                    for sid in (r.get("evidence_sources") or []):
                        citations.add(sid)
        except Exception:
            logger.debug("bridge_lens: implications query failed", exc_info=True)

    # Build summary
    concept_bridges = [e for e in evidence_items if e["type"] == "concept_bridge"]
    implications = [e for e in evidence_items if e["type"] == "cross_theme_implication"]

    summary_parts = []
    if concept_bridges:
        summary_parts.append(f"Found {len(concept_bridges)} concept-bridge connections:")
        for b in concept_bridges[:3]:
            concepts = b.get("shared_concepts", [])
            concept_str = ", ".join(concepts[:3]) if isinstance(concepts, list) else str(concepts)
            summary_parts.append(f"- {b['title'][:60]} via [{concept_str}]")
    if implications:
        summary_parts.append(f"Found {len(implications)} cross-theme implications:")
        for imp in implications[:3]:
            summary_parts.append(
                f"- {imp['source_theme']} -> {imp['target_theme']}: {imp['implication'][:80]}"
            )

    if not summary_parts:
        summary_parts.append("No bridge connections or cross-theme implications found.")

    confidence = min(1.0, len(evidence_items) * 0.1) if evidence_items else 0.0

    return LensResult(
        lens_id="bridge",
        query=query,
        summary="\n".join(summary_parts),
        confidence=confidence,
        citations=list(citations),
        evidence_items=evidence_items,
    )


# ---------------------------------------------------------------------------
# Contradiction / Coverage Gap Lens
# ---------------------------------------------------------------------------

def contradiction_lens(
    query: str,
    get_conn_fn,
    embedding: list[float] | None = None,
) -> LensResult:
    """Finds claim pairs with high semantic similarity but opposing stances,
    and identifies coverage gaps.
    """
    from retrieval.graph import GraphRetriever

    evidence_items = []
    citations = set()

    # Find contradictions via graph retriever (includes temporal metadata)
    try:
        gr = GraphRetriever(get_conn_fn)
        contradictions = gr.find_contradictions(topic=query, threshold=0.82)
        for c in contradictions[:10]:
            citations.add(c.get("source_a_id", ""))
            citations.add(c.get("source_b_id", ""))

            # Temporal trajectory: which claim is newer? Is the disagreement recent?
            date_a = c.get("source_a_date")
            date_b = c.get("source_b_date")
            newer_source = None
            temporal_note = ""
            if date_a and date_b:
                if date_a > date_b:
                    newer_source = "a"
                    temporal_note = (
                        f"Newer source ({str(date_a)[:10]}) contradicts older ({str(date_b)[:10]}) "
                        f"— disagreement may be widening"
                    )
                elif date_b > date_a:
                    newer_source = "b"
                    temporal_note = (
                        f"Newer source ({str(date_b)[:10]}) contradicts older ({str(date_a)[:10]}) "
                        f"— disagreement may be widening"
                    )
                else:
                    temporal_note = f"Same period ({str(date_a)[:10]}) — contemporaneous disagreement"

            evidence_items.append({
                "type": "potential_contradiction",
                "claim_a": c.get("claim_a_text", ""),
                "claim_b": c.get("claim_b_text", ""),
                "source_a": c.get("source_a_id", ""),
                "source_b": c.get("source_b_id", ""),
                "source_a_title": c.get("source_a_title", ""),
                "source_b_title": c.get("source_b_title", ""),
                "source_a_date": str(date_a)[:10] if date_a else None,
                "source_b_date": str(date_b)[:10] if date_b else None,
                "newer_source": newer_source,
                "temporal_note": temporal_note,
                "similarity": c.get("similarity", 0),
            })
    except Exception:
        logger.debug("contradiction_lens: find_contradictions failed", exc_info=True)

    # Coverage gap analysis — delegate to scan_coverage_gaps to avoid duplication
    theme_ids = _find_themes_for_query(query, get_conn_fn)
    if theme_ids:
        try:
            gaps = scan_coverage_gaps(get_conn_fn, theme_ids=theme_ids)
            for gap in gaps:
                evidence_items.append({
                    "type": "coverage_gap",
                    "gap_type": gap["gap_type"],
                    "theme": gap["theme"],
                    "detail": gap["detail"],
                })
        except Exception:
            logger.debug("contradiction_lens: coverage gap query failed", exc_info=True)

    # Build summary
    contradictions_found = [e for e in evidence_items if e["type"] == "potential_contradiction"]
    gaps_found = [e for e in evidence_items if e["type"] == "coverage_gap"]

    summary_parts = []
    if contradictions_found:
        summary_parts.append(f"Found {len(contradictions_found)} potential contradictions:")
        for c in contradictions_found[:3]:
            temporal = f" | {c['temporal_note']}" if c.get("temporal_note") else ""
            summary_parts.append(
                f"- \"{c['claim_a'][:60]}\" vs \"{c['claim_b'][:60]}\" "
                f"(similarity: {c['similarity']:.2f}{temporal})"
            )
    if gaps_found:
        summary_parts.append(f"Found {len(gaps_found)} coverage gaps:")
        for g in gaps_found[:3]:
            summary_parts.append(f"- [{g['gap_type']}] {g['theme']}: {g['detail'][:80]}")

    if not summary_parts:
        summary_parts.append("No contradictions or coverage gaps detected for this query.")

    confidence = min(1.0, len(evidence_items) * 0.15) if evidence_items else 0.0

    return LensResult(
        lens_id="contradiction",
        query=query,
        summary="\n".join(summary_parts),
        confidence=confidence,
        citations=list(citations),
        evidence_items=evidence_items,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _find_themes_for_query(query: str, get_conn_fn) -> list[str]:
    """Find theme IDs matching a query by name ILIKE + FTS on state_summary.

    Two-stage approach:
    1. Name ILIKE match (fast, exact)
    2. FTS on state_summary text (catches semantic matches the name misses)
    Results are deduplicated and ordered by velocity.
    """
    try:
        with get_conn_fn() as conn:
            # Stage 1: Name match (original behavior)
            name_rows = conn.execute(
                """SELECT id FROM themes
                   WHERE name ILIKE %s OR id = %s
                   ORDER BY velocity DESC NULLS LAST
                   LIMIT 5""",
                (f"%{query}%", query),
            ).fetchall()
            found_ids = [r["id"] for r in name_rows]

            # Stage 2: FTS on state_summary (if name match found < 3 themes)
            if len(found_ids) < 3:
                fts_rows = conn.execute(
                    """SELECT id FROM themes
                       WHERE state_summary IS NOT NULL
                         AND to_tsvector('english', state_summary)
                             @@ websearch_to_tsquery('english', %s)
                         AND id != ALL(%s)
                       ORDER BY velocity DESC NULLS LAST
                       LIMIT %s""",
                    (query, found_ids or [], 5 - len(found_ids)),
                ).fetchall()
                found_ids.extend(r["id"] for r in fts_rows)

            return found_ids[:5]
    except Exception:
        return []


def run_lens_by_name(
    lens_id: str,
    query: str,
    get_conn_fn,
    embedding: list[float] | None = None,
    **kwargs,
) -> LensResult:
    """Dispatch to a lens function by name.

    Used by the ReACT report agent to dynamically select lenses.
    """
    dispatchers = {
        "evidence": lambda: evidence_lens(query, get_conn_fn, embedding=embedding, k=kwargs.get("k", 15)),
        "theme_panorama": lambda: panorama_lens(query, get_conn_fn, theme_ids=kwargs.get("theme_ids")),
        "bridge": lambda: bridge_lens(query, get_conn_fn, embedding=embedding),
        "contradiction": lambda: contradiction_lens(query, get_conn_fn, embedding=embedding),
    }
    fn = dispatchers.get(lens_id)
    if not fn:
        return LensResult(lens_id=lens_id, query=query, summary=f"Unknown lens: {lens_id}", confidence=0.0)
    return fn()


def scan_coverage_gaps(
    get_conn_fn,
    theme_ids: list[str] | None = None,
) -> list[dict]:
    """Scan for coverage gaps across themes without requiring a topic query.

    Returns a list of gap dicts with keys: gap_type, theme, theme_id, detail.
    Extracted from contradiction_lens for standalone use (e.g. heartbeat).
    """
    gaps: list[dict] = []
    try:
        with get_conn_fn() as conn:
            # Get theme_ids if not provided — scan all themes
            if not theme_ids:
                rows = conn.execute(
                    "SELECT id FROM themes ORDER BY velocity DESC NULLS LAST"
                ).fetchall()
                theme_ids = [r["id"] for r in rows]

            if not theme_ids:
                return gaps

            # Over-optimistic themes: capabilities but no limitations
            over_optimistic = conn.execute(
                """SELECT t.id, t.name,
                          COUNT(DISTINCT cap.id) AS cap_count,
                          COUNT(DISTINCT lim.id) AS lim_count
                   FROM themes t
                   LEFT JOIN capabilities cap ON cap.theme_id = t.id
                   LEFT JOIN limitations lim ON lim.theme_id = t.id AND lim.severity != 'pruned'
                   WHERE t.id = ANY(%s)
                   GROUP BY t.id, t.name
                   HAVING COUNT(DISTINCT cap.id) > 0 AND COUNT(DISTINCT lim.id) = 0""",
                (theme_ids,),
            ).fetchall()

            for r in over_optimistic:
                gaps.append({
                    "gap_type": "over_optimistic",
                    "theme": r["name"],
                    "theme_id": r["id"],
                    "detail": f"{r['cap_count']} capabilities, 0 limitations",
                })

            # Blind-spot bottlenecks: no active approaches
            blind_spots = conn.execute(
                """SELECT b.id, b.description, t.name AS theme_name, t.id AS theme_id
                   FROM bottlenecks b
                   JOIN themes t ON b.theme_id = t.id
                   WHERE b.theme_id = ANY(%s)
                     AND (b.active_approaches IS NULL OR b.active_approaches = '[]'::jsonb)""",
                (theme_ids,),
            ).fetchall()

            for r in blind_spots:
                gaps.append({
                    "gap_type": "blind_spot_bottleneck",
                    "theme": r["theme_name"],
                    "theme_id": r["theme_id"],
                    "detail": r["description"][:150],
                })
    except Exception:
        logger.warning("scan_coverage_gaps failed", exc_info=True)

    return gaps


def format_lens_results_for_prompt(results: list[LensResult]) -> str:
    """Format multiple lens results into a combined context block for LLM synthesis."""
    parts = []
    for lr in results:
        if not lr.evidence_items and lr.confidence < 0.1:
            continue
        label = {
            "evidence": "Direct Evidence",
            "theme_panorama": "Landscape Panorama",
            "bridge": "Bridge Connections",
            "contradiction": "Contradictions & Coverage Gaps",
        }.get(lr.lens_id, lr.lens_id)

        parts.append(f"## {label} (confidence: {lr.confidence:.2f})")
        parts.append(lr.summary)

        # Add detailed evidence for evidence lens
        if lr.lens_id == "evidence":
            for i, item in enumerate(lr.evidence_items[:12], 1):
                sid = item.get("source_id", "?")
                claim = item.get("claim_text", "")
                snippet = item.get("evidence_snippet", "")
                line = f"{i}. [{sid[:12]}] {claim}"
                if snippet:
                    line += f'\n   Evidence: "{snippet[:200]}"'
                parts.append(line)

        # Add panorama details — wiki narrative is in summary, skip individual items
        elif lr.lens_id == "theme_panorama":
            for item in lr.evidence_items:
                if item.get("type") == "theme_narrative":
                    continue  # narrative already in summary

        # Add bridge details
        elif lr.lens_id == "bridge":
            for item in lr.evidence_items[:8]:
                if item["type"] == "cross_theme_implication":
                    parts.append(
                        f"- IMPLICATION: {item['source_theme']} -> {item['target_theme']}: "
                        f"{item.get('implication', '')[:120]}"
                    )

        parts.append("")

    return "\n".join(parts)
