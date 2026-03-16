"""Shared types, constants, and utilities for the agent executor subsystem."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

import structlog

logger = structlog.get_logger(__name__)

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WORKSPACE = _PROJECT_ROOT / "workspace"


# ---------------------------------------------------------------------------
# Environment helpers
# ---------------------------------------------------------------------------


def _env_int(*keys: str, default: int) -> int:
    for key in keys:
        raw = os.environ.get(key)
        if raw and raw.strip():
            try:
                return int(raw)
            except ValueError:
                logger.warning("env_int_invalid", key=key, value=raw)
    return default


def _env_float(*keys: str, default: float) -> float:
    for key in keys:
        raw = os.environ.get(key)
        if raw and raw.strip():
            try:
                return float(raw)
            except ValueError:
                logger.warning("env_float_invalid", key=key, value=raw)
    return default


def _env_bool(*keys: str, default: bool) -> bool:
    for key in keys:
        raw = os.environ.get(key)
        if raw and raw.strip():
            return raw.strip().lower() not in {"0", "false", "no", "off"}
    return default


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CliBackendConfig:
    """Configuration for a supported CLI backend."""

    id: str
    command: str
    command_env_var: str
    args: tuple[str, ...]
    resume_args: tuple[str, ...] | None = None
    input_mode: str = "stdin"
    output_mode: str = "stream-json"
    resume_output_mode: str | None = None
    model_arg: str | None = "--model"
    model_aliases: dict[str, str] = field(default_factory=dict)
    clear_env: tuple[str, ...] = ()
    required_env: tuple[str, ...] = ()


@dataclass
class ExecutionResult:
    """Result of a CLI execution."""

    stdout: str
    stderr: str
    return_code: int
    text: str
    cost_usd: float | None
    usage: dict | None
    session_id_out: str | None = None
    failure_type: str | None = None
    backend_id: str = "claude"

    @property
    def success(self) -> bool:
        return self.return_code == 0

    @property
    def is_timeout(self) -> bool:
        return "Timeout" in self.stderr


# ---------------------------------------------------------------------------
# Model aliases
# ---------------------------------------------------------------------------

CLAUDE_MODEL_ALIASES: dict[str, str] = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
    "opus": "claude-opus-4-6",
}

CODEX_MODEL_ALIASES: dict[str, str] = {
    "haiku": "gpt-5.1-codex-mini",
    "sonnet": "gpt-5.1-codex",
    "opus": "gpt-5.1-codex",
}

ZAI_MODEL_DEFAULTS: dict[str, str] = {
    "haiku": "GLM-4.5-Air",
    "sonnet": "GLM-4.7",
    "opus": "GLM-4.7",
}

OPENROUTER_MODEL_DEFAULTS: dict[str, str] = {
    "haiku": "minimax/minimax-m2.5",
    "sonnet": "minimax/minimax-m2.5",
    "opus": "minimax/minimax-m2.5",
}


def _zai_model_aliases() -> dict[str, str]:
    return {
        "haiku": os.getenv("ZAI_MODEL_FAST", ZAI_MODEL_DEFAULTS["haiku"]).strip(),
        "sonnet": os.getenv("ZAI_MODEL_BALANCED", ZAI_MODEL_DEFAULTS["sonnet"]).strip(),
        "opus": os.getenv("ZAI_MODEL_DEEP", ZAI_MODEL_DEFAULTS["opus"]).strip(),
    }


def _openrouter_model_aliases() -> dict[str, str]:
    return {
        "haiku": os.getenv("OPENROUTER_MODEL_FAST", OPENROUTER_MODEL_DEFAULTS["haiku"]).strip(),
        "sonnet": os.getenv("OPENROUTER_MODEL_BALANCED", OPENROUTER_MODEL_DEFAULTS["sonnet"]).strip(),
        "opus": os.getenv("OPENROUTER_MODEL_DEEP", OPENROUTER_MODEL_DEFAULTS["opus"]).strip(),
    }


# ---------------------------------------------------------------------------
# CLI backend configs
# ---------------------------------------------------------------------------

_CLAUDE_CLI_COMMON_ARGS: tuple[str, ...] = (
    "--dangerously-skip-permissions",
    "--output-format",
    "stream-json",
    "--verbose",
    "--print",
    "--setting-sources",
    "project,local",
    "--strict-mcp-config",
)

CLI_BACKENDS: dict[str, CliBackendConfig] = {
    "claude": CliBackendConfig(
        id="claude",
        command="claude",
        command_env_var="CLAUDE_CLI_PATH",
        args=_CLAUDE_CLI_COMMON_ARGS,
    ),
    "codex": CliBackendConfig(
        id="codex",
        command="codex",
        command_env_var="CODEX_CLI_PATH",
        args=(
            "exec",
            "--json",
            "--color",
            "never",
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
        ),
        resume_args=(
            "exec",
            "resume",
            "{sessionId}",
            "--color",
            "never",
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
        ),
        input_mode="arg",
        output_mode="jsonl",
        resume_output_mode="text",
        model_aliases=CODEX_MODEL_ALIASES,
    ),
    "zai": CliBackendConfig(
        id="zai",
        command="claude",
        command_env_var="CLAUDE_CLI_PATH",
        args=_CLAUDE_CLI_COMMON_ARGS,
        clear_env=("ANTHROPIC_API_KEY_OLD",),
        required_env=("ZAI_API_KEY",),
    ),
    # OpenRouter uses native API transport (openrouter_client.py), not Claude CLI.
    # This minimal config exists only for availability probes in get_backend_statuses().
    "openrouter": CliBackendConfig(
        id="openrouter",
        command="openrouter",
        command_env_var="OPENROUTER_CLI_PATH",
        args=(),
        required_env=("OPENROUTER_API_KEY",),
    ),
}

# ---------------------------------------------------------------------------
# Shared constants
# ---------------------------------------------------------------------------

_RETRYABLE_TEXT_PATTERNS = (
    "rate_limit",
    "overloaded",
    "internal_error",
    "server_error",
)
_RETRYABLE_CODE_RE = re.compile(r"\b(429|500|502|503|529)\b")
_PROGRESS_INTERVAL_S = 10

_CLAUDE_TIER_EFFORT: dict[str, str] = {
    "haiku": "low",
    "sonnet": "medium",
    "opus": "high",
}
_CLAUDE_TIER_FALLBACK: dict[str, str] = {
    "sonnet": "haiku",
    "opus": "sonnet",
}
