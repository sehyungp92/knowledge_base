"""Anticipation matching against extracted landscape signals.

After landscape extraction during /save, checks whether any extracted signals
confirm, disconfirm, or partially match open anticipations for the source's
themes and connected themes. Matches are appended to anticipation status_evidence.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from ingest.json_parser import parse_json_from_llm

logger = logging.getLogger(__name__)

# ── Thresholds ──────────────────────────────────────────────────────────────
MATCH_CONFIDENCE_FLOOR = 0.5    # Minimum confidence for a match to survive filtering
NOTIFY_CONFIDENCE_FLOOR = 0.7   # Minimum confidence to emit a Telegram notification
AUTO_CONFIRM_EVIDENCE_COUNT = 3 # Minimum evidence items to auto-transition status
AUTO_CONFIRM_AVG_CONFIDENCE = 0.7  # Minimum avg confidence for auto-transition
MATCH_TIMEOUT_SECONDS = 180     # LLM call timeout for matching

MATCH_PROMPT = """You are checking whether newly extracted AI landscape signals match any open predictions (anticipations).

**Source publication date: {published_at}**

## Open Anticipations
{anticipations_text}

## Newly Extracted Signals from Source
{signals_text}

For each anticipation, determine if ANY of the extracted signals provide evidence for or against it.

Pay special attention to the "Would confirm" and "Would invalidate" fields when present — these describe specific evidence patterns the prediction was designed to be tested against. A signal matching these criteria is stronger evidence than a tangential match.

IMPORTANT temporal reasoning:
- Each anticipation has a "created_at" date — when the prediction was made.
- The source publication date is shown above.
- Evidence published BEFORE a prediction was made does NOT confirm it — that information was already available when the prediction was made. It may still be relevant as "partial" context.
- Evidence published AFTER a prediction was made is genuinely new signal and should be weighted accordingly.
- If the source is older than the anticipation, be very conservative about "confirming" matches.

Return a JSON array of matches (empty array if no matches):
```json
[
  {{
    "anticipation_id": "the anticipation ID",
    "match_type": "confirming" | "disconfirming" | "partial",
    "evidence": "the specific signal text that matched",
    "reasoning": "1-2 sentences explaining WHY this signal is relevant to the anticipation. Note whether this is pre-prediction or post-prediction evidence.",
    "confidence": 0.0-1.0
  }}
]
```

Rules:
- Only include genuine matches where the signal meaningfully relates to the prediction
- "confirming" = signal provides evidence the prediction is happening/will happen
- "disconfirming" = signal provides evidence the prediction is wrong/won't happen
- "partial" = signal is tangentially relevant but not conclusive either way
- Set confidence based on how directly the signal addresses the prediction
- Reduce confidence for pre-prediction evidence (source published before the anticipation was created)
- If no signals match any anticipation, return an empty array []
"""


def match_anticipations(
    extracted_signals: dict,
    source_themes: list[str],
    source_id: str,
    published_at: str | None = None,
    executor=None,
) -> list[dict]:
    """Check extracted signals against open anticipations for source themes.

    Args:
        extracted_signals: Dict with capabilities, limitations, breakthroughs lists.
        source_themes: Theme IDs the source was classified under.
        source_id: Source ID for evidence linking.
        published_at: Publication date of the source (ISO-8601 string or None).
        executor: ClaudeExecutor instance.

    Returns:
        List of match dicts with anticipation_id, match_type, evidence, reasoning, confidence.
    """
    if not source_themes:
        return []

    try:
        from reading_app.db import get_open_anticipations_for_themes
        anticipations = get_open_anticipations_for_themes(source_themes)
    except Exception:
        logger.warning("Failed to fetch anticipations for themes %s", source_themes, exc_info=True)
        return []

    if not anticipations:
        logger.debug("No open anticipations for themes %s", source_themes)
        return []

    # Build text representations (include created_at for temporal reasoning)
    ant_lines = []
    for a in anticipations:
        line = (
            f"- ID: {a['id']} | Theme: {a.get('theme_name', a['theme_id'])} | "
            f"Prediction: {a['prediction']} | Confidence: {a.get('confidence', '?')} | "
            f"Timeline: {a.get('timeline', '?')} | "
            f"Created: {str(a.get('created_at', '?'))[:10]}"
        )
        if a.get("would_confirm"):
            line += f"\n  Would confirm: {a['would_confirm']}"
        if a.get("would_invalidate"):
            line += f"\n  Would invalidate: {a['would_invalidate']}"
        ant_lines.append(line)
    anticipations_text = "\n".join(ant_lines)

    signals_parts = []
    for cap in extracted_signals.get("capabilities", []):
        signals_parts.append(f"[Capability] {cap['description']} (maturity: {cap.get('maturity', '?')})")
    for lim in extracted_signals.get("limitations", []):
        signals_parts.append(f"[Limitation] {lim['description']} (type: {lim.get('limitation_type', '?')}, trajectory: {lim.get('trajectory', '?')})")
    for bn in extracted_signals.get("bottlenecks", []):
        signals_parts.append(f"[Bottleneck] {bn['description']} (horizon: {bn.get('resolution_horizon', '?')})")
    for bt in extracted_signals.get("breakthroughs", []):
        signals_parts.append(f"[Breakthrough] {bt['description']} (significance: {bt.get('significance', '?')})")

    # Fallback: use raw claims text when no structured landscape signals exist
    if not signals_parts and extracted_signals.get("claims_text"):
        signals_parts.append(f"[Claims from source]\n{extracted_signals['claims_text']}")

    signals_text = "\n".join(signals_parts)

    if not signals_text.strip():
        return []

    if executor is None:
        from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
        executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    # Resolve published_at if not provided
    if not published_at:
        try:
            from reading_app.db import get_source
            source = get_source(source_id)
            if source and source.get("published_at"):
                published_at = str(source["published_at"])[:10]
        except Exception:
            pass

    prompt = MATCH_PROMPT.format(
        anticipations_text=anticipations_text,
        signals_text=signals_text,
        published_at=published_at or "unknown",
    )

    try:
        result = executor.run_raw(
            prompt,
            session_id=f"anticipation_match_{source_id}",
            timeout=MATCH_TIMEOUT_SECONDS,
        )
        matches = _parse_matches(result.text)
    except Exception:
        logger.warning("LLM anticipation matching failed for %s", source_id, exc_info=True)
        return []

    # Filter low-confidence matches (log what gets dropped for diagnosability)
    valid_ids = {a["id"] for a in anticipations}
    valid_matches = []
    for m in matches:
        conf = m.get("confidence", 0)
        ant_id = m.get("anticipation_id")
        if ant_id not in valid_ids:
            logger.debug("Dropping match with unknown anticipation_id=%s", ant_id)
            continue
        if conf < MATCH_CONFIDENCE_FLOOR:
            logger.info(
                "Filtered sub-threshold match for %s: ant=%s type=%s conf=%.2f evidence=%.60s",
                source_id, ant_id, m.get("match_type"), conf, m.get("evidence", ""),
            )
            continue
        valid_matches.append(m)

    raw_count = len(matches)
    logger.info(
        "Anticipation matching for %s: %d/%d matches survived filtering (%d anticipations checked)",
        source_id, len(valid_matches), raw_count, len(anticipations),
    )
    return valid_matches


def persist_anticipation_matches(
    matches: list[dict],
    source_id: str,
) -> int:
    """Persist anticipation matches to status_evidence.

    Args:
        matches: List of match dicts from match_anticipations().
        source_id: Source ID for attribution.

    Returns:
        Count of successfully persisted matches.
    """
    if not matches:
        return 0

    from reading_app.db import append_anticipation_evidence, get_conn
    persisted = 0
    skipped_dup = 0

    # Pre-fetch existing evidence to guard against duplicate appends
    existing_evidence: dict[str, set[str]] = {}  # ant_id -> {source_ids already matched}
    try:
        ant_ids = {m["anticipation_id"] for m in matches if m.get("anticipation_id")}
        if ant_ids:
            with get_conn() as conn:
                for ant_id in ant_ids:
                    row = conn.execute(
                        "SELECT status_evidence FROM anticipations WHERE id = %s",
                        (ant_id,),
                    ).fetchone()
                    if row and isinstance(row["status_evidence"], list):
                        existing_evidence[ant_id] = {
                            e.get("source_id") for e in row["status_evidence"] if e.get("source_id")
                        }
    except Exception:
        logger.debug("Failed to pre-fetch evidence for idempotency check", exc_info=True)

    for match in matches:
        ant_id = match.get("anticipation_id", "?")
        try:
            # Idempotency: skip if this source already has evidence on this anticipation
            if source_id in existing_evidence.get(ant_id, set()):
                skipped_dup += 1
                logger.debug("Skipping duplicate evidence: source %s already on anticipation %s", source_id, ant_id)
                continue

            evidence = {
                "source_id": source_id,
                "match_type": match["match_type"],
                "evidence": match.get("evidence", ""),
                "reasoning": match.get("reasoning", ""),
                "confidence": match.get("confidence", 0.5),
                "matched_at": datetime.now(timezone.utc).isoformat(),
            }
            append_anticipation_evidence(ant_id, evidence)
            persisted += 1
        except Exception:
            logger.warning(
                "Failed to persist anticipation match for %s",
                ant_id, exc_info=True,
            )

    # Emit notifications only for actually persisted matches (not skipped duplicates)
    persisted_ant_ids = set()
    for match in matches:
        ant_id = match.get("anticipation_id")
        if not ant_id or source_id in existing_evidence.get(ant_id, set()):
            continue  # Skip duplicates — same logic as persist loop above
        persisted_ant_ids.add(ant_id)
        if match.get("confidence", 0) >= NOTIFY_CONFIDENCE_FLOOR:
            try:
                from ingest.notification_emitter import emit_notification
                prediction_text = match.get("evidence", match.get("reasoning", ""))[:80]
                emit_notification(
                    type="anticipation_match",
                    entity_type="anticipation",
                    entity_id=ant_id,
                    title=f"Evidence found for prediction: {prediction_text}",
                    detail={"match_type": match["match_type"], "confidence": match["confidence"]},
                    source_id=source_id,
                )
            except Exception:
                logger.debug("Failed to emit anticipation notification", exc_info=True)

    # Auto-transition anticipation status based on accumulated evidence
    # Only check anticipations that actually received new evidence
    if persisted_ant_ids:
        persisted_matches = [m for m in matches if m.get("anticipation_id") in persisted_ant_ids]
        _auto_update_anticipation_statuses(persisted_matches, source_id)

    if skipped_dup:
        logger.info("Persisted %d/%d anticipation matches for source %s (%d skipped as duplicates)",
                     persisted, len(matches), source_id, skipped_dup)
    else:
        logger.info("Persisted %d/%d anticipation matches for source %s", persisted, len(matches), source_id)
    return persisted


def _auto_update_anticipation_statuses(matches: list[dict], source_id: str) -> None:
    """Auto-transition anticipation status when evidence accumulates.

    Rules:
    - If evidence_count >= AUTO_CONFIRM_EVIDENCE_COUNT and avg confidence > AUTO_CONFIRM_AVG_CONFIDENCE:
      transition to partially_confirmed
    - Only transitions from 'open' to 'partially_confirmed' (never auto-confirms fully)
    - Emits notification for human review
    """
    from reading_app.db import get_conn, update_anticipation_status

    # Collect unique anticipation IDs from this batch
    anticipation_ids = {m["anticipation_id"] for m in matches if m.get("anticipation_id")}
    if not anticipation_ids:
        return

    with get_conn() as conn:
        for ant_id in anticipation_ids:
            try:
                row = conn.execute(
                    "SELECT id, status, status_evidence, prediction FROM anticipations WHERE id = %s",
                    (ant_id,),
                ).fetchone()
                if not row or row["status"] != "open":
                    continue

                evidence = row["status_evidence"]
                if not isinstance(evidence, list) or len(evidence) < AUTO_CONFIRM_EVIDENCE_COUNT:
                    continue

                avg_conf = sum(e.get("confidence", 0) for e in evidence) / len(evidence)
                if avg_conf < AUTO_CONFIRM_AVG_CONFIDENCE:
                    continue

                update_anticipation_status(ant_id, "partially_confirmed")
                logger.info(
                    "Auto-transitioned anticipation %s to partially_confirmed "
                    "(evidence_count=%d, avg_confidence=%.2f)",
                    ant_id, len(evidence), avg_conf,
                )

                # Emit notification for human review
                try:
                    from ingest.notification_emitter import emit_notification
                    emit_notification(
                        type="anticipation_status_change",
                        entity_type="anticipation",
                        entity_id=ant_id,
                        title=f"Auto-confirmed: {(row['prediction'] or '')[:60]}",
                        detail={
                            "new_status": "partially_confirmed",
                            "evidence_count": len(evidence),
                            "avg_confidence": round(avg_conf, 2),
                        },
                        source_id=source_id,
                    )
                except Exception:
                    logger.debug("Failed to emit status change notification", exc_info=True)

            except Exception:
                logger.warning("Failed to auto-update anticipation %s", ant_id, exc_info=True)


def _parse_matches(text: str) -> list[dict]:
    """Parse JSON array of matches from LLM output."""
    result = parse_json_from_llm(text, expect=list)
    if result is None:
        logger.warning("Failed to parse anticipation match output")
        return []
    return result
