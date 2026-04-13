"""Wiki-as-context retrieval: pre-compiled wiki pages as primary LLM context.

Reads theme wiki pages, computes staleness at read time, and falls back
to DB assembly via get_theme_state() when pages are stale or missing.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

logger = logging.getLogger(__name__)

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"


@dataclass
class WikiContext:
    """Pre-compiled wiki content for LLM context injection."""
    theme_narratives: dict[str, str] = field(default_factory=dict)   # theme_id → page body
    freshness: dict[str, float] = field(default_factory=dict)        # theme_id → staleness
    fallback_themes: list[str] = field(default_factory=list)         # themes where DB was used
    synthesis_snippets: dict[str, str] = field(default_factory=dict) # slug → page body
    entity_snippets: dict[str, str] = field(default_factory=dict)    # slug → page body
    source_snippets: dict[str, str] = field(default_factory=dict)    # slug → page body
    belief_snippets: dict[str, str] = field(default_factory=dict)    # slug → page body
    question_snippets: dict[str, str] = field(default_factory=dict)  # slug → page body


def gather_wiki_context(
    theme_ids: list[str] | None = None,
    query: str | None = None,
    get_conn_fn=None,
    max_pages: int = 5,
    include_syntheses: bool = False,
    include_entities: bool = False,
    include_sources: bool = False,
    include_beliefs: bool = False,
    include_questions: bool = False,
    source_ids: list[str] | None = None,
    concept_names: list[str] | None = None,
) -> WikiContext:
    """Main entry point: gather wiki-based context for themes.

    Theme-scoped path (theme_ids provided): read wiki pages directly.
    Discovery path (only query): find themes via DB, then read pages.
    If include_syntheses is True, also include synthesis pages whose
    themes overlap with the resolved theme_ids.
    If include_entities is True, include entity pages for concepts
    associated with the resolved themes or explicit concept_names.
    If include_sources is True, include source pages for the given
    source_ids or sources associated with the resolved themes.
    """
    wctx = WikiContext()

    # Discovery path: find theme_ids from query
    if not theme_ids and query:
        try:
            from retrieval.lenses import _find_themes_for_query
            if get_conn_fn is None:
                from reading_app.db import get_conn
                get_conn_fn = get_conn
            theme_ids = _find_themes_for_query(query, get_conn_fn)
        except Exception:
            logger.debug("wiki_context_discovery_failed", exc_info=True)
            return wctx

    if not theme_ids:
        return wctx

    for tid in theme_ids[:max_pages]:
        result = _read_wiki_page(tid)
        if result is None:
            # File missing → full DB fallback
            narrative = _format_theme_state_as_narrative(tid)
            if narrative:
                wctx.theme_narratives[tid] = narrative
                wctx.freshness[tid] = 1.0
                wctx.fallback_themes.append(tid)
            continue

        fm, body = result
        staleness = _compute_staleness(fm)
        wctx.freshness[tid] = staleness

        if staleness < 0.6:
            # Fresh — use wiki body as-is
            wctx.theme_narratives[tid] = body
        elif staleness < 0.8:
            # Moderately stale — supplement with new DB entities
            supplement = _supplement_with_db(tid, body)
            if supplement:
                wctx.theme_narratives[tid] = body + supplement
            else:
                wctx.theme_narratives[tid] = body
        else:
            # Critical staleness — full DB fallback
            narrative = _format_theme_state_as_narrative(tid)
            wctx.theme_narratives[tid] = narrative or body
            wctx.fallback_themes.append(tid)

    # Optionally gather synthesis pages that overlap with resolved themes
    if include_syntheses and theme_ids:
        wctx.synthesis_snippets = _gather_synthesis_pages(theme_ids)

    # Optionally gather entity pages for relevant concepts
    if include_entities and theme_ids:
        wctx.entity_snippets = _gather_entity_pages(
            theme_ids, concept_names=concept_names,
        )

    # Optionally gather source pages
    if include_sources:
        wctx.source_snippets = _gather_source_pages(
            theme_ids or [], source_ids=source_ids,
        )

    # Optionally gather belief pages
    if include_beliefs and theme_ids:
        wctx.belief_snippets = _gather_typed_pages("beliefs", theme_ids)

    # Optionally gather question pages
    if include_questions and theme_ids:
        wctx.question_snippets = _gather_typed_pages("questions", theme_ids)

    return wctx


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_wiki_page(theme_id: str) -> tuple[dict, str] | None:
    """Read wiki/themes/{theme_id}.md → (frontmatter, body) or None."""
    page_path = WIKI_DIR / "themes" / f"{theme_id}.md"
    if not page_path.exists():
        return None
    try:
        text = page_path.read_text(encoding="utf-8")
        from retrieval.wiki_index import _parse_frontmatter
        fm, body = _parse_frontmatter(text)
        return fm, body
    except Exception:
        logger.debug("wiki_read_failed theme_id=%s", theme_id, exc_info=True)
        return None


def _gather_synthesis_pages(theme_ids: list[str], max_pages: int = 5) -> dict[str, str]:
    """Glob syntheses/*.md and return pages whose themes overlap with theme_ids."""
    synth_dir = WIKI_DIR / "syntheses"
    if not synth_dir.is_dir():
        return {}

    theme_set = set(theme_ids)
    results: dict[str, str] = {}

    try:
        from retrieval.wiki_index import _parse_frontmatter

        for page_path in sorted(synth_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True):
            if len(results) >= max_pages:
                break
            try:
                text = page_path.read_text(encoding="utf-8")
                fm, body = _parse_frontmatter(text)
                page_themes = fm.get("themes", [])
                if isinstance(page_themes, str):
                    page_themes = [page_themes]
                if theme_set & set(page_themes):
                    results[page_path.stem] = body
            except Exception:
                continue
    except Exception:
        logger.debug("wiki_synthesis_gather_failed", exc_info=True)

    return results


def _gather_entity_pages(
    theme_ids: list[str],
    concept_names: list[str] | None = None,
    max_pages: int = 5,
) -> dict[str, str]:
    """Gather entity wiki pages that overlap with the given themes or concept names."""
    entity_dir = WIKI_DIR / "entities"
    if not entity_dir.is_dir():
        return {}

    theme_set = set(theme_ids)
    results: dict[str, str] = {}

    try:
        from retrieval.wiki_index import _parse_frontmatter

        # If specific concept names given, try to find their pages directly
        if concept_names:
            from retrieval.wiki_writer import slugify
            for name in concept_names[:max_pages]:
                slug = slugify(name)
                page_path = entity_dir / f"{slug}.md"
                if page_path.exists() and len(results) < max_pages:
                    try:
                        text = page_path.read_text(encoding="utf-8")
                        fm, body = _parse_frontmatter(text)
                        results[page_path.stem] = body
                    except Exception:
                        continue

        # Fill remaining slots from theme-overlapping entities (capped scan)
        if len(results) < max_pages:
            for page_path in sorted(
                entity_dir.glob("*.md"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )[:50]:
                if len(results) >= max_pages:
                    break
                if page_path.stem in results:
                    continue
                try:
                    text = page_path.read_text(encoding="utf-8")
                    fm, body = _parse_frontmatter(text)
                    page_themes = fm.get("theme_ids", [])
                    if isinstance(page_themes, str):
                        page_themes = [page_themes]
                    if theme_set & set(page_themes):
                        results[page_path.stem] = body
                except Exception:
                    continue
    except Exception:
        logger.debug("wiki_entity_gather_failed", exc_info=True)

    return results


def _gather_source_pages(
    theme_ids: list[str],
    source_ids: list[str] | None = None,
    max_pages: int = 5,
) -> dict[str, str]:
    """Gather source wiki pages for specific source_ids or theme-overlapping sources."""
    source_dir = WIKI_DIR / "sources"
    if not source_dir.is_dir():
        return {}

    theme_set = set(theme_ids)
    results: dict[str, str] = {}

    try:
        from retrieval.wiki_index import _parse_frontmatter

        # If specific source_ids given, try to find their pages directly
        if source_ids:
            for sid in source_ids[:max_pages]:
                page_path = source_dir / f"{sid}.md"
                if page_path.exists() and len(results) < max_pages:
                    try:
                        text = page_path.read_text(encoding="utf-8")
                        fm, body = _parse_frontmatter(text)
                        results[sid] = body
                    except Exception:
                        continue

        # Fill remaining slots from theme-overlapping sources (capped scan)
        if len(results) < max_pages and theme_set:
            for page_path in sorted(
                source_dir.glob("*.md"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )[:50]:
                if len(results) >= max_pages:
                    break
                if page_path.stem in results:
                    continue
                try:
                    text = page_path.read_text(encoding="utf-8")
                    fm, body = _parse_frontmatter(text)
                    page_themes = fm.get("theme_ids", [])
                    if isinstance(page_themes, str):
                        page_themes = [page_themes]
                    if theme_set & set(page_themes):
                        results[page_path.stem] = body
                except Exception:
                    continue
    except Exception:
        logger.debug("wiki_source_gather_failed", exc_info=True)

    return results


def _gather_typed_pages(
    subdir: str,
    theme_ids: list[str],
    max_pages: int = 5,
) -> dict[str, str]:
    """Gather wiki pages from a typed subdirectory (beliefs, questions) by theme overlap."""
    page_dir = WIKI_DIR / subdir
    if not page_dir.is_dir():
        return {}

    theme_set = set(theme_ids)
    results: dict[str, str] = {}

    try:
        from retrieval.wiki_index import _parse_frontmatter

        for page_path in sorted(
            page_dir.glob("*.md"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        ):
            if len(results) >= max_pages:
                break
            try:
                text = page_path.read_text(encoding="utf-8")
                fm, body = _parse_frontmatter(text)
                page_themes = fm.get("theme_ids", [])
                if isinstance(page_themes, str):
                    page_themes = [page_themes]
                if theme_set & set(page_themes):
                    results[page_path.stem] = body
            except Exception:
                continue
    except Exception:
        logger.debug("wiki_%s_gather_failed", subdir, exc_info=True)

    return results


def _compute_staleness(fm: dict) -> float:
    """Recompute staleness from frontmatter fields at read time."""
    sources_since = fm.get("sources_since_update", 0)
    if isinstance(sources_since, str):
        try:
            sources_since = int(sources_since)
        except (ValueError, TypeError):
            sources_since = 0

    updated_str = fm.get("updated", fm.get("created", ""))
    days = 999
    if updated_str:
        try:
            updated_str = str(updated_str).strip("'\"")
            updated_date = date.fromisoformat(updated_str)
            days = (date.today() - updated_date).days
        except (ValueError, TypeError):
            pass

    return max(0.0, min(1.0, sources_since * 0.15 + days / 60))


def _format_theme_state_as_narrative(theme_id: str) -> str:
    """DB fallback: assemble wiki-style narrative from get_theme_state()."""
    try:
        from retrieval.landscape import get_theme_state
        state = get_theme_state(theme_id)
    except Exception:
        logger.debug("wiki_db_fallback_failed theme_id=%s", theme_id, exc_info=True)
        return ""

    theme = state.get("theme")
    if not theme:
        return ""

    parts = [f"# {theme.get('name', theme_id)}"]

    parts.append("\n## Current State\n")
    parts.append(theme.get("state_summary") or "No state summary available.")

    caps = state.get("capabilities", [])
    if caps:
        parts.append("\n## Capabilities\n")
        for c in caps[:10]:
            mat = c.get("maturity", "?")
            parts.append(f"- **{c['description']}** *(maturity: {mat})*")

    lims = state.get("limitations", [])
    if lims:
        parts.append("\n## Limitations\n")
        for l in lims[:10]:
            sev = l.get("severity", "?")
            traj = l.get("trajectory", "?")
            parts.append(f"- **{l['description']}** *(severity: {sev}, trajectory: {traj})*")

    bns = state.get("bottlenecks", [])
    if bns:
        parts.append("\n## Bottlenecks\n")
        for b in bns[:10]:
            horizon = b.get("resolution_horizon", "?")
            parts.append(f"- **{b['description']}** *(horizon: {horizon})*")

    bts = state.get("breakthroughs", [])
    if bts:
        parts.append("\n## Breakthroughs\n")
        for b in bts[:5]:
            sig = b.get("significance", "?")
            parts.append(f"- **{b['description']}** *(significance: {sig})*")

    ants = state.get("anticipations", [])
    if ants:
        parts.append("\n## Anticipations\n")
        for a in ants[:5]:
            conf = a.get("confidence", "?")
            parts.append(f"- {a.get('prediction', '?')} *(confidence: {conf})*")

    impls = state.get("cross_theme_implications", [])
    if impls:
        parts.append("\n## Cross-Theme Implications\n")
        for imp in impls[:5]:
            st = imp.get("source_theme", "?")
            tt = imp.get("target_theme", "?")
            parts.append(f"- {st} → {tt}: {imp.get('implication', '?')[:200]}")

    return "\n".join(parts)


def _supplement_with_db(theme_id: str, wiki_body: str) -> str:
    """For 0.6–0.8 staleness: append only DB entities not in wiki body."""
    try:
        from retrieval.landscape import get_theme_state
        state = get_theme_state(theme_id)
    except Exception:
        return ""

    body_lower = wiki_body.lower()
    new_items = []

    for cap in state.get("capabilities", []):
        desc = cap.get("description", "")
        if desc and desc[:40].lower() not in body_lower:
            new_items.append(f"- Cap: {desc} (maturity: {cap.get('maturity', '?')})")

    for lim in state.get("limitations", []):
        desc = lim.get("description", "")
        if desc and desc[:40].lower() not in body_lower:
            new_items.append(f"- Lim: {desc} (severity: {lim.get('severity', '?')})")

    for bn in state.get("bottlenecks", []):
        desc = bn.get("description", "")
        if desc and desc[:40].lower() not in body_lower:
            new_items.append(f"- BN: {desc} (horizon: {bn.get('resolution_horizon', '?')})")

    for bt in state.get("breakthroughs", []):
        desc = bt.get("description", "")
        if desc and desc[:40].lower() not in body_lower:
            new_items.append(f"- BT: {desc} (significance: {bt.get('significance', '?')})")

    if not new_items:
        return ""

    return (
        "\n\n---\n## Recent Updates (not yet integrated into narrative)\n"
        + "\n".join(new_items)
    )


def format_wiki_context_block(
    wctx: WikiContext,
    header: str = "Thematic Context",
    max_chars_per_theme: int | None = None,
) -> str:
    """Format WikiContext as a prompt-ready markdown block."""
    if not wctx.theme_narratives:
        return ""

    parts = [f"## {header}\n"]

    for tid, narrative in wctx.theme_narratives.items():
        # Extract theme name from first heading line
        first_line = ""
        for line in narrative.split("\n"):
            stripped = line.strip()
            if stripped.startswith("# "):
                first_line = stripped.lstrip("# ").strip()
                break
        display_name = first_line or tid

        staleness = wctx.freshness.get(tid, 0.0)
        staleness_tag = f" [freshness: {staleness:.1f}]" if staleness > 0.3 else ""
        fallback_tag = " (DB fallback)" if tid in wctx.fallback_themes else ""

        parts.append(f"### {display_name} ({tid}){staleness_tag}{fallback_tag}\n")

        content = narrative
        if max_chars_per_theme and len(content) > max_chars_per_theme:
            content = content[:max_chars_per_theme] + "\n[...truncated]"
        parts.append(content)
        parts.append("")

    # Synthesis snippets (cross-cutting analytical content)
    if wctx.synthesis_snippets:
        parts.append(f"### Cross-Cutting Syntheses\n")
        for slug, body in wctx.synthesis_snippets.items():
            display = slug.replace("-", " ").replace("_", " ").title()
            content = body
            if max_chars_per_theme and len(content) > max_chars_per_theme:
                content = content[:max_chars_per_theme] + "\n[...truncated]"
            parts.append(f"#### {display}\n")
            parts.append(content)
            parts.append("")

    # Entity snippets (concept-level compiled context)
    if wctx.entity_snippets:
        parts.append(f"### Key Entities\n")
        for slug, body in wctx.entity_snippets.items():
            display = slug.replace("-", " ").replace("_", " ").title()
            content = body
            if max_chars_per_theme and len(content) > max_chars_per_theme:
                content = content[:max_chars_per_theme] + "\n[...truncated]"
            parts.append(f"#### {display}\n")
            parts.append(content)
            parts.append("")

    # Source snippets (per-source compiled summaries)
    if wctx.source_snippets:
        parts.append(f"### Source Summaries\n")
        for slug, body in wctx.source_snippets.items():
            # Extract title from first heading line
            first_line = ""
            for line in body.split("\n"):
                stripped = line.strip()
                if stripped.startswith("# "):
                    first_line = stripped.lstrip("# ").strip()
                    break
            display = first_line or slug[:30]
            content = body
            if max_chars_per_theme and len(content) > max_chars_per_theme:
                content = content[:max_chars_per_theme] + "\n[...truncated]"
            parts.append(f"#### {display}\n")
            parts.append(content)
            parts.append("")

    # Belief snippets (tracked positions with confidence)
    if wctx.belief_snippets:
        parts.append(f"### Tracked Beliefs\n")
        for slug, body in wctx.belief_snippets.items():
            display = slug.replace("-", " ").replace("_", " ").title()
            content = body
            if max_chars_per_theme and len(content) > max_chars_per_theme:
                content = content[:max_chars_per_theme] + "\n[...truncated]"
            parts.append(f"#### {display}\n")
            parts.append(content)
            parts.append("")

    # Question snippets (filed Q&A pairs)
    if wctx.question_snippets:
        parts.append(f"### Prior Questions\n")
        for slug, body in wctx.question_snippets.items():
            display = slug.replace("-", " ").replace("_", " ").title()
            content = body
            if max_chars_per_theme and len(content) > max_chars_per_theme:
                content = content[:max_chars_per_theme] + "\n[...truncated]"
            parts.append(f"#### {display}\n")
            parts.append(content)
            parts.append("")

    return "\n".join(parts)


def extract_section(body: str, section_name: str, max_chars: int = 400) -> str:
    """Extract content under a ## heading from wiki body text."""
    marker = f"## {section_name}"
    idx = body.find(marker)
    if idx == -1:
        return ""

    # Skip the heading line itself
    start = body.find("\n", idx)
    if start == -1:
        return ""
    start += 1

    # Find next ## heading
    next_heading = body.find("\n## ", start)
    if next_heading == -1:
        section_text = body[start:].strip()
    else:
        section_text = body[start:next_heading].strip()

    if len(section_text) > max_chars:
        # Truncate at sentence boundary
        cut = section_text.rfind(". ", 0, max_chars)
        if cut > max_chars // 2:
            section_text = section_text[:cut + 1]
        else:
            section_text = section_text[:max_chars] + "..."

    return section_text
