"""End-to-end smoke test for the gateway system."""

import time
from unittest.mock import MagicMock, patch

from gateway.dispatcher import Dispatcher, DEBOUNCE_THRESHOLD
from gateway.models import Event, Job
from gateway.queue import Queue
from reading_app.memory import MemorySystem


def _age_event(queue: Queue, event_id: int) -> None:
    """Push the event's created_at back past the debounce threshold."""
    past = time.time() - DEBOUNCE_THRESHOLD - 0.1
    queue._conn.execute(
        "UPDATE events SET created_at = ? WHERE id = ?", (past, event_id)
    )
    queue._conn.commit()


def _make_mock_adapter():
    """Create a mock adapter that matches the adapter_registry interface."""
    adapter = MagicMock()
    adapter.send_typing_sync = MagicMock()
    adapter.send_message_sync = MagicMock()
    return adapter


def test_full_flow(memory_path):
    """Test: message -> event -> job -> skill match -> executor -> response."""
    # Setup
    queue = Queue(":memory:")
    memory = MemorySystem(memory_path)

    # Mock skill registry
    mock_skill = MagicMock()
    mock_skill.name = "ask"
    mock_skill.prompt_text.return_value = "Answer the question."
    mock_skill.tools_allowed = ["Read"]
    mock_skill.tools_denied = []
    mock_skill.timeout = 300
    mock_skill.stream_progress = False
    mock_match = MagicMock()

    registry = MagicMock()
    registry.match.return_value = (mock_skill, mock_match)
    registry.skills = {"ask": mock_skill}

    # Mock executor
    executor = MagicMock()
    executor.run.return_value = MagicMock(
        text="RLHF stands for Reinforcement Learning from Human Feedback.",
        cost_usd=0.005,
        success=True,
        session_id_out=None,
    )

    # Mock adapter
    mock_adapter = _make_mock_adapter()

    dispatcher = Dispatcher(
        queue=queue,
        skill_registry=registry,
        executor=executor,
        memory_system=memory,
        adapter_registry={"telegram": mock_adapter},
    )

    # Simulate message arrival
    event = Event(
        type="human_message",
        payload={"text": "/ask what is RLHF?", "chat_id": "42"},
        source="telegram",
        chat_id="42",
    )
    event_id = queue.insert_event(event)
    _age_event(queue, event_id)
    queue.insert_job(Job(event_id=event_id, skill="ask"))

    # Process
    assert dispatcher.process_next() is True

    # Verify typing indicator was sent
    mock_adapter.send_typing_sync.assert_called_once_with("42")
    # Verify reply was sent
    mock_adapter.send_message_sync.assert_called_once()
    call_args = mock_adapter.send_message_sync.call_args
    assert call_args[0][0] == "42"
    assert "RLHF" in call_args[0][1]

    # Job should be complete
    job = queue.get_job(1)
    assert job.status == "complete"


def test_heartbeat_suppression_flow(memory_path):
    """Test: heartbeat -> executor returns HEARTBEAT_OK -> no Telegram message."""
    queue = Queue(":memory:")
    memory = MemorySystem(memory_path)
    registry = MagicMock()
    registry.match.return_value = None

    executor = MagicMock()
    executor.run.return_value = MagicMock(
        text="HEARTBEAT_OK",
        cost_usd=0.001,
        session_id_out=None,
    )

    mock_adapter = _make_mock_adapter()

    # Heartbeat matches via registry.match("heartbeat") — return a heartbeat skill
    mock_hb_skill = MagicMock()
    mock_hb_skill.name = "heartbeat"
    mock_hb_skill.prompt_text.return_value = "Run heartbeat checks."
    mock_hb_skill.tools_allowed = []
    mock_hb_skill.tools_denied = []
    mock_hb_skill.timeout = 300
    mock_hb_skill.stream_progress = False

    def match_side_effect(text):
        if text == "heartbeat":
            return (mock_hb_skill, MagicMock())
        return None

    registry.match.side_effect = match_side_effect
    registry.skills = {}

    dispatcher = Dispatcher(
        queue=queue,
        skill_registry=registry,
        executor=executor,
        memory_system=memory,
        adapter_registry={"heartbeat": mock_adapter},
    )

    event = Event(type="heartbeat", payload={"trigger": "scheduled"}, source="heartbeat")
    eid = queue.insert_event(event)
    _age_event(queue, eid)
    queue.insert_job(Job(event_id=eid, skill="heartbeat"))

    dispatcher.process_next()

    # Heartbeat OK should suppress the reply
    mock_adapter.send_message_sync.assert_not_called()
    job = queue.get_job(1)
    assert job.status == "complete"
    assert job.result.get("suppressed") is True
