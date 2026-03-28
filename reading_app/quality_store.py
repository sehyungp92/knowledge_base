"""Quality metrics persistence for pipeline learning loops.

Stores and retrieves quality signals from state summaries, source extractions,
and tournament strategies to enable trend analysis and self-improvement.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone

from reading_app.db import get_conn

logger = logging.getLogger(__name__)


def log_quality_metric(
    metric_type: str,
    entity_type: str,
    entity_id: str,
    dimensions: dict,
    aggregate_score: float | None = None,
    cost_usd: float | None = None,
    skill: str | None = None,
) -> None:
    """Insert a quality metric row."""
    try:
        with get_conn() as conn:
            conn.execute(
                """INSERT INTO quality_metrics
                   (metric_type, entity_type, entity_id, dimensions, aggregate_score, cost_usd, skill)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (
                    metric_type,
                    entity_type,
                    entity_id,
                    json.dumps(dimensions),
                    aggregate_score,
                    cost_usd,
                    skill,
                ),
            )
            conn.commit()
    except Exception:
        logger.debug("Failed to log quality metric %s/%s", metric_type, entity_id, exc_info=True)


def get_quality_trends(
    metric_type: str,
    entity_type: str | None = None,
    entity_id: str | None = None,
    days: int = 30,
) -> list[dict]:
    """Get quality metrics over time for trend analysis."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    try:
        with get_conn() as conn:
            query = "SELECT * FROM quality_metrics WHERE metric_type = %s AND created_at > %s"
            params: list = [metric_type, cutoff]
            if entity_type:
                query += " AND entity_type = %s"
                params.append(entity_type)
            if entity_id:
                query += " AND entity_id = %s"
                params.append(entity_id)
            query += " ORDER BY created_at DESC"
            return [dict(r) for r in conn.execute(query, params).fetchall()]
    except Exception:
        logger.debug("Failed to get quality trends", exc_info=True)
        return []


def get_strategy_performance(days: int = 90) -> list[dict]:
    """Aggregate tournament strategy performance ranked by avg idea score."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    try:
        with get_conn() as conn:
            rows = conn.execute(
                """SELECT entity_id AS strategy,
                          COUNT(*) AS runs,
                          AVG(aggregate_score) AS avg_score,
                          AVG((dimensions->>'ideas_generated')::float) AS avg_generated,
                          AVG((dimensions->>'novelty_pass_rate')::float) AS avg_novelty_rate
                   FROM quality_metrics
                   WHERE metric_type = 'tournament_strategy'
                     AND created_at > %s
                   GROUP BY entity_id
                   ORDER BY avg_score DESC NULLS LAST""",
                (cutoff,),
            ).fetchall()
            return [dict(r) for r in rows]
    except Exception:
        logger.debug("Failed to get strategy performance", exc_info=True)
        return []
