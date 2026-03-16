"""Landscape-specific retrieval queries.

Provides theme state summaries, bottleneck rankings, breakthrough timelines,
anticipation tracking, and velocity computation for skills and heartbeat.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from reading_app import db

logger = logging.getLogger(__name__)

# Significance-scaled breakthrough display windows (in days).
# Higher-significance breakthroughs remain visible longer because
# their implications take longer to fully propagate.
BREAKTHROUGH_WINDOW_DAYS = {
    "incremental": 90,
    "notable": 180,
    "major": 365,
    "paradigm_shifting": 730,
}
BREAKTHROUGH_DEFAULT_WINDOW = 90


def get_theme_state(theme_id: str) -> dict:
    """Get full landscape state for a theme: capabilities, limitations,
    bottlenecks, breakthroughs, anticipations, cross-theme implications."""
    with db.get_conn() as conn:
        theme = conn.execute(
            "SELECT * FROM themes WHERE id = %s", (theme_id,)
        ).fetchone()
        if not theme:
            return {"theme": None}

        capabilities = conn.execute(
            "SELECT * FROM capabilities WHERE theme_id = %s ORDER BY maturity DESC NULLS LAST",
            (theme_id,),
        ).fetchall()

        limitations = conn.execute(
            "SELECT * FROM limitations WHERE theme_id = %s ORDER BY severity ASC NULLS LAST",
            (theme_id,),
        ).fetchall()

        bottlenecks = conn.execute(
            "SELECT * FROM bottlenecks WHERE theme_id = %s", (theme_id,),
        ).fetchall()

        # Significance-scaled breakthrough window: paradigm_shifting breakthroughs
        # remain visible for up to 2 years, while incremental ones fade after 90 days
        max_window = max(BREAKTHROUGH_WINDOW_DAYS.values())
        all_breakthroughs = conn.execute(
            """SELECT * FROM breakthroughs WHERE theme_id = %s
               AND detected_at >= NOW() - make_interval(days => %s)
               ORDER BY detected_at DESC""",
            (theme_id, max_window),
        ).fetchall()
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        breakthroughs = []
        for bt in all_breakthroughs:
            sig = bt.get("significance") or "incremental"
            window_days = BREAKTHROUGH_WINDOW_DAYS.get(sig, BREAKTHROUGH_DEFAULT_WINDOW)
            detected = bt.get("detected_at")
            if detected:
                if hasattr(detected, 'tzinfo') and detected.tzinfo is None:
                    detected = detected.replace(tzinfo=timezone.utc)
                age_days = (now - detected).days
                if age_days <= window_days:
                    breakthroughs.append(bt)
            else:
                breakthroughs.append(bt)

        anticipations = conn.execute(
            """SELECT * FROM anticipations WHERE theme_id = %s AND status = 'open'
               ORDER BY confidence DESC""",
            (theme_id,),
        ).fetchall()

        implications = conn.execute(
            """SELECT cti.*, ts.name AS source_theme, tt.name AS target_theme
               FROM cross_theme_implications cti
               JOIN themes ts ON cti.source_theme_id = ts.id
               JOIN themes tt ON cti.target_theme_id = tt.id
               WHERE cti.source_theme_id = %s OR cti.target_theme_id = %s
               ORDER BY cti.confidence DESC NULLS LAST
               LIMIT 30""",
            (theme_id, theme_id),
        ).fetchall()

    return {
        "theme": theme,
        "capabilities": capabilities,
        "limitations": limitations,
        "bottlenecks": bottlenecks,
        "breakthroughs": breakthroughs,
        "anticipations": anticipations,
        "cross_theme_implications": implications,
    }


def get_consolidated_implications(theme_id: str, limit: int = 20) -> list[dict]:
    """Get implications grouped by (source_theme, target_theme) pair.

    Returns the top implication per pair plus count and second perspective,
    ordered by max confidence. Used by /synthesis and /landscape for compact display.
    """
    with db.get_conn() as conn:
        rows = conn.execute(
            """WITH ranked AS (
                   SELECT
                       cti.source_theme_id, cti.target_theme_id,
                       ts.name AS source_theme, tt.name AS target_theme,
                       cti.implication, cti.confidence, cti.evidence_sources,
                       ROW_NUMBER() OVER (
                           PARTITION BY cti.source_theme_id, cti.target_theme_id
                           ORDER BY cti.confidence DESC
                       ) AS rn,
                       COUNT(*) OVER (
                           PARTITION BY cti.source_theme_id, cti.target_theme_id
                       ) AS pair_count,
                       MAX(cti.confidence) OVER (
                           PARTITION BY cti.source_theme_id, cti.target_theme_id
                       ) AS max_confidence
                   FROM cross_theme_implications cti
                   JOIN themes ts ON cti.source_theme_id = ts.id
                   JOIN themes tt ON cti.target_theme_id = tt.id
                   WHERE cti.source_theme_id = %s OR cti.target_theme_id = %s
               )
               SELECT
                   source_theme_id, target_theme_id,
                   source_theme, target_theme,
                   implication, confidence, evidence_sources,
                   rn, pair_count, max_confidence
               FROM ranked
               WHERE rn <= 2
               ORDER BY max_confidence DESC, source_theme_id, target_theme_id, rn""",
            (theme_id, theme_id),
        ).fetchall()

    # Group rows in Python by (source_theme_id, target_theme_id)
    groups: dict[tuple, list] = {}
    for row in rows:
        key = (row["source_theme_id"], row["target_theme_id"])
        groups.setdefault(key, []).append(row)

    results = []
    for (src_id, tgt_id), group_rows in groups.items():
        first = group_rows[0]
        results.append({
            "source_theme_id": src_id,
            "target_theme_id": tgt_id,
            "source_theme": first["source_theme"],
            "target_theme": first["target_theme"],
            "max_confidence": first["max_confidence"],
            "observation_count": first["pair_count"],
            "top_implication": first["implication"] or "",
            "second_perspective": group_rows[1]["implication"] if len(group_rows) > 1 else None,
            "all_evidence": [r["evidence_sources"] for r in group_rows if r["evidence_sources"] is not None],
        })

    results.sort(key=lambda x: x.get("max_confidence") or 0, reverse=True)
    return results[:limit]


def get_recent_breakthroughs(days: int | None = None, theme_id: str | None = None) -> list[dict]:
    """Get recent breakthroughs with significance-scaled windows.

    When days is None (default), uses significance-based windows:
    incremental=90d, notable=180d, major=365d, paradigm_shifting=730d.
    When days is explicitly provided, uses that as a flat cutoff.
    """
    from datetime import datetime, timezone
    max_window = days if days is not None else max(BREAKTHROUGH_WINDOW_DAYS.values())

    with db.get_conn() as conn:
        if theme_id:
            rows = conn.execute(
                """SELECT b.*, t.name AS theme_name FROM breakthroughs b
                   JOIN themes t ON b.theme_id = t.id
                   WHERE b.theme_id = %s AND b.detected_at >= NOW() - make_interval(days => %s)
                   ORDER BY b.detected_at DESC""",
                (theme_id, max_window),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT b.*, t.name AS theme_name FROM breakthroughs b
                   JOIN themes t ON b.theme_id = t.id
                   WHERE b.detected_at >= NOW() - make_interval(days => %s)
                   ORDER BY b.detected_at DESC""",
                (max_window,),
            ).fetchall()

    # If a specific days cutoff was provided, return as-is (backward compat)
    if days is not None:
        return rows

    # Apply significance-scaled filtering
    now = datetime.now(timezone.utc)
    filtered = []
    for bt in rows:
        sig = bt.get("significance") or "incremental"
        window_days = BREAKTHROUGH_WINDOW_DAYS.get(sig, BREAKTHROUGH_DEFAULT_WINDOW)
        detected = bt.get("detected_at")
        if detected:
            if hasattr(detected, 'tzinfo') and detected.tzinfo is None:
                detected = detected.replace(tzinfo=timezone.utc)
            age_days = (now - detected).days
            if age_days <= window_days:
                filtered.append(bt)
        else:
            filtered.append(bt)
    return filtered


def get_bottleneck_ranking(theme_id: str | None = None) -> list[dict]:
    """Get bottlenecks ranked by impact x (1/resolution_horizon)."""
    with db.get_conn() as conn:
        where = "WHERE b.theme_id = %s" if theme_id else ""
        params = (theme_id,) if theme_id else ()
        return conn.execute(
            f"""SELECT b.*, t.name AS theme_name,
                   CASE b.resolution_horizon
                       WHEN 'months' THEN 5
                       WHEN '1-2_years' THEN 4
                       WHEN '3-5_years' THEN 3
                       WHEN '5+_years' THEN 2
                       WHEN 'possibly_fundamental' THEN 1
                       ELSE 0
                   END AS horizon_score
               FROM bottlenecks b
               JOIN themes t ON b.theme_id = t.id
               {where}
               ORDER BY horizon_score DESC, b.confidence DESC""",
            params,
        ).fetchall()


def compute_theme_velocity() -> list[dict]:
    """Compute both field velocity and reading velocity for all themes.

    - **reading_velocity** (based on ingested_at): how actively the user is
      engaging with this theme. Uses all sources.
    - **field_velocity** (based on published_at): how much is actually being
      published in this theme. Only counts sources with known publication dates.

    The combined `velocity` value uses field_velocity when available, falling
    back to reading_velocity. This is what gets persisted to themes.velocity.
    """
    with db.get_conn() as conn:
        rows = conn.execute(
            """WITH source_counts AS (
                   SELECT
                       st.theme_id,
                       COUNT(DISTINCT st.source_id) AS total_sources,
                       COUNT(DISTINCT st.source_id) FILTER (
                           WHERE s.published_at IS NOT NULL
                       ) AS total_with_pub_date
                   FROM source_themes st
                   JOIN sources s ON st.source_id = s.id
                   GROUP BY st.theme_id
               ),
               recent_ingested AS (
                   SELECT
                       t.id AS theme_id,
                       COUNT(DISTINCT st.source_id) AS recent_ingested
                   FROM themes t
                   JOIN source_themes st ON t.id = st.theme_id
                   JOIN sources s ON st.source_id = s.id
                   WHERE s.ingested_at >= NOW() - make_interval(days => t.velocity_window_days)
                   GROUP BY t.id
               ),
               recent_published AS (
                   SELECT
                       t.id AS theme_id,
                       COUNT(DISTINCT st.source_id) AS recent_published
                   FROM themes t
                   JOIN source_themes st ON t.id = st.theme_id
                   JOIN sources s ON st.source_id = s.id
                   WHERE s.published_at IS NOT NULL
                     AND s.published_at >= NOW() - make_interval(days => t.velocity_window_days)
                   GROUP BY t.id
               ),
               recent_breakthroughs AS (
                   SELECT
                       theme_id,
                       COUNT(*) AS recent_breakthroughs
                   FROM breakthroughs
                   WHERE detected_at >= NOW() - INTERVAL '180 days'
                   GROUP BY theme_id
               )
               SELECT
                   t.id,
                   t.name,
                   t.velocity_window_days,
                   COALESCE(ri.recent_ingested, 0) AS recent_ingested,
                   COALESCE(rp.recent_published, 0) AS recent_published,
                   COALESCE(sc.total_with_pub_date, 0) AS total_with_pub_date,
                   COALESCE(rb.recent_breakthroughs, 0) AS recent_breakthroughs,
                   COALESCE(sc.total_sources, 0) AS total_sources
               FROM themes t
               LEFT JOIN source_counts sc ON sc.theme_id = t.id
               LEFT JOIN recent_ingested ri ON ri.theme_id = t.id
               LEFT JOIN recent_published rp ON rp.theme_id = t.id
               LEFT JOIN recent_breakthroughs rb ON rb.theme_id = t.id
               ORDER BY COALESCE(ri.recent_ingested, 0) DESC, t.name ASC"""
        ).fetchall()

    results = []
    for row in rows:
        total = row["total_sources"] or 1
        recent_ingested = row["recent_ingested"] or 0
        recent_published = row["recent_published"] or 0
        total_with_pub = row["total_with_pub_date"] or 0
        breakthroughs = row["recent_breakthroughs"] or 0

        # Reading velocity: based on ingestion dates (user activity)
        reading_velocity = min(1.0, (recent_ingested / max(total, 5)) + (breakthroughs * 0.1))

        # Field velocity: based on publication dates (actual field activity)
        # Only meaningful if we have enough sources with publication dates
        if total_with_pub >= 3:
            field_velocity = min(1.0, (recent_published / max(total_with_pub, 5)) + (breakthroughs * 0.1))
        else:
            field_velocity = None

        # Combined velocity: prefer field velocity when available
        velocity = field_velocity if field_velocity is not None else reading_velocity

        results.append({
            **row,
            "velocity": round(velocity, 3),
            "reading_velocity": round(reading_velocity, 3),
            "field_velocity": round(field_velocity, 3) if field_velocity is not None else None,
        })
    return results


def update_all_theme_velocities() -> int:
    """Compute and persist velocity for all themes. Returns count updated."""
    velocities = compute_theme_velocity()
    count = 0
    for row in velocities:
        db.update_theme_velocity(row["id"], row["velocity"])
        count += 1
    return count


def get_anticipations_with_evidence() -> list[dict]:
    """Get open anticipations that have accumulated evidence matches."""
    with db.get_conn() as conn:
        return conn.execute(
            """SELECT a.id, a.prediction, a.theme_id, t.name AS theme_name,
                  a.confidence, a.status_evidence,
                  jsonb_array_length(COALESCE(a.status_evidence, '[]'::jsonb)) AS evidence_count
               FROM anticipations a
               JOIN themes t ON a.theme_id = t.id
               WHERE a.status = 'open'
                 AND jsonb_array_length(COALESCE(a.status_evidence, '[]'::jsonb)) > 0
               ORDER BY evidence_count DESC"""
        ).fetchall()


def get_limitation_validation_rates() -> list[dict]:
    """Get validation rates by signal_type for extraction calibration."""
    with db.get_conn() as conn:
        return conn.execute(
            """SELECT signal_type,
                  COUNT(*) AS total,
                  COUNT(*) FILTER (WHERE validated = TRUE) AS confirmed,
                  COUNT(*) FILTER (WHERE validated = FALSE) AS rejected,
                  ROUND(COUNT(*) FILTER (WHERE validated = FALSE)::numeric /
                        NULLIF(COUNT(*) FILTER (WHERE validated IS NOT NULL), 0), 2) AS rejection_rate
               FROM limitations
               WHERE signal_type LIKE 'implicit_%%'
               GROUP BY signal_type
               HAVING COUNT(*) FILTER (WHERE validated IS NOT NULL) >= 10
               ORDER BY rejection_rate DESC NULLS LAST"""
        ).fetchall()


# ---------------------------------------------------------------------------
# Coverage gap queries (for /gaps skill)
# ---------------------------------------------------------------------------

def get_over_optimistic_themes() -> list[dict]:
    """Themes with >2 capabilities but zero limitations — over-optimistic coverage."""
    with db.get_conn() as conn:
        return conn.execute(
            """WITH capability_counts AS (
                   SELECT theme_id, COUNT(*) AS capability_count
                   FROM capabilities
                   GROUP BY theme_id
               ),
               limitation_counts AS (
                   SELECT theme_id, COUNT(*) AS limitation_count
                   FROM limitations
                   GROUP BY theme_id
               )
               SELECT
                   t.id,
                   t.name,
                   COALESCE(c.capability_count, 0) AS capability_count,
                   COALESCE(l.limitation_count, 0) AS limitation_count
               FROM themes t
               LEFT JOIN capability_counts c ON c.theme_id = t.id
               LEFT JOIN limitation_counts l ON l.theme_id = t.id
               WHERE COALESCE(c.capability_count, 0) > 2
                 AND COALESCE(l.limitation_count, 0) = 0
               ORDER BY COALESCE(c.capability_count, 0) DESC"""
        ).fetchall()


def get_blind_spot_bottlenecks() -> list[dict]:
    """Bottlenecks with no active approaches — blind spots."""
    with db.get_conn() as conn:
        return conn.execute(
            """SELECT b.*, t.name AS theme_name
               FROM bottlenecks b
               JOIN themes t ON b.theme_id = t.id
               WHERE b.active_approaches IS NULL
                  OR jsonb_array_length(b.active_approaches) = 0
               ORDER BY b.confidence DESC"""
        ).fetchall()


def get_untested_anticipations(min_age_days: int = 60) -> list[dict]:
    """Anticipations with zero status_evidence after min_age_days."""
    with db.get_conn() as conn:
        return conn.execute(
            """SELECT a.*, t.name AS theme_name,
                  EXTRACT(DAY FROM NOW() - a.created_at)::int AS age_days
               FROM anticipations a
               JOIN themes t ON a.theme_id = t.id
               WHERE a.status = 'open'
                 AND (a.status_evidence IS NULL
                      OR jsonb_array_length(a.status_evidence) = 0)
                 AND a.created_at <= NOW() - make_interval(days => %s)
               ORDER BY a.created_at ASC""",
            (min_age_days,),
        ).fetchall()


def compute_anticipation_staleness(theme_id: str | None = None) -> list[dict]:
    """Compute staleness score (0.0=fresh, 1.0=should retire) for open anticipations.

    Staleness factors:
    - Timeline expiry: how close the prediction is to its stated horizon
    - No-evidence penalty: no evidence after 90 days
    - Disconfirming evidence ratio
    """
    TIMELINE_HORIZON_DAYS = {
        "months": 365,        # ~12 months grace
        "1-2_years": 900,     # ~30 months
        "3-5_years": 2160,    # ~72 months (6 years)
        "5+_years": 3600,     # 10 years
    }
    NO_EVIDENCE_PENALTY_AFTER_DAYS = 90
    NO_EVIDENCE_MAX_PENALTY = 0.3

    with db.get_conn() as conn:
        query = """
            SELECT a.*, t.name AS theme_name,
                   EXTRACT(DAY FROM NOW() - a.created_at)::int AS age_days
            FROM anticipations a
            JOIN themes t ON a.theme_id = t.id
            WHERE a.status = 'open'
        """
        params = []
        if theme_id:
            query += " AND a.theme_id = %s"
            params.append(theme_id)
        query += " ORDER BY a.created_at ASC"
        anticipations = conn.execute(query, params).fetchall()

    results = []
    for a in anticipations:
        age_days = a.get("age_days", 0)
        timeline = a.get("timeline") or "1-2_years"
        horizon_days = TIMELINE_HORIZON_DAYS.get(timeline, 900)

        # 1. Timeline expiry component (0.0 to 0.5)
        expiry_ratio = min(age_days / horizon_days, 1.0) if horizon_days > 0 else 1.0
        expiry_score = expiry_ratio * 0.5

        # 2. No-evidence penalty (0.0 to 0.3)
        evidence = a.get("status_evidence") or []
        if isinstance(evidence, str):
            import json as _json
            evidence = _json.loads(evidence)
        evidence_count = len(evidence)

        if evidence_count == 0 and age_days > NO_EVIDENCE_PENALTY_AFTER_DAYS:
            days_overdue = age_days - NO_EVIDENCE_PENALTY_AFTER_DAYS
            no_ev_score = min(days_overdue / 180, 1.0) * NO_EVIDENCE_MAX_PENALTY
        else:
            no_ev_score = 0.0

        # 3. Disconfirming evidence ratio (0.0 to 0.2)
        if evidence_count > 0:
            disconfirming = sum(1 for e in evidence if e.get("match_type") == "disconfirming")
            dis_ratio = disconfirming / evidence_count
            dis_score = dis_ratio * 0.2
        else:
            dis_score = 0.0

        staleness = min(expiry_score + no_ev_score + dis_score, 1.0)

        results.append({
            **a,
            "staleness": round(staleness, 3),
            "age_days": age_days,
            "evidence_count": evidence_count,
        })

    results.sort(key=lambda x: x["staleness"], reverse=True)
    return results


def get_incomplete_capabilities() -> list[dict]:
    """Capabilities at research_only maturity with no linked limitation."""
    with db.get_conn() as conn:
        return conn.execute(
            """SELECT c.*, t.name AS theme_name
               FROM capabilities c
               JOIN themes t ON c.theme_id = t.id
               WHERE c.maturity = 'research_only'
                 AND NOT EXISTS (
                     SELECT 1 FROM limitations l
                     WHERE l.theme_id = c.theme_id
                 )
               ORDER BY c.confidence DESC"""
        ).fetchall()


def get_unlinked_themes() -> list[dict]:
    """Themes with sources but zero cross-theme implications."""
    with db.get_conn() as conn:
        return conn.execute(
            """SELECT t.id, t.name, COUNT(st.source_id) AS source_count
               FROM themes t
               JOIN source_themes st ON t.id = st.theme_id
               WHERE NOT EXISTS (
                   SELECT 1 FROM cross_theme_implications cti
                   WHERE cti.source_theme_id = t.id OR cti.target_theme_id = t.id
               )
               GROUP BY t.id, t.name
               HAVING COUNT(st.source_id) > 0
               ORDER BY COUNT(st.source_id) DESC"""
        ).fetchall()


def get_validation_backlog() -> list[dict]:
    """Count of unvalidated implicit limitations by theme."""
    with db.get_conn() as conn:
        return conn.execute(
            """SELECT t.id AS theme_id, t.name AS theme_name,
                  COUNT(*) AS unvalidated_count
               FROM limitations l
               JOIN themes t ON l.theme_id = t.id
               WHERE l.signal_type LIKE 'implicit_%%'
                 AND l.validated IS NULL
               GROUP BY t.id, t.name
               ORDER BY COUNT(*) DESC"""
        ).fetchall()


def get_theme_source_counts() -> list[dict]:
    """Source counts per theme, for identifying themes the user is falling behind on."""
    with db.get_conn() as conn:
        return conn.execute(
            """SELECT t.id, t.name, t.velocity,
                  COUNT(st.source_id) AS source_count
               FROM themes t
               LEFT JOIN source_themes st ON t.id = st.theme_id
               GROUP BY t.id, t.name, t.velocity
               ORDER BY t.velocity DESC NULLS LAST, COUNT(st.source_id) ASC"""
        ).fetchall()


# ---------------------------------------------------------------------------
# Belief system queries (Phase 4)
# ---------------------------------------------------------------------------

def get_beliefs_for_synthesis(topic: str) -> dict:
    """Get beliefs and landscape context for topic-scoped synthesis.

    Matches topic against theme names/IDs and returns all active beliefs
    for matching themes along with their landscape context.

    Args:
        topic: Theme name, ID, or keyword to match.

    Returns:
        Dict with beliefs, themes, state_summaries, recent_breakthroughs,
        and belief_tensions.
    """
    with db.get_conn() as conn:
        # Find matching themes
        themes = conn.execute(
            """SELECT * FROM themes
               WHERE id = %s OR name ILIKE %s OR name ILIKE %s
               ORDER BY velocity DESC NULLS LAST""",
            (topic, f"%{topic}%", topic),
        ).fetchall()

        if not themes:
            return {"beliefs": [], "themes": [], "state_summaries": [],
                    "recent_breakthroughs": [], "belief_tensions": []}

        theme_ids = [t["id"] for t in themes]

        # Get beliefs for these themes
        beliefs = conn.execute(
            """SELECT b.*, t.name AS theme_name
               FROM beliefs b
               LEFT JOIN themes t ON b.domain_theme_id = t.id
               WHERE b.status = 'active'
                 AND b.domain_theme_id = ANY(%s)
               ORDER BY b.confidence DESC""",
            (theme_ids,),
        ).fetchall()

        # Get state summaries
        state_summaries = [
            {"theme_id": t["id"], "theme_name": t["name"],
             "summary": t.get("state_summary"), "velocity": t.get("velocity")}
            for t in themes if t.get("state_summary")
        ]

        # Get recent breakthroughs with significance-scaled window
        max_window = max(BREAKTHROUGH_WINDOW_DAYS.values())
        breakthroughs = conn.execute(
            """SELECT b.*, t.name AS theme_name
               FROM breakthroughs b
               JOIN themes t ON b.theme_id = t.id
               WHERE b.theme_id = ANY(%s)
                 AND b.detected_at >= NOW() - make_interval(days => %s)
               ORDER BY b.detected_at DESC""",
            (theme_ids, max_window),
        ).fetchall()

    return {
        "beliefs": beliefs,
        "themes": themes,
        "state_summaries": state_summaries,
        "recent_breakthroughs": breakthroughs,
    }


def get_belief_coverage_gaps() -> dict:
    """Get belief-driven coverage gaps for /gaps extension.

    Returns:
        Dict with low_confidence_gaps (low-confidence beliefs with thin coverage)
        and unchallenged_beliefs (high-confidence with no counter-evidence).
    """
    low_confidence = db.get_low_confidence_beliefs(threshold=0.5)
    unchallenged = db.get_unchallenged_beliefs(min_confidence=0.8)

    # Enrich low-confidence beliefs with source recency
    enriched_low = []
    with db.get_conn() as conn:
        for belief in low_confidence:
            theme_id = belief.get("domain_theme_id")
            if not theme_id:
                enriched_low.append({**belief, "recent_source_count": 0, "days_since_last_source": None})
                continue
            row = conn.execute(
                """SELECT COUNT(*) AS cnt,
                      EXTRACT(DAY FROM NOW() - MAX(s.ingested_at))::int AS days_ago
                   FROM source_themes st
                   JOIN sources s ON st.source_id = s.id
                   WHERE st.theme_id = %s
                     AND s.ingested_at >= NOW() - INTERVAL '30 days'""",
                (theme_id,),
            ).fetchone()
            enriched_low.append({
                **belief,
                "recent_source_count": row["cnt"] if row else 0,
                "days_since_last_source": row["days_ago"] if row else None,
            })

    return {
        "low_confidence_gaps": enriched_low,
        "unchallenged_beliefs": unchallenged,
    }


def get_predictive_beliefs_without_anticipations() -> list[dict]:
    """Get predictive beliefs that have no derived anticipations.

    These are beliefs that should generate testable predictions but haven't yet.
    """
    with db.get_conn() as conn:
        return conn.execute(
            """SELECT b.*, t.name AS theme_name
               FROM beliefs b
               LEFT JOIN themes t ON b.domain_theme_id = t.id
               WHERE b.status = 'active'
                 AND b.belief_type = 'predictive'
                 AND b.confidence >= 0.6
                 AND (b.derived_anticipations IS NULL
                      OR jsonb_array_length(b.derived_anticipations) = 0)
               ORDER BY b.confidence DESC"""
        ).fetchall()


# ---------------------------------------------------------------------------
# Temporal trends (for /trends page)
# ---------------------------------------------------------------------------

VALID_SOURCE_TYPES = {"paper", "article", "video", "podcast"}


def get_temporal_trends(
    start: datetime, end: datetime, source_type: str | None = None
) -> dict:
    """Aggregate theme activity, breakthroughs, capabilities, limitations,
    and anticipation updates over [start, end], optionally scoped to a
    source type."""

    with db.get_conn() as conn:
        if source_type:
            active_theme_ids = [
                row["theme_id"]
                for row in conn.execute(
                    """SELECT DISTINCT st.theme_id
                       FROM source_themes st
                       JOIN sources s ON st.source_id = s.id
                       WHERE s.ingested_at >= %s
                         AND s.ingested_at <= %s
                         AND s.source_type = %s""",
                    (start, end, source_type),
                ).fetchall()
            ]
        else:
            active_theme_ids = []

        theme_filter_sql = ""
        theme_filter_params: list = []
        if source_type:
            if not active_theme_ids:
                period_days = max((end - start).days, 1)
                return {
                    "period": {"start": start.isoformat(), "end": end.isoformat()},
                    "source_type": source_type,
                    "summary": {
                        "total_sources": 0,
                        "total_breakthroughs": 0,
                        "total_new_capabilities": 0,
                        "total_new_limitations": 0,
                        "themes_active": 0,
                    },
                    "narrative": _build_trend_narrative([], [], [], [], [], 0, period_days, source_type),
                    "theme_activity": [],
                    "breakthroughs": [],
                    "new_capabilities": [],
                    "new_limitations": [],
                    "anticipation_updates": [],
                }
            theme_filter_sql = "WHERE t.id = ANY(%s)"
            theme_filter_params = [active_theme_ids]
        activity_where_sql = theme_filter_sql or "WHERE TRUE"

        # ------------------------------------------------------------------
        # 1. Theme activity aggregation
        # ------------------------------------------------------------------
        source_filter_sql = ""
        source_filter_params: list = [start, end]
        if source_type:
            source_filter_sql = " AND s.source_type = %s"
            source_filter_params.append(source_type)

        q1 = f"""
            WITH period_sources AS (
                SELECT st.theme_id, COUNT(DISTINCT s.id) AS period_source_count
                FROM source_themes st
                JOIN sources s ON st.source_id = s.id
                WHERE s.ingested_at >= %s
                  AND s.ingested_at <= %s
                  {source_filter_sql}
                GROUP BY st.theme_id
            ),
            period_breakthroughs AS (
                SELECT theme_id, COUNT(*) AS period_breakthrough_count
                FROM breakthroughs
                WHERE detected_at >= %s
                  AND detected_at <= %s
                GROUP BY theme_id
            ),
            period_capabilities AS (
                SELECT theme_id, COUNT(*) AS period_capability_count
                FROM capabilities
                WHERE last_updated >= %s
                  AND last_updated <= %s
                GROUP BY theme_id
            ),
            period_limitations AS (
                SELECT theme_id, COUNT(*) AS period_limitation_count
                FROM limitations
                WHERE last_updated >= %s
                  AND last_updated <= %s
                GROUP BY theme_id
            ),
            total_theme_sources AS (
                SELECT theme_id, COUNT(DISTINCT source_id) AS total_sources
                FROM source_themes
                GROUP BY theme_id
            )
            SELECT
                t.id,
                t.name,
                t.velocity,
                t.created_at AS theme_created_at,
                COALESCE(ps.period_source_count, 0) AS period_source_count,
                COALESCE(pb.period_breakthrough_count, 0) AS period_breakthrough_count,
                COALESCE(pc.period_capability_count, 0) AS period_capability_count,
                COALESCE(pl.period_limitation_count, 0) AS period_limitation_count,
                COALESCE(ts.total_sources, 0) AS total_sources
            FROM themes t
            LEFT JOIN period_sources ps ON ps.theme_id = t.id
            LEFT JOIN period_breakthroughs pb ON pb.theme_id = t.id
            LEFT JOIN period_capabilities pc ON pc.theme_id = t.id
            LEFT JOIN period_limitations pl ON pl.theme_id = t.id
            LEFT JOIN total_theme_sources ts ON ts.theme_id = t.id
            {activity_where_sql}
            AND (
                COALESCE(ps.period_source_count, 0)
                + COALESCE(pb.period_breakthrough_count, 0)
                + COALESCE(pc.period_capability_count, 0)
                + COALESCE(pl.period_limitation_count, 0)
            ) > 0
            ORDER BY
                (COALESCE(pb.period_breakthrough_count, 0) * 3)
                + COALESCE(ps.period_source_count, 0)
                + COALESCE(pc.period_capability_count, 0)
                + COALESCE(pl.period_limitation_count, 0) DESC,
                t.name ASC
        """
        q1_params = (
            source_filter_params
            + [start, end]
            + [start, end]
            + [start, end]
            + theme_filter_params
        )
        theme_activity_rows = conn.execute(q1, q1_params).fetchall()

        # ------------------------------------------------------------------
        # 2. Breakthroughs in period
        # ------------------------------------------------------------------
        q2 = f"""
            SELECT br.*, t.name AS theme_name
            FROM breakthroughs br
            JOIN themes t ON br.theme_id = t.id
            WHERE br.detected_at >= %s AND br.detected_at <= %s
            {f"AND t.id = ANY(%s)" if source_type else ""}
            ORDER BY br.detected_at DESC
        """
        q2_params = [start, end] + theme_filter_params
        breakthroughs = conn.execute(q2, q2_params).fetchall()

        # ------------------------------------------------------------------
        # 3. New capabilities in period
        # ------------------------------------------------------------------
        q3 = f"""
            SELECT c.*, t.name AS theme_name
            FROM capabilities c
            JOIN themes t ON c.theme_id = t.id
            WHERE c.last_updated >= %s AND c.last_updated <= %s
            {f"AND t.id = ANY(%s)" if source_type else ""}
            ORDER BY c.last_updated DESC
        """
        q3_params = [start, end] + theme_filter_params
        new_capabilities = conn.execute(q3, q3_params).fetchall()

        # ------------------------------------------------------------------
        # 4. New limitations in period
        # ------------------------------------------------------------------
        q4 = f"""
            SELECT l.*, t.name AS theme_name
            FROM limitations l
            JOIN themes t ON l.theme_id = t.id
            WHERE l.last_updated >= %s AND l.last_updated <= %s
            {f"AND t.id = ANY(%s)" if source_type else ""}
            ORDER BY l.last_updated DESC
        """
        q4_params = [start, end] + theme_filter_params
        new_limitations = conn.execute(q4, q4_params).fetchall()

        # ------------------------------------------------------------------
        # 5. Anticipation updates in period
        # ------------------------------------------------------------------
        q5 = f"""
            SELECT a.*, t.name AS theme_name,
                   jsonb_array_length(COALESCE(a.status_evidence, '[]'::jsonb)) AS evidence_count
            FROM anticipations a
            JOIN themes t ON a.theme_id = t.id
            WHERE (
                (a.last_reviewed >= %s AND a.last_reviewed <= %s)
                OR (a.status != 'open' AND a.created_at >= %s AND a.created_at <= %s)
            )
            {f"AND t.id = ANY(%s)" if source_type else ""}
            ORDER BY a.last_reviewed DESC NULLS LAST
        """
        q5_params = [start, end, start, end] + theme_filter_params
        anticipation_updates = conn.execute(q5, q5_params).fetchall()

        # ------------------------------------------------------------------
        # 6. Total source count in period
        # ------------------------------------------------------------------
        q6_where = "WHERE s.ingested_at >= %s AND s.ingested_at <= %s"
        q6_params_list: list = [start, end]
        if source_type:
            q6_where += " AND s.source_type = %s"
            q6_params_list.append(source_type)
        total_row = conn.execute(
            f"SELECT COUNT(*) AS cnt FROM sources s {q6_where}",
            q6_params_list,
        ).fetchone()
        total_sources = total_row["cnt"] if total_row else 0

    # ------------------------------------------------------------------
    # Post-processing: acceleration per theme
    # ------------------------------------------------------------------
    period_days = max((end - start).days, 1)
    now = datetime.now(timezone.utc)

    theme_activity = []
    for row in theme_activity_rows:
        total = row["total_sources"] or 0
        period_count = row["period_source_count"] or 0
        theme_created = row.get("theme_created_at")

        period_rate = period_count / period_days

        theme_age_days = 1
        if theme_created:
            if hasattr(theme_created, "tzinfo") and theme_created.tzinfo is None:
                theme_created = theme_created.replace(tzinfo=timezone.utc)
            theme_age_days = max((now - theme_created).days, 1)

        historical_rate = total / theme_age_days if total else 0
        if historical_rate > 0:
            accel = period_rate / historical_rate
        else:
            accel = 2.0 if period_count > 0 else 1.0

        if accel > 1.5:
            accel_label = "accelerating"
        elif accel < 0.5:
            accel_label = "decelerating"
        else:
            accel_label = "steady"

        theme_activity.append({
            "id": row["id"],
            "name": row["name"],
            "velocity": row["velocity"],
            "period_source_count": period_count,
            "period_breakthrough_count": row["period_breakthrough_count"] or 0,
            "period_capability_count": row["period_capability_count"] or 0,
            "period_limitation_count": row["period_limitation_count"] or 0,
            "total_sources": total,
            "acceleration": accel_label,
        })

    # Build narrative
    narrative = _build_trend_narrative(
        theme_activity, breakthroughs, new_capabilities,
        new_limitations, anticipation_updates, total_sources,
        period_days, source_type,
    )

    return {
        "period": {"start": start.isoformat(), "end": end.isoformat()},
        "source_type": source_type,
        "summary": {
            "total_sources": total_sources,
            "total_breakthroughs": len(breakthroughs),
            "total_new_capabilities": len(new_capabilities),
            "total_new_limitations": len(new_limitations),
            "themes_active": len(theme_activity),
        },
        "narrative": narrative,
        "theme_activity": theme_activity,
        "breakthroughs": breakthroughs,
        "new_capabilities": new_capabilities,
        "new_limitations": new_limitations,
        "anticipation_updates": anticipation_updates,
    }


def _build_trend_narrative(
    theme_activity: list[dict],
    breakthroughs: list,
    new_capabilities: list,
    new_limitations: list,
    anticipation_updates: list,
    total_sources: int,
    period_days: int,
    source_type: str | None,
) -> list[str]:
    """Generate template-based narrative summary lines."""
    lines: list[str] = []
    type_label = f" {source_type}" if source_type else ""
    active = len(theme_activity)

    # Period label
    if period_days <= 7:
        period_label = "the past week"
    elif period_days <= 31:
        period_label = "the past month"
    elif period_days <= 93:
        period_label = "the past 3 months"
    elif period_days <= 183:
        period_label = "the past 6 months"
    else:
        period_label = f"the past {period_days} days"

    lines.append(
        f"Over {period_label}, you ingested {total_sources}{type_label} "
        f"source{'s' if total_sources != 1 else ''} across {active} active "
        f"theme{'s' if active != 1 else ''}."
    )

    if breakthroughs:
        sig_counts: dict[str, int] = {}
        for b in breakthroughs:
            sig = b.get("significance") or "incremental"
            sig_counts[sig] = sig_counts.get(sig, 0) + 1
        breakdown = ", ".join(f"{v} {k}" for k, v in sig_counts.items())
        lines.append(
            f"{len(breakthroughs)} breakthrough{'s' if len(breakthroughs) != 1 else ''} "
            f"detected: {breakdown}."
        )

    accelerating = [t["name"] for t in theme_activity if t["acceleration"] == "accelerating"]
    decelerating = [t["name"] for t in theme_activity if t["acceleration"] == "decelerating"]
    if accelerating:
        lines.append(f"Accelerating themes: {', '.join(accelerating[:5])}.")
    if decelerating:
        lines.append(f"Decelerating themes: {', '.join(decelerating[:5])}.")

    confirmed = [
        a for a in anticipation_updates
        if a.get("status") in ("confirmed", "partially_confirmed")
    ]
    if confirmed:
        lines.append(
            f"{len(confirmed)} anticipation{'s' if len(confirmed) != 1 else ''} "
            f"confirmed in this period."
        )

    if new_capabilities:
        lines.append(f"{len(new_capabilities)} new capabilities discovered.")
    if new_limitations:
        lines.append(f"{len(new_limitations)} new limitations identified.")

    return lines
