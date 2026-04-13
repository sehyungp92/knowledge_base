"""Deterministic wiki index and log maintenance.

Zero LLM cost — pure string manipulation of markdown index files.
Updates master index (wiki/index.md), typed sub-indexes (themes/index.md,
entities/index.md, sources/index.md), and the change log (wiki/log.md).
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import structlog

logger = structlog.get_logger(__name__)

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"

# Files that are NOT content pages (skip during rebuild_index scan)
_SKIP_FILES = frozenset({
    "index.md", "CONVENTIONS.md", "log.md", "overview.md",
})

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def on_page_created(page_path: Path, page_type: str, frontmatter: dict) -> None:
    """Register a newly created page in all relevant indexes."""
    try:
        row_fn = _ROW_FORMATTERS.get(page_type)
        if not row_fn:
            logger.warning("wiki_index_unknown_page_type", page_type=page_type)
            return

        row = row_fn(frontmatter, page_path)
        link_text = _link_text_from_path(page_path)

        # Master index
        master_marker = _PAGE_TYPE_TO_MASTER_MARKER.get(page_type)
        if master_marker:
            _upsert_table_row(WIKI_DIR / "index.md", master_marker, link_text, row)

        # Sub-index
        _update_sub_index(page_type, frontmatter, link_text, row, page_path)

        # Log
        title = frontmatter.get("title", page_path.stem)
        _append_log(f"Created {page_type} page: [[{_wiki_link_from_path(page_path)}|{title}]]")

        logger.debug("wiki_index_page_created", page_type=page_type, path=str(page_path))
    except Exception:
        logger.debug("wiki_index_on_page_created_failed", exc_info=True)


def on_page_updated(page_path: Path, page_type: str, frontmatter: dict) -> None:
    """Update existing row in all relevant indexes."""
    try:
        row_fn = _ROW_FORMATTERS.get(page_type)
        if not row_fn:
            return

        row = row_fn(frontmatter, page_path)
        link_text = _link_text_from_path(page_path)

        master_marker = _PAGE_TYPE_TO_MASTER_MARKER.get(page_type)
        if master_marker:
            _upsert_table_row(WIKI_DIR / "index.md", master_marker, link_text, row)

        _update_sub_index(page_type, frontmatter, link_text, row, page_path)

        title = frontmatter.get("title", page_path.stem)
        _append_log(f"Updated {page_type} page: [[{_wiki_link_from_path(page_path)}|{title}]]")

        logger.debug("wiki_index_page_updated", page_type=page_type, path=str(page_path))
    except Exception:
        logger.debug("wiki_index_on_page_updated_failed", exc_info=True)


def on_page_deleted(page_path: Path, page_type: str) -> None:
    """Remove a page from all indexes and log the deletion."""
    try:
        link_text = _link_text_from_path(page_path)

        master_marker = _PAGE_TYPE_TO_MASTER_MARKER.get(page_type)
        if master_marker:
            _remove_table_row(WIKI_DIR / "index.md", master_marker, link_text)

        # Remove from sub-indexes
        sub_index_path = _SUB_INDEX_PATHS.get(page_type)
        if sub_index_path:
            full_path = WIKI_DIR / sub_index_path
            if full_path.exists():
                # For sub-indexes we may have multiple markers, so just search all
                content = full_path.read_text(encoding="utf-8")
                lines = content.split("\n")
                new_lines = [l for l in lines if link_text not in l]
                if len(new_lines) != len(lines):
                    full_path.write_text("\n".join(new_lines), encoding="utf-8")

        _append_log(f"Deleted {page_type} page: {page_path.stem}")

        logger.debug("wiki_index_page_deleted", page_type=page_type, path=str(page_path))
    except Exception:
        logger.debug("wiki_index_on_page_deleted_failed", exc_info=True)


def rebuild_index() -> dict:
    """Scan all wiki pages and rebuild all index tables from scratch.

    Returns dict with counts: {"themes": N, "entities": N, "sources": N, ...}
    """
    counts: dict[str, int] = {}

    # Collect all pages by type
    pages_by_type: dict[str, list[tuple[Path, dict]]] = {}

    for md_file in WIKI_DIR.rglob("*.md"):
        # Skip index files, conventions, log, overview, and .obsidian
        rel = md_file.relative_to(WIKI_DIR)
        if rel.name in _SKIP_FILES:
            continue
        if ".obsidian" in str(rel):
            continue
        # Skip sub-directory index files
        if rel.parent != Path(".") and rel.name == "index.md":
            continue

        try:
            text = md_file.read_text(encoding="utf-8")
            fm, _ = _parse_frontmatter(text)
            if not fm:
                continue
            page_type = fm.get("type", "unknown")
            pages_by_type.setdefault(page_type, []).append((md_file, fm))
        except Exception:
            logger.debug("rebuild_index_skip_file", path=str(md_file), exc_info=True)

    # Clear and rebuild master index
    _rebuild_master_index(pages_by_type)

    # Rebuild sub-indexes
    _rebuild_theme_sub_index(pages_by_type.get("theme", []))
    _rebuild_entity_sub_index(pages_by_type.get("entity", []))
    _rebuild_source_sub_index(pages_by_type.get("source", []))

    for ptype, pages in pages_by_type.items():
        counts[ptype] = len(pages)

    logger.info("wiki_index_rebuilt", counts=counts)
    return counts


# ---------------------------------------------------------------------------
# Row formatters
# ---------------------------------------------------------------------------

def _esc(text: str) -> str:
    """Escape pipe characters for safe use inside markdown table cells."""
    return str(text).replace("|", r"\|")


def _format_theme_row(fm: dict, page_path: Path) -> str:
    link = _wiki_link_from_path(page_path)
    title = _esc(fm.get("title", page_path.stem))
    status = fm.get("status", "active")
    source_count = fm.get("source_count", 0)
    staleness = fm.get("staleness", 0.0)
    updated = fm.get("updated", "")
    return f"| [[{link}|{title}]] | {status} | {source_count} | {staleness:.1f} | {updated} |"


def _format_theme_sub_row(fm: dict, page_path: Path) -> str:
    link = _wiki_link_from_path(page_path)
    title = _esc(fm.get("title", page_path.stem))
    level = fm.get("level", 1)
    source_count = fm.get("source_count", 0)
    velocity = fm.get("velocity", 0.0)
    staleness = fm.get("staleness", 0.0)
    updated = fm.get("updated", "")

    if level == 0:
        child_themes = fm.get("child_themes", [])
        sub_count = len(child_themes) if isinstance(child_themes, list) else 0
        return f"| [[{link}|{title}]] | {sub_count} | {source_count} | {velocity} | {staleness:.1f} | {updated} |"
    else:
        parent = fm.get("parent_theme", "")
        parent_display = f"[[themes/{parent}|{parent}]]" if parent else ""
        return f"| [[{link}|{title}]] | {parent_display} | {source_count} | {velocity} | {staleness:.1f} | {updated} |"


def _format_entity_row(fm: dict, page_path: Path) -> str:
    link = _wiki_link_from_path(page_path)
    title = _esc(fm.get("title", page_path.stem))
    entity_type = fm.get("entity_type", "concept")
    theme_ids = fm.get("theme_ids", [])
    themes_str = ", ".join(
        f"[[themes/{t}|{t}]]" for t in (theme_ids if isinstance(theme_ids, list) else [])
    )
    influence = fm.get("influence_score", 0.0)
    updated = fm.get("updated", "")
    return f"| [[{link}|{title}]] | {entity_type} | {themes_str} | {influence:.2f} | {updated} |"


def _format_entity_sub_row(fm: dict, page_path: Path) -> str:
    link = _wiki_link_from_path(page_path)
    title = _esc(fm.get("title", page_path.stem))
    theme_ids = fm.get("theme_ids", [])
    themes_str = ", ".join(
        f"[[themes/{t}|{t}]]" for t in (theme_ids if isinstance(theme_ids, list) else [])
    )
    source_count = fm.get("source_count", 0)
    influence = fm.get("influence_score", 0.0)
    updated = fm.get("updated", "")
    return f"| [[{link}|{title}]] | {themes_str} | {source_count} | {influence:.2f} | {updated} |"


def _format_source_row(fm: dict, page_path: Path) -> str:
    link = _wiki_link_from_path(page_path)
    title = _esc(fm.get("title", page_path.stem))
    source_type = fm.get("source_type", "")
    theme_ids = fm.get("theme_ids", [])
    themes_str = ", ".join(
        f"[[themes/{t}|{t}]]" for t in (theme_ids if isinstance(theme_ids, list) else [])
    )
    claim_count = fm.get("claim_count", 0)
    updated = fm.get("updated", "")
    return f"| [[{link}|{title}]] | {source_type} | {themes_str} | {claim_count} | {updated} |"


def _format_source_sub_row(fm: dict, page_path: Path) -> str:
    return _format_source_row(fm, page_path)


def _format_synthesis_row(fm: dict, page_path: Path) -> str:
    link = _wiki_link_from_path(page_path)
    title = _esc(fm.get("title", page_path.stem))
    theme_ids = fm.get("theme_ids", [])
    themes_str = ", ".join(
        f"[[themes/{t}|{t}]]" for t in (theme_ids if isinstance(theme_ids, list) else [])
    )
    updated = fm.get("updated", "")
    return f"| [[{link}|{title}]] | {themes_str} | {updated} |"


def _format_belief_row(fm: dict, page_path: Path) -> str:
    link = _wiki_link_from_path(page_path)
    title = _esc(fm.get("title", page_path.stem))
    confidence = fm.get("confidence", 0.0)
    theme_ids = fm.get("theme_ids", [])
    themes_str = ", ".join(
        f"[[themes/{t}|{t}]]" for t in (theme_ids if isinstance(theme_ids, list) else [])
    )
    updated = fm.get("updated", "")
    return f"| [[{link}|{title}]] | {confidence:.2f} | {themes_str} | {updated} |"


def _format_question_row(fm: dict, page_path: Path) -> str:
    link = _wiki_link_from_path(page_path)
    title = _esc(fm.get("title", page_path.stem))
    theme_ids = fm.get("theme_ids", [])
    themes_str = ", ".join(
        f"[[themes/{t}|{t}]]" for t in (theme_ids if isinstance(theme_ids, list) else [])
    )
    updated = fm.get("updated", "")
    return f"| [[{link}|{title}]] | {themes_str} | {updated} |"


_ROW_FORMATTERS = {
    "theme": _format_theme_row,
    "entity": _format_entity_row,
    "source": _format_source_row,
    "synthesis": _format_synthesis_row,
    "belief": _format_belief_row,
    "question": _format_question_row,
}

_PAGE_TYPE_TO_MASTER_MARKER = {
    "theme": "<!-- THEME_TABLE -->",
    "entity": "<!-- ENTITY_TABLE -->",
    "source": "<!-- SOURCE_TABLE -->",
    "synthesis": "<!-- SYNTHESIS_TABLE -->",
    "belief": "<!-- BELIEF_TABLE -->",
    "question": "<!-- QUESTION_TABLE -->",
}

_SUB_INDEX_PATHS = {
    "theme": "themes/index.md",
    "entity": "entities/index.md",
    "source": "sources/index.md",
}


# ---------------------------------------------------------------------------
# Entity type → sub-index marker mapping
# ---------------------------------------------------------------------------

_ENTITY_TYPE_TO_MARKER = {
    "technique": "<!-- ENTITY_TECHNIQUE_TABLE -->",
    "method": "<!-- ENTITY_METHOD_TABLE -->",
    "model": "<!-- ENTITY_MODEL_TABLE -->",
    "company": "<!-- ENTITY_COMPANY_TABLE -->",
    "researcher": "<!-- ENTITY_COMPANY_TABLE -->",  # grouped with companies/orgs
    "dataset": "<!-- ENTITY_BENCHMARK_TABLE -->",
    "benchmark": "<!-- ENTITY_BENCHMARK_TABLE -->",
    "theory": "<!-- ENTITY_THEORY_TABLE -->",
    "metric": "<!-- ENTITY_METRIC_TABLE -->",
    "entity": "<!-- ENTITY_GENERAL_TABLE -->",
    "concept": "<!-- ENTITY_CONCEPT_TABLE -->",
}

_THEME_LEVEL_TO_MARKER = {
    0: "<!-- THEME_L0_TABLE -->",
    1: "<!-- THEME_L1_TABLE -->",
    2: "<!-- THEME_L2_TABLE -->",
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from body. Returns ({}, body) if no frontmatter."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("---", 3)
    if end == -1:
        return {}, text
    import yaml
    try:
        fm = yaml.safe_load(text[3:end]) or {}
    except Exception:
        fm = {}
    body = text[end + 3:].lstrip("\n")
    return fm, body


def _link_text_from_path(page_path: Path) -> str:
    """Extract the wikilink-style reference for matching in index tables.

    e.g. Path(".../wiki/themes/llm-reasoning.md") → "themes/llm-reasoning"
    """
    try:
        rel = page_path.relative_to(WIKI_DIR)
    except ValueError:
        rel = Path(page_path.stem)
    return str(rel.with_suffix("")).replace("\\", "/")


def _wiki_link_from_path(page_path: Path) -> str:
    """Full wikilink target from path, e.g. 'themes/llm-reasoning'."""
    return _link_text_from_path(page_path)


def _upsert_table_row(file_path: Path, marker: str, link_text: str, new_row: str) -> None:
    """Find marker comment in file, then replace or append a table row."""
    if not file_path.exists():
        return

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    marker_idx = None
    for i, line in enumerate(lines):
        if marker in line:
            marker_idx = i
            break

    if marker_idx is None:
        return

    # Find the end of any table header/separator rows and existing data rows
    existing_idx = None
    last_table_row_idx = marker_idx  # Insert point: after last table row (or marker)
    for i in range(marker_idx + 1, len(lines)):
        line = lines[i]
        # Stop at next section heading or marker
        if line.startswith("#") or (line.startswith("<!--") and line != lines[marker_idx]):
            break
        if not line.strip():
            break
        if line.startswith("|"):
            last_table_row_idx = i
            if link_text in line:
                existing_idx = i

    if existing_idx is not None:
        lines[existing_idx] = new_row
    else:
        # Append after last table row (or after marker if no rows yet)
        lines.insert(last_table_row_idx + 1, new_row)

    file_path.write_text("\n".join(lines), encoding="utf-8")


def _remove_table_row(file_path: Path, marker: str, link_text: str) -> None:
    """Remove a row containing link_text from the table after marker."""
    if not file_path.exists():
        return

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    marker_idx = None
    for i, line in enumerate(lines):
        if marker in line:
            marker_idx = i
            break

    if marker_idx is None:
        return

    # Find section boundary (next heading or next marker)
    section_end = len(lines)
    for i in range(marker_idx + 1, len(lines)):
        line = lines[i]
        if line.startswith("#") or (line.startswith("<!--") and line != lines[marker_idx]):
            section_end = i
            break
        if not line.strip():
            section_end = i
            break

    new_lines = []
    for i, line in enumerate(lines):
        if marker_idx < i < section_end and link_text in line:
            continue  # skip this row within the bounded section
        new_lines.append(line)

    if len(new_lines) != len(lines):
        file_path.write_text("\n".join(new_lines), encoding="utf-8")


def _append_log(message: str) -> None:
    """Append an entry to wiki/log.md under today's date heading."""
    log_path = WIKI_DIR / "log.md"
    if not log_path.exists():
        return

    today = date.today().isoformat()
    content = log_path.read_text(encoding="utf-8")
    heading = f"## {today}"

    if heading in content:
        # Append under existing heading
        idx = content.index(heading)
        # Find end of this section (next ## or end of file)
        next_heading = content.find("\n## ", idx + len(heading))
        if next_heading == -1:
            content = content.rstrip() + f"\n- {message}\n"
        else:
            content = content[:next_heading].rstrip() + f"\n- {message}\n" + content[next_heading:]
    else:
        # Add new date heading at the end
        content = content.rstrip() + f"\n\n{heading}\n\n- {message}\n"

    log_path.write_text(content, encoding="utf-8")


def _update_sub_index(
    page_type: str, frontmatter: dict, link_text: str, master_row: str, page_path: Path,
) -> None:
    """Route to the correct sub-index and marker."""
    sub_path_rel = _SUB_INDEX_PATHS.get(page_type)
    if not sub_path_rel:
        return

    sub_path = WIKI_DIR / sub_path_rel
    if not sub_path.exists():
        return

    if page_type == "theme":
        level = frontmatter.get("level", 1)
        marker = _THEME_LEVEL_TO_MARKER.get(level, _THEME_LEVEL_TO_MARKER[1])
        row = _format_theme_sub_row(frontmatter, page_path)
        _upsert_table_row(sub_path, marker, link_text, row)

    elif page_type == "entity":
        entity_type = frontmatter.get("entity_type", "concept")
        marker = _ENTITY_TYPE_TO_MARKER.get(entity_type, "<!-- ENTITY_CONCEPT_TABLE -->")
        row = _format_entity_sub_row(frontmatter, page_path)
        _upsert_table_row(sub_path, marker, link_text, row)

    elif page_type == "source":
        row = _format_source_sub_row(frontmatter, page_path)
        _upsert_table_row(sub_path, "<!-- SOURCE_TABLE -->", link_text, row)


# ---------------------------------------------------------------------------
# Rebuild helpers
# ---------------------------------------------------------------------------

def _rebuild_master_index(pages_by_type: dict[str, list[tuple[Path, dict]]]) -> None:
    """Clear and rebuild all tables in wiki/index.md."""
    index_path = WIKI_DIR / "index.md"
    if not index_path.exists():
        return

    content = index_path.read_text(encoding="utf-8")

    for page_type, marker in _PAGE_TYPE_TO_MASTER_MARKER.items():
        pages = pages_by_type.get(page_type, [])
        row_fn = _ROW_FORMATTERS.get(page_type)
        if not row_fn:
            continue

        rows = [row_fn(fm, path) for path, fm in pages]
        content = _replace_table_after_marker(content, marker, rows)

    index_path.write_text(content, encoding="utf-8")


def _rebuild_theme_sub_index(theme_pages: list[tuple[Path, dict]]) -> None:
    """Rebuild wiki/themes/index.md."""
    sub_path = WIKI_DIR / "themes" / "index.md"
    if not sub_path.exists():
        return

    content = sub_path.read_text(encoding="utf-8")

    by_level: dict[int, list[tuple[Path, dict]]] = {}
    for path, fm in theme_pages:
        level = fm.get("level", 1)
        by_level.setdefault(level, []).append((path, fm))

    for level, marker in _THEME_LEVEL_TO_MARKER.items():
        pages = by_level.get(level, [])
        rows = [_format_theme_sub_row(fm, path) for path, fm in pages]
        content = _replace_table_after_marker(content, marker, rows)

    sub_path.write_text(content, encoding="utf-8")


def _rebuild_entity_sub_index(entity_pages: list[tuple[Path, dict]]) -> None:
    """Rebuild wiki/entities/index.md."""
    sub_path = WIKI_DIR / "entities" / "index.md"
    if not sub_path.exists():
        return

    content = sub_path.read_text(encoding="utf-8")

    # Group by MARKER (not type) since multiple types can share a marker
    # e.g. company+researcher → ENTITY_COMPANY_TABLE
    by_marker: dict[str, list[tuple[Path, dict]]] = {}
    for path, fm in entity_pages:
        etype = fm.get("entity_type", "concept")
        marker = _ENTITY_TYPE_TO_MARKER.get(etype, "<!-- ENTITY_CONCEPT_TABLE -->")
        by_marker.setdefault(marker, []).append((path, fm))

    for marker in dict.fromkeys(_ENTITY_TYPE_TO_MARKER.values()):
        pages = by_marker.get(marker, [])
        rows = [_format_entity_sub_row(fm, path) for path, fm in pages]
        content = _replace_table_after_marker(content, marker, rows)

    sub_path.write_text(content, encoding="utf-8")


def _rebuild_source_sub_index(source_pages: list[tuple[Path, dict]]) -> None:
    """Rebuild wiki/sources/index.md."""
    sub_path = WIKI_DIR / "sources" / "index.md"
    if not sub_path.exists():
        return

    content = sub_path.read_text(encoding="utf-8")
    rows = [_format_source_sub_row(fm, path) for path, fm in source_pages]
    content = _replace_table_after_marker(content, "<!-- SOURCE_TABLE -->", rows)
    sub_path.write_text(content, encoding="utf-8")


def _replace_table_after_marker(content: str, marker: str, rows: list[str]) -> str:
    """Replace all table rows after a marker with new rows.

    Preserves everything before the marker and after the next section/marker.
    """
    if marker not in content:
        return content

    lines = content.split("\n")
    marker_idx = None
    for i, line in enumerate(lines):
        if marker in line:
            marker_idx = i
            break

    if marker_idx is None:
        return content

    # Find end of table: next heading, next marker, or empty line after rows
    end_idx = marker_idx + 1
    for i in range(marker_idx + 1, len(lines)):
        line = lines[i]
        if line.startswith("#") or (line.startswith("<!--") and line.strip() != marker.strip()):
            end_idx = i
            break
        if line.startswith("|"):
            end_idx = i + 1
            continue
        if not line.strip():
            end_idx = i
            break
    else:
        end_idx = len(lines)

    # Rebuild: lines before marker + marker + new rows + lines after table
    new_lines = lines[: marker_idx + 1] + rows + lines[end_idx:]
    return "\n".join(new_lines)
