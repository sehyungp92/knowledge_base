"""Direct Python handler for /enrich jobs.

Bypasses the Claude CLI subprocess. Loads the source's current extractions
and landscape data, presents a summary, delegates user enrichment parsing
to executor.run_raw(), and persists structured updates to landscape tables
with attribution='user_enrichment'.
"""

from __future__ import annotations

import json
import re
import time

from ingest.json_parser import parse_json_from_llm
from pathlib import Path
from typing import Callable

import structlog
from ulid import ULID

from gateway.models import Event, Job

logger = structlog.get_logger(__name__)

_ULID_RE = re.compile(r"[0-9A-Z]{26}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def handle_enrich_job(
    event: Event,
    job: Job,
    config,
    executor,
    *,
    on_progress: Callable[[str], None] | None = None,
) -> str:
    """Run /enrich directly."""
    text = event.payload.get("text", "")
    log = logger.bind(job_id=job.id)
    log.info("enrich_handler_start")
    t0 = time.monotonic()

    from reading_app.db import ensure_pool
    ensure_pool()

    source_id, user_input = _parse_command(text)
    if not source_id:
        return (
            "Usage: `/enrich <source_id> [your enrichment]`\n\n"
            "Provide a source ID (ULID) to review and enrich its extractions."
        )

    log = log.bind(source_id=source_id)

    # Load source
    from reading_app.db import get_source
    source = get_source(source_id)
    if not source:
        return f"Source not found: `{source_id}`"

    library_path = Path(config.library_path)
    source_dir = library_path / source_id
    title = source.get("title", source_id)

    if on_progress:
        on_progress(f"Loading extractions for **{title}**...")

    # Load current state
    ctx = _load_source_context(source_id, source_dir, log)

    if not user_input:
        # Present-only mode: show current state and prompt for input
        return _format_current_state(title, source_id, ctx)

    # Check for validate subcommand
    validate_lower = user_input.strip().lower()
    if validate_lower in ("validate", "validate limitations"):
        return _handle_validate(source_id, title, ctx, on_progress, log)

    # Handle validate <id> yes/no or validate all yes/no
    validate_match = re.match(
        r"validate\s+(all|\S+)\s+(yes|no|confirm|reject)", validate_lower
    )
    if validate_match:
        return _apply_validation(
            source_id, title, ctx,
            validate_match.group(1),
            validate_match.group(2) in ("yes", "confirm"),
            on_progress, log,
        )

    # User provided enrichment inline — parse and apply
    if on_progress:
        on_progress("Parsing enrichment...")

    return _process_enrichment(
        source_id, title, source_dir, ctx, user_input,
        executor, on_progress, log,
    )


# ---------------------------------------------------------------------------
# Command parser
# ---------------------------------------------------------------------------

def _parse_command(text: str) -> tuple[str | None, str]:
    """Extract source_id and optional user enrichment text."""
    cleaned = text.strip()
    for prefix in ("/enrich ", "/enrich"):
        if cleaned.lower().startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
            break

    m = _ULID_RE.search(cleaned)
    if not m:
        return None, ""

    source_id = m.group(0)
    after = cleaned[m.end():].strip()
    return source_id, after


# ---------------------------------------------------------------------------
# Context loading
# ---------------------------------------------------------------------------

def _load_source_context(source_id: str, source_dir: Path, log) -> dict:
    """Load all current extractions and landscape data for a source."""
    from reading_app.db import get_conn, get_claims_for_source

    ctx = {
        "claims": [],
        "capabilities": [],
        "limitations": [],
        "bottlenecks": [],
        "breakthroughs": [],
        "themes": [],
        "implications": [],
        "landscape_json": {},
    }

    # Claims
    try:
        ctx["claims"] = get_claims_for_source(source_id)
    except Exception as e:
        log.debug("enrich_claims_load_failed", error=str(e)[:100])

    # Landscape entities linked to this source
    with get_conn() as conn:
        try:
            ctx["capabilities"] = conn.execute(
                """SELECT c.*, t.name AS theme_name FROM capabilities c
                   LEFT JOIN themes t ON c.theme_id = t.id
                   WHERE c.evidence_sources::text LIKE %s""",
                (f"%{source_id}%",),
            ).fetchall()
        except Exception:
            pass

        try:
            ctx["limitations"] = conn.execute(
                """SELECT l.*, t.name AS theme_name FROM limitations l
                   LEFT JOIN themes t ON l.theme_id = t.id
                   WHERE l.evidence_sources::text LIKE %s""",
                (f"%{source_id}%",),
            ).fetchall()
        except Exception:
            pass

        try:
            ctx["bottlenecks"] = conn.execute(
                """SELECT b.*, t.name AS theme_name FROM bottlenecks b
                   LEFT JOIN themes t ON b.theme_id = t.id
                   WHERE b.evidence_sources::text LIKE %s""",
                (f"%{source_id}%",),
            ).fetchall()
        except Exception:
            pass

        try:
            ctx["breakthroughs"] = conn.execute(
                """SELECT b.*, t.name AS theme_name FROM breakthroughs b
                   LEFT JOIN themes t ON b.theme_id = t.id
                   WHERE b.primary_source_id = %s
                      OR b.corroborating_sources::text LIKE %s""",
                (source_id, f"%{source_id}%"),
            ).fetchall()
        except Exception:
            pass

        try:
            ctx["themes"] = conn.execute(
                """SELECT t.id, t.name, st.relevance FROM source_themes st
                   JOIN themes t ON st.theme_id = t.id
                   WHERE st.source_id = %s ORDER BY st.relevance DESC""",
                (source_id,),
            ).fetchall()
        except Exception:
            pass

        try:
            ctx["implications"] = conn.execute(
                """SELECT cti.*, ts.name AS source_theme, tt.name AS target_theme
                   FROM cross_theme_implications cti
                   JOIN themes ts ON cti.source_theme_id = ts.id
                   JOIN themes tt ON cti.target_theme_id = tt.id
                   WHERE cti.evidence_sources::text LIKE %s""",
                (f"%{source_id}%",),
            ).fetchall()
        except Exception:
            pass

    # landscape.json file
    landscape_path = source_dir / "landscape.json"
    if landscape_path.is_file():
        try:
            ctx["landscape_json"] = json.loads(landscape_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    return ctx


# ---------------------------------------------------------------------------
# Present current state (no enrichment input)
# ---------------------------------------------------------------------------

def _format_current_state(title: str, source_id: str, ctx: dict) -> str:
    """Format current extractions for user review."""
    lines = [f"**{title}** — Current Extractions\n"]

    # Capabilities
    caps = ctx["capabilities"]
    lines.append(f"**Capabilities:** {len(caps)} extracted")
    for c in caps[:8]:
        lines.append(f"- {c['description']} (maturity: {c.get('maturity', '?')})")

    # Limitations
    lims = ctx["limitations"]
    implicit_count = sum(
        1 for l in lims
        if (l.get("signal_type") or "").startswith("implicit")
    )
    unvalidated = sum(
        1 for l in lims
        if (l.get("signal_type") or "").startswith("implicit") and l.get("validated") is None
    )
    lines.append(f"\n**Limitations:** {len(lims)} ({implicit_count} implicit, {unvalidated} unvalidated)")
    for l in lims[:8]:
        validated_mark = ""
        if l.get("validated") is True:
            validated_mark = " ✓"
        elif l.get("validated") is False:
            validated_mark = " ✗"
        elif (l.get("signal_type") or "").startswith("implicit"):
            validated_mark = " ?"
        lines.append(
            f"- {l['description']} "
            f"(type: {l.get('limitation_type', '?')}, severity: {l.get('severity', '?')}{validated_mark})"
        )

    # Bottlenecks
    bns = ctx["bottlenecks"]
    lines.append(f"\n**Bottlenecks linked:** {len(bns)}")
    for b in bns[:5]:
        lines.append(f"- {b['description']} (horizon: {b.get('resolution_horizon', '?')})")

    # Themes
    themes = ctx["themes"]
    theme_list = ", ".join(f"{t['name']} ({t.get('relevance', '?')})" for t in themes)
    lines.append(f"\n**Themes assigned:** {theme_list or 'none'}")

    # Implications
    impls = ctx["implications"]
    lines.append(f"\n**Cross-theme implications:** {len(impls)}")
    for i in impls[:5]:
        lines.append(f"- {i.get('source_theme', '?')} → {i.get('target_theme', '?')}: {(i.get('implication') or '')[:100]}")

    # Items needing attention
    attention = []
    if unvalidated > 0:
        attention.append(f"- {unvalidated} implicit limitations have not been validated")
    low_conf_caps = [c for c in caps if (c.get("confidence") or 1) < 0.5]
    if low_conf_caps:
        attention.append(f"- {len(low_conf_caps)} capabilities have low confidence (<0.5)")
    if not bns and len(ctx["claims"]) > 5:
        attention.append("- No bottlenecks linked despite having substantial claims")

    if attention:
        lines.append("\n**Items needing attention:**")
        lines.extend(attention)

    lines.append(
        f"\n---\n"
        f"Reply with your enrichment, e.g.:\n"
        f"- `/enrich {source_id} add capability: <description>`\n"
        f"- `/enrich {source_id} add limitation: <description>`\n"
        f"- `/enrich {source_id} add implication: <source theme> -> <target theme>: <description>`\n"
        f"- `/enrich {source_id} validate limitations` — batch validate implicit signals\n"
        f"- Or just describe what the system missed in plain text"
    )

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Guided limitation validation
# ---------------------------------------------------------------------------

def _handle_validate(source_id: str, title: str, ctx: dict, on_progress, log) -> str:
    """Walk user through unvalidated implicit limitations for this source."""
    from reading_app.db import get_conn

    lims = ctx.get("limitations", [])
    unvalidated = [
        l for l in lims
        if (l.get("signal_type") or "").startswith("implicit")
        and l.get("validated") is None
    ]

    if not unvalidated:
        return (
            f"**{title}** — No unvalidated implicit limitations.\n\n"
            f"All {len(lims)} limitations have been reviewed."
        )

    if on_progress:
        on_progress(f"Found {len(unvalidated)} unvalidated limitations...")

    lines = [
        f"**{title}** — Limitation Validation ({len(unvalidated)} pending)\n",
        "Review each implicit limitation below. Reply with one of:\n"
        "- `/enrich {source_id} validate <id> yes` — confirm this limitation\n"
        "- `/enrich {source_id} validate <id> no` — reject this limitation\n\n"
        "Or validate in bulk:\n"
        "- `/enrich {source_id} validate all yes` — confirm all\n"
        "- `/enrich {source_id} validate all no` — reject all\n",
    ]

    for i, l in enumerate(unvalidated, 1):
        signal_type = l.get("signal_type", "implicit")
        evidence = ""
        ev_sources = l.get("evidence_sources")
        if isinstance(ev_sources, list) and ev_sources:
            evidence = f"\n  Evidence sources: {', '.join(str(e) for e in ev_sources[:3])}"

        lines.append(
            f"### {i}. `{l['id']}`\n"
            f"**Description:** {l['description']}\n"
            f"**Type:** {l.get('limitation_type', '?')} | "
            f"**Signal:** {signal_type} | "
            f"**Severity:** {l.get('severity', '?')} | "
            f"**Trajectory:** {l.get('trajectory', '?')}"
            f"{evidence}\n"
        )

    return "\n".join(lines)


def _apply_validation(
    source_id: str, title: str, ctx: dict,
    target: str, validated: bool,
    on_progress, log,
) -> str:
    """Apply validation to a specific limitation or all unvalidated ones."""
    from reading_app.db import get_conn

    lims = ctx.get("limitations", [])
    unvalidated = [
        l for l in lims
        if (l.get("signal_type") or "").startswith("implicit")
        and l.get("validated") is None
    ]

    if target == "all":
        targets = unvalidated
    else:
        targets = [l for l in unvalidated if l["id"] == target]
        if not targets:
            # Try partial match
            targets = [l for l in unvalidated if target in l["id"]]

    if not targets:
        return f"No matching unvalidated limitation found for `{target}`."

    action = "confirmed" if validated else "rejected"
    updated = 0

    with get_conn() as conn:
        for l in targets:
            try:
                conn.execute(
                    "UPDATE limitations SET validated = %s, validated_at = NOW() WHERE id = %s",
                    (validated, l["id"]),
                )
                updated += 1
                log.info("enrich_validation_applied", lim_id=l["id"], validated=validated)
            except Exception as e:
                log.warning("enrich_validation_failed", lim_id=l["id"], error=str(e)[:200])
        conn.commit()

    remaining = len(unvalidated) - updated
    lines = [
        f"**{title}** — Validated {updated} limitation(s) as **{action}**\n",
    ]
    for l in targets:
        lines.append(f"- `{l['id']}`: {l['description'][:100]} → {action}")

    if remaining > 0:
        lines.append(f"\n{remaining} limitations still unvalidated.")
        lines.append(f"Run `/enrich {source_id} validate` to see remaining.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Process enrichment
# ---------------------------------------------------------------------------

_PARSE_ENRICHMENT_PROMPT = """\
You are parsing a user's enrichment input for a source in an AI knowledge engine.
The user wants to correct, supplement, or reinterpret what was extracted from this source.

## Source Context
Title: {title}
Source ID: {source_id}

### Current Capabilities
{capabilities_text}

### Current Limitations
{limitations_text}

### Current Themes
{themes_text}

## Available Themes (for new entries)
{all_themes_text}

## User's Enrichment Input
{user_input}

## Instructions

Parse the user's input into structured updates. Be precise — only extract what the user
explicitly stated or clearly implied. Do NOT invent entries.

Output a JSON block:

```json
{{
  "new_capabilities": [
    {{
      "description": "...",
      "theme_id": "<exact theme ID from list above or null>",
      "maturity": "research_only|early_deployment|production|widespread|commodity",
      "confidence": 0.0-1.0
    }}
  ],
  "new_limitations": [
    {{
      "description": "...",
      "theme_id": "<exact theme ID or null>",
      "limitation_type": "technical|scalability|data|cost|safety|robustness|generalization",
      "severity": "minor|moderate|major|critical",
      "trajectory": "improving|stable|worsening|unknown"
    }}
  ],
  "new_bottlenecks": [
    {{
      "description": "...",
      "theme_id": "<exact theme ID or null>",
      "blocking_what": "...",
      "bottleneck_type": "technical|data|compute|regulatory|theoretical",
      "resolution_horizon": "months|1-2_years|3-5_years|5+_years|possibly_fundamental"
    }}
  ],
  "new_implications": [
    {{
      "source_theme_id": "<exact theme ID>",
      "target_theme_id": "<exact theme ID>",
      "trigger_type": "breakthrough|bottleneck_resolved|capability_matured|convergence|analogy",
      "implication": "...",
      "confidence": 0.0-1.0
    }}
  ],
  "reclassifications": [
    {{
      "entity_id": "<id of existing entity>",
      "entity_type": "capability|limitation|bottleneck",
      "field": "<field name>",
      "old_value": "...",
      "new_value": "..."
    }}
  ],
  "limitation_validations": [
    {{
      "limitation_id": "<id>",
      "validated": true
    }}
  ],
  "theme_corrections": [
    {{
      "action": "add|remove",
      "theme_id": "<theme ID>",
      "relevance": 0.0-1.0
    }}
  ],
  "summary": "Brief description of what the user wants to change"
}}
```

Only include non-empty arrays. If you cannot parse anything meaningful, return {{"summary": "Could not parse enrichment input"}}.
"""


def _process_enrichment(
    source_id: str,
    title: str,
    source_dir: Path,
    ctx: dict,
    user_input: str,
    executor,
    on_progress,
    log,
) -> str:
    """Parse user enrichment via LLM and persist to DB."""
    from reading_app.db import (
        get_conn, get_themes_by_level,
        insert_capability, insert_limitation, insert_bottleneck,
        insert_cross_theme_implication, insert_landscape_history,
        insert_source_theme,
    )

    # Build context for LLM
    capabilities_text = "\n".join(
        f"- [{c['id']}] {c['description']} (maturity: {c.get('maturity', '?')})"
        for c in ctx["capabilities"][:10]
    ) or "(none)"

    limitations_text = "\n".join(
        f"- [{l['id']}] {l['description']} (type: {l.get('limitation_type', '?')}, "
        f"signal: {l.get('signal_type', '?')}, validated: {l.get('validated', '?')})"
        for l in ctx["limitations"][:10]
    ) or "(none)"

    themes_text = "\n".join(
        f"- `{t['id']}`: {t['name']} (relevance: {t.get('relevance', '?')})"
        for t in ctx["themes"]
    ) or "(none)"

    # All available themes for new entries
    all_themes = get_themes_by_level(0) + get_themes_by_level(1)
    all_themes_text = "\n".join(
        f"- `{t['id']}`: {t['name']}"
        for t in all_themes
    ) or "(no themes in database)"

    valid_theme_ids = {t["id"] for t in all_themes}

    prompt = _PARSE_ENRICHMENT_PROMPT.format(
        title=title,
        source_id=source_id,
        capabilities_text=capabilities_text,
        limitations_text=limitations_text,
        themes_text=themes_text,
        all_themes_text=all_themes_text,
        user_input=user_input,
    )

    try:
        result = executor.run_raw(
            prompt,
            session_id="enrich_parse",
            timeout=120,
        )
        parsed = _parse_json(result.text)
    except Exception as e:
        log.error("enrich_parse_failed", error=str(e)[:200])
        return f"Failed to parse enrichment: {str(e)[:200]}"

    if not parsed or parsed.get("summary", "").startswith("Could not parse"):
        return f"Could not parse enrichment input. Try being more specific, e.g.:\n- `add capability: <description>`\n- `add limitation: <description>`"

    if on_progress:
        on_progress("Applying enrichment...")

    # Apply all updates
    summary = _apply_enrichment(
        source_id, source_dir, ctx, parsed, user_input,
        valid_theme_ids, log,
    )

    elapsed_note = parsed.get("summary", "")
    response_lines = [f"**Enrichment applied to \"{title}\"**\n"]

    # Changes applied
    response_lines.append("**Changes applied:**")
    if summary["capabilities"]:
        response_lines.append(f"- Added {summary['capabilities']} capabilities")
    if summary["limitations"]:
        response_lines.append(f"- Added {summary['limitations']} limitations")
    if summary["bottlenecks"]:
        response_lines.append(f"- Added {summary['bottlenecks']} bottlenecks")
    if summary["implications"]:
        response_lines.append(f"- Added {summary['implications']} cross-theme implications")
    if summary["reclassifications"]:
        response_lines.append(f"- Applied {summary['reclassifications']} reclassifications")
    if summary["validations"]:
        response_lines.append(f"- Validated {summary['validations']} limitations")
    if summary["theme_corrections"]:
        response_lines.append(f"- {summary['theme_corrections']} theme corrections")
    if summary["errors"]:
        response_lines.append(f"- {summary['errors']} errors (check logs)")

    # Show details of each change
    if summary["details"]:
        response_lines.append("\n**Details:**")
        for d in summary["details"]:
            response_lines.append(d)

    if not any(v for k, v in summary.items() if k not in ("errors", "downstream", "details")):
        response_lines.append("- (no changes)")

    # Downstream effects
    if summary["downstream"]:
        response_lines.append("\n**Downstream effects flagged:**")
        for d in summary["downstream"]:
            response_lines.append(f"- {d}")

    response_lines.append(f"\n**Attribution:** All changes recorded as `user_enrichment`")

    return "\n".join(response_lines)


# ---------------------------------------------------------------------------
# Apply parsed enrichment to DB
# ---------------------------------------------------------------------------

def _apply_enrichment(
    source_id: str,
    source_dir: Path,
    ctx: dict,
    parsed: dict,
    user_input: str,
    valid_theme_ids: set,
    log,
) -> dict:
    """Apply parsed enrichment entries to the database."""
    from reading_app.db import (
        get_conn, insert_capability, insert_limitation, insert_bottleneck,
        insert_cross_theme_implication, insert_landscape_history,
        insert_source_theme,
    )

    summary = {
        "capabilities": 0, "limitations": 0, "bottlenecks": 0,
        "implications": 0, "reclassifications": 0, "validations": 0,
        "theme_corrections": 0, "errors": 0, "downstream": [],
        "details": [],  # human-readable details of each change
    }

    attribution = "user_enrichment"
    attribution_reasoning = user_input[:500]

    # --- New capabilities ---
    for cap in parsed.get("new_capabilities", []):
        try:
            cap_id = f"cap_{ULID()}"
            theme_id = cap.get("theme_id")
            if theme_id and theme_id not in valid_theme_ids:
                theme_id = None
            insert_capability(
                id=cap_id,
                theme_id=theme_id or (ctx["themes"][0]["id"] if ctx["themes"] else ""),
                description=cap["description"],
                maturity=cap.get("maturity"),
                confidence=cap.get("confidence"),
                evidence_sources=[source_id],
                attribution=attribution,
                attributed_reasoning=attribution_reasoning,
            )
            summary["capabilities"] += 1
            summary["details"].append(
                f"  + Capability `{cap_id}`: {cap['description'][:120]} "
                f"(maturity: {cap.get('maturity', '?')})"
            )
            log.info("enrich_capability_added", cap_id=cap_id)
        except Exception as e:
            log.warning("enrich_capability_failed", error=str(e)[:200])
            summary["errors"] += 1

    # --- New limitations ---
    for lim in parsed.get("new_limitations", []):
        try:
            lim_id = f"lim_{ULID()}"
            theme_id = lim.get("theme_id")
            if theme_id and theme_id not in valid_theme_ids:
                theme_id = None
            insert_limitation(
                id=lim_id,
                theme_id=theme_id or (ctx["themes"][0]["id"] if ctx["themes"] else ""),
                description=lim["description"],
                limitation_type=lim.get("limitation_type"),
                signal_type="explicit",  # user-provided = explicit
                severity=lim.get("severity"),
                trajectory=lim.get("trajectory"),
                evidence_sources=[source_id],
                attribution=attribution,
                attributed_reasoning=attribution_reasoning,
            )
            summary["limitations"] += 1
            summary["details"].append(
                f"  + Limitation `{lim_id}`: {lim['description'][:120]} "
                f"(type: {lim.get('limitation_type', '?')}, severity: {lim.get('severity', '?')})"
            )
            log.info("enrich_limitation_added", lim_id=lim_id)
        except Exception as e:
            log.warning("enrich_limitation_failed", error=str(e)[:200])
            summary["errors"] += 1

    # --- New bottlenecks ---
    for bn in parsed.get("new_bottlenecks", []):
        try:
            bn_id = f"bn_{ULID()}"
            theme_id = bn.get("theme_id")
            if theme_id and theme_id not in valid_theme_ids:
                theme_id = None
            insert_bottleneck(
                id=bn_id,
                theme_id=theme_id or (ctx["themes"][0]["id"] if ctx["themes"] else ""),
                description=bn["description"],
                blocking_what=bn.get("blocking_what"),
                bottleneck_type=bn.get("bottleneck_type"),
                resolution_horizon=bn.get("resolution_horizon"),
                evidence_sources=[source_id],
                attribution=attribution,
                attributed_reasoning=attribution_reasoning,
            )
            summary["bottlenecks"] += 1
            summary["details"].append(
                f"  + Bottleneck `{bn_id}`: {bn['description'][:120]} "
                f"(blocking: {bn.get('blocking_what', '?')[:60]}, "
                f"horizon: {bn.get('resolution_horizon', '?')})"
            )
            log.info("enrich_bottleneck_added", bn_id=bn_id)
        except Exception as e:
            log.warning("enrich_bottleneck_failed", error=str(e)[:200])
            summary["errors"] += 1

    # --- New cross-theme implications ---
    for imp in parsed.get("new_implications", []):
        src_tid = imp.get("source_theme_id", "")
        tgt_tid = imp.get("target_theme_id", "")
        if src_tid not in valid_theme_ids or tgt_tid not in valid_theme_ids:
            log.info("enrich_skip_invalid_theme", src=src_tid, tgt=tgt_tid)
            continue
        try:
            impl_id = f"impl_{ULID()}"
            insert_cross_theme_implication(
                id=impl_id,
                source_theme_id=src_tid,
                target_theme_id=tgt_tid,
                trigger_type=imp.get("trigger_type", "convergence"),
                trigger_id=source_id,
                implication=imp["implication"],
                confidence=imp.get("confidence"),
                evidence_sources=[source_id],
                attribution=attribution,
                attributed_reasoning=attribution_reasoning,
            )
            summary["implications"] += 1
            summary["details"].append(
                f"  + Implication `{impl_id}`: {src_tid} → {tgt_tid}: "
                f"{imp['implication'][:100]}"
            )
            log.info("enrich_implication_added", impl_id=impl_id)
        except Exception as e:
            log.warning("enrich_implication_failed", error=str(e)[:200])
            summary["errors"] += 1

    # --- Reclassifications ---
    for reclass in parsed.get("reclassifications", []):
        entity_id = reclass.get("entity_id")
        entity_type = reclass.get("entity_type")
        field = reclass.get("field")
        new_value = reclass.get("new_value")
        old_value = reclass.get("old_value", "")

        if not entity_id or not entity_type or not field or new_value is None:
            continue

        table = {
            "capability": "capabilities",
            "limitation": "limitations",
            "bottleneck": "bottlenecks",
        }.get(entity_type)
        if not table:
            continue

        # Whitelist allowed fields to prevent SQL injection
        allowed_fields = {
            "capabilities": {"maturity", "confidence", "description"},
            "limitations": {"limitation_type", "severity", "trajectory", "confidence", "description"},
            "bottlenecks": {"resolution_horizon", "bottleneck_type", "confidence", "description", "blocking_what"},
        }
        if field not in allowed_fields.get(table, set()):
            log.warning("enrich_reclass_blocked_field", field=field, table=table)
            continue

        try:
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
                old_value=str(old_value)[:200],
                new_value=str(new_value)[:200],
                source_id=source_id,
                attribution=attribution,
            )
            summary["reclassifications"] += 1
            summary["details"].append(
                f"  ~ Reclassified {entity_type} `{entity_id}` "
                f"{field}: {str(old_value)[:40]} → {str(new_value)[:40]}"
            )
            log.info("enrich_reclass_applied", entity_id=entity_id, field=field)
        except Exception as e:
            log.warning("enrich_reclass_failed", error=str(e)[:200])
            summary["errors"] += 1

    # --- Limitation validations ---
    for val in parsed.get("limitation_validations", []):
        lim_id = val.get("limitation_id")
        validated = val.get("validated")
        if not lim_id or validated is None:
            continue
        try:
            with get_conn() as conn:
                conn.execute(
                    "UPDATE limitations SET validated = %s, validated_at = NOW() WHERE id = %s",
                    (bool(validated), lim_id),
                )
                conn.commit()
            summary["validations"] += 1
            mark = "confirmed" if validated else "rejected"
            summary["details"].append(
                f"  ✓ Limitation `{lim_id}` {mark}"
            )
            log.info("enrich_validation_applied", lim_id=lim_id, validated=validated)
        except Exception as e:
            log.warning("enrich_validation_failed", error=str(e)[:200])
            summary["errors"] += 1

    # --- Theme corrections ---
    for tc in parsed.get("theme_corrections", []):
        theme_id = tc.get("theme_id")
        action = tc.get("action")
        if not theme_id or theme_id not in valid_theme_ids:
            continue
        try:
            if action == "add":
                insert_source_theme(source_id, theme_id, relevance=tc.get("relevance", 1.0))
                summary["theme_corrections"] += 1
            elif action == "remove":
                with get_conn() as conn:
                    conn.execute(
                        "DELETE FROM source_themes WHERE source_id = %s AND theme_id = %s",
                        (source_id, theme_id),
                    )
                    conn.commit()
                summary["theme_corrections"] += 1
            log.info("enrich_theme_correction", action=action, theme_id=theme_id)
        except Exception as e:
            log.warning("enrich_theme_correction_failed", error=str(e)[:200])
            summary["errors"] += 1

    # --- Update landscape.json file ---
    _update_landscape_json(source_dir, parsed, log)

    # --- Flag downstream effects ---
    affected_themes = set()
    for cap in parsed.get("new_capabilities", []):
        if cap.get("theme_id"):
            affected_themes.add(cap["theme_id"])
    for lim in parsed.get("new_limitations", []):
        if lim.get("theme_id"):
            affected_themes.add(lim["theme_id"])
    for bn in parsed.get("new_bottlenecks", []):
        if bn.get("theme_id"):
            affected_themes.add(bn["theme_id"])

    for tid in affected_themes:
        summary["downstream"].append(
            f"Theme `{tid}` state_summary may need regeneration "
            f"(run `/landscape {tid}` to refresh)"
        )

    return summary


# ---------------------------------------------------------------------------
# landscape.json updater
# ---------------------------------------------------------------------------

def _update_landscape_json(source_dir: Path, parsed: dict, log) -> None:
    """Append user enrichments to the source's landscape.json."""
    landscape_path = source_dir / "landscape.json"
    try:
        if landscape_path.is_file():
            data = json.loads(landscape_path.read_text(encoding="utf-8"))
        else:
            data = {}

        # Ensure arrays exist
        data.setdefault("capabilities", [])
        data.setdefault("limitations", [])
        data.setdefault("bottlenecks", [])

        for cap in parsed.get("new_capabilities", []):
            data["capabilities"].append({
                **cap, "attribution": "user_enrichment",
            })
        for lim in parsed.get("new_limitations", []):
            data["limitations"].append({
                **lim, "signal_type": "explicit", "attribution": "user_enrichment",
            })
        for bn in parsed.get("new_bottlenecks", []):
            data["bottlenecks"].append({
                **bn, "attribution": "user_enrichment",
            })

        landscape_path.write_text(
            json.dumps(data, indent=2, default=str), encoding="utf-8",
        )
    except Exception as e:
        log.warning("enrich_landscape_json_update_failed", error=str(e)[:200])


# ---------------------------------------------------------------------------
# JSON parsing
# ---------------------------------------------------------------------------

def _parse_json(text: str) -> dict:
    """Extract JSON block from LLM output."""
    result = parse_json_from_llm(text, expect=dict)
    if result is None:
        logger.warning("enrich_no_json_parsed")
        return {}
    return result
