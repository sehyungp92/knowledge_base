"""Shared artifact validation and source status assessment helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SUMMARY_FAILURE_MARKERS = (
    "you've hit your limit",
    "you have hit your limit",
    "hit your limit",
    "summary generation failed",
    "summary pending",
    "error generating summary",
)
MIN_SUMMARY_CHARS = 200
LANDSCAPE_KEYS = ("capabilities", "limitations", "bottlenecks", "breakthroughs")


def resolve_source_dir(library_path: str | Path | None, source_id: str) -> Path | None:
    """Resolve a source directory from either the library root or source directory."""
    if not library_path:
        return None

    base_path = Path(library_path)
    source_dir = base_path / source_id
    if source_dir.is_dir():
        return source_dir
    return base_path


def read_source_artifact_text(
    library_path: str | Path | None,
    source_id: str,
    filename: str,
) -> str | None:
    """Read a source artifact from disk if it exists."""
    source_dir = resolve_source_dir(library_path, source_id)
    if source_dir is None:
        return None

    artifact_path = source_dir / filename
    if not artifact_path.is_file():
        return None

    try:
        return artifact_path.read_text(encoding="utf-8")
    except OSError:
        return None


def read_source_artifact_json(
    library_path: str | Path | None,
    source_id: str,
    filename: str,
) -> dict[str, Any] | None:
    """Read a JSON source artifact from disk if it exists and parses cleanly."""
    text = read_source_artifact_text(library_path, source_id, filename)
    if text is None:
        return None

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return None

    return parsed if isinstance(parsed, dict) else None


def get_summary_issue(summary_text: str | None) -> str | None:
    """Return a machine-readable summary issue, or None when summary is usable."""
    if not summary_text or not summary_text.strip():
        return "missing"

    normalized = " ".join(summary_text.lower().split())
    for marker in SUMMARY_FAILURE_MARKERS:
        if marker in normalized:
            return "placeholder"

    if len(summary_text.strip()) < MIN_SUMMARY_CHARS:
        return "too_short"

    return None


def is_valid_summary(summary_text: str | None) -> bool:
    """Check whether a summary is usable in the app."""
    return get_summary_issue(summary_text) is None


def get_landscape_counts(signals: dict[str, Any] | None) -> dict[str, int]:
    """Count landscape signals by type."""
    counts: dict[str, int] = {}
    for key in LANDSCAPE_KEYS:
        values = signals.get(key, []) if isinstance(signals, dict) else []
        counts[key] = len(values) if isinstance(values, list) else 0
    counts["total"] = sum(counts.values())
    return counts


def get_landscape_issue(signals: dict[str, Any] | None) -> str | None:
    """Return a machine-readable landscape issue, or None when usable."""
    if not isinstance(signals, dict):
        return "missing"

    for key in LANDSCAPE_KEYS:
        values = signals.get(key, [])
        if not isinstance(values, list):
            return f"invalid_{key}"

    if get_landscape_counts(signals)["total"] == 0:
        return "empty"

    return None


def assess_source_quality(
    *,
    theme_count: int,
    claim_count: int,
    summary_text: str | None,
    landscape_signals: dict[str, Any] | None,
    require_summary: bool = True,
    require_landscape: bool = True,
) -> dict[str, Any]:
    """Assess whether a source has enough usable artifacts to be 'complete'."""
    issues: list[str] = []

    if theme_count <= 0:
        issues.append("no_themes")
    if claim_count <= 0:
        issues.append("no_claims")

    summary_issue = None
    if require_summary:
        summary_issue = get_summary_issue(summary_text)
        if summary_issue:
            issues.append(f"summary:{summary_issue}")

    landscape_issue = None
    if require_landscape:
        landscape_issue = get_landscape_issue(landscape_signals)
        if landscape_issue:
            issues.append(f"landscape:{landscape_issue}")

    return {
        "status": "complete" if not issues else "incomplete",
        "issues": issues,
        "theme_count": theme_count,
        "claim_count": claim_count,
        "summary_issue": summary_issue,
        "landscape_issue": landscape_issue,
        "landscape_counts": get_landscape_counts(landscape_signals),
    }


def refresh_source_processing_status(
    source_id: str,
    get_conn_fn,
    *,
    library_path: str | Path | None = None,
    require_summary: bool = True,
    require_landscape: bool = True,
) -> dict[str, Any]:
    """Recompute processing status from the persisted DB rows and source artifacts."""
    with get_conn_fn() as conn:
        source = conn.execute(
            "SELECT library_path FROM sources WHERE id = %s",
            (source_id,),
        ).fetchone()
        if not source:
            raise LookupError(f"Source '{source_id}' not found")

        theme_count = conn.execute(
            "SELECT COUNT(*) AS cnt FROM source_themes WHERE source_id = %s",
            (source_id,),
        ).fetchone()["cnt"]
        claim_count = conn.execute(
            "SELECT COUNT(*) AS cnt FROM claims WHERE source_id = %s",
            (source_id,),
        ).fetchone()["cnt"]

    effective_library_path = library_path or source.get("library_path")
    summary_text = None
    landscape_signals = None
    if require_summary:
        summary_text = read_source_artifact_text(
            effective_library_path, source_id, "deep_summary.md",
        )
    if require_landscape:
        landscape_signals = read_source_artifact_json(
            effective_library_path, source_id, "landscape.json",
        )

    assessment = assess_source_quality(
        theme_count=theme_count,
        claim_count=claim_count,
        summary_text=summary_text,
        landscape_signals=landscape_signals,
        require_summary=require_summary,
        require_landscape=require_landscape,
    )

    with get_conn_fn() as conn:
        conn.execute(
            "UPDATE sources SET processing_status = %s WHERE id = %s",
            (assessment["status"], source_id),
        )
        conn.commit()

    return assessment
