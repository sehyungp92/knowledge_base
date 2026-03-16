"""CLI path resolution and Windows .cmd bypass for agent backends."""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import structlog

from agents.backend_config import CliBackendConfig

logger = structlog.get_logger(__name__)


def _path_runnable(path: str) -> bool:
    try:
        return Path(path).exists() and os.access(path, os.X_OK)
    except (OSError, ValueError):
        return False


def find_cli_path(backend: CliBackendConfig) -> str:
    """Locate the CLI executable for a backend."""
    explicit = os.environ.get(backend.command_env_var)
    if explicit:
        explicit_path = Path(explicit).expanduser()
        if explicit_path.exists():
            if not _path_runnable(str(explicit_path)):
                raise PermissionError(
                    f"{backend.command_env_var} points to a non-runnable executable: {explicit_path}"
                )
            return str(explicit_path)
        raise FileNotFoundError(
            f"{backend.command_env_var} points to a missing executable: {explicit_path}"
        )

    found = shutil.which(backend.command)
    if found and not found.lower().endswith(".ps1") and _path_runnable(found):
        return found

    if backend.command in ("claude", "codex"):
        npm_cmd = Path.home() / "AppData" / "Roaming" / "npm" / f"{backend.command}.cmd"
        if npm_cmd.exists() and _path_runnable(str(npm_cmd)):
            return str(npm_cmd)

    raise FileNotFoundError(
        f"{backend.command} CLI not found. Install it or set {backend.command_env_var}."
    )


def resolve_cli_exec(backend: CliBackendConfig) -> list[str]:
    """Return the full command prefix (node + cli.js or raw path) for a backend."""
    path = find_cli_path(backend)
    if backend.command != "claude":
        return [path]
    if not path.lower().endswith(".cmd"):
        return [path]

    cmd_dir = Path(path).resolve().parent
    cli_js = cmd_dir / "node_modules" / "@anthropic-ai" / "claude-code" / "cli.js"
    if not cli_js.exists():
        logger.warning("cli_js_not_found", backend_id=backend.id, expected=str(cli_js))
        return ["cmd.exe", "/c", path]

    node_local = cmd_dir / "node.exe"
    node = str(node_local) if node_local.exists() else shutil.which("node")
    if not node:
        logger.warning("node_exe_not_found", backend_id=backend.id)
        return ["cmd.exe", "/c", path]

    logger.info(
        "cli_resolved_direct",
        backend_id=backend.id,
        node=node,
        cli_js=str(cli_js),
    )
    return [node, str(cli_js)]
