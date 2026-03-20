"""Test runner for knowledge base skills with pre-fetched DB context.

Usage:
    python -m scripts.test_skill ask "What are the main limitations of current AI agent architectures?"
    python -m scripts.test_skill landscape autonomous_agents
    python -m scripts.test_skill bottlenecks
    python -m scripts.test_skill synthesis openclaw

Pre-fetches relevant DB context and injects it into the prompt so the
Claude CLI subprocess doesn't need to figure out DB access via tools.
This makes skill execution ~10x faster than tool-based DB access.
"""

from __future__ import annotations

import io
import json
import os
import sys
import time

os.environ.setdefault("PYTHONUTF8", "1")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s - %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _row_to_dict(row) -> dict:
    """Convert a DB row to a plain dict, handling JSONB and datetime."""
    from datetime import date, datetime
    d = dict(row) if hasattr(row, 'keys') else row
    out = {}
    for k, v in d.items():
        if isinstance(v, (datetime, date)):
            out[k] = str(v)
        elif isinstance(v, list) and v and hasattr(v[0], 'keys'):
            out[k] = [dict(x) for x in v]
        else:
            out[k] = v
    return out


def _fetch_context(skill_name: str, skill_args: str) -> str:
    """Pre-fetch DB context for a skill and return it as a string to inject."""
    from reading_app.db import ensure_pool, get_conn
    ensure_pool()

    if skill_name == "ask":
        return _fetch_ask_context(skill_args)
    elif skill_name == "landscape":
        return _fetch_landscape_context(skill_args)
    elif skill_name == "bottlenecks":
        return _fetch_bottleneck_context(skill_args)
    elif skill_name == "synthesis":
        return _fetch_synthesis_context(skill_args)
    elif skill_name == "contradictions":
        return _fetch_contradiction_context(skill_args)
    elif skill_name == "map":
        return _fetch_map_context(skill_args)
    elif skill_name == "gaps":
        return _fetch_gaps_context()
    elif skill_name == "reflect":
        return _fetch_reflect_context(skill_args)
    elif skill_name == "implications":
        return _fetch_implications_context(skill_args)
    elif skill_name == "anticipate":
        return _fetch_anticipate_context(skill_args)
    elif skill_name == "beliefs":
        return _fetch_beliefs_context(skill_args)
    elif skill_name == "challenge":
        return _fetch_challenge_context(skill_args)
    elif skill_name == "enrich":
        return _fetch_enrich_context(skill_args)
    else:
        return "(No pre-fetched context for this skill)"


def _fetch_ask_context(question: str) -> str:
    """Fetch claims, sources, and landscape data relevant to the question."""
    from reading_app.db import get_conn
    parts = []
    with get_conn() as conn:
        # Search claims by keyword
        keywords = [w for w in question.split() if len(w) > 3][:5]
        kw_pattern = " | ".join(keywords)

        # FTS search on claims
        claims = conn.execute(
            """SELECT c.id, c.claim_text, c.claim_type, c.confidence,
                      c.evidence_snippet, c.source_id, s.title AS source_title
               FROM claims c
               JOIN sources s ON c.source_id = s.id
               WHERE c.fts_vector @@ to_tsquery('english', %s)
               ORDER BY ts_rank(c.fts_vector, to_tsquery('english', %s)) DESC
               LIMIT 30""",
            (kw_pattern, kw_pattern),
        ).fetchall()

        if claims:
            parts.append("## Relevant Claims (from FTS search)")
            for c in claims:
                d = _row_to_dict(c)
                parts.append(f"- [{d['source_id']}] \"{d['source_title']}\": {d['claim_text']}")
                if d.get('evidence_snippet'):
                    parts.append(f"  Evidence: \"{d['evidence_snippet'][:200]}\"")

        # Get all sources for reference
        sources = conn.execute(
            "SELECT id, title, source_type, url FROM sources ORDER BY id"
        ).fetchall()
        parts.append("\n## Library Sources")
        for s in sources:
            d = _row_to_dict(s)
            parts.append(f"- [{d['id']}] \"{d['title']}\" ({d['source_type']})")

        # Relevant capabilities and limitations
        caps = conn.execute(
            "SELECT description, theme_id, maturity, confidence FROM capabilities ORDER BY confidence DESC LIMIT 20"
        ).fetchall()
        lims = conn.execute(
            "SELECT description, theme_id, severity, trajectory FROM limitations ORDER BY severity ASC LIMIT 20"
        ).fetchall()

        if caps:
            parts.append("\n## Capabilities")
            for c in caps:
                d = _row_to_dict(c)
                parts.append(f"- [{d['theme_id']}] {d['description']} (maturity: {d.get('maturity', '?')})")

        if lims:
            parts.append("\n## Limitations")
            for l in lims:
                d = _row_to_dict(l)
                parts.append(f"- [{d['theme_id']}] {d['description']} (severity: {d.get('severity', '?')}, trajectory: {d.get('trajectory', '?')})")

    return "\n".join(parts)


def _fetch_landscape_context(theme_id: str) -> str:
    """Fetch full landscape state for a theme."""
    from retrieval.landscape import get_theme_state, get_consolidated_implications
    parts = []

    if not theme_id:
        # Full overview mode
        from retrieval.landscape import compute_theme_velocity, get_recent_breakthroughs
        velocities = compute_theme_velocity()
        breakthroughs = get_recent_breakthroughs(days=90)

        parts.append("## Theme Velocities")
        for v in velocities:
            d = _row_to_dict(v)
            parts.append(f"- {d['name']} (id={d['id']}): velocity={d.get('velocity', 0)}, sources={d.get('total_sources', 0)}")

        if breakthroughs:
            parts.append("\n## Recent Breakthroughs (90 days)")
            for b in breakthroughs:
                d = _row_to_dict(b)
                parts.append(f"- [{d.get('theme_name')}] {d['description']} (significance: {d.get('significance')})")
        return "\n".join(parts)

    state = get_theme_state(theme_id)
    if not state.get("theme"):
        return f"Theme '{theme_id}' not found in database."

    theme = _row_to_dict(state["theme"])
    parts.append(f"## Theme: {theme.get('name', theme_id)}")
    parts.append(f"State summary: {theme.get('state_summary', '(none)')}")
    parts.append(f"Velocity: {theme.get('velocity', 'unknown')}")

    for label, key in [("Capabilities", "capabilities"), ("Limitations", "limitations"),
                        ("Bottlenecks", "bottlenecks"), ("Breakthroughs", "breakthroughs"),
                        ("Anticipations", "anticipations")]:
        items = state.get(key, [])
        if items:
            parts.append(f"\n## {label} ({len(items)})")
            for item in items:
                d = _row_to_dict(item)
                parts.append(f"- {json.dumps(d, default=str, ensure_ascii=False)[:300]}")

    # Consolidated implications
    try:
        implications = get_consolidated_implications(theme_id)
        if implications:
            parts.append(f"\n## Cross-Theme Implications ({len(implications)})")
            for imp in implications:
                d = _row_to_dict(imp)
                parts.append(f"- {d.get('source_theme', '?')} -> {d.get('target_theme', '?')} (conf={d.get('max_confidence')}, n={d.get('observation_count')}): {d.get('top_implication', '')[:150]}")
    except Exception:
        pass

    # Source count
    from reading_app.db import get_conn
    with get_conn() as conn:
        src_count = conn.execute(
            "SELECT count(*) as cnt FROM source_themes WHERE theme_id = %s",
            (theme_id,),
        ).fetchone()
        parts.append(f"\nSources covering this theme: {_row_to_dict(src_count)['cnt']}")

    return "\n".join(parts)


def _fetch_bottleneck_context(theme_filter: str) -> str:
    """Fetch ranked bottlenecks."""
    from retrieval.landscape import get_bottleneck_ranking
    theme_id = theme_filter.strip() if theme_filter.strip() else None
    bottlenecks = get_bottleneck_ranking(theme_id)
    parts = [f"## Bottlenecks (ranked by leverage) {'for ' + theme_id if theme_id else 'all themes'}"]
    for b in bottlenecks:
        d = _row_to_dict(b)
        parts.append(f"- [{d.get('theme_name')}] {d['description']}")
        parts.append(f"  Type: {d.get('bottleneck_type')}, Horizon: {d.get('resolution_horizon')}, Confidence: {d.get('confidence')}")
        parts.append(f"  Blocks: {d.get('blocking_what', '?')}")
        if d.get('active_approaches'):
            parts.append(f"  Active approaches: {json.dumps(d['active_approaches'], default=str)[:200]}")
        if d.get('evidence_sources'):
            parts.append(f"  Evidence: {json.dumps(d['evidence_sources'], default=str)[:200]}")
    return "\n".join(parts)


def _fetch_synthesis_context(topic: str) -> str:
    """Fetch all data for a synthesis report as compact reference blocks.

    Returns just the data — NOT the full SYNTHESIS_PROMPT template, since
    the skill prompt (synthesis.md) already contains synthesis instructions.
    format_synthesis_context() is only for the direct executor path.
    """
    from retrieval.topic_synthesis import gather_synthesis_context, _slugify
    import json as _json
    ctx = gather_synthesis_context(topic)
    if ctx is None:
        return f"No sources or summaries found for topic: \"{topic}\""

    parts = []

    # Check if cache is stale/empty and signal it
    cache_path = PROJECT_ROOT / "library" / "syntheses" / f"{_slugify(topic)}.md"
    if cache_path.exists():
        content = cache_path.read_text(encoding="utf-8").strip()
        if len(content) > 100:
            parts.append(f"### Cached Report\nA cached synthesis exists at {cache_path} ({len(content)} chars). The skill should return this if fresh (<24h).")
        else:
            parts.append("### Cache Status\nNo valid cached report exists. Generate a new report from the data above.")
    else:
        parts.append("### Cache Status\nNo cached report exists. Generate a new report from the data below.")

    # Sources
    indexed = ctx["indexed_sources"]
    parts.append(f"\n## Pre-Fetched Synthesis Data\n\nTopic: {topic}\nSources: {len(indexed)}\n")
    parts.append("### Sources")
    for i, s in enumerate(indexed):
        parts.append(f"- Source {i+1}: \"{s.get('title', s['source_id'])}\" (ID: {s['source_id']}, published: {str(s.get('published_at', '?'))[:10]})")

    # Summaries (truncated per source)
    parts.append("\n### Deep Summaries")
    max_chars = 3000
    for i, (sid, text) in enumerate(ctx["summaries"].items()):
        title = next((s.get("title", sid) for s in ctx["sources"] if s["source_id"] == sid), sid)
        trunc = text[:max_chars]
        if len(text) > max_chars:
            trunc += "\n[...truncated]"
        parts.append(f"\n#### Source {i+1}: \"{title}\"\n\n{trunc}")

    # Evidence
    parts.append("\n### Key Evidence")
    for i, src in enumerate(indexed):
        sid = src["source_id"]
        snippets = ctx["evidence"].get(sid, [])
        if snippets:
            parts.append(f"\n**Source {i+1}** evidence:")
            for ev in snippets[:5]:
                parts.append(f"- {ev['claim'][:150]}")
                if ev.get("snippet"):
                    parts.append(f"  \"{ev['snippet'][:200]}\"")

    # Landscape signals (compact)
    landscape = ctx["landscape"]
    if landscape["capabilities"]:
        parts.append(f"\n### Capabilities ({len(landscape['capabilities'])})")
        for c in landscape["capabilities"][:15]:
            parts.append(f"- {c['description'][:120]} (maturity: {c.get('maturity', '?')})")

    if landscape["limitations"]:
        parts.append(f"\n### Limitations ({len(landscape['limitations'])})")
        for l in landscape["limitations"][:15]:
            parts.append(f"- {l['description'][:120]} (severity: {l.get('severity', '?')}, trajectory: {l.get('trajectory', '?')})")

    if landscape["bottlenecks"]:
        parts.append(f"\n### Bottlenecks ({len(landscape['bottlenecks'])})")
        for b in landscape["bottlenecks"][:10]:
            parts.append(f"- {b['description'][:120]} (horizon: {b.get('resolution_horizon', '?')})")

    # Implications
    implications = ctx["implications"]
    if implications:
        parts.append(f"\n### Cross-Theme Implications ({len(implications)})")
        for imp in implications[:10]:
            parts.append(f"- {imp.get('source_theme', '?')} -> {imp.get('target_theme', '?')}: {imp.get('top_implication', '')[:120]} (conf: {imp.get('max_confidence', '?')})")

    # Anticipations
    ants = landscape.get("anticipations", [])
    if ants:
        parts.append(f"\n### Anticipations ({len(ants)})")
        for a in ants:
            parts.append(f"- {a['prediction'][:120]} (conf: {a.get('confidence', '?')})")
    else:
        parts.append("\n### Anticipations\nNone active.")

    return "\n".join(parts)


def _fetch_contradiction_context(topic: str) -> str:
    """Fetch claims that might contradict each other."""
    from reading_app.db import get_conn
    parts = []
    with get_conn() as conn:
        # Provide claims for contradiction detection
        if topic:
            claims = conn.execute(
                """SELECT c.claim_text, c.source_id, s.title, c.confidence
                   FROM claims c JOIN sources s ON c.source_id = s.id
                   WHERE c.claim_text ILIKE %s OR c.fts_vector @@ to_tsquery('english', %s)
                   ORDER BY c.confidence DESC LIMIT 40""",
                (f"%{topic}%", topic),
            ).fetchall()
            parts.append(f"\n## Claims matching '{topic}' for contradiction analysis ({len(claims)})")
            for c in claims:
                d = _row_to_dict(c)
                parts.append(f"- [{d['source_id']}] \"{d['title']}\": {d['claim_text'][:150]}")

    return "\n".join(parts)


def _fetch_map_context(source_id: str) -> str:
    """Fetch knowledge graph neighborhood for a source."""
    from reading_app.db import get_conn
    parts = []
    with get_conn() as conn:
        src = conn.execute("SELECT id, title, source_type FROM sources WHERE id = %s", (source_id,)).fetchone()
        if not src:
            return f"Source '{source_id}' not found."
        d = _row_to_dict(src)
        parts.append(f"## Source: [{d['id']}] \"{d['title']}\" ({d['source_type']})")

        # Shared concepts
        concepts = conn.execute(
            """SELECT sc.concept_id, c.canonical_name, c.concept_type
               FROM source_concepts sc
               JOIN concepts c ON sc.concept_id = c.id
               WHERE sc.source_id = %s""",
            (source_id,),
        ).fetchall()
        parts.append(f"\n## Concepts ({len(concepts)})")
        for c in concepts:
            d = _row_to_dict(c)
            parts.append(f"- {d['canonical_name']} ({d.get('concept_type', '?')})")

        # Connected sources via shared concepts
        connected = conn.execute(
            """SELECT DISTINCT s.id, s.title, s.source_type, COUNT(*) AS shared_concepts
               FROM source_concepts sc1
               JOIN source_concepts sc2 ON sc1.concept_id = sc2.concept_id AND sc1.source_id != sc2.source_id
               JOIN sources s ON sc2.source_id = s.id
               WHERE sc1.source_id = %s
               GROUP BY s.id, s.title, s.source_type
               ORDER BY shared_concepts DESC""",
            (source_id,),
        ).fetchall()
        parts.append(f"\n## Connected Sources ({len(connected)})")
        for c in connected:
            d = _row_to_dict(c)
            parts.append(f"- [{d['id']}] \"{d['title']}\" — {d['shared_concepts']} shared concepts")

    return "\n".join(parts)


def _fetch_gaps_context() -> str:
    """Fetch coverage gap data."""
    from retrieval.landscape import (
        get_theme_source_counts, get_over_optimistic_themes,
        get_blind_spot_bottlenecks, get_unlinked_themes,
        get_validation_backlog,
    )
    from reading_app.db import get_conn
    parts = []

    source_counts = get_theme_source_counts()
    parts.append("## Theme Source Counts")
    for sc in source_counts:
        d = _row_to_dict(sc)
        parts.append(f"- {d['name']}: {d['source_count']} sources (velocity: {d.get('velocity', '?')})")

    over_optimistic = get_over_optimistic_themes()
    if over_optimistic:
        parts.append("\n## Over-Optimistic Themes (capabilities without limitations)")
        for t in over_optimistic:
            d = _row_to_dict(t)
            parts.append(f"- {d['name']}: {d['capability_count']} caps, {d['limitation_count']} lims")

    blind_spots = get_blind_spot_bottlenecks()
    if blind_spots:
        parts.append(f"\n## Blind-Spot Bottlenecks (no active approaches) ({len(blind_spots)})")
        for b in blind_spots:
            d = _row_to_dict(b)
            parts.append(f"- [{d.get('theme_name')}] {d['description']}")

    unlinked = get_unlinked_themes()
    if unlinked:
        parts.append(f"\n## Unlinked Themes (no cross-theme implications) ({len(unlinked)})")
        for t in unlinked:
            d = _row_to_dict(t)
            parts.append(f"- {d['name']}: {d['source_count']} sources")

    backlog = get_validation_backlog()
    if backlog:
        parts.append(f"\n## Validation Backlog (unvalidated implicit limitations)")
        for v in backlog:
            d = _row_to_dict(v)
            parts.append(f"- {d['theme_name']}: {d['unvalidated_count']} unvalidated")

    # Check anticipations and beliefs
    with get_conn() as conn:
        ant_count = conn.execute("SELECT count(*) as cnt FROM anticipations").fetchone()
        bel_count = conn.execute("SELECT count(*) as cnt FROM beliefs").fetchone()
        parts.append(f"\n## System State")
        parts.append(f"Anticipations: {_row_to_dict(ant_count)['cnt']}")
        parts.append(f"Beliefs: {_row_to_dict(bel_count)['cnt']}")

    return "\n".join(parts)


def _fetch_reflect_context(source_id: str) -> str:
    """Fetch source and connected data for reflection."""
    from reading_app.db import get_conn
    parts = []
    with get_conn() as conn:
        src = conn.execute("SELECT * FROM sources WHERE id = %s", (source_id,)).fetchone()
        if not src:
            return f"Source '{source_id}' not found."
        d = _row_to_dict(src)
        parts.append(f"## Source: [{d['id']}] \"{d['title']}\"")

        # Claims from this source
        claims = conn.execute(
            "SELECT claim_text, claim_type, confidence, evidence_snippet FROM claims WHERE source_id = %s ORDER BY confidence DESC LIMIT 30",
            (source_id,),
        ).fetchall()
        parts.append(f"\n## Claims ({len(claims)})")
        for c in claims:
            cd = _row_to_dict(c)
            parts.append(f"- {cd['claim_text'][:150]}")

        # Connected sources
        connected = conn.execute(
            """SELECT DISTINCT s.id, s.title, COUNT(*) AS shared
               FROM source_concepts sc1
               JOIN source_concepts sc2 ON sc1.concept_id = sc2.concept_id AND sc1.source_id != sc2.source_id
               JOIN sources s ON sc2.source_id = s.id
               WHERE sc1.source_id = %s
               GROUP BY s.id, s.title ORDER BY shared DESC""",
            (source_id,),
        ).fetchall()
        if connected:
            parts.append(f"\n## Connected Sources ({len(connected)})")
            for cs in connected:
                cd = _row_to_dict(cs)
                parts.append(f"- [{cd['id']}] \"{cd['title']}\" ({cd['shared']} shared concepts)")

        # Read deep summary if available
        lib_path = d.get('library_path', '')
        if lib_path:
            summary_path = Path(lib_path) / "deep_summary.md"
            if summary_path.exists():
                summary = summary_path.read_text(encoding="utf-8")[:3000]
                parts.append(f"\n## Deep Summary (truncated)\n{summary}")

    return "\n".join(parts)


def _fetch_implications_context(args: str) -> str:
    """Fetch context for implications analysis."""
    parts_list = args.split(None, 1)
    source_id = parts_list[0] if parts_list else ""
    from reading_app.db import get_conn
    parts = []
    with get_conn() as conn:
        src = conn.execute("SELECT id, title FROM sources WHERE id = %s", (source_id,)).fetchone()
        if src:
            d = _row_to_dict(src)
            parts.append(f"## Source: [{d['id']}] \"{d['title']}\"")
        # Existing implications from this source
        imps = conn.execute(
            "SELECT * FROM cross_theme_implications WHERE evidence_sources::text LIKE %s",
            (f"%{source_id}%",),
        ).fetchall()
        parts.append(f"\n## Existing implications referencing this source: {len(imps)}")
        for i in imps:
            d = _row_to_dict(i)
            parts.append(f"- {d.get('source_theme_id')} -> {d.get('target_theme_id')}: {d.get('implication', '')[:120]}")
    return "\n".join(parts)


def _fetch_anticipate_context(args: str) -> str:
    parts = args.split()
    mode = parts[0] if parts else "generate"
    theme_id = parts[1] if len(parts) > 1 else None
    from reading_app.db import get_conn
    from retrieval.landscape import get_bottleneck_ranking, get_recent_breakthroughs
    ctx = []
    if theme_id:
        bottlenecks = get_bottleneck_ranking(theme_id)
        breakthroughs = get_recent_breakthroughs(theme_id=theme_id)
        ctx.append(f"## Bottlenecks for {theme_id} ({len(bottlenecks)})")
        for b in bottlenecks:
            d = _row_to_dict(b)
            ctx.append(f"- {d['description']} (horizon: {d.get('resolution_horizon')}, type: {d.get('bottleneck_type')})")
        if breakthroughs:
            ctx.append(f"\n## Recent Breakthroughs ({len(breakthroughs)})")
            for b in breakthroughs:
                d = _row_to_dict(b)
                ctx.append(f"- {d['description']} (significance: {d.get('significance')})")
    with get_conn() as conn:
        existing = conn.execute("SELECT prediction, confidence, timeline, theme_id FROM anticipations ORDER BY confidence DESC").fetchall()
        ctx.append(f"\n## Existing Anticipations ({len(existing)})")
        for a in existing:
            d = _row_to_dict(a)
            ctx.append(f"- [{d.get('theme_id')}] {d['prediction'][:100]} (conf={d.get('confidence')}, timeline={d.get('timeline')})")
    return "\n".join(ctx)


def _fetch_beliefs_context(args: str) -> str:
    from reading_app.db import get_conn
    parts = []
    with get_conn() as conn:
        beliefs = conn.execute("SELECT * FROM beliefs ORDER BY confidence DESC").fetchall()
        parts.append(f"## Current Beliefs ({len(beliefs)})")
        for b in beliefs:
            d = _row_to_dict(b)
            parts.append(f"- [{d.get('id', '?')}] {d.get('claim', d.get('belief_text', ''))[:120]} (conf={d.get('confidence')}, type={d.get('belief_type')})")
    return "\n".join(parts)


def _fetch_challenge_context(args: str) -> str:
    parts = args.split()
    entity_type = parts[0] if parts else ""
    entity_id = parts[1] if len(parts) > 1 else ""
    from reading_app.db import get_conn
    ctx = []
    with get_conn() as conn:
        if entity_type == "bottleneck" and entity_id:
            row = conn.execute("SELECT * FROM bottlenecks WHERE id = %s", (entity_id,)).fetchone()
            if row:
                d = _row_to_dict(row)
                ctx.append(f"## Bottleneck: {d['description']}")
                ctx.append(f"Type: {d.get('bottleneck_type')}, Horizon: {d.get('resolution_horizon')}")
                ctx.append(f"Blocking: {d.get('blocking_what')}")
                ctx.append(f"Evidence: {json.dumps(d.get('evidence_sources', []), default=str)[:300]}")
        elif entity_type == "belief" and entity_id:
            row = conn.execute("SELECT * FROM beliefs WHERE id = %s", (entity_id,)).fetchone()
            if row:
                d = _row_to_dict(row)
                ctx.append(f"## Belief: {d.get('claim', d.get('belief_text', ''))[:200]}")
                ctx.append(f"Confidence: {d.get('confidence')}, Type: {d.get('belief_type')}")
    return "\n".join(ctx)


def _fetch_enrich_context(source_id: str) -> str:
    from reading_app.db import get_conn
    parts = []
    with get_conn() as conn:
        src = conn.execute("SELECT id, title FROM sources WHERE id = %s", (source_id,)).fetchone()
        if src:
            d = _row_to_dict(src)
            parts.append(f"## Source: [{d['id']}] \"{d['title']}\"")
        claims = conn.execute("SELECT claim_text FROM claims WHERE source_id = %s LIMIT 20", (source_id,)).fetchall()
        caps = conn.execute("SELECT description FROM capabilities WHERE evidence_sources::text LIKE %s LIMIT 10", (f"%{source_id}%",)).fetchall()
        lims = conn.execute("SELECT description FROM limitations WHERE evidence_sources::text LIKE %s LIMIT 10", (f"%{source_id}%",)).fetchall()
        parts.append(f"\nClaims: {len(claims)}, Capabilities: {len(caps)}, Limitations: {len(lims)}")
        parts.append("\n## Claims")
        for c in claims:
            parts.append(f"- {_row_to_dict(c)['claim_text'][:100]}")
        if caps:
            parts.append("\n## Capabilities")
            for c in caps:
                parts.append(f"- {_row_to_dict(c)['description'][:100]}")
        if lims:
            parts.append("\n## Limitations")
            for l in lims:
                parts.append(f"- {_row_to_dict(l)['description'][:100]}")
    return "\n".join(parts)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Test a knowledge base skill")
    parser.add_argument("skill", help="Skill name")
    parser.add_argument("args", nargs="*", help="Arguments for the skill")
    parser.add_argument("--model", default=None, help="Model override")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout in seconds")
    parser.add_argument("-o", "--output", help="Output file path")
    args = parser.parse_args()

    skill_name = args.skill
    skill_args = " ".join(args.args) if args.args else ""
    user_text = f"/{skill_name} {skill_args}".strip()

    # Load skill prompt
    prompt_path = PROJECT_ROOT / "skills" / "prompts" / f"{skill_name}.md"
    if not prompt_path.exists():
        logger.error("Skill prompt not found: %s", prompt_path)
        sys.exit(1)

    skill_text = prompt_path.read_text(encoding="utf-8")
    if skill_text.startswith("---"):
        end = skill_text.find("---", 3)
        if end > 0:
            skill_text = skill_text[end + 3:].strip()

    # Pre-fetch DB context
    logger.info("Pre-fetching DB context for /%s...", skill_name)
    db_context = _fetch_context(skill_name, skill_args)
    logger.info("Context fetched (%d chars)", len(db_context))

    # Build prompt with injected context
    prompt = f"""# Context

## Pre-fetched Database Context
{db_context}

---

## Current Event
Type: message
Payload: {json.dumps({"text": user_text})}

---

## Skill Instructions
{skill_text}

---

## Important Rules
- All DB context has been pre-fetched above. DO NOT try to query the database.
- DO NOT use Bash to run Python scripts. All data you need is in the context above.
- Use the pre-fetched data to answer. Use Read/Glob only if you need to read library files.
- Always cite evidence snippets for any claim you make.

Now execute the skill for this event.
"""

    # Load skill config
    from skills import SkillRegistry
    registry = SkillRegistry()
    skill_config = registry.skills.get(skill_name)
    timeout = args.timeout or (skill_config.timeout if skill_config else 120)

    # Build executor
    from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
    executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    logger.info("Running /%s (timeout=%ds, model=%s)", skill_name, timeout, args.model or "default")
    t0 = time.monotonic()

    result = executor.run_raw(
        prompt,
        session_id=f"test_{skill_name}_{int(time.time())}",
        model=args.model,
        timeout=timeout,
    )

    elapsed = time.monotonic() - t0

    if result.is_timeout:
        logger.error("Skill timed out after %ds", timeout)
        output = f"# TIMEOUT after {timeout}s\n\nPartial output:\n{result.text[:2000]}"
    elif not result.success:
        logger.error("Skill failed (rc=%d): %s", result.return_code, result.stderr[:500])
        output = f"# ERROR (rc={result.return_code})\n\n{result.text or result.stderr}"
    else:
        output = result.text
        logger.info("Skill completed in %.1fs (%d chars output)", elapsed, len(output))

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        logger.info("Output written to %s", args.output)
    else:
        print(output)


if __name__ == "__main__":
    main()
