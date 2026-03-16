"""Direct Python handler for inspecting and updating chat provider preferences."""

from __future__ import annotations

from agents.executor import ClaudeExecutor
from gateway.providers import (
    VALID_PROVIDER_IDS,
    build_chat_session_key,
    get_default_provider_id,
    get_provider_label,
    normalize_provider_id,
)
from gateway.queue import DEFAULT_QUEUE_DB_PATH, Queue


def _status_map(executor) -> dict[str, dict]:
    status_source = getattr(executor, "_executor", executor)
    status_fn = getattr(status_source, "get_backend_statuses", None)
    if callable(status_fn):
        statuses = status_fn()
    else:
        statuses = ClaudeExecutor.get_backend_statuses()
    return {status["id"]: status for status in statuses}


def _session_key_for_event(event) -> str:
    chat_id = getattr(event, "chat_id", "") or event.payload.get("chat_id") or ""
    return build_chat_session_key(chat_id)


def _parse_requested_provider(text: str, fallback: str | None = None) -> str | None:
    parts = (text or "").strip().split()
    if parts and parts[0].lower() == "/provider" and len(parts) == 1:
        return None
    if len(parts) >= 2:
        raw = parts[1].strip()
        normalized = normalize_provider_id(raw, fallback="")
        if normalized in VALID_PROVIDER_IDS:
            return normalized
        return None
    if fallback:
        normalized = normalize_provider_id(fallback, fallback="")
        if normalized in VALID_PROVIDER_IDS:
            return normalized
    return None


def _render_provider_overview(current_provider: str, statuses: dict[str, dict]) -> str:
    lines = [f"Current provider: **{get_provider_label(current_provider)}** (`{current_provider}`)", "", "Available providers:"]
    for provider_id in VALID_PROVIDER_IDS:
        status = statuses[provider_id]
        if status.get("available"):
            lines.append(f"- `{provider_id}`: {status['label']} ready")
        else:
            reason = status.get("reason") or "Not configured."
            lines.append(f"- `{provider_id}`: {status['label']} unavailable ({reason})")
    lines.extend(
        [
            "",
            "Switch with " + ", ".join(f"`/provider {provider_id}`" for provider_id in VALID_PROVIDER_IDS) + ".",
        ]
    )
    return "\n".join(lines)


def handle_provider_job(event, job, config, executor, *, queue: Queue | None = None, on_progress=None) -> str:
    """Show or update the sticky provider for the current chat."""
    q = queue or Queue(DEFAULT_QUEUE_DB_PATH)
    statuses = _status_map(executor)
    session_key = _session_key_for_event(event)
    job_provider = getattr(job, "provider_id", None)
    current_provider = (
        q.get_chat_provider(session_key)
        or (normalize_provider_id(job_provider) if job_provider else None)
        or get_default_provider_id()
    )
    requested_provider = _parse_requested_provider(
        event.payload.get("text", ""),
        fallback=event.payload.get("provider_id"),
    )

    if requested_provider is None and (event.payload.get("text", "").strip() not in ("/provider", "")):
        return (
            "Unknown provider. Use `/provider` or one of "
            + ", ".join(f"`/provider {provider_id}`" for provider_id in VALID_PROVIDER_IDS)
            + "."
        )

    if requested_provider is None:
        return _render_provider_overview(current_provider, statuses)

    status = statuses[requested_provider]
    if not status.get("available"):
        reason = status.get("reason") or "Not configured."
        return (
            f"{status['label']} is not available yet. {reason} "
            "Choose another provider or finish the setup first."
        )

    q.set_chat_provider(session_key, requested_provider)
    return (
        f"Provider updated to **{get_provider_label(requested_provider)}** (`{requested_provider}`). "
        "Future messages in this chat will use it."
    )
