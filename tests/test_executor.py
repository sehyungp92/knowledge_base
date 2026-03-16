"""Tests for agents.executor."""

import json
import time
from pathlib import Path

from agents.executor import (
    ClaudeExecutor,
    CODEX_MODEL_ALIASES,
    CLICircuitBreaker,
    ExecutionResult,
    CLAUDE_MODEL_ALIASES,
)
from gateway.provider_capabilities import get_provider_capabilities
from gateway.queue import Queue


def test_model_aliases():
    assert "haiku" in CLAUDE_MODEL_ALIASES
    assert "sonnet" in CLAUDE_MODEL_ALIASES
    assert "opus" in CLAUDE_MODEL_ALIASES


def test_execution_result_success():
    result = ExecutionResult("out", "", 0, "hello", 0.001, {"input_tokens": 10})
    assert result.success is True
    assert result.failure_type is None


def test_execution_result_failure():
    result = ExecutionResult("", "err", 1, "", None, None)
    assert result.success is False


def test_execution_result_failure_type():
    result = ExecutionResult("", "Timeout", 1, "", None, None, failure_type="timeout")
    assert result.is_timeout
    assert result.failure_type == "timeout"

    result2 = ExecutionResult("", "", 1, "", None, None, failure_type="hook_instability")
    assert result2.failure_type == "hook_instability"

    result3 = ExecutionResult("", "circuit breaker open", 1, "", None, None, failure_type="circuit_breaker_open")
    assert result3.failure_type == "circuit_breaker_open"


def test_session_dir(tmp_path):
    executor = ClaudeExecutor(tmp_path / "workspace", default_backend_id="claude")
    sd = executor.session_dir("test_session")
    assert sd.exists()
    assert sd.name == "claude__test_session"


def test_parse_stream_json():
    executor = ClaudeExecutor(Path("/tmp/test"))
    stdout = '{"type": "assistant", "text": "partial"}\n{"type": "result", "result": "final answer", "cost_usd": 0.005, "usage": {"input_tokens": 100, "output_tokens": 50}}\n'
    text, cost, usage, session_id = executor._parse_stream_json(stdout)
    assert text == "final answer"
    assert cost == 0.005
    assert usage["input_tokens"] == 100


def test_parse_stream_json_empty():
    executor = ClaudeExecutor(Path("/tmp/test"))
    text, cost, usage, session_id = executor._parse_stream_json("")
    assert text == ""
    assert cost is None


def test_parse_stream_json_malformed():
    executor = ClaudeExecutor(Path("/tmp/test"))
    text, cost, usage, session_id = executor._parse_stream_json("not json\nalso not json\n")
    assert text == ""


def test_build_prompt():
    executor = ClaudeExecutor(Path("/tmp/test"))
    prompt = executor.build_prompt(
        "human_message",
        {"text": "hello"},
        "You are a helpful assistant.",
        "Memory context here.",
    )
    assert "Memory context here." in prompt
    assert "human_message" in prompt
    assert "hello" in prompt
    assert "You are a helpful assistant." in prompt
    assert "UNTRUSTED_CONTENT" in prompt


# ── Circuit Breaker Tests ─────────────────────────────────────────────


def test_circuit_breaker_closed_by_default():
    cb = CLICircuitBreaker(backend_id="claude", threshold=3, cooldown_s=10)
    assert cb.state == "closed"
    assert cb.allow_request() is True
    assert cb.is_open() is False


def test_circuit_breaker_opens_after_threshold():
    cb = CLICircuitBreaker(backend_id="claude", threshold=3, cooldown_s=10)
    cb.record_failure()
    cb.record_failure()
    assert cb.state == "closed"
    cb.record_failure()
    assert cb.state == "open"
    assert cb.allow_request() is False
    assert cb.is_open() is True


def test_circuit_breaker_success_resets():
    cb = CLICircuitBreaker(backend_id="claude", threshold=3, cooldown_s=10)
    cb.record_failure()
    cb.record_failure()
    cb.record_success()
    assert cb.state == "closed"
    # Should need 3 more failures to open
    cb.record_failure()
    cb.record_failure()
    assert cb.state == "closed"


def test_circuit_breaker_half_open_after_cooldown():
    cb = CLICircuitBreaker(backend_id="claude", threshold=2, cooldown_s=0.1)
    cb.record_failure()
    cb.record_failure()
    assert cb.state == "open"
    time.sleep(0.15)
    assert cb.state == "half_open"
    assert cb.allow_request() is True


def test_circuit_breaker_half_open_success_closes():
    cb = CLICircuitBreaker(backend_id="claude", threshold=2, cooldown_s=0.1)
    cb.record_failure()
    cb.record_failure()
    time.sleep(0.15)
    assert cb.state == "half_open"
    cb.record_success()
    assert cb.state == "closed"


def test_circuit_breaker_half_open_failure_reopens():
    cb = CLICircuitBreaker(backend_id="claude", threshold=2, cooldown_s=0.1)
    cb.record_failure()
    cb.record_failure()
    time.sleep(0.15)
    assert cb.state == "half_open"
    cb.record_failure()
    assert cb.state == "open"


def test_circuit_breaker_reset():
    cb = CLICircuitBreaker(backend_id="claude", threshold=2, cooldown_s=100)
    cb.record_failure()
    cb.record_failure()
    assert cb.state == "open"
    cb.reset()
    assert cb.state == "closed"
    assert cb.allow_request() is True


# ── Cleanup Session Tests ─────────────────────────────────────────────


def test_cleanup_session(tmp_path):
    executor = ClaudeExecutor(tmp_path / "workspace")
    sd = executor.session_dir("to_clean")
    assert sd.exists()
    # Put a file in it
    (sd / "test.txt").write_text("data")
    assert executor.cleanup_session("to_clean") is True
    assert not sd.exists()


def test_cleanup_session_nonexistent(tmp_path):
    executor = ClaudeExecutor(tmp_path / "workspace")
    assert executor.cleanup_session("nonexistent") is False


# ── CLI Args Tests ────────────────────────────────────────────────────


def test_build_args_contains_strict_mcp(tmp_path):
    executor = ClaudeExecutor(tmp_path / "workspace")
    executor._resolve_cli_exec = lambda backend: ["claude"]
    args, stdin_input, output_mode = executor._build_args(backend_id="claude", prompt="hello")
    assert "--strict-mcp-config" in args
    assert "--include-partial-messages" in args
    assert "--no-session-persistence" in args
    assert stdin_input == "hello"
    assert output_mode == "stream-json"


def test_build_args_persists_claude_sessions_when_resuming(tmp_path):
    executor = ClaudeExecutor(tmp_path / "workspace")
    executor._resolve_cli_exec = lambda backend: ["claude"]

    args, _, _ = executor._build_args(
        backend_id="claude",
        prompt="hello",
        continue_session=True,
        resume_session_id="session-123",
    )

    assert "--no-session-persistence" not in args
    assert "-c" in args
    assert "--resume" in args


def test_build_args_adds_max_tuning_flags_for_claude(tmp_path):
    executor = ClaudeExecutor(tmp_path / "workspace")
    executor._resolve_cli_exec = lambda backend: ["claude"]

    args, _, _ = executor._build_args(
        backend_id="claude",
        prompt="hello",
        model="deep",
    )

    assert "--effort" in args
    assert "high" in args
    assert "--fallback-model" in args
    assert CLAUDE_MODEL_ALIASES["sonnet"] in args


def test_openrouter_capabilities_are_api_key_native():
    caps = get_provider_capabilities("openrouter")

    assert caps["auth_mode"] == "api_key"
    assert caps["transport"] == "api"
    assert caps["supports_native_fallbacks"] is True


def test_codex_model_aliases():
    assert CODEX_MODEL_ALIASES["haiku"] == "gpt-5.1-codex-mini"
    assert CODEX_MODEL_ALIASES["sonnet"] == "gpt-5.1-codex"


def test_parse_codex_jsonl():
    executor = ClaudeExecutor(Path("/tmp/test"))
    stdout = '\n'.join([
        '{"thread_id": "thread-123", "usage": {"input_tokens": 10}, "message": {"content": "draft"}}',
        '{"output": {"text": "final answer"}}',
    ])
    text, cost, usage, session_id = executor._parse_codex_jsonl(stdout)
    assert text == "final answer"
    assert cost is None
    assert usage == {"input_tokens": 10}
    assert session_id == "thread-123"


def test_codex_resume_args_use_thread_id(tmp_path, monkeypatch):
    executor = ClaudeExecutor(tmp_path / "workspace")
    monkeypatch.setattr(executor, "_resolve_cli_exec", lambda backend: ["codex"])
    args, stdin_input, output_mode = executor._build_args(
        backend_id="codex",
        prompt="ignored",
        resume_session_id="thread-456",
    )
    assert args[:3] == ["codex", "exec", "resume"]
    assert "thread-456" in args
    assert stdin_input is None
    assert output_mode == "text"


def test_codex_cli_env_override(tmp_path, monkeypatch):
    cli_path = tmp_path / "codex.cmd"
    cli_path.write_text("@echo off", encoding="utf-8")
    monkeypatch.setenv("CODEX_CLI_PATH", str(cli_path))
    monkeypatch.setattr("agents.executor._path_runnable", lambda path: True)

    backend = ClaudeExecutor.get_backend_config("codex")
    assert ClaudeExecutor._find_cli_path(backend) == str(cli_path)


def test_zai_model_env_override(tmp_path, monkeypatch):
    executor = ClaudeExecutor(tmp_path / "workspace")
    monkeypatch.setenv("ZAI_MODEL_FAST", "glm-fast")
    monkeypatch.setenv("ZAI_MODEL_BALANCED", "glm-balanced")
    monkeypatch.setenv("ZAI_MODEL_DEEP", "glm-deep")

    assert executor._resolve_model_name("zai", "haiku") == "glm-fast"
    assert executor._resolve_model_name("zai", "sonnet") == "glm-balanced"
    assert executor._resolve_model_name("zai", "opus") == "glm-deep"


def test_openrouter_model_env_override(tmp_path, monkeypatch):
    executor = ClaudeExecutor(tmp_path / "workspace")
    monkeypatch.setenv("OPENROUTER_MODEL_FAST", "openrouter/fast")
    monkeypatch.setenv("OPENROUTER_MODEL_BALANCED", "openrouter/balanced")
    monkeypatch.setenv("OPENROUTER_MODEL_DEEP", "openrouter/deep")

    assert executor._resolve_model_name("openrouter", "haiku") == "openrouter/fast"
    assert executor._resolve_model_name("openrouter", "sonnet") == "openrouter/balanced"
    assert executor._resolve_model_name("openrouter", "opus") == "openrouter/deep"


def test_openrouter_clean_env_no_longer_uses_anthropic_compatibility(tmp_path, monkeypatch):
    executor = ClaudeExecutor(tmp_path / "workspace")
    backend = executor.get_backend_config("openrouter")
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-key")
    monkeypatch.setenv("OPENROUTER_BASE_URL", "https://openrouter.example.test/api")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "legacy-key")

    env = executor._clean_env(backend)

    assert env["ANTHROPIC_API_KEY"] == "legacy-key"
    assert "ANTHROPIC_AUTH_TOKEN" not in env
    assert env.get("ANTHROPIC_BASE_URL") != "https://openrouter.example.test/api"


def test_openrouter_streams_native_progress(tmp_path, monkeypatch):
    executor = ClaudeExecutor(tmp_path / "workspace")
    events = []

    monkeypatch.setattr(
        "agents.openrouter_client.stream_chat",
        lambda **kwargs: iter(
            [
                {"type": "progress", "text": "Routing request..."},
                {"type": "message", "text": "Final answer"},
            ]
        ),
    )
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-key")

    result = executor.run_raw(
        "hello",
        backend_id="openrouter",
        on_progress=events.append,
        max_retries=0,
    )

    assert events == ["Routing request..."]
    assert result.text == "Final answer"


def test_openrouter_backend_status_does_not_require_claude_cli(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-key")

    def _resolve_cli_exec(cls, backend):
        if backend.id == "openrouter":
            raise AssertionError("openrouter should not resolve a CLI")
        return ["cmd"]

    monkeypatch.setattr(
        ClaudeExecutor,
        "_resolve_cli_exec",
        classmethod(_resolve_cli_exec),
    )

    statuses = ClaudeExecutor.get_backend_statuses()
    openrouter = next(status for status in statuses if status["id"] == "openrouter")

    assert openrouter["available"] is True
    assert openrouter["authenticated"] is True


def test_openrouter_persists_local_session_history(tmp_path, monkeypatch):
    executor = ClaudeExecutor(tmp_path / "workspace")
    captured_messages = []

    def _stream_chat(**kwargs):
        captured_messages.append(kwargs["messages"])
        return iter([{"type": "message", "text": "Reply"}])

    monkeypatch.setattr("agents.openrouter_client.stream_chat", _stream_chat)
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-key")

    first = executor.run_raw(
        "hello",
        backend_id="openrouter",
        session_id="chat_42",
        continue_session=True,
        max_retries=0,
    )
    second = executor.run_raw(
        "follow up",
        backend_id="openrouter",
        session_id="chat_42",
        continue_session=True,
        resume_session_id=first.session_id_out,
        max_retries=0,
    )

    assert first.session_id_out == "chat_42"
    assert second.session_id_out == "chat_42"
    assert captured_messages[0] == [{"role": "user", "content": "hello"}]
    assert captured_messages[1] == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "Reply"},
        {"role": "user", "content": "follow up"},
    ]


def test_openrouter_run_uses_structured_system_and_user_messages(tmp_path, monkeypatch):
    executor = ClaudeExecutor(tmp_path / "workspace", default_backend_id="openrouter")
    captured_messages = []

    def _stream_chat(**kwargs):
        captured_messages.append(kwargs["messages"])
        return iter([{"type": "message", "text": "Reply"}])

    monkeypatch.setattr("agents.openrouter_client.stream_chat", _stream_chat)
    monkeypatch.setenv("OPENROUTER_API_KEY", "or-key")

    first = executor.run(
        event_type="human_message",
        payload={"text": "hello"},
        skill_text="You are a helpful assistant.",
        memory_context="Memory context here.",
        session_id="chat_structured",
        continue_session=True,
        backend_id="openrouter",
        max_retries=0,
    )
    second = executor.run(
        event_type="human_message",
        payload={"text": "follow up"},
        skill_text="You are a helpful assistant.",
        memory_context="Memory context here.",
        session_id="chat_structured",
        continue_session=True,
        resume_session_id=first.session_id_out,
        backend_id="openrouter",
        max_retries=0,
    )

    assert first.session_id_out == "chat_structured"
    assert second.session_id_out == "chat_structured"
    assert captured_messages[0][0]["role"] == "system"
    assert "## Memory" in captured_messages[0][0]["content"]
    assert captured_messages[0][1]["role"] == "user"
    assert "## Current Event" in captured_messages[0][1]["content"]
    assert "## Memory" not in captured_messages[1][1]["content"]
    assert captured_messages[1][2] == {"role": "assistant", "content": "Reply"}


def test_openrouter_history_trim_keeps_user_boundary(tmp_path, monkeypatch):
    executor = ClaudeExecutor(tmp_path / "workspace")
    monkeypatch.setenv("KB_OPENROUTER_MAX_SESSION_MESSAGES", "4")

    executor._save_openrouter_history(
        "chat_99",
        [
            {"role": "user", "content": "one"},
            {"role": "assistant", "content": "two"},
            {"role": "user", "content": "three"},
            {"role": "assistant", "content": "four"},
            {"role": "user", "content": "five"},
        ],
    )

    history = executor._load_openrouter_history("chat_99")

    assert history[0]["role"] == "user"
    assert len(history) <= 4


def test_openrouter_history_load_drops_legacy_system_messages(tmp_path):
    executor = ClaudeExecutor(tmp_path / "workspace")
    history_path = executor._openrouter_history_path("chat_legacy")
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history_path.write_text(
        json.dumps(
            [
                {"role": "system", "content": "Old instructions"},
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": "Reply"},
            ],
            ensure_ascii=True,
        ),
        encoding="utf-8",
    )

    history = executor._load_openrouter_history("chat_legacy")

    assert history == [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "Reply"},
    ]


def test_claude_clean_env_prefers_subscription_auth(tmp_path, monkeypatch):
    executor = ClaudeExecutor(tmp_path / "workspace")
    backend = executor.get_backend_config("claude")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "api-key")
    monkeypatch.setenv("ANTHROPIC_AUTH_TOKEN", "auth-token")
    monkeypatch.setenv("ANTHROPIC_BASE_URL", "https://proxy.example.test")
    monkeypatch.setattr(
        executor,
        "_get_claude_auth_status",
        lambda *args, **kwargs: {
            "loggedIn": True,
            "apiProvider": "firstParty",
            "subscriptionType": "max",
        },
    )

    env = executor._clean_env(backend)

    assert "ANTHROPIC_API_KEY" not in env
    assert "ANTHROPIC_AUTH_TOKEN" not in env
    assert "ANTHROPIC_BASE_URL" not in env


def test_claude_backend_status_requires_auth(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_AUTH_TOKEN", raising=False)
    monkeypatch.setattr(
        ClaudeExecutor,
        "_resolve_cli_exec",
        classmethod(lambda cls, backend: ["claude"] if backend.id == "claude" else ["cmd"]),
    )
    monkeypatch.setattr(
        ClaudeExecutor,
        "_get_claude_auth_status",
        classmethod(lambda cls, force_refresh=False: {"loggedIn": False}),
    )

    statuses = ClaudeExecutor.get_backend_statuses()
    claude = next(status for status in statuses if status["id"] == "claude")

    assert claude["available"] is False
    assert claude["authenticated"] is False
    assert "auth" in claude["reason"].lower()


def test_codex_auth_status_reads_local_auth_file(tmp_path, monkeypatch):
    auth_dir = tmp_path / ".codex"
    auth_dir.mkdir()
    payload = {
        "https://api.openai.com/auth": {
            "chatgpt_plan_type": "plus",
        }
    }
    payload_bytes = json.dumps(payload).encode("utf-8")
    payload_b64 = __import__("base64").urlsafe_b64encode(payload_bytes).decode("ascii").rstrip("=")
    token = f"header.{payload_b64}.sig"
    (auth_dir / "auth.json").write_text(
        json.dumps(
            {
                "auth_mode": "chatgpt",
                "OPENAI_API_KEY": None,
                "tokens": {"access_token": token},
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)

    status = ClaudeExecutor._get_codex_auth_status(force_refresh=True)

    assert status is not None
    assert status["loggedIn"] is True
    assert status["authMethod"] == "chatgpt"
    assert status["subscriptionType"] == "plus"


def test_codex_backend_status_requires_auth(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(
        ClaudeExecutor,
        "_resolve_cli_exec",
        classmethod(lambda cls, backend: ["codex"] if backend.id == "codex" else ["claude"]),
    )
    monkeypatch.setattr(
        ClaudeExecutor,
        "_get_codex_auth_status",
        classmethod(lambda cls, force_refresh=False: {"loggedIn": False}),
    )
    monkeypatch.setattr(
        "agents.executor.subprocess.run",
        lambda *args, **kwargs: type("Result", (), {"returncode": 0, "stdout": "codex 1.0", "stderr": ""})(),
    )

    statuses = ClaudeExecutor.get_backend_statuses()
    codex = next(status for status in statuses if status["id"] == "codex")

    assert codex["available"] is False
    assert codex["authenticated"] is False
    assert "auth" in codex["reason"].lower()


def test_executor_uses_env_default_model_tier(tmp_path, monkeypatch):
    executor = ClaudeExecutor(tmp_path / "workspace")
    monkeypatch.setenv("KB_DEFAULT_MODEL", "deep")
    monkeypatch.setattr("gateway.queue.DEFAULT_QUEUE_DB_PATH", tmp_path / "missing-queue.db")

    assert executor._resolve_model_name("claude", None) == CLAUDE_MODEL_ALIASES["opus"]


def test_executor_uses_persisted_global_model_tier(tmp_path, monkeypatch):
    db_path = tmp_path / "queue.db"
    queue = Queue(db_path)
    queue.set_global_model("fast")
    executor = ClaudeExecutor(tmp_path / "workspace")
    monkeypatch.setenv("KB_DEFAULT_MODEL", "opus")
    monkeypatch.setattr("gateway.queue.DEFAULT_QUEUE_DB_PATH", db_path)

    assert executor._resolve_model_name("codex", None) == CODEX_MODEL_ALIASES["haiku"]
