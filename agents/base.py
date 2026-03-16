"""BaseAgent wrapping ClaudeExecutor with shared model/session and cost tracking."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

from agents.executor import ClaudeExecutor, ExecutionResult

logger = logging.getLogger(__name__)


class DeadlineExceeded(Exception):
    """Raised when a deadline is about to be exceeded."""


@dataclass
class AgentCostTracker:
    """Tracks cumulative cost across agent invocations."""
    total_usd: float = 0.0
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0

    def record(self, result: ExecutionResult):
        self.calls += 1
        if result.cost_usd:
            self.total_usd += result.cost_usd
        if result.usage:
            self.input_tokens += result.usage.get("input_tokens", 0)
            self.output_tokens += result.usage.get("output_tokens", 0)


class BaseAgent:
    """Base class for tournament pipeline agents."""

    def __init__(
        self,
        executor: ClaudeExecutor,
        model: str | None = None,
        session_prefix: str = "agent",
    ):
        self.executor = executor
        self.model = model
        self.session_prefix = session_prefix
        self.cost_tracker = AgentCostTracker()

    def _run(
        self,
        prompt: str,
        session_id: str | None = None,
        deadline: float | None = None,
        **kwargs,
    ) -> ExecutionResult:
        """Run a prompt through the executor with cost tracking.

        Args:
            deadline: Optional monotonic timestamp. When set, dynamically
                computes the subprocess timeout from remaining time. Raises
                DeadlineExceeded if <=10s remain before starting.
        """
        if deadline is not None:
            remaining = deadline - time.monotonic()
            if remaining <= 10:
                raise DeadlineExceeded(
                    f"Only {remaining:.0f}s remaining, skipping {session_id or self.session_prefix}"
                )
            kwargs["timeout"] = max(30, int(remaining))

        sid = session_id or f"{self.session_prefix}_default"
        result = self.executor.run_raw(
            prompt,
            session_id=sid,
            model=self.model,
            **kwargs,
        )
        self.cost_tracker.record(result)
        self.executor.cleanup_session(sid)
        return result
