"""Shared utilities for source ingestion: date normalization, meta.yaml writing, participant parsing."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


def normalize_date(raw: str | None) -> str | None:
    """Normalize a date string to YYYY-MM-DD format.

    Handles: already-clean dates, YYYYMMDD (yt-dlp), D:YYYYMMDD... (PDF),
    ISO-8601 with time/tz, RFC 2822 (RSS). Returns None on failure.
    """
    if not raw:
        return None

    raw = raw.strip()
    if not raw:
        return None

    # Already YYYY-MM-DD
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
        return raw

    # PDF format: D:YYYYMMDD...
    if raw.startswith("D:"):
        raw = raw[2:]

    # Bare YYYYMMDD (yt-dlp or stripped PDF prefix)
    if re.fullmatch(r"\d{8}", raw):
        return f"{raw[:4]}-{raw[4:6]}-{raw[6:8]}"

    # ISO-8601 with time component: YYYY-MM-DDT... or YYYY-MM-DD ...
    m = re.match(r"(\d{4}-\d{2}-\d{2})[T ]", raw)
    if m:
        return m.group(1)

    # General fallback via dateutil
    try:
        from dateutil.parser import parse as dateutil_parse
        dt = dateutil_parse(raw, fuzzy=True)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None


# Fields to include in meta.yaml, in display order.
_META_FIELD_ORDER = [
    "id", "source_type", "url", "title", "authors", "published_at", "abstract",
    "arxiv_id", "categories", "category_theme_hints",
    "video_id", "channel", "podcast_name",
]

# Internal fields that should never appear in meta.yaml
_META_EXCLUDE = {
    "clean_text", "library_path", "processing_status", "metadata",
    "ingested_at", "fts_vector",
}


def write_meta_yaml(source_dir: Path, data: dict) -> None:
    """Write meta.yaml with consistent field order, skipping None/empty values."""
    ordered = {}
    for key in _META_FIELD_ORDER:
        if key in data:
            val = data[key]
            if val is None:
                continue
            if isinstance(val, (list, dict)) and not val:
                continue
            ordered[key] = val

    # Include any extra keys not in the standard order (but not excluded)
    for key, val in data.items():
        if key not in ordered and key not in _META_EXCLUDE:
            if val is None:
                continue
            if isinstance(val, (list, dict)) and not val:
                continue
            ordered[key] = val

    (source_dir / "meta.yaml").write_text(
        yaml.dump(ordered, default_flow_style=False, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def parse_participants_from_summary(summary: str) -> list[str]:
    """Extract participant names from a deep summary header.

    Looks for a 'Participants:' line before the first '---' separator.
    Returns a list of name strings with affiliations stripped.
    """
    if not summary:
        return []

    # Only search header (before first ---)
    header_end = summary.find("\n---\n")
    header = summary[:header_end] if header_end != -1 else summary[:500]

    # Match 'Participants:' or '**Participants:**' (with optional bold)
    m = re.search(r"\*{0,2}Participants:?\*{0,2}\s*(.+)", header)
    if not m:
        return []

    raw_line = m.group(1).strip()
    if not raw_line:
        return []

    # Split on commas, but respect parentheses
    # e.g. "Demis Hassabis (CEO, Google DeepMind), Alex Kantrowitz (host)"
    parts = []
    depth = 0
    current = []
    for char in raw_line:
        if char == "(":
            depth += 1
            current.append(char)
        elif char == ")":
            depth -= 1
            current.append(char)
        elif char == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if current:
        parts.append("".join(current).strip())

    # Strip parenthetical affiliations, return clean names
    names = []
    for part in parts:
        if not part:
            continue
        # Remove parenthetical suffix
        name = re.sub(r"\s*\(.*?\)\s*$", "", part).strip()
        if name:
            names.append(name)

    return names
