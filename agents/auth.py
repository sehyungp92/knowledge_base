"""Authentication status checking for Claude and Codex backends."""

from __future__ import annotations

import base64
import json
import os
import subprocess
import threading
import time
from pathlib import Path
from typing import Any

import structlog

from agents.backend_config import CLI_BACKENDS, _env_float
from agents.cli_resolver import resolve_cli_exec

logger = structlog.get_logger(__name__)

_claude_auth_cache: dict[str, Any] = {"checked_at": 0.0, "status": None}
_claude_auth_lock = threading.Lock()
_codex_auth_cache: dict[str, Any] = {"checked_at": 0.0, "status": None}
_codex_auth_lock = threading.Lock()


def _decode_jwt_payload(token: str) -> dict[str, Any] | None:
    """Decode a JWT payload without verification for local status metadata only."""
    try:
        parts = token.split(".")
        if len(parts) < 2:
            return None
        payload = parts[1]
        payload += "=" * (-len(payload) % 4)
        raw = base64.urlsafe_b64decode(payload.encode("ascii"))
        decoded = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError):
        return None
    return decoded if isinstance(decoded, dict) else None


def has_claude_env_auth() -> bool:
    return bool(
        os.getenv("ANTHROPIC_API_KEY", "").strip()
        or os.getenv("ANTHROPIC_AUTH_TOKEN", "").strip()
    )


def has_codex_env_auth() -> bool:
    return bool(os.getenv("OPENAI_API_KEY", "").strip())


def get_claude_auth_status(*, force_refresh: bool = False) -> dict[str, Any] | None:
    ttl_s = _env_float("KB_CLAUDE_AUTH_STATUS_TTL_S", default=30.0)
    now = time.monotonic()

    with _claude_auth_lock:
        cached_status = _claude_auth_cache.get("status")
        checked_at = float(_claude_auth_cache.get("checked_at") or 0.0)
        if (
            not force_refresh
            and cached_status is not None
            and now - checked_at < ttl_s
        ):
            return cached_status

    try:
        backend = CLI_BACKENDS["claude"]
        result = subprocess.run(
            resolve_cli_exec(backend) + ["auth", "status", "--json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
            env=os.environ.copy(),
        )
    except (FileNotFoundError, PermissionError, OSError, subprocess.TimeoutExpired) as exc:
        logger.debug("claude_auth_status_unavailable", error=str(exc))
        status = None
    else:
        if result.returncode != 0:
            logger.debug(
                "claude_auth_status_failed",
                return_code=result.returncode,
                stderr=result.stderr[:200],
            )
            status = None
        else:
            try:
                raw_status = json.loads(result.stdout)
            except json.JSONDecodeError:
                logger.debug("claude_auth_status_invalid_json")
                status = None
            else:
                status = raw_status if isinstance(raw_status, dict) else None

    with _claude_auth_lock:
        _claude_auth_cache["checked_at"] = now
        _claude_auth_cache["status"] = status

    return status


def codex_auth_file_path() -> Path:
    return Path.home() / ".codex" / "auth.json"


def read_codex_auth_file() -> dict[str, Any] | None:
    auth_path = codex_auth_file_path()
    if not auth_path.exists():
        return None

    try:
        raw = json.loads(auth_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        logger.debug("codex_auth_status_invalid_file", path=str(auth_path))
        return None

    if not isinstance(raw, dict):
        return None

    auth_mode = str(raw.get("auth_mode") or "").strip().lower()
    tokens = raw.get("tokens")
    token_map = tokens if isinstance(tokens, dict) else {}
    access_token = str(token_map.get("access_token") or "").strip()
    embedded_api_key = str(raw.get("OPENAI_API_KEY") or "").strip()

    status: dict[str, Any] = {
        "loggedIn": False,
        "authMethod": "api_key" if embedded_api_key else auth_mode or None,
    }

    if embedded_api_key:
        status["loggedIn"] = True
        status["subscriptionType"] = "api_key"
        return status

    if auth_mode == "chatgpt" and access_token:
        status["loggedIn"] = True
        payload = _decode_jwt_payload(access_token) or {}
        auth_data = payload.get("https://api.openai.com/auth")
        auth_section = auth_data if isinstance(auth_data, dict) else {}
        plan_type = str(auth_section.get("chatgpt_plan_type") or "").strip().lower()
        if plan_type:
            status["subscriptionType"] = plan_type
        return status

    return status if status["authMethod"] else None


def get_codex_auth_status(*, force_refresh: bool = False) -> dict[str, Any] | None:
    ttl_s = _env_float("KB_CODEX_AUTH_STATUS_TTL_S", default=30.0)
    now = time.monotonic()

    with _codex_auth_lock:
        cached_status = _codex_auth_cache.get("status")
        checked_at = float(_codex_auth_cache.get("checked_at") or 0.0)
        if (
            not force_refresh
            and cached_status is not None
            and now - checked_at < ttl_s
        ):
            return cached_status

    status = read_codex_auth_file()

    with _codex_auth_lock:
        _codex_auth_cache["checked_at"] = now
        _codex_auth_cache["status"] = status

    return status
