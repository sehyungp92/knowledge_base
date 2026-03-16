"""Stable provider capability metadata used by runtime selection and UI."""

from __future__ import annotations

from typing import Any

from gateway.providers import VALID_PROVIDER_IDS, normalize_provider_id

PROVIDER_CAPABILITIES: dict[str, dict[str, Any]] = {
    "claude": {
        "auth_mode": "subscription_or_api",
        "transport": "cli",
        "cli_family": "claude",
        "supports_resume": True,
        "supports_native_fallbacks": True,
        "supports_partial_messages": True,
    },
    "codex": {
        "auth_mode": "subscription_or_api",
        "transport": "cli",
        "cli_family": "codex",
        "supports_resume": True,
        "supports_native_fallbacks": False,
        "supports_partial_messages": False,
    },
    "zai": {
        "auth_mode": "api_key",
        "transport": "claude_cli_compat",
        "cli_family": "claude",
        "supports_resume": True,
        "supports_native_fallbacks": False,
        "supports_partial_messages": True,
    },
    "openrouter": {
        "auth_mode": "api_key",
        "transport": "api",
        "cli_family": None,
        "supports_resume": True,
        "supports_native_fallbacks": True,
        "supports_partial_messages": False,
    },
}


def get_provider_capabilities(provider_id: str) -> dict[str, Any]:
    """Return capability metadata for a normalized provider."""
    normalized = normalize_provider_id(provider_id)
    return dict(PROVIDER_CAPABILITIES[normalized])


def list_provider_capabilities() -> list[dict[str, Any]]:
    """Return the full capability table in stable provider order."""
    return [
        {"id": provider_id, **get_provider_capabilities(provider_id)}
        for provider_id in VALID_PROVIDER_IDS
    ]


def uses_claude_cli_family(provider_id: str) -> bool:
    """Return True when the provider currently speaks Claude CLI semantics."""
    capabilities = get_provider_capabilities(provider_id)
    return (
        capabilities.get("cli_family") == "claude"
        and capabilities.get("transport") in {"cli", "claude_cli_compat"}
    )
