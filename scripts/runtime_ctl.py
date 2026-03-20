"""Local runtime controller for the gateway and API."""

from __future__ import annotations

import argparse
import getpass
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from reading_app.config import Config
from reading_app.runtime import (
    PROJECT_ROOT,
    get_process_files,
    launch_background_process,
    python_command_for_module,
    read_live_pid,
    request_shutdown,
    wait_for_postgres,
    wait_for_process_exit,
    wait_for_process_ready,
)

_TASK_NAME = "KnowledgeBase Local Runtime"

_COMPONENTS = {
    "gateway": "gateway.main",
    "api": "webapp.api.server",
}


def _component_names(selection: str) -> list[str]:
    if selection == "all":
        return ["gateway", "api"]
    if selection not in _COMPONENTS:
        raise ValueError(f"Unknown component: {selection}")
    return [selection]


def _ensure_postgres_ready(config: Config) -> tuple[bool, str]:
    docker_dir = PROJECT_ROOT / "docker"
    compose_attempts = (
        ["docker", "compose", "up", "-d", "postgres"],
        ["docker-compose", "up", "-d", "postgres"],
    )

    for command in compose_attempts:
        try:
            completed = subprocess.run(
                command,
                cwd=str(docker_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
        except OSError:
            continue
        if completed.returncode == 0:
            break

    return wait_for_postgres(config.postgres_dsn, config.runtime_db_wait_seconds)


def _start_components(selection: str) -> int:
    config = Config()
    ok, last_error = _ensure_postgres_ready(config)
    if not ok:
        print(
            "PostgreSQL is not ready yet.\n"
            f"Waited {config.runtime_db_wait_seconds}s for {config.postgres_dsn}.\n"
            f"Last error: {last_error or 'unknown'}",
            file=sys.stderr,
        )
        return 1

    exit_code = 0
    for name in _component_names(selection):
        files = get_process_files(name)
        live_pid = read_live_pid(files.pid_file)
        if live_pid is not None:
            if files.ready_file.exists():
                print(f"{name}: already running (PID {live_pid})")
            else:
                print(f"{name}: running but still initializing (PID {live_pid})")
            continue

        command = python_command_for_module(_COMPONENTS[name])
        launch_background_process(command, cwd=PROJECT_ROOT, log_file=files.log_file, env=os.environ.copy())

        ready = wait_for_process_ready(name, timeout_s=45.0)
        live_pid = read_live_pid(files.pid_file)

        if live_pid is None or not ready:
            print(f"{name}: failed to become ready, check {files.log_file}", file=sys.stderr)
            exit_code = 1
        else:
            print(f"{name}: started (PID {live_pid})")

    return exit_code


def _stop_components(selection: str, timeout_s: float = 45.0) -> int:
    exit_code = 0
    for name in _component_names(selection):
        files = get_process_files(name)
        pid = read_live_pid(files.pid_file)
        if pid is None:
            print(f"{name}: not running")
            continue

        request_shutdown(name)
        if wait_for_process_exit(name, timeout_s=timeout_s):
            print(f"{name}: stopped")
        else:
            print(f"{name}: did not stop within {timeout_s:.0f}s, check {files.log_file}", file=sys.stderr)
            exit_code = 1
    return exit_code


def _status_components(selection: str) -> int:
    for name in _component_names(selection):
        files = get_process_files(name)
        pid = read_live_pid(files.pid_file)
        if pid is None:
            print(f"{name}: stopped")
        elif files.ready_file.exists():
            print(f"{name}: running (PID {pid}) log={files.log_file}")
        else:
            print(f"{name}: starting (PID {pid}) log={files.log_file}")
    return 0


def _restart_components(selection: str) -> int:
    stop_code = _stop_components(selection)
    start_code = _start_components(selection)
    return 1 if stop_code or start_code else 0


def _ps_quote(value: str) -> str:
    return value.replace("'", "''")


def _build_install_task_script() -> str:
    python_path = _ps_quote(sys.executable)
    working_dir = _ps_quote(str(PROJECT_ROOT))
    username = _ps_quote(getpass.getuser())
    argument = _ps_quote("-m scripts.runtime_ctl start --component all")
    task_name = _ps_quote(_TASK_NAME)

    return "\n".join(
        [
            f"$action = New-ScheduledTaskAction -Execute '{python_path}' -Argument '{argument}' -WorkingDirectory '{working_dir}'",
            f"$trigger = New-ScheduledTaskTrigger -AtLogOn -User '{username}'",
            (
                "$settings = New-ScheduledTaskSettingsSet "
                "-AllowStartIfOnBatteries "
                "-DontStopIfGoingOnBatteries "
                "-MultipleInstances IgnoreNew "
                "-RestartCount 3 "
                "-RestartInterval (New-TimeSpan -Minutes 5) "
                "-Hidden"
            ),
            (
                f"Register-ScheduledTask -TaskName '{task_name}' -Action $action -Trigger $trigger "
                "-Settings $settings -Description 'Starts the knowledge_base local runtime at Windows logon.' -Force | Out-Null"
            ),
        ]
    )


def _build_uninstall_task_script() -> str:
    task_name = _ps_quote(_TASK_NAME)
    return (
        f"if (Get-ScheduledTask -TaskName '{task_name}' -ErrorAction SilentlyContinue) "
        f"{{ Unregister-ScheduledTask -TaskName '{task_name}' -Confirm:$false }}"
    )


def _run_powershell(script: str) -> int:
    if os.name != "nt":
        print("Task Scheduler integration is only supported on Windows.", file=sys.stderr)
        return 1
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        cwd=str(PROJECT_ROOT),
        check=False,
    )
    return completed.returncode


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Manage the local knowledge_base runtime.")
    parser.add_argument(
        "command",
        choices=["start", "stop", "restart", "status", "install-login-task", "uninstall-login-task"],
    )
    parser.add_argument(
        "--component",
        default="all",
        choices=["all", "gateway", "api"],
        help="Which runtime component(s) to operate on.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv or sys.argv[1:])

    if args.command == "start":
        return _start_components(args.component)
    if args.command == "stop":
        return _stop_components(args.component)
    if args.command == "restart":
        return _restart_components(args.component)
    if args.command == "status":
        return _status_components(args.component)
    if args.command == "install-login-task":
        return _run_powershell(_build_install_task_script())
    if args.command == "uninstall-login-task":
        return _run_powershell(_build_uninstall_task_script())
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
