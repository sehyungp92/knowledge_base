"""Direct Python handler for inspecting and updating the global model default."""

from __future__ import annotations

from gateway.model_preferences import (
    get_config_default_model_tier,
    get_model_tier_label,
    list_model_tier_metadata,
    match_model_tier,
)
from gateway.queue import DEFAULT_QUEUE_DB_PATH, Queue


def _parse_requested_model(text: str, fallback: str | None = None) -> str | None:
    parts = (text or "").strip().split()
    if parts and parts[0].lower() == "/model" and len(parts) == 1:
        return None
    if len(parts) >= 2:
        return match_model_tier(parts[1].strip())
    if fallback:
        return match_model_tier(fallback)
    return None


def _render_model_overview(current_model: str) -> str:
    lines = [
        f"Current global model: **{get_model_tier_label(current_model)}** (`{current_model}`)",
        "",
        "Available tiers:",
    ]
    for option in list_model_tier_metadata():
        lines.append(f"- `{option['id']}`: {option['label']} - {option['description']}")
    lines.extend(
        [
            "",
            "Switch with `/model fast`, `/model balanced`, `/model deep`, or `/model haiku`, `/model sonnet`, `/model opus`.",
        ]
    )
    return "\n".join(lines)


def handle_model_job(event, job, config, executor, *, queue: Queue | None = None, on_progress=None) -> str:
    """Show or update the global default model tier."""
    q = queue or Queue(DEFAULT_QUEUE_DB_PATH)
    current_model = q.get_global_model() or get_config_default_model_tier()
    requested_model = _parse_requested_model(
        event.payload.get("text", ""),
        fallback=event.payload.get("model_tier"),
    )

    if requested_model is None and (event.payload.get("text", "").strip() not in ("/model", "")):
        return (
            "Unknown model tier. Use `/model`, `/model fast`, `/model balanced`, `/model deep`, "
            "or `/model haiku`, `/model sonnet`, `/model opus`."
        )

    if requested_model is None:
        return _render_model_overview(current_model)

    updated = q.set_global_model(requested_model)
    return (
        f"Global default model updated to **{get_model_tier_label(updated)}** (`{updated}`). "
        "New direct, queued, and scheduled work will use it."
    )
