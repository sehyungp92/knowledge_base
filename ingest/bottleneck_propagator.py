"""Bottleneck propagation from breakthrough detection.

When a breakthrough is detected with bottlenecks_affected entries, this module
propagates the effects: adds to active_approaches, conservatively adjusts
resolution_horizon, and logs changes to challenge_log for auditability.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

# Horizon ordering from longest to shortest
HORIZON_ORDER = [
    "possibly_fundamental",
    "5+_years",
    "unknown",
    "3-5_years",
    "1-2_years",
    "months",
]


@dataclass
class BottleneckUpdate:
    """Represents a pending update to a bottleneck from breakthrough propagation."""
    bottleneck_id: str
    add_approach: dict | None = None
    new_horizon: str | None = None
    note: str | None = None
    old_horizon: str | None = None
    attribution: str = "automated_propagation"
    propagation_source: str | None = None


def propagate_breakthrough_to_bottlenecks(
    breakthrough: dict,
    source_id: str,
) -> list[BottleneckUpdate]:
    """Determine bottleneck updates from a breakthrough's bottlenecks_affected.

    For each affected bottleneck:
    1. Load current bottleneck state
    2. Determine updates based on effect type (resolves/reduces/reframes)
    3. Return list of pending updates (not yet persisted)

    Args:
        breakthrough: Dict with description, bottlenecks_affected, primary_source_id, etc.
        source_id: Source ID that triggered the breakthrough.

    Returns:
        List of BottleneckUpdate objects describing pending changes.
    """
    affected = breakthrough.get("bottlenecks_affected", [])
    if not affected:
        return []

    if isinstance(affected, str):
        try:
            affected = json.loads(affected)
        except (json.JSONDecodeError, TypeError):
            logger.warning("Could not parse bottlenecks_affected: %s", affected)
            return []

    from reading_app.db import get_bottleneck

    updates = []
    for entry in affected:
        if not isinstance(entry, dict):
            continue

        bottleneck_id = entry.get("bottleneck_id")
        effect = entry.get("effect", "reduces")

        if not bottleneck_id:
            continue

        try:
            bottleneck = get_bottleneck(bottleneck_id)
        except Exception:
            logger.warning("Failed to load bottleneck %s", bottleneck_id, exc_info=True)
            continue

        if not bottleneck:
            logger.debug("Bottleneck %s not found, skipping propagation", bottleneck_id)
            continue

        update = BottleneckUpdate(
            bottleneck_id=bottleneck_id,
            old_horizon=bottleneck.get("resolution_horizon"),
            propagation_source=source_id,
        )

        # Add breakthrough as an active approach
        promise_level = _effect_to_promise(effect)
        update.add_approach = {
            "approach": breakthrough["description"],
            "who": breakthrough.get("primary_source_id", source_id),
            "promise_level": promise_level,
            "source_ids": [source_id],
            "effect": effect,
        }

        # Conservative horizon adjustment
        current_horizon = bottleneck.get("resolution_horizon", "unknown")
        if effect == "resolves" and current_horizon in ("3-5_years", "5+_years", "unknown"):
            update.new_horizon = "1-2_years"
        elif effect == "reduces" and current_horizon in ("5+_years", "unknown", "possibly_fundamental"):
            update.new_horizon = "3-5_years"
        elif effect == "reframes":
            update.note = f"Reframed by: {breakthrough['description'][:120]}"
            # No horizon change for reframes

        updates.append(update)

    logger.info(
        "Breakthrough propagation: %d bottleneck updates from '%s'",
        len(updates), breakthrough.get("description", "?")[:60],
    )
    return updates


def persist_bottleneck_updates(
    updates: list[BottleneckUpdate],
    source_id: str,
    breakthrough_description: str = "",
) -> int:
    """Apply bottleneck updates to database with change tracking.

    For each update:
    - Adds approach to active_approaches
    - Adjusts resolution_horizon if warranted
    - Logs changes to challenge_log for auditability
    - Records in landscape_history for temporal trajectory

    Args:
        updates: List of BottleneckUpdate objects from propagate_breakthrough_to_bottlenecks().
        source_id: Source ID for attribution.
        breakthrough_description: Description of the triggering breakthrough (for history note).

    Returns:
        Count of successfully applied updates.
    """
    if not updates:
        return 0

    from ulid import ULID
    from reading_app.db import (
        append_bottleneck_approach, update_bottleneck,
        insert_challenge_log, insert_landscape_history,
    )

    applied = 0
    for update in updates:
        try:
            # Add approach
            if update.add_approach:
                append_bottleneck_approach(update.bottleneck_id, update.add_approach)

            # Adjust horizon
            if update.new_horizon:
                update_bottleneck(
                    update.bottleneck_id,
                    resolution_horizon=update.new_horizon,
                )

                # Log to challenge_log for auditability
                insert_challenge_log(
                    id=f"cl_{ULID()}",
                    entity_type="bottleneck",
                    entity_id=update.bottleneck_id,
                    system_position=f"resolution_horizon was {update.old_horizon}",
                    outcome="system_updated",
                    resolution_reasoning=f"Breakthrough propagation from source {source_id}",
                    changes_made=[{
                        "table": "bottlenecks",
                        "id": update.bottleneck_id,
                        "field": "resolution_horizon",
                        "old_value": update.old_horizon,
                        "new_value": update.new_horizon,
                    }],
                )

                # Record in landscape_history
                _note = (
                    f"Triggered by breakthrough: {breakthrough_description[:120]}"
                    if breakthrough_description else None
                )
                insert_landscape_history(
                    entity_type="bottleneck",
                    entity_id=update.bottleneck_id,
                    field="resolution_horizon",
                    old_value=update.old_horizon,
                    new_value=update.new_horizon,
                    source_id=source_id,
                    attribution=update.attribution,
                    note=_note,
                )

            applied += 1

            # Emit notification for horizon shifts
            if update.new_horizon and update.old_horizon:
                try:
                    from ingest.notification_emitter import emit_notification
                    emit_notification(
                        type="bottleneck_horizon_shift",
                        entity_type="bottleneck",
                        entity_id=update.bottleneck_id,
                        title=f"Resolution horizon shifted: {update.old_horizon} \u2192 {update.new_horizon}",
                        detail={"old_horizon": update.old_horizon, "new_horizon": update.new_horizon},
                        source_id=source_id,
                    )
                except Exception:
                    logger.debug("Failed to emit bottleneck notification", exc_info=True)
        except Exception:
            logger.warning(
                "Failed to apply bottleneck update for %s",
                update.bottleneck_id, exc_info=True,
            )

    logger.info("Applied %d/%d bottleneck updates for source %s", applied, len(updates), source_id)
    return applied


def _effect_to_promise(effect: str) -> str:
    """Map breakthrough effect type to approach promise level."""
    return {
        "resolves": "high",
        "reduces": "medium",
        "reframes": "medium",
    }.get(effect, "low")
