"""Structured run stages for long-running jobs.

Provides RunStage dataclass and stage map definitions for /save, /reflect topic,
and /reflect deep jobs.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class RunStage:
    """A single stage in a multi-step job run."""
    stage_key: str          # e.g. "claim_extraction", "landscape_update"
    stage_label: str        # e.g. "Extracting claims"
    status: str = "pending" # pending | running | complete | failed | skipped
    progress: float | None = None  # 0-1, None if indeterminate
    elapsed_ms: int = 0
    latest_message: str = ""
    artifacts: list[str] = field(default_factory=list)
    _start_time: float | None = field(default=None, repr=False)

    def start(self, message: str = ""):
        self.status = "running"
        self._start_time = time.monotonic()
        if message:
            self.latest_message = message

    def complete(self, message: str = "", artifacts: list[str] | None = None):
        self.status = "complete"
        if self._start_time:
            self.elapsed_ms = int((time.monotonic() - self._start_time) * 1000)
        self.progress = 1.0
        if message:
            self.latest_message = message
        if artifacts:
            self.artifacts.extend(artifacts)

    def fail(self, message: str = ""):
        self.status = "failed"
        if self._start_time:
            self.elapsed_ms = int((time.monotonic() - self._start_time) * 1000)
        if message:
            self.latest_message = message

    def skip(self, message: str = ""):
        self.status = "skipped"
        if message:
            self.latest_message = message

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage_key": self.stage_key,
            "stage_label": self.stage_label,
            "status": self.status,
            "progress": self.progress,
            "elapsed_ms": self.elapsed_ms,
            "latest_message": self.latest_message,
            "artifacts": self.artifacts,
        }


class StageTracker:
    """Manages a sequence of RunStages and emits progress updates."""

    def __init__(self, stage_defs: list[tuple[str, str]], on_progress: Callable[[str], None] | None = None):
        """Initialize with list of (stage_key, stage_label) tuples."""
        self.stages: list[RunStage] = [
            RunStage(stage_key=key, stage_label=label)
            for key, label in stage_defs
        ]
        self._stage_map: dict[str, RunStage] = {s.stage_key: s for s in self.stages}
        self._on_progress = on_progress

    def start(self, stage_key: str, message: str = ""):
        stage = self._stage_map.get(stage_key)
        if stage:
            stage.start(message)
            self._emit()

    def complete(self, stage_key: str, message: str = "", artifacts: list[str] | None = None):
        stage = self._stage_map.get(stage_key)
        if stage:
            stage.complete(message, artifacts)
            self._emit()

    def fail(self, stage_key: str, message: str = ""):
        stage = self._stage_map.get(stage_key)
        if stage:
            stage.fail(message)
            self._emit()

    def skip(self, stage_key: str, message: str = ""):
        stage = self._stage_map.get(stage_key)
        if stage:
            stage.skip(message)
            self._emit()

    def current_stage_index(self) -> int:
        """Return index of the currently running or next pending stage."""
        for i, s in enumerate(self.stages):
            if s.status == "running":
                return i
            if s.status == "pending":
                return i
        return len(self.stages)

    def progress_text(self) -> str:
        """Generate human-readable progress text with step counter."""
        idx = self.current_stage_index()
        total = len(self.stages)
        current = self.stages[idx] if idx < total else None
        if current:
            return f"Step {idx + 1}/{total}: {current.stage_label}"
        return f"Complete ({total}/{total})"

    def to_list(self) -> list[dict[str, Any]]:
        return [s.to_dict() for s in self.stages]

    def _emit(self):
        """Emit current progress via callback."""
        if self._on_progress:
            self._on_progress(self.progress_text())


# ---------------------------------------------------------------------------
# Stage definitions per job type
# ---------------------------------------------------------------------------

SAVE_STAGES: list[tuple[str, str]] = [
    ("fetch", "Fetching source content"),
    ("classify", "Classifying themes"),
    ("extract_claims", "Extracting claims with evidence"),
    ("summary", "Generating deep summary"),
    ("landscape", "Extracting landscape signals"),
    ("implications", "Cross-theme implications"),
    ("graph", "Computing edges"),
    ("wiki", "Updating wiki"),
]

REFLECT_TOPIC_STAGES: list[tuple[str, str]] = [
    ("outline", "Planning report structure"),
    ("retrieve", "Running analytical lenses"),
    ("generate", "Writing sections"),
    ("persist", "Saving artifacts"),
]

REFLECT_DEEP_STAGES: list[tuple[str, str]] = [
    ("retrieve", "Finding neighbors"),
    ("generate", "Generating candidates"),
    ("novelty", "Novelty gate"),
    ("critique", "Individual critique"),
    ("debate", "Two-tier debate"),
    ("evolve", "Evolving weak candidates"),
    ("rank", "Final ranking"),
]
