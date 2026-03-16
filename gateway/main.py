"""Entry point for the knowledge_base gateway system."""

from __future__ import annotations

import asyncio
import logging
import signal
import sys
import threading
import time

import structlog

from adapters.discord import DiscordAdapter
from adapters.heartbeat import HeartbeatAdapter
from adapters.telegram import TelegramAdapter
from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
from gateway.dispatcher import Dispatcher
from gateway.queue import Queue
from reading_app.config import Config
from reading_app.db import close_pool, init_pool
from reading_app.memory import MemorySystem
from reading_app.runtime import PROJECT_ROOT, acquire_pid_lock, clear_process_ready, mark_process_ready
from skills import SkillRegistry

_VAR_DIR = PROJECT_ROOT / "var"


def _configure_logging() -> None:
    """Configure structlog with JSON output and stdlib integration."""
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer()
            if sys.stderr.isatty()
            else structlog.processors.JSONRenderer(),
        ],
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.INFO)


_configure_logging()
logger = structlog.get_logger(__name__)


def main() -> None:
    files = acquire_pid_lock("gateway")
    config = Config()

    init_pool(config.postgres_dsn)

    from ingest.theme_classifier import refresh_static_theme_block
    from reading_app.db import get_conn

    try:
        refresh_static_theme_block(get_conn)
    except Exception:
        logger.warning("Failed to refresh theme block at startup", exc_info=True)

    queue = Queue()
    queue.cleanup_stale_sessions()
    queue.mark_running_interrupted()
    memory = MemorySystem(config.memory_path)
    skills = SkillRegistry()
    executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    adapters: list[object] = []

    if config.telegram_bot_token:
        adapters.append(
            TelegramAdapter(
                bot_token=config.telegram_bot_token,
                queue=queue,
                allowed_chat_id=config.telegram_allowed_chat_id,
                state_path=_VAR_DIR / "telegram_state.json",
            )
        )

    if config.discord_bot_token:
        adapters.append(
            DiscordAdapter(
                bot_token=config.discord_bot_token,
                queue=queue,
                allowed_user_id=config.discord_allowed_user_id,
            )
        )

    adapters.append(
        HeartbeatAdapter(
            queue=queue,
            memory_path=config.memory_path,
            timezone=config.heartbeat_timezone,
        )
    )

    if config.youtube_monitor_enabled:
        from adapters.youtube_monitor import YouTubeMonitorAdapter

        adapters.append(
            YouTubeMonitorAdapter(
                queue=queue,
                config=config,
                watchlist_path=config.memory_path / "youtube_watchlist.yaml",
                state_path=_VAR_DIR / "youtube_monitor_state.json",
                timezone=config.heartbeat_timezone,
            )
        )

    if config.news_digest_enabled:
        from adapters.news_digest import NewsDigestAdapter

        adapters.append(
            NewsDigestAdapter(
                queue=queue,
                config=config,
                config_path=config.memory_path / "news_digest_config.yaml",
                state_path=_VAR_DIR / "news_digest_state.json",
                timezone=config.heartbeat_timezone,
            )
        )

    adapter_registry = {adapter.name: adapter for adapter in adapters if adapter.name != "heartbeat"}
    dispatcher = Dispatcher(
        queue=queue,
        skill_registry=skills,
        executor=executor,
        memory_system=memory,
        adapter_registry=adapter_registry,
        config=config,
    )

    stop_event = threading.Event()

    def worker_loop() -> None:
        logger.info("worker_started")
        while not stop_event.is_set():
            try:
                processed = dispatcher.process_next()
                if not processed:
                    time.sleep(1)
            except Exception:
                logger.error("worker_error", exc_info=True)
                time.sleep(5)
        logger.info("worker_stopped")

    worker = threading.Thread(target=worker_loop, name="job-worker")
    worker.start()

    pp_executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    def postprocess_worker_loop() -> None:
        logger.info("postprocess_worker_started")
        from ingest.post_processor import poll_pending_source, run_post_processing
        from reading_app.db import get_conn

        while not stop_event.is_set():
            try:
                pending = poll_pending_source(get_conn)
                if not pending:
                    stop_event.wait(timeout=10)
                    continue

                source_id, theme_ids = pending
                pp_log = logger.bind(source_id=source_id)
                pp_log.info("postprocess_job_started")

                try:
                    result = run_post_processing(
                        source_id=source_id,
                        theme_ids=theme_ids,
                        executor=pp_executor,
                        get_conn_fn=get_conn,
                    )
                    pp_log.info(
                        "postprocess_job_complete",
                        steps={key: "ok" if not value.get("error") else "error" for key, value in result.items()},
                    )
                except Exception as exc:
                    pp_log.error("postprocess_job_failed", error=str(exc)[:200])
            except Exception:
                logger.error("postprocess_worker_error", exc_info=True)
                stop_event.wait(timeout=10)
        logger.info("postprocess_worker_stopped")

    pp_worker = threading.Thread(target=postprocess_worker_loop, name="postprocess-worker")
    pp_worker.start()

    async def run_gateway() -> None:
        for adapter in adapters:
            await adapter.start()
            logger.info("adapter_started", adapter=adapter.name)
        logger.info("system_ready", adapters=[adapter.name for adapter in adapters])
        mark_process_ready(files)

        loop = asyncio.get_running_loop()
        shutdown = asyncio.Event()

        def handle_signal() -> None:
            shutdown.set()

        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, handle_signal)
            except NotImplementedError:
                pass

        def _sync_signal_handler(signum, frame):
            loop.call_soon_threadsafe(shutdown.set)

        try:
            signal.signal(signal.SIGTERM, _sync_signal_handler)
            signal.signal(signal.SIGINT, _sync_signal_handler)
        except (OSError, ValueError):
            pass

        async def _poll_shutdown_file() -> None:
            while not shutdown.is_set():
                if files.shutdown_file.exists():
                    logger.info("shutdown_file_detected")
                    files.shutdown_file.unlink(missing_ok=True)
                    shutdown.set()
                    break
                await asyncio.sleep(1)

        asyncio.create_task(_poll_shutdown_file())

        try:
            await shutdown.wait()
        except KeyboardInterrupt:
            pass
        finally:
            clear_process_ready(files)
            logger.info("shutting_down")
            stop_event.set()
            for adapter in reversed(adapters):
                await adapter.stop()
                logger.info("adapter_stopped", adapter=adapter.name)
            max_timeout = max((skill.timeout for skill in skills.skills.values()), default=300) + 30
            logger.info("waiting_for_workers", max_timeout_s=max_timeout)
            worker.join(timeout=max_timeout)
            pp_worker.join(timeout=30)
            if worker.is_alive() or pp_worker.is_alive():
                logger.warning("worker_timeout", msg="marking in-flight jobs interrupted")
                queue.mark_running_interrupted()
            close_pool()
            logger.info("shutdown_complete")

    try:
        asyncio.run(run_gateway())
    except KeyboardInterrupt:
        stop_event.set()
        worker.join(timeout=30)
        pp_worker.join(timeout=15)
        logger.info("interrupted")


if __name__ == "__main__":
    main()
