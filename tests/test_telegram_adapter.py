"""Tests for adapters.telegram."""

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from adapters.telegram import TelegramAdapter
from adapters.telegram import _markdown_to_telegram_html, _chunk_text


def test_markdown_to_html_bold():
    assert _markdown_to_telegram_html("**bold**") == "<b>bold</b>"


def test_markdown_to_html_code():
    assert _markdown_to_telegram_html("`code`") == "<code>code</code>"


def test_markdown_to_html_link():
    result = _markdown_to_telegram_html("[text](https://example.com)")
    assert '<a href="https://example.com">text</a>' in result


def test_chunk_text_short():
    assert _chunk_text("short", limit=4096) == ["short"]


def test_chunk_text_splits():
    lines = ["Line " + str(i) for i in range(200)]
    text = "\n".join(lines)
    chunks = _chunk_text(text, limit=500)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= 500


def test_markdown_to_html_code_block():
    text = "```python\nprint('hello')\n```"
    result = _markdown_to_telegram_html(text)
    assert "<pre>" in result


def test_record_update_id_persists_latest(tmp_path):
    adapter = TelegramAdapter("token", MagicMock(), state_path=tmp_path / "telegram_state.json")
    adapter._record_update_id(12)
    adapter._record_update_id(10)

    state = json.loads((tmp_path / "telegram_state.json").read_text(encoding="utf-8"))
    assert state["last_update_id"] == 12


def test_drain_pending_updates_uses_saved_offset_and_persists_latest(tmp_path):
    state_path = tmp_path / "telegram_state.json"
    state_path.write_text(json.dumps({"last_update_id": 10}), encoding="utf-8")

    adapter = TelegramAdapter("token", MagicMock(), state_path=state_path)
    adapter._handle_message = AsyncMock()
    adapter._handle_callback = AsyncMock()

    update_message = SimpleNamespace(
        update_id=11,
        callback_query=None,
        effective_message=SimpleNamespace(text="hello"),
    )
    update_callback = SimpleNamespace(
        update_id=12,
        callback_query=SimpleNamespace(data="/save"),
        effective_message=None,
    )

    bot = MagicMock()
    bot.__aenter__ = AsyncMock(return_value=bot)
    bot.__aexit__ = AsyncMock(return_value=None)
    bot.get_updates = AsyncMock(side_effect=[[update_message, update_callback], []])

    with patch("adapters.telegram.Bot", return_value=bot):
        asyncio.run(adapter._drain_pending_updates())

    assert bot.get_updates.await_args_list[0].kwargs["offset"] == 11
    assert bot.get_updates.await_args_list[1].kwargs["offset"] == 13
    assert adapter._handle_message.await_count == 1
    assert adapter._handle_callback.await_count == 1

    state = json.loads(state_path.read_text(encoding="utf-8"))
    assert state["last_update_id"] == 12


def test_handle_message_uses_chat_provider_preference():
    queue = MagicMock()
    queue.insert_event.return_value = 7
    queue.get_chat_provider.return_value = "codex"
    adapter = TelegramAdapter("token", queue)

    update = SimpleNamespace(
        update_id=1,
        effective_message=SimpleNamespace(
            text="/ask hello",
            chat_id=42,
            message_id=99,
        ),
    )

    asyncio.run(adapter._handle_message(update, None))

    queue.insert_job.assert_called_once()
    job = queue.insert_job.call_args.args[0]
    assert job.provider_id == "codex"
