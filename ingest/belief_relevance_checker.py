"""Belief relevance checking during source ingestion.

Replaces binary "conflict detection" with a 5-type relationship taxonomy:
contradicts, undermines, supports, extends, supersedes.

Called during /save Step 5c (best-effort — failure does not abort save).
Checks new claims against active beliefs and persists relevance hits
to evidence_for/evidence_against as appropriate.
"""

from __future__ import annotations

import json
import logging
import re
from datetime import datetime, timezone

from ingest.json_parser import parse_json_from_llm
from pathlib import Path

logger = logging.getLogger(__name__)

VALID_RELATIONSHIPS = {"contradicts", "undermines", "supports", "extends", "supersedes"}

RELEVANCE_CHECK_PROMPT = """You are checking whether newly extracted claims are relevant to the user's tracked beliefs about AI.

{temporal_context}

## Active Beliefs
{beliefs_text}

## New Claims from Source "{source_id}"
{claims_text}

For each belief, check if ANY of the new claims are relevant. Classify the relationship:

| Relationship | Description | Example |
|---|---|---|
| contradicts | New evidence directly opposes belief | Belief: "Scaling laws will hold" + Claim: "We found diminishing returns at 10T params" |
| undermines | New evidence weakens a premise the belief rests on | Belief: "Data is the bottleneck" + Claim: "Synthetic data reaches 90% of real data quality" |
| supports | New evidence strengthens belief | Belief: "RL is key for reasoning" + Claim: "RL-trained models outperform SFT on math" |
| extends | New evidence adds nuance or scope | Belief: "LLMs can reason" + Claim: "LLMs reason well on math but fail at spatial reasoning" |
| supersedes | New framing makes belief obsolete | Belief: "Transformers are the best architecture" + Claim: "SSMs match transformers with 10x efficiency" |

Return a JSON array of relevance hits (empty array if none):
```json
[
  {{
    "belief_id": "the belief ID",
    "relationship": "contradicts" | "undermines" | "supports" | "extends" | "supersedes",
    "evidence": "the specific claim text that is relevant",
    "reasoning": "1-2 sentences explaining the relationship, including temporal reasoning if source date is known",
    "confidence": 0.0-1.0,
    "landscape_entity": {{"type": "capability"|"limitation"|"bottleneck"|"anticipation", "id": "entity_id"}} or null
  }}
]
```

Rules:
- Only include genuine relevance — not tangential connections
- A single claim can be relevant to multiple beliefs
- "supports" is as important as "contradicts" — track both
- Set confidence based on how directly the claim addresses the belief
- When a recent source contradicts or supersedes a belief, this is a stronger signal than an older source doing the same — set confidence higher accordingly
- When an old source supports a belief, note that this doesn't confirm the belief is still current
- If the triggering claim maps to a known landscape entity (capability, limitation, bottleneck, or anticipation), include it in landscape_entity. Otherwise set to null.
- If no claims are relevant to any belief, return []
"""


def check_belief_relevance(
    claims: list[dict],
    active_beliefs: list[dict],
    source_id: str,
    published_at: str | None = None,
    executor=None,
) -> list[dict]:
    """Check new claims against active beliefs for relevance.

    Args:
        claims: List of claim dicts from extraction (with claim_text, source_id).
        active_beliefs: List of active belief dicts from DB.
        source_id: Source ID for attribution.
        published_at: Publication date of the source (ISO-8601 string or None).
        executor: ClaudeExecutor instance.

    Returns:
        List of relevance hit dicts with belief_id, relationship, evidence, reasoning, confidence.
    """
    if not claims or not active_beliefs:
        return []

    # Build text representations
    beliefs_text = "\n".join(
        f"- ID: {b['id']} | Claim: {b['claim']} | Confidence: {b.get('confidence', 0.5)} | "
        f"Type: {b.get('belief_type', 'factual')} | Theme: {b.get('theme_name', b.get('domain_theme_id', '?'))}"
        for b in active_beliefs
    )

    claims_text = "\n".join(
        f"- {c.get('claim_text', c.get('claim', ''))}"
        for c in claims[:30]  # Cap at 30 claims to fit context
    )

    if not claims_text.strip():
        return []

    if executor is None:
        from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
        executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    # Build temporal context
    if published_at:
        temporal_context = (
            f"**This source was published on {published_at}.**\n"
            "Consider recency when assessing relevance — recent contradictions are stronger "
            "signals than old ones, and old supporting evidence doesn't confirm a belief is still current."
        )
    else:
        temporal_context = "**Source publication date: unknown.** Assess relevance without temporal weighting."

    prompt = RELEVANCE_CHECK_PROMPT.format(
        beliefs_text=beliefs_text,
        claims_text=claims_text,
        source_id=source_id,
        temporal_context=temporal_context,
    )

    try:
        result = executor.run_raw(
            prompt,
            session_id=f"belief_relevance_{source_id}",
            timeout=180,
        )
        hits = _parse_relevance_hits(result.text)
    except Exception:
        logger.warning("LLM belief relevance check failed for %s", source_id, exc_info=True)
        return []

    # Validate hits
    valid_belief_ids = {b["id"] for b in active_beliefs}
    valid_hits = []
    for hit in hits:
        if hit.get("belief_id") not in valid_belief_ids:
            continue
        if hit.get("relationship") not in VALID_RELATIONSHIPS:
            continue
        if hit.get("confidence", 0) < 0.5:
            continue
        valid_hits.append(hit)

    logger.info(
        "Belief relevance check for %s: %d hits from %d beliefs",
        source_id, len(valid_hits), len(active_beliefs),
    )
    return valid_hits


def persist_belief_updates(
    relevance_hits: list[dict],
    source_id: str,
) -> dict:
    """Persist belief relevance hits to evidence_for/evidence_against.

    Args:
        relevance_hits: List of relevance hit dicts from check_belief_relevance().
        source_id: Source ID for attribution.

    Returns:
        Dict with counts: {supports, contradicts, undermines, extends, supersedes, total}.
    """
    if not relevance_hits:
        return {"supports": 0, "contradicts": 0, "undermines": 0,
                "extends": 0, "supersedes": 0, "total": 0}

    from reading_app.db import append_belief_evidence, append_belief_landscape_link

    counts = {r: 0 for r in VALID_RELATIONSHIPS}
    counts["total"] = 0

    for hit in relevance_hits:
        try:
            relationship = hit["relationship"]
            evidence = {
                "source_id": source_id,
                "relationship": relationship,
                "evidence": hit.get("evidence", ""),
                "reasoning": hit.get("reasoning", ""),
                "confidence": hit.get("confidence", 0.5),
                "added_at": datetime.now(timezone.utc).isoformat(),
            }

            # Supports and extends go to evidence_for; contradicts, undermines, supersedes to evidence_against
            if relationship in ("supports", "extends"):
                evidence_type = "for"
            else:
                evidence_type = "against"

            append_belief_evidence(hit["belief_id"], evidence, evidence_type=evidence_type)
            counts[relationship] = counts.get(relationship, 0) + 1
            counts["total"] += 1

            # Populate landscape_links if the LLM identified a landscape entity
            landscape_entity = hit.get("landscape_entity")
            if (landscape_entity
                    and isinstance(landscape_entity, dict)
                    and landscape_entity.get("type") in ("capability", "limitation", "bottleneck", "anticipation")
                    and landscape_entity.get("id")):
                try:
                    append_belief_landscape_link(hit["belief_id"], {
                        "type": landscape_entity["type"],
                        "id": landscape_entity["id"],
                        "relationship": relationship,
                        "source_id": source_id,
                    })
                except Exception:
                    logger.debug("Failed to add landscape link for belief %s", hit["belief_id"], exc_info=True)

        except Exception:
            logger.warning(
                "Failed to persist belief relevance hit for belief %s",
                hit.get("belief_id", "?"), exc_info=True,
            )

    # Emit notifications for contradicts/undermines relationships
    for hit in relevance_hits:
        if hit.get("relationship") in ("contradicts", "undermines"):
            try:
                from ingest.notification_emitter import emit_notification
                emit_notification(
                    type="belief_challenged",
                    entity_type="belief",
                    entity_id=hit["belief_id"],
                    title=f"New evidence {hit['relationship']} your belief",
                    detail={"relationship": hit["relationship"], "evidence": hit.get("evidence", "")[:200]},
                    source_id=source_id,
                )
            except Exception:
                logger.debug("Failed to emit belief notification", exc_info=True)

    logger.info("Persisted %d belief relevance hits for source %s: %s", counts["total"], source_id, counts)
    return counts


def categorize_hits(hits: list[dict]) -> dict:
    """Categorize relevance hits for response formatting.

    Returns:
        Dict with keys: has_challenges (bool), has_support (bool),
        challenges (contradicts + undermines + supersedes), support (supports + extends).
    """
    challenges = [h for h in hits if h.get("relationship") in ("contradicts", "undermines", "supersedes")]
    support = [h for h in hits if h.get("relationship") in ("supports", "extends")]
    return {
        "has_challenges": len(challenges) > 0,
        "has_support": len(support) > 0,
        "challenges": challenges,
        "support": support,
    }


def _parse_relevance_hits(text: str) -> list[dict]:
    """Parse JSON array of relevance hits from LLM output."""
    result = parse_json_from_llm(text, expect=list)
    if result is None:
        logger.warning("Failed to parse belief relevance check output")
        return []
    return result
