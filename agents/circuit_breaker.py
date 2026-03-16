"""Circuit breaker and concurrency control for CLI backends."""

from __future__ import annotations

import threading
import time

import structlog

from agents.backend_config import _env_int, _env_float
from gateway.providers import normalize_provider_id, VALID_PROVIDER_IDS

logger = structlog.get_logger(__name__)

_api_semaphores: dict[str, threading.Semaphore] = {}
_circuit_breakers: dict[str, "CLICircuitBreaker"] = {}
_sem_lock = threading.Lock()
_cb_lock = threading.Lock()


class CLICircuitBreaker:
    """Trip after consecutive CLI failures to avoid wasting time on doomed calls."""

    def __init__(
        self,
        *,
        backend_id: str,
        threshold: int | None = None,
        cooldown_s: float | None = None,
    ):
        env_suffix = backend_id.upper()
        self.backend_id = backend_id
        self.threshold = threshold or _env_int(
            f"KB_CIRCUIT_BREAKER_THRESHOLD_{env_suffix}",
            "KB_CIRCUIT_BREAKER_THRESHOLD",
            default=5,
        )
        self.cooldown_s = cooldown_s or _env_float(
            f"KB_CIRCUIT_BREAKER_COOLDOWN_S_{env_suffix}",
            "KB_CIRCUIT_BREAKER_COOLDOWN_S",
            default=120.0,
        )
        self._consecutive_failures = 0
        self._state = "closed"
        self._opened_at = 0.0
        self._lock = threading.Lock()

    @property
    def state(self) -> str:
        with self._lock:
            if self._state == "open" and time.monotonic() - self._opened_at >= self.cooldown_s:
                self._state = "half_open"
                logger.info("circuit_breaker_half_open", backend_id=self.backend_id)
            return self._state

    def is_open(self) -> bool:
        return self.state == "open"

    def allow_request(self) -> bool:
        return self.state in ("closed", "half_open")

    def record_success(self) -> None:
        with self._lock:
            self._consecutive_failures = 0
            if self._state in ("open", "half_open"):
                logger.info(
                    "circuit_breaker_closed",
                    backend_id=self.backend_id,
                    previous=self._state,
                )
            self._state = "closed"

    def record_failure(self) -> None:
        with self._lock:
            self._consecutive_failures += 1
            if self._state == "half_open":
                self._state = "open"
                self._opened_at = time.monotonic()
                logger.warning("circuit_breaker_reopened", backend_id=self.backend_id)
            elif self._state == "closed" and self._consecutive_failures >= self.threshold:
                self._state = "open"
                self._opened_at = time.monotonic()
                logger.warning(
                    "circuit_breaker_opened",
                    backend_id=self.backend_id,
                    consecutive_failures=self._consecutive_failures,
                    cooldown_s=self.cooldown_s,
                )

    def reset(self) -> None:
        with self._lock:
            self._consecutive_failures = 0
            self._state = "closed"


def get_circuit_breaker(backend_id: str = "claude") -> CLICircuitBreaker:
    """Return the provider-specific circuit breaker."""
    normalized = normalize_provider_id(backend_id)
    with _cb_lock:
        breaker = _circuit_breakers.get(normalized)
        if breaker is None:
            breaker = CLICircuitBreaker(backend_id=normalized)
            _circuit_breakers[normalized] = breaker
    return breaker


def get_semaphore(backend_id: str) -> threading.Semaphore:
    """Return the provider-specific concurrency semaphore."""
    normalized = normalize_provider_id(backend_id)
    with _sem_lock:
        sem = _api_semaphores.get(normalized)
        if sem is None:
            env_suffix = normalized.upper()
            limit = _env_int(
                f"KB_MAX_CONCURRENT_API_CALLS_{env_suffix}",
                "KB_MAX_CONCURRENT_API_CALLS",
                default=5,
            )
            sem = threading.Semaphore(limit)
            _api_semaphores[normalized] = sem
            logger.info("api_semaphore_init", backend_id=normalized, limit=limit)
    return sem


def configure_concurrency(n: int, backend_id: str | None = None) -> None:
    """Override the API concurrency limit programmatically."""
    backend_ids = [normalize_provider_id(backend_id)] if backend_id else list(VALID_PROVIDER_IDS)
    with _sem_lock:
        for normalized in backend_ids:
            _api_semaphores[normalized] = threading.Semaphore(n)
            logger.info("api_semaphore_configured", backend_id=normalized, limit=n)
