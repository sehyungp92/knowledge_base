"""Managed API server entrypoint for local background execution."""

from __future__ import annotations

import asyncio
import logging
import signal

import uvicorn

from reading_app.config import Config
from reading_app.runtime import acquire_pid_lock, clear_process_ready, mark_process_ready

logger = logging.getLogger(__name__)


def main() -> None:
    files = acquire_pid_lock("api")
    config = Config()
    server = uvicorn.Server(
        uvicorn.Config(
            "webapp.api.main:app",
            host=config.api_host,
            port=config.api_port,
            log_level="info",
        )
    )

    async def _serve() -> None:
        loop = asyncio.get_running_loop()
        shutdown = asyncio.Event()

        def _request_shutdown() -> None:
            server.should_exit = True
            shutdown.set()

        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, _request_shutdown)
            except NotImplementedError:
                pass

        def _sync_signal_handler(signum, frame):
            loop.call_soon_threadsafe(_request_shutdown)

        try:
            signal.signal(signal.SIGTERM, _sync_signal_handler)
            signal.signal(signal.SIGINT, _sync_signal_handler)
        except (OSError, ValueError):
            pass

        async def _poll_shutdown_file() -> None:
            while not shutdown.is_set():
                if files.shutdown_file.exists():
                    logger.info("api_shutdown_file_detected")
                    files.shutdown_file.unlink(missing_ok=True)
                    _request_shutdown()
                    break
                await asyncio.sleep(1)

        async def _mark_ready_when_started() -> None:
            while not shutdown.is_set():
                if server.started:
                    mark_process_ready(files)
                    return
                await asyncio.sleep(0.1)

        poll_task = asyncio.create_task(_poll_shutdown_file())
        ready_task = asyncio.create_task(_mark_ready_when_started())
        try:
            await server.serve()
        finally:
            clear_process_ready(files)
            _request_shutdown()
            poll_task.cancel()
            ready_task.cancel()
            await asyncio.gather(poll_task, ready_task, return_exceptions=True)

    asyncio.run(_serve())


if __name__ == "__main__":
    main()
