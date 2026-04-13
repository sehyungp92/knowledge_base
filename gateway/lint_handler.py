"""Direct Python handler for /lint jobs.

Runs wiki lint checks and reports results.
"""

from __future__ import annotations

import time
from typing import Callable

import structlog

from gateway.models import Event, Job

logger = structlog.get_logger(__name__)


def handle_lint_job(
    event: Event,
    job: Job,
    config,
    executor,
    *,
    on_progress: Callable[[str], None] | None = None,
) -> str:
    """Run /lint directly."""
    from reading_app.db import ensure_pool
    ensure_pool()

    text = event.payload.get("text", "")
    log = logger.bind(job_id=job.id)
    log.info("lint_handler_start")
    t0 = time.monotonic()

    from retrieval.wiki_lint import run_lint

    # Parse subcommand
    parts = text.strip().split()
    # Remove "/lint" prefix if present
    if parts and parts[0].lower() in ("/lint", "lint"):
        parts = parts[1:]

    mode = "summary"
    scope = None

    if parts:
        subcmd = parts[0].lower()
        if subcmd == "fix":
            mode = "fix"
        elif subcmd == "full":
            mode = "full"
        elif subcmd == "theme" and len(parts) > 1:
            scope = parts[1]
        else:
            # Treat as theme_id
            scope = parts[0]

    report = run_lint(
        mode=mode,
        scope=scope,
        executor=executor if mode == "full" else None,
        on_progress=on_progress,
    )

    elapsed = time.monotonic() - t0
    log.info("lint_handler_done", elapsed=f"{elapsed:.1f}s", issues=len(report.issues), fixed=report.fixed)

    # Format Telegram-compatible response
    lines = [f"**Wiki Health: {report.health_score:.2f}/1.00**"]
    lines.append(
        f"Scanned {report.pages_scanned} pages | "
        f"{len(report.issues)} issues | "
        f"{report.fixed} auto-fixed"
    )
    lines.append("")

    errors = [i for i in report.issues if i.severity == "error"]
    warnings = [i for i in report.issues if i.severity == "warning"]
    infos = [i for i in report.issues if i.severity == "info"]

    if errors:
        lines.append(f"**Errors ({len(errors)}):**")
        for e in errors[:10]:
            lines.append(f"- {e.check}: {e.page} — {e.message}")
        if len(errors) > 10:
            lines.append(f"  ...and {len(errors) - 10} more")
        lines.append("")

    if warnings:
        lines.append(f"**Warnings ({len(warnings)}):**")
        for w in warnings[:10]:
            lines.append(f"- {w.check}: {w.page} — {w.message}")
        if len(warnings) > 10:
            lines.append(f"  ...and {len(warnings) - 10} more")
        lines.append("")

    if infos and not errors and not warnings:
        lines.append(f"**Info ({len(infos)}):**")
        for i in infos[:5]:
            lines.append(f"- {i.check}: {i.page} — {i.message}")
        lines.append("")

    auto_fixable = sum(1 for i in report.issues if i.auto_fixable)
    review_needed = sum(1 for i in report.issues if i.tier == "flag_review")

    if auto_fixable > report.fixed:
        lines.append(f"**Auto-fixable:** {auto_fixable - report.fixed} issues (run `/lint fix`)")
    if review_needed:
        lines.append(f"**Needs review:** {review_needed} issues")
    if mode != "full":
        lines.append("**LLM analysis available:** run `/lint full`")

    return "\n".join(lines)
