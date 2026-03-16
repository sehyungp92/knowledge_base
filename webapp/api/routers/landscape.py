"""Landscape API router -- theme state, briefings, contributions, changelog."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timedelta, timezone
from threading import Lock
from time import monotonic

from fastapi import APIRouter, HTTPException, Query

from reading_app import db
from retrieval import landscape

router = APIRouter(prefix="/api/landscape", tags=["landscape"])

_BRIEFING_BREAKTHROUGH_LIMIT = 20
_BRIEFING_SIGNAL_LIMIT = 12
_TRENDS_BREAKTHROUGH_LIMIT = 40
_TRENDS_ENTITY_LIMIT = 120
_TRENDS_ANTICIPATION_LIMIT = 40
_BRIEFING_CACHE_TTL_SECONDS = 300
_THEME_PREVIEW_LIMIT = 4
_THEME_SECTION_DEFAULT_LIMIT = 12
_THEME_SECTION_MAX_LIMIT = 50

_SEVERITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}
_SIGNIFICANCE_ORDER = {
    "paradigm_shifting": 0,
    "major": 1,
    "notable": 2,
    "incremental": 3,
}
_MATURITY_ORDER = {
    "mature": 0,
    "developing": 1,
    "emerging": 2,
}

_briefing_cache_lock = Lock()
_briefing_cache: dict[str, object] = {
    "payload": None,
    "generated_at": None,
    "expires_at": 0.0,
}


def _briefing_theme_activity() -> list[dict]:
    """Return persisted theme velocity plus source-count rollups for briefing cards."""
    with db.get_conn() as conn:
        return conn.execute(
            """SELECT
                   t.id,
                   t.name,
                   COALESCE(t.velocity, 0) AS velocity,
                   COUNT(DISTINCT st.source_id) AS total_sources,
                   COUNT(DISTINCT st.source_id) FILTER (
                       WHERE s.ingested_at >= NOW() - make_interval(days => COALESCE(t.velocity_window_days, 90))
                   ) AS recent_sources
               FROM themes t
               LEFT JOIN source_themes st ON t.id = st.theme_id
               LEFT JOIN sources s ON st.source_id = s.id
               GROUP BY t.id, t.name, t.velocity, t.velocity_window_days
               ORDER BY COALESCE(t.velocity, 0) DESC, recent_sources DESC, total_sources ASC"""
        ).fetchall()


def _build_briefing_payload(since_dt: datetime | None) -> dict:
    """Build the landscape briefing payload from lightweight queries."""
    recent_sources = db.list_sources(limit=20)
    if since_dt:
        recent_sources = [
            s for s in recent_sources
            if s.get("ingested_at") and s["ingested_at"] >= since_dt
        ]

    breakthroughs = landscape.get_recent_breakthroughs(30)[:_BRIEFING_BREAKTHROUGH_LIMIT]

    stale_beliefs: list[dict] = []
    try:
        stale_beliefs = db.get_stale_beliefs()[:_BRIEFING_SIGNAL_LIMIT]
    except Exception:
        pass

    anticipations_with_evidence = landscape.get_anticipations_with_evidence()[:_BRIEFING_SIGNAL_LIMIT]
    over_optimistic = landscape.get_over_optimistic_themes()[:_BRIEFING_SIGNAL_LIMIT]
    blind_spots = landscape.get_blind_spot_bottlenecks()[:_BRIEFING_SIGNAL_LIMIT]

    theme_activity = _briefing_theme_activity()
    highest_movement = [
        {
            "id": theme["id"],
            "name": theme["name"],
            "velocity": theme.get("velocity") or 0,
            "recent_sources": theme.get("recent_sources") or 0,
            "total_sources": theme.get("total_sources") or 0,
        }
        for theme in theme_activity[:5]
    ]
    reading_recs = [
        {
            "id": theme["id"],
            "name": theme["name"],
            "source_count": theme.get("total_sources") or 0,
        }
        for theme in theme_activity
        if (theme.get("velocity") or 0) > 0.3 and (theme.get("total_sources") or 0) < 5
    ][: _BRIEFING_SIGNAL_LIMIT]

    return {
        "recent_sources": recent_sources,
        "breakthroughs": breakthroughs,
        "attention_signals": {
            "stale_beliefs": stale_beliefs,
            "anticipations_with_evidence": anticipations_with_evidence,
            "over_optimistic_themes": over_optimistic,
            "blind_spot_bottlenecks": blind_spots,
        },
        "highest_movement": highest_movement,
        "reading_recommendations": reading_recs,
    }


def _get_cached_briefing() -> tuple[dict | None, str | None]:
    """Return a defensive copy of the cached briefing if it is still fresh."""
    with _briefing_cache_lock:
        payload = _briefing_cache.get("payload")
        expires_at = _briefing_cache.get("expires_at", 0.0) or 0.0
        generated_at = _briefing_cache.get("generated_at")
        if payload is None or monotonic() >= expires_at:
            return None, None
        return deepcopy(payload), str(generated_at) if generated_at else None


def _store_cached_briefing(payload: dict) -> str:
    """Persist the latest briefing payload in a short-lived in-memory cache."""
    generated_at = datetime.now(timezone.utc).isoformat()
    with _briefing_cache_lock:
        _briefing_cache["payload"] = deepcopy(payload)
        _briefing_cache["generated_at"] = generated_at
        _briefing_cache["expires_at"] = monotonic() + _BRIEFING_CACHE_TTL_SECONDS
    return generated_at


def _importance_label(theme: dict) -> str:
    """Convert a theme velocity into a short editorial label."""
    velocity = theme.get("velocity") or 0
    if velocity >= 0.75:
        return "fast-moving"
    if velocity >= 0.4:
        return "active"
    return "stable"


def _limitation_sort_key(item: dict) -> tuple[int, str]:
    return (_SEVERITY_ORDER.get((item.get("severity") or "").lower(), 99), item.get("description", ""))


def _breakthrough_sort_key(item: dict) -> tuple[int, str]:
    return (_SIGNIFICANCE_ORDER.get((item.get("significance") or "").lower(), 99), item.get("description", ""))


def _capability_sort_key(item: dict) -> tuple[int, str]:
    return (_MATURITY_ORDER.get((item.get("maturity") or "").lower(), 99), item.get("description", ""))


def _theme_exists(theme_id: str) -> dict:
    """Load a theme row or raise a 404."""
    with db.get_conn() as conn:
        theme = conn.execute(
            """SELECT id, name, description, velocity, state_summary
               FROM themes WHERE id = %s""",
            (theme_id,),
        ).fetchone()
    if not theme:
        raise HTTPException(status_code=404, detail=f"Theme '{theme_id}' not found")
    return theme


def _fetch_theme_counts(theme_id: str) -> dict:
    """Collect section counts for the theme detail page without loading full arrays."""
    like_pattern = f"%{theme_id}%"
    with db.get_conn() as conn:
        row = conn.execute(
            """SELECT
                   (SELECT COUNT(*) FROM source_themes WHERE theme_id = %s) AS source_count,
                   (SELECT COUNT(*) FROM capabilities WHERE theme_id = %s) AS capability_count,
                   (SELECT COUNT(*) FROM limitations WHERE theme_id = %s) AS limitation_count,
                   (SELECT COUNT(*) FROM bottlenecks WHERE theme_id = %s) AS bottleneck_count,
                   (SELECT COUNT(*) FROM breakthroughs WHERE theme_id = %s) AS breakthrough_count,
                   (SELECT COUNT(*) FROM anticipations WHERE theme_id = %s AND status = 'open') AS anticipation_count,
                   (SELECT COUNT(*) FROM cross_theme_implications WHERE source_theme_id = %s) AS implication_out_count,
                   (SELECT COUNT(*) FROM cross_theme_implications WHERE target_theme_id = %s) AS implication_in_count,
                   (SELECT COUNT(*) FROM beliefs WHERE domain_theme_id = %s AND status = 'active') AS belief_count,
                   (SELECT COUNT(*) FROM ideas
                      WHERE novelty_check_passed = TRUE
                        AND grounding::text LIKE %s) AS idea_count,
                   (SELECT COUNT(*) FROM challenge_log
                      WHERE entity_type = 'theme' AND entity_id = %s) AS challenge_count""",
            (
                theme_id,
                theme_id,
                theme_id,
                theme_id,
                theme_id,
                theme_id,
                theme_id,
                theme_id,
                theme_id,
                like_pattern,
                theme_id,
            ),
        ).fetchone()

    return {
        "sources": row["source_count"] if row else 0,
        "capabilities": row["capability_count"] if row else 0,
        "limitations": row["limitation_count"] if row else 0,
        "bottlenecks": row["bottleneck_count"] if row else 0,
        "breakthroughs": row["breakthrough_count"] if row else 0,
        "anticipations": row["anticipation_count"] if row else 0,
        "implications_out": row["implication_out_count"] if row else 0,
        "implications_in": row["implication_in_count"] if row else 0,
        "beliefs": row["belief_count"] if row else 0,
        "ideas": row["idea_count"] if row else 0,
        "challenges": row["challenge_count"] if row else 0,
    }


def _fetch_theme_previews(theme_id: str) -> dict:
    """Fetch small preview slices for the layered theme detail page."""
    implication_rows = landscape.get_consolidated_implications(theme_id, limit=8)
    outgoing = [row for row in implication_rows if row["source_theme_id"] == theme_id][: _THEME_PREVIEW_LIMIT]
    incoming = [row for row in implication_rows if row["target_theme_id"] == theme_id][: _THEME_PREVIEW_LIMIT]

    with db.get_conn() as conn:
        capabilities = conn.execute(
            """SELECT id, description, maturity, attribution
               FROM capabilities
               WHERE theme_id = %s
               ORDER BY confidence DESC NULLS LAST, last_updated DESC NULLS LAST
               LIMIT %s""",
            (theme_id, _THEME_PREVIEW_LIMIT),
        ).fetchall()
        limitations = conn.execute(
            """SELECT id, description, limitation_type, severity, trajectory, attribution, bottleneck_id
               FROM limitations
               WHERE theme_id = %s
               ORDER BY confidence DESC NULLS LAST, last_updated DESC NULLS LAST
               LIMIT %s""",
            (theme_id, _THEME_PREVIEW_LIMIT),
        ).fetchall()
        bottlenecks = conn.execute(
            """SELECT id, description, resolution_horizon, active_approaches, attribution
               FROM bottlenecks
               WHERE theme_id = %s
               ORDER BY confidence DESC NULLS LAST, last_updated DESC NULLS LAST
               LIMIT %s""",
            (theme_id, _THEME_PREVIEW_LIMIT),
        ).fetchall()
        breakthroughs = conn.execute(
            """SELECT id, description, significance, attribution
               FROM breakthroughs
               WHERE theme_id = %s
               ORDER BY detected_at DESC
               LIMIT %s""",
            (theme_id, _THEME_PREVIEW_LIMIT),
        ).fetchall()
        anticipations = conn.execute(
            """SELECT id, prediction, confidence, timeline, status,
                      jsonb_array_length(COALESCE(status_evidence, '[]'::jsonb)) AS evidence_count
               FROM anticipations
               WHERE theme_id = %s AND status = 'open'
               ORDER BY confidence DESC NULLS LAST
               LIMIT %s""",
            (theme_id, _THEME_PREVIEW_LIMIT),
        ).fetchall()
        authoritative_sources = conn.execute(
            """SELECT s.id, s.title, gm.score AS influence_score
               FROM source_themes st
               JOIN sources s ON st.source_id = s.id
               LEFT JOIN graph_metrics gm
                 ON gm.entity_id = s.id
                 AND gm.metric_type = 'pagerank'
                 AND gm.entity_type = 'source'
               WHERE st.theme_id = %s
               ORDER BY COALESCE(gm.score, 0) DESC, s.ingested_at DESC
               LIMIT %s""",
            (theme_id, _THEME_PREVIEW_LIMIT + 1),
        ).fetchall()

    capabilities = sorted(capabilities, key=_capability_sort_key)
    limitations = sorted(limitations, key=_limitation_sort_key)
    breakthroughs = sorted(breakthroughs, key=_breakthrough_sort_key)

    return {
        "capabilities": capabilities,
        "limitations": limitations,
        "bottlenecks": bottlenecks,
        "breakthroughs": breakthroughs,
        "anticipations": anticipations,
        "implications_out": outgoing,
        "implications_in": incoming,
        "authoritative_sources": authoritative_sources,
    }


def _build_theme_overview(theme: dict, counts: dict, previews: dict) -> dict:
    """Create an editorial summary layer from compact preview data."""
    top_takeaways: list[dict] = []
    key_tensions: list[dict] = []
    strongest_evidence: list[dict] = []

    if theme.get("state_summary"):
        top_takeaways.append({
            "label": "State of play",
            "text": str(theme["state_summary"]).strip(),
        })

    top_takeaways.append({
        "label": "Momentum",
        "text": (
            f"{theme['name']} is {_importance_label(theme)} with velocity "
            f"{(theme.get('velocity') or 0):.2f} across {counts['sources']} linked sources."
        ),
    })

    if previews["capabilities"]:
        capability = previews["capabilities"][0]
        top_takeaways.append({
            "label": "Leading capability",
            "text": capability["description"],
        })

    blocker = previews["limitations"][0] if previews["limitations"] else None
    if blocker:
        top_takeaways.append({
            "label": "Main limitation",
            "text": blocker["description"],
        })
    elif previews["bottlenecks"]:
        top_takeaways.append({
            "label": "Main bottleneck",
            "text": previews["bottlenecks"][0]["description"],
        })

    if previews["capabilities"] and previews["limitations"]:
        key_tensions.append({
            "label": "Capability vs reliability",
            "text": (
                f"{previews['capabilities'][0]['description']} "
                f"but {previews['limitations'][0]['description']}"
            ),
        })
    if previews["breakthroughs"] and previews["bottlenecks"]:
        key_tensions.append({
            "label": "Progress vs blocker",
            "text": (
                f"{previews['breakthroughs'][0]['description']} "
                f"while {previews['bottlenecks'][0]['description']} remains unresolved."
            ),
        })
    if previews["anticipations"]:
        anticipation = previews["anticipations"][0]
        key_tensions.append({
            "label": "Still unresolved",
            "text": anticipation["prediction"],
        })
    if not key_tensions and previews["implications_out"]:
        implication = previews["implications_out"][0]
        key_tensions.append({
            "label": "Downstream effect",
            "text": implication["top_implication"],
        })

    if previews["breakthroughs"]:
        breakthrough = previews["breakthroughs"][0]
        strongest_evidence.append({
            "label": "Breakthrough",
            "text": breakthrough["description"],
            "meta": breakthrough.get("significance") or "recent",
        })
    if previews["authoritative_sources"]:
        source = previews["authoritative_sources"][0]
        strongest_evidence.append({
            "label": "Key source",
            "text": source["title"],
            "meta": f"Influence {source.get('influence_score', 0):.4f}" if source.get("influence_score") else "Top-ranked source",
            "href": f"/library/{source['id']}",
        })
    if previews["implications_in"]:
        implication = previews["implications_in"][0]
        strongest_evidence.append({
            "label": "Cross-theme pressure",
            "text": implication["top_implication"],
            "meta": implication["source_theme"],
            "href": f"/landscape/{implication['source_theme_id']}",
        })

    return {
        "top_takeaways": top_takeaways[:4],
        "key_tensions": key_tensions[:3],
        "strongest_evidence": strongest_evidence[:3],
    }


def _source_ids_from_evidence(items: list[dict], *, breakthrough: bool = False) -> list[str]:
    """Collect unique source IDs from evidence JSON fields."""
    source_ids: set[str] = set()
    for item in items:
        if breakthrough:
            primary_source_id = item.get("primary_source_id")
            if primary_source_id:
                source_ids.add(primary_source_id)
            corroborating_sources = item.get("corroborating_sources")
            if isinstance(corroborating_sources, list):
                for candidate in corroborating_sources:
                    source_id = None
                    if isinstance(candidate, dict):
                        source_id = candidate.get("source_id")
                    elif isinstance(candidate, str):
                        source_id = candidate
                    if source_id:
                        source_ids.add(source_id)
            continue

        evidence_sources = item.get("evidence_sources")
        if not isinstance(evidence_sources, list):
            continue
        for candidate in evidence_sources:
            source_id = None
            if isinstance(candidate, dict):
                source_id = candidate.get("source_id")
            elif isinstance(candidate, str):
                source_id = candidate
            if source_id:
                source_ids.add(source_id)
    return list(source_ids)


def _resolve_source_titles(source_ids: list[str]) -> dict[str, str]:
    """Resolve source IDs into titles for evidence footers."""
    if not source_ids:
        return {}
    with db.get_conn() as conn:
        rows = conn.execute(
            "SELECT id, title FROM sources WHERE id = ANY(%s)",
            (source_ids,),
        ).fetchall()
    return {row["id"]: row["title"] for row in rows}


def _attach_resolved_sources(items: list[dict], *, breakthrough: bool = False) -> list[dict]:
    """Inject a compact resolved_sources array into evidence-backed items."""
    source_lookup = _resolve_source_titles(_source_ids_from_evidence(items, breakthrough=breakthrough))
    for item in items:
        resolved_sources = []
        if breakthrough:
            primary_source_id = item.get("primary_source_id")
            if primary_source_id and primary_source_id in source_lookup:
                resolved_sources.append({"id": primary_source_id, "title": source_lookup[primary_source_id]})
            corroborating_sources = item.get("corroborating_sources")
            if isinstance(corroborating_sources, list):
                for candidate in corroborating_sources:
                    source_id = candidate.get("source_id") if isinstance(candidate, dict) else candidate if isinstance(candidate, str) else None
                    if source_id and source_id in source_lookup and source_id != primary_source_id:
                        resolved_sources.append({"id": source_id, "title": source_lookup[source_id]})
        else:
            evidence_sources = item.get("evidence_sources")
            if isinstance(evidence_sources, list):
                for candidate in evidence_sources:
                    source_id = candidate.get("source_id") if isinstance(candidate, dict) else candidate if isinstance(candidate, str) else None
                    if source_id and source_id in source_lookup:
                        resolved_sources.append({"id": source_id, "title": source_lookup[source_id]})
        item["resolved_sources"] = resolved_sources
    return items


@router.get("/briefing")
def briefing(
    since: str | None = Query(None, description="ISO timestamp to filter recent items"),
    refresh: bool = Query(False, description="Bypass the cached default briefing"),
):
    """Aggregate briefing from landscape queries with a short-lived cache."""
    if not isinstance(since, str):
        since = None
    if not isinstance(refresh, bool):
        refresh = False

    since_dt: datetime | None = None
    if since:
        try:
            since_dt = datetime.fromisoformat(since)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ISO timestamp for 'since'")

    cache_hit = False
    generated_at: str | None = None
    payload: dict

    if since_dt is None and not refresh:
        payload, generated_at = _get_cached_briefing()
        cache_hit = payload is not None
    else:
        payload = None

    if payload is None:
        payload = _build_briefing_payload(since_dt)
        generated_at = _store_cached_briefing(payload) if since_dt is None else datetime.now(timezone.utc).isoformat()

    return {
        **payload,
        "meta": {
            "cached": cache_hit,
            "generated_at": generated_at,
            "cache_ttl_seconds": _BRIEFING_CACHE_TTL_SECONDS if since_dt is None else 0,
        },
    }


@router.get("/themes")
def list_themes():
    """List all themes with sub-entity counts and theme edges."""
    with db.get_conn() as conn:
        themes = conn.execute(
            """SELECT t.id, t.name, t.description, t.velocity, t.state_summary,
                  (SELECT COUNT(*) FROM capabilities c WHERE c.theme_id = t.id) AS cap_count,
                  (SELECT COUNT(*) FROM bottlenecks b WHERE b.theme_id = t.id) AS bot_count,
                  (SELECT COUNT(*) FROM anticipations a WHERE a.theme_id = t.id) AS ant_count
               FROM themes t
               ORDER BY t.velocity DESC NULLS LAST"""
        ).fetchall()

        edges = conn.execute(
            "SELECT parent_id, child_id, relationship, strength FROM theme_edges"
        ).fetchall()

    return {"themes": themes, "theme_edges": edges}


@router.get("/themes/{theme_id}/synthesis")
def theme_synthesis(theme_id: str):
    """Compact synthesis overview for a single theme."""
    theme = _theme_exists(theme_id)
    counts = _fetch_theme_counts(theme_id)
    previews = _fetch_theme_previews(theme_id)

    return {
        "theme": theme,
        "counts": counts,
        "overview": _build_theme_overview(theme, counts, previews),
        "previews": previews,
    }


@router.get("/themes/{theme_id}/synthesis/sections/{section}")
def theme_synthesis_section(
    theme_id: str,
    section: str,
    limit: int = Query(_THEME_SECTION_DEFAULT_LIMIT, ge=1, le=_THEME_SECTION_MAX_LIMIT),
    offset: int = Query(0, ge=0),
):
    """Paginated raw detail for a theme synthesis section."""
    _theme_exists(theme_id)
    like_pattern = f"%{theme_id}%"

    with db.get_conn() as conn:
        if section == "capabilities":
            total = conn.execute(
                "SELECT COUNT(*) AS cnt FROM capabilities WHERE theme_id = %s",
                (theme_id,),
            ).fetchone()["cnt"]
            items = conn.execute(
                """SELECT id, description, maturity, attribution, evidence_sources
                   FROM capabilities
                   WHERE theme_id = %s
                   ORDER BY confidence DESC NULLS LAST, last_updated DESC NULLS LAST
                   LIMIT %s OFFSET %s""",
                (theme_id, limit, offset),
            ).fetchall()
            items = _attach_resolved_sources(items)
        elif section == "limitations":
            total = conn.execute(
                "SELECT COUNT(*) AS cnt FROM limitations WHERE theme_id = %s",
                (theme_id,),
            ).fetchone()["cnt"]
            items = conn.execute(
                """SELECT id, description, limitation_type, severity, trajectory,
                          attribution, bottleneck_id, evidence_sources
                   FROM limitations
                   WHERE theme_id = %s
                   ORDER BY confidence DESC NULLS LAST, last_updated DESC NULLS LAST
                   LIMIT %s OFFSET %s""",
                (theme_id, limit, offset),
            ).fetchall()
            items = _attach_resolved_sources(items)
        elif section == "bottlenecks":
            total = conn.execute(
                "SELECT COUNT(*) AS cnt FROM bottlenecks WHERE theme_id = %s",
                (theme_id,),
            ).fetchone()["cnt"]
            items = conn.execute(
                """SELECT id, description, resolution_horizon, active_approaches,
                          attribution, evidence_sources
                   FROM bottlenecks
                   WHERE theme_id = %s
                   ORDER BY confidence DESC NULLS LAST, last_updated DESC NULLS LAST
                   LIMIT %s OFFSET %s""",
                (theme_id, limit, offset),
            ).fetchall()
            items = _attach_resolved_sources(items)
        elif section == "breakthroughs":
            total = conn.execute(
                "SELECT COUNT(*) AS cnt FROM breakthroughs WHERE theme_id = %s",
                (theme_id,),
            ).fetchone()["cnt"]
            items = conn.execute(
                """SELECT id, description, significance, attribution,
                          primary_source_id, corroborating_sources, bottlenecks_affected
                   FROM breakthroughs
                   WHERE theme_id = %s
                   ORDER BY detected_at DESC
                   LIMIT %s OFFSET %s""",
                (theme_id, limit, offset),
            ).fetchall()
            items = _attach_resolved_sources(items, breakthrough=True)
        elif section == "anticipations":
            total = conn.execute(
                "SELECT COUNT(*) AS cnt FROM anticipations WHERE theme_id = %s AND status = 'open'",
                (theme_id,),
            ).fetchone()["cnt"]
            items = conn.execute(
                """SELECT id, prediction, confidence, timeline, status,
                          jsonb_array_length(COALESCE(status_evidence, '[]'::jsonb)) AS evidence_count
                   FROM anticipations
                   WHERE theme_id = %s AND status = 'open'
                   ORDER BY confidence DESC NULLS LAST
                   LIMIT %s OFFSET %s""",
                (theme_id, limit, offset),
            ).fetchall()
        elif section == "beliefs":
            total = conn.execute(
                "SELECT COUNT(*) AS cnt FROM beliefs WHERE domain_theme_id = %s AND status = 'active'",
                (theme_id,),
            ).fetchone()["cnt"]
            items = conn.execute(
                """SELECT id, claim, confidence, evidence_for, evidence_against
                   FROM beliefs
                   WHERE domain_theme_id = %s AND status = 'active'
                   ORDER BY confidence DESC
                   LIMIT %s OFFSET %s""",
                (theme_id, limit, offset),
            ).fetchall()
        elif section == "ideas":
            total = conn.execute(
                """SELECT COUNT(*) AS cnt
                   FROM ideas
                   WHERE novelty_check_passed = TRUE
                     AND grounding::text LIKE %s""",
                (like_pattern,),
            ).fetchone()["cnt"]
            items = conn.execute(
                """SELECT id, idea_text, overall_score, grounding
                   FROM ideas
                   WHERE novelty_check_passed = TRUE
                     AND grounding::text LIKE %s
                   ORDER BY overall_score DESC NULLS LAST
                   LIMIT %s OFFSET %s""",
                (like_pattern, limit, offset),
            ).fetchall()
        elif section == "implications_out":
            total = conn.execute(
                "SELECT COUNT(*) AS cnt FROM cross_theme_implications WHERE source_theme_id = %s",
                (theme_id,),
            ).fetchone()["cnt"]
            items = conn.execute(
                """SELECT cti.id, cti.implication, cti.confidence, cti.attribution,
                          cti.source_theme_id, cti.target_theme_id,
                          ts.name AS source_theme, tt.name AS target_theme
                   FROM cross_theme_implications cti
                   JOIN themes ts ON cti.source_theme_id = ts.id
                   JOIN themes tt ON cti.target_theme_id = tt.id
                   WHERE cti.source_theme_id = %s
                   ORDER BY cti.confidence DESC NULLS LAST
                   LIMIT %s OFFSET %s""",
                (theme_id, limit, offset),
            ).fetchall()
        elif section == "implications_in":
            total = conn.execute(
                "SELECT COUNT(*) AS cnt FROM cross_theme_implications WHERE target_theme_id = %s",
                (theme_id,),
            ).fetchone()["cnt"]
            items = conn.execute(
                """SELECT cti.id, cti.implication, cti.confidence, cti.attribution,
                          cti.source_theme_id, cti.target_theme_id,
                          ts.name AS source_theme, tt.name AS target_theme
                   FROM cross_theme_implications cti
                   JOIN themes ts ON cti.source_theme_id = ts.id
                   JOIN themes tt ON cti.target_theme_id = tt.id
                   WHERE cti.target_theme_id = %s
                   ORDER BY cti.confidence DESC NULLS LAST
                   LIMIT %s OFFSET %s""",
                (theme_id, limit, offset),
            ).fetchall()
        elif section == "challenges":
            total = conn.execute(
                "SELECT COUNT(*) AS cnt FROM challenge_log WHERE entity_type = 'theme' AND entity_id = %s",
                (theme_id,),
            ).fetchone()["cnt"]
            items = conn.execute(
                """SELECT id, entity_type, entity_id, system_position, outcome, created_at
                   FROM challenge_log
                   WHERE entity_type = 'theme' AND entity_id = %s
                   ORDER BY created_at DESC
                   LIMIT %s OFFSET %s""",
                (theme_id, limit, offset),
            ).fetchall()
        else:
            raise HTTPException(status_code=404, detail=f"Unknown theme synthesis section '{section}'")

    return {
        "section": section,
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + len(items) < total,
    }


@router.get("/themes/{theme_id}/timeline")
def theme_timeline(theme_id: str):
    """Temporal timeline for a theme: landscape signals grouped by month.

    Returns capabilities, limitations, bottlenecks, breakthroughs, source
    ingestions, and landscape_history changes bucketed into calendar months.
    """
    with db.get_conn() as conn:
        # Verify theme exists
        theme = conn.execute(
            "SELECT id, name FROM themes WHERE id = %s", (theme_id,)
        ).fetchone()
        if not theme:
            raise HTTPException(status_code=404, detail=f"Theme '{theme_id}' not found")

        # Capabilities with their last_updated as the temporal anchor
        capabilities = conn.execute(
            """SELECT id, description, maturity, last_updated,
                      TO_CHAR(last_updated, 'YYYY-MM') AS month
               FROM capabilities
               WHERE theme_id = %s
               ORDER BY last_updated DESC""",
            (theme_id,),
        ).fetchall()

        # Limitations
        limitations = conn.execute(
            """SELECT id, description, limitation_type, trajectory, severity,
                      last_updated,
                      TO_CHAR(last_updated, 'YYYY-MM') AS month
               FROM limitations
               WHERE theme_id = %s
               ORDER BY last_updated DESC""",
            (theme_id,),
        ).fetchall()

        # Bottlenecks
        bottlenecks_rows = conn.execute(
            """SELECT id, description, resolution_horizon, bottleneck_type,
                      last_updated,
                      TO_CHAR(last_updated, 'YYYY-MM') AS month
               FROM bottlenecks
               WHERE theme_id = %s
               ORDER BY last_updated DESC""",
            (theme_id,),
        ).fetchall()

        # Breakthroughs (use detected_at as temporal anchor)
        breakthroughs_rows = conn.execute(
            """SELECT id, description, significance, detected_at,
                      TO_CHAR(detected_at, 'YYYY-MM') AS month
               FROM breakthroughs
               WHERE theme_id = %s
               ORDER BY detected_at DESC""",
            (theme_id,),
        ).fetchall()

        # Recent source ingestions for this theme
        sources = conn.execute(
            """SELECT s.id, s.title, s.source_type, s.ingested_at,
                      TO_CHAR(s.ingested_at, 'YYYY-MM') AS month
               FROM source_themes st
               JOIN sources s ON st.source_id = s.id
               WHERE st.theme_id = %s
               ORDER BY s.ingested_at DESC""",
            (theme_id,),
        ).fetchall()

        # Landscape history changes for this theme
        history = conn.execute(
            """SELECT lh.id, lh.entity_type, lh.entity_id, lh.field,
                      lh.old_value, lh.new_value, lh.changed_at,
                      lh.source_id, lh.attribution,
                      TO_CHAR(lh.changed_at, 'YYYY-MM') AS month
               FROM landscape_history lh
               WHERE (lh.entity_type = 'capability' AND lh.entity_id IN (
                   SELECT id FROM capabilities WHERE theme_id = %s))
               OR (lh.entity_type = 'limitation' AND lh.entity_id IN (
                   SELECT id FROM limitations WHERE theme_id = %s))
               OR (lh.entity_type = 'bottleneck' AND lh.entity_id IN (
                   SELECT id FROM bottlenecks WHERE theme_id = %s))
               OR (lh.entity_type = 'anticipation' AND lh.entity_id IN (
                   SELECT id FROM anticipations WHERE theme_id = %s))
               ORDER BY lh.changed_at DESC""",
            (theme_id, theme_id, theme_id, theme_id),
        ).fetchall()

    # Collect all months that appear and build a sorted set
    all_months: set[str] = set()
    for row in capabilities:
        if row.get("month"):
            all_months.add(row["month"])
    for row in limitations:
        if row.get("month"):
            all_months.add(row["month"])
    for row in bottlenecks_rows:
        if row.get("month"):
            all_months.add(row["month"])
    for row in breakthroughs_rows:
        if row.get("month"):
            all_months.add(row["month"])
    for row in sources:
        if row.get("month"):
            all_months.add(row["month"])
    for row in history:
        if row.get("month"):
            all_months.add(row["month"])

    sorted_months = sorted(all_months, reverse=True)

    # Group into month buckets
    months_data = []
    for month in sorted_months:
        months_data.append({
            "month": month,
            "capabilities": [
                {"id": r["id"], "description": r["description"], "maturity": r.get("maturity"), "date": r["last_updated"].isoformat() if r.get("last_updated") else None}
                for r in capabilities if r.get("month") == month
            ],
            "limitations": [
                {"id": r["id"], "description": r["description"], "type": r.get("limitation_type"), "trajectory": r.get("trajectory"), "date": r["last_updated"].isoformat() if r.get("last_updated") else None}
                for r in limitations if r.get("month") == month
            ],
            "bottlenecks": [
                {"id": r["id"], "description": r["description"], "horizon": r.get("resolution_horizon"), "type": r.get("bottleneck_type"), "date": r["last_updated"].isoformat() if r.get("last_updated") else None}
                for r in bottlenecks_rows if r.get("month") == month
            ],
            "breakthroughs": [
                {"id": r["id"], "description": r["description"], "significance": r.get("significance"), "date": r["detected_at"].isoformat() if r.get("detected_at") else None}
                for r in breakthroughs_rows if r.get("month") == month
            ],
            "sources": [
                {"id": r["id"], "title": r["title"], "type": r.get("source_type"), "date": r["ingested_at"].isoformat() if r.get("ingested_at") else None}
                for r in sources if r.get("month") == month
            ],
            "changes": [
                {"id": r["id"], "entity_type": r["entity_type"], "entity_id": r["entity_id"], "field": r["field"], "old_value": r.get("old_value"), "new_value": r.get("new_value"), "date": r["changed_at"].isoformat() if r.get("changed_at") else None}
                for r in history if r.get("month") == month
            ],
        })

    return {
        "theme_id": theme_id,
        "theme_name": theme["name"],
        "months": months_data,
    }


@router.get("/themes/{theme_id}/incoming-implications")
def incoming_implications(theme_id: str):
    """Get cross-theme implications targeting this theme."""
    with db.get_conn() as conn:
        rows = conn.execute(
            """SELECT cti.*, ts.name AS source_theme_name
               FROM cross_theme_implications cti
               JOIN themes ts ON cti.source_theme_id = ts.id
               WHERE cti.target_theme_id = %s
               ORDER BY cti.confidence DESC NULLS LAST""",
            (theme_id,),
        ).fetchall()
    return rows


@router.get("/entity/{entity_type}/{entity_id}/history")
def entity_history(entity_type: str, entity_id: str):
    """Get change history and challenge log for a landscape entity."""
    history = db.get_landscape_history(entity_type, entity_id)

    with db.get_conn() as conn:
        challenges = conn.execute(
            """SELECT * FROM challenge_log
               WHERE entity_type = %s AND entity_id = %s
               ORDER BY created_at DESC""",
            (entity_type, entity_id),
        ).fetchall()

    return {"history": history, "challenges": challenges}


@router.get("/stale")
def stale_entities(
    threshold: float = Query(0.3, ge=0.0, le=1.0),
    limit: int = Query(50, ge=1, le=200),
):
    """Return landscape entities with staleness_score above threshold."""
    entities = db.get_stale_landscape_entities(threshold=threshold, limit=limit)
    # Enrich with theme names
    if entities:
        theme_ids = {e["theme_id"] for e in entities if e.get("theme_id")}
        theme_names: dict[str, str] = {}
        if theme_ids:
            with db.get_conn() as conn:
                rows = conn.execute(
                    "SELECT id, name FROM themes WHERE id = ANY(%s)",
                    (list(theme_ids),),
                ).fetchall()
                theme_names = {r["id"]: r["name"] for r in rows}
        for e in entities:
            e["theme_name"] = theme_names.get(e.get("theme_id", ""), "")
    return {"threshold": threshold, "total": len(entities), "entities": entities}


@router.get("/implications")
def all_implications(
    min_confidence: float = Query(0.0, ge=0.0, le=1.0),
    limit: int = Query(100, ge=1, le=500),
):
    """Return all cross-theme implications with resolved theme names."""
    with db.get_conn() as conn:
        rows = conn.execute(
            """SELECT cti.*,
                      ts.name AS source_theme_name,
                      tt.name AS target_theme_name
               FROM cross_theme_implications cti
               JOIN themes ts ON cti.source_theme_id = ts.id
               JOIN themes tt ON cti.target_theme_id = tt.id
               WHERE cti.confidence >= %s OR cti.confidence IS NULL
               ORDER BY cti.confidence DESC NULLS LAST
               LIMIT %s""",
            (min_confidence, limit),
        ).fetchall()
    return {"total": len(rows), "implications": rows}


@router.get("/contributions")
def contributions():
    """Count human-enrichment contributions across landscape tables."""
    tables = ["capabilities", "limitations", "bottlenecks", "breakthroughs", "anticipations",
              "cross_theme_implications"]
    counts: dict[str, int] = {}
    with db.get_conn() as conn:
        for table in tables:
            row = conn.execute(
                f"SELECT COUNT(*) AS cnt FROM {table} WHERE attribution = 'human_enrichment'"
            ).fetchone()
            counts[table] = row["cnt"] if row else 0
    return {"contributions": counts}


@router.get("/changelog")
def changelog(
    since: str | None = Query(None),
    theme_id: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
):
    """Paginated changelog of landscape_history entries."""
    conditions: list[str] = []
    params: list = []

    if since:
        try:
            datetime.fromisoformat(since)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ISO timestamp for 'since'")
        conditions.append("lh.changed_at >= %s")
        params.append(since)

    if theme_id:
        conditions.append("""(
            (lh.entity_type = 'capability' AND lh.entity_id IN (SELECT id FROM capabilities WHERE theme_id = %s))
            OR (lh.entity_type = 'limitation' AND lh.entity_id IN (SELECT id FROM limitations WHERE theme_id = %s))
            OR (lh.entity_type = 'bottleneck' AND lh.entity_id IN (SELECT id FROM bottlenecks WHERE theme_id = %s))
            OR (lh.entity_type = 'anticipation' AND lh.entity_id IN (SELECT id FROM anticipations WHERE theme_id = %s))
        )""")
        params.extend([theme_id, theme_id, theme_id, theme_id])

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    offset = (page - 1) * page_size
    params.extend([page_size, offset])

    with db.get_conn() as conn:
        rows = conn.execute(
            f"""SELECT lh.* FROM landscape_history lh
                {where}
                ORDER BY lh.changed_at DESC
                LIMIT %s OFFSET %s""",
            params,
        ).fetchall()

    return {"page": page, "page_size": page_size, "entries": rows}


# ---------------------------------------------------------------------------
# Temporal trends
# ---------------------------------------------------------------------------

_PERIOD_DAYS = {"1w": 7, "1m": 30, "3m": 90, "6m": 180, "1y": 365}
_VALID_SOURCE_TYPES = {"paper", "article", "video", "podcast"}


@router.get("/trends")
def trends(
    period: str | None = Query(None, description="1w, 1m, 3m, 6m, 1y"),
    start: str | None = Query(None, description="ISO timestamp"),
    end: str | None = Query(None, description="ISO timestamp"),
    source_type: str | None = Query(None, description="paper, article, video, podcast"),
):
    """Aggregate theme activity over a configurable time window."""
    now = datetime.now(timezone.utc)

    if start and end:
        try:
            start_dt = datetime.fromisoformat(start)
            end_dt = datetime.fromisoformat(end)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ISO timestamp")
    else:
        days = _PERIOD_DAYS.get(period or "3m")
        if days is None:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid period. Use one of: {', '.join(_PERIOD_DAYS)}",
            )
        end_dt = now
        start_dt = now - timedelta(days=days)

    if source_type and source_type not in _VALID_SOURCE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid source_type. Use one of: {', '.join(_VALID_SOURCE_TYPES)}",
        )

    trends_data = landscape.get_temporal_trends(start_dt, end_dt, source_type=source_type)
    trends_data["breakthroughs"] = trends_data["breakthroughs"][:_TRENDS_BREAKTHROUGH_LIMIT]
    trends_data["new_capabilities"] = trends_data["new_capabilities"][:_TRENDS_ENTITY_LIMIT]
    trends_data["new_limitations"] = trends_data["new_limitations"][:_TRENDS_ENTITY_LIMIT]
    trends_data["anticipation_updates"] = trends_data["anticipation_updates"][:_TRENDS_ANTICIPATION_LIMIT]
    return trends_data


@router.get("/timeline")
def timeline(
    period: str = Query("3m", description="1w, 1m, 3m, 6m, 1y"),
    source_type: str | None = Query(None),
):
    """Time-bucketed data for trend charts: ingestion timeline, landscape entity counts."""
    days = _PERIOD_DAYS.get(period)
    if days is None:
        raise HTTPException(status_code=400, detail="Invalid period")

    now = datetime.now(timezone.utc)
    start_dt = now - timedelta(days=days)

    # Choose bucket size based on period
    if days <= 7:
        bucket = "day"
    elif days <= 90:
        bucket = "week"
    else:
        bucket = "month"

    type_filter = ""
    params: list = [start_dt]
    if source_type:
        if source_type not in _VALID_SOURCE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid source_type")
        type_filter = "AND source_type = %s"
        params.append(source_type)

    with db.get_conn() as conn:
        # Source ingestion timeline
        ingestion = conn.execute(
            f"""SELECT date_trunc(%s, ingested_at) AS bucket,
                       source_type,
                       count(*) AS count
                FROM sources
                WHERE ingested_at >= %s {type_filter}
                GROUP BY bucket, source_type
                ORDER BY bucket""",
            [bucket] + params,
        ).fetchall()

        # Landscape entity growth (cumulative)
        landscape_growth = conn.execute(
            """SELECT date_trunc(%s, last_updated) AS bucket,
                      'capabilities' AS entity_type, count(*) AS count
               FROM capabilities WHERE last_updated >= %s
               GROUP BY bucket
               UNION ALL
               SELECT date_trunc(%s, last_updated) AS bucket,
                      'limitations' AS entity_type, count(*) AS count
               FROM limitations WHERE last_updated >= %s
               GROUP BY bucket
               UNION ALL
               SELECT date_trunc(%s, detected_at) AS bucket,
                      'breakthroughs' AS entity_type, count(*) AS count
               FROM breakthroughs WHERE detected_at >= %s
               GROUP BY bucket
               ORDER BY bucket""",
            [bucket, start_dt, bucket, start_dt, bucket, start_dt],
        ).fetchall()

    return {
        "period": period,
        "bucket": bucket,
        "ingestion": [dict(r) for r in ingestion],
        "landscape_growth": [dict(r) for r in landscape_growth],
    }
