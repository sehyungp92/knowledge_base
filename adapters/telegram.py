"""Telegram long-polling adapter."""

from __future__ import annotations

import asyncio
import json
import logging
import re
from collections import deque
from pathlib import Path

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import Application, CallbackQueryHandler, MessageHandler, filters

from gateway.followups import extract_followups, strip_followups_section
from gateway.models import Event, Job
from gateway.providers import build_chat_session_key, get_default_provider_id
from gateway.queue import Queue

logger = logging.getLogger(__name__)


class TelegramAdapter:
    """Telegram bot adapter using long polling.

    Implements the Adapter protocol from adapters.base.
    """

    name: str = "telegram"

    def __init__(
        self,
        bot_token: str,
        queue: Queue,
        allowed_chat_id: str = "",
        state_path: Path | str | None = None,
    ):
        self.bot_token = bot_token
        self.queue = queue
        self.allowed_chat_id = allowed_chat_id
        self._state_path = Path(state_path) if state_path is not None else None
        self._seen_updates: deque[int] = deque(maxlen=100)
        self._loop: asyncio.AbstractEventLoop | None = None
        self._app: Application | None = None

    async def start(self):
        """Start the Telegram bot with long polling."""
        await self._drain_pending_updates()
        self._app = Application.builder().token(self.bot_token).build()
        self._app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))
        self._app.add_handler(MessageHandler(filters.COMMAND, self._handle_message))
        self._app.add_handler(CallbackQueryHandler(self._handle_callback))
        await self._app.initialize()
        await self._app.start()
        await self._app.updater.start_polling()
        logger.info("Telegram adapter started")

    async def stop(self):
        """Stop the Telegram bot."""
        if self._app:
            await self._app.updater.stop()
            await self._app.stop()
            await self._app.shutdown()

    async def _handle_message(self, update: Update, context):
        """Handle incoming Telegram messages."""
        if update.update_id in self._seen_updates:
            return
        self._seen_updates.append(update.update_id)

        # Capture event loop on first message
        if self._loop is None:
            self._loop = asyncio.get_running_loop()

        message = update.effective_message
        if not message or not message.text:
            return

        chat_id = str(message.chat_id)

        # Access control
        if self.allowed_chat_id and chat_id != self.allowed_chat_id:
            logger.warning("Rejected message from unauthorized chat_id: %s", chat_id)
            return

        # Create event
        event = Event(
            type="human_message",
            payload={"text": message.text, "chat_id": chat_id, "message_id": message.message_id},
            source="telegram",
            chat_id=chat_id,
        )
        event_id = self.queue.insert_event(event)
        session_key = build_chat_session_key(chat_id)
        provider_id = self.queue.get_chat_provider(session_key) or get_default_provider_id()
        self.queue.insert_job(Job(event_id=event_id, skill="pending", provider_id=provider_id))
        self._record_update_id(update.update_id)
        logger.info("Telegram event %d created for chat %s: %s", event_id, chat_id, message.text[:50])

    async def _handle_callback(self, update: Update, context):
        """Handle inline keyboard button taps."""
        query = update.callback_query
        if not query or not query.data:
            return

        if self._loop is None:
            self._loop = asyncio.get_running_loop()

        if context is not None:
            await query.answer()

        if query.message is None:
            return

        chat_id = str(query.message.chat_id)

        if self.allowed_chat_id and chat_id != self.allowed_chat_id:
            return

        event = Event(
            type="human_message",
            payload={"text": query.data, "chat_id": chat_id, "message_id": query.message.message_id},
            source="telegram",
            chat_id=chat_id,
        )
        event_id = self.queue.insert_event(event)
        session_key = build_chat_session_key(chat_id)
        provider_id = self.queue.get_chat_provider(session_key) or get_default_provider_id()
        self.queue.insert_job(Job(event_id=event_id, skill="pending", provider_id=provider_id))
        self._record_update_id(update.update_id)
        logger.info("Telegram callback event %d for chat %s: %s", event_id, chat_id, query.data[:50])

    def _load_state(self) -> dict:
        if self._state_path is None or not self._state_path.exists():
            return {}
        try:
            return json.loads(self._state_path.read_text(encoding="utf-8"))
        except Exception:
            logger.warning("telegram_state_corrupt", exc_info=True)
            return {}

    def _save_state(self, state: dict) -> None:
        if self._state_path is None:
            return
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        self._state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    def _record_update_id(self, update_id: int | None) -> None:
        if self._state_path is None or update_id is None:
            return
        state = self._load_state()
        current = int(state.get("last_update_id", -1))
        if update_id > current:
            state["last_update_id"] = update_id
            self._save_state(state)

    async def _drain_pending_updates(self) -> None:
        """Fetch any buffered Telegram updates before steady-state polling starts."""
        state = self._load_state()
        last_update_id = state.get("last_update_id")
        offset = int(last_update_id) + 1 if last_update_id is not None else None

        bot = Bot(self.bot_token)
        async with bot:
            updates = await bot.get_updates(
                offset=offset,
                timeout=0,
                allowed_updates=["message", "callback_query"],
            )
            max_update_id = int(last_update_id) if last_update_id is not None else -1
            for update in updates:
                if update.callback_query and update.callback_query.data:
                    await self._handle_callback(update, None)
                elif update.effective_message and update.effective_message.text:
                    await self._handle_message(update, None)
                max_update_id = max(max_update_id, update.update_id)

            if max_update_id >= 0:
                await bot.get_updates(offset=max_update_id + 1, timeout=0)
                self._record_update_id(max_update_id)

    async def send_typing(self, chat_id: str):
        """Send typing indicator."""
        bot = Bot(self.bot_token)
        async with bot:
            await bot.send_chat_action(chat_id=int(chat_id), action=ChatAction.TYPING)

    async def send_message(self, chat_id: str, text: str, reply_markup=None):
        """Send a message, with HTML formatting and fallback."""
        bot = Bot(self.bot_token)
        async with bot:
            html_text = _markdown_to_telegram_html(text)
            chunks = _chunk_text(html_text, limit=4096)
            for i, chunk in enumerate(chunks):
                is_last = i == len(chunks) - 1
                try:
                    await bot.send_message(
                        chat_id=int(chat_id),
                        text=chunk,
                        parse_mode=ParseMode.HTML,
                        reply_markup=reply_markup if is_last else None,
                    )
                except Exception:
                    # Fallback to plain text
                    logger.warning("HTML send failed, falling back to plain text")
                    plain_chunks = _chunk_text(text, limit=4096)
                    for j, plain in enumerate(plain_chunks):
                        is_last_plain = j == len(plain_chunks) - 1
                        await bot.send_message(
                            chat_id=int(chat_id),
                            text=plain,
                            reply_markup=reply_markup if is_last_plain else None,
                        )
                    break

    def send_message_sync(self, chat_id: str, text: str):
        """Send a message from a non-async context (worker thread)."""
        if self._loop is None:
            logger.error("No event loop available for sync send")
            return

        followups = extract_followups(text)
        reply_markup = None
        if followups:
            text = strip_followups_section(text)
            buttons = [
                [InlineKeyboardButton(text=fu["label"][:64], callback_data=fu["command"][:64])]
                for fu in followups[:5]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)

        future = asyncio.run_coroutine_threadsafe(
            self.send_message(chat_id, text, reply_markup=reply_markup), self._loop
        )
        future.result(timeout=30)

    def send_typing_sync(self, chat_id: str):
        """Send a typing indicator from a non-async context (worker thread)."""
        if self._loop is None:
            return
        future = asyncio.run_coroutine_threadsafe(
            self.send_typing(chat_id), self._loop
        )
        try:
            future.result(timeout=10)
        except Exception:
            logger.warning("send_typing_sync failed", exc_info=True)


def _markdown_to_telegram_html(text: str) -> str:
    """Convert basic Markdown to Telegram HTML."""
    # Code blocks first (before inline code): ```text``` -> <pre>text</pre>
    text = re.sub(r"```(?:\w+)?\n?(.*?)```", r"<pre>\1</pre>", text, flags=re.DOTALL)
    # Bold: **text** -> <b>text</b>
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    # Italic: *text* -> <i>text</i>  (but not inside bold tags)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    # Inline code: `text` -> <code>text</code>
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # Links: [text](url) -> <a href="url">text</a>
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def _append_web_link(output: str, link_type: str, params: dict | None = None) -> str:
    """Append a web UI link if WEB_UI_ENABLED=true."""
    import os
    if os.getenv("WEB_UI_ENABLED", "").lower() != "true":
        return output

    params = params or {}
    base = "http://localhost:3000"
    links = {
        "landscape": f"{base}/landscape?theme={params.get('theme_id', '')}",
        "briefing": base + "/landscape",
        "beliefs": base + "/beliefs",
        "challenge": f"{base}/landscape?entity={params.get('entity_type', '')}&id={params.get('entity_id', '')}&tab=history",
        "activity": base + "/activity",
        "ideas": f"{base}/library?tab=ideas&source={params.get('source_id', '')}",
        "predictions": f"{base}/predictions?filter={params.get('filter', '')}",
        "gaps": base + "/landscape",
    }
    url = links.get(link_type, base)
    return f"{output}\n\n🔗 <a href=\"{url}\">Open in Web UI</a>"


def _chunk_text(text: str, limit: int = 4096) -> list[str]:
    """Split text into chunks at newline boundaries."""
    if len(text) <= limit:
        return [text]

    chunks = []
    current = ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 > limit:
            if current:
                chunks.append(current)
            current = line[:limit]  # Truncate very long lines
        else:
            current = current + "\n" + line if current else line

    if current:
        chunks.append(current)

    return chunks
