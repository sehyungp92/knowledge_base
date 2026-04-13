"""Direct Python handler for /landscape jobs.

Queries the DB for theme state data and formats it as markdown.
No LLM needed — pure data retrieval and formatting.
"""

from __future__ import annotations

import time
from typing import Callable

import structlog

from gateway.models import Event, Job

logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def handle_landscape_job(
    event: Event,
    job: Job,
    config,
    executor,
    *,
    on_progress: Callable[[str], None] | None = None,
) -> str:
    """Run /landscape directly."""
    text = event.payload.get("text", "")
    log = logger.bind(job_id=job.id)
    log.info("landscape_handler_start")
    t0 = time.monotonic()

    from reading_app.db import ensure_pool
    ensure_pool()

    theme_query = _parse_command(text)
    log = log.bind(theme_query=theme_query)

    if theme_query:
        result = _landscape_for_theme(theme_query, on_progress, log)
    else:
        result = _landscape_overview(on_progress, log)

    elapsed = time.monotonic() - t0
    log.info("landscape_handler_complete", elapsed_s=round(elapsed, 1))
    return result


# ---------------------------------------------------------------------------
# Command parser
# ---------------------------------------------------------------------------

def _parse_command(text: str) -> str | None:
    """Parse '/landscape [theme]'. Returns theme query or None."""
    cleaned = text.strip()
    for prefix in ("/landscape ", "/landscape"):
        if cleaned.lower().startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
            break
    return cleaned if cleaned else None


# ---------------------------------------------------------------------------
# Theme-scoped landscape
# ---------------------------------------------------------------------------

def _landscape_for_theme(theme_query: str, on_progress, log) -> str:
    from reading_app.db import get_conn
    from retrieval.landscape import get_theme_state, get_consolidated_implications

    if on_progress:
        on_progress(f"Loading landscape for `{theme_query}`...")

    # Resolve theme by ID or name
    with get_conn() as conn:
        theme = conn.execute(
            "SELECT id, name FROM themes WHERE id = %s", (theme_query,)
        ).fetchone()
        if not theme:
            theme = conn.execute(
                "SELECT id, name FROM themes WHERE name ILIKE %s LIMIT 1",
                (f"%{theme_query}%",),
            ).fetchone()
        if not theme:
            return f"Theme not found: `{theme_query}`"

    theme_id = theme["id"]

    # Try wiki-first: if theme page is fresh, serve from wiki
    try:
        from retrieval.wiki_retrieval import gather_wiki_context
        wctx = gather_wiki_context(theme_ids=[theme_id], max_pages=1)
        staleness = wctx.freshness.get(theme_id, 1.0)
        if wctx.theme_narratives.get(theme_id) and staleness < 0.6:
            log.info("landscape_wiki_hit", theme_id=theme_id, staleness=staleness)
            wiki_body = wctx.theme_narratives[theme_id]
            header = f"**{theme.get('name', theme_query)}**: State of AI *(from wiki, freshness: {staleness:.2f})*\n"
            return header + "\n" + wiki_body
    except Exception:
        log.debug("landscape_wiki_fallback", theme_id=theme_id, exc_info=True)

    # DB fallback: original path
    state = get_theme_state(theme_id)
    t = state.get("theme") or {}
    lines = [f"**{t.get('name', theme_query)}**: State of AI\n"]

    # Trajectory
    summary = t.get("state_summary")
    if summary:
        lines.append(f"**Trajectory:**\n{summary}\n")
    else:
        src_count = _count_theme_sources(theme_id)
        if src_count < 3:
            lines.append(f"*(Limited coverage: only {src_count} sources — understanding may be incomplete)*\n")
        else:
            lines.append("*(No state summary generated yet)*\n")

    # Capabilities
    caps = state.get("capabilities", [])
    if caps:
        lines.append("**Current Capabilities:**")
        for c in caps:
            maturity = c.get("maturity", "?")
            lines.append(f"- {c.get('description', '?')} (maturity: {maturity})")
        lines.append("")

    # Limitations
    lims = state.get("limitations", [])
    if lims:
        lines.append("**Key Limitations:**")
        for l in lims:
            ltype = l.get("limitation_type", "?")
            traj = l.get("trajectory", "?")
            severity = l.get("severity", "?")
            desc = l.get("description", "?")
            line = f"- {desc} [{ltype}] — trajectory: {traj}"
            if severity:
                line += f", severity: {severity}"
            if l.get("signal_type") and l["signal_type"] != "explicit":
                line += f" (implicit: {l['signal_type']})"
            lines.append(line)
        lines.append("")

    # Bottlenecks
    bots = state.get("bottlenecks", [])
    if bots:
        lines.append("**Active Bottlenecks:**")
        for b in bots:
            horizon = b.get("resolution_horizon", "?")
            btype = b.get("bottleneck_type", "?")
            blocking = b.get("blocking_what", "?")
            approaches = b.get("active_approaches") or []
            appr_str = f" — {len(approaches)} active approach(es)" if approaches else ""
            lines.append(
                f"- {b.get('description', '?')} ({btype}) — "
                f"horizon: {horizon}, blocks: {blocking}{appr_str}"
            )
        lines.append("")

    # Breakthroughs
    brks = state.get("breakthroughs", [])
    if brks:
        lines.append("**Recent Breakthroughs** (last 90 days):")
        for br in brks:
            sig = br.get("significance", "?")
            lines.append(f"- {br.get('description', '?')} (significance: {sig})")
            if br.get("immediate_implications"):
                lines.append(f"  Implications: {br['immediate_implications']}")
        lines.append("")
    else:
        lines.append("**Recent Breakthroughs:** None in last 90 days.\n")

    # Anticipations
    ants = state.get("anticipations", [])
    if ants:
        lines.append("**Anticipations:**")
        for a in ants:
            conf = a.get("confidence", "?")
            timeline = a.get("timeline", "?")
            lines.append(
                f"- {a.get('prediction', '?')} (confidence: {conf}, timeline: {timeline})"
            )
        lines.append("")

    # Cross-theme implications
    try:
        impls = get_consolidated_implications(theme_id, limit=10)
        if impls:
            lines.append("**Connected Themes:**")
            for impl in impls:
                src = impl.get("source_theme", "?")
                tgt = impl.get("target_theme", "?")
                top = impl.get("top_implication", impl.get("implication", "?"))
                n = impl.get("observation_count", 1)
                lines.append(f"- {src} → {tgt}: {top} ({n} observation(s))")
            lines.append("")
    except Exception:
        pass

    # Footer
    velocity = t.get("velocity", "?")
    updated = t.get("state_summary_updated_at", "never")
    src_count = _count_theme_sources(theme_id)
    lines.append(f"Last updated: {updated} | Velocity: {velocity} | Sources: {src_count}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Cross-theme overview
# ---------------------------------------------------------------------------

def _landscape_overview(on_progress, log) -> str:
    from reading_app.db import get_conn

    if on_progress:
        on_progress("Loading landscape overview...")

    with get_conn() as conn:
        themes = conn.execute(
            """SELECT id, name, velocity, state_summary, state_summary_updated_at
               FROM themes ORDER BY velocity DESC NULLS LAST"""
        ).fetchall()

        total_sources = conn.execute("SELECT COUNT(*) AS cnt FROM sources").fetchone()["cnt"]

        recent_breakthroughs = conn.execute(
            """SELECT br.*, t.name AS theme_name
               FROM breakthroughs br
               JOIN themes t ON br.theme_id = t.id
               WHERE br.detected_at >= NOW() - INTERVAL '30 days'
               ORDER BY br.detected_at DESC LIMIT 10"""
        ).fetchall()

        # Anticipations with recent evidence
        active_ants = conn.execute(
            """SELECT a.*, t.name AS theme_name
               FROM anticipations a
               JOIN themes t ON a.theme_id = t.id
               WHERE a.status = 'open'
               ORDER BY a.confidence DESC LIMIT 10"""
        ).fetchall()

    lines = ["**AI Landscape Overview**\n"]

    # Themes by velocity
    if themes:
        lines.append("**Themes by Velocity:**")
        for t in themes:
            vel = t.get("velocity", "?")
            summary = t.get("state_summary") or ""
            # Extract first sentence of state_summary
            first_sentence = summary.split(".")[0].strip() + "." if summary else "No summary yet."
            if len(first_sentence) > 120:
                first_sentence = first_sentence[:117] + "..."
            lines.append(f"- **{t['name']}**: {vel} — {first_sentence}")
        lines.append("")

    # Recent breakthroughs
    if recent_breakthroughs:
        lines.append("**Recent Breakthroughs** (last 30 days):")
        for br in recent_breakthroughs:
            lines.append(f"- [{br.get('theme_name', '?')}] {br.get('description', '?')}")
        lines.append("")
    else:
        lines.append("**Recent Breakthroughs:** None in last 30 days.\n")

    # Active anticipations
    if active_ants:
        lines.append("**Active Anticipations:**")
        for a in active_ants:
            lines.append(
                f"- [{a.get('theme_name', '?')}] {a.get('prediction', '?')} "
                f"(confidence: {a.get('confidence', '?')})"
            )
        lines.append("")

    # Coverage
    themes_with_sources = sum(1 for t in themes if _count_theme_sources(t["id"]) > 0)
    lines.append(
        f"Coverage: {total_sources} sources across {themes_with_sources}/{len(themes)} themes"
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _count_theme_sources(theme_id: str) -> int:
    """Count sources linked to a theme via source_themes."""
    from reading_app.db import get_conn
    try:
        with get_conn() as conn:
            row = conn.execute(
                """SELECT COUNT(DISTINCT s.id) AS cnt
                   FROM sources s
                   JOIN source_themes st ON s.id = st.source_id
                   WHERE st.theme_id = %s""",
                (theme_id,),
            ).fetchone()
            return row["cnt"] if row else 0
    except Exception:
        return 0
