"""Direct Python handler for daily news digest jobs."""

from __future__ import annotations

import time
from pathlib import Path

import structlog

from gateway.digest_context import (
    gather_landscape_briefing,
    load_digest_voice,
    persist_signal_scan_results,
    scan_digest_for_signals,
    send_signal_alerts,
)
from gateway.models import Event, Job
from notify.email import send_digest_email
from notify.telegram import send_telegram_message

logger = structlog.get_logger(__name__)

_DIGEST_DIR = Path("var/news_digests/daily")


def handle_news_digest_job(
    event: Event, job: Job, config, executor, *, on_progress=None
) -> str:
    """Process a daily news digest from aggregated source materials."""
    payload = event.payload
    date = payload.get("date", "unknown")
    items = payload.get("items") or payload.get("newsletters", [])

    log = logger.bind(job_id=job.id, date=date, item_count=len(items))
    log.info("news_digest_handler_start")
    t0 = time.monotonic()

    voice = load_digest_voice(config)
    landscape_briefing = ""
    try:
        landscape_briefing = gather_landscape_briefing()
    except Exception:
        log.debug("landscape_briefing_failed", exc_info=True)

    by_category: dict[str, list[dict]] = {}
    for item in items:
        cat = item.get("category", "other")
        by_category.setdefault(cat, []).append(item)

    prompt = _build_daily_prompt(date, by_category, voice, landscape_briefing)

    result = executor.run_raw(
        prompt=prompt,
        session_id=f"news_digest_{date}",
        timeout=480,
        on_progress=on_progress,
    )
    digest_text = result.text

    _DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    digest_path = _DIGEST_DIR / f"{date}.md"
    digest_path.write_text(digest_text, encoding="utf-8")
    log.info("digest_saved", path=str(digest_path), chars=len(digest_text))

    scan_results = {"anticipation_flags": [], "bottleneck_signals": [], "belief_tensions": []}
    signal_counts = {}
    try:
        from reading_app.db import get_active_beliefs, get_open_anticipations_for_themes
        from reading_app.db import get_conn as _get_conn
        from retrieval.landscape import get_bottleneck_ranking

        with _get_conn() as conn:
            all_theme_ids = [r["id"] for r in conn.execute("SELECT id FROM themes").fetchall()]
        open_ants = get_open_anticipations_for_themes(all_theme_ids) if all_theme_ids else []
        active_bots = get_bottleneck_ranking()[:10]
        active_bels = get_active_beliefs()[:10]

        scan_results = scan_digest_for_signals(
            digest_text,
            open_ants,
            active_bots,
            active_bels,
            executor,
        )
        signal_counts = persist_signal_scan_results(scan_results, date)
        log.info("signal_scan_complete", **signal_counts)

        alert_counts = send_signal_alerts(scan_results, open_ants, active_bels)
        log.info("signal_alerts_sent", **alert_counts)
    except Exception:
        log.debug("signal_scan_failed", exc_info=True)

    email_sent = send_digest_email(
        date=date,
        digest_markdown=digest_text,
        digest_type="daily",
    )

    condensed = _condensed_telegram_version(digest_text, date)
    signal_footer = _format_signal_footer(scan_results)
    if signal_footer:
        condensed = condensed.rstrip() + "\n\n" + signal_footer
        if len(condensed) > 4000:
            condensed = condensed[:3997] + "..."
    telegram_sent = send_telegram_message(condensed)

    elapsed = time.monotonic() - t0
    log.info(
        "news_digest_handler_complete",
        elapsed_s=round(elapsed, 1),
        digest_chars=len(digest_text),
        email_sent=email_sent,
        telegram_sent=telegram_sent,
    )

    return (
        f"Daily digest generated for {date}\n"
        f"Content: {len(digest_text)} chars\n"
        f"Email: {'sent' if email_sent else 'skipped'}\n"
        f"Telegram: {'sent' if telegram_sent else 'skipped'}\n"
        f"Completed in {elapsed:.0f}s"
    )


def _render_prompt_item(item: dict) -> list[str]:
    lines = [f"### Source: {item.get('source', 'Unknown')} -- {item.get('subject', '')}"]

    if item.get("kind") in {"article", "social"}:
        if item.get("published_at"):
            lines.append(f"Published: {item['published_at']}")
        if item.get("url"):
            lines.append(f"URL: {item['url']}")
        if item.get("discussion_url"):
            lines.append(f"Discussion URL: {item['discussion_url']}")
        if item.get("topic_tags"):
            lines.append(f"Topic Tags: {', '.join(item['topic_tags'])}")

    lines.append(item.get("clean_text", ""))

    social_proof = item.get("social_proof") or []
    if isinstance(social_proof, dict):
        social_proof = [social_proof]
    if social_proof:
        lines.append("#### Social Proof:")
        for proof in social_proof:
            parts = [f"platform={proof.get('platform', 'social')}"]
            if proof.get("author"):
                parts.append(f"author={proof['author']}")
            if proof.get("subreddit"):
                parts.append(f"subreddit=r/{proof['subreddit']}")
            if proof.get("points") is not None:
                parts.append(f"points={proof.get('points', 0)}")
            if proof.get("comments") is not None:
                parts.append(f"comments={proof.get('comments', 0)}")
            if proof.get("likes") is not None:
                parts.append(f"likes={proof.get('likes', 0)}")
            if proof.get("reposts") is not None:
                parts.append(f"reposts={proof.get('reposts', 0)}")
            if proof.get("discussion_url"):
                parts.append(f"url={proof['discussion_url']}")
            lines.append(f"- {' | '.join(parts)}")
            if proof.get("top_comment"):
                lines.append(f"  Top comment: {proof['top_comment'][:240]}")

    if item.get("links_context"):
        lines.append("#### Linked Articles (fetched for additional context):")
        for link in item["links_context"]:
            lines.append(f"**{link['url']}**: {link['snippet'][:1000]}")

    lines.append("---")
    return lines


def _build_daily_prompt(
    date: str,
    by_category: dict[str, list[dict]],
    voice: str = "",
    landscape_briefing: str = "",
) -> str:
    parts: list[str] = []

    if voice:
        parts.append("## Voice & Personality")
        parts.append(voice)
        parts.append("")

    parts.extend([
        f"You are writing a daily intelligence briefing for {date}.",
        "",
    ])

    if landscape_briefing:
        parts.append(landscape_briefing)
        parts.append("")
        parts.append(
            "When synthesizing today's news, note any connections to the tracked "
            "predictions, bottlenecks, or beliefs above. If a development provides "
            "evidence for or against a tracked prediction, call it out explicitly."
        )
        parts.append("")

    parts.extend([
        "Below are the source materials collected for today's digest. Synthesize them into a structured daily digest.",
        "",
        "Use social items and attached social proof as supporting evidence when they corroborate a story from a newsletter or article.",
        "Do not create duplicate bullets for the same underlying story across platforms.",
        "When a story is also trending on X, Reddit, or Hacker News, fold that into the same bullet instead of creating a second bullet.",
        "Only surface a standalone social-driven bullet when the social discussion itself is the news event.",
        "",
    ])

    if "ai_tech" in by_category:
        parts.append("## AI & TECH SOURCE MATERIALS")
        for item in by_category["ai_tech"]:
            parts.extend(_render_prompt_item(item))

    if "startups" in by_category:
        parts.append("")
        parts.append("## STARTUPS & VENTURE SOURCE MATERIALS")
        for item in by_category["startups"]:
            parts.extend(_render_prompt_item(item))

    other_cats = [cat for cat in by_category if cat not in ("ai_tech", "startups")]
    for cat in other_cats:
        parts.append("")
        parts.append(f"## {cat.upper().replace('_', ' ')} SOURCE MATERIALS")
        for item in by_category[cat]:
            parts.extend(_render_prompt_item(item))

    parts.extend([
        "",
        "## OUTPUT FORMAT",
        "",
        f"# Daily Digest -- {date}",
        "",
        "## AI & Technology",
        "### What's New",
        "- **[Headline/development]**: [2-3 sentence description with specifics]",
        "[5-10 items covering all significant developments]",
        "",
        "### What This Means",
        "[2-3 paragraphs synthesizing into broader patterns and trajectories]",
        "",
        "### Potential Impact & Implications",
        "- **[Area of impact]**: [Specific implication with reasoning]",
        "[3-5 bullets]",
        "",
        "---",
        "",
        "## Startups & Venture",
        "### What's New",
        "- **[Company/deal/development]**: [2-3 sentences with specifics]",
        "",
        "### What This Means",
        "[2-3 paragraphs on sectors, market direction, funding patterns]",
        "",
        "### Potential Impact & Implications",
        "- **[Area]**: [Implication]",
        "",
        "---",
        "",
        "## Cross-Section Signals",
        "[Connections between AI/tech developments and startup activity]",
    ])

    return "\n".join(parts)


def _condensed_telegram_version(digest_text: str, date: str) -> str:
    lines = digest_text.split("\n")
    condensed = [f"*Daily Digest -- {date}*", ""]
    in_section = False
    current_section = ""

    for line in lines:
        if "### What's New" in line:
            in_section = True
            condensed.append(line)
            continue
        if line.startswith("###") and in_section:
            in_section = False
        if in_section and line.startswith("- **"):
            headline = line.split("**")[1] if "**" in line else line
            condensed.append(f"- {headline}")
        if "## Cross-Section Signals" in line:
            condensed.append("")
            condensed.append(line)
            in_section = True
            current_section = "cross"
            continue
        if current_section == "cross" and in_section:
            if line.startswith("##"):
                in_section = False
                current_section = ""
            else:
                condensed.append(line)

    result = "\n".join(condensed)
    if len(result) > 4000:
        result = result[:3997] + "..."
    return result


def _format_signal_footer(scan_results: dict) -> str:
    lines: list[str] = []

    ant_flags = scan_results.get("anticipation_flags", [])
    bot_signals = scan_results.get("bottleneck_signals", [])
    bel_tensions = scan_results.get("belief_tensions", [])

    if not any([ant_flags, bot_signals, bel_tensions]):
        return ""

    lines.append("*Landscape Signals*")

    if ant_flags:
        for flag in ant_flags[:3]:
            direction = flag.get("direction", "?")
            lines.append(f"- Prediction {direction}: {flag.get('snippet', '')[:100]}")

    if bot_signals:
        for signal in bot_signals[:3]:
            lines.append(f"- Bottleneck: {signal.get('development', '')[:100]}")

    if bel_tensions:
        for tension in bel_tensions[:2]:
            lines.append(f"- Belief tension: {tension.get('tension', '')[:100]}")

    return "\n".join(lines)
