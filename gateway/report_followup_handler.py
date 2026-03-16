"""Follow-up handler for interactive report Q&A.

After a /reflect topic report is generated, the user can ask follow-up
questions that are answered in the context of the report. The handler
loads the persisted ReportRunState and uses the ReACT agent to answer
with access to the same lenses.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Callable

import structlog

logger = structlog.get_logger(__name__)

# How long after report generation a follow-up is allowed (seconds)
FOLLOWUP_WINDOW_SECONDS = 30 * 60  # 30 minutes


def find_recent_report_state(library_path: Path) -> dict | None:
    """Find the most recently generated report state within the follow-up window.

    Returns the parsed state dict or None if no recent report exists.
    """
    syntheses_dir = library_path / "syntheses"
    if not syntheses_dir.exists():
        return None

    state_files = sorted(
        syntheses_dir.glob("*_state.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not state_files:
        return None

    most_recent = state_files[0]
    age_seconds = time.time() - most_recent.stat().st_mtime

    if age_seconds > FOLLOWUP_WINDOW_SECONDS:
        return None

    try:
        return json.loads(most_recent.read_text(encoding="utf-8"))
    except Exception:
        logger.debug("Failed to load report state from %s", most_recent, exc_info=True)
        return None


def handle_report_followup(
    question: str,
    report_state: dict,
    get_conn_fn,
    executor,
    on_progress: Callable[[str], None] | None = None,
) -> str:
    """Answer a follow-up question in the context of a recent report.

    Uses the ReACT agent with access to lenses, injecting the report
    context so answers reference specific content from the report.
    """
    from retrieval.lenses import (
        run_lens_by_name, format_lens_results_for_prompt,
    )

    if on_progress:
        on_progress("Answering in context of recent report...")

    topic = report_state.get("topic", "")
    sections = report_state.get("section_content", {})

    # Build report context summary (truncated for prompt size)
    report_summary_parts = [f"Report topic: {topic}\n"]
    for title, content in sections.items():
        report_summary_parts.append(f"## {title}\n{content[:500]}\n")
    report_context = "\n".join(report_summary_parts)[:4000]

    # Get embedding for the follow-up question
    embedding = None
    try:
        from reading_app.embeddings import embed_batch
        embedding = embed_batch([question])[0]
    except Exception:
        pass

    # Run evidence lens focused on the follow-up question
    lens_results = []
    try:
        evidence = run_lens_by_name("evidence", question, get_conn_fn, embedding=embedding)
        lens_results.append(evidence)
    except Exception:
        logger.debug("followup evidence lens failed", exc_info=True)

    # Also run contradiction lens if question is about gaps/limitations
    q_lower = question.lower()
    if any(kw in q_lower for kw in ("limitation", "gap", "weak", "miss", "contradiction", "problem")):
        try:
            contradiction = run_lens_by_name("contradiction", question, get_conn_fn, embedding=embedding)
            lens_results.append(contradiction)
        except Exception:
            pass

    fresh_evidence = format_lens_results_for_prompt(lens_results) if lens_results else ""

    prompt = f"""You are answering a follow-up question about a research report you just generated.

## Original Report Context
{report_context}

## Fresh Evidence (from follow-up query)
{fresh_evidence}

## Follow-up Question
{question}

## Instructions
- Answer the question by referencing specific content from the report
- Supplement with fresh evidence where relevant
- Cite sources using [source_id] inline
- Be specific about which section of the report you're elaborating on
- If the question asks about something not covered in the report, say so and provide
  what evidence is available from the knowledge base

Answer:"""

    try:
        result = executor.run_raw(prompt, session_id="report_followup", timeout=90)
        if result.text and len(result.text) > 20:
            return result.text
    except Exception:
        logger.warning("report followup synthesis failed", exc_info=True)

    return "I couldn't generate a follow-up answer. Try rephrasing your question."
