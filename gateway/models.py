"""Event and Job data models for the gateway."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    type: str
    payload: dict
    source: str = ""
    chat_id: str = ""
    id: int | None = None
    created_at: float | None = None
    status: str = "pending"


@dataclass
class Job:
    event_id: int
    skill: str
    id: int | None = None
    status: str = "pending"
    logs_path: str = ""
    result: dict | None = None
    created_at: float | None = None
    updated_at: float | None = None
    retry_count: int = 0
    max_retries: int = 2
    provider_id: str = ""
