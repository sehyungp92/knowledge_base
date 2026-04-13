"""Wiki migration operations for theme taxonomy changes.

Handles wiki-side effects of theme creation, renaming, splitting, merging,
and reparenting. Called from /themes approve and taxonomy evolution tools.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import structlog

from retrieval import wiki_index

logger = structlog.get_logger(__name__)

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"


# ---------------------------------------------------------------------------
# Public dispatch — single entry point for the themes skill
# ---------------------------------------------------------------------------


def execute_wiki_migration(proposal: dict, executor) -> dict:
    """Execute wiki migration for an approved taxonomy evolution proposal.

    Args:
        proposal: Proposal row dict with: change_type, target_theme_id, proposed_changes
        executor: ClaudeExecutor instance (for split/merge LLM calls).

    Returns:
        {change_type, pages_created, pages_deleted, errors}
    """
    change_type = proposal["change_type"]
    target_theme_id = proposal["target_theme_id"]
    changes = proposal["proposed_changes"]
    if isinstance(changes, str):
        changes = json.loads(changes)

    result = {
        "change_type": change_type,
        "pages_created": 0,
        "pages_deleted": 0,
        "errors": [],
    }

    try:
        if change_type in ("new_l1", "new_l2"):
            _dispatch_new(changes, executor, result)
        elif change_type == "rename":
            migrate_theme_rename(target_theme_id, changes)
        elif change_type == "reparent":
            migrate_theme_reparent(target_theme_id, changes["new_parent_id"])
        elif change_type == "split_l2":
            paths = migrate_theme_split(
                target_theme_id,
                changes["new_themes"],
                changes.get("parent_id"),
                executor,
            )
            result["pages_created"] = len(paths)
            result["pages_deleted"] = 1 if paths else 0
        elif change_type == "merge_l2":
            path = migrate_theme_merge(
                [target_theme_id],
                changes["merge_into"],
                executor,
            )
            if path:
                result["pages_deleted"] = 1
        else:
            result["errors"].append(f"Unknown change_type: {change_type}")

    except Exception as exc:
        logger.debug("wiki_migration_dispatch_failed", change_type=change_type, exc_info=True)
        result["errors"].append(str(exc))

    return result


def _dispatch_new(changes: dict, executor, result: dict) -> None:
    """Handle new_l1 / new_l2 wiki migration."""
    from reading_app.db import get_conn
    from retrieval.landscape import get_theme_state

    theme_id = changes["id"]
    theme_data = get_theme_state(theme_id)
    with get_conn() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS cnt FROM source_themes WHERE theme_id = %s",
            (theme_id,),
        ).fetchone()
        theme_data["source_count"] = row["cnt"] if row else 0

        parent_row = conn.execute(
            "SELECT parent_id FROM theme_edges WHERE child_id = %s AND relationship = 'contains' LIMIT 1",
            (theme_id,),
        ).fetchone()
        parent_id = parent_row["parent_id"] if parent_row else changes.get("parent_id", changes.get("suggested_l0_parent", ""))
        theme_data["theme_edges"] = {"parent_id": parent_id, "child_ids": []}

    path = migrate_theme_new(theme_id, theme_data, executor)
    if path:
        result["pages_created"] = 1


# ---------------------------------------------------------------------------
# Public migration operations
# ---------------------------------------------------------------------------


def migrate_theme_new(theme_id: str, theme_data: dict, executor) -> Path | None:
    """Create a wiki page for a newly approved theme and update its parent.

    Args:
        theme_id: The new theme's identifier.
        theme_data: Dict with theme info (from get_theme_state or constructed).
            Must include theme_edges.parent_id for parent page update.
        executor: ClaudeExecutor instance.

    Returns:
        Path to created page, or None on failure.
    """
    try:
        from retrieval.wiki_writer import create_theme_page

        path = create_theme_page(theme_id, theme_data, executor, model="sonnet")
        if path:
            parent_id = (theme_data.get("theme_edges") or {}).get("parent_id", "")
            if parent_id:
                _update_parent_page(parent_id, theme_id)
        return path
    except Exception:
        logger.debug("wiki_migrate_theme_new_failed", theme_id=theme_id, exc_info=True)
        return None


def migrate_theme_rename(theme_id: str, changes: dict) -> None:
    """Update a theme page's title and/or description in-place.

    DB rename only changes name/description, never the ID. So the file stays
    at the same path — we just update frontmatter fields and wikilink display text.

    Args:
        theme_id: Theme identifier (unchanged).
        changes: Dict with optional 'new_name' and/or 'new_description'.
    """
    try:
        from retrieval.wiki_writer import _parse_frontmatter, _render_frontmatter

        page_path = WIKI_DIR / "themes" / f"{theme_id}.md"
        if not page_path.exists():
            logger.warning("wiki_migrate_rename_source_missing", theme_id=theme_id)
            return

        text = page_path.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(text)

        new_name = changes.get("new_name")
        new_desc = changes.get("new_description")

        if new_name:
            fm["title"] = new_name
        if new_desc:
            fm["description"] = new_desc

        page_path.write_text(_render_frontmatter(fm) + "\n" + body, encoding="utf-8")

        # Update wikilink display text across wiki (link target unchanged)
        if new_name:
            _replace_wikilinks_across_wiki(
                f"themes/{theme_id}", f"themes/{theme_id}", new_name
            )

        wiki_index.on_page_updated(page_path, "theme", fm)
        logger.info("wiki_migrate_theme_renamed", theme_id=theme_id)

    except Exception:
        logger.debug("wiki_migrate_rename_failed", theme_id=theme_id, exc_info=True)


def migrate_theme_split(
    old_theme_id: str,
    new_themes: list[dict],
    parent_id: str | None,
    executor,
) -> list[Path]:
    """Split a theme page into multiple new theme pages.

    Uses LLM (Sonnet) to distribute content across new pages, writing the
    LLM output directly (not discarding it via create_theme_page).

    Args:
        old_theme_id: Theme being split.
        new_themes: List of dicts with 'id' and 'name' for each new theme.
        parent_id: Parent theme ID for the new themes.
        executor: ClaudeExecutor instance.

    Returns:
        List of paths to created pages.
    """
    created = []
    session_id = f"wiki_split_{old_theme_id}"

    try:
        from reading_app.db import get_conn
        from retrieval.landscape import get_theme_state
        from retrieval.wiki_writer import (
            _parse_frontmatter,
            _render_frontmatter,
            _strip_llm_frontmatter,
        )

        old_path = WIKI_DIR / "themes" / f"{old_theme_id}.md"
        if not old_path.exists():
            logger.warning("wiki_migrate_split_source_missing", old_theme_id=old_theme_id)
            return created

        old_text = old_path.read_text(encoding="utf-8")
        _, old_body = _parse_frontmatter(old_text)

        new_ids = [t["id"] for t in new_themes]
        new_names = [t["name"] for t in new_themes]
        theme_list_str = ", ".join(f"'{t['name']}' ({t['id']})" for t in new_themes)

        for i, new_theme in enumerate(new_themes):
            new_id = new_theme["id"]
            new_name = new_theme["name"]
            child_session = f"{session_id}_{new_id}"

            prompt = (
                f"You are splitting the theme '{old_theme_id}' into {len(new_themes)} new themes: {theme_list_str}.\n"
                f"Extract content for '{new_name}' ({new_id}). Include all relevant sections, "
                f"timeline entries, landscape data. Do NOT include frontmatter.\n\n"
                f"Original page content:\n```\n{old_body}\n```\n\n"
                f"Follow the standard theme page structure. Use Obsidian wikilinks."
            )

            result = executor.run_raw(
                prompt,
                session_id=child_session,
                model="sonnet",
                timeout=120,
            )

            if result and result.text and len(result.text) > 50:
                try:
                    body = _strip_llm_frontmatter(result.text)

                    # Build frontmatter from DB state
                    theme_data = get_theme_state(new_id)
                    with get_conn() as conn:
                        row = conn.execute(
                            "SELECT COUNT(*) AS cnt FROM source_themes WHERE theme_id = %s",
                            (new_id,),
                        ).fetchone()
                        source_count = row["cnt"] if row else 0

                    theme_info = theme_data.get("theme", {})
                    from datetime import date as _date
                    from retrieval.wiki_lint import FM_DEFAULTS
                    fm = {
                        "type": "theme",
                        "theme_id": new_id,
                        "title": new_name,
                        "level": theme_info.get("level", 2),
                        "description": new_theme.get("description", theme_info.get("description", "")),
                        "parent_theme": parent_id or "",
                        "child_themes": [],
                        "created": _date.today().isoformat(),
                        "updated": _date.today().isoformat(),
                        "source_count": source_count,
                        "sources_since_update": FM_DEFAULTS["sources_since_update"],
                        "update_count": FM_DEFAULTS["update_count"],
                        "velocity": theme_info.get("velocity", FM_DEFAULTS["velocity"]),
                        "staleness": FM_DEFAULTS["staleness"],
                        "status": FM_DEFAULTS["status"],
                        "tags": FM_DEFAULTS["tags"].copy(),
                    }

                    page_path = WIKI_DIR / "themes" / f"{new_id}.md"
                    page_path.parent.mkdir(parents=True, exist_ok=True)
                    page_path.write_text(
                        _render_frontmatter(fm) + "\n" + body + "\n",
                        encoding="utf-8",
                    )
                    wiki_index.on_page_created(page_path, "theme", fm)
                    created.append(page_path)

                except Exception:
                    logger.debug("wiki_split_create_failed", new_id=new_id, exc_info=True)

            try:
                executor.cleanup_session(child_session)
            except Exception:
                pass

        # Delete old page
        if created:
            old_path.unlink(missing_ok=True)
            wiki_index.on_page_deleted(old_path, "theme")

            # Update source/entity frontmatter: DB assigns all sources to new_ids[0]
            _update_frontmatter_theme_refs(old_theme_id, new_ids[0])

            # Redirect all wikilinks to first child (matches DB assignment)
            _replace_wikilinks_across_wiki(
                f"themes/{old_theme_id}",
                f"themes/{new_ids[0]}",
                new_names[0],
            )

            # Update parent page: remove old_id, add all new_ids
            if parent_id:
                _update_split_parent(parent_id, old_theme_id, new_ids)

            wiki_index.rebuild_index()

        logger.info(
            "wiki_migrate_split_complete",
            old=old_theme_id,
            new=new_ids,
            created=len(created),
        )

    except Exception:
        logger.debug("wiki_migrate_split_failed", old_theme_id=old_theme_id, exc_info=True)

    return created


def migrate_theme_merge(
    theme_ids: list[str],
    target_theme_id: str,
    executor,
) -> Path | None:
    """Merge theme pages into one target (surviving) page.

    Uses LLM (Sonnet) to merge and deduplicate content, writing it directly
    to the surviving page.

    Args:
        theme_ids: Theme IDs being consumed/deleted.
        target_theme_id: Surviving theme to merge into.
        executor: ClaudeExecutor instance.

    Returns:
        Path to merged page, or None on failure.
    """
    session_id = f"wiki_merge_{target_theme_id}"

    try:
        from reading_app.db import get_conn
        from retrieval.landscape import get_theme_state
        from retrieval.wiki_writer import (
            _parse_frontmatter,
            _render_frontmatter,
            _strip_llm_frontmatter,
        )

        # Collect all page bodies (consumed + survivor)
        all_ids = list(theme_ids) + ([target_theme_id] if target_theme_id not in theme_ids else [])
        bodies = {}
        for tid in all_ids:
            path = WIKI_DIR / "themes" / f"{tid}.md"
            if path.exists():
                text = path.read_text(encoding="utf-8")
                _, body = _parse_frontmatter(text)
                bodies[tid] = body

        if not bodies:
            logger.warning("wiki_migrate_merge_no_source_pages", theme_ids=theme_ids)
            return None

        # Build merge prompt — full bodies, no truncation
        sources_text = "\n\n---\n\n".join(
            f"# Content from theme: {tid}\n\n{body}" for tid, body in bodies.items()
        )

        prompt = (
            f"Merge the following theme pages into a single page for theme '{target_theme_id}'.\n"
            f"Deduplicate overlapping information. Preserve all unique data points.\n"
            f"Combine Development Timeline entries in chronological order.\n"
            f"Follow the standard theme page structure. Use Obsidian wikilinks.\n"
            f"Do NOT include frontmatter.\n\n"
            f"{sources_text}"
        )

        result = executor.run_raw(
            prompt,
            session_id=session_id,
            model="sonnet",
            timeout=180,
        )

        if not result or not result.text or len(result.text) < 50:
            return None

        body = _strip_llm_frontmatter(result.text)

        # Build frontmatter for surviving theme from DB
        theme_data = get_theme_state(target_theme_id)
        with get_conn() as conn:
            row = conn.execute(
                "SELECT COUNT(*) AS cnt FROM source_themes WHERE theme_id = %s",
                (target_theme_id,),
            ).fetchone()
            source_count = row["cnt"] if row else 0

            parent_row = conn.execute(
                "SELECT parent_id FROM theme_edges WHERE child_id = %s AND relationship = 'contains' LIMIT 1",
                (target_theme_id,),
            ).fetchone()
            parent_id = parent_row["parent_id"] if parent_row else ""

            child_rows = conn.execute(
                "SELECT child_id FROM theme_edges WHERE parent_id = %s AND relationship = 'contains'",
                (target_theme_id,),
            ).fetchall()
            child_ids = [r["child_id"] for r in child_rows]

        theme_info = theme_data.get("theme", {})
        from datetime import date as _date
        from retrieval.wiki_lint import FM_DEFAULTS
        fm = {
            "type": "theme",
            "theme_id": target_theme_id,
            "title": theme_info.get("name", target_theme_id),
            "level": theme_info.get("level", 2),
            "description": theme_info.get("description", ""),
            "parent_theme": parent_id,
            "child_themes": child_ids,
            "created": _date.today().isoformat(),
            "updated": _date.today().isoformat(),
            "source_count": source_count,
            "sources_since_update": FM_DEFAULTS["sources_since_update"],
            "update_count": FM_DEFAULTS["update_count"],
            "velocity": theme_info.get("velocity", FM_DEFAULTS["velocity"]),
            "staleness": FM_DEFAULTS["staleness"],
            "status": FM_DEFAULTS["status"],
            "tags": FM_DEFAULTS["tags"].copy(),
        }

        target_path = WIKI_DIR / "themes" / f"{target_theme_id}.md"
        target_path.write_text(
            _render_frontmatter(fm) + "\n" + body + "\n",
            encoding="utf-8",
        )
        wiki_index.on_page_updated(target_path, "theme", fm)

        # Delete consumed pages and redirect their references
        for tid in theme_ids:
            if tid != target_theme_id:
                old_path = WIKI_DIR / "themes" / f"{tid}.md"
                if old_path.exists():
                    old_path.unlink()
                    wiki_index.on_page_deleted(old_path, "theme")

                # Update source/entity frontmatter
                _update_frontmatter_theme_refs(tid, target_theme_id)

                # Redirect wikilinks
                _replace_wikilinks_across_wiki(
                    f"themes/{tid}",
                    f"themes/{target_theme_id}",
                    fm["title"],
                )

        # Update parent page: remove consumed theme IDs
        if parent_id:
            _remove_children_from_parent(parent_id, [t for t in theme_ids if t != target_theme_id])

        wiki_index.rebuild_index()
        logger.info("wiki_migrate_merge_complete", target=target_theme_id, merged=theme_ids)
        return target_path

    except Exception:
        logger.debug("wiki_migrate_merge_failed", target=target_theme_id, exc_info=True)
        return None
    finally:
        try:
            executor.cleanup_session(session_id)
        except Exception:
            pass


def migrate_theme_reparent(theme_id: str, new_parent_id: str) -> None:
    """Update parent/child relationships in wiki frontmatter and body text.

    Args:
        theme_id: Theme being reparented.
        new_parent_id: New parent theme identifier.
    """
    try:
        from retrieval.wiki_writer import _parse_frontmatter, _render_frontmatter

        page_path = WIKI_DIR / "themes" / f"{theme_id}.md"
        if not page_path.exists():
            return

        # Update this page's parent in frontmatter
        text = page_path.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(text)
        old_parent = fm.get("parent_theme", "")
        fm["parent_theme"] = new_parent_id
        page_path.write_text(_render_frontmatter(fm) + "\n" + body, encoding="utf-8")

        # Update new parent's child_themes
        new_parent_path = WIKI_DIR / "themes" / f"{new_parent_id}.md"
        if new_parent_path.exists():
            text = new_parent_path.read_text(encoding="utf-8")
            fm_p, body_p = _parse_frontmatter(text)
            children = fm_p.get("child_themes", [])
            if isinstance(children, list) and theme_id not in children:
                children.append(theme_id)
                fm_p["child_themes"] = children
                new_parent_path.write_text(
                    _render_frontmatter(fm_p) + "\n" + body_p, encoding="utf-8"
                )

        # Remove from old parent's child_themes
        if old_parent:
            old_parent_path = WIKI_DIR / "themes" / f"{old_parent}.md"
            if old_parent_path.exists():
                text = old_parent_path.read_text(encoding="utf-8")
                fm_o, body_o = _parse_frontmatter(text)
                children = fm_o.get("child_themes", [])
                if isinstance(children, list) and theme_id in children:
                    children.remove(theme_id)
                    fm_o["child_themes"] = children
                    old_parent_path.write_text(
                        _render_frontmatter(fm_o) + "\n" + body_o, encoding="utf-8"
                    )

        # Update body hierarchy lines on all three affected pages
        _update_body_hierarchy_links(page_path)
        if new_parent_path.exists():
            _update_body_hierarchy_links(new_parent_path)
        if old_parent and old_parent_path.exists():
            _update_body_hierarchy_links(old_parent_path)

        wiki_index.rebuild_index()
        logger.info(
            "wiki_migrate_reparent_complete",
            theme_id=theme_id,
            new_parent=new_parent_id,
        )

    except Exception:
        logger.debug("wiki_migrate_reparent_failed", theme_id=theme_id, exc_info=True)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _update_frontmatter_theme_refs(old_id: str, new_id: str) -> int:
    """Replace old_id with new_id in theme_ids frontmatter across source/entity pages.

    Returns number of pages updated.
    """
    updated = 0
    try:
        from retrieval.wiki_writer import _parse_frontmatter, _render_frontmatter

        for subdir in ("sources", "entities"):
            dir_path = WIKI_DIR / subdir
            if not dir_path.exists():
                continue
            for md_file in dir_path.iterdir():
                if not md_file.name.endswith(".md"):
                    continue
                try:
                    text = md_file.read_text(encoding="utf-8")
                    fm, body = _parse_frontmatter(text)
                    theme_ids = fm.get("theme_ids", [])
                    if not isinstance(theme_ids, list) or old_id not in theme_ids:
                        continue

                    # Replace old_id with new_id, deduplicate
                    new_list = []
                    for tid in theme_ids:
                        replacement = new_id if tid == old_id else tid
                        if replacement not in new_list:
                            new_list.append(replacement)
                    fm["theme_ids"] = new_list
                    md_file.write_text(
                        _render_frontmatter(fm) + "\n" + body, encoding="utf-8"
                    )
                    updated += 1
                except Exception:
                    continue

    except Exception:
        logger.debug("wiki_update_frontmatter_refs_failed", old_id=old_id, exc_info=True)

    logger.info("wiki_frontmatter_refs_updated", old_id=old_id, new_id=new_id, count=updated)
    return updated


def _update_body_hierarchy_links(page_path: Path) -> None:
    """Reconstruct **Parent:** and **Sub-themes:** body lines from frontmatter.

    Reads the page's own frontmatter to get parent_theme and child_themes,
    looks up display names, then replaces the corresponding lines in the body.
    """
    try:
        from retrieval.wiki_writer import _parse_frontmatter, _render_frontmatter

        text = page_path.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(text)

        # Build Parent line
        parent_id = fm.get("parent_theme", "")
        if parent_id:
            parent_title = _get_theme_title(parent_id)
            parent_line = f"**Parent:** [[themes/{parent_id}|{parent_title}]]"
        else:
            parent_line = ""

        # Build Sub-themes line
        child_ids = fm.get("child_themes", [])
        if isinstance(child_ids, list) and child_ids:
            child_links = []
            for cid in child_ids:
                ctitle = _get_theme_title(cid)
                child_links.append(f"[[themes/{cid}|{ctitle}]]")
            subthemes_line = "**Sub-themes:** " + ", ".join(child_links)
        else:
            subthemes_line = ""

        # Replace existing lines in body
        new_body = _replace_hierarchy_line(body, r"\*\*Parent:\*\*.*", parent_line)
        new_body = _replace_hierarchy_line(new_body, r"\*\*Sub-themes:\*\*.*", subthemes_line)

        if new_body != body:
            page_path.write_text(
                _render_frontmatter(fm) + "\n" + new_body, encoding="utf-8"
            )

    except Exception:
        logger.debug("wiki_update_body_hierarchy_failed", path=str(page_path), exc_info=True)


def _replace_hierarchy_line(body: str, pattern: str, replacement: str) -> str:
    """Replace a hierarchy line in the body, or append if not found."""
    if re.search(pattern, body):
        if replacement:
            return re.sub(pattern, replacement, body, count=1)
        else:
            # Remove the line entirely (including trailing newline)
            return re.sub(pattern + r"\n?", "", body, count=1)
    elif replacement:
        # Insert after the first heading line
        lines = body.split("\n")
        insert_idx = 1  # Default: after first line
        for idx, line in enumerate(lines):
            if line.startswith("# "):
                insert_idx = idx + 1
                break
        lines.insert(insert_idx, replacement)
        return "\n".join(lines)
    return body


def _update_parent_page(parent_id: str, child_id: str) -> None:
    """Add a child to parent page's child_themes frontmatter and update body."""
    try:
        from retrieval.wiki_writer import _parse_frontmatter, _render_frontmatter

        parent_path = WIKI_DIR / "themes" / f"{parent_id}.md"
        if not parent_path.exists():
            return

        text = parent_path.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(text)

        children = fm.get("child_themes", [])
        if not isinstance(children, list):
            children = []
        if child_id not in children:
            children.append(child_id)
            fm["child_themes"] = children
            parent_path.write_text(
                _render_frontmatter(fm) + "\n" + body, encoding="utf-8"
            )

        _update_body_hierarchy_links(parent_path)

    except Exception:
        logger.debug("wiki_update_parent_failed", parent_id=parent_id, exc_info=True)


def _update_split_parent(
    parent_id: str, old_child_id: str, new_child_ids: list[str]
) -> None:
    """Update parent page after a split: remove old child, add new children."""
    try:
        from retrieval.wiki_writer import _parse_frontmatter, _render_frontmatter

        parent_path = WIKI_DIR / "themes" / f"{parent_id}.md"
        if not parent_path.exists():
            return

        text = parent_path.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(text)

        children = fm.get("child_themes", [])
        if not isinstance(children, list):
            children = []

        # Remove old, add new
        if old_child_id in children:
            children.remove(old_child_id)
        for nid in new_child_ids:
            if nid not in children:
                children.append(nid)
        fm["child_themes"] = children

        parent_path.write_text(
            _render_frontmatter(fm) + "\n" + body, encoding="utf-8"
        )
        _update_body_hierarchy_links(parent_path)

    except Exception:
        logger.debug("wiki_update_split_parent_failed", parent_id=parent_id, exc_info=True)


def _remove_children_from_parent(parent_id: str, child_ids_to_remove: list[str]) -> None:
    """Remove child IDs from parent page's child_themes frontmatter."""
    try:
        from retrieval.wiki_writer import _parse_frontmatter, _render_frontmatter

        parent_path = WIKI_DIR / "themes" / f"{parent_id}.md"
        if not parent_path.exists():
            return

        text = parent_path.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(text)

        children = fm.get("child_themes", [])
        if not isinstance(children, list):
            return

        changed = False
        for cid in child_ids_to_remove:
            if cid in children:
                children.remove(cid)
                changed = True

        if changed:
            fm["child_themes"] = children
            parent_path.write_text(
                _render_frontmatter(fm) + "\n" + body, encoding="utf-8"
            )
            _update_body_hierarchy_links(parent_path)

    except Exception:
        logger.debug(
            "wiki_remove_children_from_parent_failed",
            parent_id=parent_id,
            exc_info=True,
        )


def _get_theme_title(theme_id: str) -> str:
    """Look up a theme's display title from its wiki page frontmatter."""
    try:
        from retrieval.wiki_writer import _parse_frontmatter

        path = WIKI_DIR / "themes" / f"{theme_id}.md"
        if path.exists():
            text = path.read_text(encoding="utf-8")
            fm, _ = _parse_frontmatter(text)
            return fm.get("title", theme_id)
    except Exception:
        pass
    return theme_id


def _replace_wikilinks_across_wiki(
    old_link: str, new_link: str, new_display: str
) -> int:
    """Scan all wiki *.md files and replace [[wikilinks]] referencing old_link.

    Returns count of files modified.
    """
    count = 0
    try:
        for md_file in WIKI_DIR.rglob("*.md"):
            if ".obsidian" in str(md_file):
                continue
            try:
                content = md_file.read_text(encoding="utf-8")
                if old_link not in content:
                    continue

                # Replace [[old_link|...]] with [[new_link|new_display]]
                pattern = re.compile(
                    r"\[\[" + re.escape(old_link) + r"\|[^\]]*\]\]"
                )
                replacement = f"[[{new_link}|{new_display}]]"
                new_content = pattern.sub(replacement, content)

                # Also replace bare [[old_link]]
                bare_pattern = re.compile(
                    r"\[\[" + re.escape(old_link) + r"\]\]"
                )
                new_content = bare_pattern.sub(replacement, new_content)

                if new_content != content:
                    md_file.write_text(new_content, encoding="utf-8")
                    count += 1
                    logger.debug("wiki_wikilink_replaced", file=str(md_file))
            except Exception:
                continue
    except Exception:
        logger.debug("wiki_replace_wikilinks_failed", exc_info=True)

    return count
