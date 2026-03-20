"""Direct Python handler for /anticipate jobs.

Bypasses the Claude CLI subprocess. Handles review (direct evidence surfacing)
and calibration (Brier score tracking) natively. Delegates generate mode
to executor.run_raw().
"""

from __future__ import annotations

import json
import math
import re
import time

from ingest.json_parser import parse_json_from_llm
from typing import Callable

import structlog
from ulid import ULID

from gateway.models import Event, Job
from reading_app.text_utils import truncate, truncate_sentences

logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def handle_anticipate_job(
    event: Event,
    job: Job,
    config,
    executor,
    *,
    on_progress: Callable[[str], None] | None = None,
) -> str:
    """Run /anticipate directly."""
    text = event.payload.get("text", "")
    log = logger.bind(job_id=job.id)
    log.info("anticipate_handler_start")
    t0 = time.monotonic()

    from reading_app.db import ensure_pool
    ensure_pool()

    subcmd, args = _parse_command(text)
    log = log.bind(subcmd=subcmd)

    if subcmd == "review":
        result = _handle_review(args, on_progress, log)
    elif subcmd == "calibration":
        result = _handle_calibration(on_progress, log)
    elif subcmd == "confirm":
        result = _handle_status_update(args, "confirmed", log)
    elif subcmd == "invalidate":
        result = _handle_status_update(args, "invalidated", log)
    elif subcmd == "generate":
        result = _handle_generate(args, executor, on_progress, log)
    elif subcmd == "evolve":
        result = _handle_evolve(args, executor, on_progress, log)
    else:
        # Default: show overview
        result = _handle_overview(on_progress, log)

    elapsed = time.monotonic() - t0
    log.info("anticipate_handler_complete", elapsed_s=round(elapsed, 1))
    return result


# ---------------------------------------------------------------------------
# Command parser
# ---------------------------------------------------------------------------

def _parse_command(text: str) -> tuple[str, str]:
    """Parse '/anticipate [subcmd] [args]'."""
    cleaned = text.strip()
    for prefix in ("/anticipate ", "/anticipate"):
        if cleaned.lower().startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
            break

    if not cleaned:
        return "overview", ""

    parts = cleaned.split(None, 1)
    subcmd = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    known = {"review", "generate", "calibration", "confirm", "invalidate", "evolve"}
    if subcmd in known:
        return subcmd, args

    return "overview", cleaned


# ---------------------------------------------------------------------------
# /anticipate (overview)
# ---------------------------------------------------------------------------

def _handle_overview(on_progress, log) -> str:
    """Show anticipations needing attention."""
    from retrieval.landscape import (
        get_anticipations_with_evidence,
        get_untested_anticipations,
    )

    if on_progress:
        on_progress("Loading anticipations...")

    with_evidence = get_anticipations_with_evidence()
    untested = get_untested_anticipations(min_age_days=30)

    lines = ["**Anticipation Overview**\n"]

    # Anticipations with accumulated evidence (need review)
    if with_evidence:
        lines.append(f"**Needs review** ({len(with_evidence)} with evidence):")
        for a in with_evidence[:10]:
            ev_count = a.get("evidence_count", 0)
            evidence = a.get("status_evidence") or []
            if isinstance(evidence, str):
                evidence = json.loads(evidence)
            confirming = sum(1 for e in evidence if e.get("match_type") == "confirming")
            disconfirming = sum(1 for e in evidence if e.get("match_type") == "disconfirming")

            lines.append(
                f"- `{a['id']}` [{a.get('theme_name', '?')}] "
                f"{a['prediction'][:100]}\n"
                f"  Evidence: {ev_count} total ({confirming} confirming, {disconfirming} disconfirming)"
            )
        lines.append("")

    # Untested anticipations
    if untested:
        lines.append(f"**Untested** ({len(untested)} with no evidence after 30+ days):")
        for a in untested[:5]:
            lines.append(
                f"- `{a['id']}` [{a.get('theme_name', '?')}] "
                f"{a.get('prediction', '?')[:100]} — {a.get('age_days', '?')} days old"
            )
        lines.append("")

    if not with_evidence and not untested:
        lines.append("All anticipations are up to date.")

    lines.append(
        "---\n"
        "Commands:\n"
        "- `/anticipate review [theme]` — review evidence for anticipations\n"
        "- `/anticipate confirm <id>` — mark as confirmed\n"
        "- `/anticipate invalidate <id>` — mark as invalidated\n"
        "- `/anticipate generate <theme>` — generate new predictions\n"
        "- `/anticipate evolve <theme>` — retire stale predictions and regenerate\n"
        "- `/anticipate calibration` — view prediction accuracy"
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# /anticipate review
# ---------------------------------------------------------------------------

def _handle_review(theme_filter: str, on_progress, log) -> str:
    """Review anticipations with accumulated evidence."""
    from retrieval.landscape import get_anticipations_with_evidence
    from reading_app.db import get_conn

    if on_progress:
        on_progress("Loading anticipations with evidence...")

    all_with_evidence = get_anticipations_with_evidence()

    # Filter by theme if specified
    if theme_filter:
        filtered = [
            a for a in all_with_evidence
            if theme_filter.lower() in (a.get("theme_name") or "").lower()
            or theme_filter == a.get("theme_id")
        ]
    else:
        filtered = all_with_evidence

    if not filtered:
        return (
            "**No anticipations need review.**\n\n"
            "All open anticipations either have no evidence yet or have been recently reviewed.\n"
            "Use `/anticipate generate <theme>` to create new predictions."
        )

    lines = [f"**Anticipation Review** ({len(filtered)} to review)\n"]

    for a in filtered[:15]:
        ant_id = a["id"]
        prediction = a.get("prediction", "?")
        confidence = a.get("confidence", "?")
        theme_name = a.get("theme_name", "?")

        # Parse evidence
        evidence = a.get("status_evidence") or []
        if isinstance(evidence, str):
            evidence = json.loads(evidence)

        confirming = [e for e in evidence if e.get("match_type") == "confirming"]
        disconfirming = [e for e in evidence if e.get("match_type") == "disconfirming"]
        partial = [e for e in evidence if e.get("match_type") == "partial"]

        lines.append(f"### `{ant_id}` [{theme_name}]")
        lines.append(f"**Prediction:** {prediction}")
        lines.append(f"**Confidence:** {confidence}")
        lines.append(
            f"**Evidence:** {len(confirming)} confirming, "
            f"{len(disconfirming)} disconfirming, {len(partial)} partial\n"
        )

        # Show evidence details
        if confirming:
            lines.append("**Confirming:**")
            for e in confirming[:3]:
                lines.append(
                    f"  - [{e.get('source_id', '?')}] {e.get('evidence_text', '')[:120]}"
                )
        if disconfirming:
            lines.append("**Disconfirming:**")
            for e in disconfirming[:3]:
                lines.append(
                    f"  - [{e.get('source_id', '?')}] {e.get('evidence_text', '')[:120]}"
                )
        if partial:
            lines.append("**Partial:**")
            for e in partial[:2]:
                lines.append(
                    f"  - [{e.get('source_id', '?')}] {e.get('evidence_text', '')[:120]}"
                )

        # Suggest verdict
        verdict = _suggest_verdict(confirming, disconfirming, partial)
        lines.append(f"\n**Suggested action:** {verdict}")
        lines.append("")

    # Update last_reviewed for all reviewed anticipations
    try:
        with get_conn() as conn:
            ids = [a["id"] for a in filtered[:15]]
            conn.execute(
                "UPDATE anticipations SET last_reviewed = NOW() WHERE id = ANY(%s)",
                (ids,),
            )
            conn.commit()
        log.info("anticipations_reviewed", count=len(ids))
    except Exception as e:
        log.warning("anticipation_review_update_failed", error=str(e)[:200])

    lines.append(
        "---\n"
        "To resolve: `/anticipate confirm <id>` or `/anticipate invalidate <id>`"
    )

    return "\n".join(lines)


def _suggest_verdict(confirming, disconfirming, partial) -> str:
    """Suggest a verdict based on evidence balance."""
    n_conf = len(confirming)
    n_dis = len(disconfirming)

    if n_conf >= 5 and n_dis == 0:
        return "Strong confirming evidence — consider `/anticipate confirm <id>`"
    if n_conf >= 3 and n_dis == 0:
        return "Moderate confirming evidence — partially confirmed, keep open for more data"
    if n_dis >= 2 and n_conf == 0:
        return "Disconfirming evidence — consider `/anticipate invalidate <id>`"
    if n_dis >= 2 and n_conf >= 2:
        return "Mixed evidence — keep open, needs more data to resolve"
    if n_conf > n_dis:
        return "Leaning confirmed — keep monitoring"
    if n_dis > n_conf:
        return "Leaning invalidated — keep monitoring"
    return "Inconclusive — keep open"


# ---------------------------------------------------------------------------
# /anticipate confirm|invalidate
# ---------------------------------------------------------------------------

def _handle_status_update(args: str, new_status: str, log) -> str:
    """Update an anticipation's status to confirmed or invalidated."""
    from reading_app.db import get_conn, get_anticipation, insert_landscape_history

    ant_id = args.strip().split()[0] if args.strip() else ""
    if not ant_id:
        return f"Usage: `/anticipate {new_status} <anticipation_id>`"

    ant = get_anticipation(ant_id)
    if not ant:
        return f"Anticipation not found: `{ant_id}`"

    old_status = ant.get("status", "open")
    if old_status == new_status:
        return f"Anticipation `{ant_id}` is already `{new_status}`."

    with get_conn() as conn:
        conn.execute(
            "UPDATE anticipations SET status = %s, last_reviewed = NOW() WHERE id = %s",
            (new_status, ant_id),
        )
        conn.commit()

    insert_landscape_history(
        entity_type="anticipation",
        entity_id=ant_id,
        field="status",
        old_value=old_status,
        new_value=new_status,
        attribution="user_review",
    )

    log.info("anticipation_resolved", id=ant_id, old=old_status, new=new_status)

    prediction = ant.get("prediction", "?")[:120]
    confidence = ant.get("confidence", "?")
    return (
        f"**Anticipation {new_status}:** `{ant_id}`\n\n"
        f"> {prediction}\n\n"
        f"Confidence was: {confidence} | Status: {old_status} → {new_status}"
    )


# ---------------------------------------------------------------------------
# /anticipate generate
# ---------------------------------------------------------------------------

_GENERATE_PROMPT = """\
You are generating predictions about where AI is heading, grounded in a knowledge engine's landscape model.

## Theme Context
{theme_context}

## Current Bottlenecks
{bottlenecks_text}

## Recent Breakthroughs
{breakthroughs_text}

## Cross-Theme Implications
{implications_text}

## Specific Evidence from Sources
{claims_text}

## Existing Anticipations (avoid duplicates)
{existing_text}

## Instructions

Generate 3-7 concrete, testable predictions about this theme based on:
1. **Bottleneck trajectories**: Which are shifting? What happens when they resolve?
2. **Breakthrough implications**: What second-order effects are emerging?
3. **Capability convergence**: What becomes possible when capabilities combine?
4. **Evidence gaps**: What should be true if the claims above are correct but isn't yet demonstrated?

## Quality Constraints

- **Confidence diversity**: At least one prediction with confidence >= 0.8 (you're quite sure) and at least one <= 0.4 (contrarian or uncertain). Avoid clustering all predictions in the 0.5-0.7 range.
- **Timeline diversity**: At least one prediction at a different horizon than the majority.
- **Non-obvious**: Each prediction should pass the test "would a knowledgeable AI researcher disagree or be surprised?" Generic trend extrapolations (e.g. "models will get bigger") fail this test.
- **Falsifiable**: Predictions must describe concrete, observable outcomes — not trend directions. Bad: "reasoning capabilities will improve." Good: "At least one LLM will pass the IMO gold medal threshold by 2027."
- **Specific would_confirm/would_invalidate**: Describe observable evidence patterns, not vague sentiment. Bad: "more papers on this topic." Good: "A benchmark showing >90% accuracy on multi-hop reasoning tasks with <1B parameter models."

For each prediction, provide:
- A concrete, falsifiable prediction
- Confidence (0.0-1.0)
- Timeline (months, 1-2_years, 3-5_years, 5+_years)
- What evidence would confirm it (specific observable patterns)
- What evidence would invalidate it (specific observable patterns)
- Reasoning grounded in specific bottlenecks/breakthroughs/claims

Output a JSON block:
```json
{{
  "anticipations": [
    {{
      "prediction": "...",
      "confidence": 0.0-1.0,
      "timeline": "months|1-2_years|3-5_years|5+_years",
      "would_confirm": "...",
      "would_invalidate": "...",
      "reasoning": "...",
      "based_on": ["entity_id from the context above"]
    }}
  ]
}}
```
"""


def _budget_generate_sections(
    sections: list[tuple[int, str, str]], total_limit: int,
) -> dict[str, str]:
    """Allocate a character budget across named sections by priority.

    Surplus from small sections flows to larger ones.
    """
    if not sections:
        return {}
    sections = [(p, k, t) for p, k, t in sections if t and t.strip()]
    sections = sorted(sections, key=lambda s: s[0], reverse=True)
    total_needed = sum(len(t) for _, _, t in sections)
    if total_needed <= total_limit:
        return {k: t for _, k, t in sections}

    total_priority = sum(p for p, _, _ in sections) or len(sections)
    allocations = {k: int((p / total_priority) * total_limit) for p, k, _ in sections}

    surplus = 0
    needs_more = []
    for _, k, t in sections:
        if len(t) <= allocations[k]:
            surplus += allocations[k] - len(t)
            allocations[k] = len(t)
        else:
            needs_more.append(k)

    for k in needs_more:
        if surplus <= 0:
            break
        text_len = next(len(t) for _, kk, t in sections if kk == k)
        deficit = text_len - allocations[k]
        give = min(surplus, deficit)
        allocations[k] += give
        surplus -= give

    result = {}
    for _, k, t in sections:
        if len(t) > allocations[k]:
            result[k] = truncate_sentences(t, allocations[k])
        else:
            result[k] = t
    return result


def _handle_generate(theme_filter: str, executor, on_progress, log) -> str:
    """Generate new anticipations for a theme."""
    from reading_app.db import get_conn, insert_anticipation
    from retrieval.landscape import (
        get_theme_state, get_recent_breakthroughs,
        get_bottleneck_ranking, get_consolidated_implications,
    )

    if executor is None:
        return "Error: This skill requires an LLM executor. Check your configuration."

    if not theme_filter:
        return "Usage: `/anticipate generate <theme>`"

    if on_progress:
        on_progress(f"Loading landscape for **{theme_filter}**...")

    # Resolve theme
    with get_conn() as conn:
        theme = conn.execute(
            "SELECT id, name FROM themes WHERE id = %s OR name ILIKE %s LIMIT 1",
            (theme_filter, f"%{theme_filter}%"),
        ).fetchone()

    if not theme:
        return f"Theme not found: `{theme_filter}`"

    theme_id = theme["id"]
    theme_name = theme["name"]

    # Gather context
    state = get_theme_state(theme_id)
    breakthroughs = get_recent_breakthroughs(days=90, theme_id=theme_id)
    ranked_bottlenecks = get_bottleneck_ranking(theme_id=theme_id)
    implications = get_consolidated_implications(theme_id, limit=10)

    theme_context = f"**{theme_name}** (`{theme_id}`)"
    if state.get("theme", {}).get("state_summary"):
        theme_context += f"\n{truncate_sentences(state['theme']['state_summary'], 600)}"

    # Bottleneck descriptions kept full — core signal for predictions
    bottlenecks_text = "\n".join(
        f"- {b['description']} (horizon: {b.get('resolution_horizon', '?')}, "
        f"blocking: {truncate(b.get('blocking_what', '?'), 175)})"
        for b in ranked_bottlenecks[:8]
    ) or "(no bottlenecks)"

    # Breakthroughs: what_is_now_possible kept full — causal chain for predictions
    breakthroughs_text = "\n".join(
        f"- {b['description']} → {b.get('what_is_now_possible', '?')}"
        for b in breakthroughs[:5]
    ) or "(no recent breakthroughs)"

    implications_text = "\n".join(
        f"- {i['source_theme']} → {i['target_theme']}: "
        f"{truncate_sentences(i['top_implication'], 300)}"
        for i in implications[:8]
    ) or "(no implications)"

    # Fetch top claims for this theme by confidence
    with get_conn() as conn:
        top_claims = conn.execute(
            """SELECT c.claim_text, c.confidence, s.title
               FROM claims c
               JOIN source_themes st ON c.source_id = st.source_id
               JOIN sources s ON c.source_id = s.id
               WHERE st.theme_id = %s AND c.confidence >= 0.7
               ORDER BY c.confidence DESC
               LIMIT 15""",
            (theme_id,),
        ).fetchall()

    claims_text = "\n".join(
        f"- [{c.get('title', '?')[:40]}] {truncate_sentences(c['claim_text'], 200)} "
        f"(conf: {c.get('confidence', '?')})"
        for c in top_claims
    ) or "(no claims available)"

    existing_text = "\n".join(
        f"- {truncate_sentences(a.get('prediction', '?'), 200)} (conf: {a.get('confidence', '?')})"
        for a in state.get("anticipations", [])[:10]
    ) or "(no existing anticipations)"

    if on_progress:
        on_progress("Generating predictions...")

    # Priority-based context budgeting across sections
    _sections = [
        (10, "bottlenecks",   bottlenecks_text),
        (9,  "breakthroughs", breakthroughs_text),
        (8,  "implications",  implications_text),
        (7,  "claims",        claims_text),
        (5,  "theme_context", theme_context),
        (3,  "existing",      existing_text),
    ]
    _allocated = _budget_generate_sections(_sections, 8000)

    prompt = _GENERATE_PROMPT.format(
        theme_context=_allocated.get("theme_context", theme_context),
        bottlenecks_text=_allocated.get("bottlenecks", bottlenecks_text),
        breakthroughs_text=_allocated.get("breakthroughs", breakthroughs_text),
        implications_text=_allocated.get("implications", implications_text),
        claims_text=_allocated.get("claims", claims_text),
        existing_text=_allocated.get("existing", existing_text),
    )

    try:
        result = executor.run_raw(
            prompt,
            session_id="anticipate_generate",
            timeout=120,
        )
        llm_text = result.text
    except Exception as e:
        log.error("anticipate_generate_failed", error=str(e)[:200])
        return f"Anticipation generation failed: {str(e)[:200]}"

    parsed = _parse_json(llm_text)
    anticipations = parsed.get("anticipations", [])

    if not anticipations and llm_text:
        log.warning(
            "anticipate_zero_parsed",
            llm_text_len=len(llm_text),
            llm_text_snippet=llm_text[:300],
            parsed_keys=list(parsed.keys()) if parsed else [],
        )

    # Collect source IDs from landscape entities for provenance
    based_on_ids = []
    for b in breakthroughs[:5]:
        for sid in (b.get("evidence_sources") or []):
            if sid not in based_on_ids:
                based_on_ids.append(sid)
        if b.get("primary_source_id") and b["primary_source_id"] not in based_on_ids:
            based_on_ids.append(b["primary_source_id"])
    for b in ranked_bottlenecks[:8]:
        for sid in (b.get("evidence_sources") or []):
            if sid not in based_on_ids:
                based_on_ids.append(sid)
    for imp in implications[:8]:
        for sid in (imp.get("source_ids") or []):
            if sid not in based_on_ids:
                based_on_ids.append(sid)

    # Persist
    created = []
    for ant in anticipations:
        try:
            ant_id = f"ant_{ULID()}"
            insert_anticipation(
                id=ant_id,
                theme_id=theme_id,
                prediction=ant["prediction"],
                based_on=based_on_ids or [],
                reasoning=ant.get("reasoning"),
                confidence=ant.get("confidence"),
                timeline=ant.get("timeline"),
                attribution="user_generation",
                would_confirm=ant.get("would_confirm"),
                would_invalidate=ant.get("would_invalidate"),
            )
            created.append({"id": ant_id, **ant})
        except Exception as e:
            log.warning("anticipation_insert_failed", error=str(e)[:200])

    # Format response
    lines = [f"**Generated {len(created)} anticipations for {theme_name}**\n"]

    # Show narrative before JSON
    json_start = llm_text.find("```json")
    if json_start > 0:
        lines.append(llm_text[:json_start].strip())
        lines.append("")

    for a in created:
        lines.append(
            f"- `{a['id']}` [{a.get('timeline', '?')}] (conf: {a.get('confidence', '?')})\n"
            f"  {a.get('prediction', '?')[:150]}"
        )

    if not created:
        lines.append("No anticipations could be created. Try a different theme.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# /anticipate evolve
# ---------------------------------------------------------------------------

def _handle_evolve(theme_filter: str, executor, on_progress, log) -> str:
    """Retire stale anticipations and regenerate replacements."""
    from reading_app.db import get_conn, update_anticipation_status, insert_landscape_history
    from retrieval.landscape import compute_anticipation_staleness

    if not theme_filter:
        return "Usage: `/anticipate evolve <theme>`"

    if on_progress:
        on_progress(f"Computing staleness for **{theme_filter}**...")

    # Resolve theme
    with get_conn() as conn:
        theme = conn.execute(
            "SELECT id, name FROM themes WHERE id = %s OR name ILIKE %s LIMIT 1",
            (theme_filter, f"%{theme_filter}%"),
        ).fetchone()

    if not theme:
        return f"Theme not found: `{theme_filter}`"

    theme_id = theme["id"]
    theme_name = theme["name"]

    stale = compute_anticipation_staleness(theme_id)
    stale_threshold = [a for a in stale if a["staleness"] > 0.5]

    lines = [f"**Anticipation Evolution — {theme_name}**\n"]

    if not stale_threshold:
        lines.append("No stale anticipations found (staleness > 0.5).")
        lines.append(f"\nAll {len(stale)} open anticipations are fresh enough to keep.")
        return "\n".join(lines)

    # Show stale anticipations
    lines.append(f"**{len(stale_threshold)} stale anticipations** (of {len(stale)} open):\n")

    retired = []
    kept = []

    for a in stale_threshold:
        staleness = a["staleness"]
        age_days = a["age_days"]
        evidence_count = a.get("evidence_count", 0)

        # Auto-retire if staleness > 0.7 or timeline clearly expired
        should_retire = staleness > 0.7

        status_label = "RETIRING" if should_retire else "STALE (keeping)"
        lines.append(
            f"- `{a['id']}` [{status_label}] staleness={staleness:.2f}, "
            f"age={age_days}d, evidence={evidence_count}\n"
            f"  {a.get('prediction', '?')[:120]}"
        )

        if should_retire:
            try:
                update_anticipation_status(a["id"], "expired")
                insert_landscape_history(
                    entity_type="anticipation",
                    entity_id=a["id"],
                    field="status",
                    old_value="open",
                    new_value="expired",
                    attribution="staleness_evolution",
                )
                retired.append(a)
            except Exception as e:
                log.warning("evolve_retire_failed", id=a["id"], error=str(e)[:200])
        else:
            kept.append(a)

    lines.append(f"\n**Retired:** {len(retired)} | **Kept (monitoring):** {len(kept)}")

    # Regenerate if we retired any
    if retired and executor:
        if on_progress:
            on_progress(f"Regenerating predictions for {theme_name}...")

        result = _handle_generate(theme_id, executor, on_progress, log)
        lines.append(f"\n---\n{result}")
    elif retired:
        lines.append(
            f"\nUse `/anticipate generate {theme_name}` to create replacement predictions."
        )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# /anticipate calibration
# ---------------------------------------------------------------------------

def _handle_calibration(on_progress, log) -> str:
    """Compute Brier scores for resolved anticipations."""
    from reading_app.db import get_conn

    if on_progress:
        on_progress("Computing calibration scores...")

    with get_conn() as conn:
        resolved = conn.execute(
            """SELECT a.*, t.name AS theme_name
               FROM anticipations a
               LEFT JOIN themes t ON a.theme_id = t.id
               WHERE a.status IN ('confirmed', 'invalidated')
               ORDER BY a.last_reviewed DESC NULLS LAST"""
        ).fetchall()

    if not resolved:
        # Even without resolutions, show open prediction portfolio stats
        with get_conn() as conn2:
            return _format_open_portfolio(conn2, log)

    # Compute Brier scores
    brier_scores = []
    by_bucket = {}  # confidence bucket -> [outcomes]

    for a in resolved:
        confidence = a.get("confidence") or 0.5
        outcome = 1.0 if a["status"] == "confirmed" else 0.0
        brier = (confidence - outcome) ** 2
        brier_scores.append(brier)

        # Bucket by confidence ranges
        bucket = _confidence_bucket(confidence)
        by_bucket.setdefault(bucket, []).append(outcome)

    mean_brier = sum(brier_scores) / len(brier_scores) if brier_scores else 0
    n_confirmed = sum(1 for a in resolved if a["status"] == "confirmed")
    n_invalidated = len(resolved) - n_confirmed

    lines = ["**Anticipation Calibration**\n"]
    lines.append(f"**Resolved:** {len(resolved)} ({n_confirmed} confirmed, {n_invalidated} invalidated)")
    lines.append(f"**Mean Brier Score:** {mean_brier:.3f} (0 = perfect, 0.25 = random)")

    # Interpret
    if mean_brier < 0.1:
        lines.append("Calibration: **Excellent** — predictions are well-calibrated")
    elif mean_brier < 0.2:
        lines.append("Calibration: **Good** — somewhat overconfident or underconfident")
    elif mean_brier < 0.25:
        lines.append("Calibration: **Fair** — comparable to random guessing")
    else:
        lines.append("Calibration: **Poor** — predictions are systematically miscalibrated")

    # Calibration curve
    lines.append("\n**Calibration by confidence bucket:**")
    lines.append(f"{'Bucket':<15} {'Predicted':>10} {'Actual':>10} {'Count':>7} {'Gap':>7}")
    lines.append("-" * 52)

    for bucket_label in ["0.0-0.3", "0.3-0.5", "0.5-0.7", "0.7-0.9", "0.9-1.0"]:
        outcomes = by_bucket.get(bucket_label, [])
        if not outcomes:
            continue
        actual_rate = sum(outcomes) / len(outcomes)
        # Midpoint of bucket as predicted
        lo, hi = [float(x) for x in bucket_label.split("-")]
        predicted = (lo + hi) / 2
        gap = abs(predicted - actual_rate)
        lines.append(
            f"{bucket_label:<15} {predicted:>10.2f} {actual_rate:>10.2f} "
            f"{len(outcomes):>7} {gap:>7.2f}"
        )

    # Recent resolutions
    lines.append("\n**Recent resolutions:**")
    for a in resolved[:10]:
        conf = a.get("confidence") or 0.5
        outcome = "confirmed" if a["status"] == "confirmed" else "invalidated"
        brier = (conf - (1.0 if outcome == "confirmed" else 0.0)) ** 2
        lines.append(
            f"- `{a['id']}` [{a.get('theme_name', '?')}] "
            f"conf={conf:.2f} → {outcome} (Brier: {brier:.3f})\n"
            f"  {a.get('prediction', '?')[:100]}"
        )

    # Bias detection
    if n_confirmed > 0 and n_invalidated > 0:
        avg_conf_confirmed = sum(
            (a.get("confidence") or 0.5) for a in resolved if a["status"] == "confirmed"
        ) / n_confirmed
        avg_conf_invalidated = sum(
            (a.get("confidence") or 0.5) for a in resolved if a["status"] == "invalidated"
        ) / n_invalidated

        lines.append(f"\n**Bias check:**")
        lines.append(f"- Avg confidence on confirmed: {avg_conf_confirmed:.2f}")
        lines.append(f"- Avg confidence on invalidated: {avg_conf_invalidated:.2f}")

        if avg_conf_invalidated > 0.6:
            lines.append("⚠ You may be systematically overconfident — "
                         "high-confidence predictions are being invalidated")
        if avg_conf_confirmed < 0.4:
            lines.append("⚠ You may be systematically underconfident — "
                         "low-confidence predictions are being confirmed")

    # Append open portfolio stats
    try:
        with get_conn() as conn2:
            open_ants = conn2.execute(
                """SELECT a.confidence, a.timeline, t.name AS theme_name
                   FROM anticipations a
                   LEFT JOIN themes t ON a.theme_id = t.id
                   WHERE a.status NOT IN ('confirmed', 'invalidated')"""
            ).fetchall()
        if open_ants:
            lines.append(f"\n**Open predictions:** {len(open_ants)} still pending")
            avg_open = sum((a.get("confidence") or 0.5) for a in open_ants) / len(open_ants)
            lines.append(f"Average open confidence: {avg_open:.2f}")
    except Exception:
        pass

    return "\n".join(lines)


def _format_open_portfolio(conn, log) -> str:
    """Show portfolio stats for open predictions even when nothing is resolved."""
    try:
        open_ants = conn.execute(
            """SELECT a.*, t.name AS theme_name
               FROM anticipations a
               LEFT JOIN themes t ON a.theme_id = t.id
               WHERE a.status NOT IN ('confirmed', 'invalidated')
               ORDER BY a.confidence DESC NULLS LAST"""
        ).fetchall()
    except Exception as e:
        log.warning("calibration_open_portfolio_failed", error=str(e)[:200])
        return (
            "**No resolved anticipations for calibration.**\n\n"
            "Resolve anticipations with `/anticipate confirm <id>` or "
            "`/anticipate invalidate <id>` to start tracking calibration."
        )

    if not open_ants:
        return (
            "**No anticipations tracked.**\n\n"
            "Generate predictions with `/anticipate generate <theme>`."
        )

    lines = ["**Anticipation Calibration — No Resolutions Yet**\n"]
    lines.append(f"**Open predictions:** {len(open_ants)}\n")

    # By confidence bucket
    by_bucket: dict[str, list] = {}
    for a in open_ants:
        bucket = _confidence_bucket(a.get("confidence") or 0.5)
        by_bucket.setdefault(bucket, []).append(a)

    lines.append("**Confidence distribution:**")
    for bucket_label in ["0.0-0.3", "0.3-0.5", "0.5-0.7", "0.7-0.9", "0.9-1.0"]:
        ants = by_bucket.get(bucket_label, [])
        if ants:
            bar = "█" * len(ants)
            lines.append(f"  {bucket_label}: {bar} ({len(ants)})")

    # By timeline
    by_timeline: dict[str, int] = {}
    for a in open_ants:
        tl = a.get("timeline") or "unknown"
        by_timeline[tl] = by_timeline.get(tl, 0) + 1

    lines.append("\n**Timeline distribution:**")
    for tl, count in sorted(by_timeline.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {tl}: {count}")

    # By theme
    by_theme: dict[str, int] = {}
    for a in open_ants:
        tn = a.get("theme_name") or "unlinked"
        by_theme[tn] = by_theme.get(tn, 0) + 1

    lines.append("\n**Theme coverage:**")
    for tn, count in sorted(by_theme.items(), key=lambda x: x[1], reverse=True)[:10]:
        lines.append(f"  {tn}: {count}")

    avg_conf = sum((a.get("confidence") or 0.5) for a in open_ants) / len(open_ants)
    lines.append(f"\n**Average confidence:** {avg_conf:.2f}")

    if avg_conf > 0.7:
        lines.append("Note: High average confidence — consider whether you're being overconfident.")
    elif avg_conf < 0.4:
        lines.append("Note: Low average confidence — consider strengthening predictions with evidence.")

    lines.append(
        "\n---\n"
        "Resolve predictions to start tracking calibration:\n"
        "- `/anticipate confirm <id>`\n"
        "- `/anticipate invalidate <id>`"
    )

    return "\n".join(lines)


def _confidence_bucket(confidence: float) -> str:
    if confidence < 0.3:
        return "0.0-0.3"
    if confidence < 0.5:
        return "0.3-0.5"
    if confidence < 0.7:
        return "0.5-0.7"
    if confidence < 0.9:
        return "0.7-0.9"
    return "0.9-1.0"


# ---------------------------------------------------------------------------
# JSON parsing
# ---------------------------------------------------------------------------

def _parse_json(text: str) -> dict:
    """Extract JSON block from LLM output."""
    result = parse_json_from_llm(text, expect=dict)
    if result is None:
        logger.warning("anticipate_no_json_parsed", llm_text_snippet=text[:500] if text else "(empty)")
        return {}
    return result
