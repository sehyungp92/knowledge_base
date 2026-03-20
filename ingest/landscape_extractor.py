"""Landscape signal extraction from source text.

Extracts capabilities, limitations (explicit + implicit), and bottlenecks
from ingested source text. Called during /save after claim extraction.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

from agents.base import BaseAgent
from ingest.json_parser import parse_json_from_llm
from ingest.section_slicer import budget_for_source_type, prioritized_slice, timeout_for_text
from ingest.theme_validator import load_valid_theme_ids, resolve_theme_id

logger = logging.getLogger(__name__)

# Landscape extraction prioritizes sections where limitations and future work
# live — these are systematically lost by naive truncation.
LANDSCAPE_PRIORITIES = {
    "limitations": 2,
    "future work": 2,
    "discussion": 3,
    "conclusion": 3,
    "conclusions": 3,
    "error analysis": 2,
    "failure analysis": 2,
    "ablation": 3,
    "cost": 3,
    "scalability": 3,
}

@dataclass
class LandscapeDelta:
    """Rich delta report from landscape signal persistence.

    Tracks exactly what changed: new vs merged entities, maturity changes,
    breakthrough effects, anticipation matches. The .counts property provides
    backward-compatible summary dict.
    """
    new_capabilities: list[dict] = field(default_factory=list)
    merged_capabilities: list[dict] = field(default_factory=list)
    maturity_changes: list[dict] = field(default_factory=list)
    new_limitations: list[dict] = field(default_factory=list)
    merged_limitations: list[dict] = field(default_factory=list)
    new_bottlenecks: list[dict] = field(default_factory=list)
    merged_bottlenecks: list[dict] = field(default_factory=list)
    breakthroughs: list[dict] = field(default_factory=list)
    bottleneck_propagations: list[dict] = field(default_factory=list)
    anticipation_matches: list[dict] = field(default_factory=list)

    @property
    def counts(self) -> dict:
        """Backward-compatible summary counts."""
        return {
            "capabilities": len(self.new_capabilities) + len(self.merged_capabilities),
            "limitations": len(self.new_limitations) + len(self.merged_limitations),
            "bottlenecks": len(self.new_bottlenecks) + len(self.merged_bottlenecks),
            "breakthroughs": len(self.breakthroughs),
            "merged": {
                "capabilities": len(self.merged_capabilities),
                "limitations": len(self.merged_limitations),
                "bottlenecks": len(self.merged_bottlenecks),
            },
        }

    def summary_text(self) -> str:
        """Human-readable delta narrative for /save responses."""
        parts = []
        if self.new_capabilities:
            descs = [c.get("description", "?")[:80] for c in self.new_capabilities]
            parts.append(f"**New capabilities ({len(descs)}):** " + "; ".join(descs))
        if self.merged_capabilities:
            parts.append(f"**Updated capabilities:** {len(self.merged_capabilities)} merged with existing")
        if self.maturity_changes:
            for mc in self.maturity_changes:
                parts.append(f"**Maturity change:** {mc.get('description', '?')[:60]} "
                             f"({mc.get('old_maturity')} -> {mc.get('new_maturity')})")
        if self.new_limitations:
            implicit = [l for l in self.new_limitations if l.get("signal_type", "").startswith("implicit")]
            explicit = [l for l in self.new_limitations if not l.get("signal_type", "").startswith("implicit")]
            if explicit:
                parts.append(f"**New explicit limitations:** {len(explicit)}")
            if implicit:
                parts.append(f"**New implicit limitations:** {len(implicit)}")
        if self.merged_limitations:
            parts.append(f"**Updated limitations:** {len(self.merged_limitations)} merged")
        if self.new_bottlenecks:
            parts.append(f"**New bottlenecks:** {len(self.new_bottlenecks)}")
        if self.breakthroughs:
            for bt in self.breakthroughs:
                parts.append(f"**Breakthrough:** {bt.get('description', '?')[:80]} "
                             f"(significance: {bt.get('significance', '?')})")
        if self.bottleneck_propagations:
            parts.append(f"**Bottleneck updates:** {len(self.bottleneck_propagations)} "
                         f"bottlenecks affected by breakthroughs")
        if self.anticipation_matches:
            parts.append(f"**Anticipation matches:** {len(self.anticipation_matches)}")
        return "\n".join(parts) if parts else "No landscape changes detected."


LANDSCAPE_EXTRACTION_PROMPT = """Analyze the following source text and extract landscape signals about the current state of AI.

{temporal_context}

Extract four types of signals:

## 1. Capabilities
What AI systems can now do, as demonstrated or claimed in this source.
For each capability:
- description: clear statement of what's possible
- theme_id: which theme this belongs to (from the list below)
- maturity: one of research_only, demo, narrow_production, broad_production, commoditized
- maturity_evidence: specific evidence grounding the maturity classification (e.g. "deployed in production at X" or "only tested on benchmark Y") (optional)
- first_demonstrated_at: approximate date or year this capability was first shown (if mentioned in source), e.g. "2023-Q3"
- production_ready_at: approximate date or year this reached production use (if mentioned), e.g. "2024"
- temporal_marker: brief string capturing when this was observed, e.g. "as of Q3 2024" or "March 2025" (optional)
- confidence: 0.0-1.0
- evidence_snippet: verbatim quote from source

## 2. Limitations
What AI systems CANNOT do or where they struggle. Extract BOTH explicit and implicit signals.

Explicit signals: stated directly in "Limitations", "Future work", caveats.
Implicit signals (MORE VALUABLE — look carefully for these):
- Performance cliffs: where the approach fails or degrades
- Controlled conditions: assumptions that success depends on (lab vs real-world, dataset-specific)
- Conspicuous absences: what is NOT discussed but should be (security, real-world testing, contamination)
- Hedging language: "preliminary results suggest...", "under certain conditions..."
- Scale and cost: training cost, inference latency, data requirements buried in appendices

For each limitation:
- description: clear, specific claim about what's limited
- theme_id: which theme
- limitation_type: architectural, data, compute, theoretical, engineering, unknown
- signal_type: explicit, implicit_performance_cliff, implicit_controlled_conditions, implicit_conspicuous_absence, implicit_hedging, implicit_scale_cost
- severity: blocking, significant, minor, workaround_exists
- trajectory: improving, stable, worsening, unclear
- related_bottleneck: brief description of the bottleneck this limitation relates to, if any (helps pre-link limitations to bottlenecks) (optional)
- temporal_marker: brief string capturing when this was observed, e.g. "as of Q3 2024" (optional)
- confidence: 0.0-1.0
- evidence_snippet: verbatim quote (for implicit: quote the passage that reveals it)
- underlying_reason: why this limitation exists (optional)

## 3. Bottlenecks
Key constraints that are blocking progress in a theme.
For each bottleneck:
- description: what's blocked and why
- theme_id: which theme
- blocking_what: what capability or progress this blocks
- bottleneck_type: compute, data, algorithmic, hardware, theoretical, regulatory, integration
- resolution_horizon: months, 1-2_years, 3-5_years, 5+_years, unknown, possibly_fundamental
- temporal_marker: brief string capturing when this was observed, e.g. "as of Q3 2024" (optional)
- confidence: 0.0-1.0
- evidence_snippet: verbatim quote

## 4. Breakthroughs
Significant advances that change what was believed possible.
Only flag genuine breakthroughs — not incremental improvements.

For each breakthrough:
- description: clear statement of what changed
- theme_id: which theme
- significance: incremental, notable, major, paradigm_shifting
- what_was_believed_before: the prior consensus or state
- what_is_now_possible: what this enables
- bottlenecks_affected: list of objects [{{"bottleneck_id": "snake_case slug matching a known bottleneck description", "effect": "resolves"|"reduces"|"reframes"}}] — or empty array
- immediate_implications: list of strings — direct consequences
- downstream_implications: list of strings — second-order effects
- temporal_marker: brief string capturing when this was observed, e.g. "as of Q3 2024" (optional)
- confidence: 0.0-1.0
- evidence_snippet: verbatim quote from source

## Available themes:
{theme_block}

Return a JSON object with four arrays:
```json
{{
  "capabilities": [...],
  "limitations": [...],
  "bottlenecks": [...],
  "breakthroughs": [...]
}}
```

Be thorough but precise. Only include signals with genuine evidence in the text.
Limitations are the most valuable signal — extract ALL implicit ones you can find.

SOURCE TEXT (truncated):
{text}
"""

# Valid enum values for validation
VALID_MATURITY = {"research_only", "demo", "narrow_production", "broad_production", "commoditized"}
VALID_LIMITATION_TYPE = {"architectural", "data", "compute", "theoretical", "engineering", "behavioral", "evaluation", "unknown"}
VALID_SIGNAL_TYPE = {
    "explicit", "implicit_performance_cliff", "implicit_controlled_conditions",
    "implicit_conspicuous_absence", "implicit_hedging", "implicit_scale_cost",
}
VALID_SEVERITY = {"blocking", "significant", "minor", "workaround_exists"}
VALID_TRAJECTORY = {"improving", "stable", "worsening", "unclear"}
VALID_BOTTLENECK_TYPE = {"compute", "data", "algorithmic", "hardware", "theoretical", "regulatory", "integration"}
VALID_RESOLUTION_HORIZON = {"months", "1-2_years", "3-5_years", "5+_years", "unknown", "possibly_fundamental"}
VALID_SIGNIFICANCE = {"incremental", "notable", "major", "paradigm_shifting"}


def _build_landscape_context(source_themes: list[str]) -> str:
    """Build existing landscape state context for themes so the LLM can
    reference actual bottleneck IDs and detect maturity changes.

    Returns a prompt section string (empty if no context available).
    """
    if not source_themes:
        return ""

    try:
        from reading_app.db import get_conn
    except Exception:
        return ""

    parts = []
    try:
        with get_conn() as conn:
            # Existing bottlenecks (most important — enables ID-based linking)
            bottlenecks = conn.execute(
                """SELECT id, description, resolution_horizon, bottleneck_type, blocking_what
                   FROM bottlenecks WHERE theme_id = ANY(%s)
                   ORDER BY confidence DESC NULLS LAST LIMIT 30""",
                (source_themes,),
            ).fetchall()
            if bottlenecks:
                bn_lines = []
                for b in bottlenecks:
                    bn_lines.append(
                        f"- ID: {b['id']} | \"{b['description'][:120]}\" "
                        f"(type: {b.get('bottleneck_type', '?')}, "
                        f"horizon: {b.get('resolution_horizon', '?')})"
                    )
                parts.append("**Known Bottlenecks:**\n" + "\n".join(bn_lines))

            # Existing capabilities (for maturity change detection)
            capabilities = conn.execute(
                """SELECT id, description, maturity
                   FROM capabilities WHERE theme_id = ANY(%s)
                   ORDER BY confidence DESC NULLS LAST LIMIT 30""",
                (source_themes,),
            ).fetchall()
            if capabilities:
                cap_lines = []
                for c in capabilities:
                    cap_lines.append(
                        f"- ID: {c['id']} | \"{c['description'][:120]}\" "
                        f"(maturity: {c.get('maturity', '?')})"
                    )
                parts.append("**Existing Capabilities:**\n" + "\n".join(cap_lines))

            # Open anticipations
            anticipations = conn.execute(
                """SELECT id, prediction, confidence, timeline
                   FROM anticipations WHERE theme_id = ANY(%s) AND status = 'open'
                   ORDER BY confidence DESC LIMIT 15""",
                (source_themes,),
            ).fetchall()
            if anticipations:
                ant_lines = []
                for a in anticipations:
                    ant_lines.append(
                        f"- ID: {a['id']} | \"{a['prediction'][:120]}\" "
                        f"(confidence: {a.get('confidence', '?')}, "
                        f"timeline: {a.get('timeline', '?')})"
                    )
                parts.append("**Open Anticipations:**\n" + "\n".join(ant_lines))
    except Exception:
        logger.debug("Failed to build landscape context", exc_info=True)

    if not parts:
        return ""

    return (
        "\n\n## Existing Landscape State\n"
        "Use this to reference ACTUAL entity IDs. For breakthroughs, use real bottleneck IDs "
        "from below in bottlenecks_affected. For capabilities matching an existing one, "
        "note if the maturity level has changed.\n\n"
        + "\n\n".join(parts)
    )


def extract_landscape_signals(
    clean_text: str,
    source_id: str,
    source_themes: list[str] | None = None,
    published_at: str | None = None,
    executor=None,
    source_type: str | None = None,
) -> dict:
    """Extract landscape signals (capabilities, limitations, bottlenecks) from source text.

    Args:
        clean_text: Cleaned source text.
        source_id: Source ID for logging.
        source_themes: Already-classified theme IDs (for context).
        published_at: Publication date of the source (ISO-8601 string or None).
        executor: ClaudeExecutor instance.
        source_type: Source type for budget selection (paper, article, video, podcast).

    Returns:
        Dict with keys: capabilities, limitations, bottlenecks (each a list of dicts).
    """
    if executor is None:
        from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
        executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    budget = budget_for_source_type(source_type)
    # For very long text, use chunked parallel extraction
    if len(clean_text) > 2 * budget:
        from ingest.chunked_extractor import chunked_landscape_signals
        logger.info("Text exceeds 2x budget (%d > %d), using chunked landscape extraction", len(clean_text), 2 * budget)
        return chunked_landscape_signals(
            clean_text, source_id,
            source_themes=source_themes,
            published_at=published_at,
            executor=executor,
            budget=budget,
        )

    # Use section-prioritized slicing instead of naive truncation.
    sliced_text = prioritized_slice(clean_text, budget=budget, priorities=LANDSCAPE_PRIORITIES)
    dynamic_timeout = timeout_for_text(len(sliced_text))

    # Build temporal context for the prompt
    if published_at:
        temporal_context = (
            f"**Source publication date: {published_at}**\n"
            "When extracting signals, consider temporal context:\n"
            "- Are capabilities described as current achievements or future possibilities at time of publication?\n"
            "- Are limitations still likely to hold, or might they reflect the state at publication?\n"
            "- For bottlenecks, note whether the source describes the current situation or a past state.\n"
            "- For first_demonstrated_at / production_ready_at, use dates mentioned in the source text."
        )
    else:
        temporal_context = (
            "**Source publication date: unknown.**\n"
            "Extract signals as described. If the text mentions specific dates for capabilities "
            "or breakthroughs, capture them in first_demonstrated_at."
        )

    # Build dynamic theme block from DB (falls back to static list)
    from ingest.theme_classifier import get_available_themes
    try:
        from reading_app.db import get_conn as _get_conn_for_themes
        theme_block = get_available_themes(_get_conn_for_themes)
    except Exception:
        theme_block = get_available_themes(None)

    def _build_prompt(text_slice: str) -> str:
        p = LANDSCAPE_EXTRACTION_PROMPT.format(
            text=text_slice, temporal_context=temporal_context, theme_block=theme_block,
        )
        if source_themes:
            landscape_context = _build_landscape_context(source_themes)
            if landscape_context:
                p += landscape_context
            p += f"\n\nNote: This source has been classified under themes: {', '.join(source_themes)}"
        return p

    prompt = _build_prompt(sliced_text)

    # Use sonnet for papers/articles (higher precision needed),
    # haiku for video/podcast transcripts (faster, lower-quality text)
    landscape_model = "haiku" if source_type in ("video", "podcast") else "sonnet"

    result = executor.run_raw(
        prompt,
        session_id=f"landscape_{source_id}",
        model=landscape_model,
        timeout=dynamic_timeout,
    )

    # Timeout fallback: retry with halved budget to prevent silent data loss
    if result.is_timeout:
        reduced_budget = budget // 2
        logger.warning(
            "Landscape extraction timed out for %s, retrying with reduced budget (%d -> %d)",
            source_id, budget, reduced_budget,
        )
        sliced_text = prioritized_slice(clean_text, budget=reduced_budget, priorities=LANDSCAPE_PRIORITIES)
        prompt = _build_prompt(sliced_text)
        result = executor.run_raw(
            prompt,
            session_id=f"landscape_{source_id}_retry",
            model=landscape_model,
            timeout=dynamic_timeout + 60,  # Extra buffer for retry
        )

    if not result.success:
        detail = result.stderr[:300] if result.stderr.strip() else f"stdout={result.stdout[:300]}"
        raise RuntimeError(
            f"Landscape CLI failed for {source_id}: rc={result.return_code}, "
            f"{detail}"
        )

    signals = _parse_signals(result.text)

    # Validate and filter
    signals["capabilities"] = [
        _validate_capability(c) for c in signals.get("capabilities", [])
        if _validate_capability(c) is not None
    ]
    signals["limitations"] = [
        _validate_limitation(l) for l in signals.get("limitations", [])
        if _validate_limitation(l) is not None
    ]
    signals["bottlenecks"] = [
        _validate_bottleneck(b) for b in signals.get("bottlenecks", [])
        if _validate_bottleneck(b) is not None
    ]
    signals["breakthroughs"] = [
        _validate_breakthrough(bt) for bt in signals.get("breakthroughs", [])
        if _validate_breakthrough(bt) is not None
    ]

    logger.info(
        "Extracted landscape signals for %s: %d capabilities, %d limitations, %d bottlenecks, %d breakthroughs",
        source_id,
        len(signals["capabilities"]),
        len(signals["limitations"]),
        len(signals["bottlenecks"]),
        len(signals["breakthroughs"]),
    )

    return signals


def _get_source_published_at(source_id: str) -> str | None:
    """Look up published_at for a source. Returns ISO string or None."""
    try:
        from reading_app.db import get_conn
        with get_conn() as conn:
            row = conn.execute(
                "SELECT published_at FROM sources WHERE id = %s", (source_id,)
            ).fetchone()
            if row and row.get("published_at"):
                return str(row["published_at"])
    except Exception:
        pass
    return None


def _is_newer_source(new_source_id: str, existing_evidence_sources: list[dict] | str | None) -> bool | None:
    """Determine if the new source is newer than the most recent source in existing evidence.

    Returns True if new is newer, False if older, None if comparison is impossible
    (either date is NULL).
    """
    new_pub = _get_source_published_at(new_source_id)
    if not new_pub:
        return None

    if not existing_evidence_sources:
        return True

    # Handle JSON string if not already parsed
    if isinstance(existing_evidence_sources, str):
        try:
            existing_evidence_sources = json.loads(existing_evidence_sources)
        except (json.JSONDecodeError, TypeError):
            return None

    if not isinstance(existing_evidence_sources, list):
        return None

    # Find the most recent publication date among existing sources
    latest_existing = None
    for ev in existing_evidence_sources:
        if not isinstance(ev, dict):
            continue
        sid = ev.get("source_id")
        if sid:
            pub = _get_source_published_at(sid)
            if pub and (latest_existing is None or pub > latest_existing):
                latest_existing = pub

    if not latest_existing:
        return None

    return new_pub > latest_existing


def _maybe_rederive_trajectory(
    existing: dict,
    new_lim: dict,
    merged_row: dict,
    source_id: str,
    insert_landscape_history_fn,
) -> None:
    """Re-derive a limitation's trajectory when it has accumulated 3+ evidence sources.

    Examines the temporal pattern of severity and trajectory signals across
    evidence sources to determine if the trajectory should be updated.
    The new source's trajectory signal is compared against the existing one,
    and if enough evidence points in a different direction, the trajectory is updated.
    """
    # Count evidence sources
    evidence = merged_row.get("evidence_sources")
    if isinstance(evidence, str):
        try:
            evidence = json.loads(evidence)
        except (json.JSONDecodeError, TypeError):
            return
    if not isinstance(evidence, list) or len(evidence) < 3:
        return

    old_trajectory = existing.get("trajectory")
    new_trajectory = new_lim.get("trajectory")

    # Only re-derive if the new source disagrees with current trajectory
    if not new_trajectory or new_trajectory == old_trajectory:
        return

    # Check if the new source is actually newer (don't let old sources rewrite)
    source_is_newer = _is_newer_source(source_id, existing.get("evidence_sources"))
    if source_is_newer is False:
        return

    # With 3+ sources, if the newest source disagrees, update trajectory
    # This is conservative: we still require the new source to be more recent
    try:
        from reading_app.db import get_conn
        with get_conn() as conn:
            conn.execute(
                "UPDATE limitations SET trajectory = %s, last_updated = NOW() WHERE id = %s",
                (new_trajectory, existing["id"]),
            )
            conn.commit()

        insert_landscape_history_fn(
            entity_type="limitation",
            entity_id=existing["id"],
            field="trajectory",
            old_value=old_trajectory,
            new_value=new_trajectory,
            source_id=source_id,
            attribution="automated_rederivation",
        )
        logger.info(
            "Re-derived trajectory for limitation %s: %s -> %s (based on %d evidence sources)",
            existing["id"], old_trajectory, new_trajectory, len(evidence),
        )
    except Exception:
        logger.warning("Failed to re-derive trajectory for %s", existing["id"], exc_info=True)


def persist_landscape_signals(
    signals: dict,
    source_id: str,
    get_conn_fn=None,
) -> LandscapeDelta:
    """Persist extracted landscape signals to database with deduplication.

    Before inserting a new entity, checks for existing entries in the same theme
    with high text similarity (pg_trgm similarity >= 0.7). If a match is found,
    merges evidence_sources and updates confidence (weighted average) instead of
    creating a duplicate. Breakthroughs are always inserted as new (unique events).

    Deduplication is temporally aware: when merging, if the new source is older
    than existing evidence, maturity/trajectory/severity are NOT overwritten.
    Only newer sources can update those fields.

    Args:
        signals: Dict with capabilities, limitations, bottlenecks lists.
        source_id: Source ID for evidence linking.
        get_conn_fn: Callable returning a DB connection context manager.

    Returns:
        LandscapeDelta with rich details of what changed. Use .counts for
        backward-compatible summary dict.
    """
    delta = LandscapeDelta()

    if not get_conn_fn:
        return delta

    try:
        from ulid import ULID
        from reading_app.db import (
            insert_capability, insert_limitation, insert_bottleneck,
            insert_breakthrough,
            find_similar_capability, find_similar_limitation, find_similar_bottleneck,
            find_similar_breakthrough, merge_breakthrough,
            merge_capability, merge_limitation, merge_bottleneck,
            insert_landscape_history, invalidate_theme_summaries,
        )

        # Maturity progression order for detecting forward changes
        _MATURITY_ORDER = {
            "research_only": 0, "demo": 1, "narrow_production": 2,
            "broad_production": 3, "commoditized": 4,
        }

        # ── Validate theme_ids: drop entities referencing non-existent themes ──
        valid_themes = load_valid_theme_ids(get_conn_fn)

        for cap in signals.get("capabilities", []):
            resolved_tid = resolve_theme_id(cap.get("theme_id", ""), valid_themes)
            if resolved_tid is None:
                continue
            cap["theme_id"] = resolved_tid
            try:
                evidence = [{"source_id": source_id, "snippet": cap.get("evidence_snippet", "")}]
                confidence = cap.get("confidence", 0.5)
                existing = find_similar_capability(cap["theme_id"], cap["description"])
                if existing:
                    merge_capability(existing["id"], evidence, confidence, source_id=source_id)
                    delta.merged_capabilities.append({
                        "id": existing["id"],
                        "description": cap["description"],
                        "sim": existing.get("sim", 0),
                    })
                    # Detect maturity advancement — only if new source is not older
                    new_maturity = cap.get("maturity")
                    old_maturity = existing.get("maturity")
                    source_is_newer = _is_newer_source(
                        source_id, existing.get("evidence_sources")
                    )
                    if (new_maturity and old_maturity
                            and new_maturity != old_maturity
                            and _MATURITY_ORDER.get(new_maturity, -1)
                                > _MATURITY_ORDER.get(old_maturity, -1)
                            and source_is_newer is not False):
                        try:
                            insert_landscape_history(
                                entity_type="capability",
                                entity_id=existing["id"],
                                field="maturity",
                                old_value=old_maturity,
                                new_value=new_maturity,
                                source_id=source_id,
                                attribution="automated_extraction",
                            )
                            # Update the capability's maturity in DB
                            from reading_app.db import get_conn
                            with get_conn() as conn:
                                conn.execute(
                                    "UPDATE capabilities SET maturity = %s, last_updated = NOW() WHERE id = %s",
                                    (new_maturity, existing["id"]),
                                )
                                conn.commit()
                            delta.maturity_changes.append({
                                "id": existing["id"],
                                "description": cap["description"],
                                "old_maturity": old_maturity,
                                "new_maturity": new_maturity,
                            })
                            logger.info(
                                "Maturity change for %s: %s -> %s",
                                existing["id"], old_maturity, new_maturity,
                            )
                        except Exception:
                            logger.warning("Failed to record maturity change for %s", existing["id"], exc_info=True)
                    elif (new_maturity and old_maturity
                            and new_maturity != old_maturity
                            and source_is_newer is False):
                        logger.info(
                            "Skipping maturity change for %s: source is older than existing evidence "
                            "(new=%s, existing=%s)", existing["id"], new_maturity, old_maturity,
                        )
                    logger.debug("Merged capability into %s (sim=%.2f)", existing["id"], existing.get("sim", 0))
                else:
                    cap_id = f"cap_{ULID()}"
                    insert_capability(
                        id=cap_id,
                        theme_id=cap["theme_id"],
                        description=cap["description"],
                        maturity=cap.get("maturity"),
                        confidence=confidence,
                        evidence_sources=evidence,
                        attribution="automated_extraction",
                        first_demonstrated_at=cap.get("first_demonstrated_at"),
                        production_ready_at=cap.get("production_ready_at"),
                    )
                    delta.new_capabilities.append({
                        "id": cap_id,
                        "description": cap["description"],
                        "maturity": cap.get("maturity"),
                        "theme_id": cap["theme_id"],
                    })
            except Exception:
                logger.warning("Failed to persist capability: %s", cap.get("description", "?")[:60], exc_info=True)

        # Persist bottlenecks first so limitations can reference them
        bottleneck_map = {}  # description -> id for limitation linking
        for bn in signals.get("bottlenecks", []):
            resolved_tid = resolve_theme_id(bn.get("theme_id", ""), valid_themes)
            if resolved_tid is None:
                continue
            bn["theme_id"] = resolved_tid
            try:
                evidence = [{"source_id": source_id, "snippet": bn.get("evidence_snippet", "")}]
                confidence = bn.get("confidence", 0.5)
                existing = find_similar_bottleneck(bn["theme_id"], bn["description"])
                if existing:
                    merge_bottleneck(existing["id"], evidence, confidence, source_id=source_id)
                    bottleneck_map[bn["description"].lower().strip()] = existing["id"]
                    delta.merged_bottlenecks.append({
                        "id": existing["id"],
                        "description": bn["description"],
                        "sim": existing.get("sim", 0),
                    })
                    logger.debug("Merged bottleneck into %s (sim=%.2f)", existing["id"], existing.get("sim", 0))
                else:
                    bn_id = f"bn_{ULID()}"
                    insert_bottleneck(
                        id=bn_id,
                        theme_id=bn["theme_id"],
                        description=bn["description"],
                        blocking_what=bn.get("blocking_what"),
                        bottleneck_type=bn.get("bottleneck_type"),
                        resolution_horizon=bn.get("resolution_horizon"),
                        evidence_sources=evidence,
                        confidence=confidence,
                        attribution="automated_extraction",
                    )
                    bottleneck_map[bn["description"].lower().strip()] = bn_id
                    delta.new_bottlenecks.append({
                        "id": bn_id,
                        "description": bn["description"],
                        "theme_id": bn["theme_id"],
                        "resolution_horizon": bn.get("resolution_horizon"),
                    })
            except Exception:
                logger.warning("Failed to persist bottleneck: %s", bn.get("description", "?")[:60], exc_info=True)

        for lim in signals.get("limitations", []):
            resolved_tid = resolve_theme_id(lim.get("theme_id", ""), valid_themes)
            if resolved_tid is None:
                continue
            lim["theme_id"] = resolved_tid
            try:
                evidence = [{"source_id": source_id, "snippet": lim.get("evidence_snippet", "")}]
                confidence = lim.get("confidence", 0.5)
                existing = find_similar_limitation(lim["theme_id"], lim["description"])
                if existing:
                    merged_row = merge_limitation(existing["id"], evidence, confidence, source_id=source_id)
                    delta.merged_limitations.append({
                        "id": existing["id"],
                        "description": lim["description"],
                        "sim": existing.get("sim", 0),
                    })
                    # Re-derive trajectory when 3+ evidence sources accumulated
                    if merged_row:
                        _maybe_rederive_trajectory(
                            existing, lim, merged_row, source_id,
                            insert_landscape_history,
                        )
                    logger.debug("Merged limitation into %s (sim=%.2f)", existing["id"], existing.get("sim", 0))
                else:
                    lim_id = f"lim_{ULID()}"
                    insert_limitation(
                        id=lim_id,
                        theme_id=lim["theme_id"],
                        description=lim["description"],
                        limitation_type=lim.get("limitation_type"),
                        signal_type=lim.get("signal_type", "explicit"),
                        severity=lim.get("severity"),
                        trajectory=lim.get("trajectory"),
                        confidence=confidence,
                        evidence_sources=evidence,
                        underlying_reason=lim.get("underlying_reason"),
                        attribution="automated_extraction",
                    )
                    delta.new_limitations.append({
                        "id": lim_id,
                        "description": lim["description"],
                        "signal_type": lim.get("signal_type", "explicit"),
                        "theme_id": lim["theme_id"],
                    })
            except Exception:
                logger.warning("Failed to persist limitation: %s", lim.get("description", "?")[:60], exc_info=True)

        # Persist breakthroughs with deduplication — corroborating sources merge
        # into existing breakthroughs instead of creating duplicates
        themes_to_invalidate = set()
        for bt in signals.get("breakthroughs", []):
            resolved_tid = resolve_theme_id(bt.get("theme_id", ""), valid_themes)
            if resolved_tid is None:
                continue
            bt["theme_id"] = resolved_tid
            try:
                # Check for existing similar breakthrough in same theme
                existing_bt = find_similar_breakthrough(bt["theme_id"], bt["description"])
                if existing_bt:
                    merge_breakthrough(existing_bt["id"], source_id, bt.get("confidence", 0.5))
                    bt_id = existing_bt["id"]
                    delta.breakthroughs.append({
                        "id": bt_id,
                        "description": bt["description"],
                        "significance": bt.get("significance"),
                        "theme_id": bt["theme_id"],
                        "merged_into_existing": True,
                    })
                    logger.info(
                        "Merged breakthrough into %s (sim=%.2f): %s",
                        existing_bt["id"], existing_bt.get("sim", 0),
                        bt["description"][:60],
                    )
                else:
                    bt_id = f"bt_{ULID()}"
                    insert_breakthrough(
                        id=bt_id,
                        theme_id=bt["theme_id"],
                        description=bt["description"],
                        significance=bt.get("significance"),
                        what_was_believed_before=bt.get("what_was_believed_before"),
                        what_is_now_possible=bt.get("what_is_now_possible"),
                        immediate_implications=bt.get("immediate_implications"),
                        downstream_implications=bt.get("downstream_implications"),
                        bottlenecks_affected=bt.get("bottlenecks_affected"),
                        primary_source_id=source_id,
                        confidence=bt.get("confidence", 0.5),
                        attribution="automated_extraction",
                    )
                    delta.breakthroughs.append({
                        "id": bt_id,
                        "description": bt["description"],
                        "significance": bt.get("significance"),
                        "theme_id": bt["theme_id"],
                    })
                # Event-driven staleness: flag theme for summary regeneration
                themes_to_invalidate.add(bt["theme_id"])
                # Trigger bottleneck propagation if breakthrough affects bottlenecks
                # (only for new breakthroughs, not corroborating merges)
                if bt.get("bottlenecks_affected") and not existing_bt:
                    try:
                        from ingest.bottleneck_propagator import (
                            propagate_breakthrough_to_bottlenecks,
                            persist_bottleneck_updates,
                        )
                        bt_with_id = {**bt, "id": bt_id, "primary_source_id": source_id}
                        bn_updates = propagate_breakthrough_to_bottlenecks(bt_with_id, source_id)
                        if bn_updates:
                            persist_bottleneck_updates(
                                bn_updates, source_id,
                                breakthrough_description=bt.get("description", ""),
                            )
                            delta.bottleneck_propagations.extend(bn_updates)
                            # Also invalidate themes for any bottlenecks whose horizons shifted
                            for upd in bn_updates:
                                if hasattr(upd, 'new_horizon') and upd.new_horizon:
                                    try:
                                        from reading_app.db import get_bottleneck
                                        bn = get_bottleneck(upd.bottleneck_id)
                                        if bn:
                                            themes_to_invalidate.add(bn["theme_id"])
                                    except Exception:
                                        pass
                            logger.info("Propagated breakthrough %s to %d bottlenecks", bt_id, len(bn_updates))
                    except Exception:
                        logger.warning("Bottleneck propagation failed for %s", bt_id, exc_info=True)
            except Exception:
                logger.warning("Failed to persist breakthrough: %s", bt.get("description", "?")[:60], exc_info=True)

        # Event-driven summary staleness: immediately flag affected themes
        if themes_to_invalidate:
            try:
                count = invalidate_theme_summaries(list(themes_to_invalidate))
                if count:
                    logger.info("Invalidated state summaries for %d themes due to breakthroughs/bottleneck shifts", count)
            except Exception:
                logger.warning("Failed to invalidate theme summaries", exc_info=True)

    except Exception:
        logger.error("Failed to persist landscape signals for %s", source_id, exc_info=True)

    logger.info("Persisted landscape signals for %s: %s", source_id, delta.counts)

    # Update theme velocities after landscape changes
    try:
        from retrieval.landscape import update_all_theme_velocities
        update_all_theme_velocities()
    except Exception:
        logger.warning("Failed to update theme velocities after persist", exc_info=True)

    return delta


def save_landscape_json(
    signals: dict,
    library_path: Path | str,
) -> Path | None:
    """Save landscape signals to library/{source_id}/landscape.json."""
    try:
        path = Path(library_path) / "landscape.json"
        path.write_text(json.dumps(signals, indent=2, default=str), encoding="utf-8")
        return path
    except Exception:
        logger.warning("Failed to save landscape.json to %s", library_path, exc_info=True)
        return None


def _parse_signals(text: str) -> dict:
    """Parse JSON object with capabilities, limitations, bottlenecks from LLM output."""
    result = parse_json_from_llm(text, expect=dict)
    if result is None:
        logger.warning(
            "Failed to parse landscape extraction output (len=%d, preview=%.300s)",
            len(text), text[:300],
        )
        return {"capabilities": [], "limitations": [], "bottlenecks": [], "breakthroughs": []}
    return result


def _validate_capability(cap: dict) -> dict | None:
    """Validate and normalize a capability dict. Returns None if invalid."""
    if not isinstance(cap, dict):
        return None
    if not cap.get("description") or not cap.get("theme_id"):
        return None
    # Normalize maturity
    if cap.get("maturity") and cap["maturity"] not in VALID_MATURITY:
        cap["maturity"] = None
    # Clamp confidence
    if "confidence" in cap:
        cap["confidence"] = max(0.0, min(1.0, float(cap["confidence"])))
    return cap


def _validate_limitation(lim: dict) -> dict | None:
    """Validate and normalize a limitation dict. Returns None if invalid."""
    if not isinstance(lim, dict):
        return None
    if not lim.get("description") or not lim.get("theme_id"):
        return None
    # Normalize enum fields
    if lim.get("limitation_type") and lim["limitation_type"] not in VALID_LIMITATION_TYPE:
        lim["limitation_type"] = "unknown"
    if lim.get("signal_type") and lim["signal_type"] not in VALID_SIGNAL_TYPE:
        lim["signal_type"] = "explicit"
    if lim.get("severity") and lim["severity"] not in VALID_SEVERITY:
        lim["severity"] = None
    if lim.get("trajectory") and lim["trajectory"] not in VALID_TRAJECTORY:
        lim["trajectory"] = "unclear"
    if "confidence" in lim:
        lim["confidence"] = max(0.0, min(1.0, float(lim["confidence"])))
    return lim


def _validate_bottleneck(bn: dict) -> dict | None:
    """Validate and normalize a bottleneck dict. Returns None if invalid."""
    if not isinstance(bn, dict):
        return None
    if not bn.get("description") or not bn.get("theme_id"):
        return None
    if bn.get("bottleneck_type") and bn["bottleneck_type"] not in VALID_BOTTLENECK_TYPE:
        bn["bottleneck_type"] = None
    if bn.get("resolution_horizon") and bn["resolution_horizon"] not in VALID_RESOLUTION_HORIZON:
        bn["resolution_horizon"] = "unknown"
    if "confidence" in bn:
        bn["confidence"] = max(0.0, min(1.0, float(bn["confidence"])))
    return bn


def _validate_breakthrough(bt: dict) -> dict | None:
    """Validate and normalize a breakthrough dict. Returns None if invalid."""
    if not isinstance(bt, dict):
        return None
    if not bt.get("description") or not bt.get("theme_id"):
        return None
    if bt.get("significance") and bt["significance"] not in VALID_SIGNIFICANCE:
        bt["significance"] = None
    if "confidence" in bt:
        bt["confidence"] = max(0.0, min(1.0, float(bt["confidence"])))
    if not isinstance(bt.get("bottlenecks_affected"), list):
        bt["bottlenecks_affected"] = []
    if not isinstance(bt.get("immediate_implications"), list):
        bt["immediate_implications"] = []
    if not isinstance(bt.get("downstream_implications"), list):
        bt["downstream_implications"] = []
    return bt
