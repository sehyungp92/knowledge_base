"""Discord DM adapter."""

from __future__ import annotations

import asyncio
import logging

import discord

from gateway.followups import extract_followups, strip_followups_section
from gateway.models import Event, Job
from gateway.providers import build_chat_session_key, get_default_provider_id
from gateway.queue import Queue

logger = logging.getLogger(__name__)


class DiscordAdapter:
    """Discord bot adapter for DM-based interaction.

    Implements the Adapter protocol from adapters.base.
    """

    name: str = "discord"

    def __init__(self, bot_token: str, queue: Queue, allowed_user_id: str = ""):
        self.bot_token = bot_token
        self.queue = queue
        self.allowed_user_id = allowed_user_id
        self._loop: asyncio.AbstractEventLoop | None = None
        self._client: discord.Client | None = None

    async def start(self):
        """Start the Discord bot (non-blocking)."""
        intents = discord.Intents.default()
        intents.dm_messages = True
        intents.message_content = True

        self._client = discord.Client(intents=intents)

        @self._client.event
        async def on_ready():
            logger.info("Discord bot connected as %s", self._client.user)

        @self._client.event
        async def on_message(message: discord.Message):
            await self._handle_message(message)

        @self._client.event
        async def on_interaction(interaction: discord.Interaction):
            await self._handle_interaction(interaction)

        self._loop = asyncio.get_running_loop()
        asyncio.ensure_future(self._client.start(self.bot_token))
        logger.info("Discord adapter started")

    async def stop(self):
        """Stop the Discord bot."""
        if self._client:
            await self._client.close()

    async def _handle_message(self, message: discord.Message):
        """Handle incoming Discord DMs."""
        # Skip bot messages
        if message.author.bot:
            return

        # Only accept DMs (no guild messages)
        if message.guild is not None:
            return

        # Skip empty messages
        if not message.content:
            return

        user_id = str(message.author.id)

        # Access control
        if self.allowed_user_id and user_id != self.allowed_user_id:
            logger.warning("Rejected message from unauthorized user_id: %s", user_id)
            return

        # Create event
        event = Event(
            type="human_message",
            payload={"text": message.content, "chat_id": user_id, "message_id": message.id},
            source="discord",
            chat_id=user_id,
        )
        event_id = self.queue.insert_event(event)
        session_key = build_chat_session_key(user_id)
        provider_id = self.queue.get_chat_provider(session_key) or get_default_provider_id()
        self.queue.insert_job(Job(event_id=event_id, skill="pending", provider_id=provider_id))
        logger.info("Discord event %d created for user %s: %s", event_id, user_id, message.content[:50])

    async def _handle_interaction(self, interaction: discord.Interaction):
        """Handle button clicks from follow-up options."""
        if interaction.type != discord.InteractionType.component:
            return

        custom_id = interaction.data.get("custom_id", "") if interaction.data else ""
        if not custom_id:
            return

        user_id = str(interaction.user.id)

        if self.allowed_user_id and user_id != self.allowed_user_id:
            return

        await interaction.response.defer()

        event = Event(
            type="human_message",
            payload={"text": custom_id, "chat_id": user_id, "message_id": interaction.message.id if interaction.message else 0},
            source="discord",
            chat_id=user_id,
        )
        event_id = self.queue.insert_event(event)
        session_key = build_chat_session_key(user_id)
        provider_id = self.queue.get_chat_provider(session_key) or get_default_provider_id()
        self.queue.insert_job(Job(event_id=event_id, skill="pending", provider_id=provider_id))
        logger.info("Discord interaction event %d for user %s: %s", event_id, user_id, custom_id[:50])

    async def send_message(self, chat_id: str, text: str):
        """Send a message via Discord DM."""
        if not self._client:
            return
        user = await self._client.fetch_user(int(chat_id))
        dm_channel = user.dm_channel or await user.create_dm()

        followups = extract_followups(text)
        view = None
        if followups:
            text = strip_followups_section(text)
            view = discord.ui.View(timeout=None)
            for fu in followups[:5]:
                view.add_item(discord.ui.Button(
                    label=fu["label"][:80],
                    custom_id=fu["command"][:100],
                    style=discord.ButtonStyle.secondary,
                ))

        chunks = _chunk_text(text, limit=2000)
        for i, chunk in enumerate(chunks):
            is_last = i == len(chunks) - 1
            await dm_channel.send(chunk, view=view if is_last and view else None)

    async def send_typing(self, chat_id: str):
        """Send typing indicator via Discord DM."""
        if not self._client:
            return
        user = await self._client.fetch_user(int(chat_id))
        dm_channel = user.dm_channel or await user.create_dm()
        await dm_channel.typing()

    def send_message_sync(self, chat_id: str, text: str):
        """Send a message from a non-async context (worker thread)."""
        if self._loop is None:
            logger.error("No event loop available for sync send")
            return
        future = asyncio.run_coroutine_threadsafe(
            self.send_message(chat_id, text), self._loop
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


def _chunk_text(text: str, limit: int = 2000) -> list[str]:
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
