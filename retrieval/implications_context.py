"""Pre-fetch context for /implications skill.

Loads all data the Claude subprocess needs for the 7-step implications
reasoning, eliminating tool-call overhead inside the subprocess.
Follows the same pattern as retrieval/topic_synthesis.py.
"""

from __future__ import annotations

import logging
from pathlib import Path

from reading_app import db
from retrieval.landscape import get_consolidated_implications

logger = logging.getLogger(__name__)

LIBRARY_DIR = Path(__file__).resolve().parent.parent / "library"


def gather_implications_context(source_id: str) -> dict | None:
    """Gather all data needed for /implications Mode A — no LLM calls.

    Returns a dict with keys: source_id, source_meta, themes, claims,
    deep_summary, landscape_json, wiki_context, anticipations,
    consolidated_implications.  Returns None if the source doesn't exist.
    """
    # Source metadata
    try:
        with db.get_conn() as conn:
            source_meta = conn.execute(
                "SELECT id, title, url, source_type, published_at FROM sources WHERE id = %s",
                (source_id,),
            ).fetchone()
    except Exception:
        logger.warning("Failed to load source meta for %s", source_id, exc_info=True)
        return None

    if not source_meta:
        return None

    # Source themes
    try:
        with db.get_conn() as conn:
            themes = conn.execute(
                """SELECT t.id, t.name, t.velocity, t.state_summary
                   FROM themes t
                   JOIN source_themes st ON t.id = st.theme_id
                   WHERE st.source_id = %s""",
                (source_id,),
            ).fetchall()
    except Exception:
        logger.warning("Failed to load themes for %s", source_id, exc_info=True)
        themes = []

    theme_ids = [t["id"] for t in themes]

    # Claims (top 50 by confidence)
    try:
        with db.get_conn() as conn:
            claims = conn.execute(
                """SELECT claim_text, section, confidence, evidence_snippet
                   FROM claims WHERE source_id = %s
                   ORDER BY confidence DESC NULLS LAST
                   LIMIT 50""",
                (source_id,),
            ).fetchall()
    except Exception:
        logger.warning("Failed to load claims for %s", source_id, exc_info=True)
        claims = []

    # Deep summary
    deep_summary = ""
    summary_path = LIBRARY_DIR / source_id / "deep_summary.md"
    if summary_path.exists():
        try:
            deep_summary = summary_path.read_text(encoding="utf-8")
        except Exception:
            logger.debug("Failed to read deep_summary.md for %s", source_id)

    # landscape.json
    landscape_json = ""
    landscape_path = LIBRARY_DIR / source_id / "landscape.json"
    if landscape_path.exists():
        try:
            landscape_json = landscape_path.read_text(encoding="utf-8")
        except Exception:
            logger.debug("Failed to read landscape.json for %s", source_id)

    # Wiki-based theme context (replaces per-theme DB assembly)
    from retrieval.wiki_retrieval import gather_wiki_context
    wiki_ctx = gather_wiki_context(theme_ids=theme_ids)

    # Open anticipations for these themes
    anticipations = []
    if theme_ids:
        try:
            with db.get_conn() as conn:
                anticipations = conn.execute(
                    """SELECT a.id, a.prediction, a.confidence, a.timeline,
                              a.theme_id, t.name AS theme_name, a.status_evidence
                       FROM anticipations a
                       JOIN themes t ON a.theme_id = t.id
                       WHERE a.theme_id = ANY(%s) AND a.status = 'open'
                       ORDER BY a.confidence DESC""",
                    (theme_ids,),
                ).fetchall()
        except Exception:
            logger.warning("Failed to load anticipations", exc_info=True)

    # Consolidated implications
    consolidated = []
    for tid in theme_ids:
        try:
            consolidated.extend(get_consolidated_implications(tid))
        except Exception:
            logger.debug("Failed to load consolidated implications for %s", tid)
    # Deduplicate by (source_theme_id, target_theme_id)
    seen = set()
    deduped = []
    for imp in consolidated:
        key = (imp["source_theme_id"], imp["target_theme_id"])
        if key not in seen:
            seen.add(key)
            deduped.append(imp)
    deduped.sort(key=lambda x: x.get("max_confidence") or 0, reverse=True)

    return {
        "source_id": source_id,
        "source_meta": dict(source_meta),
        "themes": [dict(t) for t in themes],
        "claims": [dict(c) for c in claims],
        "deep_summary": deep_summary,
        "landscape_json": landscape_json,
        "wiki_context": wiki_ctx,
        "anticipations": [dict(a) for a in anticipations],
        "consolidated_implications": deduped,
    }


def format_implications_context(ctx: dict) -> str:
    """Format a gathered implications context dict into prompt-injectable markdown."""
    parts = []

    # Source metadata
    meta = ctx["source_meta"]
    parts.append(f"### Source: {meta.get('title', meta['id'])}")
    parts.append(f"- ID: {meta['id']}")
    parts.append(f"- URL: {meta.get('url', 'N/A')}")
    parts.append(f"- Type: {meta.get('source_type', 'N/A')}")
    parts.append(f"- Published: {str(meta.get('published_at', 'N/A'))[:10]}")
    parts.append("")

    # Themes
    parts.append("### Source Themes")
    for t in ctx["themes"]:
        velocity = f", velocity: {t.get('velocity', '?')}" if t.get("velocity") else ""
        parts.append(f"- **{t['name']}** (ID: {t['id']}{velocity})")
    parts.append("")

    # Claims
    parts.append(f"### Key Claims ({len(ctx['claims'])} loaded)")
    for c in ctx["claims"][:50]:
        conf = f" (confidence: {c['confidence']:.2f})" if c.get("confidence") else ""
        parts.append(f"- [{c.get('section', '?')}] {c['claim_text']}{conf}")
        if c.get("evidence_snippet"):
            parts.append(f"  Evidence: \"{c['evidence_snippet'][:200]}\"")
    parts.append("")

    # Deep summary
    if ctx["deep_summary"]:
        parts.append("### Deep Summary")
        summary = ctx["deep_summary"][:5000]
        if len(ctx["deep_summary"]) > 5000:
            summary += "\n[...truncated]"
        parts.append(summary)
        parts.append("")

    # landscape.json
    if ctx["landscape_json"]:
        parts.append("### Source Landscape Signals (landscape.json)")
        lj = ctx["landscape_json"][:3000]
        if len(ctx["landscape_json"]) > 3000:
            lj += "\n[...truncated]"
        parts.append(f"```json\n{lj}\n```")
        parts.append("")

    # Theme landscape (wiki-based narratives)
    if ctx.get("wiki_context"):
        from retrieval.wiki_retrieval import format_wiki_context_block
        parts.append(format_wiki_context_block(ctx["wiki_context"], header="Theme Landscape"))
        parts.append("")

    # Open anticipations
    if ctx["anticipations"]:
        parts.append(f"### Open Anticipations ({len(ctx['anticipations'])})")
        for a in ctx["anticipations"][:15]:
            ev_count = len(a.get("status_evidence") or []) if isinstance(a.get("status_evidence"), list) else 0
            parts.append(
                f"- [{a.get('theme_name', '?')}] {a['prediction']} "
                f"(confidence: {a.get('confidence', '?')}, timeline: {a.get('timeline', '?')}, "
                f"evidence: {ev_count})"
            )
        parts.append("")

    # Consolidated implications
    if ctx["consolidated_implications"]:
        parts.append(f"### Existing Cross-Theme Implications ({len(ctx['consolidated_implications'])})")
        for imp in ctx["consolidated_implications"][:15]:
            parts.append(
                f"- {imp['source_theme']} -> {imp['target_theme']}: "
                f"{imp['top_implication']} "
                f"({imp['observation_count']} obs, confidence: {imp.get('max_confidence', '?')})"
            )
            if imp.get("second_perspective"):
                parts.append(f"  Also: {imp['second_perspective']}")
        parts.append("")

    return "\n".join(parts)
