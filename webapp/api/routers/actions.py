"""Actions API router for provider-aware chat commands."""

from __future__ import annotations

from functools import lru_cache
from importlib import import_module
import re

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
from gateway.model_preferences import (
    get_config_default_model_tier,
    get_model_tier_label,
    list_model_tier_metadata,
    match_model_tier,
)
from gateway.models import Event, Job
from gateway.providers import (
    WEBAPP_CHAT_ID,
    build_chat_session_key,
    get_default_provider_id,
    get_provider_label,
    normalize_provider_id,
)
from gateway.queue import DEFAULT_QUEUE_DB_PATH, Queue
from reading_app.config import Config
from reading_app.runtime import get_process_files, read_live_pid

router = APIRouter(prefix="/api/actions", tags=["actions"])

_JOBS_DB_PATH = DEFAULT_QUEUE_DB_PATH
_DIRECT_WEB_HANDLERS = {
    "ask": ("gateway.ask_handler", "handle_ask_job"),
    "landscape": ("gateway.landscape_handler", "handle_landscape_job"),
    "provider": ("gateway.provider_handler", "handle_provider_job"),
    "model": ("gateway.model_handler", "handle_model_job"),
}
_COMMAND_RE = re.compile(r"^/(?P<command>[a-z_]+)\b", re.IGNORECASE)

_ACTION_SKILL_MAP = {
    "save": "save",
    "enrich": "enrich",
    "challenge": "challenge",
    "ask": "ask",
    "reflect": "reflect",
    "delete": "delete",
    "implications": "implications",
    "provider": "provider",
    "model": "model",
}


class ActionRequest(BaseModel):
    text: str
    context: dict | None = None
    provider_id: str | None = None


class ProviderUpdateRequest(BaseModel):
    provider_id: str


class ModelUpdateRequest(BaseModel):
    model_tier: str


@lru_cache(maxsize=1)
def _get_config() -> Config:
    return Config()


@lru_cache(maxsize=1)
def _get_executor() -> ClaudeExecutor:
    return ClaudeExecutor(DEFAULT_WORKSPACE)


def _extract_command(text: str) -> str | None:
    match = _COMMAND_RE.match((text or "").strip())
    if not match:
        return None
    return match.group("command").lower()


def _gateway_ready() -> bool:
    files = get_process_files("gateway")
    return read_live_pid(files.pid_file) is not None and files.ready_file.exists()


def _web_session_key() -> str:
    return build_chat_session_key(WEBAPP_CHAT_ID)


def _provider_status_map() -> dict[str, dict]:
    return {status["id"]: status for status in _get_executor().get_backend_statuses()}


def _require_provider_available(provider_id: str) -> dict:
    status = _provider_status_map()[provider_id]
    if not status.get("available"):
        reason = status.get("reason") or "Finish that provider's setup first."
        raise HTTPException(
            status_code=503,
            detail=f"{status['label']} is not available. {reason}",
        )
    return status


def _resolve_provider_id(q: Queue, explicit_provider_id: str | None = None) -> str:
    if explicit_provider_id:
        return normalize_provider_id(explicit_provider_id)
    return q.get_chat_provider(_web_session_key()) or get_default_provider_id()


def _provider_payload(req: ActionRequest, provider_id: str) -> dict:
    return {
        "text": req.text,
        "context": req.context or {},
        "provider_id": provider_id,
        "chat_id": WEBAPP_CHAT_ID,
    }


def _run_direct_command(command: str, req: ActionRequest) -> dict:
    module_path, func_name = _DIRECT_WEB_HANDLERS[command]
    handler = getattr(import_module(module_path), func_name)
    q = Queue(db_path=_JOBS_DB_PATH)
    provider_id = _resolve_provider_id(q, req.provider_id)

    if command not in {"provider", "model"}:
        _require_provider_available(provider_id)
        if req.provider_id:
            q.set_chat_provider(_web_session_key(), provider_id)

    event = Event(
        type="human_message",
        payload=_provider_payload(req, provider_id),
        source="webapp",
        chat_id=WEBAPP_CHAT_ID,
    )
    job = Job(event_id=0, skill=command, id=0, provider_id=provider_id)
    executor = _get_executor().for_backend(provider_id)

    if command == "provider":
        response = handler(event, job, _get_config(), executor, queue=q)
        provider_id = q.get_chat_provider(_web_session_key()) or provider_id
        model_tier = q.get_global_model() or get_config_default_model_tier()
    elif command == "model":
        response = handler(event, job, _get_config(), executor, queue=q)
        model_tier = q.get_global_model() or get_config_default_model_tier()
    else:
        response = handler(event, job, _get_config(), executor)
        model_tier = q.get_global_model() or get_config_default_model_tier()

    if not response:
        response = f"/{command} completed with no output."

    payload = {
        "mode": "direct",
        "skill": command,
        "status": "complete",
        "response": response,
        "provider_id": provider_id,
        "provider_label": get_provider_label(provider_id),
    }
    if command == "model":
        payload["model_tier"] = model_tier
        payload["model_label"] = get_model_tier_label(model_tier)
    return payload


def _submit(action: str, req: ActionRequest) -> dict:
    skill = _ACTION_SKILL_MAP.get(action, action)
    q = Queue(db_path=_JOBS_DB_PATH)
    provider_id = _resolve_provider_id(q, req.provider_id)
    _require_provider_available(provider_id)

    if req.provider_id:
        q.set_chat_provider(_web_session_key(), provider_id)

    event = Event(
        type=action,
        payload=_provider_payload(req, provider_id),
        source="webapp",
        chat_id=WEBAPP_CHAT_ID,
    )
    event_id = q.insert_event(event)

    job = Job(event_id=event_id, skill=skill, provider_id=provider_id)
    job_id = q.insert_job(job)

    return {
        "job_id": job_id,
        "event_id": event_id,
        "skill": skill,
        "status": "pending",
        "provider_id": provider_id,
        "provider_label": get_provider_label(provider_id),
    }


@router.post("/command")
def action_command(req: ActionRequest):
    command = _extract_command(req.text)
    if command in _DIRECT_WEB_HANDLERS:
        return _run_direct_command(command, req)

    if not _gateway_ready():
        raise HTTPException(
            status_code=503,
            detail=(
                "The background worker is offline. Use /ask, /landscape, or /provider for direct actions, "
                "or /model to update the global default, "
                "or start the gateway to run queued commands."
            ),
        )

    q = Queue(db_path=_JOBS_DB_PATH)
    provider_id = _resolve_provider_id(q, req.provider_id)
    _require_provider_available(provider_id)

    if req.provider_id:
        q.set_chat_provider(_web_session_key(), provider_id)

    event = Event(
        type="human_message",
        payload=_provider_payload(req, provider_id),
        source="webapp",
        chat_id=WEBAPP_CHAT_ID,
    )
    event_id = q.insert_event(event)

    job = Job(event_id=event_id, skill="pending", provider_id=provider_id)
    job_id = q.insert_job(job)

    return {
        "mode": "queued",
        "job_id": job_id,
        "event_id": event_id,
        "skill": "pending",
        "status": "pending",
        "provider_id": provider_id,
        "provider_label": get_provider_label(provider_id),
    }


@router.post("/provider")
def action_provider(req: ProviderUpdateRequest):
    q = Queue(db_path=_JOBS_DB_PATH)
    provider_id = normalize_provider_id(req.provider_id)
    _require_provider_available(provider_id)
    q.set_chat_provider(_web_session_key(), provider_id)
    return {
        "status": "ok",
        "provider_id": provider_id,
        "provider_label": get_provider_label(provider_id),
        "providers": _get_executor().get_backend_statuses(),
    }


@router.post("/model")
def action_model(req: ModelUpdateRequest):
    q = Queue(db_path=_JOBS_DB_PATH)
    model_tier = match_model_tier(req.model_tier)
    if not model_tier:
        raise HTTPException(
            status_code=400,
            detail="Unknown model tier. Use fast, balanced, deep, haiku, sonnet, or opus.",
        )
    model_tier = q.set_global_model(model_tier)
    return {
        "status": "ok",
        "model_tier": model_tier,
        "model_label": get_model_tier_label(model_tier),
        "model_options": list_model_tier_metadata(),
    }


@router.post("/save")
def action_save(req: ActionRequest):
    return _submit("save", req)


@router.post("/enrich")
def action_enrich(req: ActionRequest):
    return _submit("enrich", req)


@router.post("/challenge")
def action_challenge(req: ActionRequest):
    return _submit("challenge", req)


@router.post("/ask")
def action_ask(req: ActionRequest):
    return _submit("ask", req)


@router.post("/reflect")
def action_reflect(req: ActionRequest):
    return _submit("reflect", req)


@router.post("/delete")
def action_delete(req: ActionRequest):
    return _submit("delete", req)


@router.post("/implications")
def action_implications(req: ActionRequest):
    return _submit("implications", req)
