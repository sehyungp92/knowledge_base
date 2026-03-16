"""Small benchmarking helpers for comparing provider latency and stability."""

from __future__ import annotations

import json
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE


def run_latency_harness(
    *,
    output_path: Path | str,
    providers: list[str] | None = None,
    samples_per_provider: int = 1,
    measure: Callable[[str], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Run a lightweight latency harness and write a JSON report."""
    executor: ClaudeExecutor | None = None
    if measure is None or providers is None:
        executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    if providers is not None:
        provider_ids = list(providers)
    else:
        assert executor is not None
        provider_ids = [
            status["id"]
            for status in executor.get_backend_statuses()
            if status.get("available")
        ]

    report: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "providers": [],
    }

    for provider_id in provider_ids:
        sample_rows: list[dict[str, Any]] = []
        for _ in range(max(samples_per_provider, 1)):
            started_at = time.perf_counter()
            if measure is not None:
                sample = dict(measure(provider_id) or {})
            else:
                assert executor is not None
                result = executor.health_check(backend_id=provider_id)
                sample = {
                    "success": result.success,
                    "failure_type": result.failure_type,
                }
            total_ms = int(sample.get("total_ms") or ((time.perf_counter() - started_at) * 1000))
            ttft_ms = sample.get("ttft_ms")
            sample_rows.append(
                {
                    "success": bool(sample.get("success", True)),
                    "failure_type": sample.get("failure_type"),
                    "resume_success": bool(sample.get("resume_success", False)),
                    "total_ms": total_ms,
                    "ttft_ms": int(ttft_ms) if ttft_ms is not None else total_ms,
                }
            )

        median_total_ms = int(statistics.median(row["total_ms"] for row in sample_rows))
        median_ttft_ms = int(statistics.median(row["ttft_ms"] for row in sample_rows))
        success_count = sum(1 for row in sample_rows if row["success"])
        resume_success_count = sum(1 for row in sample_rows if row["resume_success"])

        report["providers"].append(
            {
                "id": provider_id,
                "samples": len(sample_rows),
                "median_total_ms": median_total_ms,
                "median_ttft_ms": median_ttft_ms,
                "success_rate": round(success_count / len(sample_rows), 3),
                "resume_success_rate": round(resume_success_count / len(sample_rows), 3),
                "failures": [row["failure_type"] for row in sample_rows if row["failure_type"]],
            }
        )

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
