"""Tests for the local runtime controller."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from scripts import runtime_ctl


def test_parse_args_for_gateway_start():
    args = runtime_ctl._parse_args(["start", "--component", "gateway"])

    assert args.command == "start"
    assert args.component == "gateway"


def test_component_names_for_all():
    assert runtime_ctl._component_names("all") == ["gateway", "api"]


def test_build_install_task_script_contains_runtime_start(monkeypatch):
    monkeypatch.setattr(runtime_ctl.sys, "executable", r"C:\Python\python.exe")
    monkeypatch.setattr(runtime_ctl, "PROJECT_ROOT", Path(r"C:\kb"))
    monkeypatch.setattr(runtime_ctl.getpass, "getuser", lambda: "kb-user")

    script = runtime_ctl._build_install_task_script()

    assert "scripts.runtime_ctl start --component all" in script
    assert "KnowledgeBase Local Runtime" in script
    assert "kb-user" in script


def test_ensure_postgres_ready_runs_compose_and_waits(monkeypatch, tmp_path):
    docker_dir = tmp_path / "docker"
    docker_dir.mkdir()
    monkeypatch.setattr(runtime_ctl, "PROJECT_ROOT", tmp_path)

    run_calls = []

    def fake_run(command, **kwargs):
        run_calls.append(command)
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(runtime_ctl.subprocess, "run", fake_run)
    monkeypatch.setattr(runtime_ctl, "wait_for_postgres", lambda dsn, timeout: (True, ""))

    ok, last_error = runtime_ctl._ensure_postgres_ready(
        SimpleNamespace(postgres_dsn="postgresql://example", runtime_db_wait_seconds=30)
    )

    assert ok is True
    assert last_error == ""
    assert run_calls[0] == ["docker", "compose", "up", "-d", "postgres"]
