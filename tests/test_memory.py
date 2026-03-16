"""Tests for reading_app.memory."""

from pathlib import Path

from reading_app.memory import MemorySystem


def test_load_context(memory_path):
    ms = MemorySystem(memory_path)
    ctx = ms.load_context()
    assert "memory" in ctx.lower() or len(ctx) > 0


def test_append_to_log(memory_path):
    ms = MemorySystem(memory_path)
    ms.append_to_log("What I Read", "- Test article about AI safety")
    log_path = ms._today_log_path()
    assert log_path.exists()
    content = log_path.read_text(encoding="utf-8")
    assert "Test article" in content


def test_append_to_log_creates_file(memory_path):
    ms = MemorySystem(memory_path)
    ms.append_to_log("Key Insights", "- Insight 1")
    log_path = ms._today_log_path()
    assert log_path.exists()


def test_get_heartbeat_instructions(memory_path):
    ms = MemorySystem(memory_path)
    instructions = ms.get_heartbeat_instructions()
    assert isinstance(instructions, str)


def test_today_log_path(memory_path):
    ms = MemorySystem(memory_path)
    log_path = ms._today_log_path()
    assert "logs" in str(log_path)
    assert log_path.suffix == ".md"
