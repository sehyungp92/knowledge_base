"""Direct Python handler for /challenge jobs.

Bypasses the Claude CLI subprocess. Loads the target entity from DB,
builds a challenge context, delegates adversarial reasoning to
executor.run_raw(), parses the structured resolution, and persists
to challenge_log + conditionally updates the entity.
"""

from __future__ import annotations

import json
import re
import time

from ingest.json_parser import parse_json_from_llm
from typing import Callable

import structlog
from ulid import ULID

from gateway.models import Event, Job
from reading_app.text_utils import truncate, truncate_sentences, budget_context

logger = structlog.get_logger(__name__)

_ENTITY_TYPES = {"capability", "limitation", "bottleneck", "breakthrough", "anticipation"}


def _budget_sections(
    sections: list[tuple[int, str, str]], total_limit: int,
) -> dict[str, str]:
    """Allocate a character budget across named sections by priority.

    Takes ``(priority, key, text)`` tuples and returns ``{key: truncated_text}``.
    Higher priority = more space. Surplus from small sections flows to larger ones.
    """
    if not sections:
        return {}

    # Filter empty, sort by priority descending
    sections = [(p, k, t) for p, k, t in sections if t and t.strip()]
    sections = sorted(sections, key=lambda s: s[0], reverse=True)

    total_needed = sum(len(t) for _, _, t in sections)
    if total_needed <= total_limit:
        return {k: t for _, k, t in sections}

    total_priority = sum(p for p, _, _ in sections) or len(sections)
    allocations = {k: int((p / total_priority) * total_limit) for p, k, _ in sections}

    # Top-down fill: sections that fit donate surplus
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


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def handle_challenge_job(
    event: Event,
    job: Job,
    config,
    executor,
    *,
    on_progress: Callable[[str], None] | None = None,
) -> str:
    """Run /challenge directly."""
    text = event.payload.get("text", "")
    log = logger.bind(job_id=job.id)
    log.info("challenge_handler_start")
    t0 = time.monotonic()

    from reading_app.db import ensure_pool
    ensure_pool()

    entity_type, entity_id, steelman = _parse_command(text)
    log = log.bind(entity_type=entity_type, entity_id=entity_id, steelman=steelman)

    if entity_type == "belief":
        result = _handle_belief_challenge(entity_id, steelman, executor, on_progress, log)
    elif entity_type in _ENTITY_TYPES:
        result = _handle_landscape_challenge(entity_type, entity_id, executor, on_progress, log)
    else:
        return (
            f"Unknown entity type: `{entity_type}`\n\n"
            f"Usage:\n"
            f"- `/challenge <entity_type> <entity_id>` — challenge a landscape entity\n"
            f"  entity_type: capability, limitation, bottleneck, breakthrough, anticipation\n"
            f"- `/challenge belief <belief_id>` — self-challenge a tracked belief\n"
            f"- `/challenge belief <belief_id> steelman` — steelman mode"
        )

    elapsed = time.monotonic() - t0
    log.info("challenge_handler_complete", elapsed_s=round(elapsed, 1))
    return result


# ---------------------------------------------------------------------------
# Command parser
# ---------------------------------------------------------------------------

def _parse_command(text: str) -> tuple[str, str, bool]:
    """Parse '/challenge <entity_type> <entity_id> [steelman]'.

    Returns (entity_type, entity_id, is_steelman).
    """
    cleaned = text.strip()
    for prefix in ("/challenge ", "/challenge"):
        if cleaned.lower().startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
            break

    parts = cleaned.split()
    if len(parts) < 2:
        return cleaned or "unknown", "", False

    entity_type = parts[0].lower()
    entity_id = parts[1]
    steelman = len(parts) >= 3 and parts[2].lower() == "steelman"
    return entity_type, entity_id, steelman


# ---------------------------------------------------------------------------
# Entity loading helpers
# ---------------------------------------------------------------------------

def _load_entity(entity_type: str, entity_id: str) -> dict | None:
    """Load a landscape entity by type and ID."""
    from reading_app.db import get_conn, get_bottleneck, get_anticipation

    if entity_type == "bottleneck":
        return get_bottleneck(entity_id)
    if entity_type == "anticipation":
        return get_anticipation(entity_id)

    # capability, limitation, breakthrough — no dedicated getter, use raw query
    table = {
        "capability": "capabilities",
        "limitation": "limitations",
        "breakthrough": "breakthroughs",
    }.get(entity_type)
    if not table:
        return None

    with get_conn() as conn:
        return conn.execute(
            f"SELECT * FROM {table} WHERE id = %s", (entity_id,)
        ).fetchone()


def _entity_description(entity_type: str, entity: dict) -> str:
    """Build a human-readable description of the entity for prompts."""
    desc = entity.get("description", "N/A")
    conf = entity.get("confidence")
    conf_str = f" (confidence: {conf:.2f})" if conf is not None else ""

    lines = [f"**{entity_type.title()}**: {desc}{conf_str}"]

    if entity_type == "bottleneck":
        lines.append(f"  Blocking: {entity.get('blocking_what', 'N/A')}")
        lines.append(f"  Type: {entity.get('bottleneck_type', 'N/A')}")
        lines.append(f"  Resolution horizon: {entity.get('resolution_horizon', 'N/A')}")
    elif entity_type == "capability":
        lines.append(f"  Maturity: {entity.get('maturity', 'N/A')}")
    elif entity_type == "limitation":
        lines.append(f"  Type: {entity.get('limitation_type', 'N/A')}")
        lines.append(f"  Severity: {entity.get('severity', 'N/A')}")
        lines.append(f"  Trajectory: {entity.get('trajectory', 'N/A')}")
    elif entity_type == "breakthrough":
        lines.append(f"  Significance: {entity.get('significance', 'N/A')}")
        lines.append(f"  Previously believed: {entity.get('what_was_believed_before', 'N/A')}")
        lines.append(f"  Now possible: {entity.get('what_is_now_possible', 'N/A')}")
    elif entity_type == "anticipation":
        lines.append(f"  Prediction: {entity.get('prediction', 'N/A')}")
        lines.append(f"  Timeline: {entity.get('timeline', 'N/A')}")

    ev = entity.get("evidence_sources")
    if ev and isinstance(ev, list):
        lines.append(f"  Evidence sources: {', '.join(str(e) for e in ev[:5])}")

    return "\n".join(lines)


def _get_history_text(entity_type: str, entity_id: str) -> str:
    """Load landscape_history for an entity."""
    from reading_app.db import get_landscape_history
    history = get_landscape_history(entity_type, entity_id, limit=10)
    if not history:
        return "(no change history)"
    lines = []
    for h in history:
        lines.append(
            f"- [{str(h.get('changed_at', '?'))[:10]}] "
            f"{h.get('field', '?')}: {h.get('old_value', '?')} → {h.get('new_value', '?')} "
            f"(by: {h.get('attribution', '?')})"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Landscape challenge
# ---------------------------------------------------------------------------

_LANDSCAPE_CHALLENGE_PROMPT = """\
You are conducting an adversarial review of a landscape entity in an AI knowledge engine.

## Entity Under Challenge
{entity_text}

## Change History
{history_text}

## Library Evidence (related claims)
{evidence_text}

## Theme Context
{theme_text}

## Instructions

### Step 1: Present the System's Position
Articulate why the system currently holds this assessment. Cite specific evidence.

### Step 2: Construct the Challenge
Build the strongest possible case that this assessment is WRONG or INCOMPLETE:
- What evidence contradicts it?
- What has the assessment missed?
- What implicit assumptions could be invalid?
- Are there newer developments that change the picture?

### Step 3: Weigh Both Sides
Provide an honest assessment of both positions. Don't be afraid to conclude that the current assessment is correct.

### Step 4: Output

Write a narrative analysis, then output a JSON block:

```json
{{
  "system_position_summary": "Current assessment summary",
  "challenge_arguments": ["argument 1", "argument 2"],
  "challenge_evidence": ["specific claim or source reference"],
  "verdict": "system_updated|system_maintained|ambiguous_flagged",
  "reasoning": "Why this verdict",
  "suggested_changes": {{
    "field_name": "new_value"
  }}
}}
```

If verdict is "system_maintained", suggested_changes should be empty.
If verdict is "system_updated", include specific field changes.
If verdict is "ambiguous_flagged", explain what additional evidence is needed.
"""


def _handle_landscape_challenge(
    entity_type: str, entity_id: str, executor, on_progress, log
) -> str:
    """Challenge a landscape entity (capability, limitation, bottleneck, etc.)."""
    from reading_app.db import (
        get_conn, insert_challenge_log, insert_landscape_history,
        update_bottleneck,
    )
    from retrieval.hybrid import hybrid_retrieve

    if on_progress:
        on_progress(f"Loading {entity_type} `{entity_id}`...")

    entity = _load_entity(entity_type, entity_id)
    if not entity:
        return f"{entity_type.title()} not found: `{entity_id}`"

    entity_text = _entity_description(entity_type, entity)
    history_text = _get_history_text(entity_type, entity_id)

    # Load theme context
    theme_id = entity.get("theme_id")
    theme_text = "(no theme linked)"
    if theme_id:
        with get_conn() as conn:
            theme = conn.execute(
                "SELECT id, name, state_summary, velocity FROM themes WHERE id = %s",
                (theme_id,),
            ).fetchone()
            if theme:
                theme_text = (
                    f"**{theme['name']}** (velocity: {theme.get('velocity', '?')})\n"
                    f"{truncate_sentences(theme.get('state_summary') or 'no summary', 500)}"
                )

    # Evidence search
    if on_progress:
        on_progress("Searching for evidence...")

    evidence_text = "(no evidence found)"
    try:
        query = entity.get("description") or entity.get("prediction") or entity_id
        results = hybrid_retrieve(query, get_conn, k=10)
        if results:
            evidence_text = "\n".join(
                f"- [{r.get('source_id', '?')}] {truncate_sentences((r.get('claim_text') or ''), 250)}"
                for r in results
            )
    except Exception as e:
        log.warning("challenge_evidence_search_failed", error=str(e)[:200])

    # LLM analysis
    if on_progress:
        on_progress(f"Analysing challenge for {entity_type}...")

    prompt = _LANDSCAPE_CHALLENGE_PROMPT.format(
        entity_text=entity_text,
        history_text=history_text,
        evidence_text=evidence_text,
        theme_text=theme_text,
    )

    try:
        result = executor.run_raw(
            prompt,
            session_id="challenge_landscape",
            timeout=180,
        )
        llm_text = result.text
    except Exception as e:
        log.error("challenge_llm_failed", error=str(e)[:200])
        return f"Challenge analysis failed: {str(e)[:200]}"

    parsed = _parse_json(llm_text)
    verdict = parsed.get("verdict", "system_maintained")
    changes = parsed.get("suggested_changes", {})

    # Persist challenge log
    challenge_id = f"chal_{ULID()}"
    try:
        insert_challenge_log(
            id=challenge_id,
            entity_type=entity_type,
            entity_id=entity_id,
            system_position=parsed.get("system_position_summary"),
            system_evidence=parsed.get("challenge_evidence"),
            user_argument=None,  # system-initiated challenge
            outcome=verdict,
            resolution_reasoning=parsed.get("reasoning"),
            changes_made=list(changes.keys()) if changes else None,
        )
    except Exception as e:
        log.warning("challenge_log_insert_failed", error=str(e)[:200])

    # Apply changes if verdict is system_updated
    # Whitelist updatable fields per entity type to prevent SQL errors
    _ALLOWED_FIELDS = {
        "capability": {"description", "maturity", "confidence"},
        "limitation": {"description", "limitation_type", "severity", "trajectory", "confidence"},
        "bottleneck": {"description", "resolution_horizon", "confidence", "blocking_what", "bottleneck_type"},
        "breakthrough": {"description", "significance", "confidence"},
        "anticipation": {"prediction", "confidence", "timeline"},
    }
    allowed = _ALLOWED_FIELDS.get(entity_type, set())

    applied_changes = []
    if verdict == "system_updated" and changes:
        for field, new_value in changes.items():
            if field not in allowed:
                log.info("challenge_skip_unknown_field", field=field, entity_type=entity_type)
                continue
            try:
                old_value = str(entity.get(field, ""))
                if entity_type == "bottleneck":
                    update_bottleneck(entity_id, **{field: new_value})
                else:
                    table = {
                        "capability": "capabilities",
                        "limitation": "limitations",
                        "breakthrough": "breakthroughs",
                        "anticipation": "anticipations",
                    }.get(entity_type)
                    if table:
                        with get_conn() as conn:
                            conn.execute(
                                f"UPDATE {table} SET {field} = %s, last_updated = NOW() WHERE id = %s",
                                (new_value, entity_id),
                            )
                            conn.commit()

                insert_landscape_history(
                    entity_type=entity_type,
                    entity_id=entity_id,
                    field=field,
                    old_value=old_value[:200],
                    new_value=str(new_value)[:200],
                    attribution="user_challenge",
                )
                applied_changes.append(f"{field}: {old_value[:50]} → {str(new_value)[:50]}")
                try:
                    from ingest.correction_store import store_correction
                    store_correction(
                        entity_type, "reclassified",
                        {"field": field, "value": old_value[:200]},
                        {"field": field, "value": str(new_value)[:200]},
                        source_id=entity.get("source_id"),
                        theme_id=entity.get("theme_id"),
                        skill_origin="challenge",
                    )
                except Exception:
                    pass
            except Exception as e:
                log.warning("challenge_change_failed", field=field, error=str(e)[:200])

    # Check for linked beliefs, stale implications, anticipations, and dependent bottlenecks
    belief_warnings = []
    implication_warnings = []
    anticipation_warnings = []
    bottleneck_cascade_warnings = []
    if verdict == "system_updated" and applied_changes:
        belief_warnings = _check_beliefs_for_landscape_entity(
            entity_type, entity_id, entity, changes, log,
        )
        implication_warnings = _check_stale_implications(
            entity_type, entity_id, entity, log,
        )
        anticipation_warnings = _cascade_to_anticipations(
            entity_type, entity_id, entity, changes, log,
        )
        if entity_type == "bottleneck":
            bottleneck_cascade_warnings = _cascade_to_dependent_bottlenecks(
                entity_id, entity, changes, log,
            )

    # Build response
    response_lines = [llm_text, "\n---\n"]
    response_lines.append(f"**Resolution:** {verdict}")
    response_lines.append(f"Challenge log: `{challenge_id}`")
    if applied_changes:
        response_lines.append("\n**Changes applied:**")
        for c in applied_changes:
            response_lines.append(f"- {c}")
    if belief_warnings:
        response_lines.append("\n**Linked beliefs to review:**")
        for w in belief_warnings:
            response_lines.append(f"- {w}")
    if implication_warnings:
        response_lines.append("\n**Potentially stale implications:**")
        for w in implication_warnings:
            response_lines.append(f"- {w}")
    if anticipation_warnings:
        response_lines.append("\n**Anticipations re-evaluated:**")
        for w in anticipation_warnings:
            response_lines.append(f"- {w}")
    if bottleneck_cascade_warnings:
        response_lines.append("\n**Dependent bottlenecks flagged for review:**")
        for w in bottleneck_cascade_warnings:
            response_lines.append(f"- {w}")
    if verdict == "ambiguous_flagged":
        response_lines.append("\nFlagged for future review when more evidence arrives.")

    return "\n".join(response_lines)


# ---------------------------------------------------------------------------
# Belief challenge
# ---------------------------------------------------------------------------

_BELIEF_CHALLENGE_PROMPT = """\
You are {mode_description} for a personal AI knowledge engine.

## Belief Under Challenge
**Claim:** {claim}
**Confidence:** {confidence}
**Type:** {belief_type}
**Theme:** {theme_name}

## Evidence For
{evidence_for_text}

## Evidence Against
{evidence_against_text}

## Landscape Context
{landscape_text}

## Library Evidence (claims that may contradict this belief)
{search_evidence_text}

## Instructions

{mode_instructions}

Write a substantive narrative, then output a JSON block:

```json
{{
  "counter_arguments": ["argument 1", "argument 2"],
  "weakest_foundations": ["weakness 1", "weakness 2"],
  "supporting_evidence_from_library": ["claim/source references that support the belief"],
  "contradicting_evidence_from_library": ["claim/source references that contradict"],
  "suggested_confidence": 0.0-1.0,
  "confidence_direction": "up|down|unchanged",
  "reasoning": "Why confidence should change (or not)"
}}
```

Be honest. If the belief is well-grounded, say so. Don't manufacture objections.
"""

_SELF_CHALLENGE_INSTRUCTIONS = """\
### Self-Challenge Mode

1. Identify the logical foundations of this belief
2. Search for contradicting evidence in the library claims above
3. Check if any supporting evidence has been weakened by newer sources
4. Identify implicit assumptions that may not hold
5. Assess whether the belief's confidence level is justified by the evidence balance
6. Present the counter-case clearly but fairly
"""

_STEELMAN_INSTRUCTIONS = """\
### Steelman Mode

Construct the STRONGEST possible case AGAINST this belief:

1. Find the best evidence against it from the library
2. Build the most compelling theoretical argument against it
3. What would need to be true for this belief to be wrong?
4. Who in the AI field would disagree, and what is their strongest argument?
5. Are there historical precedents where similar beliefs were overturned?

Present this as a devil's advocate case — rigorous but not a verdict.
Make it genuinely challenging, not a strawman.
"""


def _handle_belief_challenge(
    belief_id: str, steelman: bool, executor, on_progress, log
) -> str:
    """Self-challenge or steelman a tracked belief."""
    from reading_app.db import (
        get_conn, get_belief, insert_challenge_log,
        update_belief_confidence,
    )
    from retrieval.hybrid import hybrid_retrieve
    from retrieval.landscape import get_theme_state

    if not belief_id:
        return (
            "Usage:\n"
            "- `/challenge belief <belief_id>` — self-challenge\n"
            "- `/challenge belief <belief_id> steelman` — steelman mode"
        )

    if on_progress:
        on_progress(f"Loading belief `{belief_id}`...")

    belief = get_belief(belief_id)
    if not belief:
        return f"Belief not found: `{belief_id}`"

    claim = belief.get("claim", "")
    confidence = belief.get("confidence", 0.5)
    belief_type = belief.get("belief_type", "factual")
    theme_id = belief.get("domain_theme_id")

    # Evidence for/against — keep all items, sentence-truncate each claim
    ev_for = belief.get("evidence_for") or []
    if isinstance(ev_for, str):
        ev_for = json.loads(ev_for)
    ev_against = belief.get("evidence_against") or []
    if isinstance(ev_against, str):
        ev_against = json.loads(ev_against)

    evidence_for_text = "\n".join(
        f"- {truncate_sentences(e.get('claim_text', str(e)), 250)}" for e in ev_for
    ) if ev_for else "(no evidence for)"

    evidence_against_text = "\n".join(
        f"- {truncate_sentences(e.get('claim_text', str(e)), 250)}" for e in ev_against
    ) if ev_against else "(no evidence against)"

    # Theme context — full descriptions, let budget_context allocate space
    theme_name = "Unlinked"
    landscape_text = "(no landscape context)"
    if theme_id:
        try:
            state = get_theme_state(theme_id)
            theme_data = state.get("theme")
            if theme_data:
                theme_name = theme_data.get("name", theme_id)
                parts = []
                for cap in state.get("capabilities", [])[:3]:
                    parts.append(f"- Cap: {cap['description']} ({cap.get('maturity', '?')})")
                for lim in state.get("limitations", [])[:3]:
                    parts.append(f"- Lim: {lim['description']} ({lim.get('severity', '?')})")
                for bn in state.get("bottlenecks", [])[:2]:
                    parts.append(f"- BN: {bn['description']} ({bn.get('resolution_horizon', '?')})")
                landscape_text = "\n".join(parts) if parts else "(empty landscape)"
        except Exception as e:
            log.debug("challenge_landscape_load_failed", error=str(e)[:100])

    # Library evidence search — search for contradicting evidence
    if on_progress:
        on_progress("Searching for counter-evidence...")

    search_evidence_text = "(no library evidence found)"
    try:
        # Search for evidence that might contradict
        contra_query = f"NOT {claim}" if len(claim) < 100 else claim
        results = hybrid_retrieve(contra_query, get_conn, k=10)
        if results:
            search_evidence_text = "\n".join(
                f"- [{r.get('source_id', '?')}] {truncate_sentences((r.get('claim_text') or ''), 250)} "
                f"(score: {r.get('rrf_score', 0):.3f})"
                for r in results
            )
    except Exception as e:
        log.warning("challenge_evidence_search_failed", error=str(e)[:200])

    # Priority-based context budgeting across all context sections
    _context_sections = [
        (10, "evidence_for",     evidence_for_text),
        (10, "evidence_against", evidence_against_text),
        (9,  "search_evidence",  search_evidence_text),
        (5,  "landscape",        landscape_text),
    ]
    _allocated = _budget_sections(_context_sections, 6000)
    evidence_for_text = _allocated.get("evidence_for", evidence_for_text)
    evidence_against_text = _allocated.get("evidence_against", evidence_against_text)
    search_evidence_text = _allocated.get("search_evidence", search_evidence_text)
    landscape_text = _allocated.get("landscape", landscape_text)

    # LLM analysis
    mode = "steelman" if steelman else "self-challenge"
    if on_progress:
        on_progress(f"Running {mode} analysis...")

    prompt = _BELIEF_CHALLENGE_PROMPT.format(
        mode_description="constructing the strongest possible counter-case (steelman)"
        if steelman else "conducting a self-challenge review",
        claim=claim,
        confidence=confidence,
        belief_type=belief_type,
        theme_name=theme_name,
        evidence_for_text=evidence_for_text,
        evidence_against_text=evidence_against_text,
        landscape_text=landscape_text,
        search_evidence_text=search_evidence_text,
        mode_instructions=_STEELMAN_INSTRUCTIONS if steelman else _SELF_CHALLENGE_INSTRUCTIONS,
    )

    try:
        result = executor.run_raw(
            prompt,
            session_id="challenge_belief",
            timeout=300,
        )
        llm_text = result.text
    except Exception as e:
        log.error("challenge_llm_failed", error=str(e)[:200])
        return f"Belief challenge failed: {str(e)[:200]}"

    parsed = _parse_json(llm_text)
    direction = parsed.get("confidence_direction", "unchanged")
    suggested_conf = parsed.get("suggested_confidence", confidence)

    # Persist challenge log
    challenge_id = f"chal_{ULID()}"
    try:
        insert_challenge_log(
            id=challenge_id,
            entity_type="belief",
            entity_id=belief_id,
            system_position=f"Confidence: {confidence}, Type: {belief_type}",
            system_evidence=[e.get("claim_text", str(e))[:100] for e in ev_for[:5]],
            outcome=f"confidence_{direction}",
            resolution_reasoning=parsed.get("reasoning"),
            changes_made=[f"confidence: {confidence} → {suggested_conf}"] if direction != "unchanged" else None,
            belief_id=belief_id,
        )
    except Exception as e:
        log.warning("challenge_log_insert_failed", error=str(e)[:200])

    # Build response
    mode_label = "Steelman Counter-Case" if steelman else "Self-Challenge"
    response_lines = [
        f"**{mode_label}: \"{claim}\"**",
        f"Current confidence: {confidence:.2f}",
        "",
        llm_text,
        "\n---\n",
        f"Challenge log: `{challenge_id}`",
    ]

    if direction != "unchanged":
        direction_icon = "↑" if direction == "up" else "↓"
        # Auto-apply confidence change
        try:
            update_belief_confidence(
                belief_id,
                suggested_conf,
                trigger=f"{mode} challenge",
                trigger_type="challenge",
            )
            response_lines.append(
                f"\n**Confidence updated:** {confidence:.2f} {direction_icon} {suggested_conf:.2f}"
            )
            log.info(
                "belief_confidence_updated",
                belief_id=belief_id,
                old=confidence,
                new=suggested_conf,
                direction=direction,
            )
        except Exception as e:
            log.warning("belief_confidence_update_failed", error=str(e)[:200])
            response_lines.append(
                f"\n**Suggested confidence change:** {confidence:.2f} {direction_icon} {suggested_conf:.2f}"
            )
            response_lines.append(
                f"\nAuto-update failed. To apply manually: "
                f"`/beliefs update {belief_id} {suggested_conf} {mode} challenge`"
            )

        # Check for linked beliefs that reference the same theme
        _flag_linked_beliefs(belief_id, belief, direction, log)
    else:
        response_lines.append("\n**Verdict:** Confidence unchanged — belief appears well-grounded.")

    return "\n".join(response_lines)


# ---------------------------------------------------------------------------
# Linked belief flagging
# ---------------------------------------------------------------------------

def _flag_linked_beliefs(
    entity_id: str,
    entity: dict,
    direction: str,
    log,
) -> list[str]:
    """Check if any active beliefs reference the entity's theme and flag them.

    Returns list of warning strings for response.
    """
    from reading_app.db import get_beliefs_for_theme
    theme_id = entity.get("domain_theme_id") or entity.get("theme_id")
    if not theme_id:
        return []

    try:
        linked = get_beliefs_for_theme(theme_id)
        if not linked:
            return []
        warnings = []
        for b in linked:
            if b["id"] == entity_id:
                continue
            warnings.append(
                f"Belief `{b['id']}` (\"{b['claim'][:60]}…\") shares theme `{theme_id}` — "
                f"consider reviewing"
            )
            log.info("linked_belief_flagged", belief_id=b["id"], theme_id=theme_id)
        return warnings
    except Exception as e:
        log.debug("linked_belief_check_failed", error=str(e)[:100])
        return []


def _check_stale_implications(
    entity_type: str,
    entity_id: str,
    entity: dict,
    log,
) -> list[str]:
    """After a landscape entity is updated, check if any cross_theme_implications
    reference its theme and may be stale."""
    from reading_app.db import get_conn

    theme_id = entity.get("theme_id")
    if not theme_id:
        return []

    try:
        with get_conn() as conn:
            # Find implications where this entity's theme is source or target
            impls = conn.execute(
                """SELECT cti.id, cti.implication, cti.confidence,
                      ts.name AS source_theme, tt.name AS target_theme,
                      cti.created_at
                   FROM cross_theme_implications cti
                   JOIN themes ts ON cti.source_theme_id = ts.id
                   JOIN themes tt ON cti.target_theme_id = tt.id
                   WHERE (cti.source_theme_id = %s OR cti.target_theme_id = %s)
                   ORDER BY cti.confidence DESC
                   LIMIT 10""",
                (theme_id, theme_id),
            ).fetchall()

        if not impls:
            return []

        warnings = []
        for imp in impls:
            warnings.append(
                f"Implication `{imp['id']}` ({imp['source_theme']} → {imp['target_theme']}): "
                f"\"{(imp.get('implication') or '')[:60]}…\" — "
                f"may be stale after {entity_type} change"
            )
            log.info(
                "stale_implication_flagged",
                implication_id=imp["id"],
                entity_type=entity_type,
                entity_id=entity_id,
            )

        return warnings[:5]  # Cap at 5 to avoid overwhelming output
    except Exception as e:
        log.debug("stale_implication_check_failed", error=str(e)[:100])
        return []


def _check_beliefs_for_landscape_entity(
    entity_type: str,
    entity_id: str,
    entity: dict,
    changes: dict,
    log,
) -> list[str]:
    """After a landscape entity is updated, check if any beliefs reference its theme."""
    from reading_app.db import get_beliefs_for_theme
    theme_id = entity.get("theme_id")
    if not theme_id:
        return []

    try:
        linked = get_beliefs_for_theme(theme_id)
        if not linked:
            return []
        warnings = []
        for b in linked:
            warnings.append(
                f"Belief `{b['id']}` (\"{b['claim'][:60]}…\") references theme — "
                f"may need review after {entity_type} change"
            )
            log.info(
                "landscape_challenge_belief_flagged",
                belief_id=b["id"],
                entity_type=entity_type,
                entity_id=entity_id,
            )
        return warnings
    except Exception as e:
        log.debug("landscape_belief_check_failed", error=str(e)[:100])
        return []


# ---------------------------------------------------------------------------
# Challenge cascade: anticipations
# ---------------------------------------------------------------------------

def _cascade_to_anticipations(
    entity_type: str,
    entity_id: str,
    entity: dict,
    changes: dict,
    log,
) -> list[str]:
    """After a landscape entity changes, find and flag anticipations in the same theme."""
    from reading_app.db import get_conn, insert_landscape_history

    theme_id = entity.get("theme_id")
    if not theme_id:
        return []

    try:
        with get_conn() as conn:
            anticipations = conn.execute(
                """SELECT id, prediction, confidence, timeline, status
                   FROM anticipations
                   WHERE theme_id = %s AND status = 'open'
                   ORDER BY confidence DESC
                   LIMIT 10""",
                (theme_id,),
            ).fetchall()

        if not anticipations:
            return []

        warnings = []
        # Determine what changed (particularly resolution_horizon or confidence)
        changed_fields = ", ".join(f"{k}={v}" for k, v in changes.items())

        for ant in anticipations:
            # Log the cascade event
            try:
                insert_landscape_history(
                    entity_type="anticipation",
                    entity_id=ant["id"],
                    field="cascade_review",
                    old_value=None,
                    new_value=f"Triggered by {entity_type} {entity_id} change: {changed_fields[:200]}",
                    attribution="challenge_cascade",
                )
            except Exception:
                pass

            warnings.append(
                f"Anticipation `{ant['id']}` (\"{ant['prediction'][:60]}…\", "
                f"conf: {ant.get('confidence', '?')}) — may need re-evaluation "
                f"after {entity_type} {changed_fields[:80]}"
            )
            log.info(
                "challenge_cascade_anticipation",
                anticipation_id=ant["id"],
                entity_type=entity_type,
                entity_id=entity_id,
            )

        return warnings[:5]
    except Exception as e:
        log.debug("cascade_anticipation_failed", error=str(e)[:100])
        return []


# ---------------------------------------------------------------------------
# Challenge cascade: dependent bottlenecks
# ---------------------------------------------------------------------------

def _cascade_to_dependent_bottlenecks(
    bottleneck_id: str,
    entity: dict,
    changes: dict,
    log,
) -> list[str]:
    """If a bottleneck's horizon or confidence shifted, flag related bottlenecks."""
    from reading_app.db import get_conn, insert_landscape_history

    # Only cascade if resolution_horizon or confidence changed
    if not any(k in changes for k in ("resolution_horizon", "confidence")):
        return []

    theme_id = entity.get("theme_id")
    description = entity.get("description", "")
    if not theme_id:
        return []

    try:
        with get_conn() as conn:
            # Find other bottlenecks in the same theme (potential dependents)
            related = conn.execute(
                """SELECT id, description, resolution_horizon, confidence,
                          blocking_what
                   FROM bottlenecks
                   WHERE theme_id = %s AND id != %s
                   ORDER BY confidence DESC
                   LIMIT 10""",
                (theme_id, bottleneck_id),
            ).fetchall()

        if not related:
            return []

        warnings = []
        changed_fields = ", ".join(f"{k}={v}" for k, v in changes.items())

        for bn in related:
            # Log cascade review
            try:
                insert_landscape_history(
                    entity_type="bottleneck",
                    entity_id=bn["id"],
                    field="cascade_review",
                    old_value=None,
                    new_value=(
                        f"Related bottleneck {bottleneck_id} changed: {changed_fields[:200]}. "
                        f"Review whether this affects dependent bottleneck."
                    ),
                    attribution="challenge_cascade",
                )
            except Exception:
                pass

            warnings.append(
                f"Bottleneck `{bn['id']}` (\"{bn['description'][:60]}…\", "
                f"horizon: {bn.get('resolution_horizon', '?')}) — review for cascade effect"
            )
            log.info(
                "challenge_cascade_bottleneck",
                dependent_id=bn["id"],
                trigger_id=bottleneck_id,
            )

        return warnings[:5]
    except Exception as e:
        log.debug("cascade_bottleneck_failed", error=str(e)[:100])
        return []


# ---------------------------------------------------------------------------
# JSON parsing
# ---------------------------------------------------------------------------

def _parse_json(text: str) -> dict:
    """Extract JSON block from LLM output."""
    result = parse_json_from_llm(text, expect=dict)
    if result is None:
        logger.warning("challenge_no_json_parsed")
        return {}
    return result
