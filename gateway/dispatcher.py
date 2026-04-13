"""Event router, skill matcher, and executor wiring."""

from __future__ import annotations

import time
import structlog

from gateway.models import Event, Job
from gateway.providers import (
    build_chat_session_key,
    get_default_provider_id,
    get_provider_label,
    normalize_provider_id,
)
from gateway.queue import Queue
from reading_app.scheduler_ledger import SchedulerLedger

logger = structlog.get_logger(__name__)

DEBOUNCE_THRESHOLD = 0.5  # seconds
_FILE_WRITING_TOOLS = frozenset({"Write", "Edit", "Bash", "NotebookEdit"})


class Dispatcher:
    """Routes events to skills via the executor."""

    def __init__(
        self,
        queue: Queue,
        skill_registry,
        executor,
        memory_system,
        adapter_registry: dict[str, object] | None = None,
        config=None,
    ):
        self.queue = queue
        self.skill_registry = skill_registry
        self.executor = executor
        self.memory = memory_system
        self.adapter_registry = adapter_registry or {}
        self._config = config
        self._scheduler_ledger = SchedulerLedger()

    def _send_typing(self, source: str, chat_id: str) -> None:
        adapter = self.adapter_registry.get(source)
        if adapter and chat_id:
            try:
                adapter.send_typing_sync(chat_id)
            except Exception:
                logger.warning("send_typing_failed", source=source, exc_info=True)

    def _send_reply(self, source: str, chat_id: str, text: str) -> None:
        adapter = self.adapter_registry.get(source)
        if adapter and chat_id and text:
            try:
                adapter.send_message_sync(chat_id, text)
            except Exception:
                logger.error("send_reply_failed", source=source, exc_info=True)

    def _provider_status_map(self) -> dict[str, dict]:
        statuses = self.executor.get_backend_statuses()
        return {status["id"]: status for status in statuses}

    def _provider_executor(self, provider_id: str):
        binder = getattr(self.executor, "for_backend", None)
        if not callable(binder):
            return self.executor
        # Real executor class with a declared for_backend method
        if any("for_backend" in klass.__dict__ for klass in type(self.executor).__mro__):
            return binder(provider_id)
        # Support test mocks with explicitly configured for_backend
        try:
            from unittest.mock import DEFAULT
            if getattr(binder, "_mock_return_value", DEFAULT) is not DEFAULT:
                return binder(provider_id)
        except ImportError:
            pass
        return self.executor

    def _resolve_provider_id(self, event: Event, job: Job, chat_session_key: str) -> str:
        payload = event.payload if isinstance(event.payload, dict) else {}
        explicit = payload.get("provider_id")
        if explicit:
            return normalize_provider_id(explicit)
        stored = self.queue.get_chat_provider(chat_session_key)
        if stored:
            return stored
        if job.provider_id:
            return normalize_provider_id(job.provider_id)
        return get_default_provider_id()

    def _log_result_cost(
        self,
        result,
        *,
        provider_id: str,
        skill: str = "",
        job_id: int | None = None,
    ) -> None:
        """Extract cost/usage from an ExecutionResult and log it."""
        cost_usd = getattr(result, "cost_usd", None)
        usage = getattr(result, "usage", None) or {}
        input_tokens = usage.get("input_tokens") or usage.get("prompt_tokens")
        output_tokens = usage.get("output_tokens") or usage.get("completion_tokens")
        model = usage.get("model", "")
        if cost_usd is not None or input_tokens is not None or output_tokens is not None:
            try:
                self.queue.log_cost(
                    provider_id=provider_id,
                    model=model,
                    cost_usd=cost_usd,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    skill=skill,
                    job_id=job_id,
                )
            except Exception:
                logger.debug("cost_log_failed", exc_info=True)

    def _provider_unavailable_message(self, provider_id: str, reason: str) -> str:
        label = get_provider_label(provider_id)
        guidance = reason.strip() if reason.strip() else "Finish that provider's setup first."
        return f"{label} is not available for this chat. {guidance}"

    def _scheduled_slot(self, event: Event) -> dict | None:
        payload = event.payload if isinstance(event.payload, dict) else {}
        schedule = payload.get("_schedule")
        if not isinstance(schedule, dict):
            return None
        adapter = str(schedule.get("adapter") or "").strip()
        job_type = str(schedule.get("job_type") or "").strip()
        slot_key = str(schedule.get("slot_key") or "").strip()
        scheduled_for = str(schedule.get("scheduled_for") or "").strip()
        if not adapter or not job_type or not slot_key or not scheduled_for:
            return None
        metadata = schedule.get("metadata")
        if not isinstance(metadata, dict):
            metadata = {}
        return {
            "adapter": adapter,
            "job_type": job_type,
            "slot_key": slot_key,
            "scheduled_for": scheduled_for,
            "metadata": metadata,
        }

    def _mark_scheduled_status(self, event: Event, status: str) -> None:
        schedule = self._scheduled_slot(event)
        if schedule is None:
            return

        marker = {
            "complete": self._scheduler_ledger.mark_complete,
            "pending": self._scheduler_ledger.mark_pending,
            "failed": self._scheduler_ledger.mark_failed,
            "skipped_empty": self._scheduler_ledger.mark_skipped_empty,
            "enqueued": self._scheduler_ledger.mark_enqueued,
        }.get(status)
        if marker is None:
            return
        marker(
            schedule["adapter"],
            schedule["job_type"],
            schedule["slot_key"],
            scheduled_for=schedule["scheduled_for"],
            metadata=schedule["metadata"],
        )

    def process_next(self) -> bool:
        """Claim and process the next pending job.

        Returns True if a job was processed, False if the queue was empty.
        """
        job = self.queue.claim_next_job()
        if job is None:
            return False

        event = self.queue.get_event(job.event_id)
        if event is None:
            logger.error("event_not_found", job_id=job.id, event_id=job.event_id)
            self.queue.update_job_status(job.id, "failed", {"error": "event not found"})
            return True

        log = logger.bind(job_id=job.id, event_id=job.event_id, chat_id=event.chat_id)

        if event.created_at and (time.time() - event.created_at) < DEBOUNCE_THRESHOLD:
            log.debug("debounced")
            self.queue.update_job_status(job.id, "pending")
            return True

        chat_id = event.chat_id
        chat_session_key = build_chat_session_key(chat_id)
        provider_id = self._resolve_provider_id(event, job, chat_session_key)
        if provider_id != normalize_provider_id(job.provider_id or ""):
            self.queue.update_job_provider(job.id, provider_id)
            job.provider_id = provider_id

        self._send_typing(event.source, chat_id)

        text = event.payload.get("text", "")

        match_result = None
        if job.skill and job.skill in self.skill_registry.skills:
            skill = self.skill_registry.skills[job.skill]
            match_result = (skill, skill.match(text) or skill.match(f"/{job.skill} {text}"))

        if match_result is None:
            match_result = self.skill_registry.match(text)

        if event.type == "heartbeat":
            # Pre-heartbeat: incremental wiki lint (deterministic, <5s)
            try:
                from reading_app.db import ensure_pool
                ensure_pool()
                from retrieval.wiki_lint import run_lint_incremental
                run_lint_incremental()
                from retrieval.wiki_writer import populate_overview
                populate_overview()
            except Exception:
                logger.debug("heartbeat_lint_failed", exc_info=True)
            match_result = self.skill_registry.match("heartbeat")
        if event.type == "youtube_monitor":
            match_result = self.skill_registry.match("youtube_monitor")
        if event.type == "news_digest":
            match_result = self.skill_registry.match("news_digest")
        if event.type == "news_weekly":
            match_result = self.skill_registry.match("news_weekly")

        if match_result is None:
            skill_text = "You are a helpful research assistant. Answer the user's message."
            allowed_tools: list[str] = []
            denied_tools: list[str] = []
            timeout = 300
            stream_progress = False
            session_id = chat_session_key
            continue_session = True
            skill_name = "chat"
        else:
            skill, _match = match_result
            skill_text = skill.prompt_text(strip_frontmatter=True)
            allowed_tools = skill.tools_allowed
            denied_tools = skill.tools_denied
            timeout = skill.timeout
            stream_progress = skill.stream_progress
            is_stateless = skill.name in (
                "heartbeat",
                "save",
                "reflect",
                "delete",
                "implications",
                "beliefs",
                "challenge",
                "enrich",
                "changelog",
                "ideas",
                "next",
                "anticipate",
                "summarise",
                "save_confirmed",
                "youtube_monitor",
                "news_digest",
                "news_weekly",
                "path",
                "provider",
                "model",
            )
            session_id = skill.name if is_stateless else chat_session_key
            continue_session = not is_stateless
            skill_name = skill.name

        merge_meta = None

        if match_result is not None and skill_name == "synthesis":
            try:
                from retrieval.topic_synthesis import (
                    analyze_synthesis_context,
                    check_merge_cache,
                    format_merge_context,
                    format_synthesis_context,
                    gather_merge_context,
                    gather_synthesis_context,
                    resolve_source_refs,
                )

                raw_topic = text
                for prefix in ("/synthesis ", "/synthesis"):
                    if raw_topic.lower().startswith(prefix):
                        raw_topic = raw_topic[len(prefix):].strip()
                        break
                if raw_topic:
                    log.info("synthesis_prefetch_start", topic=raw_topic)

                    tokens = raw_topic.split()
                    source_ids = resolve_source_refs(tokens)

                    if source_ids and len(source_ids) >= 2:
                        cached = check_merge_cache(source_ids)
                        if cached:
                            log.info("merge_cache_hit", source_ids=source_ids)
                            skill_text += (
                                "\n\n---\n\n"
                                "## Cached Merge Report\n\n"
                                "A recent merge report already exists for these sources. "
                                "Return it directly to the user without modification.\n\n"
                                + cached
                            )
                        else:
                            ctx = gather_merge_context(source_ids)
                            if ctx is not None:
                                formatted = format_merge_context(ctx)
                                skill_text += (
                                    "\n\n---\n\n"
                                    "## Pre-Fetched Merge Data\n\n"
                                    "The following data has been gathered for a merge report. "
                                    "Write a standalone professional report following the merge prompt "
                                    "instructions below. Do NOT call any Python functions.\n\n"
                                    + formatted
                                )
                                merge_meta = {
                                    "source_ids": source_ids,
                                    "topic": ctx["topic"],
                                    "titles": [source["title"] for source in ctx["sources"]],
                                }
                                log.info("merge_prefetch_done", chars=len(formatted))
                            else:
                                skill_text += (
                                    "\n\n---\n\n"
                                    "## Pre-Fetched Merge Data\n\n"
                                    "Could not load data for the specified sources. "
                                    "Some sources may not exist or may not have completed processing. "
                                    "Inform the user."
                                )
                    else:
                        ctx = gather_synthesis_context(raw_topic)
                        if ctx is not None:
                            analysis = analyze_synthesis_context(ctx)
                            formatted = format_synthesis_context(ctx, analysis=analysis)
                            skill_text += (
                                "\n\n---\n\n"
                                "## Pre-Fetched Synthesis Data\n\n"
                                "The following data has been gathered from the knowledge base. "
                                "Synthesize your report directly from this data. "
                                "Do NOT call generate_topic_synthesis() or any Python functions.\n\n"
                                + formatted
                            )
                            log.info("synthesis_prefetch_done", chars=len(formatted))
                        else:
                            skill_text += (
                                "\n\n---\n\n"
                                "## Pre-Fetched Synthesis Data\n\n"
                                f"No sources or summaries found for topic: \"{raw_topic}\". "
                                "Inform the user that the knowledge base has no content matching this topic."
                            )
            except Exception:
                log.warning("synthesis_prefetch_failed", exc_info=True)

        memory_context = self.memory.load_context()

        resume_session_id = None
        if continue_session:
            resume_session_id = self.queue.get_session(session_id, provider_id)
            if resume_session_id:
                log.debug(
                    "session_resumed",
                    backend_id=provider_id,
                    backend_session_id=resume_session_id,
                )

        if skill_name != job.skill:
            self.queue.update_job_skill(job.id, skill_name)

        log = log.bind(skill=skill_name, timeout=timeout, provider_id=provider_id)
        log.info("job_started")
        start_ts = time.time()

        direct_handlers = {}
        if self._config is not None:
            direct_handlers["save"] = ("gateway.save_handler", "handle_save_job")
            direct_handlers["delete"] = ("gateway.delete_handler", "handle_delete_job")
            direct_handlers["reflect"] = ("gateway.reflect_handler", "handle_reflect_job")
            direct_handlers["implications"] = ("gateway.implications_handler", "handle_implications_job")
            direct_handlers["beliefs"] = ("gateway.beliefs_handler", "handle_beliefs_job")
            direct_handlers["challenge"] = ("gateway.challenge_handler", "handle_challenge_job")
            direct_handlers["enrich"] = ("gateway.enrich_handler", "handle_enrich_job")
            direct_handlers["changelog"] = ("gateway.changelog_handler", "handle_changelog_job")
            direct_handlers["ideas"] = ("gateway.ideas_handler", "handle_ideas_job")
            direct_handlers["next"] = ("gateway.next_handler", "handle_next_job")
            direct_handlers["anticipate"] = ("gateway.anticipate_handler", "handle_anticipate_job")
            direct_handlers["landscape"] = ("gateway.landscape_handler", "handle_landscape_job")
            direct_handlers["ask"] = ("gateway.ask_handler", "handle_ask_job")
            direct_handlers["summarise"] = ("gateway.summarise_handler", "handle_summarise_job")
            direct_handlers["save_confirmed"] = ("gateway.save_confirmed_handler", "handle_save_confirmed_job")
            direct_handlers["youtube_monitor"] = ("gateway.youtube_monitor_handler", "handle_youtube_monitor_job")
            direct_handlers["news_digest"] = ("gateway.news_digest_handler", "handle_news_digest_job")
            direct_handlers["news_weekly"] = ("gateway.news_weekly_handler", "handle_news_weekly_job")
            direct_handlers["path"] = ("gateway.path_handler", "handle_path_job")
            direct_handlers["provider"] = ("gateway.provider_handler", "handle_provider_job")
            direct_handlers["model"] = ("gateway.model_handler", "handle_model_job")
            direct_handlers["lint"] = ("gateway.lint_handler", "handle_lint_job")

        provider_status = self._provider_status_map().get(provider_id, {})
        if skill_name not in ("provider", "model") and not provider_status.get("available", True):
            message = self._provider_unavailable_message(
                provider_id,
                provider_status.get("reason", ""),
            )
            self.queue.update_job_status(
                job.id,
                "failed",
                {"error": message, "provider_id": provider_id},
            )
            self._mark_scheduled_status(event, "failed")
            self._send_reply(event.source, chat_id, message)
            return True

        if skill_name in direct_handlers:
            module_path, func_name = direct_handlers[skill_name]
            try:
                import importlib

                mod = importlib.import_module(module_path)
                handler_fn = getattr(mod, func_name)
                provider_executor = self._provider_executor(provider_id)

                direct_progress_cb = None
                if stream_progress:

                    def direct_progress_cb(snippet: str):
                        self.queue.update_job_progress(
                            job.id,
                            snippet,
                            provider_id=provider_id,
                            skill=skill_name,
                        )
                        if chat_id:
                            self._send_reply(event.source, chat_id, snippet)

                handler_kwargs = {"on_progress": direct_progress_cb}
                if skill_name in ("provider", "model"):
                    handler_kwargs["queue"] = self.queue

                response_text = handler_fn(
                    event,
                    job,
                    self._config,
                    provider_executor,
                    **handler_kwargs,
                )
                duration_ms = int((time.time() - start_ts) * 1000)

                if not response_text:
                    response_text = f"/{skill_name} completed but produced no output."
                    log.warning("empty_response", skill=skill_name)

                self._send_reply(event.source, chat_id, response_text)
                self._fire_memory_signals(skill_name, text, response_text)
                log.info("job_complete", duration_ms=duration_ms, handler=f"{skill_name}_direct")
                self.queue.update_job_status(
                    job.id,
                    "complete",
                    {
                        "response": response_text,
                        "handler": f"{skill_name}_direct",
                        "provider_id": provider_id,
                    },
                )
                self._mark_scheduled_status(event, "complete")
            except Exception as exc:
                duration_ms = int((time.time() - start_ts) * 1000)
                new_status = self.queue.retry_or_dead_letter(job.id, str(exc))
                if new_status == "pending":
                    self._mark_scheduled_status(event, "pending")
                    log.warning(
                        "job_retrying",
                        error=str(exc),
                        duration_ms=duration_ms,
                        retry_count=job.retry_count + 1,
                        handler=f"{skill_name}_direct",
                    )
                else:
                    self._mark_scheduled_status(event, "failed")
                    log.error(
                        "job_dead_letter",
                        error=str(exc),
                        duration_ms=duration_ms,
                        handler=f"{skill_name}_direct",
                        exc_info=True,
                    )
                    self._send_reply(event.source, chat_id, f"/{skill_name} failed: {str(exc)[:200]}")
            return True

        progress_cb = None
        if stream_progress:

            def progress_cb(snippet: str):
                self.queue.update_job_progress(
                    job.id,
                    snippet,
                    provider_id=provider_id,
                    skill=skill_name,
                )
                if chat_id:
                    self._send_reply(event.source, chat_id, snippet)

        sandbox_mode = (
            "full" if allowed_tools and _FILE_WRITING_TOOLS.intersection(allowed_tools) else None
        )

        try:
            provider_executor = self._provider_executor(provider_id)
            result = provider_executor.run(
                event_type=event.type,
                payload=event.payload,
                skill_text=skill_text,
                memory_context=memory_context,
                session_id=session_id,
                continue_session=continue_session,
                allowed_tools=allowed_tools if allowed_tools else None,
                denied_tools=denied_tools if denied_tools else None,
                timeout=timeout,
                on_progress=progress_cb,
                resume_session_id=resume_session_id,
                sandbox_mode=sandbox_mode,
            )

            duration_ms = int((time.time() - start_ts) * 1000)
            response_text = result.text

            if merge_meta and response_text and len(response_text) > 100:
                try:
                    from retrieval.topic_synthesis import save_merge_cache

                    save_merge_cache(
                        merge_meta["source_ids"],
                        response_text,
                        merge_meta["topic"],
                        merge_meta["titles"],
                    )
                except Exception:
                    log.warning("merge_cache_save_failed", exc_info=True)

            if continue_session and result.session_id_out:
                self.queue.upsert_session(
                    session_key=session_id,
                    backend_session_id=result.session_id_out,
                    backend_id=provider_id,
                    chat_id=chat_id,
                    skill=skill_name,
                )

            self._log_result_cost(result, provider_id=provider_id, skill=skill_name, job_id=job.id)

            if event.type == "heartbeat" and _is_heartbeat_ok(response_text):
                log.info("heartbeat_suppressed", cost_usd=result.cost_usd, duration_ms=duration_ms)
                self.queue.update_job_status(
                    job.id,
                    "complete",
                    {"suppressed": True, "cost_usd": result.cost_usd, "provider_id": provider_id},
                )
                self._mark_scheduled_status(event, "complete")
                return True

            if not response_text:
                response_text = f"/{skill_name} completed but produced no output."
                log.warning("empty_response", skill=skill_name)

            self._send_reply(event.source, chat_id, response_text)
            self._fire_memory_signals(skill_name, text, response_text)
            self._fire_wiki_filing(skill_name, text, response_text)

            log.info("job_complete", cost_usd=result.cost_usd, duration_ms=duration_ms)
            self.queue.update_job_status(
                job.id,
                "complete",
                {
                    "response": response_text,
                    "cost_usd": result.cost_usd,
                    "provider_id": provider_id,
                },
            )
            self._mark_scheduled_status(event, "complete")

        except Exception as exc:
            duration_ms = int((time.time() - start_ts) * 1000)
            new_status = self.queue.retry_or_dead_letter(job.id, str(exc))
            if new_status == "pending":
                self._mark_scheduled_status(event, "pending")
                log.warning(
                    "job_retrying",
                    error=str(exc),
                    duration_ms=duration_ms,
                    retry_count=job.retry_count + 1,
                )
            else:
                self._mark_scheduled_status(event, "failed")
                log.error("job_dead_letter", error=str(exc), duration_ms=duration_ms, exc_info=True)
                self._send_reply(event.source, chat_id, f"/{skill_name} failed: {str(exc)[:200]}")

        return True

    _MEMORY_SKILLS = frozenset({
        "save", "enrich", "challenge", "ask", "reflect", "landscape", "implications",
    })

    def _fire_memory_signals(self, skill_name: str, user_input: str, response_text: str) -> None:
        """Fire-and-forget: extract memory signals from this interaction in a daemon thread."""
        if skill_name not in self._MEMORY_SKILLS:
            return
        try:
            import threading
            from reading_app.memory_signals import extract_and_persist_signals
            memory_path = self.memory.memory_path / "memory.md"
            threading.Thread(
                target=extract_and_persist_signals,
                args=(skill_name, user_input, response_text, memory_path, self.executor),
            ).start()
        except Exception:
            logger.debug("memory_signal_extraction_failed", exc_info=True)

    _WIKI_SKILLS = frozenset({"synthesis", "contradictions", "bottlenecks"})

    def _fire_wiki_filing(self, skill_name: str, text: str, response_text: str) -> None:
        """Best-effort wiki auto-filing for executor-routed skills that produce wiki-ready output."""
        if skill_name not in self._WIKI_SKILLS:
            return
        try:
            import threading

            def _file():
                try:
                    from retrieval.wiki_writer import auto_file_skill_output
                    auto_file_skill_output(skill_name, text, response_text)
                except Exception:
                    logger.debug("wiki_filing_thread_failed", skill=skill_name, exc_info=True)

            threading.Thread(target=_file, name=f"wiki-file-{skill_name}").start()
        except Exception:
            logger.debug("wiki_filing_failed", exc_info=True)


def _is_heartbeat_ok(text: str) -> bool:
    """Check if the response is a heartbeat suppression signal."""
    return text.strip().upper() == "HEARTBEAT_OK"
