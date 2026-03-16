"""Output parsing for CLI backend responses."""

from __future__ import annotations

import json
from typing import Any


def extract_text_from_value(value: Any) -> str:
    """Recursively extract text from CLI output values."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts = [extract_text_from_value(item) for item in value]
        return "\n".join(part for part in parts if part).strip()
    if isinstance(value, dict):
        for key in ("text", "content", "output", "result", "message"):
            text = extract_text_from_value(value.get(key))
            if text:
                return text
    return ""


def parse_stream_json(stdout: str) -> tuple[str, float | None, dict | None, str | None]:
    """Parse Claude CLI stream-json output format."""
    text = ""
    cost = None
    usage = None
    session_id = None
    for line in stdout.strip().splitlines():
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "result":
            text = extract_text_from_value(event.get("result")) or text
            cost = event.get("cost_usd")
            usage = event.get("usage")
            session_id = event.get("session_id")
    return text, cost, usage, session_id


def parse_codex_jsonl(
    stdout: str,
    *,
    resume_session_id: str | None = None,
) -> tuple[str, float | None, dict | None, str | None]:
    """Parse Codex CLI JSONL output format."""
    text = ""
    usage = None
    session_id = resume_session_id
    non_json_lines: list[str] = []

    for raw_line in stdout.strip().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            non_json_lines.append(line)
            continue

        session_candidate = (
            event.get("thread_id")
            or event.get("threadId")
            or event.get("session_id")
            or event.get("sessionId")
        )
        if session_candidate:
            session_id = str(session_candidate)

        usage_candidate = event.get("usage")
        if isinstance(usage_candidate, dict):
            usage = usage_candidate

        candidate = ""
        for key in ("result", "output", "message", "content"):
            candidate = extract_text_from_value(event.get(key))
            if candidate:
                break
        if candidate:
            text = candidate

    if not text and non_json_lines:
        text = "\n".join(non_json_lines).strip()

    return text, None, usage, session_id
