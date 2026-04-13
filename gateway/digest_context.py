"""Shared context helpers for news digest and weekly roundup handlers.

Provides voice loading, landscape briefing assembly, and post-digest
signal scanning — connecting the digest system to the knowledge engine's
landscape model, anticipations, beliefs, and bottlenecks.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


# ── Voice ───────────────────────────────────────────────────────────────


def load_digest_voice(config) -> str:
    """Load soul.md narrative voice, matching reflect_handler pattern."""
    try:
        from reading_app.memory import MemorySystem

        ms = MemorySystem(Path(config.memory_path))
        return ms.load_voice()
    except Exception:
        logger.debug("Could not load digest voice", exc_info=True)
        return ""


# ── Landscape briefing (daily) ──────────────────────────────────────────


def gather_landscape_briefing(get_conn_fn=None) -> str:
    """Assemble a concise landscape context block for daily digest prompts.

    Pure DB queries, zero LLM calls.  Returns a formatted text block
    covering high-velocity themes, top bottlenecks, recent breakthroughs,
    open anticipations, and active beliefs.
    """
    if get_conn_fn is None:
        from reading_app.db import get_conn

        get_conn_fn = get_conn

    sections: list[str] = []

    try:
        # High-velocity themes
        with get_conn_fn() as conn:
            themes = conn.execute(
                """SELECT id, name, velocity
                   FROM themes
                   WHERE velocity > 0
                   ORDER BY velocity DESC
                   LIMIT 5"""
            ).fetchall()
        if themes:
            from retrieval.wiki_retrieval import gather_wiki_context, extract_section
            wiki_ctx = gather_wiki_context(theme_ids=[t["id"] for t in themes])
            lines = ["### Active Themes (by velocity)"]
            for t in themes:
                narrative = wiki_ctx.theme_narratives.get(t["id"], "")
                excerpt = extract_section(narrative, "Current State", max_chars=400) if narrative else ""
                excerpt = excerpt.replace("\n", " ").strip() if excerpt else "(no summary)"
                lines.append(
                    f"- **{t['name']}** (velocity {t['velocity']:.1f}): {excerpt}"
                )
            sections.append("\n".join(lines))
    except Exception:
        logger.debug("landscape_briefing: themes query failed", exc_info=True)

    try:
        from retrieval.landscape import get_bottleneck_ranking

        bottlenecks = get_bottleneck_ranking()[:5]
        if bottlenecks:
            lines = ["### Top Bottlenecks"]
            for b in bottlenecks:
                lines.append(
                    f"- **{b['description'][:120]}** "
                    f"({b.get('theme_name', '?')}, horizon: {b.get('resolution_horizon', '?')})"
                )
            sections.append("\n".join(lines))
    except Exception:
        logger.debug("landscape_briefing: bottlenecks query failed", exc_info=True)

    try:
        from retrieval.landscape import get_recent_breakthroughs

        breakthroughs = get_recent_breakthroughs(days=14)[:5]
        if breakthroughs:
            lines = ["### Recent Breakthroughs (14 days)"]
            for b in breakthroughs:
                lines.append(
                    f"- **{b['description'][:120]}** "
                    f"({b.get('theme_name', '?')}, significance: {b.get('significance', '?')})"
                )
            sections.append("\n".join(lines))
    except Exception:
        logger.debug("landscape_briefing: breakthroughs query failed", exc_info=True)

    try:
        from reading_app.db import get_open_anticipations_for_themes

        # Get all theme IDs for broad coverage
        with get_conn_fn() as conn:
            all_theme_ids = [
                r["id"]
                for r in conn.execute("SELECT id FROM themes").fetchall()
            ]
        if all_theme_ids:
            anticipations = get_open_anticipations_for_themes(all_theme_ids)[:10]
            if anticipations:
                lines = ["### Open Predictions Being Tracked"]
                for a in anticipations:
                    lines.append(
                        f"- [{a.get('theme_name', '?')}] {a['prediction'][:150]} "
                        f"(confidence: {a.get('confidence', '?')})"
                    )
                sections.append("\n".join(lines))
    except Exception:
        logger.debug("landscape_briefing: anticipations query failed", exc_info=True)

    try:
        from reading_app.db import get_active_beliefs

        beliefs = get_active_beliefs()[:5]
        if beliefs:
            lines = ["### Active Beliefs"]
            for b in beliefs:
                lines.append(
                    f"- [{b.get('theme_name', '?')}] {b['position'][:150]} "
                    f"(confidence: {b.get('confidence', '?')})"
                )
            sections.append("\n".join(lines))
    except Exception:
        logger.debug("landscape_briefing: beliefs query failed", exc_info=True)

    if not sections:
        return ""

    return "## Landscape Context\n\n" + "\n\n".join(sections)


# ── Landscape briefing (weekly — richer) ────────────────────────────────


def gather_weekly_landscape_context(get_conn_fn=None) -> str:
    """Richer landscape context for weekly roundup prompts.

    Includes full state summaries, more bottlenecks, anticipations with
    recent evidence, and breakthroughs from the past 7 days.
    """
    if get_conn_fn is None:
        from reading_app.db import get_conn

        get_conn_fn = get_conn

    sections: list[str] = []

    try:
        with get_conn_fn() as conn:
            themes = conn.execute(
                """SELECT id, name, velocity
                   FROM themes
                   WHERE velocity > 0
                   ORDER BY velocity DESC"""
            ).fetchall()
        if themes:
            from retrieval.wiki_retrieval import gather_wiki_context
            wiki_ctx = gather_wiki_context(theme_ids=[t["id"] for t in themes], max_pages=20)
            lines = ["### Active Themes"]
            for t in themes:
                narrative = wiki_ctx.theme_narratives.get(t["id"], "")
                content = narrative[:4000] if narrative else "No state summary yet."
                lines.append(
                    f"#### {t['name']} (velocity {t['velocity']:.1f})\n{content}"
                )
            sections.append("\n\n".join(lines))
    except Exception:
        logger.debug("weekly_landscape: themes query failed", exc_info=True)

    try:
        from retrieval.landscape import get_bottleneck_ranking

        bottlenecks = get_bottleneck_ranking()[:10]
        if bottlenecks:
            lines = ["### Top Bottlenecks"]
            for b in bottlenecks:
                lines.append(
                    f"- **{b['description'][:200]}** "
                    f"({b.get('theme_name', '?')}, horizon: {b.get('resolution_horizon', '?')}, "
                    f"confidence: {b.get('confidence', '?')})"
                )
            sections.append("\n".join(lines))
    except Exception:
        logger.debug("weekly_landscape: bottlenecks query failed", exc_info=True)

    try:
        from retrieval.landscape import get_recent_breakthroughs

        breakthroughs = get_recent_breakthroughs(days=7)
        if breakthroughs:
            lines = ["### Breakthroughs This Week"]
            for b in breakthroughs:
                lines.append(
                    f"- **{b['description'][:200]}** "
                    f"({b.get('theme_name', '?')}, significance: {b.get('significance', '?')})"
                )
            sections.append("\n".join(lines))
    except Exception:
        logger.debug("weekly_landscape: breakthroughs query failed", exc_info=True)

    try:
        from reading_app.db import get_open_anticipations_for_themes

        with get_conn_fn() as conn:
            all_theme_ids = [
                r["id"]
                for r in conn.execute("SELECT id FROM themes").fetchall()
            ]
        if all_theme_ids:
            anticipations = get_open_anticipations_for_themes(all_theme_ids)
            if anticipations:
                lines = ["### Open Predictions"]
                for a in anticipations:
                    evidence = a.get("status_evidence") or []
                    if isinstance(evidence, str):
                        evidence = json.loads(evidence)
                    # Flag anticipations with recent evidence
                    recent_tag = ""
                    if evidence:
                        recent_tag = f" [{len(evidence)} evidence entries]"
                    lines.append(
                        f"- [{a.get('theme_name', '?')}] {a['prediction'][:200]} "
                        f"(confidence: {a.get('confidence', '?')}){recent_tag}"
                    )
                sections.append("\n".join(lines))
    except Exception:
        logger.debug("weekly_landscape: anticipations query failed", exc_info=True)

    try:
        from reading_app.db import get_active_beliefs

        beliefs = get_active_beliefs()
        if beliefs:
            lines = ["### Active Beliefs"]
            for b in beliefs:
                lines.append(
                    f"- [{b.get('theme_name', '?')}] {b['position'][:200]} "
                    f"(confidence: {b.get('confidence', '?')})"
                )
            sections.append("\n".join(lines))
    except Exception:
        logger.debug("weekly_landscape: beliefs query failed", exc_info=True)

    if not sections:
        return ""

    return "## Weekly Landscape Context\n\n" + "\n\n".join(sections)


# ── Signal scan (daily digest post-processing) ─────────────────────────


def scan_digest_for_signals(
    digest_text: str,
    open_anticipations: list[dict],
    active_bottlenecks: list[dict],
    active_beliefs: list[dict],
    executor,
) -> dict:
    """Single Haiku call to scan digest output for landscape-relevant signals.

    Returns dict with keys:
        anticipation_flags: list of {anticipation_id, direction, snippet}
        bottleneck_signals: list of {bottleneck_id, development, relevance}
        belief_tensions: list of {belief_id, tension, snippet}
    """
    if not any([open_anticipations, active_bottlenecks, active_beliefs]):
        return {"anticipation_flags": [], "bottleneck_signals": [], "belief_tensions": []}

    # Build compact context for the scan prompt
    ant_ctx = ""
    if open_anticipations:
        ant_lines = []
        for a in open_anticipations[:15]:
            ant_lines.append(
                f"  - id={a['id']}: [{a.get('theme_name', '?')}] {a['prediction'][:200]}"
            )
        ant_ctx = "TRACKED PREDICTIONS:\n" + "\n".join(ant_lines)

    bot_ctx = ""
    if active_bottlenecks:
        bot_lines = []
        for b in active_bottlenecks[:10]:
            bot_lines.append(
                f"  - id={b['id']}: [{b.get('theme_name', '?')}] {b['description'][:200]}"
            )
        bot_ctx = "ACTIVE BOTTLENECKS:\n" + "\n".join(bot_lines)

    bel_ctx = ""
    if active_beliefs:
        bel_lines = []
        for b in active_beliefs[:10]:
            bel_lines.append(
                f"  - id={b['id']}: [{b.get('theme_name', '?')}] {b['position'][:200]} "
                f"(confidence: {b.get('confidence', '?')})"
            )
        bel_ctx = "ACTIVE BELIEFS:\n" + "\n".join(bel_lines)

    prompt = f"""You are scanning a daily news digest for signals relevant to a knowledge engine's tracked state.

DIGEST TEXT:
{digest_text}

{ant_ctx}

{bot_ctx}

{bel_ctx}

For each category, identify matches ONLY if there is a clear, specific connection (not vague thematic overlap).

Return JSON (no markdown fences):
{{
  "anticipation_flags": [
    {{"anticipation_id": "...", "direction": "confirming|disconfirming", "snippet": "relevant excerpt from digest"}}
  ],
  "bottleneck_signals": [
    {{"bottleneck_id": "...", "development": "what changed", "relevance": "how it relates"}}
  ],
  "belief_tensions": [
    {{"belief_id": "...", "tension": "what challenges the belief", "snippet": "relevant excerpt"}}
  ]
}}

Return empty arrays if no clear matches found. Be conservative — only flag genuine connections."""

    try:
        result = executor.run_raw(
            prompt=prompt,
            session_id="digest_signal_scan",
            timeout=60,
        )
        parsed = json.loads(result.text.strip())
        return {
            "anticipation_flags": parsed.get("anticipation_flags", []),
            "bottleneck_signals": parsed.get("bottleneck_signals", []),
            "belief_tensions": parsed.get("belief_tensions", []),
        }
    except (json.JSONDecodeError, Exception):
        logger.warning("digest signal scan failed", exc_info=True)
        return {"anticipation_flags": [], "bottleneck_signals": [], "belief_tensions": []}


def persist_signal_scan_results(scan_results: dict, date: str) -> dict:
    """Persist signal scan results: anticipation evidence + notifications.

    Anticipation matches → append_anticipation_evidence (soft signal).
    Bottleneck signals + belief tensions → emit_notification for user review.

    Returns summary dict with counts.
    """
    from reading_app.db import append_anticipation_evidence
    from ingest.notification_emitter import emit_notification

    counts = {"anticipations": 0, "bottleneck_notifications": 0, "belief_notifications": 0}

    for flag in scan_results.get("anticipation_flags", []):
        try:
            evidence = {
                "source_type": "newsletter",
                "date": date,
                "direction": flag.get("direction", "unknown"),
                "snippet": flag.get("snippet", ""),
                "confidence": 0.4,  # Soft signal from secondary source
            }
            append_anticipation_evidence(flag["anticipation_id"], evidence)
            counts["anticipations"] += 1
        except Exception:
            logger.debug("Failed to append anticipation evidence", exc_info=True)

    for signal in scan_results.get("bottleneck_signals", []):
        try:
            emit_notification(
                type="bottleneck_signal",
                entity_type="bottleneck",
                entity_id=signal.get("bottleneck_id", ""),
                title=f"Newsletter signal: {signal.get('development', '')[:100]}",
                detail={
                    "source": f"daily_digest_{date}",
                    "relevance": signal.get("relevance", ""),
                },
            )
            counts["bottleneck_notifications"] += 1
        except Exception:
            logger.debug("Failed to emit bottleneck notification", exc_info=True)

    for tension in scan_results.get("belief_tensions", []):
        try:
            emit_notification(
                type="belief_tension",
                entity_type="belief",
                entity_id=tension.get("belief_id", ""),
                title=f"Newsletter tension: {tension.get('tension', '')[:100]}",
                detail={
                    "source": f"daily_digest_{date}",
                    "snippet": tension.get("snippet", ""),
                },
            )
            counts["belief_notifications"] += 1
        except Exception:
            logger.debug("Failed to emit belief notification", exc_info=True)

    return counts


# ── Cross-system triggers ───────────────────────────────────────────────


def send_signal_alerts(
    scan_results: dict,
    open_anticipations: list[dict],
    active_beliefs: list[dict],
) -> dict:
    """Send Telegram alerts for high-confidence signal scan matches.

    5a: Anticipation alerts for high-confidence matches.
    5b: Belief tension alerts for beliefs with confidence >= 0.8.

    Returns counts dict.
    """
    from notify.telegram import send_telegram_message

    counts = {"anticipation_alerts": 0, "belief_alerts": 0}

    # Build lookup maps
    ant_map = {str(a["id"]): a for a in open_anticipations}
    bel_map = {str(b["id"]): b for b in active_beliefs}

    # 5a: Anticipation alerts
    for flag in scan_results.get("anticipation_flags", []):
        ant_id = str(flag.get("anticipation_id", ""))
        ant = ant_map.get(ant_id)
        if not ant:
            continue
        try:
            direction = flag.get("direction", "?")
            msg = (
                f"*Prediction Signal ({direction})*\n"
                f"_{ant.get('theme_name', '?')}_: {ant['prediction'][:200]}\n\n"
                f"Evidence: {flag.get('snippet', '')[:200]}\n\n"
                f"`/anticipate review {ant.get('theme_id', '')}`"
            )
            send_telegram_message(msg)
            counts["anticipation_alerts"] += 1
        except Exception:
            logger.debug("Failed to send anticipation alert", exc_info=True)

    # 5b: Belief tension alerts (only for high-confidence beliefs >= 0.8)
    for tension in scan_results.get("belief_tensions", []):
        bel_id = str(tension.get("belief_id", ""))
        bel = bel_map.get(bel_id)
        if not bel:
            continue
        bel_confidence = bel.get("confidence", 0)
        if isinstance(bel_confidence, str):
            try:
                bel_confidence = float(bel_confidence)
            except (ValueError, TypeError):
                bel_confidence = 0
        if bel_confidence < 0.8:
            continue
        try:
            msg = (
                f"*Belief Tension Detected*\n"
                f"_{bel.get('theme_name', '?')}_: {bel['position'][:200]}\n"
                f"Confidence: {bel_confidence}\n\n"
                f"Challenge: {tension.get('tension', '')[:200]}\n\n"
                f"`/challenge {bel['id']}`"
            )
            send_telegram_message(msg)
            counts["belief_alerts"] += 1
        except Exception:
            logger.debug("Failed to send belief tension alert", exc_info=True)

    return counts


_AUTO_REFLECT_STATE = Path("var/state/auto_reflect_last.json")


def maybe_trigger_auto_reflect(pipeline_result: dict) -> bool:
    """5c: After YouTube save pipeline, enqueue /reflect if significant.

    Triggers if: breakthrough detected OR 3+ implications.
    Cooldown: only if last auto-reflect was > 24 hours ago.
    """
    breakthroughs = []
    landscape_signals = pipeline_result.get("landscape_signals", {})
    if isinstance(landscape_signals, dict):
        breakthroughs = landscape_signals.get("breakthroughs", [])
    implications = pipeline_result.get("implications", [])

    should_trigger = bool(breakthroughs) or len(implications) >= 3
    if not should_trigger:
        return False

    # Check cooldown
    import time as _time

    _AUTO_REFLECT_STATE.parent.mkdir(parents=True, exist_ok=True)
    try:
        if _AUTO_REFLECT_STATE.exists():
            state = json.loads(_AUTO_REFLECT_STATE.read_text(encoding="utf-8"))
            last_ts = state.get("last_auto_reflect", 0)
            if _time.time() - last_ts < 86400:
                logger.debug("auto_reflect_cooldown_active")
                return False
    except Exception:
        pass

    # Find most-impacted theme
    theme_id = None
    if breakthroughs:
        theme_id = breakthroughs[0].get("theme_id")
    elif implications:
        theme_id = implications[0].get("target_theme_id") or implications[0].get("source_theme_id")

    if not theme_id:
        return False

    # Enqueue reflect event
    try:
        from gateway.models import Event, Job
        from gateway.queue import Queue

        queue = Queue()
        event = Event(
            type="reflect",
            payload={
                "text": f'/reflect topic "{theme_id}"',
                "topic": theme_id,
                "trigger": "auto_reflect_youtube",
            },
            source="youtube_monitor",
        )
        event_id = queue.insert_event(event)
        queue.insert_job(Job(event_id=event_id, skill="reflect"))

        # Update cooldown state
        _AUTO_REFLECT_STATE.write_text(
            json.dumps({"last_auto_reflect": _time.time(), "theme_id": theme_id}),
            encoding="utf-8",
        )
        logger.info("auto_reflect_enqueued", theme_id=theme_id, event_id=event_id)
        return True
    except Exception:
        logger.debug("Failed to enqueue auto-reflect", exc_info=True)
        return False


def scan_weekly_for_anticipation_suggestions(
    roundup_text: str, executor
) -> list[dict]:
    """5d: Scan weekly roundup Open Questions for trackable predictions.

    Single Haiku call. Returns list of suggested anticipations.
    """
    prompt = f"""You are reviewing a weekly news roundup's "Open Questions for Next Week" section
to identify questions that could be tracked as formal predictions/anticipations.

ROUNDUP TEXT (focus on Open Questions section):
{roundup_text[-3000:]}

Identify questions that are:
1. Specific enough to be confirmed or disconfirmed by future evidence
2. Time-bounded (within weeks to months)
3. Relevant to AI/technology themes

Return JSON (no markdown fences):
{{
  "suggestions": [
    {{
      "prediction": "reworded as a trackable prediction statement",
      "theme_hint": "likely theme name",
      "timeframe": "weeks|months|quarters",
      "confidence": 0.5
    }}
  ]
}}

Return empty suggestions array if no questions are suitable for tracking."""

    try:
        result = executor.run_raw(
            prompt=prompt,
            session_id="weekly_anticipation_scan",
            timeout=60,
        )
        parsed = json.loads(result.text.strip())
        return parsed.get("suggestions", [])
    except (json.JSONDecodeError, Exception):
        logger.debug("weekly anticipation scan failed", exc_info=True)
        return []


def send_anticipation_suggestions(suggestions: list[dict]) -> int:
    """Send Telegram notifications for suggested anticipations."""
    from notify.telegram import send_telegram_message

    sent = 0
    for s in suggestions[:5]:
        try:
            msg = (
                f"*Suggested Prediction to Track*\n"
                f"_{s.get('theme_hint', '?')}_ ({s.get('timeframe', '?')})\n\n"
                f"{s['prediction'][:300]}\n\n"
                f"`/anticipate {s.get('theme_hint', 'general')}`"
            )
            send_telegram_message(msg)
            sent += 1
        except Exception:
            logger.debug("Failed to send anticipation suggestion", exc_info=True)
    return sent
