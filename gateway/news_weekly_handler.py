"""Direct Python handler for news_weekly jobs.

Reads the week's daily digests, synthesizes a weekly roundup via
executor.run_raw(), saves to disk, and sends notifications.
"""

from __future__ import annotations

import time
from datetime import datetime, timedelta
from pathlib import Path

import structlog

from gateway.digest_context import (
    gather_weekly_landscape_context,
    load_digest_voice,
    scan_weekly_for_anticipation_suggestions,
    send_anticipation_suggestions,
)
from gateway.models import Event, Job
from notify.email import send_digest_email
from notify.telegram import send_telegram_message

logger = structlog.get_logger(__name__)

_DAILY_DIR = Path("var/news_digests/daily")
_WEEKLY_DIR = Path("var/news_digests/weekly")


def handle_news_weekly_job(
    event: Event, job: Job, config, executor, *, on_progress=None
) -> str:
    """Generate a weekly roundup from daily digests.

    Flow: read daily digests for past 7 days -> build prompt ->
    executor.run_raw() -> save to var/news_digests/weekly/YYYY-WNN.md ->
    email + Telegram.

    Returns a short status string.
    """
    week_label = event.payload.get("week_label", "unknown")

    log = logger.bind(job_id=job.id, week=week_label)
    log.info("news_weekly_handler_start")
    t0 = time.monotonic()

    # ── Read daily digests from past 7 days ───────────────────────────
    daily_digests = _collect_daily_digests(week_label)

    if not daily_digests:
        log.warning("no_daily_digests", week=week_label)
        return f"No daily digests found for {week_label}"

    # ── Load voice + landscape context ─────────────────────────────────
    voice = load_digest_voice(config)
    landscape_context = ""
    try:
        landscape_context = gather_weekly_landscape_context()
    except Exception:
        log.debug("weekly_landscape_context_failed", exc_info=True)

    # ── Build prompt ──────────────────────────────────────────────────
    prompt = _build_weekly_prompt(week_label, daily_digests, voice, landscape_context)

    # ── Call executor ─────────────────────────────────────────────────
    result = executor.run_raw(
        prompt=prompt,
        session_id=f"news_weekly_{week_label}",
        timeout=600,
        on_progress=on_progress,
    )

    roundup_text = result.text

    # ── Save to disk ──────────────────────────────────────────────────
    _WEEKLY_DIR.mkdir(parents=True, exist_ok=True)
    roundup_path = _WEEKLY_DIR / f"{week_label}.md"
    roundup_path.write_text(roundup_text, encoding="utf-8")
    log.info("weekly_saved", path=str(roundup_path), chars=len(roundup_text))

    # ── Email notification ────────────────────────────────────────────
    email_sent = send_digest_email(
        date=week_label,
        digest_markdown=roundup_text,
        digest_type="weekly",
    )

    # ── Telegram notification ─────────────────────────────────────────
    condensed = _condensed_weekly_telegram(roundup_text, week_label)
    telegram_sent = send_telegram_message(condensed)

    # ── Anticipation suggestions (5d, best-effort) ────────────────────
    try:
        suggestions = scan_weekly_for_anticipation_suggestions(roundup_text, executor)
        if suggestions:
            send_anticipation_suggestions(suggestions)
            log.info("anticipation_suggestions_sent", count=len(suggestions))
    except Exception:
        log.debug("anticipation_suggestions_failed", exc_info=True)

    elapsed = time.monotonic() - t0
    log.info(
        "news_weekly_handler_complete",
        elapsed_s=round(elapsed, 1),
        roundup_chars=len(roundup_text),
        daily_count=len(daily_digests),
        email_sent=email_sent,
        telegram_sent=telegram_sent,
    )

    return (
        f"Weekly roundup generated for {week_label}\n"
        f"Daily digests: {len(daily_digests)}\n"
        f"Content: {len(roundup_text)} chars\n"
        f"Email: {'sent' if email_sent else 'skipped'}\n"
        f"Telegram: {'sent' if telegram_sent else 'skipped'}\n"
        f"Completed in {elapsed:.0f}s"
    )


def _collect_daily_digests(week_label: str) -> list[tuple[str, str]]:
    """Read daily digests for the given ISO week.

    Returns list of (date_str, content) tuples, oldest first.
    """
    try:
        year, week_num = week_label.split("-W")
        year, week_num = int(year), int(week_num)
    except (ValueError, AttributeError):
        logger.warning("Invalid week label: %s", week_label)
        return []

    # ISO week: Monday is day 1. Jan 4 is always in ISO week 1.
    jan4 = datetime(year, 1, 4)
    week_1_monday = jan4 - timedelta(days=jan4.weekday())
    monday = week_1_monday + timedelta(weeks=week_num - 1)

    digests = []
    for i in range(7):  # Mon through Sun
        date = monday + timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        daily_file = _DAILY_DIR / f"{date_str}.md"

        if daily_file.exists():
            try:
                content = daily_file.read_text(encoding="utf-8")
                digests.append((date_str, content))
            except Exception:
                logger.warning("Failed to read daily digest: %s", date_str)

    return digests


def _build_weekly_prompt(
    week_label: str,
    daily_digests: list[tuple[str, str]],
    voice: str = "",
    landscape_context: str = "",
) -> str:
    """Build the full LLM prompt for weekly roundup generation."""
    parts = []

    # Voice from soul.md
    if voice:
        parts.append("## Voice & Personality")
        parts.append(voice)
        parts.append("")

    parts.extend([
        f"You are writing a weekly intelligence roundup for {week_label}.",
        "",
    ])

    # Landscape context for grounding
    if landscape_context:
        parts.append(landscape_context)
        parts.append("")
        parts.append(
            "Use the landscape context above to ground your analysis. When this week's "
            "news provides evidence for or against tracked predictions, call it out in "
            "the Prediction Tracker section. When developments relate to active bottlenecks, "
            "include them in Bottleneck Watch. If any news challenges active beliefs, flag "
            "it in Belief Check."
        )
        parts.append("")

    parts.extend([
        "Below are the daily digests from this week.",
        "",
    ])

    for date_str, content in daily_digests:
        parts.append(f"## {date_str}")
        parts.append(content)
        parts.append("")

    parts.extend([
        "## OUTPUT FORMAT",
        "",
        f"# Weekly Roundup — {week_label}",
        "",
        "## Executive Summary",
        "[The week's 'story' in 3-5 sentences]",
        "",
        "---",
        "",
        "## AI & Technology",
        "",
        "### Theme Analysis",
        "#### [Theme Name]",
        "- **What happened**: [Summary of developments under this theme]",
        "- **Trajectory**: [Accelerating, stalling, or shifting? Based on what evidence?]",
        "- **Open questions**: [What remains unresolved?]",
        "[3-5 themes]",
        "",
        "### Emerging Signals",
        "[Minor developments that could become significant]",
        "",
        "---",
        "",
        "## Startups & Venture",
        "",
        "### Theme Analysis",
        "#### [Theme Name]",
        "- **What happened** / **Trajectory** / **Open questions**",
        "[2-4 themes]",
        "",
        "### Emerging Signals",
        "[New sectors, pivot patterns, geographic shifts]",
        "",
        "---",
        "",
        "## Prediction Tracker",
        "[Which tracked predictions received evidence this week? Reference specific",
        "predictions from the landscape context if provided.]",
        "- **[Prediction]**: [Evidence from this week — confirming or disconfirming]",
        "",
        "---",
        "",
        "## Bottleneck Watch",
        "[Developments relevant to active bottlenecks. Reference specific bottlenecks",
        "from the landscape context if provided.]",
        "- **[Bottleneck]**: [What changed this week]",
        "",
        "---",
        "",
        "## Belief Check",
        "[Do any active beliefs need updating based on this week's evidence?",
        "Only include if there is genuine tension with tracked beliefs.]",
        "",
        "---",
        "",
        "## Convergence Patterns",
        "[HIGHEST VALUE SECTION — identify where unrelated stories from different",
        "days or sections point at the same underlying shift]",
        "- **[Convergence title]**: [Explanation citing specific stories from specific days]",
        "",
        "---",
        "",
        "## Open Questions for Next Week",
        "1. [Specific, answerable question next week's news could address]",
        "[5-8 questions]",
    ])

    return "\n".join(parts)


def _condensed_weekly_telegram(roundup_text: str, week_label: str) -> str:
    """Extract Executive Summary + Prediction Tracker + Convergence for Telegram."""
    lines = roundup_text.split("\n")
    condensed = [f"*Weekly Roundup — {week_label}*", ""]

    in_exec = False
    in_convergence = False
    in_predictions = False

    for line in lines:
        if "## Executive Summary" in line:
            in_exec = True
            continue
        if in_exec:
            if line.startswith("---") or (line.startswith("##") and "Executive" not in line):
                in_exec = False
                condensed.append("")
            else:
                condensed.append(line)

        if "## Prediction Tracker" in line:
            in_predictions = True
            condensed.append("*Prediction Tracker*")
            continue
        if in_predictions:
            if line.startswith("---") or (line.startswith("##") and "Prediction" not in line):
                in_predictions = False
                condensed.append("")
            else:
                condensed.append(line)

        if "## Convergence Patterns" in line:
            in_convergence = True
            condensed.append("*Convergence Patterns*")
            continue
        if in_convergence:
            if line.startswith("---") or (line.startswith("##") and "Convergence" not in line):
                in_convergence = False
            else:
                condensed.append(line)

    result = "\n".join(condensed)
    if len(result) > 4000:
        result = result[:3997] + "..."
    return result
