"""Provider IDs, labels, and chat-scoped runtime preference helpers."""

from __future__ import annotations

import os
from typing import Any

VALID_PROVIDER_IDS = ("claude", "codex", "zai", "openrouter")
WEBAPP_CHAT_ID = "webapp"

_PROVIDER_LABELS = {
    "claude": "Claude Code",
    "codex": "Codex",
    "zai": "Z.AI",
    "openrouter": "OpenRouter",
}

_PROVIDER_ALIASES = {
    "anthropic": "claude",
    "claude": "claude",
    "claude-code": "claude",
    "chatgpt": "codex",
    "codex": "codex",
    "openai": "codex",
    "open-router": "openrouter",
    "openrouter": "openrouter",
    "openrouter.ai": "openrouter",
    "z-ai": "zai",
    "z.ai": "zai",
    "zai": "zai",
}


def normalize_provider_id(value: str | None, fallback: str = "claude") -> str:
    """Normalize a user or config supplied provider ID."""
    if value is None:
        return fallback
    normalized = _PROVIDER_ALIASES.get(str(value).strip().lower(), "")
    if normalized in VALID_PROVIDER_IDS:
        return normalized
    return fallback


def get_default_provider_id() -> str:
    """Return the configured default provider, falling back to Claude."""
    return normalize_provider_id(os.getenv("KB_DEFAULT_PROVIDER"), fallback="claude")


def get_provider_label(provider_id: str) -> str:
    """Return a human-readable label for a provider ID."""
    normalized = normalize_provider_id(provider_id)
    return _PROVIDER_LABELS[normalized]


def get_provider_metadata(provider_id: str) -> dict[str, Any]:
    """Return the stable provider catalog entry for UI and runtime use."""
    from gateway.provider_capabilities import get_provider_capabilities

    normalized = normalize_provider_id(provider_id)
    metadata: dict[str, Any] = {
        "id": normalized,
        "label": get_provider_label(normalized),
    }
    metadata.update(get_provider_capabilities(normalized))
    return metadata


def list_provider_metadata() -> list[dict[str, Any]]:
    """Return the stable provider catalog for UI and help text."""
    return [get_provider_metadata(provider_id) for provider_id in VALID_PROVIDER_IDS]


def build_chat_session_key(chat_id: str | None) -> str:
    """Return the persisted chat session key used for session state."""
    normalized = str(chat_id or "").strip() or "default"
    return f"chat_{normalized}"
