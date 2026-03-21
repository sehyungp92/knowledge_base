"""Tests for gateway.dispatcher."""

import time
from unittest.mock import MagicMock, patch

from gateway.dispatcher import Dispatcher, _is_heartbeat_ok
from gateway.models import Event, Job
from gateway.providers import get_default_provider_id
from gateway.queue import Queue


def _make_dispatcher(queue=None, **kwargs):
    if queue is None:
        queue = Queue(":memory:")
    registry = MagicMock()
    registry.skills = {}
    executor = MagicMock()
    memory = MagicMock()
    memory.load_context.return_value = "Test memory context"
    executor.run.return_value = MagicMock(text="Response text", cost_usd=0.01, session_id_out=None)
    executor.get_backend_statuses.return_value = [
        {"id": "claude", "label": "Claude Code", "available": True, "reason": ""},
        {"id": "codex", "label": "Codex", "available": True, "reason": ""},
        {"id": "zai", "label": "Z.AI", "available": True, "reason": ""},
    ]
    executor.for_backend.return_value = executor
    defaults = dict(
        queue=queue,
        skill_registry=registry,
        executor=executor,
        memory_system=memory,
    )
    defaults.update(kwargs)
    return Dispatcher(**defaults)


def test_process_empty_queue():
    d = _make_dispatcher()
    assert d.process_next() is False


def test_process_job():
    q = Queue(":memory:")
    eid = q.insert_event(Event(type="human_message", payload={"text": "/ask test"}, source="telegram", chat_id="42"))
    q.insert_job(Job(event_id=eid, skill="ask"))

    mock_adapter = MagicMock()
    d = _make_dispatcher(queue=q, adapter_registry={"telegram": mock_adapter})
    d.skill_registry.match.return_value = None  # fallback to general chat

    # Advance time past debounce threshold
    with patch("gateway.dispatcher.time") as mock_time:
        mock_time.time.return_value = time.time() + 1.0
        assert d.process_next() is True
    mock_adapter.send_message_sync.assert_called_once()


def test_heartbeat_suppression():
    q = Queue(":memory:")
    eid = q.insert_event(Event(type="heartbeat", payload={"trigger": "scheduled"}, source="heartbeat"))
    q.insert_job(Job(event_id=eid, skill="heartbeat"))

    d = _make_dispatcher(queue=q)
    d.executor.run.return_value = MagicMock(text="HEARTBEAT_OK", cost_usd=0.001, session_id_out=None)
    d.skill_registry.match.return_value = None

    with patch("gateway.dispatcher.time") as mock_time:
        mock_time.time.return_value = time.time() + 1.0
        d.process_next()
    # Heartbeat has no adapter in registry, so no reply sent — verify suppression via job status
    job = q._conn.execute("SELECT status FROM jobs WHERE event_id = ?", (eid,)).fetchone()
    assert job[0] == "complete"


def test_is_heartbeat_ok():
    assert _is_heartbeat_ok("HEARTBEAT_OK") is True
    assert _is_heartbeat_ok("  heartbeat_ok  ") is True
    assert _is_heartbeat_ok("Here is a report") is False


def test_on_start_callback():
    q = Queue(":memory:")
    eid = q.insert_event(Event(type="human_message", payload={"text": "hello"}, source="telegram", chat_id="42"))
    q.insert_job(Job(event_id=eid, skill="ask"))

    mock_adapter = MagicMock()
    d = _make_dispatcher(queue=q, adapter_registry={"telegram": mock_adapter})
    d.skill_registry.match.return_value = None

    with patch("gateway.dispatcher.time") as mock_time:
        mock_time.time.return_value = time.time() + 1.0
        d.process_next()
    mock_adapter.send_typing_sync.assert_called_once_with("42")


def test_reply_routes_to_correct_adapter():
    """Verify that replies route to the adapter matching event.source."""
    q = Queue(":memory:")
    eid = q.insert_event(Event(type="human_message", payload={"text": "hi"}, source="discord", chat_id="999"))
    q.insert_job(Job(event_id=eid, skill="ask"))

    telegram_adapter = MagicMock()
    discord_adapter = MagicMock()
    d = _make_dispatcher(
        queue=q,
        adapter_registry={"telegram": telegram_adapter, "discord": discord_adapter},
    )
    d.skill_registry.match.return_value = None

    with patch("gateway.dispatcher.time") as mock_time:
        mock_time.time.return_value = time.time() + 1.0
        d.process_next()

    discord_adapter.send_message_sync.assert_called_once()
    telegram_adapter.send_message_sync.assert_not_called()


def test_stream_progress_updates_job_result():
    q = Queue(":memory:")
    eid = q.insert_event(Event(type="human_message", payload={"text": "/save https://example.com"}, source="telegram", chat_id="42"))
    job_id = q.insert_job(Job(event_id=eid, skill="save", provider_id="claude"))

    registry = MagicMock()
    skill = MagicMock()
    skill.name = "save"
    skill.prompt_text.return_value = "Save this source."
    skill.tools_allowed = []
    skill.tools_denied = []
    skill.timeout = 300
    skill.stream_progress = True
    registry.skills = {"save": skill}
    registry.match.return_value = (skill, True)

    executor = MagicMock()

    def _run_with_progress(*args, **kwargs):
        kwargs["on_progress"]("Fetching page metadata...")
        return MagicMock(text="Saved.", cost_usd=0.01, session_id_out=None)

    executor.for_backend.return_value = executor
    executor.run.side_effect = _run_with_progress
    executor.get_backend_statuses.return_value = [
        {"id": "claude", "label": "Claude Code", "available": True, "reason": ""},
        {"id": "codex", "label": "Codex", "available": True, "reason": ""},
        {"id": "zai", "label": "Z.AI", "available": True, "reason": ""},
    ]
    memory = MagicMock()
    memory.load_context.return_value = "memory"
    adapter = MagicMock()

    d = Dispatcher(
        queue=q,
        skill_registry=registry,
        executor=executor,
        memory_system=memory,
        adapter_registry={"telegram": adapter},
    )

    with patch("gateway.dispatcher.time") as mock_time:
        mock_time.time.return_value = time.time() + 1.0
        assert d.process_next() is True

    job = q.get_job(job_id)
    assert job is not None
    assert job.status == "complete"
    assert job.result["provider_id"] == "claude"
    sent_messages = [call.args[1] for call in adapter.send_message_sync.call_args_list]
    assert "Fetching page metadata..." in sent_messages


def test_direct_handler_progress_updates_job_result():
    q = Queue(":memory:")
    eid = q.insert_event(Event(type="save", payload={"text": "https://example.com"}, source="webapp", chat_id="webapp"))
    job_id = q.insert_job(Job(event_id=eid, skill="save", provider_id="claude"))

    registry = MagicMock()
    skill = MagicMock()
    skill.name = "save"
    skill.prompt_text.return_value = "Save this source."
    skill.tools_allowed = []
    skill.tools_denied = []
    skill.timeout = 300
    skill.stream_progress = True
    registry.skills = {"save": skill}
    registry.match.return_value = (skill, True)

    executor = MagicMock()
    executor.for_backend.return_value = executor
    executor.get_backend_statuses.return_value = [
        {"id": "claude", "label": "Claude Code", "available": True, "reason": ""},
        {"id": "codex", "label": "Codex", "available": True, "reason": ""},
        {"id": "zai", "label": "Z.AI", "available": True, "reason": ""},
    ]
    memory = MagicMock()
    memory.load_context.return_value = "memory"
    config = MagicMock()

    d = Dispatcher(
        queue=q,
        skill_registry=registry,
        executor=executor,
        memory_system=memory,
        config=config,
    )

    def _fake_handle_save_job(event, job, config, executor, on_progress=None):
        assert on_progress is not None
        on_progress("Fetching source content...")
        running_job = q.get_job(job_id)
        assert running_job is not None
        assert running_job.result["progress"] == "Fetching source content..."
        return "Saved."

    with patch("gateway.save_handler.handle_save_job", side_effect=_fake_handle_save_job), \
         patch("gateway.dispatcher.time") as mock_time:
        mock_time.time.return_value = time.time() + 1.0
        assert d.process_next() is True

    job = q.get_job(job_id)
    assert job is not None
    assert job.status == "complete"
    assert job.result["handler"] == "save_direct"
    assert job.result["response"] == "Saved."


def test_dispatcher_uses_provider_scoped_session_and_executor():
    q = Queue(":memory:")
    q.set_chat_provider("chat_42", "codex")
    q.upsert_session("chat_42", "thread-123", backend_id="codex")

    eid = q.insert_event(Event(type="human_message", payload={"text": "hello"}, source="telegram", chat_id="42"))
    q.insert_job(Job(event_id=eid, skill="ask"))

    registry = MagicMock()
    registry.skills = {}
    executor = MagicMock()
    provider_executor = MagicMock()
    provider_executor.run.return_value = MagicMock(text="Codex reply", cost_usd=0.02, session_id_out="thread-456")
    executor.for_backend.return_value = provider_executor
    executor.get_backend_statuses.return_value = [
        {"id": "claude", "label": "Claude Code", "available": True, "reason": ""},
        {"id": "codex", "label": "Codex", "available": True, "reason": ""},
        {"id": "zai", "label": "Z.AI", "available": True, "reason": ""},
    ]
    memory = MagicMock()
    memory.load_context.return_value = "memory"

    d = Dispatcher(queue=q, skill_registry=registry, executor=executor, memory_system=memory)
    registry.match.return_value = None

    with patch("gateway.dispatcher.time") as mock_time:
        mock_time.time.return_value = time.time() + 1.0
        assert d.process_next() is True

    executor.for_backend.assert_called_once_with("codex")
    provider_executor.run.assert_called_once()
    assert provider_executor.run.call_args.kwargs["resume_session_id"] == "thread-123"
    assert q.get_session("chat_42", "codex") == "thread-456"


def test_dispatcher_falls_back_to_plain_executor_when_for_backend_is_not_declared():
    q = Queue(":memory:")
    eid = q.insert_event(Event(type="human_message", payload={"text": "hello"}, source="telegram", chat_id="42"))
    q.insert_job(Job(event_id=eid, skill="ask"))

    registry = MagicMock()
    registry.skills = {}
    registry.match.return_value = None

    executor = MagicMock()
    executor.run.return_value = MagicMock(text="Base executor reply", cost_usd=0.02, session_id_out=None)
    executor.get_backend_statuses.return_value = [
        {"id": "claude", "label": "Claude Code", "available": True, "reason": ""},
        {"id": "codex", "label": "Codex", "available": True, "reason": ""},
        {"id": "zai", "label": "Z.AI", "available": True, "reason": ""},
        {"id": "openrouter", "label": "OpenRouter", "available": True, "reason": ""},
    ]
    memory = MagicMock()
    memory.load_context.return_value = "memory"
    adapter = MagicMock()

    d = Dispatcher(
        queue=q,
        skill_registry=registry,
        executor=executor,
        memory_system=memory,
        adapter_registry={"telegram": adapter},
    )

    with patch("gateway.dispatcher.time") as mock_time:
        mock_time.time.return_value = time.time() + 1.0
        assert d.process_next() is True

    executor.run.assert_called_once()
    adapter.send_message_sync.assert_called_once()
    job = q.get_job(1)
    assert job is not None
    assert job.status == "complete"
    assert job.result["provider_id"] == get_default_provider_id()


def test_dispatcher_fails_fast_when_provider_unavailable():
    q = Queue(":memory:")
    eid = q.insert_event(Event(type="human_message", payload={"text": "hello"}, source="telegram", chat_id="42"))
    q.insert_job(Job(event_id=eid, skill="ask", provider_id="codex"))

    registry = MagicMock()
    registry.skills = {}
    executor = MagicMock()
    executor.get_backend_statuses.return_value = [
        {"id": "claude", "label": "Claude Code", "available": True, "reason": ""},
        {"id": "codex", "label": "Codex", "available": False, "reason": "Missing CODEX_CLI_PATH."},
        {"id": "zai", "label": "Z.AI", "available": True, "reason": ""},
    ]
    memory = MagicMock()
    memory.load_context.return_value = "memory"
    adapter = MagicMock()

    d = Dispatcher(
        queue=q,
        skill_registry=registry,
        executor=executor,
        memory_system=memory,
        adapter_registry={"telegram": adapter},
    )
    registry.match.return_value = None

    with patch("gateway.dispatcher.time") as mock_time:
        mock_time.time.return_value = time.time() + 1.0
        assert d.process_next() is True

    executor.for_backend.assert_not_called()
    adapter.send_message_sync.assert_called_once()
    job = q.get_job(1)
    assert job is not None
    assert job.status == "failed"
    assert "Missing CODEX_CLI_PATH" in job.result["error"]


# ---------------------------------------------------------------------------
# Tests merged from test_api_main.py — FastAPI application setup
# ---------------------------------------------------------------------------


def test_health_endpoint():
    with patch("webapp.api.main.init_pool"), \
         patch("webapp.api.main.close_pool"):
        from webapp.api.main import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"


def test_cors_allows_localhost():
    with patch("webapp.api.main.init_pool"), \
         patch("webapp.api.main.close_pool"):
        from webapp.api.main import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        resp = client.get("/api/health", headers={"Origin": "http://localhost:3000"})
        assert resp.status_code == 200
