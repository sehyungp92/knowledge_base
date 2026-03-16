"""Phase 5 integration tests — API router smoke tests."""

from unittest.mock import patch, MagicMock

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create a test client with patched DB pool."""
    with patch("reading_app.db.init_pool"), \
         patch("reading_app.db.close_pool"):
        from webapp.api.main import app
        yield TestClient(app)


def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


ROUTER_SMOKE_ENDPOINTS = [
    "/api/landscape/themes",
    "/api/landscape/contributions",
    "/api/landscape/changelog",
    "/api/library/sources",
    "/api/beliefs",
    "/api/predictions",
    "/api/graph/communities",
    "/api/activity/stats",
    "/api/activity/runtime",
    "/api/notifications",
]


@pytest.mark.parametrize("endpoint", ROUTER_SMOKE_ENDPOINTS)
def test_router_registered(client, endpoint):
    """Verify that all Phase 5 routers are reachable (not 404)."""
    with patch("reading_app.db.get_conn") as mock_conn:
        conn = MagicMock()
        conn.__enter__ = MagicMock(return_value=conn)
        conn.__exit__ = MagicMock(return_value=False)
        conn.execute.return_value.fetchall.return_value = []
        conn.execute.return_value.fetchone.return_value = {"cnt": 0, "total": 0, "running": 0, "failed": 0, "pending": 0, "completed": 0}
        mock_conn.return_value = conn

        # Patch landscape module to avoid real DB calls
        with patch("retrieval.landscape.get_recent_breakthroughs", return_value=[]), \
             patch("retrieval.landscape.get_anticipations_with_evidence", return_value=[]), \
             patch("retrieval.landscape.get_over_optimistic_themes", return_value=[]), \
             patch("retrieval.landscape.get_blind_spot_bottlenecks", return_value=[]), \
             patch("retrieval.landscape.compute_theme_velocity", return_value=[]), \
             patch("retrieval.landscape.get_theme_source_counts", return_value=[]), \
             patch("gateway.queue.Queue") as MockQueue, \
             patch("webapp.api.routers.activity.ClaudeExecutor.get_backend_statuses", return_value=[
                 {"id": "claude", "label": "Claude Code", "available": True, "reason": ""},
                 {"id": "codex", "label": "Codex", "available": True, "reason": ""},
                 {"id": "zai", "label": "Z.AI", "available": True, "reason": ""},
                 {"id": "openrouter", "label": "OpenRouter", "available": True, "reason": ""},
             ]), \
             patch("webapp.api.routers.activity._gateway_runtime_status", return_value={
                 "state": "offline",
                 "running": False,
                 "ready": False,
                 "pid": None,
                 "ready_at": None,
                 "log_path": "var/runtime/logs/gateway.log",
             }):
            mock_q = MagicMock()
            mock_q._conn.execute.return_value.fetchall.return_value = []
            mock_q._conn.execute.return_value.fetchone.return_value = None
            mock_q.get_chat_provider.return_value = "claude"
            mock_q.get_global_model.return_value = "sonnet"
            MockQueue.return_value = mock_q
            resp = client.get(endpoint)
            # Should not be 404 (router not found) or 405 (method not allowed)
            assert resp.status_code not in (404, 405), f"{endpoint} returned {resp.status_code}"


def test_search_requires_query(client):
    """GET /api/search without q param should return 422."""
    resp = client.get("/api/search")
    assert resp.status_code == 422


def test_actions_save_enqueues(client):
    """POST /api/actions/save should enqueue and return a job_id."""
    with patch("webapp.api.routers.actions.Queue") as MockQueue:
        mock_q = MagicMock()
        mock_q.insert_event.return_value = 1
        mock_q.insert_job.return_value = 42
        mock_q.get_chat_provider.return_value = "claude"
        MockQueue.return_value = mock_q
        with patch("webapp.api.routers.actions._get_executor") as get_executor:
            get_executor.return_value.get_backend_statuses.return_value = [
                {"id": "claude", "label": "Claude Code", "available": True, "reason": ""},
                {"id": "codex", "label": "Codex", "available": True, "reason": ""},
                {"id": "zai", "label": "Z.AI", "available": True, "reason": ""},
                {"id": "openrouter", "label": "OpenRouter", "available": True, "reason": ""},
            ]

            resp = client.post(
                "/api/actions/save",
                json={"text": "https://example.com/paper", "provider_id": "codex"},
            )
        assert resp.status_code == 200
        body = resp.json()
        assert "job_id" in body
        assert body["job_id"] == 42
        assert body["provider_id"] == "codex"


def test_actions_command_runs_direct_handler(client):
    """Selected low-latency commands should complete directly through the API."""
    with patch("webapp.api.routers.actions._run_direct_command") as run_direct:
        run_direct.return_value = {
            "mode": "direct",
            "skill": "ask",
            "status": "complete",
            "response": "Direct response",
            "provider_id": "codex",
        }

        resp = client.post("/api/actions/command", json={"text": "/ask what changed?", "provider_id": "codex"})

    assert resp.status_code == 200
    assert resp.json()["mode"] == "direct"
    assert resp.json()["response"] == "Direct response"
    assert resp.json()["provider_id"] == "codex"


def test_actions_command_returns_503_when_gateway_offline(client):
    """Commands that still require the worker should fail fast when the gateway is offline."""
    with patch("webapp.api.routers.actions._gateway_ready", return_value=False):
        resp = client.post("/api/actions/command", json={"text": "/reflect"})

    assert resp.status_code == 503
    assert "background worker is offline" in resp.json()["detail"]


def test_actions_provider_updates_chat_preference(client):
    with patch("webapp.api.routers.actions.Queue") as MockQueue, \
         patch("webapp.api.routers.actions._get_executor") as get_executor:
        mock_q = MagicMock()
        MockQueue.return_value = mock_q
        get_executor.return_value.get_backend_statuses.return_value = [
            {"id": "claude", "label": "Claude Code", "available": True, "reason": ""},
            {"id": "codex", "label": "Codex", "available": True, "reason": ""},
            {"id": "zai", "label": "Z.AI", "available": True, "reason": ""},
            {"id": "openrouter", "label": "OpenRouter", "available": True, "reason": ""},
        ]

        resp = client.post("/api/actions/provider", json={"provider_id": "openrouter"})

    assert resp.status_code == 200
    assert resp.json()["provider_id"] == "openrouter"
    mock_q.set_chat_provider.assert_called_once()


def test_actions_model_updates_global_preference(client):
    with patch("webapp.api.routers.actions.Queue") as MockQueue:
        mock_q = MagicMock()
        mock_q.set_global_model.return_value = "opus"
        MockQueue.return_value = mock_q

        resp = client.post("/api/actions/model", json={"model_tier": "deep"})

    assert resp.status_code == 200
    assert resp.json()["model_tier"] == "opus"
    mock_q.set_global_model.assert_called_once_with("opus")


def test_actions_command_model_skips_provider_availability_check(client):
    with patch("webapp.api.routers.actions._run_direct_command") as run_direct:
        run_direct.return_value = {
            "mode": "direct",
            "skill": "model",
            "status": "complete",
            "response": "Global default model updated",
            "provider_id": "codex",
            "model_tier": "haiku",
        }

        resp = client.post("/api/actions/command", json={"text": "/model fast", "provider_id": "codex"})

    assert resp.status_code == 200
    assert resp.json()["skill"] == "model"
    assert resp.json()["model_tier"] == "haiku"


def test_runtime_endpoint_reports_gateway_and_queue_state(client):
    """Runtime endpoint should expose gateway readiness and queue counts for the web UI."""
    mock_queue = MagicMock()
    mock_queue.get_chat_provider.return_value = "codex"
    mock_queue.get_global_model.return_value = "opus"
    mock_queue._conn.execute.side_effect = [
        MagicMock(fetchall=MagicMock(return_value=[
            {"status": "pending", "cnt": 2},
            {"status": "running", "cnt": 1},
            {"status": "complete", "cnt": 5},
        ])),
        MagicMock(fetchone=MagicMock(return_value={
            "id": 12,
            "skill": "ask",
            "status": "complete",
            "updated_at": 1_773_187_659.0,
            "result": '{"response":"Done"}',
        })),
        MagicMock(fetchone=MagicMock(return_value=None)),
    ]

    with patch("webapp.api.routers.activity._gateway_runtime_status", return_value={
        "state": "ready",
        "running": True,
        "ready": True,
        "pid": 1234,
        "ready_at": "2026-03-11T00:00:00+00:00",
        "log_path": "var/runtime/logs/gateway.log",
    }), patch("gateway.queue.Queue", return_value=mock_queue), \
         patch("webapp.api.routers.activity.ClaudeExecutor.get_backend_statuses", return_value=[
             {"id": "claude", "label": "Claude Code", "available": True, "reason": ""},
             {"id": "codex", "label": "Codex", "available": False, "reason": "Missing CODEX_CLI_PATH."},
             {"id": "zai", "label": "Z.AI", "available": True, "reason": ""},
             {"id": "openrouter", "label": "OpenRouter", "available": True, "reason": ""},
         ]):
        resp = client.get("/api/activity/runtime")

    assert resp.status_code == 200
    body = resp.json()
    assert body["gateway"]["ready"] is True
    assert body["queue"]["pending"] == 2
    assert body["queue"]["running"] == 1
    assert body["queue"]["last_completed"]["skill"] == "ask"
    assert body["chat"]["current_provider"] == "codex"
    assert body["chat"]["current_model"] == "opus"
    assert "/provider" in body["chat"]["direct_commands"]
    assert "/model" in body["chat"]["direct_commands"]
    assert body["chat"]["providers"][1]["available"] is False
    assert body["chat"]["providers"][3]["id"] == "openrouter"
    assert body["chat"]["model_options"][2]["id"] == "opus"


def test_jobs_endpoint_parses_payloads_and_adds_iso_timestamps(client):
    """Recent jobs should expose parsed JSON payloads plus additive ISO timestamp fields."""
    mock_queue = MagicMock()
    mock_queue._conn.execute.return_value.fetchall.return_value = [
        {
            "id": 21,
            "event_id": 9,
            "skill": "save",
            "status": "running",
            "logs_path": "",
            "result": '{"progress":"Fetching source content...","provider_id":"claude"}',
            "created_at": 1_773_274_800.0,
            "updated_at": 1_773_274_860.0,
            "retry_count": 0,
            "max_retries": 2,
            "provider_id": "claude",
            "event_type": "save",
            "event_payload": '{"text":"https://example.com"}',
            "event_source": "webapp",
        }
    ]

    with patch("gateway.queue.Queue", return_value=mock_queue):
        resp = client.get("/api/activity/jobs?limit=5")

    assert resp.status_code == 200
    body = resp.json()
    assert body[0]["result"]["progress"] == "Fetching source content..."
    assert body[0]["event_payload"]["text"] == "https://example.com"
    assert body[0]["progress"] == "Fetching source content..."
    assert body[0]["created_at_iso"] == "2026-03-12T00:20:00+00:00"
    assert body[0]["updated_at_iso"] == "2026-03-12T00:21:00+00:00"
