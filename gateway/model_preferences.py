"""Global model tier metadata and runtime preference helpers."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

VALID_MODEL_TIERS = ("haiku", "sonnet", "opus")
DEFAULT_MODEL_TIER = "sonnet"
DEFAULT_MODEL_PREFERENCE_KEY = "default_model"

_MODEL_TIER_ALIASES = {
    "fast": "haiku",
    "haiku": "haiku",
    "mini": "haiku",
    "balanced": "sonnet",
    "default": "sonnet",
    "medium": "sonnet",
    "sonnet": "sonnet",
    "deep": "opus",
    "max": "opus",
    "opus": "opus",
    "quality": "opus",
}

_MODEL_TIER_METADATA = {
    "haiku": {
        "label": "Fast",
        "description": "Lowest-latency tier for lighter tasks.",
    },
    "sonnet": {
        "label": "Balanced",
        "description": "Best default balance of speed and reasoning.",
    },
    "opus": {
        "label": "Deep",
        "description": "Highest-effort tier for the most complex work.",
    },
}


def match_model_tier(value: str | None) -> str | None:
    """Return the canonical model tier for a user-friendly alias."""
    if value is None:
        return None
    return _MODEL_TIER_ALIASES.get(str(value).strip().lower())


def normalize_model_tier(value: str | None, fallback: str = DEFAULT_MODEL_TIER) -> str:
    """Normalize a model tier, falling back to the configured default tier."""
    matched = match_model_tier(value)
    if matched in VALID_MODEL_TIERS:
        return matched
    return fallback


def resolve_model_selector(value: str | None) -> str:
    """Resolve a caller-supplied model selector into a tier or raw model string."""
    if value is None or not str(value).strip():
        return get_effective_default_model_tier()
    matched = match_model_tier(value)
    if matched:
        return matched
    return str(value).strip()


def get_model_tier_label(model_tier: str) -> str:
    """Return the UI label for a canonical model tier."""
    return _MODEL_TIER_METADATA[normalize_model_tier(model_tier)]["label"]


def list_model_tier_metadata() -> list[dict[str, str]]:
    """Return stable metadata for the supported model tiers."""
    return [
        {
            "id": model_tier,
            "label": _MODEL_TIER_METADATA[model_tier]["label"],
            "description": _MODEL_TIER_METADATA[model_tier]["description"],
        }
        for model_tier in VALID_MODEL_TIERS
    ]


def get_config_default_model_tier() -> str:
    """Return the env-configured default model tier."""
    return normalize_model_tier(os.getenv("KB_DEFAULT_MODEL"), fallback=DEFAULT_MODEL_TIER)


def _queue_db_path(db_path: Path | str | None = None) -> Path:
    if db_path is not None:
        return Path(db_path)
    from gateway.queue import DEFAULT_QUEUE_DB_PATH

    return Path(DEFAULT_QUEUE_DB_PATH)


def _read_global_preference(key: str, db_path: Path | str | None = None) -> str | None:
    queue_db_path = _queue_db_path(db_path)
    if not queue_db_path.exists():
        return None

    conn = sqlite3.connect(queue_db_path)
    conn.row_factory = sqlite3.Row
    try:
        row = conn.execute(
            "SELECT value FROM global_runtime_preferences WHERE key = ?",
            (key,),
        ).fetchone()
        if row is None:
            return None
        return str(row["value"]).strip()
    except sqlite3.DatabaseError:
        return None
    finally:
        conn.close()


def get_persisted_default_model_tier(db_path: Path | str | None = None) -> str | None:
    """Return the persisted runtime default model tier, if one exists."""
    stored = _read_global_preference(DEFAULT_MODEL_PREFERENCE_KEY, db_path=db_path)
    if not stored:
        return None
    return normalize_model_tier(stored, fallback=DEFAULT_MODEL_TIER)


def get_effective_default_model_tier(db_path: Path | str | None = None) -> str:
    """Return the runtime default model tier with env fallback."""
    return get_persisted_default_model_tier(db_path=db_path) or get_config_default_model_tier()
