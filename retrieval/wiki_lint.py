"""Wiki lint — detection engine, auto-fix, and orchestrator.

Checks wiki pages for staleness drift, broken links, missing pages,
coverage gaps, convention violations, and (optionally) contradictions.
Auto-fixes safe issues without resetting staleness counters.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Callable, Literal

import structlog

from retrieval import wiki_index
from retrieval.wiki_writer import (
    WIKI_DIR,
    _parse_frontmatter,
    _patch_frontmatter,
    _read_page,
    _render_frontmatter,
    slugify,
)

logger = structlog.get_logger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
LINT_REPORT_PATH = WIKI_DIR / ".lint_report.md"
LINT_CACHE_PATH = WIKI_DIR / ".lint_cache.json"

THEME_EXPECTED_SECTIONS = [
    "Current State",
    "Capabilities",
    "Limitations",
    "Bottlenecks",
    "Breakthroughs",
    "Anticipations",
    "Cross-Theme Implications",
    "Development Timeline",
]
ENTITY_EXPECTED_SECTIONS = [
    "Overview",
    "Key Findings",
    "Limitations and Open Questions",
    "Relationships",
    "Sources",
]

THEME_REQUIRED_FM = {
    "type", "title", "theme_id", "level", "created", "updated",
    "source_count", "sources_since_update", "update_count",
    "staleness", "status", "tags",
}
ENTITY_REQUIRED_FM = {
    "type", "title", "entity_type", "theme_ids", "created", "updated",
    "source_count", "influence_score", "staleness", "status", "tags",
}
SOURCE_REQUIRED_FM = {
    "type", "title", "source_id", "source_type", "published_at",
    "theme_ids", "created", "updated", "tags",
}

FM_DEFAULTS = {
    "staleness": 0.0,
    "sources_since_update": 0,
    "update_count": 1,
    "velocity": 0.0,
    "tags": [],
    "status": "active",
    "source_count": 0,
}

_CONTENT_DIRS = {"themes", "entities", "sources", "beliefs", "syntheses"}
_SKIP_FILES = {"index.md", "CONVENTIONS.md", "overview.md", "log.md"}

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

Severity = Literal["error", "warning", "info"]
Tier = Literal["auto_fix", "llm_assisted", "flag_review", "report_only"]


@dataclass
class LintIssue:
    check: str
    severity: Severity
    tier: Tier
    page: str
    message: str
    detail: str = ""
    auto_fixable: bool = False


@dataclass
class LintReport:
    issues: list[LintIssue] = field(default_factory=list)
    pages_scanned: int = 0
    checks_run: list[str] = field(default_factory=list)
    fixed: int = 0
    elapsed_ms: int = 0

    @property
    def health_score(self) -> float:
        if self.pages_scanned == 0:
            return 1.0
        errors = sum(1 for i in self.issues if i.severity == "error")
        warnings = sum(1 for i in self.issues if i.severity == "warning")
        error_rate = errors / max(self.pages_scanned, 1)
        warning_rate = warnings / max(self.pages_scanned, 1)
        return max(0.0, min(1.0, 1.0 - error_rate * 5.0 - warning_rate * 2.0))

    def summary_md(self) -> str:
        lines = [
            "# Wiki Lint Report",
            f"Generated: {date.today().isoformat()}",
            "",
            f"Health: {self.health_score:.2f}/1.00 | "
            f"Scanned: {self.pages_scanned} pages | "
            f"Issues: {len(self.issues)} | Fixed: {self.fixed}",
            "",
        ]

        for sev in ("error", "warning", "info"):
            items = [i for i in self.issues if i.severity == sev]
            if not items:
                continue
            lines.append(f"## {sev.title()}s ({len(items)})")
            for it in items:
                lines.append(f"- {it.check}: {it.page} — {it.message}")
            lines.append("")

        fixed_items = [i for i in self.issues if i.auto_fixable and i.tier == "auto_fix"]
        if self.fixed > 0:
            lines.append(f"## Auto-Fixed ({self.fixed})")
            for it in fixed_items:
                lines.append(f"- {it.check}: {it.page} — {it.message}")
            lines.append("")

        # Suggested actions
        auto_fixable = sum(1 for i in self.issues if i.auto_fixable and i.tier == "auto_fix")
        review_needed = sum(1 for i in self.issues if i.tier == "flag_review")
        llm_needed = sum(1 for i in self.issues if i.tier == "llm_assisted")

        lines.append("## Suggested Actions")
        if auto_fixable > self.fixed:
            lines.append(f"- Run /lint fix for {auto_fixable - self.fixed} remaining auto-fixable issues")
        if llm_needed:
            lines.append(f"- Run /lint full for {llm_needed} issues needing LLM analysis")
        if review_needed:
            lines.append(f"- {review_needed} issues need manual review")
        if not (auto_fixable or review_needed or llm_needed):
            lines.append("- No actions needed")
        lines.append("")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Bulk page loader
# ---------------------------------------------------------------------------


def _load_pages(
    page_paths: list[Path] | None = None,
) -> dict[Path, tuple[dict, str]]:
    """Read target pages into memory. Returns {path: (fm, body)}."""
    if page_paths is not None:
        targets = page_paths
    else:
        targets = []
        for subdir_name in _CONTENT_DIRS:
            subdir = WIKI_DIR / subdir_name
            if not subdir.is_dir():
                continue
            for md in subdir.rglob("*.md"):
                if md.name in _SKIP_FILES:
                    continue
                targets.append(md)

    pages: dict[Path, tuple[dict, str]] = {}
    for p in targets:
        try:
            result = _read_page(p)
            if result is not None:
                pages[p] = result
        except Exception:
            logger.debug("lint_page_read_failed", path=str(p), exc_info=True)
    return pages


def _page_type(page_path: Path) -> str | None:
    """Determine page type from directory."""
    rel = page_path.relative_to(WIKI_DIR)
    top = rel.parts[0] if rel.parts else ""
    mapping = {
        "themes": "theme",
        "entities": "entity",
        "sources": "source",
        "beliefs": "belief",
        "syntheses": "synthesis",
    }
    return mapping.get(top)


def _relative_path(page_path: Path) -> str:
    """Get relative path from WIKI_DIR as string."""
    try:
        return str(page_path.relative_to(WIKI_DIR)).replace("\\", "/")
    except ValueError:
        return str(page_path)


# ---------------------------------------------------------------------------
# Detection 1: Staleness
# ---------------------------------------------------------------------------


def check_staleness(pages: dict[Path, tuple[dict, str]]) -> list[LintIssue]:
    """Check theme pages for staleness drift."""
    issues: list[LintIssue] = []

    theme_pages = {
        p: (fm, body) for p, (fm, body) in pages.items()
        if _page_type(p) == "theme"
    }
    if not theme_pages:
        return issues

    # Batch DB query for latest source ingestion per theme
    latest_by_theme: dict[str, datetime] = {}
    try:
        from reading_app.db import get_conn
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT st.theme_id, MAX(s.ingested_at) as latest "
                "FROM sources s JOIN source_themes st ON s.id = st.source_id "
                "GROUP BY st.theme_id"
            ).fetchall()
            for r in rows:
                try:
                    latest_by_theme[r["theme_id"]] = datetime.fromisoformat(str(r["latest"]))
                except (ValueError, TypeError):
                    pass
    except Exception:
        logger.debug("lint_staleness_db_failed", exc_info=True)

    for p, (fm, body) in theme_pages.items():
        rel = _relative_path(p)
        try:
            sources_since = fm.get("sources_since_update", 0) or 0
            updated_str = fm.get("updated", "")
            if not updated_str:
                continue

            updated_date = date.fromisoformat(str(updated_str))
            days = (date.today() - updated_date).days
            computed = min(1.0, sources_since * 0.15 + days / 60)

            fm_staleness = fm.get("staleness", 0.0)
            if isinstance(fm_staleness, str):
                try:
                    fm_staleness = float(fm_staleness)
                except ValueError:
                    fm_staleness = 0.0

            # Check for staleness field drift
            if abs(computed - fm_staleness) > 0.05:
                issues.append(LintIssue(
                    check="staleness_drift",
                    severity="warning",
                    tier="auto_fix",
                    page=rel,
                    message=f"staleness {fm_staleness:.2f} → {computed:.2f}",
                    auto_fixable=True,
                ))

            # High staleness
            if computed > 0.8:
                issues.append(LintIssue(
                    check="stale_page",
                    severity="error",
                    tier="llm_assisted",
                    page=rel,
                    message=f"staleness {computed:.2f}, {sources_since} new sources",
                ))
            elif computed > 0.5:
                issues.append(LintIssue(
                    check="stale_page",
                    severity="warning",
                    tier="report_only",
                    page=rel,
                    message=f"staleness {computed:.2f}",
                ))

            # Cross-check sources_since_update against DB
            theme_id = fm.get("theme_id", "")
            if theme_id in latest_by_theme and sources_since == 0:
                latest_dt = latest_by_theme[theme_id]
                latest_d = latest_dt.date() if isinstance(latest_dt, datetime) else latest_dt
                if latest_d > updated_date:
                    issues.append(LintIssue(
                        check="sources_since_drift",
                        severity="warning",
                        tier="report_only",
                        page=rel,
                        message=f"sources_since_update=0 but sources ingested after {updated_str}",
                    ))
        except Exception:
            logger.debug("lint_staleness_check_failed", page=rel, exc_info=True)

    return issues


# ---------------------------------------------------------------------------
# Detection 2: Link integrity
# ---------------------------------------------------------------------------


def check_link_integrity(pages: dict[Path, tuple[dict, str]]) -> list[LintIssue]:
    """Check for broken wikilinks and orphan pages."""
    issues: list[LintIssue] = []

    # Build page lookup: lowered no-ext path → actual rel path (O(1) lookup)
    path_to_rel: dict[Path, str] = {}
    lower_to_rel: dict[str, str] = {}
    for p in pages:
        rel = _relative_path(p)
        path_to_rel[p] = rel
        rel_no_ext = rel.rsplit(".", 1)[0] if rel.endswith(".md") else rel
        lower_to_rel[rel_no_ext.lower()] = rel

    # Build inbound counts
    inbound: dict[str, int] = {rel: 0 for rel in path_to_rel.values()}

    for p, (fm, body) in pages.items():
        rel = path_to_rel[p]
        for target in WIKILINK_RE.findall(body):
            target = target.strip()
            if target.startswith("http"):
                continue

            matched_rel = lower_to_rel.get(target.lower())
            if matched_rel:
                inbound[matched_rel] += 1
            else:
                issues.append(LintIssue(
                    check="broken_link",
                    severity="error",
                    tier="flag_review",
                    page=rel,
                    message=f"→ [[{target}]]",
                ))

    # Orphan pages (entities/sources with zero inbound)
    for p in pages:
        ptype = _page_type(p)
        if ptype not in ("entity", "source"):
            continue
        rel = path_to_rel[p]
        if inbound.get(rel, 0) == 0:
            issues.append(LintIssue(
                check="orphan_page",
                severity="info" if ptype == "entity" else "warning",
                tier="report_only",
                page=rel,
                message="zero inbound wikilinks",
            ))

    # Missing cross-refs from DB
    try:
        from reading_app.db import get_conn
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT source_theme_id, target_theme_id FROM cross_theme_implications"
            ).fetchall()

        for src_tid, tgt_tid in rows:
            src_slug = slugify(src_tid)
            tgt_slug = slugify(tgt_tid)
            src_path = WIKI_DIR / "themes" / f"{src_slug}.md"
            if src_path not in pages:
                continue
            _, body = pages[src_path]
            if f"themes/{tgt_slug}" not in body.lower() and tgt_tid.lower() not in body.lower():
                rel = _relative_path(src_path)
                issues.append(LintIssue(
                    check="missing_cross_ref",
                    severity="info",
                    tier="auto_fix",
                    page=rel,
                    message=f"missing cross-ref to {tgt_tid}",
                    detail=f"source_theme={src_tid}, target_theme={tgt_tid}",
                    auto_fixable=True,
                ))
    except Exception:
        logger.debug("lint_cross_ref_db_failed", exc_info=True)

    return issues


# ---------------------------------------------------------------------------
# Detection 3: Missing pages
# ---------------------------------------------------------------------------


def check_missing_pages(pages: dict[Path, tuple[dict, str]]) -> list[LintIssue]:
    """Check for concepts with 3+ sources that lack entity pages."""
    issues: list[LintIssue] = []

    all_pages_lower: set[str] = set()
    for p in pages:
        rel = _relative_path(p)
        rel_no_ext = rel.rsplit(".", 1)[0] if rel.endswith(".md") else rel
        all_pages_lower.add(rel_no_ext.lower())

    try:
        from reading_app.db import get_conn
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT c.id, c.canonical_name, COUNT(DISTINCT sc.source_id) as src_count "
                "FROM concepts c "
                "JOIN source_concepts sc ON c.id = sc.concept_id "
                "GROUP BY c.id, c.canonical_name "
                "HAVING COUNT(DISTINCT sc.source_id) >= 3"
            ).fetchall()

        for r in rows:
            concept_id, name, src_count = r["id"], r["canonical_name"], r["src_count"]
            slug = slugify(name)
            expected_path = f"entities/{slug}"
            if expected_path.lower() not in all_pages_lower:
                issues.append(LintIssue(
                    check="missing_page",
                    severity="warning",
                    tier="llm_assisted",
                    page=f"entities/{slug}.md",
                    message=f"concept '{name}' has {src_count} sources but no wiki page",
                    auto_fixable=False,
                ))
    except Exception:
        logger.debug("lint_missing_pages_db_failed", exc_info=True)

    return issues


# ---------------------------------------------------------------------------
# Detection 4: Coverage
# ---------------------------------------------------------------------------


def check_coverage(pages: dict[Path, tuple[dict, str]]) -> list[LintIssue]:
    """Check for missing sections and thin coverage."""
    issues: list[LintIssue] = []

    # Batch query: source count per theme
    theme_source_counts: dict[str, int] = {}
    try:
        from reading_app.db import get_conn
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT theme_id, COUNT(*) FROM source_themes GROUP BY theme_id"
            ).fetchall()
            theme_source_counts = {r["theme_id"]: r["count"] for r in rows}
    except Exception:
        logger.debug("lint_coverage_db_failed", exc_info=True)

    for p, (fm, body) in pages.items():
        ptype = _page_type(p)
        rel = _relative_path(p)

        if ptype == "theme":
            # Check expected sections
            for section in THEME_EXPECTED_SECTIONS:
                if f"## {section}" not in body:
                    issues.append(LintIssue(
                        check="missing_section",
                        severity="warning",
                        tier="auto_fix",
                        page=rel,
                        message=f"missing ## {section}",
                        auto_fixable=True,
                    ))

            # Thin coverage check
            theme_id = fm.get("theme_id", "")
            src_count = theme_source_counts.get(theme_id, 0)
            if src_count >= 5 and len(body) < 500:
                issues.append(LintIssue(
                    check="thin_coverage",
                    severity="warning",
                    tier="llm_assisted",
                    page=rel,
                    message=f"{src_count} sources but body is {len(body)} chars",
                ))

        elif ptype == "entity":
            for section in ENTITY_EXPECTED_SECTIONS:
                if f"## {section}" not in body:
                    issues.append(LintIssue(
                        check="missing_section",
                        severity="info",
                        tier="auto_fix",
                        page=rel,
                        message=f"missing ## {section}",
                        auto_fixable=True,
                    ))

    return issues


# ---------------------------------------------------------------------------
# Detection 5: Conventions
# ---------------------------------------------------------------------------


def check_conventions(pages: dict[Path, tuple[dict, str]]) -> list[LintIssue]:
    """Check frontmatter conventions and required fields."""
    issues: list[LintIssue] = []

    type_to_required = {
        "theme": THEME_REQUIRED_FM,
        "entity": ENTITY_REQUIRED_FM,
        "source": SOURCE_REQUIRED_FM,
    }

    for p, (fm, body) in pages.items():
        ptype = _page_type(p)
        rel = _relative_path(p)

        if ptype not in type_to_required:
            continue

        required = type_to_required[ptype]
        missing = required - set(fm.keys())

        for f_name in missing:
            if f_name in FM_DEFAULTS:
                issues.append(LintIssue(
                    check="convention_violation",
                    severity="warning",
                    tier="auto_fix",
                    page=rel,
                    message=f"missing field '{f_name}' (default available)",
                    detail=f_name,
                    auto_fixable=True,
                ))
            else:
                issues.append(LintIssue(
                    check="convention_violation",
                    severity="error",
                    tier="flag_review",
                    page=rel,
                    message=f"missing required field '{f_name}'",
                ))

        # Type field matches directory
        fm_type = fm.get("type", "")
        if fm_type and fm_type != ptype:
            issues.append(LintIssue(
                check="convention_violation",
                severity="error",
                tier="flag_review",
                page=rel,
                message=f"type field '{fm_type}' doesn't match directory '{ptype}'",
            ))

        # Validate field types
        staleness = fm.get("staleness")
        if staleness is not None and not isinstance(staleness, (int, float)):
            try:
                float(staleness)
            except (ValueError, TypeError):
                issues.append(LintIssue(
                    check="convention_violation",
                    severity="error",
                    tier="flag_review",
                    page=rel,
                    message=f"staleness field is not numeric: {staleness!r}",
                ))

        tags = fm.get("tags")
        if tags is not None and not isinstance(tags, list):
            issues.append(LintIssue(
                check="convention_violation",
                severity="warning",
                tier="auto_fix",
                page=rel,
                message="tags field is not a list",
                detail="tags",
                auto_fixable=True,
            ))

    return issues


# ---------------------------------------------------------------------------
# Detection 6: Contradictions (LLM-based)
# ---------------------------------------------------------------------------


def check_contradictions(
    pages: dict[Path, tuple[dict, str]],
    executor=None,
    max_pairs: int = 5,
) -> list[LintIssue]:
    """LLM-based contradiction detection between theme pairs."""
    issues: list[LintIssue] = []

    if executor is None:
        return issues

    # Load lint cache
    cache: dict = {}
    if LINT_CACHE_PATH.exists():
        try:
            cache = json.loads(LINT_CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            cache = {}

    # Find theme pairs with most cross-references
    pairs: list[tuple[str, str]] = []
    try:
        from reading_app.db import get_conn
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT source_theme_id, target_theme_id, COUNT(*) as cnt "
                "FROM cross_theme_implications "
                "GROUP BY source_theme_id, target_theme_id "
                "ORDER BY cnt DESC "
                f"LIMIT {max_pairs * 2}"
            ).fetchall()

        seen = set()
        for src, tgt, _ in rows:
            pair_key = tuple(sorted([src, tgt]))
            if pair_key not in seen:
                seen.add(pair_key)
                pairs.append(pair_key)
            if len(pairs) >= max_pairs:
                break
    except Exception:
        logger.debug("lint_contradictions_db_failed", exc_info=True)
        return issues

    def _extract_sections(body: str) -> str:
        """Extract Current State + Capabilities + Limitations sections, truncated."""
        result = []
        for section_name in ("Current State", "Capabilities", "Limitations"):
            marker = f"## {section_name}"
            idx = body.find(marker)
            if idx == -1:
                continue
            after = body[idx:]
            next_section = re.search(r"\n## ", after[len(marker):])
            if next_section:
                section_text = after[:len(marker) + next_section.start()]
            else:
                section_text = after
            result.append(section_text[:2000])
        return "\n\n".join(result)

    theme_pages_by_id: dict[str, tuple[Path, dict, str]] = {}
    for p, (fm, body) in pages.items():
        if _page_type(p) == "theme":
            tid = fm.get("theme_id", "")
            if tid:
                theme_pages_by_id[tid] = (p, fm, body)

    for theme_a, theme_b in pairs:
        if theme_a not in theme_pages_by_id or theme_b not in theme_pages_by_id:
            continue

        p_a, fm_a, body_a = theme_pages_by_id[theme_a]
        p_b, fm_b, body_b = theme_pages_by_id[theme_b]

        # Check cache
        pair_hash = f"{theme_a}:{theme_b}"
        cached = cache.get(pair_hash)
        if cached:
            cached_a_updated = cached.get("page_a_updated", "")
            cached_b_updated = cached.get("page_b_updated", "")
            if (cached_a_updated == str(fm_a.get("updated", ""))
                    and cached_b_updated == str(fm_b.get("updated", ""))):
                continue

        sections_a = _extract_sections(body_a)
        sections_b = _extract_sections(body_b)

        if not sections_a or not sections_b:
            continue

        prompt = (
            "Compare these two wiki theme pages for factual contradictions "
            "about the same entities or capabilities.\n\n"
            f"Theme A: {theme_a}\n{sections_a}\n\n"
            f"Theme B: {theme_b}\n{sections_b}\n\n"
            "List any direct contradictions, temporal inconsistencies, "
            "or scope disagreements.\n"
            'Output JSON array: [{"claim_a": "...", "claim_b": "...", '
            '"nature": "direct_contradiction|temporal_inconsistency|scope_disagreement", '
            '"explanation": "..."}]\n'
            "If no contradictions found, output: []"
        )

        try:
            result = executor.run_raw(prompt, model="haiku")
            response = result.text if hasattr(result, "text") else str(result)

            # Parse JSON from response
            json_match = re.search(r"\[.*\]", response, re.DOTALL)
            if json_match:
                contradictions = json.loads(json_match.group())
                for c in contradictions:
                    issues.append(LintIssue(
                        check="contradiction",
                        severity="error",
                        tier="flag_review",
                        page=f"themes/{slugify(theme_a)}.md ↔ themes/{slugify(theme_b)}.md",
                        message=c.get("nature", "contradiction"),
                        detail=c.get("explanation", ""),
                    ))
        except Exception:
            logger.debug("lint_contradiction_llm_failed", pair=pair_hash, exc_info=True)

        # Update cache
        cache[pair_hash] = {
            "checked": date.today().isoformat(),
            "page_a_updated": str(fm_a.get("updated", "")),
            "page_b_updated": str(fm_b.get("updated", "")),
        }

    # Persist cache
    try:
        LINT_CACHE_PATH.write_text(json.dumps(cache, indent=2), encoding="utf-8")
    except Exception:
        logger.debug("lint_cache_write_failed", exc_info=True)

    return issues


# ---------------------------------------------------------------------------
# Auto-fix functions
# ---------------------------------------------------------------------------


def _fix_staleness_drift(page_path: Path, fm: dict) -> bool:
    """Recompute and correct staleness value."""
    sources_since = fm.get("sources_since_update", 0) or 0
    updated_str = fm.get("updated", "")
    if not updated_str:
        return False
    try:
        updated_date = date.fromisoformat(str(updated_str))
    except ValueError:
        return False
    days = (date.today() - updated_date).days
    computed = min(1.0, sources_since * 0.15 + days / 60)
    return _patch_frontmatter(page_path, {"staleness": round(computed, 3)})


def _fix_frontmatter_defaults(page_path: Path, fm: dict, missing_field: str) -> bool:
    """Insert default value for a missing required field."""
    if missing_field not in FM_DEFAULTS:
        return False
    return _patch_frontmatter(page_path, {missing_field: FM_DEFAULTS[missing_field]})


def _fix_missing_sections(page_path: Path, missing_section: str) -> bool:
    """Insert empty section header before Development Timeline or at end."""
    result = _read_page(page_path)
    if result is None:
        return False
    fm, body = result

    header = f"## {missing_section}"
    if header in body:
        return False

    timeline_idx = body.find("## Development Timeline")
    if timeline_idx != -1:
        new_body = (
            body[:timeline_idx].rstrip()
            + f"\n\n{header}\n\n"
            + body[timeline_idx:]
        )
    else:
        new_body = body.rstrip() + f"\n\n{header}\n\n"

    page_path.write_text(
        _render_frontmatter(fm) + "\n" + new_body.strip() + "\n",
        encoding="utf-8",
    )
    return True


def _fix_missing_cross_refs(page_path: Path, source_tid: str, target_tid: str) -> bool:
    """Append cross-reference to Cross-Theme Implications section."""
    result = _read_page(page_path)
    if result is None:
        return False
    fm, body = result

    target_slug = slugify(target_tid)
    entry = f"- → [[themes/{target_slug}|{target_tid}]]: cross-reference detected by lint"

    from retrieval.wiki_writer import _append_to_section
    new_body = _append_to_section(body, "## Cross-Theme Implications", entry, target_slug)
    if new_body == body:
        return False

    page_path.write_text(
        _render_frontmatter(fm) + "\n" + new_body.strip() + "\n",
        encoding="utf-8",
    )
    return True


def _fix_tags_not_list(page_path: Path, fm: dict) -> bool:
    """Convert tags to list if it isn't one."""
    tags = fm.get("tags")
    if isinstance(tags, list):
        return False
    if isinstance(tags, str):
        new_tags = [t.strip() for t in tags.split(",") if t.strip()]
    else:
        new_tags = []
    return _patch_frontmatter(page_path, {"tags": new_tags})


def _apply_auto_fixes(report: LintReport, pages: dict[Path, tuple[dict, str]]) -> int:
    """Apply all auto_fixable issues. Returns count of fixes applied."""
    fixed = 0

    for issue in report.issues:
        if not issue.auto_fixable or issue.tier != "auto_fix":
            continue

        try:
            page_path = WIKI_DIR / issue.page
            if page_path not in pages:
                # Try to find by matching
                for p in pages:
                    if _relative_path(p) == issue.page:
                        page_path = p
                        break

            if page_path not in pages and not page_path.exists():
                continue

            cached = pages.get(page_path)
            fm = cached[0] if cached else None
            if fm is None:
                result = _read_page(page_path)
                if result is None:
                    continue
                fm = result[0]

            success = False
            if issue.check == "staleness_drift":
                success = _fix_staleness_drift(page_path, fm)
            elif issue.check == "convention_violation" and issue.detail == "tags":
                success = _fix_tags_not_list(page_path, fm)
            elif issue.check == "convention_violation" and issue.detail in FM_DEFAULTS:
                success = _fix_frontmatter_defaults(page_path, fm, issue.detail)
            elif issue.check == "missing_section":
                section_name = issue.message.replace("missing ## ", "")
                success = _fix_missing_sections(page_path, section_name)
            elif issue.check == "missing_cross_ref":
                parts = issue.detail.split(", ")
                src_tid = parts[0].split("=")[1] if len(parts) > 0 else ""
                tgt_tid = parts[1].split("=")[1] if len(parts) > 1 else ""
                if src_tid and tgt_tid:
                    success = _fix_missing_cross_refs(page_path, src_tid, tgt_tid)

            if success:
                fixed += 1
        except Exception:
            logger.debug("lint_auto_fix_failed", issue=issue.check, page=issue.page, exc_info=True)

    return fixed


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run_lint(
    mode: Literal["summary", "fix", "full"] = "summary",
    scope: str | None = None,
    executor=None,
    on_progress: Callable[[str], None] | None = None,
    max_pages: int | None = None,
) -> LintReport:
    """Run wiki lint checks.

    Caller must ensure DB pool is initialized.

    Args:
        mode: "summary" (deterministic only), "fix" (+ auto-fix), "full" (+ LLM contradictions)
        scope: theme_id for single-theme focus
        executor: needed for mode="full" (contradiction detection)
        on_progress: optional callback for status updates
        max_pages: limit to N stalest theme pages (for incremental heartbeat runs)
    """
    t0 = time.monotonic()
    report = LintReport()

    def progress(msg: str) -> None:
        if on_progress:
            on_progress(msg)

    # Determine target pages
    progress("Loading pages...")
    page_paths = None

    if scope:
        # Single theme
        theme_slug = slugify(scope)
        theme_path = WIKI_DIR / "themes" / f"{theme_slug}.md"
        if theme_path.exists():
            page_paths = [theme_path]
        else:
            report.elapsed_ms = int((time.monotonic() - t0) * 1000)
            return report

    pages = _load_pages(page_paths)

    if max_pages and not scope:
        # Sort theme pages by staleness descending, take top N
        theme_entries = []
        non_theme_entries = []
        for p, (fm, body) in pages.items():
            if _page_type(p) == "theme":
                staleness = fm.get("staleness", 0.0)
                if isinstance(staleness, str):
                    try:
                        staleness = float(staleness)
                    except ValueError:
                        staleness = 0.0
                theme_entries.append((staleness, p))
            else:
                non_theme_entries.append(p)

        theme_entries.sort(reverse=True)
        selected_paths = [p for _, p in theme_entries[:max_pages]]
        pages = {p: pages[p] for p in selected_paths if p in pages}

    report.pages_scanned = len(pages)

    if not pages:
        report.elapsed_ms = int((time.monotonic() - t0) * 1000)
        return report

    # Run checks cheap → expensive
    progress("Checking conventions...")
    try:
        report.issues.extend(check_conventions(pages))
        report.checks_run.append("conventions")
    except Exception:
        logger.debug("lint_check_conventions_failed", exc_info=True)

    progress("Checking staleness...")
    try:
        report.issues.extend(check_staleness(pages))
        report.checks_run.append("staleness")
    except Exception:
        logger.debug("lint_check_staleness_failed", exc_info=True)

    progress("Checking link integrity...")
    try:
        report.issues.extend(check_link_integrity(pages))
        report.checks_run.append("link_integrity")
    except Exception:
        logger.debug("lint_check_links_failed", exc_info=True)

    progress("Checking missing pages...")
    try:
        report.issues.extend(check_missing_pages(pages))
        report.checks_run.append("missing_pages")
    except Exception:
        logger.debug("lint_check_missing_failed", exc_info=True)

    progress("Checking coverage...")
    try:
        report.issues.extend(check_coverage(pages))
        report.checks_run.append("coverage")
    except Exception:
        logger.debug("lint_check_coverage_failed", exc_info=True)

    if mode == "full" and executor:
        progress("Checking contradictions (LLM)...")
        try:
            report.issues.extend(check_contradictions(pages, executor))
            report.checks_run.append("contradictions")
        except Exception:
            logger.debug("lint_check_contradictions_failed", exc_info=True)

    if mode in ("fix", "full"):
        progress("Applying auto-fixes...")
        report.fixed = _apply_auto_fixes(report, pages)

    report.elapsed_ms = int((time.monotonic() - t0) * 1000)

    # Persist report
    try:
        write_lint_report_md(report)
    except Exception:
        logger.debug("lint_report_write_failed", exc_info=True)

    return report


def run_lint_incremental(on_progress: Callable[[str], None] | None = None) -> LintReport:
    """Heartbeat-oriented: top 10 stalest pages, deterministic checks + auto-fix."""
    return run_lint(mode="fix", max_pages=10, on_progress=on_progress)


# ---------------------------------------------------------------------------
# Report persistence
# ---------------------------------------------------------------------------


def write_lint_report_md(report: LintReport) -> None:
    """Write human/LLM-readable report to wiki/.lint_report.md."""
    LINT_REPORT_PATH.write_text(report.summary_md(), encoding="utf-8")


# ---------------------------------------------------------------------------
# Wiki-wide link repair
# ---------------------------------------------------------------------------


def repair_broken_links(
    dry_run: bool = True,
    on_progress: Callable[[str], None] | None = None,
    *,
    strip_unresolvable: bool = True,
) -> dict:
    """Scan all wiki pages for broken wikilinks and replace with canonical targets.

    Uses the cached wiki target lookup from wiki_writer, then regex-replaces
    broken links with the nearest match (by source_id prefix or slug similarity).
    Unresolvable links (no matching wiki page) are converted to plain text
    when strip_unresolvable is True (default).

    Args:
        dry_run: If True, report changes without writing. If False, apply fixes.
        on_progress: Optional progress callback.
        strip_unresolvable: If True, convert unresolvable wikilinks to plain text.
            If False, only normalize links that have a canonical match.

    Returns:
        Dict with keys: pages_scanned, links_checked, links_fixed,
        links_stripped, details.
    """
    from retrieval.wiki_writer import _normalize_wikilinks, _build_wiki_target_lookup

    stats = {
        "pages_scanned": 0,
        "links_checked": 0,
        "links_fixed": 0,
        "links_stripped": 0,
        "details": [],
    }

    # Prime the lookup cache once (reused by all _normalize_wikilinks calls)
    canonical = _build_wiki_target_lookup()
    if on_progress:
        on_progress(f"Built canonical lookup with {len(canonical)} targets")

    pages = _load_pages()
    stats["pages_scanned"] = len(pages)

    for page_path, (fm, body) in pages.items():
        rel = _relative_path(page_path)

        old_links = set(WIKILINK_RE.findall(body))
        stats["links_checked"] += len(old_links)

        new_body = _normalize_wikilinks(body, strip_unresolvable=strip_unresolvable)

        if new_body != body:
            new_links = set(WIKILINK_RE.findall(new_body))
            normalized = old_links - new_links
            # Links that were in old but not in new AND still appear as
            # wikilinks in new_body were normalized; those that disappeared
            # entirely were stripped to plain text
            stripped = len([l for l in normalized if f"[[{l}" not in new_body])
            fixed = len(normalized) - stripped
            stats["links_fixed"] += fixed
            stats["links_stripped"] += stripped
            stats["details"].append(
                f"{rel}: {fixed} normalized, {stripped} stripped"
            )

            if not dry_run:
                content = _render_frontmatter(fm) + "\n" + new_body.strip() + "\n"
                page_path.write_text(content, encoding="utf-8")

    if on_progress:
        mode = "dry run" if dry_run else "applied"
        on_progress(
            f"Link repair {mode}: {stats['links_fixed']} normalized, "
            f"{stats['links_stripped']} stripped across {stats['pages_scanned']} pages"
        )

    return stats
