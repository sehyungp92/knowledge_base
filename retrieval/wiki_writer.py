"""Wiki page generation and update engine.

Every wiki write goes through this module. Creates and incrementally updates
theme, entity, source, and synthesis pages using LLM calls for narrative
sections and deterministic operations for timeline entries and frontmatter.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any

import structlog

from retrieval import wiki_index

logger = structlog.get_logger(__name__)

WIKI_DIR = Path(__file__).resolve().parent.parent / "wiki"


# ---------------------------------------------------------------------------
# Public API — Theme pages
# ---------------------------------------------------------------------------


def create_theme_page(
    theme_id: str,
    theme_data: dict,
    executor,
    model: str = "sonnet",
) -> Path | None:
    """Generate a new theme wiki page from landscape data.

    Args:
        theme_id: Theme identifier (e.g. 'llm-reasoning').
        theme_data: Dict from get_theme_state() with keys: theme, capabilities,
            limitations, bottlenecks, breakthroughs, anticipations,
            cross_theme_implications. Plus source_count, theme_edges.
        executor: ClaudeExecutor instance.
        model: LLM model tier for generation.

    Returns:
        Path to created page, or None on failure.
    """
    session_id = f"wiki_create_{theme_id}"
    try:
        theme = theme_data.get("theme")
        if not theme:
            logger.warning("wiki_create_theme_no_data", theme_id=theme_id)
            return None

        page_path = WIKI_DIR / "themes" / f"{theme_id}.md"
        page_path.parent.mkdir(parents=True, exist_ok=True)

        # Build frontmatter
        theme_edges = theme_data.get("theme_edges", {})
        fm = {
            "type": "theme",
            "title": theme.get("name", theme_id),
            "theme_id": theme_id,
            "level": theme.get("level", 1),
            "parent_theme": theme_edges.get("parent_id", ""),
            "child_themes": theme_edges.get("child_ids", []),
            "created": date.today().isoformat(),
            "updated": date.today().isoformat(),
            "source_count": theme_data.get("source_count", 0),
            "sources_since_update": 0,
            "update_count": 1,
            "velocity": theme.get("velocity", 0.0),
            "staleness": 0.0,
            "status": "active",
            "tags": [],
        }

        # Query sources for this theme to inject canonical wikilinks
        source_refs = None
        try:
            from reading_app.db import get_conn as _get_conn
            with _get_conn() as conn:
                src_rows = conn.execute(
                    "SELECT s.id, s.title FROM sources s "
                    "JOIN source_themes st ON s.id = st.source_id "
                    "WHERE st.theme_id = %s LIMIT 20",
                    (theme_id,),
                ).fetchall()
            if src_rows:
                source_refs = [(r["id"], r["title"]) for r in src_rows if r["title"]]
        except Exception:
            logger.debug("wiki_create_theme_source_lookup_failed", theme_id=theme_id, exc_info=True)

        # Build prompt
        prompt = _build_theme_create_prompt(theme_data, source_refs=source_refs)
        result = executor.run_raw(
            prompt,
            session_id=session_id,
            model=model,
            timeout=300,
        )

        body = result.text if result and result.text else ""
        if not body or len(body) < 50:
            logger.warning("wiki_create_theme_empty_response", theme_id=theme_id)
            body = _build_theme_fallback(theme_data)

        body = _sanitize_llm_output(body)

        # Assemble page
        content = _render_frontmatter(fm) + "\n" + body.strip() + "\n"
        page_path.write_text(content, encoding="utf-8")

        wiki_index.on_page_created(page_path, "theme", fm)
        logger.info("wiki_theme_created", theme_id=theme_id, path=str(page_path))
        return page_path

    except Exception:
        logger.debug("wiki_create_theme_failed", theme_id=theme_id, exc_info=True)
        return None
    finally:
        try:
            executor.cleanup_session(session_id)
        except Exception:
            pass


def update_theme_page(
    theme_id: str,
    source_data: dict,
    executor,
    model: str = "haiku",
) -> Path | None:
    """Incrementally update a theme page with new source data.

    Args:
        theme_id: Theme identifier.
        source_data: Dict with keys: source_id, title, published_at, claims,
            landscape_signals, implications.
        executor: ClaudeExecutor instance.
        model: LLM model tier for updates.

    Returns:
        Path to updated page, or None on failure.
    """
    page_path = WIKI_DIR / "themes" / f"{theme_id}.md"

    if not page_path.exists():
        # Delegate to create — need full theme data
        try:
            from retrieval.landscape import get_theme_state
            from reading_app.db import get_conn

            theme_data = get_theme_state(theme_id)
            with get_conn() as conn:
                row = conn.execute(
                    "SELECT COUNT(*) AS cnt FROM source_themes WHERE theme_id = %s",
                    (theme_id,),
                ).fetchone()
                theme_data["source_count"] = row["cnt"] if row else 0

                edges = conn.execute(
                    "SELECT parent_id, child_id FROM theme_edges WHERE child_id = %s OR parent_id = %s",
                    (theme_id, theme_id),
                ).fetchall()
                parent_id = ""
                child_ids = []
                for e in edges:
                    if e["child_id"] == theme_id:
                        parent_id = e["parent_id"]
                    if e["parent_id"] == theme_id:
                        child_ids.append(e["child_id"])
                theme_data["theme_edges"] = {"parent_id": parent_id, "child_ids": child_ids}

            return create_theme_page(theme_id, theme_data, executor, model="sonnet")
        except Exception:
            logger.debug("wiki_update_theme_create_fallback_failed", theme_id=theme_id, exc_info=True)
            return None

    session_id = f"wiki_update_{theme_id}"
    try:
        text = page_path.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(text)

        # Insert timeline entry (deterministic, no LLM)
        published_at = source_data.get("published_at")
        pub_date = _to_date(published_at) if published_at else date.today()
        source_id = source_data.get("source_id", "unknown")
        title = source_data.get("title", "Untitled")
        claims = source_data.get("claims", [])
        signals = source_data.get("landscape_signals") or {}

        timeline_summary = _build_timeline_summary(title, claims, signals)
        entry = f"- **{pub_date.isoformat()}** — [Source: {source_id}, published {pub_date.isoformat()}] {timeline_summary}"
        body = _insert_timeline_entry(body, entry, pub_date)

        # Extract body without timeline for LLM update
        body_without_timeline, timeline_section = _split_timeline(body)

        # Compute canonical wikilink refs for the new source
        source_ref = _format_source_ref(source_id, title)
        # Query entities for this source
        entity_refs = None
        try:
            from reading_app.db import get_conn as _get_conn
            with _get_conn() as conn:
                concept_rows = conn.execute(
                    "SELECT c.canonical_name FROM source_concepts sc "
                    "JOIN concepts c ON sc.concept_id = c.id "
                    "WHERE sc.source_id = %s",
                    (source_id,),
                ).fetchall()
            if concept_rows:
                entity_refs = [(r["canonical_name"], slugify(r["canonical_name"])) for r in concept_rows]
        except Exception:
            pass

        # Build LLM prompt for incremental update
        prompt = _build_theme_update_prompt(
            body_without_timeline, source_data,
            source_ref=source_ref, entity_refs=entity_refs,
        )
        result = executor.run_raw(
            prompt,
            session_id=session_id,
            model=model,
            timeout=60,
        )

        updated_body = result.text if result and result.text else body_without_timeline
        if len(updated_body) < 50:
            updated_body = body_without_timeline

        # Extract and file emergent connections (before timeline strip)
        updated_body, emergent = _extract_emergent_connections(updated_body)
        if emergent:
            _file_emergent_connections(emergent, source_data.get("source_id", ""))

        # Defensive: strip LLM wrapper prose and frontmatter
        updated_body = _sanitize_llm_output(updated_body)

        # Defensive: strip any LLM-generated timeline (prompt says not to, but be safe)
        updated_body, _ = _split_timeline(updated_body)

        # Reassemble: updated body + preserved timeline
        full_body = updated_body.strip() + "\n\n" + timeline_section.strip() + "\n"

        # Update frontmatter
        fm["updated"] = date.today().isoformat()
        fm["update_count"] = fm.get("update_count", 0) + 1
        fm["sources_since_update"] = 0
        fm["staleness"] = 0.0

        content = _render_frontmatter(fm) + "\n" + full_body
        page_path.write_text(content, encoding="utf-8")

        wiki_index.on_page_updated(page_path, "theme", fm)
        logger.info("wiki_theme_updated", theme_id=theme_id)
        return page_path

    except Exception:
        logger.debug("wiki_update_theme_failed", theme_id=theme_id, exc_info=True)
        return None
    finally:
        try:
            executor.cleanup_session(session_id)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Public API — Source pages
# ---------------------------------------------------------------------------


def create_source_page(
    source_id: str,
    source_data: dict,
    executor,
    model: str = "sonnet",
) -> Path | None:
    """Generate a wiki page for a source.

    Args:
        source_id: ULID source identifier.
        source_data: Dict with keys: title, authors, published_at, source_type,
            claims, landscape_contributions, theme_ids.
        executor: ClaudeExecutor instance.
        model: LLM model tier.

    Returns:
        Path to created page, or None on failure.
    """
    session_id = f"wiki_source_{source_id[:10]}"
    try:
        title = source_data.get("title", "Untitled")
        slug = slugify(title)
        filename = f"{source_id[:10]}-{slug}.md"
        page_path = WIKI_DIR / "sources" / filename
        page_path.parent.mkdir(parents=True, exist_ok=True)

        authors = source_data.get("authors", [])
        if isinstance(authors, str):
            import json as _json
            try:
                authors = _json.loads(authors)
            except Exception:
                authors = [authors]

        fm = {
            "type": "source",
            "title": title,
            "source_id": source_id,
            "source_type": source_data.get("source_type", "article"),
            "authors": authors if isinstance(authors, list) else [],
            "published_at": str(source_data.get("published_at", "")),
            "theme_ids": source_data.get("theme_ids", []),
            "created": date.today().isoformat(),
            "updated": date.today().isoformat(),
            "claim_count": len(source_data.get("claims", [])),
            "tags": [],
        }

        # Query entities for this source to inject canonical wikilinks
        entity_refs = None
        try:
            from reading_app.db import get_conn as _get_conn
            with _get_conn() as conn:
                concept_rows = conn.execute(
                    "SELECT c.canonical_name FROM source_concepts sc "
                    "JOIN concepts c ON sc.concept_id = c.id "
                    "WHERE sc.source_id = %s",
                    (source_id,),
                ).fetchall()
            if concept_rows:
                entity_refs = [(r["canonical_name"], slugify(r["canonical_name"])) for r in concept_rows]
        except Exception:
            logger.debug("wiki_source_entity_lookup_failed", source_id=source_id, exc_info=True)

        prompt = _build_source_create_prompt(source_data, entity_refs=entity_refs)
        result = executor.run_raw(
            prompt,
            session_id=session_id,
            model=model,
            timeout=120,
        )

        body = result.text if result and result.text else _build_source_fallback(source_data)
        body = _sanitize_llm_output(body)
        content = _render_frontmatter(fm) + "\n" + body.strip() + "\n"
        page_path.write_text(content, encoding="utf-8")

        wiki_index.on_page_created(page_path, "source", fm)
        logger.info("wiki_source_created", source_id=source_id, path=str(page_path))
        return page_path

    except Exception:
        logger.debug("wiki_create_source_failed", source_id=source_id, exc_info=True)
        return None
    finally:
        try:
            executor.cleanup_session(session_id)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Public API — Entity pages
# ---------------------------------------------------------------------------


def create_entity_page(
    concept_id: str,
    concept_data: dict,
    executor,
    model: str = "sonnet",
) -> Path | None:
    """Generate a wiki page for a concept/entity.

    Args:
        concept_id: Concept identifier.
        concept_data: Dict with keys: canonical_name, concept_type, description,
            theme_ids, source_references, influence_score.
        executor: ClaudeExecutor instance.
        model: LLM model tier.

    Returns:
        Path to created page, or None on failure.
    """
    session_id = f"wiki_entity_{concept_id[:10]}"
    try:
        name = concept_data.get("canonical_name", concept_id)
        slug = slugify(name)
        page_path = WIKI_DIR / "entities" / f"{slug}.md"
        page_path.parent.mkdir(parents=True, exist_ok=True)

        fm = {
            "type": "entity",
            "title": name,
            "entity_type": concept_data.get("concept_type", "concept"),
            "theme_ids": concept_data.get("theme_ids", []),
            "created": date.today().isoformat(),
            "updated": date.today().isoformat(),
            "source_count": len(concept_data.get("source_references", [])),
            "sources_since_update": 0,
            "update_count": 1,
            "influence_score": concept_data.get("influence_score", 0.0),
            "staleness": 0.0,
            "status": "active",
            "tags": [],
        }

        # Compute canonical source wikilink targets
        source_refs = None
        sources = concept_data.get("source_references", [])
        if sources:
            source_refs = []
            for s in sources[:10]:
                if isinstance(s, dict):
                    sid = s.get("source_id", "")
                    stitle = s.get("title", "")
                    if sid and stitle:
                        source_refs.append((sid, stitle, f"{sid[:10]}-{slugify(stitle)}"))

        prompt = _build_entity_create_prompt(concept_data, source_refs=source_refs)
        result = executor.run_raw(
            prompt,
            session_id=session_id,
            model=model,
            timeout=120,
        )

        body = result.text if result and result.text else _build_entity_fallback(concept_data)
        body = _sanitize_llm_output(body)
        content = _render_frontmatter(fm) + "\n" + body.strip() + "\n"
        page_path.write_text(content, encoding="utf-8")

        wiki_index.on_page_created(page_path, "entity", fm)
        logger.info("wiki_entity_created", concept_id=concept_id, path=str(page_path))
        return page_path

    except Exception:
        logger.debug("wiki_create_entity_failed", concept_id=concept_id, exc_info=True)
        return None
    finally:
        try:
            executor.cleanup_session(session_id)
        except Exception:
            pass


def update_entity_page(
    slug: str,
    new_data: dict,
    executor,
    model: str = "haiku",
) -> Path | None:
    """Incrementally update an entity page with new information."""
    page_path = WIKI_DIR / "entities" / f"{slug}.md"
    if not page_path.exists():
        logger.debug("wiki_update_entity_not_found", slug=slug)
        return None

    session_id = f"wiki_update_entity_{slug}"
    try:
        text = page_path.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(text)

        prompt = _build_entity_update_prompt(body, new_data)
        result = executor.run_raw(
            prompt,
            session_id=session_id,
            model=model,
            timeout=60,
        )

        updated_body = result.text if result and result.text else body
        if len(updated_body) < 30:
            updated_body = body

        # Defensive: strip LLM wrapper prose and frontmatter
        updated_body = _sanitize_llm_output(updated_body)

        fm["updated"] = date.today().isoformat()
        fm["update_count"] = fm.get("update_count", 0) + 1
        fm["sources_since_update"] = 0
        fm["staleness"] = 0.0

        content = _render_frontmatter(fm) + "\n" + updated_body.strip() + "\n"
        page_path.write_text(content, encoding="utf-8")

        wiki_index.on_page_updated(page_path, "entity", fm)
        logger.info("wiki_entity_updated", slug=slug)
        return page_path

    except Exception:
        logger.debug("wiki_update_entity_failed", slug=slug, exc_info=True)
        return None
    finally:
        try:
            executor.cleanup_session(session_id)
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Public API — Synthesis pages
# ---------------------------------------------------------------------------


def create_synthesis_page(
    slug: str,
    content_text: str,
    theme_ids: list[str],
    executor,
) -> Path | None:
    """Write a synthesis page from skill output.

    Args:
        slug: URL-safe slug for the filename.
        content_text: Markdown content (from /synthesis or /reflect topic).
        theme_ids: Related theme identifiers.
        executor: ClaudeExecutor instance (unused — no LLM call needed).

    Returns:
        Path to created page, or None on failure.
    """
    try:
        slug = slugify(slug)
        page_path = WIKI_DIR / "syntheses" / f"{slug}.md"
        page_path.parent.mkdir(parents=True, exist_ok=True)

        # Extract title from first heading or slug
        title = slug.replace("-", " ").title()
        first_heading = re.search(r"^#\s+(.+)$", content_text, re.MULTILINE)
        if first_heading:
            title = first_heading.group(1).strip()

        fm = {
            "type": "synthesis",
            "title": title,
            "theme_ids": theme_ids,
            "created": date.today().isoformat(),
            "updated": date.today().isoformat(),
            "source_count": 0,
            "tags": [],
        }

        # Add theme wikilinks if not already present
        theme_links = "\n".join(
            f"- {_format_theme_ref(t)}" for t in theme_ids
        )
        body = _sanitize_llm_output(content_text.strip())
        if theme_links and "[[themes/" not in body:
            body += f"\n\n## Related Themes\n\n{theme_links}\n"

        full_content = _render_frontmatter(fm) + "\n" + body + "\n"
        page_path.write_text(full_content, encoding="utf-8")

        wiki_index.on_page_created(page_path, "synthesis", fm)
        logger.info("wiki_synthesis_created", slug=slug, path=str(page_path))
        return page_path

    except Exception:
        logger.debug("wiki_create_synthesis_failed", slug=slug, exc_info=True)
        return None


def create_question_page(
    question: str,
    answer: str,
    theme_ids: list[str],
) -> Path | None:
    """File a question-answer pair as a wiki page. No LLM call needed."""
    try:
        slug = slugify(question)
        page_path = WIKI_DIR / "questions" / f"{slug}.md"
        page_path.parent.mkdir(parents=True, exist_ok=True)

        if page_path.exists():
            # Update existing question page with new answer
            result = _read_page(page_path)
            if result:
                old_fm, old_body = result
                old_fm["updated"] = date.today().isoformat()
                if theme_ids:
                    existing = set(old_fm.get("theme_ids", []))
                    existing.update(theme_ids)
                    old_fm["theme_ids"] = sorted(existing)
                new_body = f"# {question}\n\n{answer}"
                if theme_ids:
                    theme_links = "\n".join(f"- {_format_theme_ref(t)}" for t in old_fm["theme_ids"])
                    new_body += f"\n\n## Related Themes\n\n{theme_links}"
                _write_page(page_path, old_fm, new_body, "question")
            return page_path

        fm = {
            "type": "question",
            "title": question[:120],
            "theme_ids": theme_ids,
            "created": date.today().isoformat(),
            "updated": date.today().isoformat(),
            "tags": [],
        }

        body = f"# {question}\n\n{answer}"

        # Add theme wikilinks for navigability (matching synthesis page pattern)
        if theme_ids:
            theme_links = "\n".join(f"- {_format_theme_ref(t)}" for t in theme_ids)
            body += f"\n\n## Related Themes\n\n{theme_links}"

        full_content = _render_frontmatter(fm) + "\n" + body + "\n"
        page_path.write_text(full_content, encoding="utf-8")

        wiki_index.on_page_created(page_path, "question", fm)
        logger.info("wiki_question_page_created", slug=slug)
        return page_path
    except Exception:
        logger.warning("wiki_question_page_failed", exc_info=True)
        return None


# ---------------------------------------------------------------------------
# Public API — Orchestrator for /save pipeline
# ---------------------------------------------------------------------------


def update_wiki_for_source(
    source_id: str,
    title: str,
    theme_ids: list[str],
    published_at: datetime | None,
    claims: list[dict],
    landscape_signals: dict | None,
    implications: list[dict],
    executor,
    model: str = "haiku",
    summary: str = "",
) -> dict:
    """Orchestrate all wiki updates after a source is saved.

    Called from save_handler as a background task.

    Returns:
        Summary dict: {source_page, themes_updated, entities_updated}.
    """
    result = {"source_page": None, "themes_updated": [], "entities_updated": []}

    source_data = {
        "source_id": source_id,
        "title": title,
        "published_at": published_at,
        "claims": claims,
        "landscape_signals": landscape_signals,
        "implications": implications,
    }

    # 1. Create source summary page
    try:
        from reading_app.db import get_conn

        with get_conn() as conn:
            source_row = conn.execute(
                "SELECT * FROM sources WHERE id = %s", (source_id,)
            ).fetchone()

        if source_row:
            page_data = {
                "title": title,
                "authors": source_row.get("authors") or [],
                "published_at": published_at,
                "source_type": source_row.get("source_type", "article"),
                "claims": claims,
                "landscape_contributions": landscape_signals,
                "theme_ids": theme_ids,
                "deep_summary": summary,
            }
            sp = create_source_page(source_id, page_data, executor, model=model)
            result["source_page"] = str(sp) if sp else None
    except Exception:
        logger.debug("wiki_update_source_page_failed", source_id=source_id, exc_info=True)

    # 2. Update theme pages
    for tid in theme_ids:
        try:
            p = update_theme_page(tid, source_data, executor, model=model)
            if p:
                result["themes_updated"].append(tid)
        except Exception:
            logger.debug("wiki_update_theme_page_failed", theme_id=tid, exc_info=True)

    # 3. Update entity pages for concepts in this source
    try:
        from reading_app.db import get_conn

        with get_conn() as conn:
            concepts = conn.execute(
                """SELECT c.id, c.canonical_name, c.concept_type, c.description
                   FROM source_concepts sc
                   JOIN concepts c ON sc.concept_id = c.id
                   WHERE sc.source_id = %s""",
                (source_id,),
            ).fetchall()

        for concept in concepts:
            slug = slugify(concept["canonical_name"])
            entity_path = WIKI_DIR / "entities" / f"{slug}.md"
            if entity_path.exists():
                try:
                    new_data = {
                        "source_id": source_id,
                        "source_title": title,
                        "published_at": published_at,
                        "claims": [c for c in claims if concept["canonical_name"].lower() in c.get("claim_text", "").lower()],
                        "landscape_signals": _filter_signals_for_entity(landscape_signals, concept["canonical_name"]),
                    }
                    p = update_entity_page(slug, new_data, executor, model=model)
                    if p:
                        result["entities_updated"].append(slug)
                except Exception:
                    logger.debug("wiki_update_entity_failed", slug=slug, exc_info=True)

        # 4. Create pages for new concepts with >= 3 distinct sources in corpus
        # Batch: collect concepts needing pages, then query corpus counts in one go
        candidates = []
        for concept in concepts:
            slug = slugify(concept["canonical_name"])
            entity_path = WIKI_DIR / "entities" / f"{slug}.md"
            if not entity_path.exists():
                candidates.append((concept, slug))

        if candidates:
            # Batch corpus-count query for all candidate concept IDs
            candidate_ids = [c["id"] for c, _ in candidates]
            corpus_counts: dict[str, int] = {}
            try:
                with get_conn() as conn2:
                    rows = conn2.execute(
                        "SELECT concept_id, COUNT(DISTINCT source_id) AS cnt "
                        "FROM source_concepts WHERE concept_id = ANY(%s) "
                        "GROUP BY concept_id",
                        (candidate_ids,),
                    ).fetchall()
                corpus_counts = {r["concept_id"]: r["cnt"] for r in rows}
            except Exception:
                logger.debug("wiki_batch_corpus_count_failed", exc_info=True)

            # Batch source-references query for qualifying concepts
            qualifying_ids = [cid for cid in candidate_ids if corpus_counts.get(cid, 0) >= 3]
            source_refs_by_concept: dict[str, list[dict]] = {}
            if qualifying_ids:
                try:
                    with get_conn() as conn3:
                        ref_rows = conn3.execute(
                            "SELECT sc.concept_id, s.id, s.title FROM sources s "
                            "JOIN source_concepts sc ON s.id = sc.source_id "
                            "WHERE sc.concept_id = ANY(%s)",
                            (qualifying_ids,),
                        ).fetchall()
                    for r in ref_rows:
                        cid = r["concept_id"]
                        source_refs_by_concept.setdefault(cid, []).append(
                            {"source_id": r["id"], "title": r["title"]}
                        )
                except Exception:
                    logger.debug("wiki_batch_source_refs_failed", exc_info=True)

            for concept, slug in candidates:
                cid = concept["id"]
                if corpus_counts.get(cid, 0) >= 3:
                    try:
                        related = [c for c in claims if concept["canonical_name"].lower() in c.get("claim_text", "").lower()]
                        source_references = source_refs_by_concept.get(cid, [{"source_id": source_id, "title": title}])[:10]

                        concept_data = {
                            "canonical_name": concept["canonical_name"],
                            "concept_type": concept.get("concept_type", "concept"),
                            "description": concept.get("description", ""),
                            "theme_ids": theme_ids,
                            "source_references": source_references,
                            "related_claims": related,
                        }
                        p = create_entity_page(concept["id"], concept_data, executor, model=model)
                        if p:
                            result["entities_created"] = result.get("entities_created", [])
                            result["entities_created"].append(slug)
                    except Exception:
                        logger.debug("wiki_create_new_entity_failed", slug=slug, exc_info=True)

    except Exception:
        logger.debug("wiki_update_entities_failed", source_id=source_id, exc_info=True)

    # 5. Propagate staleness to parent themes
    neighbours_patched = _propagate_to_parent_themes(theme_ids, result["themes_updated"])
    result["neighbours_patched"] = neighbours_patched

    logger.info("wiki_update_for_source_complete",
        source_id=source_id,
        source_page_created=result["source_page"] is not None,
        themes_updated=result["themes_updated"],
        themes_failed=[t for t in theme_ids if t not in result["themes_updated"]],
        entities_updated=result["entities_updated"],
        entities_created=result.get("entities_created", []),
        neighbours_patched=result.get("neighbours_patched", []),
    )
    return result


def delete_source_from_wiki(source_id: str, theme_ids: list[str] | None = None) -> None:
    """Remove a source's wiki page and update affected theme staleness.

    Args:
        source_id: Source identifier.
        theme_ids: Pre-fetched theme IDs for this source. If None, attempts
            DB lookup (may return empty if source already deleted).
    """
    try:
        # Find and delete source page
        source_dir = WIKI_DIR / "sources"
        if source_dir.exists():
            for p in source_dir.glob(f"{source_id[:10]}-*.md"):
                wiki_index.on_page_deleted(p, "source")
                p.unlink()
                logger.info("wiki_source_deleted", path=str(p))

        # Increment staleness on affected theme pages
        _increment_theme_staleness(source_id, theme_ids=theme_ids)

    except Exception:
        logger.debug("wiki_delete_source_failed", source_id=source_id, exc_info=True)


def prune_sub_threshold_entities(
    min_source_count: int = 3,
    *,
    dry_run: bool = True,
) -> dict:
    """Remove or flag entity pages that don't meet the cross-source threshold.

    Scans wiki/entities/ for pages whose corpus-wide distinct source count
    is below min_source_count. In dry_run mode, reports what would be pruned.
    Otherwise, deletes the pages and updates the wiki index.

    Args:
        min_source_count: Minimum distinct sources required (default 3).
        dry_run: If True, report only. If False, delete sub-threshold pages.

    Returns:
        {"pruned": [...slugs...], "kept": int, "errors": [...]}
    """
    from reading_app.db import get_conn

    result: dict = {"pruned": [], "kept": 0, "errors": []}
    entity_dir = WIKI_DIR / "entities"
    if not entity_dir.exists():
        return result

    # Collect all entity page slugs
    entity_pages = [p for p in entity_dir.glob("*.md")
                    if p.name not in ("index.md", "overview.md")]
    if not entity_pages:
        return result

    # Build slug → concept_id mapping via DB
    # Entity pages are named by slugify(canonical_name)
    try:
        with get_conn() as conn:
            all_concepts = conn.execute(
                "SELECT id, canonical_name FROM concepts"
            ).fetchall()
        slug_to_concept: dict[str, str] = {}
        for c in all_concepts:
            slug_to_concept[slugify(c["canonical_name"])] = c["id"]

        # Batch query corpus-wide source counts
        concept_ids = list(slug_to_concept.values())
        if concept_ids:
            with get_conn() as conn:
                rows = conn.execute(
                    "SELECT concept_id, COUNT(DISTINCT source_id) AS cnt "
                    "FROM source_concepts WHERE concept_id = ANY(%s) "
                    "GROUP BY concept_id",
                    (concept_ids,),
                ).fetchall()
            corpus_counts = {r["concept_id"]: r["cnt"] for r in rows}
        else:
            corpus_counts = {}
    except Exception as exc:
        result["errors"].append(f"DB query failed: {exc}")
        return result

    for page_path in entity_pages:
        slug = page_path.stem
        concept_id = slug_to_concept.get(slug)

        if concept_id is None:
            # Entity page with no matching concept in DB — candidate for pruning
            source_count = 0
        else:
            source_count = corpus_counts.get(concept_id, 0)

        if source_count < min_source_count:
            if dry_run:
                result["pruned"].append(slug)
            else:
                try:
                    wiki_index.on_page_deleted(page_path, "entity")
                    page_path.unlink()
                    result["pruned"].append(slug)
                    logger.info("wiki_entity_pruned", slug=slug, source_count=source_count)
                except Exception as exc:
                    result["errors"].append(f"Delete {slug}: {exc}")
        else:
            result["kept"] += 1

    if not dry_run and result["pruned"]:
        invalidate_wiki_target_cache()
    logger.info(
        "wiki_entity_prune_complete",
        pruned=len(result["pruned"]),
        kept=result["kept"],
        dry_run=dry_run,
    )
    return result


def link_source_entities(*, dry_run: bool = True) -> dict:
    """Add entity wikilinks to source pages that lack them.

    Queries source_concepts to find entities discussed in each source,
    then appends a '## Key Concepts' section with canonical entity wikilinks
    (only for entities that have an existing wiki page).

    Returns:
        {"updated": int, "skipped": int, "errors": [...]}
    """
    from collections import defaultdict

    from reading_app.db import get_conn

    result: dict = {"updated": 0, "skipped": 0, "errors": []}
    source_dir = WIKI_DIR / "sources"
    if not source_dir.exists():
        return result

    # Batch: source_id prefix → entity names
    try:
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT s.id, c.canonical_name "
                "FROM source_concepts sc "
                "JOIN concepts c ON sc.concept_id = c.id "
                "JOIN sources s ON sc.source_id = s.id "
                "ORDER BY s.id, c.canonical_name"
            ).fetchall()
    except Exception as exc:
        result["errors"].append(f"DB query failed: {exc}")
        return result

    prefix_entities: dict[str, list[str]] = defaultdict(list)
    for r in rows:
        prefix = r["id"][:10]
        name = r["canonical_name"]
        if name not in prefix_entities[prefix]:
            prefix_entities[prefix].append(name)

    # Only link to entities that have wiki pages
    entity_dir = WIKI_DIR / "entities"
    existing_slugs = set()
    if entity_dir.exists():
        existing_slugs = {p.stem for p in entity_dir.glob("*.md")}

    for page_path in source_dir.glob("*.md"):
        prefix = page_path.stem[:10]
        entities = prefix_entities.get(prefix, [])
        if not entities:
            result["skipped"] += 1
            continue

        linkable = [n for n in entities if slugify(n) in existing_slugs]
        if not linkable:
            result["skipped"] += 1
            continue

        try:
            text = page_path.read_text(encoding="utf-8")
            if "## Key Concepts" in text:
                result["skipped"] += 1
                continue

            section = "\n\n## Key Concepts\n\n"
            for name in sorted(linkable)[:20]:
                section += f"- [[entities/{slugify(name)}|{name}]]\n"

            timeline = "## Development Timeline"
            if timeline in text:
                idx = text.index(timeline)
                new_text = text[:idx].rstrip() + section + "\n" + text[idx:]
            else:
                new_text = text.rstrip() + section

            if not dry_run:
                page_path.write_text(new_text, encoding="utf-8")
            result["updated"] += 1
        except Exception as exc:
            result["errors"].append(f"{page_path.stem}: {exc}")

    if not dry_run and result["updated"]:
        invalidate_wiki_target_cache()
    logger.info("wiki_link_source_entities_complete", dry_run=dry_run, **{k: v for k, v in result.items() if k != "errors"})
    return result


def auto_file_skill_output(skill_name: str, user_input: str, response_text: str) -> None:
    """Parse skill output and route to appropriate wiki page update.

    Called from dispatcher's _fire_wiki_filing for executor-routed skills.
    """
    try:
        from reading_app.db import ensure_pool
        ensure_pool()

        if skill_name == "synthesis":
            # Extract topic from user input
            topic = re.sub(r"^/synthesis\s+", "", user_input).strip()
            slug = slugify(topic)
            # Attempt to find theme_ids
            theme_ids = extract_theme_ids_from_text(topic)
            create_synthesis_page(slug, response_text, theme_ids, executor=None)

        elif skill_name == "contradictions":
            _file_contradictions_output(user_input, response_text)

        elif skill_name == "bottlenecks":
            _file_bottlenecks_output(user_input, response_text)

    except Exception:
        logger.debug("wiki_auto_file_failed", skill_name=skill_name, exc_info=True)


def populate_overview() -> dict:
    """Fill the four data sections in wiki/overview.md from existing wiki pages.

    Reads directly from wiki files (no DB dependency). Sections:
    - Meta-Themes: level-0 themes with child theme links
    - Active Bottlenecks: bottleneck bullets extracted from theme pages
    - Recent Breakthroughs: breakthrough bullets extracted from theme pages
    - Coverage Summary: file counts by type

    Returns dict with counts for logging.
    """
    overview_path = WIKI_DIR / "overview.md"
    if not overview_path.exists():
        return {"error": "overview.md not found"}

    stats = {"meta_themes": 0, "bottlenecks": 0, "breakthroughs": 0}

    # --- Single pass over theme pages ---
    meta_themes_lines = []
    bottleneck_lines = []
    breakthrough_lines = []
    theme_dir = WIKI_DIR / "themes"
    if theme_dir.exists():
        for md in sorted(theme_dir.glob("*.md")):
            if md.name == "index.md":
                continue
            try:
                text = md.read_text(encoding="utf-8")
                fm, body = _parse_frontmatter(text)
                tid = fm.get("theme_id", md.stem)
                title = fm.get("title", md.stem)

                # Meta-themes (level-0)
                if fm.get("level") == 0:
                    children = fm.get("child_themes", [])
                    child_links = ", ".join(
                        _format_theme_ref(c)
                        for c in (children if isinstance(children, list) else [])
                    )
                    line = f"- **[[themes/{tid}|{title}]]**"
                    if child_links:
                        line += f" — {child_links}"
                    meta_themes_lines.append(line)
                    stats["meta_themes"] += 1

                # Extract bottleneck bullets
                for bullet in _extract_section_bullets(body, "## Bottlenecks"):
                    if "active" in bullet.lower() or "status: active" in bullet.lower():
                        short = _truncate_bullet(bullet, 150)
                        bottleneck_lines.append(
                            f"- [[themes/{tid}|{title}]]: {short}"
                        )
                        stats["bottlenecks"] += 1

                # Extract breakthrough bullets
                for bullet in _extract_section_bullets(body, "## Breakthroughs"):
                    if any(kw in bullet.lower() for kw in ("major", "paradigm", "notable")):
                        short = _truncate_bullet(bullet, 150)
                        breakthrough_lines.append(
                            f"- [[themes/{tid}|{title}]]: {short}"
                        )
                        stats["breakthroughs"] += 1
            except Exception:
                continue

    # Limit to top entries
    bottleneck_lines = bottleneck_lines[:20]
    breakthrough_lines = breakthrough_lines[:15]

    # --- Coverage summary ---
    def _content_page_count(directory: Path) -> int:
        """Count .md files excluding index.md."""
        if not directory.exists():
            return 0
        return sum(1 for f in directory.glob("*.md") if f.name != "index.md")

    theme_count = _content_page_count(theme_dir)
    entity_dir = WIKI_DIR / "entities"
    entity_count = _content_page_count(entity_dir)
    source_dir = WIKI_DIR / "sources"
    source_count = _content_page_count(source_dir)
    synthesis_dir = WIKI_DIR / "syntheses"
    synthesis_count = _content_page_count(synthesis_dir)
    belief_dir = WIKI_DIR / "beliefs"
    belief_count = _content_page_count(belief_dir)

    coverage_lines = [
        f"| Themes | {theme_count} |",
        f"| Entities | {entity_count} |",
        f"| Sources | {source_count} |",
        f"| Syntheses | {synthesis_count} |",
        f"| Beliefs | {belief_count} |",
    ]

    # --- Write overview ---
    text = overview_path.read_text(encoding="utf-8")
    fm, body = _parse_frontmatter(text)

    meta_content = "\n".join(meta_themes_lines) if meta_themes_lines else "No level-0 themes found."
    body = _update_section(body, "## Meta-Themes", meta_content)

    bn_content = "\n".join(bottleneck_lines) if bottleneck_lines else "No active bottlenecks extracted yet."
    body = _update_section(body, "## Active Bottlenecks", bn_content)

    bt_content = "\n".join(breakthrough_lines) if breakthrough_lines else "No major breakthroughs extracted yet."
    body = _update_section(body, "## Recent Breakthroughs", bt_content)

    cov_header = "| Category | Count |\n|----------|------:|\n"
    cov_content = cov_header + "\n".join(coverage_lines)
    body = _update_section(body, "## Coverage Summary", cov_content)

    fm["updated"] = date.today().isoformat()
    content = _render_frontmatter(fm) + "\n" + body.strip() + "\n"
    overview_path.write_text(content, encoding="utf-8")

    logger.info("wiki_overview_populated", **stats,
                themes=theme_count, entities=entity_count, sources=source_count)
    return stats


def _extract_section_bullets(body: str, section_header: str) -> list[str]:
    """Extract bullet lines from a section."""
    idx = body.find(section_header)
    if idx == -1:
        return []
    after = body[idx + len(section_header):]
    next_section = re.search(r"\n## ", after)
    section_text = after[:next_section.start()] if next_section else after
    return [
        line.strip() for line in section_text.split("\n")
        if line.strip().startswith("- ")
    ]


def _truncate_bullet(bullet: str, max_len: int) -> str:
    """Truncate bullet text, stripping the leading '- '."""
    text = bullet.strip()
    if text.startswith("- "):
        text = text[2:]
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text


# ---------------------------------------------------------------------------
# Public API — Skill wiki-write functions (Phase 5)
# ---------------------------------------------------------------------------


def file_enrichment_to_wiki(parsed: dict) -> dict:
    """Update theme wiki pages after /enrich persists entries. Best-effort."""
    stats: dict[str, int] = {"themes_updated": 0, "entries_added": 0, "errors": 0}

    # Group entries by theme_id for single read-modify-write per page
    theme_entries: dict[str, dict] = {}
    for cap in parsed.get("new_capabilities", []):
        tid = cap.get("theme_id")
        if tid:
            theme_entries.setdefault(tid, {"caps": [], "lims": [], "bns": []})["caps"].append(cap)
    for lim in parsed.get("new_limitations", []):
        tid = lim.get("theme_id")
        if tid:
            theme_entries.setdefault(tid, {"caps": [], "lims": [], "bns": []})["lims"].append(lim)
    for bn in parsed.get("new_bottlenecks", []):
        tid = bn.get("theme_id")
        if tid:
            theme_entries.setdefault(tid, {"caps": [], "lims": [], "bns": []})["bns"].append(bn)

    for tid, entries in theme_entries.items():
        try:
            result = _read_page(WIKI_DIR / "themes" / f"{tid}.md")
            if result is None:
                continue
            fm, body = result

            for cap in entries["caps"]:
                desc = cap.get("description", "")[:200]
                mat = cap.get("maturity", "emerging")
                bullet = f"- **{desc}** ({mat}) *(user enrichment)*"
                body = _append_to_section(body, "## Capabilities", bullet, dedup_key=desc[:40])
                stats["entries_added"] += 1

            for lim in entries["lims"]:
                desc = lim.get("description", "")[:200]
                sev = lim.get("severity", "moderate")
                traj = lim.get("trajectory", "unclear")
                bullet = f"- **{desc}** (severity: {sev}, trajectory: {traj}) *(user enrichment)*"
                body = _append_to_section(body, "## Limitations", bullet, dedup_key=desc[:40])
                stats["entries_added"] += 1

            for bn in entries["bns"]:
                desc = bn.get("description", "")[:200]
                horizon = bn.get("resolution_horizon", "unknown")
                bullet = f"- **{desc}** (status: active) — Resolution horizon: {horizon}. *(user enrichment)*"
                body = _append_to_section(body, "## Bottlenecks", bullet, dedup_key=desc[:40])
                stats["entries_added"] += 1

            _write_page(WIKI_DIR / "themes" / f"{tid}.md", fm, body, "theme")
            stats["themes_updated"] += 1
        except Exception:
            logger.debug("wiki_enrich_theme_failed", theme_id=tid, exc_info=True)
            stats["errors"] += 1

    # Cross-theme implications (touch 2 theme pages each)
    for imp in parsed.get("new_implications", []):
        src = imp.get("source_theme_id")
        tgt = imp.get("target_theme_id")
        desc = imp.get("implication", "")[:300]
        if not src or not tgt or not desc:
            continue
        for tid, other, arrow in [(src, tgt, "→"), (tgt, src, "←")]:
            try:
                result = _read_page(WIKI_DIR / "themes" / f"{tid}.md")
                if result is None:
                    continue
                fm, body = result
                bullet = f"- {arrow} {_format_theme_ref(other)}: {desc} *(user enrichment)*"
                body = _append_to_section(body, "## Cross-Theme Implications", bullet, dedup_key=desc[:40])
                _write_page(WIKI_DIR / "themes" / f"{tid}.md", fm, body, "theme")
            except Exception:
                logger.debug("wiki_enrich_impl_failed", theme_id=tid, exc_info=True)
                stats["errors"] += 1
        stats["entries_added"] += 1

    return stats


def file_challenge_to_wiki(
    entity_type: str,
    entity_id: str,
    entity: dict,
    verdict: str,
    applied_changes: list[str],
    challenge_id: str,
) -> None:
    """Update theme wiki page after /challenge landscape resolves. Best-effort."""
    theme_id = entity.get("theme_id")
    if not theme_id:
        return

    result = _read_page(WIKI_DIR / "themes" / f"{theme_id}.md")
    if result is None:
        return

    fm, body = result
    today = date.today().isoformat()

    # 1. If fields were updated, modify the entity's bullet on the theme page
    if verdict == "system_updated" and applied_changes:
        section_map = {
            "capability": "## Capabilities",
            "limitation": "## Limitations",
            "bottleneck": "## Bottlenecks",
            "breakthrough": "## Breakthroughs",
            "anticipation": "## Anticipations",
        }
        section = section_map.get(entity_type)
        entity_desc = entity.get("description", entity.get("prediction", ""))[:40]
        if section and entity_desc:
            escaped = re.escape(entity_desc)
            for change in applied_changes:
                match = re.match(r"(\w+): .+ → (.+)", change)
                if match:
                    field, new_val = match.group(1), match.group(2)
                    if field in ("maturity", "severity", "trajectory", "status",
                                 "resolution_horizon", "significance", "confidence"):
                        pattern = rf"({escaped}.*?){field}: [\w.]+"
                        replacement = rf"\g<1>{field}: {new_val}"
                        body = _replace_in_section(body, section, pattern, replacement)

    # 2. Add timeline entry recording the challenge
    changes_str = "; ".join(c[:60] for c in applied_changes[:3]) if applied_changes else "no changes"
    timeline_entry = (
        f"- **{today}** — Challenge ({verdict}): {entity_type} "
        f"`{entity_id[:20]}…` — {changes_str}. (`{challenge_id}`)"
    )
    body = _append_to_section(body, "## Development Timeline", timeline_entry)

    _write_page(WIKI_DIR / "themes" / f"{theme_id}.md", fm, body, "theme")


def file_implications_to_wiki(structured: dict, attribution: str) -> dict:
    """Update wiki theme pages after /implications persists entries. Best-effort."""
    stats: dict[str, int] = {"pages_updated": 0, "errors": 0}
    updated_pages: set[str] = set()

    attr_tag = " *(user implication)*" if "user" in attribution else ""

    for imp in structured.get("cross_theme_implications", []):
        src = imp.get("source_theme_id")
        tgt = imp.get("target_theme_id")
        desc = imp.get("implication", "")[:300]
        if not src or not tgt or not desc:
            continue
        for tid, other, arrow in [(src, tgt, "→"), (tgt, src, "←")]:
            try:
                result = _read_page(WIKI_DIR / "themes" / f"{tid}.md")
                if result is None:
                    continue
                fm, body = result
                bullet = f"- {arrow} {_format_theme_ref(other)}: {desc}{attr_tag}"
                body = _append_to_section(body, "## Cross-Theme Implications", bullet, dedup_key=desc[:40])
                _write_page(WIKI_DIR / "themes" / f"{tid}.md", fm, body, "theme")
                updated_pages.add(tid)
            except Exception:
                logger.debug("wiki_impl_failed", theme_id=tid, exc_info=True)
                stats["errors"] += 1

    for ant in structured.get("new_anticipations", []):
        tid = ant.get("theme_id")
        pred = ant.get("prediction", "")[:200]
        conf = ant.get("confidence", "?")
        if not tid or not pred:
            continue
        try:
            result = _read_page(WIKI_DIR / "themes" / f"{tid}.md")
            if result is None:
                continue
            fm, body = result
            bullet = f"- **{pred}** (confidence: {conf}, status: open)"
            body = _append_to_section(body, "## Anticipations", bullet, dedup_key=pred[:40])
            _write_page(WIKI_DIR / "themes" / f"{tid}.md", fm, body, "theme")
            updated_pages.add(tid)
        except Exception:
            logger.debug("wiki_impl_ant_failed", theme_id=tid, exc_info=True)
            stats["errors"] += 1

    stats["pages_updated"] = len(updated_pages)
    return stats


def file_belief_to_wiki(
    belief_id: str,
    claim: str,
    confidence: float,
    belief_type: str | None = None,
    domain_theme_id: str | None = None,
    evidence_for: list | None = None,
    evidence_against: list | None = None,
    *,
    is_update: bool = False,
    trigger: str = "",
) -> None:
    """Create or update a belief wiki page. Best-effort."""
    slug = slugify(claim)
    page_path = WIKI_DIR / "beliefs" / f"{slug}.md"
    today = date.today().isoformat()

    if is_update and page_path.exists():
        result = _read_page(page_path)
        if result is None:
            return
        fm, body = result
        fm["confidence"] = confidence
        row = f"| {today} | {confidence:.2f} | {trigger or 'manual update'} | manual |"
        body = _append_to_section(body, "## Confidence History", row)
        body = re.sub(r"(confidence) [\d.]+", rf"\g<1> {confidence:.2f}", body, count=1)
        _write_page(page_path, fm, body, "belief")
        return

    if page_path.exists():
        return  # Don't overwrite on create

    # Create new belief page
    (WIKI_DIR / "beliefs").mkdir(parents=True, exist_ok=True)

    fm = {
        "type": "belief",
        "title": claim[:120],
        "belief_id": belief_id,
        "confidence": confidence,
        "belief_type": belief_type or "position",
        "theme_ids": [domain_theme_id] if domain_theme_id else [],
        "created": today,
        "updated": today,
        "tags": [],
    }

    ev_for_text = "\n".join(
        f"- [{e.get('source_id', '?')}] {e.get('claim_text', '')[:150]}"
        for e in (evidence_for or [])[:10]
    ) or "No supporting evidence found yet."

    ev_against_text = "\n".join(
        f"- [{e.get('source_id', '?')}] {e.get('claim_text', '')[:150]}"
        for e in (evidence_against or [])[:10]
    ) or "No contradicting evidence found yet."

    theme_link = _format_theme_ref(domain_theme_id) if domain_theme_id else "(no theme linked)"

    body = f"""# {claim[:120]}

> {belief_type or 'position'} belief — confidence {confidence:.2f}

## Position

{claim}

## Evidence For

{ev_for_text}

## Evidence Against

{ev_against_text}

## Confidence History

| Date | Confidence | Trigger | Type |
|------|-----------|---------|------|
| {today} | {confidence:.2f} | Initial creation | manual |

## Challenge History

No challenges recorded yet.

## Landscape Links

Theme: {theme_link}"""

    page_path.write_text(
        _render_frontmatter(fm) + "\n" + body.strip() + "\n", encoding="utf-8",
    )
    wiki_index.on_page_created(page_path, "belief", fm)


def file_anticipation_to_wiki(
    theme_id: str,
    prediction: str,
    confidence: float | str,
    new_status: str | None = None,
    old_status: str | None = None,
    *,
    is_new: bool = False,
) -> None:
    """Update or add anticipation on theme wiki page. Best-effort."""
    result = _read_page(WIKI_DIR / "themes" / f"{theme_id}.md")
    if result is None:
        return

    fm, body = result

    if is_new:
        bullet = f"- **{prediction[:200]}** (confidence: {confidence}, status: open)"
        body = _append_to_section(body, "## Anticipations", bullet, dedup_key=prediction[:40])
    elif new_status and old_status:
        escaped_pred = re.escape(prediction[:40])
        pattern = rf"(- \*\*{escaped_pred}.*?status: ){re.escape(old_status)}(\))"
        replacement = rf"\g<1>{new_status}\2"
        new_body = _replace_in_section(body, "## Anticipations", pattern, replacement)
        if new_body == body:
            # Not found — append with resolved status
            bullet = f"- **{prediction[:200]}** (confidence: {confidence}, status: {new_status})"
            body = _append_to_section(body, "## Anticipations", bullet, dedup_key=prediction[:40])
        else:
            body = new_body
    else:
        return  # No changes to make

    _write_page(WIKI_DIR / "themes" / f"{theme_id}.md", fm, body, "theme")


def file_idea_to_wiki(
    idea_id: str,
    idea_text: str,
    idea_type: str | None,
    rating: int,
    theme_ids: list[str],
) -> None:
    """Promote highly-rated idea to theme page Research Opportunities. Best-effort."""
    for tid in theme_ids[:3]:
        try:
            result = _read_page(WIKI_DIR / "themes" / f"{tid}.md")
            if result is None:
                continue
            fm, body = result
            bullet = (
                f"- **{idea_text[:120]}** "
                f"(rating: {rating}/5, type: {idea_type or '?'}) "
                f"— ID: `{idea_id}`"
            )
            body = _append_to_section(
                body, "## Research Opportunities", bullet, dedup_key=idea_id,
            )
            _write_page(WIKI_DIR / "themes" / f"{tid}.md", fm, body, "theme")
        except Exception:
            logger.debug("wiki_idea_promote_failed", theme_id=tid, exc_info=True)


# ---------------------------------------------------------------------------
# Internal — Frontmatter helpers
# ---------------------------------------------------------------------------

# Reuse from wiki_index to avoid duplicate definition
_parse_frontmatter = wiki_index._parse_frontmatter


def _render_frontmatter(meta: dict) -> str:
    """Render a dict as YAML frontmatter block."""
    import yaml
    # Use block style for lists, default flow for short lists
    yaml_str = yaml.dump(
        meta,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
    ).rstrip()
    return f"---\n{yaml_str}\n---"


# ---------------------------------------------------------------------------
# Internal — Staleness
# ---------------------------------------------------------------------------


def _compute_staleness(sources_since_update: int, updated_date: date) -> float:
    """Compute page staleness metric.

    staleness = min(1.0, (sources_since_update * 0.15) + (days_since_update / 60))
    """
    days = (date.today() - updated_date).days
    return min(1.0, (sources_since_update * 0.15) + (days / 60))


def _increment_theme_staleness(source_id: str, theme_ids: list[str] | None = None) -> None:
    """Increment sources_since_update for themes affected by a source deletion.

    Args:
        source_id: Source identifier (used for logging).
        theme_ids: Pre-fetched theme IDs. If None, attempts DB lookup
            (may return empty if source_themes already cascade-deleted).
    """
    try:
        if theme_ids is None:
            from reading_app.db import get_conn

            with get_conn() as conn:
                theme_ids = [
                    r["theme_id"] for r in conn.execute(
                        "SELECT theme_id FROM source_themes WHERE source_id = %s",
                        (source_id,),
                    ).fetchall()
                ]

        for tid in theme_ids:
            page_path = WIKI_DIR / "themes" / f"{tid}.md"
            if not page_path.exists():
                continue
            try:
                text = page_path.read_text(encoding="utf-8")
                fm, body = _parse_frontmatter(text)
                fm["sources_since_update"] = fm.get("sources_since_update", 0) + 1
                updated_str = fm.get("updated", date.today().isoformat())
                try:
                    updated_dt = date.fromisoformat(str(updated_str))
                except Exception:
                    updated_dt = date.today()
                fm["staleness"] = _compute_staleness(fm["sources_since_update"], updated_dt)
                content = _render_frontmatter(fm) + "\n" + body
                page_path.write_text(content, encoding="utf-8")
            except Exception:
                logger.debug("wiki_increment_staleness_failed", theme_id=tid, exc_info=True)
    except Exception:
        logger.debug("wiki_increment_theme_staleness_failed", source_id=source_id, exc_info=True)


def _propagate_to_parent_themes(theme_ids: list[str], updated_theme_ids: list[str]) -> list[str]:
    """Increment staleness on parent themes not directly updated."""
    patched = []
    try:
        from reading_app.db import get_parent_theme

        seen_parents = set()
        for tid in updated_theme_ids:
            parent = get_parent_theme(tid)
            if not parent:
                continue
            parent_id = parent["id"]
            if parent_id in seen_parents or parent_id in theme_ids:
                continue  # Already directly updated or already patched
            seen_parents.add(parent_id)
            page_path = WIKI_DIR / "themes" / f"{parent_id}.md"
            if not page_path.exists():
                continue
            try:
                text = page_path.read_text(encoding="utf-8")
                fm, body = _parse_frontmatter(text)
                fm["sources_since_update"] = fm.get("sources_since_update", 0) + 1
                updated_str = fm.get("updated", date.today().isoformat())
                try:
                    updated_dt = date.fromisoformat(str(updated_str))
                except Exception:
                    updated_dt = date.today()
                fm["staleness"] = _compute_staleness(fm["sources_since_update"], updated_dt)
                content = _render_frontmatter(fm) + "\n" + body
                page_path.write_text(content, encoding="utf-8")
                patched.append(parent_id)
            except Exception:
                logger.debug("wiki_propagate_parent_failed", parent_id=parent_id, exc_info=True)
    except Exception:
        logger.debug("wiki_propagate_to_parents_failed", exc_info=True)
    return patched


# ---------------------------------------------------------------------------
# Internal — Timeline operations
# ---------------------------------------------------------------------------


def _insert_timeline_entry(body: str, entry: str, published_at: date) -> str:
    """Insert a timeline entry at the correct reverse-chronological position.

    Finds '## Development Timeline' section, inserts entry by date.
    Deterministic string operation, no LLM.
    """
    timeline_header = "## Development Timeline"
    idx = body.find(timeline_header)
    if idx == -1:
        # Append timeline section at end
        body = body.rstrip() + f"\n\n{timeline_header}\n{_TIMELINE_COMMENT}\n{entry}\n"
        return body

    # Find the lines in the timeline section
    before = body[:idx]
    after_header = body[idx:]

    lines = after_header.split("\n")
    header_line = lines[0]  # "## Development Timeline"
    rest = lines[1:]

    # Find where timeline entries are (lines starting with "- **")
    timeline_entries = []
    non_entry_prefix = []
    non_entry_suffix = []
    in_entries = False
    entry_done = False

    for line in rest:
        if line.strip().startswith("- **") and not entry_done:
            in_entries = True
            timeline_entries.append(line)
        elif in_entries and not line.strip().startswith("- **"):
            if line.strip() == "" and timeline_entries:
                # Could be blank line between entries, or end of entries
                # Check if next non-blank starts with "- **"
                timeline_entries.append(line)
            elif line.strip().startswith("##"):
                entry_done = True
                non_entry_suffix.append(line)
            elif line.strip().startswith("<!--"):
                non_entry_prefix.append(line) if not timeline_entries else timeline_entries.append(line)
            else:
                entry_done = True
                non_entry_suffix.append(line)
        elif not in_entries and not entry_done:
            non_entry_prefix.append(line)
        else:
            non_entry_suffix.append(line)

    # Filter out blank entries
    timeline_entries = [e for e in timeline_entries if e.strip()]

    # Parse dates from existing entries and find insertion point
    inserted = False
    new_entries = []
    for existing in timeline_entries:
        existing_date = _extract_date_from_entry(existing)
        if not inserted and existing_date and published_at >= existing_date:
            new_entries.append(entry)
            inserted = True
        new_entries.append(existing)

    if not inserted:
        new_entries.append(entry)

    # Reassemble
    reassembled = [header_line] + non_entry_prefix + new_entries + non_entry_suffix
    return before + "\n".join(reassembled)


_TIMELINE_COMMENT = "<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->"


def _extract_date_from_entry(entry: str) -> date | None:
    """Extract date from a timeline entry like '- **2026-04-07** — ...'."""
    m = re.search(r"\*\*(\d{4}-\d{2}-\d{2})\*\*", entry)
    if m:
        try:
            return date.fromisoformat(m.group(1))
        except ValueError:
            return None
    return None


def _split_timeline(body: str) -> tuple[str, str]:
    """Split body into (body_without_timeline, timeline_section)."""
    timeline_header = "## Development Timeline"
    idx = body.find(timeline_header)
    if idx == -1:
        return body, ""

    # Find next ## heading after timeline
    after = body[idx + len(timeline_header):]
    next_section = re.search(r"\n## ", after)
    if next_section:
        timeline_end = idx + len(timeline_header) + next_section.start()
        return body[:idx].rstrip(), body[idx:timeline_end]
    else:
        return body[:idx].rstrip(), body[idx:]


def _build_timeline_summary(title: str, claims: list[dict], signals: dict) -> str:
    """Build a one-line summary for a timeline entry from source data."""
    parts = []
    if signals:
        caps = signals.get("capabilities", [])
        lims = signals.get("limitations", [])
        bts = signals.get("breakthroughs", [])
        if bts:
            parts.append(f"Breakthrough: {bts[0].get('description', '')[:80]}")
        elif caps:
            parts.append(f"New capability: {caps[0].get('description', '')[:80]}")
        elif lims:
            parts.append(f"Limitation identified: {lims[0].get('description', '')[:80]}")

    if not parts and claims:
        first_claim = claims[0].get("claim_text", "")[:100]
        parts.append(first_claim)

    if not parts:
        parts.append(title)

    return ". ".join(parts)


# ---------------------------------------------------------------------------
# Internal — Entity signal filtering
# ---------------------------------------------------------------------------


def _filter_signals_for_entity(signals: dict | None, entity_name: str) -> dict:
    """Filter landscape signals to those mentioning a specific entity."""
    if not signals:
        return {}
    name_lower = entity_name.lower()
    filtered = {}
    for key in ("capabilities", "limitations", "bottlenecks", "breakthroughs"):
        items = signals.get(key, [])
        matching = [item for item in items if name_lower in item.get("description", "").lower()]
        if matching:
            filtered[key] = matching
    return filtered


# ---------------------------------------------------------------------------
# Internal — Emergent connections
# ---------------------------------------------------------------------------


def _extract_emergent_connections(text: str) -> tuple[str, list[dict]]:
    """Extract ```json:emergent``` block from LLM output.

    Returns:
        (cleaned_body, list_of_connections) — body with block stripped.
    """
    import json as _json

    pattern = r"```json:emergent\s*\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return text, []

    try:
        connections = _json.loads(match.group(1).strip())
        if not isinstance(connections, list):
            connections = []
    except (ValueError, TypeError):
        connections = []

    cleaned = text[:match.start()].rstrip() + text[match.end():]
    return cleaned.strip(), connections


def _file_emergent_connections(connections: list[dict], source_id: str) -> int:
    """Persist emergent cross-theme implications discovered during wiki synthesis.

    Returns:
        Count of successfully filed connections.
    """
    from ulid import ULID

    from reading_app.db import insert_cross_theme_implication

    filed = 0
    for conn in connections:
        source_theme = conn.get("source_theme", "")
        target_theme = conn.get("target_theme", "")
        implication = conn.get("implication", "")
        confidence = conn.get("confidence", 0.5)
        if not (source_theme and target_theme and implication):
            continue
        try:
            insert_cross_theme_implication(
                id=str(ULID()),
                source_theme_id=source_theme,
                target_theme_id=target_theme,
                trigger_type="wiki_synthesis",
                trigger_id=source_id,
                implication=implication,
                confidence=confidence,
                evidence_sources=[source_id],
                attribution="wiki_emergent",
            )
            filed += 1
        except Exception:
            logger.debug("wiki_file_emergent_connection_failed", exc_info=True)
    return filed


# ---------------------------------------------------------------------------
# Internal — Slug & utility
# ---------------------------------------------------------------------------


def slugify(title: str) -> str:
    """Convert title to URL-safe slug."""
    s = title.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")[:80]


_wiki_target_cache: dict[str, str] | None = None
_wiki_target_cache_time: float = 0.0
_WIKI_TARGET_CACHE_TTL = 30.0  # seconds


def _build_wiki_target_lookup() -> dict[str, str]:
    """Build lowered-path → canonical-path lookup from existing wiki files.

    Used by _normalize_wikilinks to fix LLM-generated link paths.
    Cached for 30s to avoid redundant filesystem scans during batch operations.
    """
    import time as _time

    global _wiki_target_cache, _wiki_target_cache_time
    now = _time.monotonic()
    if _wiki_target_cache is not None and (now - _wiki_target_cache_time) < _WIKI_TARGET_CACHE_TTL:
        return _wiki_target_cache

    targets: dict[str, str] = {}
    for subdir in ("themes", "entities", "sources", "syntheses", "beliefs", "questions"):
        d = WIKI_DIR / subdir
        if not d.exists():
            continue
        for md in d.glob("*.md"):
            if md.name in ("index.md", "CONVENTIONS.md", "overview.md"):
                continue
            canonical = f"{subdir}/{md.stem}"
            targets[canonical.lower()] = canonical
            # For sources, also index by source_id prefix for fuzzy matching
            if subdir == "sources" and len(md.stem) > 10:
                sid_prefix = md.stem[:10]
                targets[f"sources/{sid_prefix}"] = canonical

    _wiki_target_cache = targets
    _wiki_target_cache_time = now
    return targets


def invalidate_wiki_target_cache() -> None:
    """Force rebuild of the wiki target lookup on next call."""
    global _wiki_target_cache
    _wiki_target_cache = None


def _normalize_wikilinks(text: str, *, strip_unresolvable: bool = True) -> str:
    """Normalize wikilinks in LLM output to match actual wiki file paths.

    Handles cases where the LLM approximates but doesn't nail the slug
    (e.g., wrong slugification, missing source_id prefix).

    Args:
        text: Text containing wikilinks.
        strip_unresolvable: If True (default), convert unresolvable wikilinks
            to plain text to prevent broken links from accumulating.
            If False, leave unresolvable links as-is (legacy behavior).
    """
    try:
        targets = _build_wiki_target_lookup()
    except Exception:
        return text

    if not targets:
        return text

    def _replace(m: re.Match) -> str:
        target = m.group(1).strip()
        display = m.group(2)

        # Strip .md extension if present
        if target.endswith(".md"):
            target = target[:-3]

        target_lower = target.lower()

        # Exact match
        canonical = targets.get(target_lower)
        if canonical:
            return f"[[{canonical}|{display}]]" if display else f"[[{canonical}]]"

        # For sources: try matching by source_id prefix (first 10 chars)
        if target_lower.startswith("sources/") and len(target_lower) > 18:
            stem = target_lower[8:]  # strip "sources/"
            prefix_key = f"sources/{stem[:10]}"
            canonical = targets.get(prefix_key)
            if canonical:
                return f"[[{canonical}|{display}]]" if display else f"[[{canonical}]]"

        if strip_unresolvable:
            # Convert to plain text: use display text if available, else the
            # target's last path segment as readable text
            if display:
                return display
            # Extract readable name from path: "entities/some-slug" → "some-slug"
            name_part = target.split("/")[-1] if "/" in target else target
            return name_part.replace("-", " ").replace("_", " ")

        return m.group(0)  # No match, leave as-is

    return re.sub(r"\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]", _replace, text)


def _format_source_ref(source_id: str, title: str) -> str:
    """Compute canonical wikilink string for a source."""
    return f"[[sources/{source_id[:10]}-{slugify(title)}|{title}]]"


def _format_entity_ref(name: str) -> str:
    """Compute canonical wikilink string for an entity."""
    return f"[[entities/{slugify(name)}|{name}]]"


@lru_cache(maxsize=128)
def _format_theme_ref(theme_id: str) -> str:
    """Compute canonical wikilink string for a theme, using frontmatter title."""
    try:
        page = WIKI_DIR / "themes" / f"{theme_id}.md"
        if page.exists():
            fm, _ = _parse_frontmatter(page.read_text(encoding="utf-8"))
            title = fm.get("title")
            if title:
                return f"[[themes/{theme_id}|{title}]]"
    except Exception:
        logger.debug("format_theme_ref_failed", theme_id=theme_id, exc_info=True)
    # Fallback: prettify slug
    display = theme_id.replace("-", " ").replace("_", " ").title()
    return f"[[themes/{theme_id}|{display}]]"


def _strip_llm_frontmatter(text: str) -> str:
    """Remove YAML frontmatter if the LLM included it despite instructions."""
    stripped = text.lstrip()
    if stripped.startswith("---"):
        end = stripped.find("---", 3)
        if end != -1:
            return stripped[end + 3:].lstrip("\n")
    return text


# Patterns that indicate LLM wrapper prose (meta-output about the generation
# process rather than actual page content).  Each pattern matches from the
# start of a line.
_WRAPPER_PROSE_PATTERNS = [
    re.compile(r"^Wiki page (?:generated|written|created) (?:at|to) .+$", re.MULTILINE),
    re.compile(r"^The wiki page has been (?:written|created|generated) .+$", re.MULTILINE),
    re.compile(r"^Here(?:'s| is) (?:the|a) (?:wiki page|summary).+$", re.MULTILINE),
    re.compile(r"^No em dashes used throughout.+$", re.MULTILINE),
    re.compile(r"^All sections use the Obsidian wikilink format.+$", re.MULTILINE),
    # "Written to `wiki/path/file.md`." or "Written to 'path'."
    re.compile(r"^Written to [`'].+[`']\.?\s*$", re.MULTILINE),
    # Broader "Here is the generated/updated/complete ..."
    re.compile(r"^Here is the (?:generated|updated|created|complete|new|full)\b.+$", re.MULTILINE),
    # "The page synthesizes/covers/is organised..." meta-commentary
    re.compile(r"^The page (?:synthesize|cover|is organis|is complete|is structured)\w*\b.+$", re.MULTILINE),
]

# Block that follows a "Key decisions/choices" header: the header line itself
# plus the following bulleted/numbered list.
_DECISION_BLOCK_PATTERN = re.compile(
    r"^(?:\*\*)?Key (?:structural choices|decisions) made:?\*?\*?\s*\n"
    r"(?:(?:[ \t]*[-\d.*]+[ \t]+.+\n?)+)",
    re.MULTILINE,
)

# Standalone header line (no following list matched — strip it alone)
_DECISION_HEADER_PATTERN = re.compile(
    r"^(?:\*\*)?Key (?:structural choices|decisions) made:?\*?\*?\s*$",
    re.MULTILINE,
)

# "What's in the page:" header followed by a bulleted list
_WHATS_IN_PAGE_BLOCK = re.compile(
    r"^\*\*What.s in the page:?\*\*\s*\n"
    r"(?:(?:[ \t]*[-*]+[ \t]+.+\n?)+)",
    re.MULTILINE,
)

# Meta description blocks: "**Section name**: description" paragraphs that
# describe what was written rather than being the content itself.  These appear
# after "Here's a summary" preambles.
_META_DESCRIPTION_PATTERN = re.compile(
    r"^\*\*(?:Summary paragraph|Current State|Key structural choices)\*\*:.*$",
    re.MULTILINE,
)


def _sanitize_llm_output(text: str) -> str:
    """Strip both YAML frontmatter AND LLM wrapper prose from generated output.

    Handles:
    - Accidental YAML frontmatter (``---...---``)
    - "Wiki page generated/written/created at ..." preamble lines
    - "The wiki page has been written to ..." preamble lines
    - "Key structural choices/decisions made:" + following bullet list
    - "Here's the/a wiki page/summary ..." preamble lines
    - "No em dashes used throughout..." trailing style notes
    """
    # 1. Strip accidental YAML frontmatter
    text = _strip_llm_frontmatter(text)

    # 2. Strip "Key decisions/choices made:" blocks (header + list)
    text = _DECISION_BLOCK_PATTERN.sub("", text)

    # 3. Strip standalone decision headers (if list wasn't attached)
    text = _DECISION_HEADER_PATTERN.sub("", text)

    # 3b. Strip "What's in the page" blocks (header + list)
    text = _WHATS_IN_PAGE_BLOCK.sub("", text)

    # 4. Strip individual wrapper prose lines
    for pat in _WRAPPER_PROSE_PATTERNS:
        text = pat.sub("", text)

    # 5. Strip meta-description paragraphs
    text = _META_DESCRIPTION_PATTERN.sub("", text)

    # 6. Collapse excessive blank lines (3+ → 2) and strip leading blanks
    text = re.sub(r"\n{3,}", "\n\n", text).lstrip("\n")

    # 7. Normalize wikilinks to match actual wiki file paths
    text = _normalize_wikilinks(text)

    return text


def _to_date(val: Any) -> date:
    """Convert various date representations to date object."""
    # Check datetime BEFORE date — datetime is a subclass of date
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, date):
        return val
    if isinstance(val, str):
        try:
            return date.fromisoformat(val[:10])
        except ValueError:
            return date.today()
    return date.today()


def extract_theme_ids_from_text(text: str) -> list[str]:
    """Best-effort extraction of theme_ids from natural language text."""
    try:
        from reading_app.db import get_conn

        with get_conn() as conn:
            themes = conn.execute("SELECT id FROM themes").fetchall()
            all_ids = [r["id"] for r in themes]

        # Check if the text matches or contains a theme id
        text_lower = text.lower().replace(" ", "-")
        matches = [tid for tid in all_ids if tid in text_lower or text_lower in tid]
        return matches[:5]
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Internal — Auto-filing helpers
# ---------------------------------------------------------------------------


def _file_contradictions_output(user_input: str, response_text: str) -> None:
    """Parse /contradictions output and update relevant theme pages."""
    # Extract theme from command
    theme_match = re.search(r"/contradictions\s+(\S+)", user_input)
    if not theme_match:
        return

    theme_id = theme_match.group(1)
    page_path = WIKI_DIR / "themes" / f"{theme_id}.md"
    if not page_path.exists():
        return

    try:
        text = page_path.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(text)

        # Truncate to prevent section bloat from full LLM output
        section_content = response_text[:3000]
        if len(response_text) > 3000:
            section_content += "\n\n*... truncated — see full /contradictions output in chat*"
        body = _update_section(body, "## Contradictions", section_content)

        fm["updated"] = date.today().isoformat()
        content = _render_frontmatter(fm) + "\n" + body.strip() + "\n"
        page_path.write_text(content, encoding="utf-8")
        wiki_index.on_page_updated(page_path, "theme", fm)
    except Exception:
        logger.debug("wiki_file_contradictions_failed", theme_id=theme_id, exc_info=True)


def _file_bottlenecks_output(user_input: str, response_text: str) -> None:
    """Parse /bottlenecks output and update relevant theme pages."""
    theme_match = re.search(r"/bottlenecks\s+(\S+)", user_input)
    if not theme_match:
        return

    theme_id = theme_match.group(1)
    page_path = WIKI_DIR / "themes" / f"{theme_id}.md"
    if not page_path.exists():
        return

    try:
        text = page_path.read_text(encoding="utf-8")
        fm, body = _parse_frontmatter(text)

        section_content = response_text[:3000]
        if len(response_text) > 3000:
            section_content += "\n\n*... truncated — see full /bottlenecks output in chat*"
        body = _update_section(body, "## Bottlenecks", section_content)

        fm["updated"] = date.today().isoformat()
        content = _render_frontmatter(fm) + "\n" + body.strip() + "\n"
        page_path.write_text(content, encoding="utf-8")
        wiki_index.on_page_updated(page_path, "theme", fm)
    except Exception:
        logger.debug("wiki_file_bottlenecks_failed", theme_id=theme_id, exc_info=True)


def file_changelog_to_wiki(theme_id: str, changelog_text: str) -> dict:
    """Append changelog temporal narrative to theme page's Development Timeline.

    Does NOT reset staleness — changelog is derived content, not new source info.
    """
    page_path = WIKI_DIR / "themes" / f"{theme_id}.md"
    result = _read_page(page_path)
    if result is None:
        return {"pages_updated": 0}

    fm, body = result

    # Extract per-date change entries (lines like "- **type** ... → ...")
    entries = []
    for line in changelog_text.split("\n"):
        line_s = line.strip()
        if line_s.startswith("- **") and "→" in line_s:
            entries.append(line_s)

    if not entries:
        return {"pages_updated": 0}

    today = date.today().isoformat()
    summary = f"- **{today}** — Changelog snapshot ({len(entries)} changes):"
    for entry in entries[:10]:
        summary += f"\n  {entry}"
    if len(entries) > 10:
        summary += f"\n  *(… {len(entries) - 10} more)*"

    # Dedup by date so re-running on the same day is idempotent
    dedup_marker = f"**{today}**" + " \u2014 Changelog snapshot"
    body = _append_to_section(
        body, "## Development Timeline", summary,
        dedup_key=dedup_marker,
    )

    # Write without resetting staleness counters
    content = _render_frontmatter(fm) + "\n" + body.strip() + "\n"
    page_path.write_text(content, encoding="utf-8")
    wiki_index.on_page_updated(page_path, "theme", fm)
    return {"pages_updated": 1, "entries": len(entries)}


def _update_section(body: str, section_header: str, new_content: str) -> str:
    """Replace content of a section while preserving other sections."""
    idx = body.find(section_header)
    if idx == -1:
        # Append section before Development Timeline or at end
        timeline_idx = body.find("## Development Timeline")
        if timeline_idx != -1:
            return body[:timeline_idx].rstrip() + f"\n\n{section_header}\n\n{new_content}\n\n" + body[timeline_idx:]
        return body.rstrip() + f"\n\n{section_header}\n\n{new_content}\n"

    # Find next section
    after = body[idx + len(section_header):]
    next_section = re.search(r"\n## ", after)
    if next_section:
        section_end = idx + len(section_header) + next_section.start()
        return body[:idx] + section_header + "\n\n" + new_content + "\n" + body[section_end:]
    else:
        return body[:idx] + section_header + "\n\n" + new_content + "\n"


# ---------------------------------------------------------------------------
# Internal — Page read/write & section surgery helpers
# ---------------------------------------------------------------------------


def _read_page(page_path: Path) -> tuple[dict, str] | None:
    """Read wiki page, parse frontmatter. Returns (fm, body) or None if missing."""
    if not page_path.exists():
        return None
    text = page_path.read_text(encoding="utf-8")
    fm, body = _parse_frontmatter(text)
    return fm, body


def _write_page(page_path: Path, fm: dict, body: str, page_type: str) -> None:
    """Write page with updated frontmatter fields. Single write per page."""
    fm["updated"] = date.today().isoformat()
    fm["sources_since_update"] = 0
    fm["update_count"] = fm.get("update_count", 0) + 1
    fm["staleness"] = 0.0
    content = _render_frontmatter(fm) + "\n" + body.strip() + "\n"
    page_path.write_text(content, encoding="utf-8")
    wiki_index.on_page_updated(page_path, page_type, fm)


def _patch_frontmatter(page_path: Path, updates: dict) -> bool:
    """Update specific frontmatter fields without resetting staleness counters."""
    result = _read_page(page_path)
    if result is None:
        return False
    fm, body = result
    fm.update(updates)
    page_path.write_text(_render_frontmatter(fm) + "\n" + body.strip() + "\n", encoding="utf-8")
    return True


def _append_to_section(
    body: str, section_header: str, new_entry: str, dedup_key: str | None = None,
) -> str:
    """Append new_entry at end of section. Dedup if key found in section text."""
    idx = body.find(section_header)
    if idx == -1:
        # Create section before Development Timeline or at end
        timeline_idx = body.find("## Development Timeline")
        if timeline_idx != -1:
            return (
                body[:timeline_idx].rstrip()
                + f"\n\n{section_header}\n\n{new_entry}\n\n"
                + body[timeline_idx:]
            )
        return body.rstrip() + f"\n\n{section_header}\n\n{new_entry}\n"

    # Find section boundaries
    after = body[idx + len(section_header):]
    next_section = re.search(r"\n## ", after)
    if next_section:
        section_end = idx + len(section_header) + next_section.start()
        section_text = body[idx:section_end]
    else:
        section_end = len(body)
        section_text = body[idx:]

    # Dedup check
    if dedup_key and dedup_key.lower() in section_text.lower():
        return body

    # Append entry at end of section
    insert_pos = section_end
    return body[:insert_pos].rstrip() + "\n" + new_entry + "\n" + body[insert_pos:]


def _replace_in_section(
    body: str, section_header: str, pattern: str, replacement: str,
) -> str:
    """Regex replace within section boundaries only. Returns body unchanged if not found."""
    idx = body.find(section_header)
    if idx == -1:
        return body

    after = body[idx + len(section_header):]
    next_section = re.search(r"\n## ", after)
    if next_section:
        section_end = idx + len(section_header) + next_section.start()
    else:
        section_end = len(body)

    section_text = body[idx:section_end]
    new_section, count = re.subn(pattern, replacement, section_text, count=1)
    if count == 0:
        return body
    return body[:idx] + new_section + body[section_end:]


# ---------------------------------------------------------------------------
# Internal — LLM prompt builders
# ---------------------------------------------------------------------------


def _build_theme_fallback(theme_data: dict) -> str:
    """Fallback body for theme page if LLM fails or times out."""
    theme = theme_data.get("theme", {})
    name = theme.get("name", theme.get("id", "Unknown"))
    state_summary = theme.get("state_summary", "")
    edges = theme_data.get("theme_edges", {})

    lines = [f"# {name}", ""]

    if edges.get("parent_id"):
        lines.append(f"**Parent:** {_format_theme_ref(edges['parent_id'])}")
    children = edges.get("child_ids", [])
    if children:
        child_links = ", ".join(_format_theme_ref(c) for c in children)
        lines.append(f"**Sub-themes:** {child_links}")
    lines.append("")

    lines.extend(["## Current State", ""])
    if state_summary:
        lines.extend([state_summary, ""])
    else:
        lines.extend(["No state summary available yet.", ""])

    for section, key in [("Capabilities", "capabilities"), ("Limitations", "limitations"),
                         ("Bottlenecks", "bottlenecks"), ("Breakthroughs", "breakthroughs")]:
        items = theme_data.get(key, [])
        lines.extend([f"## {section}", ""])
        if items:
            for item in items:
                lines.append(f"- {item.get('description', '')[:300]}")
            lines.append("")

    ants = theme_data.get("anticipations", [])
    lines.extend(["## Anticipations", ""])
    if ants:
        for a in ants:
            lines.append(f"- {a.get('prediction', '')} (confidence: {a.get('confidence', 0)}, status: {a.get('status', 'open')})")
        lines.append("")

    impls = theme_data.get("cross_theme_implications", [])
    lines.extend(["## Cross-Theme Implications", ""])
    if impls:
        for imp in impls:
            target = imp.get("target_theme_id", imp.get("theme_id", ""))
            lines.append(f"- → {_format_theme_ref(target)}: {imp.get('implication', imp.get('description', ''))}")
        lines.append("")

    lines.extend(["## Contradictions", "", "## Research Opportunities", ""])
    lines.extend([
        "## Development Timeline",
        "<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->",
        f"- **{date.today().isoformat()}** — Wiki page created. Theme has {theme_data.get('source_count', 0)} sources.",
    ])

    return "\n".join(lines)


def _build_theme_create_prompt(theme_data: dict, source_refs: list[tuple[str, str]] | None = None) -> str:
    """Build prompt for initial theme page generation.

    Args:
        theme_data: Full theme state dict.
        source_refs: Optional list of (source_id, title) for sources in this theme.
    """
    theme = theme_data.get("theme", {})
    name = theme.get("name", theme.get("id", "Unknown"))
    state_summary = theme.get("state_summary", "")

    caps = theme_data.get("capabilities", [])
    lims = theme_data.get("limitations", [])
    bots = theme_data.get("bottlenecks", [])
    bts = theme_data.get("breakthroughs", [])
    ants = theme_data.get("anticipations", [])
    impls = theme_data.get("cross_theme_implications", [])
    edges = theme_data.get("theme_edges", {})

    parts = [
        f"Generate a wiki page for the AI research theme: **{name}**",
        "",
        "Follow this exact template structure (do NOT include frontmatter — it's added separately):",
        "",
        f"# {name}",
        "",
        "> One-paragraph summary of this theme's current state and trajectory.",
        "",
    ]

    if edges.get("parent_id"):
        parts.append(f"**Parent:** {_format_theme_ref(edges['parent_id'])}")
    children = edges.get("child_ids", [])
    if children:
        child_links = ", ".join(_format_theme_ref(c) for c in children)
        parts.append(f"**Sub-themes:** {child_links}")

    parts.extend([
        "",
        "## Current State",
        "(Write a temporal narrative synthesis based on the data below)",
        "",
        "## Capabilities",
        "## Limitations",
        "## Bottlenecks",
        "## Breakthroughs",
        "## Anticipations",
        "## Cross-Theme Implications",
        "## Contradictions",
        "## Research Opportunities",
        "## Development Timeline",
        "<!-- APPEND-ONLY: New entries inserted by published_at date (reverse chronological). Do not rewrite existing entries. -->",
        f"- **{date.today().isoformat()}** — Wiki page created. Theme has {theme_data.get('source_count', 0)} sources.",
        "",
        "---",
        "DATA TO USE:",
        "",
    ])

    if state_summary:
        parts.append(f"State summary:\n{state_summary}\n")

    if caps:
        parts.append("Capabilities:")
        for c in caps:
            parts.append(f"  - {c.get('description', '')[:120]} (maturity: {c.get('maturity', 'unknown')})")

    if lims:
        parts.append("\nLimitations:")
        for l in lims:
            parts.append(f"  - {l.get('description', '')[:120]} (severity: {l.get('severity', 'unknown')}, trajectory: {l.get('trajectory', 'unknown')}, type: {l.get('signal_type', '')})")

    if bots:
        parts.append("\nBottlenecks:")
        for b in bots:
            parts.append(f"  - {b.get('description', '')[:120]} (status: {b.get('status', 'active')}, blocking: {b.get('blocking_what', '')}, horizon: {b.get('resolution_horizon', '')})")

    if bts:
        parts.append("\nBreakthroughs:")
        for b in bts:
            parts.append(f"  - {b.get('description', '')[:120]} (significance: {b.get('significance', 'incremental')}, prior belief: {b.get('what_was_believed_before', '')})")

    if ants:
        parts.append("\nAnticipations:")
        for a in ants:
            parts.append(f"  - {a.get('prediction', '')} (confidence: {a.get('confidence', 0)}, status: {a.get('status', 'open')})")

    if impls:
        parts.append("\nCross-theme implications:")
        for imp in impls:
            target = imp.get("target_theme_id", imp.get("theme_id", ""))
            parts.append(f"  - → {target}: {imp.get('implication', imp.get('description', ''))}")

    # Canonical wikilink references for sources
    if source_refs:
        parts.extend(["", "CANONICAL SOURCE WIKILINKS (use these exact links):"])
        for sid, stitle in source_refs:
            parts.append(f"  - [[sources/{sid[:10]}-{slugify(stitle)}|{stitle}]]")

    # Canonical theme wikilinks — parent, children, and cross-theme implication targets
    theme_targets: dict[str, str] = {}  # theme_id → display name
    if edges.get("parent_id"):
        theme_targets[edges["parent_id"]] = edges["parent_id"]
    for c in children:
        theme_targets[c] = c
    for imp in impls:
        target = imp.get("target_theme_id", imp.get("theme_id", ""))
        if target:
            theme_targets[target] = target
    if theme_targets:
        parts.extend(["", "CANONICAL THEME WIKILINKS (use these exact links for cross-references):"])
        for tid, tname in sorted(theme_targets.items()):
            parts.append(f"  - [[themes/{tid}|{tname}]]")

    parts.extend([
        "",
        "IMPORTANT INSTRUCTIONS:",
        "- Use ONLY the canonical wikilinks listed above — do not invent link targets",
        "- If you need to reference a theme or source not listed above, use plain text instead of a wikilink",
        "- Write as temporal narrative, not static inventory",
        "- Include ALL provided data in appropriate sections",
        "- Do NOT include frontmatter (--- block) — it's added separately",
        "- Preserve the exact section headers listed above",
    ])

    return "\n".join(parts)


def _build_theme_update_prompt(
    current_body: str,
    source_data: dict,
    source_ref: str | None = None,
    entity_refs: list[tuple[str, str]] | None = None,
) -> str:
    """Build prompt for incremental theme page update.

    Args:
        current_body: Current page body (without timeline).
        source_data: New source data dict.
        source_ref: Pre-computed canonical wikilink for this source.
        entity_refs: Optional list of (name, slug) for entities in this source.
    """
    source_id = source_data.get("source_id", "")
    title = source_data.get("title", "Untitled")
    claims = source_data.get("claims", [])
    signals = source_data.get("landscape_signals") or {}
    implications = source_data.get("implications", [])
    published_at = source_data.get("published_at")
    pub_str = str(published_at)[:10] if published_at else "unknown"

    parts = [
        "Update this wiki theme page to integrate new information from a recently ingested source.",
        "",
        f"NEW SOURCE: \"{title}\" (ID: {source_id})",
        f"Published: {pub_str}",
        "",
    ]

    if claims:
        parts.append("Key claims from this source:")
        for c in claims[:15]:
            parts.append(f"  - {c.get('claim_text', '')[:300]}")

    if signals:
        caps = signals.get("capabilities", [])
        if caps:
            parts.append("\nNew capabilities:")
            for c in caps:
                parts.append(f"  - {c.get('description', '')} (maturity: {c.get('maturity', 'unknown')})")
        lims = signals.get("limitations", [])
        if lims:
            parts.append("\nNew limitations:")
            for l in lims:
                parts.append(f"  - {l.get('description', '')} (severity: {l.get('severity', 'unknown')}, trajectory: {l.get('trajectory', 'unknown')})")
        bots = signals.get("bottlenecks", [])
        if bots:
            parts.append("\nNew bottlenecks:")
            for b in bots:
                parts.append(f"  - {b.get('description', '')} (status: {b.get('status', 'active')}, horizon: {b.get('resolution_horizon', 'unknown')}, blocking: {b.get('blocking_what', '')})")
        bts = signals.get("breakthroughs", [])
        if bts:
            parts.append("\nNew breakthroughs:")
            for bt in bts:
                parts.append(f"  - {bt.get('description', '')} (significance: {bt.get('significance', 'unknown')})")

    if implications:
        parts.append("\nCross-theme implications:")
        for imp in implications[:5]:
            parts.append(f"  - {imp.get('description', imp.get('implication', ''))[:200]}")

    parts.extend([
        "",
        "CURRENT PAGE BODY (excluding Development Timeline — that's handled separately):",
        "```",
        current_body,
        "```",
        "",
        "INSTRUCTIONS:",
        f"- TEMPORAL: This source was published {pub_str}. If it shifts the trajectory in Current State, update the narrative arc. If it merely adds evidence to an existing trend, integrate without restructuring.",
        "- CAPABILITIES: Preserve maturity levels (research / experimental / narrow-production / broad-production). Update existing entries if maturity changed rather than duplicating.",
        "- LIMITATIONS: Preserve type, severity (critical/high/medium/low), and trajectory (worsening/stable/improving).",
        "- BOTTLENECKS: Preserve resolution horizon and what they block. If this source reports progress, UPDATE the existing bottleneck status.",
        "- BREAKTHROUGHS: Include significance and link to bottleneck(s) they address.",
        "- CONTRADICTIONS: If this source contradicts anything on the page, note it in the Contradictions section with evidence from both sides.",
    ])

    # Inject canonical wikilink references
    ref_lines = []
    if source_ref:
        ref_lines.append(f"- THIS SOURCE: {source_ref}")
    if entity_refs:
        ref_lines.append("- ENTITY WIKILINKS (use these exact links):")
        for ename, eslug in entity_refs:
            ref_lines.append(f"  - [[entities/{eslug}|{ename}]]")

    if ref_lines:
        parts.append("- CROSS-REFERENCES: Use ONLY these canonical wikilinks:")
        parts.extend(ref_lines)
    else:
        parts.append("- CROSS-REFERENCES: Do not use wikilinks for entities or themes unless canonical links are listed above. Use plain text instead.")

    parts.extend([
        "- REVISE vs APPEND: When new information supersedes an existing bullet, revise it. Only append when genuinely new.",
        "- EMERGENT CONNECTIONS: If you notice a cross-theme implication NOT in the source data above, append a fenced block at the very end:",
        "  ```json:emergent",
        '  [{"source_theme": "theme_id", "target_theme": "theme_id", "implication": "text", "confidence": 0.7}]',
        "  ```",
        "  Omit this block entirely if no new connections found.",
        "- Do NOT include frontmatter or Development Timeline.",
        "- Return ONLY the updated page body (plus the optional emergent block).",
    ])

    return "\n".join(parts)


def _build_source_create_prompt(source_data: dict, entity_refs: list[tuple[str, str]] | None = None) -> str:
    """Build prompt for source page generation.

    Args:
        source_data: Source metadata dict.
        entity_refs: Optional list of (name, slug) for entities in this source.
    """
    title = source_data.get("title", "Untitled")
    authors = source_data.get("authors", [])
    published_at = source_data.get("published_at", "")
    source_type = source_data.get("source_type", "article")
    claims = source_data.get("claims", [])
    signals = source_data.get("landscape_contributions") or {}
    theme_ids = source_data.get("theme_ids", [])
    deep_summary = source_data.get("deep_summary", "")

    parts = [
        f"Generate a wiki page for this source following the template below.",
        "",
        f"# {title}",
        "",
        "> One-paragraph summary of what this source contributes.",
        "",
        f"**Authors:** {', '.join(authors) if isinstance(authors, list) else authors}",
        f"**Published:** {published_at}",
        f"**Type:** {source_type}",
        "",
    ]

    if deep_summary:
        parts.extend([
            "## Expert Analysis (existing deep summary)",
            "",
            deep_summary[:6000],
            "",
        ])

    parts.extend([
        "## Key Claims",
        "",
    ])

    for i, c in enumerate(claims[:15], 1):
        text = c.get("claim_text", "")[:200]
        evidence = c.get("evidence_snippet", "")[:100]
        parts.append(f"{i}. {text}" + (f' — "{evidence}"' if evidence else ""))

    parts.extend([
        "",
        "## Landscape Contributions",
        "",
    ])

    for key, label in [("capabilities", "Capabilities"), ("limitations", "Limitations"),
                        ("bottlenecks", "Bottlenecks"), ("breakthroughs", "Breakthroughs")]:
        items = signals.get(key, []) if signals else []
        if items:
            parts.append(f"### {label}")
            for item in items:
                desc = item.get("description", "")[:200]
                if key == "capabilities":
                    parts.append(f"- {desc} (maturity: {item.get('maturity', 'unknown')})")
                elif key == "limitations":
                    parts.append(f"- {desc} (severity: {item.get('severity', '')}, trajectory: {item.get('trajectory', '')})")
                elif key == "bottlenecks":
                    parts.append(f"- {desc} (blocking: {item.get('blocking_what', '')}, horizon: {item.get('resolution_horizon', '')})")
                elif key == "breakthroughs":
                    parts.append(f"- {desc} (significance: {item.get('significance', 'incremental')})")
                evidence = item.get("evidence_snippet", "")
                if evidence:
                    parts.append(f'  > "{evidence[:150]}"')
            parts.append("")

    parts.extend([
        "## Themes",
        "",
    ])
    for t in theme_ids:
        parts.append(f"- {_format_theme_ref(t)}")

    # Canonical wikilink references
    ref_lines = []
    if entity_refs:
        ref_lines.append("CANONICAL ENTITY WIKILINKS (use these exact links):")
        for name, slug in entity_refs:
            ref_lines.append(f"  - [[entities/{slug}|{name}]]")
    if theme_ids:
        ref_lines.append("CANONICAL THEME WIKILINKS:")
        for t in theme_ids:
            ref_lines.append(f"  - {_format_theme_ref(t)}")

    if ref_lines:
        parts.extend(["", *ref_lines])

    parts.extend([
        "",
        "INSTRUCTIONS:",
        "- Synthesize the expert analysis, claims, and landscape data into a well-structured wiki page",
        "- Preserve the analytical depth of the expert analysis while adding proper cross-references and structure",
        "- Do NOT include frontmatter",
        "- Use ONLY the canonical wikilinks listed above — do not invent link targets. Use plain text for any reference not listed.",
        "- Emphasize limitations and open questions alongside capabilities",
    ])

    return "\n".join(parts)


def _build_source_fallback(source_data: dict) -> str:
    """Fallback body for source page if LLM fails."""
    title = source_data.get("title", "Untitled")
    authors = source_data.get("authors", [])
    claims = source_data.get("claims", [])
    theme_ids = source_data.get("theme_ids", [])
    deep_summary = source_data.get("deep_summary", "")
    signals = source_data.get("landscape_contributions") or {}

    lines = [
        f"# {title}",
        "",
        f"**Authors:** {', '.join(authors) if isinstance(authors, list) else ''}",
        f"**Published:** {source_data.get('published_at', '')}",
        f"**Type:** {source_data.get('source_type', 'article')}",
        "",
    ]

    if deep_summary:
        lines.extend(["## Analysis", "", deep_summary[:6000], ""])

    lines.extend(["## Key Claims", ""])
    for i, c in enumerate(claims[:10], 1):
        lines.append(f"{i}. {c.get('claim_text', '')[:200]}")

    for key in ("capabilities", "limitations", "bottlenecks", "breakthroughs"):
        items = signals.get(key, [])
        if items:
            lines.extend(["", f"## {key.title()}", ""])
            for item in items:
                lines.append(f"- {item.get('description', '')[:300]}")

    lines.extend(["", "## Themes", ""])
    for t in theme_ids:
        lines.append(f"- {_format_theme_ref(t)}")

    return "\n".join(lines)


def _build_entity_create_prompt(concept_data: dict, source_refs: list[tuple[str, str, str]] | None = None) -> str:
    """Build prompt for entity page generation.

    Args:
        concept_data: Concept metadata dict.
        source_refs: Optional list of (source_id, title, path_stem) for sources referencing this entity.
    """
    name = concept_data.get("canonical_name", "Unknown")
    ctype = concept_data.get("concept_type", "concept")
    description = concept_data.get("description", "")
    theme_ids = concept_data.get("theme_ids", [])
    sources = concept_data.get("source_references", [])
    related_claims = concept_data.get("related_claims", [])
    related_capabilities = concept_data.get("related_capabilities", [])
    related_limitations = concept_data.get("related_limitations", [])

    theme_links = ", ".join(_format_theme_ref(t) for t in theme_ids)

    parts = [
        f"Generate a wiki page for this entity following the template below.",
        "",
        f"# {name}",
        "",
        "> One-paragraph summary of this entity and its significance.",
        "",
        f"**Type:** {ctype}",
        f"**Themes:** {theme_links}",
        "",
        "## Overview",
        "",
        f"Description: {description}",
        "",
    ]

    if related_claims:
        parts.extend([
            "## Key Findings (claims mentioning this entity)",
            "",
        ])
        for i, c in enumerate(related_claims[:15], 1):
            claim_text = c.get("claim_text", "")[:200]
            source_title = c.get("source_title", "")
            evidence = c.get("evidence_snippet", "")[:150]
            parts.append(f"{i}. {claim_text} (from \"{source_title}\")")
            if evidence:
                parts.append(f'   Evidence: "{evidence}"')
        parts.append("")

    if related_capabilities:
        parts.extend(["## Capabilities", ""])
        for cap in related_capabilities:
            parts.append(f"- {cap.get('description', '')[:200]} (maturity: {cap.get('maturity', 'unknown')})")
        parts.append("")

    if related_limitations:
        parts.extend(["## Known Limitations", ""])
        for lim in related_limitations:
            parts.append(f"- {lim.get('description', '')[:200]} (severity: {lim.get('severity', '')}, trajectory: {lim.get('trajectory', '')})")
        parts.append("")

    if not related_claims:
        parts.extend([
            "## Key Findings",
            "(Synthesize findings from the sources below)",
            "",
        ])

    if sources:
        parts.append("Source references:")
        for s in sources[:10]:
            if isinstance(s, dict):
                parts.append(f"  - {s.get('title', s.get('source_id', ''))}")
            else:
                parts.append(f"  - {s}")

    # Canonical wikilink references
    ref_lines = []
    if source_refs:
        ref_lines.append("CANONICAL SOURCE WIKILINKS (use these exact links):")
        for sid, stitle, stem in source_refs:
            ref_lines.append(f"  - [[sources/{stem}|{stitle}]]")
    if theme_ids:
        ref_lines.append("CANONICAL THEME WIKILINKS:")
        for t in theme_ids:
            ref_lines.append(f"  - {_format_theme_ref(t)}")

    if ref_lines:
        parts.extend(["", *ref_lines])

    parts.extend([
        "",
        "## Relationships",
        "(Mention related entities and source connections)",
        "",
        "INSTRUCTIONS:",
        "- Synthesize findings into a narrative — do not just list claims",
        "- Emphasize limitations and open questions",
        "- Do NOT include frontmatter",
        "- Use ONLY the canonical wikilinks listed above — do not invent link targets. Use plain text for any reference not listed.",
    ])

    return "\n".join(parts)


def _build_entity_fallback(concept_data: dict) -> str:
    """Fallback body for entity page if LLM fails."""
    name = concept_data.get("canonical_name", "Unknown")
    ctype = concept_data.get("concept_type", "concept")
    theme_ids = concept_data.get("theme_ids", [])
    related_claims = concept_data.get("related_claims", [])
    related_capabilities = concept_data.get("related_capabilities", [])
    related_limitations = concept_data.get("related_limitations", [])

    lines = [
        f"# {name}",
        "",
        f"**Type:** {ctype}",
        f"**Themes:** {', '.join(_format_theme_ref(t) for t in theme_ids)}",
        "",
        "## Overview",
        "",
        concept_data.get("description", "No description available."),
        "",
    ]

    lines.extend(["## Key Findings", ""])
    if related_claims:
        for i, c in enumerate(related_claims[:15], 1):
            lines.append(f"{i}. {c.get('claim_text', '')[:200]} (from \"{c.get('source_title', '')}\")")
        lines.append("")

    if related_capabilities:
        lines.extend(["## Capabilities", ""])
        for cap in related_capabilities:
            lines.append(f"- {cap.get('description', '')[:200]} (maturity: {cap.get('maturity', 'unknown')})")
        lines.append("")

    if related_limitations:
        lines.extend(["## Known Limitations", ""])
        for lim in related_limitations:
            lines.append(f"- {lim.get('description', '')[:200]} (severity: {lim.get('severity', '')}, trajectory: {lim.get('trajectory', '')})")
        lines.append("")

    lines.extend(["## Relationships", ""])
    return "\n".join(lines)


def _build_entity_update_prompt(current_body: str, new_data: dict) -> str:
    """Build prompt for incremental entity page update."""
    source_id = new_data.get("source_id", "")
    source_title = new_data.get("source_title", "")
    published_at = new_data.get("published_at")
    pub_str = str(published_at)[:10] if published_at else "unknown"
    claims = new_data.get("claims", [])
    signals = new_data.get("landscape_signals") or {}

    parts = [
        f"Update this entity wiki page to integrate new information from source: \"{source_title}\".",
        f"Source ID: {source_id}, Published: {pub_str}",
        "",
    ]

    if claims:
        parts.append("New claims mentioning this entity:")
        for c in claims[:15]:
            parts.append(f"  - {c.get('claim_text', '')[:300]}")

    if signals:
        caps = signals.get("capabilities", [])
        if caps:
            parts.append("\nRelevant capabilities:")
            for c in caps:
                parts.append(f"  - {c.get('description', '')} (maturity: {c.get('maturity', 'unknown')})")
        lims = signals.get("limitations", [])
        if lims:
            parts.append("\nRelevant limitations:")
            for l in lims:
                parts.append(f"  - {l.get('description', '')} (severity: {l.get('severity', 'unknown')}, trajectory: {l.get('trajectory', 'unknown')})")
        bots = signals.get("bottlenecks", [])
        if bots:
            parts.append("\nRelevant bottlenecks:")
            for b in bots:
                parts.append(f"  - {b.get('description', '')} (status: {b.get('status', 'active')})")
        bts = signals.get("breakthroughs", [])
        if bts:
            parts.append("\nRelevant breakthroughs:")
            for bt in bts:
                parts.append(f"  - {bt.get('description', '')} (significance: {bt.get('significance', 'unknown')})")

    parts.extend([
        "",
        "CURRENT PAGE BODY:",
        "```",
        current_body,
        "```",
        "",
        "INSTRUCTIONS:",
        "- Integrate new claims and landscape signals into existing sections",
        "- Note if this source changes the entity's significance, role, or maturity",
        f"- THIS SOURCE: [[sources/{source_id[:10]}-{slugify(source_title)}|{source_title}]]",
        "- Use ONLY canonical wikilinks — do not invent link targets",
        "- When new information updates existing content, revise rather than duplicate",
        "- Do NOT include frontmatter. Return ONLY the updated page body.",
    ])

    return "\n".join(parts)
