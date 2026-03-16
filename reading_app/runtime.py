"""Shared local runtime helpers for background processes and state."""

from __future__ import annotations

import atexit
import ctypes
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import psycopg

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VAR_DIR = PROJECT_ROOT / "var"
RUNTIME_DIR = VAR_DIR / "runtime"


@dataclass(frozen=True)
class ProcessFiles:
    """Filesystem paths for a managed local process."""

    name: str
    pid_file: Path
    ready_file: Path
    shutdown_file: Path
    log_file: Path


def get_runtime_log_dir() -> Path:
    """Return the configured runtime log directory."""
    return Path(os.getenv("RUNTIME_LOG_DIR", RUNTIME_DIR / "logs"))


def get_runtime_db_path() -> Path:
    """Return the configured runtime SQLite DB path."""
    return Path(os.getenv("RUNTIME_DB_PATH", RUNTIME_DIR / "runtime.db"))


def get_process_files(name: str) -> ProcessFiles:
    """Return PID, shutdown, and log file locations for a named process."""
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    log_dir = get_runtime_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    return ProcessFiles(
        name=name,
        pid_file=RUNTIME_DIR / f"{name}.pid",
        ready_file=RUNTIME_DIR / f"{name}.ready",
        shutdown_file=RUNTIME_DIR / f"{name}.shutdown",
        log_file=log_dir / f"{name}.log",
    )


def _pid_exists(pid: int) -> bool:
    """Return whether a process ID is alive on the current platform."""
    if pid <= 0:
        return False

    if os.name == "nt":
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        access = 0x1000 | 0x00100000  # QUERY_LIMITED_INFORMATION | SYNCHRONIZE
        handle = kernel32.OpenProcess(access, False, pid)
        if handle:
            kernel32.CloseHandle(handle)
            return True
        return ctypes.get_last_error() == 5  # Access denied can still mean the PID exists.

    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def read_live_pid(pid_file: Path) -> int | None:
    """Return the live PID from a PID file, cleaning up stale files."""
    if not pid_file.exists():
        return None
    try:
        pid = int(pid_file.read_text(encoding="utf-8").strip())
        if not _pid_exists(pid):
            raise OSError("stale pid")
        return pid
    except (ValueError, OSError, SystemError):
        pid_file.unlink(missing_ok=True)
        return None


def acquire_pid_lock(name: str) -> ProcessFiles:
    """Create the PID file for a process, raising if a live instance exists."""
    files = get_process_files(name)
    live_pid = read_live_pid(files.pid_file)
    if live_pid is not None:
        raise RuntimeError(f"{name} is already running (PID {live_pid})")

    files.shutdown_file.unlink(missing_ok=True)
    files.ready_file.unlink(missing_ok=True)
    files.pid_file.write_text(str(os.getpid()), encoding="utf-8")

    def _cleanup() -> None:
        files.pid_file.unlink(missing_ok=True)
        files.ready_file.unlink(missing_ok=True)

    atexit.register(_cleanup)
    return files


def mark_process_ready(files: ProcessFiles) -> None:
    """Write the ready marker for a managed process."""
    files.ready_file.write_text(str(time.time()), encoding="utf-8")


def clear_process_ready(files: ProcessFiles) -> None:
    """Remove the ready marker for a managed process."""
    files.ready_file.unlink(missing_ok=True)


def request_shutdown(name: str) -> bool:
    """Write the graceful shutdown marker for a named process."""
    files = get_process_files(name)
    pid = read_live_pid(files.pid_file)
    if pid is None:
        return False
    files.shutdown_file.write_text("stop", encoding="utf-8")
    return True


def wait_for_process_exit(name: str, timeout_s: float = 30.0) -> bool:
    """Wait for a managed process to exit."""
    files = get_process_files(name)
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if read_live_pid(files.pid_file) is None:
            return True
        time.sleep(0.5)
    return read_live_pid(files.pid_file) is None


def wait_for_process_ready(name: str, timeout_s: float = 30.0) -> bool:
    """Wait for a managed process to report readiness."""
    files = get_process_files(name)
    deadline = time.monotonic() + timeout_s
    seen_live_pid = False
    while time.monotonic() < deadline:
        live_pid = read_live_pid(files.pid_file)
        if live_pid is None:
            if seen_live_pid:
                return False
            time.sleep(0.5)
            continue
        seen_live_pid = True
        if files.ready_file.exists():
            return True
        time.sleep(0.5)
    return files.ready_file.exists() and read_live_pid(files.pid_file) is not None


def detached_popen_kwargs() -> dict[str, Any]:
    """Return subprocess kwargs for detached background execution."""
    if os.name == "nt":
        creationflags = (
            getattr(subprocess, "DETACHED_PROCESS", 0)
            | getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        )
        return {"creationflags": creationflags, "close_fds": True}
    return {"start_new_session": True}


def launch_background_process(
    command: list[str],
    *,
    cwd: Path,
    log_file: Path,
    env: dict[str, str] | None = None,
) -> subprocess.Popen:
    """Launch a detached process with stdout/stderr redirected to a log file."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    stream = open(log_file, "a", encoding="utf-8")
    try:
        process = subprocess.Popen(
            command,
            cwd=str(cwd),
            stdin=subprocess.DEVNULL,
            stdout=stream,
            stderr=subprocess.STDOUT,
            env=env,
            **detached_popen_kwargs(),
        )
    finally:
        stream.close()
    return process


def wait_for_postgres(dsn: str, timeout_s: int, *, interval_s: float = 2.0) -> tuple[bool, str]:
    """Poll PostgreSQL until it becomes reachable or the timeout elapses."""
    deadline = time.monotonic() + timeout_s
    last_error = ""
    while time.monotonic() < deadline:
        try:
            with psycopg.connect(dsn, connect_timeout=5):
                return True, ""
        except Exception as exc:  # pragma: no cover - exact psycopg errors vary by host
            last_error = str(exc)
            time.sleep(interval_s)
    return False, last_error


def python_command_for_module(module: str, *args: str) -> list[str]:
    """Build a Python module execution command using the current interpreter."""
    return [sys.executable, "-m", module, *args]
