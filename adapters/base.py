"""Base adapter protocol for messaging integrations."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Adapter(Protocol):
    """Protocol that all messaging adapters must implement.

    Adapters bridge external messaging platforms (Telegram, Discord, etc.)
    to the gateway's event queue. New adapters can be added by implementing
    this protocol and registering in gateway/main.py's ADAPTERS list.

    Lifecycle: start() and stop() are called from the async main loop.
    send_message_sync() and send_typing_sync() are called from the
    synchronous worker thread.
    """

    name: str

    async def start(self) -> None:
        """Start the adapter (connect, begin polling/listening)."""
        ...

    async def stop(self) -> None:
        """Gracefully stop the adapter."""
        ...

    def send_message_sync(self, chat_id: str, text: str) -> None:
        """Send a message from the sync worker thread."""
        ...

    def send_typing_sync(self, chat_id: str) -> None:
        """Send a typing indicator from the sync worker thread."""
        ...
