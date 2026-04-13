"""Direct Python handler for /implications jobs.

Bypasses the Claude CLI subprocess. Pre-fetches context, runs parallel
sub-analyses (Mode A) or a single thesis-validation call (Mode B),
parses structured output, and persists landscape entities to DB.
"""

from __future__ import annotations

import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable

import structlog
from ulid import ULID

from gateway.models import Event, Job

logger = structlog.get_logger(__name__)

_ID_RE = re.compile(r"[0-9A-Z]{26}")


# ---------------------------------------------------------------------------
# Per-call prompt templates (Mode A — parallel sub-analyses)
# ---------------------------------------------------------------------------

_CALL_A_PROMPT = """\
You are analysing a source's impact on AI landscape themes and capabilities.

## Source
{source_header}

## Claims
{claims_text}

## Theme States
{theme_states_text}

## Instructions

Answer two questions:

1. **Theme impact**: Which themes does this source affect, and how? Be specific.
2. **Capability maturity**: Does this change any capability maturity levels?
   If yes, specify old → new with evidence from the claims above.

Write a narrative analysis, then output a JSON block:

```json
{{
  "cross_theme_implications": [
    {{
      "source_theme_id": "...",
      "target_theme_id": "...",
      "trigger_type": "breakthrough|bottleneck_resolved|capability_matured|convergence|analogy",
      "implication": "...",
      "confidence": 0.0-1.0,
      "strength": "strong|moderate|speculative",
      "temporal_projection": "If this trend continues, within [timeframe]...",
      "evidence_sources": ["{source_id}"]
    }}
  ]
}}
```

- **strength**: "strong" = multiple sources with direct evidence; "moderate" = single source but clear mechanism; "speculative" = plausible but thin evidence.
- **temporal_projection**: What happens if this implication plays out? Be specific about timeframe and concrete effects.

Only output implications with genuine evidence. Do not pad the list.
"""

_CALL_B_PROMPT = """\
You are analysing a source for limitation signals and bottleneck effects.

## Source
{source_header}

## Claims
{claims_text}

## Current Bottlenecks
{bottlenecks_text}

## Current Limitations
{limitations_text}

## Instructions

Answer two questions:

1. **Limitation signals**: Does this source reveal new limitations or confirm existing ones?
   Pay special attention to implicit signals: performance cliffs, hedging language,
   controlled conditions, conspicuous absences, buried scale/cost.
2. **Bottleneck effects**: Which bottlenecks above does this affect?
   For each: does it reduce, confirm, reveal, or reframe the bottleneck?

Write a narrative analysis, then output a JSON block:

```json
{{
  "bottleneck_updates": [
    {{
      "bottleneck_id": "...",
      "change": "reduce|confirm|reveal|reframe",
      "reasoning": "..."
    }}
  ]
}}
```

Only reference bottleneck IDs from the list above. Be specific about evidence.
"""

_CALL_C_PROMPT = """\
You are analysing a source for breakthrough signals and anticipation matches.

## Source
{source_header}

## Claims
{claims_text}

## Open Anticipations
{anticipations_text}

## Recent Breakthroughs
{breakthroughs_text}

## Instructions

Answer two questions:

1. **Breakthrough assessment**: Does this source change what was believed possible?
   If yes, describe: what was believed before, what is now possible,
   immediate implications, downstream implications.
2. **Anticipation updates**: Do any open anticipations above match evidence from
   this source? For each match, specify the anticipation ID, match_type
   (confirming/disconfirming/partial), and the evidence text from the claims.

Write a narrative analysis, then output a JSON block:

```json
{{
  "anticipation_updates": [
    {{
      "anticipation_id": "...",
      "match_type": "confirming|disconfirming|partial",
      "evidence_text": "..."
    }}
  ],
  "new_anticipations": [
    {{
      "theme_id": "...",
      "prediction": "...",
      "confidence": 0.0-1.0,
      "timeline": "...",
      "reasoning": "..."
    }}
  ]
}}
```

Only create new anticipations when the source reveals genuinely predictable trajectories.
"""

_CALL_D_PROMPT = """\
You are identifying cross-theme implications and reading directions.

## Source
{source_header}

## Source Themes
{themes_text}

## Summary
{summary_excerpt}

## Existing Cross-Theme Implications
{existing_implications_text}

## Instructions

Answer two questions:

1. **Cross-theme implications**: What non-obvious connections does this source
   reveal between different AI themes? Look for: mechanisms that transfer between
   domains, convergences that amplify effects, analogies that reframe problems.
   Do NOT repeat implications already listed above.
2. **Reading directions**: What should the user read next to better understand
   this source's implications? Be specific about topics and why.

Write a narrative analysis, then output a JSON block:

```json
{{
  "cross_theme_implications": [
    {{
      "source_theme_id": "...",
      "target_theme_id": "...",
      "trigger_type": "breakthrough|bottleneck_resolved|capability_matured|convergence|analogy",
      "implication": "...",
      "confidence": 0.0-1.0,
      "strength": "strong|moderate|speculative",
      "temporal_projection": "If this trend continues, within [timeframe]...",
      "evidence_sources": ["{source_id}"]
    }}
  ]
}}
```

- **strength**: "strong" = multiple sources with direct evidence; "moderate" = single source but clear mechanism; "speculative" = plausible but thin evidence.
- **temporal_projection**: What happens if this implication plays out? Be specific about timeframe and concrete effects.

Only output genuinely non-obvious implications grounded in this source.
"""


# ---------------------------------------------------------------------------
# Mode B prompt (single call — holistic thesis validation)
# ---------------------------------------------------------------------------

_MODE_B_PROMPT = """\
You are validating a user-provided thesis about cross-domain implications.

## Source
{source_header}

## Claims
{claims_text}

## Theme States
{theme_states_text}

## Existing Implications
{existing_implications_text}

## User Thesis

{user_thesis}

## Instructions

### Step 1: Parse the thesis
Decompose into:
- **Source theme(s)**: where the insight originates
- **Target theme(s)**: where it has implications
- **Trigger type**: breakthrough | bottleneck_resolved | capability_matured | convergence | analogy
- **Mechanism**: HOW does progress in source theme affect the target?
- **Confidence assessment**: how speculative is this?

### Step 2: Validate against evidence
Search the claims and theme states for:
- **Supporting evidence**: claims, capabilities, breakthroughs that align. Quote specific evidence_snippets.
- **Contradicting evidence**: claims, limitations, bottlenecks that challenge. Be honest.
- **Gaps**: what evidence is MISSING that would strengthen or weaken the case?

### Step 3: Output

Write a **narrative validation** with supporting/contradicting evidence.

Then output a JSON block:

```json
{{
  "cross_theme_implications": [
    {{
      "source_theme_id": "...",
      "target_theme_id": "...",
      "trigger_type": "...",
      "implication": "...",
      "confidence": 0.0-1.0,
      "strength": "strong|moderate|speculative",
      "temporal_projection": "If this trend continues, within [timeframe]...",
      "evidence_sources": ["{source_id}"]
    }}
  ],
  "new_anticipations": [
    {{
      "theme_id": "...",
      "prediction": "...",
      "confidence": 0.0-1.0,
      "timeline": "...",
      "reasoning": "..."
    }}
  ],
  "bottleneck_updates": [
    {{
      "bottleneck_id": "...",
      "change": "reduce|confirm|reveal|reframe",
      "reasoning": "..."
    }}
  ]
}}
```

- **strength**: "strong" = multiple sources with direct evidence; "moderate" = single source but clear mechanism; "speculative" = plausible but thin evidence.
- **temporal_projection**: What happens if this implication plays out? Be specific about timeframe and concrete effects.

Every entry must be grounded in specific claims from the context.
"""


# ---------------------------------------------------------------------------
# Context slice builders
# ---------------------------------------------------------------------------

def _source_header(ctx: dict) -> str:
    meta = ctx["source_meta"]
    return (
        f"**{meta.get('title', meta['id'])}**\n"
        f"- ID: `{meta['id']}`\n"
        f"- Type: {meta.get('source_type', 'N/A')}\n"
        f"- Published: {str(meta.get('published_at', 'N/A'))[:10]}"
    )


def _claims_text(ctx: dict, limit: int = 30) -> str:
    claims = ctx.get("claims", [])[:limit]
    if not claims:
        return "(no claims)"
    lines = []
    for c in claims:
        conf = f" (conf: {c['confidence']:.2f})" if c.get("confidence") else ""
        lines.append(f"- [{c.get('section', '?')}] {c['claim_text']}{conf}")
        if c.get("evidence_snippet"):
            lines.append(f"  > \"{c['evidence_snippet'][:200]}\"")
    return "\n".join(lines)


def _wiki_section_text(ctx: dict, section_name: str, max_chars: int = 600) -> str:
    """Extract a named section from wiki theme narratives."""
    wiki_ctx = ctx.get("wiki_context")
    if not wiki_ctx or not getattr(wiki_ctx, 'theme_narratives', None):
        return ""
    from retrieval.wiki_retrieval import extract_section
    parts = []
    for tid, narrative in wiki_ctx.theme_narratives.items():
        section = extract_section(narrative, section_name, max_chars=max_chars)
        if not section:
            continue
        # Extract theme name from first heading
        name = tid
        for line in narrative.split("\n"):
            if line.strip().startswith("# "):
                name = line.strip().lstrip("# ").strip()
                break
        parts.append(f"**{name}**:\n{section}")
    return "\n\n".join(parts)


def _theme_states_text(ctx: dict) -> str:
    # Primary: wiki-based landscape narratives (pre-compiled)
    wiki_ctx = ctx.get("wiki_context")
    if wiki_ctx and getattr(wiki_ctx, 'theme_narratives', None):
        from retrieval.wiki_retrieval import format_wiki_context_block
        return format_wiki_context_block(wiki_ctx, header="Theme Landscape")
    # Fallback: structured DB theme states
    parts = []
    for tid, state in ctx.get("theme_states", {}).items():
        theme = state.get("theme")
        if not theme:
            continue
        parts.append(f"### {theme.get('name', tid)} (`{tid}`)")

        caps = state.get("capabilities", [])
        if caps:
            parts.append("**Capabilities:**")
            for c in caps[:8]:
                parts.append(f"- {c['description']} (maturity: {c.get('maturity', '?')})")

        lims = state.get("limitations", [])
        if lims:
            parts.append("**Limitations:**")
            for lim in lims[:8]:
                parts.append(
                    f"- {lim['description']} (type: {lim.get('limitation_type', '?')}, "
                    f"severity: {lim.get('severity', '?')})"
                )

        bns = state.get("bottlenecks", [])
        if bns:
            parts.append("**Bottlenecks:**")
            for b in bns[:8]:
                parts.append(
                    f"- [{b.get('id', '?')}] {b['description']} "
                    f"(horizon: {b.get('resolution_horizon', '?')})"
                )
        parts.append("")
    return "\n".join(parts) if parts else "(no theme states)"


def _bottlenecks_text(ctx: dict) -> str:
    # Primary: wiki section extraction
    wiki_text = _wiki_section_text(ctx, "Bottlenecks")
    if wiki_text:
        return wiki_text
    # Fallback: structured DB theme states
    lines = []
    for state in ctx.get("theme_states", {}).values():
        for b in state.get("bottlenecks", []):
            lines.append(
                f"- **{b.get('id', '?')}**: {b['description']}\n"
                f"  Type: {b.get('bottleneck_type', '?')} | "
                f"Horizon: {b.get('resolution_horizon', '?')} | "
                f"Blocking: {b.get('blocking_what', '?')[:80]}"
            )
    return "\n".join(lines) if lines else "(no bottlenecks)"


def _limitations_text(ctx: dict) -> str:
    # Primary: wiki section extraction
    wiki_text = _wiki_section_text(ctx, "Limitations")
    if wiki_text:
        return wiki_text
    # Fallback: structured DB theme states
    lines = []
    for state in ctx.get("theme_states", {}).values():
        for lim in state.get("limitations", []):
            lines.append(
                f"- {lim['description']} "
                f"(type: {lim.get('limitation_type', '?')}, "
                f"severity: {lim.get('severity', '?')}, "
                f"trajectory: {lim.get('trajectory', '?')})"
            )
    return "\n".join(lines) if lines else "(no limitations)"


def _anticipations_text(ctx: dict) -> str:
    ants = ctx.get("anticipations", [])
    if not ants:
        return "(no open anticipations)"
    lines = []
    for a in ants[:15]:
        ev_count = len(a.get("status_evidence") or []) if isinstance(a.get("status_evidence"), list) else 0
        lines.append(
            f"- **{a.get('id', '?')}** [{a.get('theme_name', '?')}]: {a['prediction']}\n"
            f"  Confidence: {a.get('confidence', '?')} | "
            f"Timeline: {a.get('timeline', '?')} | "
            f"Evidence so far: {ev_count}"
        )
    return "\n".join(lines)


def _breakthroughs_text(ctx: dict) -> str:
    # Primary: wiki section extraction
    wiki_text = _wiki_section_text(ctx, "Breakthroughs")
    if wiki_text:
        return wiki_text
    # Fallback: structured DB theme states
    lines = []
    for state in ctx.get("theme_states", {}).values():
        for b in state.get("breakthroughs", []):
            lines.append(
                f"- {b['description']} (significance: {b.get('significance', '?')})\n"
                f"  Now possible: {b.get('what_is_now_possible', '?')[:120]}"
            )
    return "\n".join(lines) if lines else "(no recent breakthroughs)"


def _themes_text(ctx: dict) -> str:
    lines = []
    for t in ctx.get("themes", []):
        vel = f", velocity: {t.get('velocity', '?')}" if t.get("velocity") else ""
        lines.append(f"- **{t['name']}** (`{t['id']}`{vel})")
        if t.get("state_summary"):
            lines.append(f"  {t['state_summary'][:200]}")
    return "\n".join(lines) if lines else "(no themes)"


def _summary_excerpt(ctx: dict, limit: int = 3000) -> str:
    s = ctx.get("deep_summary", "")
    if not s:
        return "(no summary)"
    return s[:limit]


def _valid_theme_ids_hint(ctx: dict) -> str:
    """Build a hint listing all valid theme IDs for the LLM."""
    from reading_app.db import get_conn
    try:
        with get_conn() as conn:
            rows = conn.execute("SELECT id, name FROM themes ORDER BY id").fetchall()
            lines = [f"**Valid theme IDs** (use these exact IDs, not names):"]
            for r in rows:
                lines.append(f"- `{r['id']}` ({r['name']})")
            return "\n".join(lines)
    except Exception:
        # Fall back to source themes only
        lines = ["**Valid theme IDs** (use these exact IDs, not names):"]
        for t in ctx.get("themes", []):
            lines.append(f"- `{t['id']}` ({t['name']})")
        return "\n".join(lines)


def _existing_implications_text(ctx: dict) -> str:
    imps = ctx.get("consolidated_implications", [])
    if not imps:
        return "(no existing implications)"
    lines = []
    for imp in imps[:15]:
        lines.append(
            f"- {imp['source_theme']} → {imp['target_theme']}: "
            f"{imp['top_implication'][:150]}"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def handle_implications_job(
    event: Event,
    job: Job,
    config,
    executor,
    *,
    on_progress: Callable[[str], None] | None = None,
) -> str:
    """Run /implications directly.

    Mode A: 4 parallel sub-analyses → merge → persist.
    Mode B: single thesis-validation call → persist.
    """
    text = event.payload.get("text", "")
    source_id, user_thesis = _parse_command(text)

    log = logger.bind(job_id=job.id, source_id=source_id, mode="B" if user_thesis else "A")
    log.info("implications_handler_start")
    t0 = time.monotonic()

    # Pre-fetch context
    if on_progress:
        on_progress("Loading implications context...")

    from reading_app.db import ensure_pool
    ensure_pool()

    from retrieval.implications_context import gather_implications_context
    ctx = gather_implications_context(source_id)
    if ctx is None:
        raise ValueError(f"Source not found: {source_id}")

    title = ctx["source_meta"].get("title", source_id)
    log.info("implications_context_loaded", themes=len(ctx["themes"]),
             claims=len(ctx.get("claims", [])))

    if on_progress:
        themes_str = ", ".join(t["name"] for t in ctx["themes"])
        on_progress(f"Analysing **{title}** (themes: {themes_str})...")

    # Run analysis
    if user_thesis:
        llm_text, structured = _run_mode_b(ctx, source_id, user_thesis, executor, log, on_progress)
        attribution = "user_implication"
    else:
        llm_text, structured = _run_mode_a(ctx, source_id, executor, log, on_progress)
        attribution = "automated_implication"

    # Persist
    if on_progress:
        on_progress("Persisting landscape entries...")

    persist_summary = _persist_entries(structured, source_id, attribution, user_thesis, log)

    # --- Wiki updates (best-effort) ---
    _wiki_pages_updated = 0
    try:
        from retrieval.wiki_writer import file_implications_to_wiki
        wiki_stats = file_implications_to_wiki(structured, attribution)
        _wiki_pages_updated = wiki_stats.get("pages_updated", 0)
        if _wiki_pages_updated:
            log.info("implications_wiki_updated", **wiki_stats)
    except Exception:
        log.debug("implications_wiki_update_failed", exc_info=True)

    elapsed = time.monotonic() - t0
    log.info("implications_handler_complete", elapsed_s=round(elapsed, 1), **persist_summary)

    # Build response
    summary_lines = [llm_text, "\n---\n", "**Persisted to landscape:**"]
    summary_lines.append(f"- {persist_summary.get('implications', 0)} cross-theme implications")
    summary_lines.append(f"- {persist_summary.get('anticipation_updates', 0)} anticipation updates")
    summary_lines.append(f"- {persist_summary.get('new_anticipations', 0)} new anticipations")
    summary_lines.append(f"- {persist_summary.get('bottleneck_updates', 0)} bottleneck updates")
    if persist_summary.get("skipped"):
        summary_lines.append(f"- {persist_summary['skipped']} skipped (unknown theme IDs)")
    if persist_summary.get("errors"):
        summary_lines.append(f"- {persist_summary['errors']} errors (check logs)")
    summary_lines.append(f"\nAttribution: `{attribution}` | Completed in {elapsed:.0f}s")
    if _wiki_pages_updated:
        summary_lines.append(f"\n_Wiki updated: {_wiki_pages_updated} theme page(s) updated._")

    if on_progress:
        on_progress(
            f"Done: {persist_summary.get('implications', 0)} implications, "
            f"{persist_summary.get('new_anticipations', 0)} anticipations persisted "
            f"({elapsed:.0f}s)"
        )

    return "\n".join(summary_lines)


# ---------------------------------------------------------------------------
# Mode A — parallel sub-analyses
# ---------------------------------------------------------------------------

def _run_mode_a(ctx, source_id, executor, log, on_progress) -> tuple[str, dict]:
    """Run 4 parallel sub-analyses, merge narratives and structured output."""
    header = _source_header(ctx)
    claims = _claims_text(ctx, limit=30)
    theme_ids_hint = _valid_theme_ids_hint(ctx)

    calls = {
        "themes_capabilities": _CALL_A_PROMPT.format(
            source_header=header,
            claims_text=claims,
            theme_states_text=_theme_states_text(ctx),
            source_id=source_id,
        ) + f"\n\n{theme_ids_hint}",
        "limitations_bottlenecks": _CALL_B_PROMPT.format(
            source_header=header,
            claims_text=claims,
            bottlenecks_text=_bottlenecks_text(ctx),
            limitations_text=_limitations_text(ctx),
        ),
        "anticipations_breakthroughs": _CALL_C_PROMPT.format(
            source_header=header,
            claims_text=claims,
            anticipations_text=_anticipations_text(ctx),
            breakthroughs_text=_breakthroughs_text(ctx),
        ) + f"\n\n{theme_ids_hint}",
        "cross_theme_reading": _CALL_D_PROMPT.format(
            source_header=header,
            themes_text=_themes_text(ctx),
            summary_excerpt=_summary_excerpt(ctx),
            existing_implications_text=_existing_implications_text(ctx),
            source_id=source_id,
        ) + f"\n\n{theme_ids_hint}",
    }

    if on_progress:
        on_progress(f"Running 4 parallel analyses...")

    results: dict[str, str] = {}
    errors: dict[str, str] = {}

    def _run_call(name: str, prompt: str) -> tuple[str, str]:
        r = executor.run_raw(
            prompt,
            session_id=f"impl_{name}",
            timeout=300,
        )
        return name, r.text

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = {pool.submit(_run_call, n, p): n for n, p in calls.items()}
        for future in as_completed(futures):
            name = futures[future]
            try:
                _, text = future.result()
                results[name] = text
                log.info("implications_subcall_done", call=name, chars=len(text))
                if on_progress:
                    on_progress(f"  {name}: {len(text)} chars")
            except Exception as e:
                log.warning("implications_subcall_failed", call=name, error=str(e)[:200])
                errors[name] = str(e)[:200]

    # Merge narratives
    narrative_parts = []
    ordered_calls = ["themes_capabilities", "limitations_bottlenecks",
                     "anticipations_breakthroughs", "cross_theme_reading"]
    section_titles = {
        "themes_capabilities": "Theme Impact & Capability Maturity",
        "limitations_bottlenecks": "Limitation Signals & Bottleneck Effects",
        "anticipations_breakthroughs": "Breakthrough Assessment & Anticipation Updates",
        "cross_theme_reading": "Cross-Theme Implications & Reading Directions",
    }
    for call_name in ordered_calls:
        if call_name in results:
            # Extract narrative (everything before the JSON block)
            text = results[call_name]
            json_start = text.find("```json")
            if json_start == -1:
                json_start = text.rfind("{")
            narrative = text[:json_start].strip() if json_start > 0 else text
            narrative_parts.append(f"## {section_titles[call_name]}\n\n{narrative}")
        elif call_name in errors:
            narrative_parts.append(
                f"## {section_titles[call_name]}\n\n*(analysis failed: {errors[call_name]})*"
            )

    llm_text = "\n\n---\n\n".join(narrative_parts)

    # Merge structured outputs
    merged = {
        "cross_theme_implications": [],
        "anticipation_updates": [],
        "new_anticipations": [],
        "bottleneck_updates": [],
    }
    for text in results.values():
        parsed = _parse_structured_output(text)
        for key in merged:
            merged[key].extend(parsed.get(key, []))

    return llm_text, merged


# ---------------------------------------------------------------------------
# Mode B — single thesis validation call
# ---------------------------------------------------------------------------

def _run_mode_b(ctx, source_id, user_thesis, executor, log, on_progress) -> tuple[str, dict]:
    """Single holistic call for user thesis validation."""
    prompt = _MODE_B_PROMPT.format(
        source_header=_source_header(ctx),
        claims_text=_claims_text(ctx, limit=30),
        theme_states_text=_theme_states_text(ctx),
        existing_implications_text=_existing_implications_text(ctx),
        user_thesis=user_thesis,
        source_id=source_id,
    ) + f"\n\n{_valid_theme_ids_hint(ctx)}"

    result = executor.run_raw(
        prompt,
        session_id="implications_thesis",
        timeout=300,
    )

    structured = _parse_structured_output(result.text)
    return result.text, structured


# ---------------------------------------------------------------------------
# Command parsing
# ---------------------------------------------------------------------------

def _parse_command(text: str) -> tuple[str, str | None]:
    """Extract source_id and optional user thesis."""
    m = _ID_RE.search(text)
    if not m:
        raise ValueError(f"No source ID (ULID) found in: {text!r}")
    source_id = m.group(0)
    after = text[m.end():].strip()
    user_thesis = after if after else None
    return source_id, user_thesis


# ---------------------------------------------------------------------------
# Structured output parsing
# ---------------------------------------------------------------------------

def _parse_structured_output(text: str) -> dict:
    """Extract JSON block from LLM output."""
    json_match = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # Try bare JSON object (search from end for last complete object)
    brace = text.rfind("{")
    if brace >= 0:
        depth = 0
        for i in range(brace, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[brace:i + 1])
                    except json.JSONDecodeError:
                        break

    logger.warning("implications_no_json_parsed")
    return {}


# ---------------------------------------------------------------------------
# DB persistence
# ---------------------------------------------------------------------------

def _persist_entries(
    structured: dict,
    source_id: str,
    attribution: str,
    user_thesis: str | None,
    log,
) -> dict:
    """Persist structured entries to DB. Returns summary counts."""
    from reading_app.db import (
        get_conn,
        insert_cross_theme_implication,
        insert_anticipation,
        update_bottleneck,
        insert_landscape_history,
    )

    summary = {"implications": 0, "anticipation_updates": 0, "new_anticipations": 0,
               "bottleneck_updates": 0, "errors": 0, "skipped": 0}

    # Load valid theme IDs for FK validation
    valid_themes = set()
    try:
        with get_conn() as conn:
            rows = conn.execute("SELECT id FROM themes").fetchall()
            valid_themes = {r["id"] for r in rows}
    except Exception:
        log.warning("implications_theme_load_failed")

    # Cross-theme implications
    for imp in structured.get("cross_theme_implications", []):
        src_tid = imp.get("source_theme_id", "")
        tgt_tid = imp.get("target_theme_id", "")
        if valid_themes and (src_tid not in valid_themes or tgt_tid not in valid_themes):
            log.info("implications_skip_unknown_theme", source_theme=src_tid, target_theme=tgt_tid)
            summary["skipped"] += 1
            continue
        try:
            impl_id = f"impl_{ULID()}"
            # Build extended implication text with strength and temporal projection
            implication_text = imp["implication"]
            strength = imp.get("strength", "")
            temporal_projection = imp.get("temporal_projection", "")

            insert_cross_theme_implication(
                id=impl_id,
                source_theme_id=src_tid,
                target_theme_id=tgt_tid,
                trigger_type=imp.get("trigger_type", "convergence"),
                trigger_id=source_id,
                implication=implication_text,
                confidence=imp.get("confidence"),
                evidence_sources=imp.get("evidence_sources", [source_id]),
                attribution=attribution,
                attributed_reasoning=user_thesis,
            )

            # Store strength and temporal projection as landscape_history metadata
            if strength or temporal_projection:
                try:
                    meta_value = ""
                    if strength:
                        meta_value += f"strength={strength}"
                    if temporal_projection:
                        meta_value += f"; projection={temporal_projection[:200]}"
                    insert_landscape_history(
                        entity_type="implication",
                        entity_id=impl_id,
                        field="strength_and_projection",
                        old_value=None,
                        new_value=meta_value[:400],
                        source_id=source_id,
                        attribution=attribution,
                    )
                except Exception:
                    pass  # Non-critical metadata

            summary["implications"] += 1
        except Exception as e:
            log.warning("implications_persist_failed", entry_type="implication", error=str(e)[:200])
            summary["errors"] += 1

    # Anticipation updates (add evidence to existing)
    for upd in structured.get("anticipation_updates", []):
        try:
            ant_id = upd.get("anticipation_id")
            if not ant_id:
                continue
            with get_conn() as conn:
                row = conn.execute(
                    "SELECT status_evidence FROM anticipations WHERE id = %s", (ant_id,)
                ).fetchone()
                if row:
                    existing_evidence = row.get("status_evidence") or []
                    if not isinstance(existing_evidence, list):
                        existing_evidence = []
                    existing_evidence.append({
                        "source_id": source_id,
                        "match_type": upd.get("match_type", "partial"),
                        "evidence_text": upd.get("evidence_text", ""),
                        "attribution": attribution,
                    })
                    conn.execute(
                        "UPDATE anticipations SET status_evidence = %s WHERE id = %s",
                        (json.dumps(existing_evidence), ant_id),
                    )
                    conn.commit()
                    summary["anticipation_updates"] += 1

                    insert_landscape_history(
                        entity_type="anticipation",
                        entity_id=ant_id,
                        field="status_evidence",
                        old_value=None,
                        new_value=upd.get("evidence_text", "")[:200],
                        source_id=source_id,
                        attribution=attribution,
                    )
        except Exception as e:
            log.warning("implications_persist_failed", entry_type="anticipation_update", error=str(e)[:200])
            summary["errors"] += 1

    # New anticipations
    for ant in structured.get("new_anticipations", []):
        try:
            ant_id = f"ant_{ULID()}"
            insert_anticipation(
                id=ant_id,
                theme_id=ant["theme_id"],
                prediction=ant["prediction"],
                based_on=[source_id],
                reasoning=ant.get("reasoning"),
                confidence=ant.get("confidence"),
                timeline=ant.get("timeline"),
                attribution=attribution,
                attributed_reasoning=user_thesis,
            )
            summary["new_anticipations"] += 1
        except Exception as e:
            log.warning("implications_persist_failed", entry_type="new_anticipation", error=str(e)[:200])
            summary["errors"] += 1

    # Bottleneck updates
    for bu in structured.get("bottleneck_updates", []):
        try:
            bn_id = bu.get("bottleneck_id")
            if not bn_id:
                continue
            insert_landscape_history(
                entity_type="bottleneck",
                entity_id=bn_id,
                field="status",
                old_value=None,
                new_value=f"{bu.get('change', '?')}: {bu.get('reasoning', '')[:200]}",
                source_id=source_id,
                attribution=attribution,
            )
            summary["bottleneck_updates"] += 1
        except Exception as e:
            log.warning("implications_persist_failed", entry_type="bottleneck_update", error=str(e)[:200])
            summary["errors"] += 1

    return summary
