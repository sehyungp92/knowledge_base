"""OpenRouter API session management and streaming."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Callable

import httpx
import structlog

from agents import openrouter_client
from agents.backend_config import (
    ExecutionResult,
    _env_bool,
    _env_int,
    _CLAUDE_TIER_FALLBACK,
    _PROGRESS_INTERVAL_S,
    _RETRYABLE_TEXT_PATTERNS,
    _RETRYABLE_CODE_RE,
)

logger = structlog.get_logger(__name__)


def openrouter_history_path(session_dir: Path) -> Path:
    """Return the path to the message history file for a conversation."""
    return session_dir / "messages.json"


def trim_openrouter_history(messages: list[dict[str, str]]) -> list[dict[str, str]]:
    """Filter and trim conversation history to stay within limits."""
    trimmed = [
        {"role": message["role"], "content": message["content"]}
        for message in messages
        if message.get("role") in {"user", "assistant"} and str(message.get("content") or "").strip()
    ]
    max_messages = _env_int("KB_OPENROUTER_MAX_SESSION_MESSAGES", default=12)
    if max_messages > 0 and len(trimmed) > max_messages:
        trimmed = trimmed[-max_messages:]
    if len(trimmed) > 1 and trimmed[0].get("role") == "assistant":
        trimmed = trimmed[1:]
    return trimmed


def load_openrouter_history(session_dir: Path) -> list[dict[str, str]]:
    """Load and validate conversation history from disk."""
    history_path = openrouter_history_path(session_dir)
    if not history_path.exists():
        return []

    try:
        raw = json.loads(history_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        logger.warning("openrouter_history_invalid", session_dir=str(session_dir))
        return []

    if not isinstance(raw, list):
        return []

    messages: list[dict[str, str]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        role = str(item.get("role") or "").strip().lower()
        content = str(item.get("content") or "").strip()
        if role in {"user", "assistant", "system"} and content:
            messages.append({"role": role, "content": content})
    return trim_openrouter_history(messages)


def save_openrouter_history(session_dir: Path, messages: list[dict[str, str]]) -> None:
    """Persist trimmed conversation history to disk."""
    history_path = openrouter_history_path(session_dir)
    messages = trim_openrouter_history(messages)
    history_path.write_text(json.dumps(messages, ensure_ascii=True, indent=2), encoding="utf-8")


def openrouter_fallback_models(
    resolved_tier: str | None,
    resolve_model_fn: Callable[[str, str | None], str | None],
) -> list[str]:
    """Compute fallback model list based on tier."""
    enable_fallback = _env_bool("KB_OPENROUTER_ENABLE_FALLBACK_MODEL", default=True)
    if not enable_fallback or not resolved_tier:
        return []
    fallback_tier = _CLAUDE_TIER_FALLBACK.get(resolved_tier)
    if not fallback_tier:
        return []
    fallback_model = resolve_model_fn("openrouter", fallback_tier)
    return [fallback_model] if fallback_model else []


def run_openrouter_api(
    *,
    prompt: str,
    system_message: str | None,
    user_message: str | None,
    session_id: str,
    timeout: int,
    on_progress: Callable[[str], None] | None,
    resume_session_id: str | None,
    continue_session: bool,
    max_retries: int,
    resolved_model: str | None,
    fallback_models: list[str],
    session_dir: Path,
) -> ExecutionResult:
    """Execute a prompt via the OpenRouter native API with retry logic."""
    if not resolved_model:
        return ExecutionResult(
            "", "OpenRouter model could not be resolved.", 1, "", None, None,
            failure_type="server_error", backend_id="openrouter",
        )

    provider_order = [
        item.strip()
        for item in os.getenv("OPENROUTER_PROVIDER_ORDER", "").split(",")
        if item.strip()
    ]
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").strip()
    app_name = os.getenv("OPENROUTER_APP_NAME", "knowledge_base").strip()
    http_referer = os.getenv("OPENROUTER_HTTP_REFERER", "").strip() or None
    conversation_id = resume_session_id or session_id
    should_persist_session = continue_session or bool(resume_session_id)
    history = load_openrouter_history(session_dir) if should_persist_session else []
    current_user_message = (user_message or prompt).strip()
    messages: list[dict[str, str]] = []
    if system_message:
        messages.append({"role": "system", "content": system_message.strip()})
    messages.extend(history)
    messages.append({"role": "user", "content": current_user_message})

    base_delay = 3
    result: ExecutionResult | None = None
    for attempt in range(max_retries + 1):
        stdout_events: list[str] = []
        usage: dict | None = None
        provider_name: str | None = None
        response_text = ""
        last_progress_ts = 0.0

        try:
            for event in openrouter_client.stream_chat(
                api_key=api_key,
                base_url=base_url,
                model=resolved_model,
                messages=messages,
                timeout=timeout,
                fallback_models=fallback_models,
                provider_order=provider_order or None,
                app_name=app_name or None,
                http_referer=http_referer,
            ):
                stdout_events.append(json.dumps(event, ensure_ascii=True))
                event_type = str(event.get("type") or "").strip().lower()
                if event_type == "progress":
                    if on_progress and event.get("text"):
                        on_progress(str(event["text"]).strip())
                    continue
                if event_type == "delta":
                    response_text += str(event.get("text") or "")
                    now = time.monotonic()
                    if on_progress and response_text.strip() and now - last_progress_ts >= _PROGRESS_INTERVAL_S:
                        on_progress(f"... {response_text[-200:].strip()}")
                        last_progress_ts = now
                    continue
                if event_type == "message":
                    response_text = str(event.get("text") or "").strip() or response_text
                    continue
                if event_type == "meta":
                    usage_candidate = event.get("usage")
                    if isinstance(usage_candidate, dict):
                        usage = usage_candidate
                    provider_candidate = event.get("provider")
                    if provider_candidate:
                        provider_name = str(provider_candidate)
                    continue

            session_out = conversation_id if should_persist_session else None
            if should_persist_session and response_text.strip():
                save_openrouter_history(
                    session_dir,
                    [
                        *history,
                        {"role": "user", "content": current_user_message},
                        {"role": "assistant", "content": response_text.strip()},
                    ],
                )

            if usage and provider_name:
                usage = {**usage, "provider": provider_name}

            result = ExecutionResult(
                "\n".join(stdout_events), "", 0, response_text.strip(),
                None, usage, session_out, backend_id="openrouter",
            )
        except openrouter_client.OpenRouterAPIError as exc:
            is_rate_limit = exc.status_code == 429 or "429" in str(exc)
            result = ExecutionResult(
                "", str(exc), exc.status_code or 1, "", None, None,
                failure_type="rate_limit" if is_rate_limit else "server_error",
                backend_id="openrouter",
            )
        except httpx.TimeoutException:
            result = ExecutionResult(
                "", "Timeout", 1, "", None, None,
                failure_type="timeout", backend_id="openrouter",
            )
        except Exception as exc:
            result = ExecutionResult(
                "", str(exc), 1, "", None, None,
                failure_type="server_error", backend_id="openrouter",
            )

        if result.return_code == 0 or attempt >= max_retries:
            return result

        stderr_lower = result.stderr.lower()
        is_retryable = any(pattern in stderr_lower for pattern in _RETRYABLE_TEXT_PATTERNS)
        if not is_retryable:
            is_retryable = bool(_RETRYABLE_CODE_RE.search(result.stderr))
        if not is_retryable:
            return result

        delay = base_delay * (2 ** attempt)
        logger.warning(
            "openrouter_retry",
            session_id=session_id,
            attempt=attempt + 1,
            max_retries=max_retries,
            delay_s=delay,
            stderr_snippet=result.stderr[:200],
        )
        time.sleep(delay)

    return result or ExecutionResult("", "Unknown OpenRouter failure", 1, "", None, None, backend_id="openrouter")
