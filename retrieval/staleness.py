"""Entity staleness decay computation.

Computes exponential decay scores for landscape entities based on time
since last corroboration. More evidence slows decay. Entities past a
retirement threshold are flagged for review.
"""

from __future__ import annotations

import logging
import math
from datetime import datetime, timezone

from reading_app.db import get_conn

logger = logging.getLogger(__name__)

STALENESS_CONFIG = {
    "capability": {"half_life_days": 180, "retirement_threshold": 0.8},
    "limitation": {"half_life_days": 120, "retirement_threshold": 0.85},
    "bottleneck": {"half_life_days": 270, "retirement_threshold": 0.9},
}

# Tables mapping
_TABLE_MAP = {
    "capability": "capabilities",
    "limitation": "limitations",
    "bottleneck": "bottlenecks",
}


def compute_staleness_score(
    entity_type: str,
    created_at: datetime,
    last_corroborated_at: datetime | None,
    evidence_count: int = 1,
) -> float:
    """Compute staleness score (0.0 = fresh, 1.0 = maximally stale).

    Uses exponential decay from max(created_at, last_corroborated_at).
    More evidence sources slow the decay rate.
    """
    config = STALENESS_CONFIG.get(entity_type)
    if not config:
        return 0.0

    # Use the later of created_at and last_corroborated_at (matches SQL GREATEST)
    anchor = max(created_at, last_corroborated_at) if last_corroborated_at else created_at
    if anchor.tzinfo is None:
        anchor = anchor.replace(tzinfo=timezone.utc)

    days_elapsed = (datetime.now(timezone.utc) - anchor).total_seconds() / 86400

    # Evidence count slows decay: each additional source adds 20% to half-life
    evidence_factor = 1.0 + 0.2 * max(0, (evidence_count or 1) - 1)
    effective_half_life = config["half_life_days"] * evidence_factor

    # Exponential decay toward 1.0
    score = 1.0 - math.exp(-0.693 * days_elapsed / effective_half_life)
    return round(min(1.0, max(0.0, score)), 4)


def update_all_staleness_scores() -> dict[str, dict]:
    """Batch UPDATE staleness_score for all entities.

    Returns summary: {entity_type: {updated, stale, retirement_candidates}}.
    """
    results = {}

    for entity_type, config in STALENESS_CONFIG.items():
        table = _TABLE_MAP[entity_type]
        half_life = config["half_life_days"]
        threshold = config["retirement_threshold"]

        try:
            with get_conn() as conn:
                # Single batch UPDATE using SQL computation
                # evidence_count approximated from jsonb_array_length(evidence_sources)
                conn.execute(
                    f"""UPDATE {table}
                        SET staleness_score = ROUND(CAST(
                            1.0 - EXP(
                                -0.693 * EXTRACT(EPOCH FROM (NOW() - GREATEST(created_at, COALESCE(last_corroborated_at, created_at)))) / 86400.0
                                / (%s * (1.0 + 0.2 * GREATEST(0, COALESCE(jsonb_array_length(evidence_sources), 1) - 1)))
                            ) AS NUMERIC), 4)""",
                    (half_life,),
                )
                conn.commit()

                # Count results
                stats = conn.execute(
                    f"""SELECT
                            COUNT(*) AS total,
                            COUNT(*) FILTER (WHERE staleness_score > 0.3) AS stale,
                            COUNT(*) FILTER (WHERE staleness_score > %s) AS retirement_candidates
                        FROM {table}""",
                    (threshold,),
                ).fetchone()

                results[entity_type] = {
                    "updated": stats["total"],
                    "stale": stats["stale"],
                    "retirement_candidates": stats["retirement_candidates"],
                }
                logger.info(
                    "staleness_updated",
                    entity_type=entity_type,
                    **results[entity_type],
                )

        except Exception:
            logger.error("Failed to update staleness for %s", entity_type, exc_info=True)
            results[entity_type] = {"updated": 0, "stale": 0, "retirement_candidates": 0, "error": True}

    # Log to quality_metrics if available
    try:
        from reading_app.quality_store import log_quality_metric
        total_stale = sum(r.get("stale", 0) for r in results.values())
        total_retirement = sum(r.get("retirement_candidates", 0) for r in results.values())
        log_quality_metric(
            "staleness_decay", "system", "all",
            {**{et: r for et, r in results.items()},
             "total_stale": total_stale, "total_retirement_candidates": total_retirement},
            aggregate_score=total_stale,
            skill="heartbeat",
        )
    except Exception:
        pass

    return results


def get_retirement_candidates(entity_type: str | None = None) -> list[dict]:
    """Get entities past retirement threshold for review."""
    candidates = []
    types = [entity_type] if entity_type else list(STALENESS_CONFIG.keys())

    for etype in types:
        config = STALENESS_CONFIG.get(etype)
        table = _TABLE_MAP.get(etype)
        if not config or not table:
            continue

        try:
            with get_conn() as conn:
                rows = conn.execute(
                    f"""SELECT id, description, staleness_score, created_at, last_corroborated_at
                        FROM {table}
                        WHERE staleness_score > %s
                        ORDER BY staleness_score DESC
                        LIMIT 20""",
                    (config["retirement_threshold"],),
                ).fetchall()
                for r in rows:
                    candidates.append({
                        "entity_type": etype,
                        **dict(r),
                    })
        except Exception:
            logger.debug("Failed to get retirement candidates for %s", etype, exc_info=True)

    return candidates
