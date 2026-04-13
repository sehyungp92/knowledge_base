"""Bootstrap wiki pages from existing database data.

Generates theme, entity, and source pages using Sonnet for quality.
Designed to be run once to populate the wiki from the existing knowledge graph.

Usage:
    python scripts/bootstrap_wiki.py [--dry-run] [--themes-only] [--entities-only]
                                     [--sources-only] [--limit N]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import date
from pathlib import Path

import structlog

# Force UTF-8 for stdout/stderr on Windows (prevents cp949 encoding errors)
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

logger = structlog.get_logger(__name__)

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

WIKI_DIR = PROJECT_ROOT / "wiki"


def bootstrap_wiki(
    executor,
    get_conn_fn=None,
    *,
    dry_run: bool = False,
    themes_only: bool = False,
    entities_only: bool = False,
    sources_only: bool = False,
    limit: int = 0,
) -> dict:
    """Populate wiki from existing database data.

    Args:
        executor: ClaudeExecutor instance for LLM calls.
        get_conn_fn: Connection factory (uses default if None).
        dry_run: If True, log what would be created without writing.
        themes_only: Only bootstrap theme pages.
        entities_only: Only bootstrap entity pages.
        sources_only: Only bootstrap source pages.
        limit: Max pages per type (0 = unlimited).

    Returns:
        Summary dict: {"themes": N, "entities": N, "sources": N, "errors": [...]}.
    """
    from reading_app.db import ensure_pool, get_conn

    if get_conn_fn is None:
        ensure_pool()
        get_conn_fn = get_conn

    from retrieval import wiki_writer, wiki_index
    from retrieval.landscape import get_theme_state

    result = {"themes": 0, "sources": 0, "entities": 0, "timeline_entries": 0, "errors": []}
    do_all = not (themes_only or entities_only or sources_only)
    t0 = time.monotonic()

    # ----- Theme pages (backbone) -----
    if do_all or themes_only:
        result["themes"] = _bootstrap_themes(
            executor, get_conn_fn, get_theme_state, wiki_writer,
            dry_run=dry_run, limit=limit, errors=result["errors"],
        )

    # ----- Source pages (link to themes) -----
    if do_all or sources_only:
        result["sources"] = _bootstrap_sources(
            executor, get_conn_fn, wiki_writer,
            dry_run=dry_run, limit=limit, errors=result["errors"],
        )

    # ----- Entity pages (link to both) -----
    if do_all or entities_only:
        result["entities"] = _bootstrap_entities(
            executor, get_conn_fn, wiki_writer,
            dry_run=dry_run, limit=limit, errors=result["errors"],
        )

    # ----- Populate theme timelines -----
    if do_all or themes_only or sources_only:
        result["timeline_entries"] = _populate_theme_timelines(
            get_conn_fn, wiki_writer,
            dry_run=dry_run, errors=result["errors"],
        )

    # ----- Rebuild indexes -----
    if not dry_run:
        try:
            counts = wiki_index.rebuild_index()
            logger.info("bootstrap_index_rebuilt", counts=counts)
        except Exception as exc:
            result["errors"].append(f"Index rebuild failed: {exc}")

    elapsed = time.monotonic() - t0
    logger.info(
        "bootstrap_complete",
        themes=result["themes"],
        sources=result["sources"],
        entities=result["entities"],
        timeline_entries=result["timeline_entries"],
        errors=len(result["errors"]),
        elapsed_s=round(elapsed, 1),
    )
    return result


# ---------------------------------------------------------------------------
# Per-type bootstrap functions
# ---------------------------------------------------------------------------


def _bootstrap_themes(
    executor, get_conn_fn, get_theme_state, wiki_writer,
    *, dry_run, limit, errors,
) -> int:
    """Bootstrap theme pages. Returns count of pages created."""
    count = 0
    with get_conn_fn() as conn:
        themes = conn.execute(
            "SELECT id, name, level FROM themes ORDER BY level, id"
        ).fetchall()

    total = min(len(themes), limit) if limit else len(themes)
    logger.info("bootstrap_themes_start", total=total)

    for i, theme in enumerate(themes[:total]):
        theme_id = theme["id"]
        try:
            # Skip if page already exists (idempotent re-runs)
            page_path = WIKI_DIR / "themes" / f"{theme_id}.md"
            if not dry_run and page_path.exists():
                logger.info(f"Skipping theme {i+1}/{total}: {theme_id} (already exists)")
                count += 1
                continue

            logger.info(f"Bootstrapping theme {i+1}/{total}: {theme_id}")

            if dry_run:
                count += 1
                continue

            # Gather full theme data
            theme_data = get_theme_state(theme_id)

            with get_conn_fn() as conn:
                row = conn.execute(
                    "SELECT COUNT(*) AS cnt FROM source_themes WHERE theme_id = %s",
                    (theme_id,),
                ).fetchone()
                theme_data["source_count"] = row["cnt"] if row else 0

                # Get theme edges
                edges = conn.execute(
                    """SELECT parent_id, child_id FROM theme_edges
                       WHERE child_id = %s OR parent_id = %s""",
                    (theme_id, theme_id),
                ).fetchall()
                parent_id = ""
                child_ids = []
                for e in edges:
                    if e["child_id"] == theme_id:
                        parent_id = e["parent_id"]
                    if e["parent_id"] == theme_id:
                        child_ids.append(e["child_id"])
                theme_data["theme_edges"] = {
                    "parent_id": parent_id,
                    "child_ids": child_ids,
                }

            path = wiki_writer.create_theme_page(
                theme_id, theme_data, executor, model="sonnet",
            )
            if path:
                count += 1
            else:
                errors.append(f"Theme {theme_id}: create returned None")

        except Exception as exc:
            errors.append(f"Theme {theme_id}: {str(exc)[:200]}")
            logger.warning("bootstrap_theme_failed", theme_id=theme_id, error=str(exc))

    logger.info("bootstrap_themes_complete", created=count)
    return count


def _bootstrap_entities(
    executor, get_conn_fn, wiki_writer,
    *, dry_run, limit, errors,
) -> int:
    """Bootstrap entity pages for top concepts by influence.

    Only creates pages for concepts with >= 3 distinct corpus sources
    (cross-source threshold) to ensure editorial quality.

    Returns count.
    """
    count = 0

    with get_conn_fn() as conn:
        # Join source_concepts to enforce 3+ distinct source threshold
        base_query = """
            SELECT gm.entity_id, gm.score, c.id, c.canonical_name,
                   c.concept_type, c.description, src_cnt.source_count
            FROM graph_metrics gm
            JOIN concepts c ON gm.entity_id = c.id
            JOIN (
                SELECT concept_id, COUNT(DISTINCT source_id) AS source_count
                FROM source_concepts
                GROUP BY concept_id
                HAVING COUNT(DISTINCT source_id) >= 3
            ) src_cnt ON c.id = src_cnt.concept_id
            WHERE gm.metric_type = 'betweenness' AND gm.entity_type = 'concept'
            ORDER BY gm.score DESC"""

        if limit:
            concepts = conn.execute(base_query + " LIMIT %s", (limit,)).fetchall()
        else:
            concepts = conn.execute(base_query).fetchall()

    total = len(concepts)
    logger.info("bootstrap_entities_start", total=total)

    for i, concept in enumerate(concepts):
        concept_id = concept["id"]
        name = concept["canonical_name"]
        try:
            # Skip if page already exists (idempotent re-runs)
            from retrieval.wiki_writer import slugify
            entity_path = WIKI_DIR / "entities" / f"{slugify(name)}.md"
            if not dry_run and entity_path.exists():
                logger.info(f"Skipping entity {i+1}/{total}: {name} (already exists)")
                count += 1
                continue

            logger.info(f"Bootstrapping entity {i+1}/{total}: {name}")

            if dry_run:
                count += 1
                continue

            # Get source references, theme associations, claims, and landscape signals
            with get_conn_fn() as conn:
                source_refs = conn.execute(
                    """SELECT DISTINCT s.id, s.title
                       FROM source_concepts sc
                       JOIN sources s ON sc.source_id = s.id
                       WHERE sc.concept_id = %s
                       LIMIT 20""",
                    (concept_id,),
                ).fetchall()

                theme_rows = conn.execute(
                    """SELECT DISTINCT st.theme_id
                       FROM source_concepts sc
                       JOIN source_themes st ON sc.source_id = st.source_id
                       WHERE sc.concept_id = %s""",
                    (concept_id,),
                ).fetchall()

                related_claims = conn.execute(
                    """SELECT cl.claim_text, cl.evidence_snippet, s.title as source_title
                       FROM claims cl
                       JOIN sources s ON cl.source_id = s.id
                       JOIN source_concepts sc ON sc.source_id = cl.source_id AND sc.concept_id = %s
                       ORDER BY cl.confidence DESC NULLS LAST
                       LIMIT 15""",
                    (concept_id,),
                ).fetchall()

                related_capabilities = conn.execute(
                    """SELECT description, maturity, theme_id
                       FROM capabilities
                       WHERE LOWER(description) LIKE LOWER(%s)
                       LIMIT 5""",
                    (f"%{name}%",),
                ).fetchall()

                related_limitations = conn.execute(
                    """SELECT description, severity, trajectory, theme_id
                       FROM limitations
                       WHERE LOWER(description) LIKE LOWER(%s)
                       LIMIT 5""",
                    (f"%{name}%",),
                ).fetchall()

            concept_data = {
                "canonical_name": name,
                "concept_type": concept.get("concept_type") or "concept",
                "description": concept.get("description") or "",
                "theme_ids": [r["theme_id"] for r in theme_rows],
                "source_references": [
                    {"source_id": r["id"], "title": r["title"]} for r in source_refs
                ],
                "influence_score": concept.get("score", 0.0),
                "related_claims": [dict(c) for c in related_claims],
                "related_capabilities": [dict(c) for c in related_capabilities],
                "related_limitations": [dict(c) for c in related_limitations],
            }

            path = wiki_writer.create_entity_page(
                concept_id, concept_data, executor, model="sonnet",
            )
            if path:
                count += 1
            else:
                errors.append(f"Entity {name}: create returned None")

        except Exception as exc:
            errors.append(f"Entity {name}: {str(exc)[:200]}")
            logger.warning("bootstrap_entity_failed", name=name, error=str(exc))

    logger.info("bootstrap_entities_complete", created=count)
    return count


def _bootstrap_sources(
    executor, get_conn_fn, wiki_writer,
    *, dry_run, limit, errors,
) -> int:
    """Bootstrap source pages for top sources by claim count. Returns count."""
    count = 0

    with get_conn_fn() as conn:
        if limit:
            sources = conn.execute(
                """SELECT s.*, COUNT(cl.id) AS claim_count
                   FROM sources s
                   LEFT JOIN claims cl ON s.id = cl.source_id
                   WHERE s.processing_status = 'complete'
                   GROUP BY s.id
                   ORDER BY claim_count DESC
                   LIMIT %s""",
                (limit,),
            ).fetchall()
        else:
            sources = conn.execute(
                """SELECT s.*, COUNT(cl.id) AS claim_count
                   FROM sources s
                   LEFT JOIN claims cl ON s.id = cl.source_id
                   WHERE s.processing_status = 'complete'
                   GROUP BY s.id
                   ORDER BY claim_count DESC""",
            ).fetchall()

    total = len(sources)
    logger.info("bootstrap_sources_start", total=total)

    for i, source in enumerate(sources):
        source_id = source["id"]
        title = source.get("title", "(untitled)")
        try:
            # Skip if page already exists (idempotent re-runs)
            if not dry_run and list((WIKI_DIR / "sources").glob(f"{source_id[:10]}-*.md")):
                logger.info(f"Skipping source {i+1}/{total}: {title[:60]} (already exists)")
                count += 1
                continue

            logger.info(f"Bootstrapping source {i+1}/{total}: {title[:60]}")

            if dry_run:
                count += 1
                continue

            # Get claims
            with get_conn_fn() as conn:
                claims = conn.execute(
                    """SELECT claim_text, evidence_snippet
                       FROM claims WHERE source_id = %s
                       ORDER BY id LIMIT 20""",
                    (source_id,),
                ).fetchall()

                theme_rows = conn.execute(
                    "SELECT theme_id FROM source_themes WHERE source_id = %s",
                    (source_id,),
                ).fetchall()

            # Read library artifacts
            library_dir = PROJECT_ROOT / "library" / source_id

            deep_summary = ""
            if (library_dir / "deep_summary.md").exists():
                deep_summary = (library_dir / "deep_summary.md").read_text(encoding="utf-8")

            landscape_signals = {}
            if (library_dir / "landscape.json").exists():
                landscape_signals = json.loads(
                    (library_dir / "landscape.json").read_text(encoding="utf-8")
                )

            authors = source.get("authors") or []
            if isinstance(authors, str):
                try:
                    authors = json.loads(authors)
                except Exception:
                    authors = [authors]

            source_data = {
                "title": title,
                "authors": authors,
                "published_at": source.get("published_at", ""),
                "source_type": source.get("source_type", "article"),
                "claims": [dict(c) for c in claims],
                "landscape_contributions": landscape_signals,
                "deep_summary": deep_summary,
                "theme_ids": [r["theme_id"] for r in theme_rows],
            }

            path = wiki_writer.create_source_page(
                source_id, source_data, executor, model="sonnet",
            )
            if path:
                count += 1
            else:
                errors.append(f"Source {title[:60]}: create returned None")

        except Exception as exc:
            errors.append(f"Source {title[:60]}: {str(exc)[:200]}")
            logger.warning("bootstrap_source_failed", source_id=source_id, error=str(exc))

    logger.info("bootstrap_sources_complete", created=count)
    return count


def _populate_theme_timelines(
    get_conn_fn, wiki_writer,
    *, dry_run, errors,
) -> int:
    """Populate theme page timelines from source data. Deterministic, zero LLM calls.

    For each theme, inserts a timeline entry for every source associated with it,
    ordered by published_at date. Uses existing _insert_timeline_entry and
    _build_timeline_summary functions from wiki_writer.

    Returns count of timeline entries inserted.
    """
    from retrieval.wiki_writer import (
        WIKI_DIR, _insert_timeline_entry, _build_timeline_summary,
        _to_date, _parse_frontmatter, _render_frontmatter, slugify,
    )

    count = 0
    landscape_cache: dict[str, dict] = {}  # source_id -> parsed landscape.json

    with get_conn_fn() as conn:
        themes = conn.execute("SELECT id FROM themes ORDER BY id").fetchall()

    total = len(themes)
    logger.info("bootstrap_timelines_start", total=total)

    for i, theme_row in enumerate(themes):
        theme_id = theme_row["id"]
        page_path = WIKI_DIR / "themes" / f"{theme_id}.md"
        if not page_path.exists():
            continue

        try:
            # Get sources + batch claims in one connection
            with get_conn_fn() as conn:
                sources = conn.execute(
                    """SELECT s.id, s.title, s.published_at
                       FROM source_themes st
                       JOIN sources s ON st.source_id = s.id
                       WHERE st.theme_id = %s AND s.processing_status = 'complete'
                       ORDER BY s.published_at ASC NULLS LAST""",
                    (theme_id,),
                ).fetchall()

                if not sources:
                    continue

                source_ids = [s["id"] for s in sources]

                all_claims = conn.execute(
                    """SELECT source_id, claim_text FROM claims
                       WHERE source_id = ANY(%s)
                       ORDER BY confidence DESC NULLS LAST""",
                    (source_ids,),
                ).fetchall()

            # Group claims by source (top 5 each)
            claims_by_source: dict[str, list] = {}
            for c in all_claims:
                sid = c["source_id"]
                if sid not in claims_by_source:
                    claims_by_source[sid] = []
                if len(claims_by_source[sid]) < 5:
                    claims_by_source[sid].append(dict(c))

            logger.info(f"Populating timeline {i+1}/{total}: {theme_id} ({len(sources)} sources)")

            if dry_run:
                count += len(sources)
                continue

            body = page_path.read_text(encoding="utf-8")
            fm, page_body = _parse_frontmatter(body)

            for source in sources:
                source_id = source["id"]
                title = source["title"] or "(untitled)"

                # Skip if this source already has a timeline entry
                if source_id[:10] in page_body:
                    count += 1
                    continue

                published_at = _to_date(source.get("published_at"))

                # Read landscape.json with cross-theme cache
                if source_id not in landscape_cache:
                    library_dir = PROJECT_ROOT / "library" / source_id
                    lpath = library_dir / "landscape.json"
                    if lpath.exists():
                        try:
                            landscape_cache[source_id] = json.loads(
                                lpath.read_text(encoding="utf-8")
                            )
                        except Exception:
                            landscape_cache[source_id] = {}
                    else:
                        landscape_cache[source_id] = {}

                # Filter signals to this theme
                all_signals = landscape_cache[source_id]
                theme_signals = {}
                for key in ("capabilities", "limitations", "bottlenecks", "breakthroughs"):
                    items = all_signals.get(key, [])
                    filtered = [s for s in items if s.get("theme_id") == theme_id]
                    if filtered:
                        theme_signals[key] = filtered

                claim_list = claims_by_source.get(source_id, [])
                summary = _build_timeline_summary(title, claim_list, theme_signals)
                slug = slugify(title)
                entry = f"- **{published_at.isoformat()}** — [[sources/{source_id[:10]}-{slug}|{title}]]: {summary}"

                page_body = _insert_timeline_entry(page_body, entry, published_at)
                count += 1

            # Write updated page
            fm["updated"] = date.today().isoformat()
            content = _render_frontmatter(fm) + "\n" + page_body.strip() + "\n"
            page_path.write_text(content, encoding="utf-8")

        except Exception as exc:
            errors.append(f"Timeline {theme_id}: {str(exc)[:200]}")
            logger.warning("bootstrap_timeline_failed", theme_id=theme_id, error=str(exc))

    logger.info("bootstrap_timelines_complete", entries=count)
    return count


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from reading_app.db import ensure_pool, get_conn
    from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE

    parser = argparse.ArgumentParser(description="Bootstrap wiki from database")
    parser.add_argument("--dry-run", action="store_true", help="Log without writing")
    parser.add_argument("--themes-only", action="store_true", help="Only bootstrap themes")
    parser.add_argument("--entities-only", action="store_true", help="Only bootstrap entities")
    parser.add_argument("--sources-only", action="store_true", help="Only bootstrap sources")
    parser.add_argument("--limit", type=int, default=0, help="Max pages per type (0=unlimited)")
    args = parser.parse_args()

    ensure_pool()
    executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    result = bootstrap_wiki(
        executor,
        get_conn,
        dry_run=args.dry_run,
        themes_only=args.themes_only,
        entities_only=args.entities_only,
        sources_only=args.sources_only,
        limit=args.limit,
    )
    print(json.dumps(result, indent=2, default=str))
