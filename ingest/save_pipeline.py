"""Parallel orchestrator for the /save ingestion pipeline.

Two-phase parallel execution with optional prompt merging to reduce
subprocess spawn overhead.

Dependency graph (merge_prompts=True, default):
    themes (sonnet, 1 subprocess)
          |
    +-----+-----+
    v           v
  claims+     landscape+        <- Phase 1: 2 merged parallel subprocesses
  summary     implications
  (sonnet)    (sonnet)
    |           |
    +-----+-----+
          v
  beliefs + anticipations       <- Phase 2: 0-2 subprocesses (early-exit if empty)

Dependency graph (merge_prompts=False, original):
    themes (sonnet, 1 subprocess)
          |
    +-----+-----+----------+
    v           v           v
  claims     summary     landscape     <- Phase 1: 3 parallel subprocesses
  (sonnet)   (sonnet)    (sonnet)
    |                       |
    +---+-------------------+
        v
  beliefs + anticipations + implications  <- Phase 2: 0-3 subprocesses
"""

from __future__ import annotations

import logging
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from ingest.source_quality import (
    get_landscape_issue,
    get_summary_issue,
    refresh_source_processing_status,
)
from ingest.step_status import (
    ensure_step_rows,
    mark_step_completed,
    mark_step_failed,
    mark_step_running,
)

logger = logging.getLogger(__name__)


def run_save_pipeline(
    source_id: str,
    clean_text: str,
    title: str,
    source_type: str,
    url: str | None = None,
    authors: list[str] | None = None,
    published_at: str | None = None,
    library_path: Path | str | None = None,
    category_hints: list[str] | None = None,
    show_name: str | None = None,
    executor=None,
    get_conn_fn=None,
    merge_prompts: bool = True,
    skip_landscape: bool = False,
    skip_summary: bool = False,
    pre_classified_themes: list[dict] | None = None,
    abstract: str | None = None,
    metadata: dict | None = None,
    on_step: callable | None = None,
) -> dict:
    """Run the full extraction pipeline with parallel phases.

    Args:
        source_id: ULID for this source.
        clean_text: Cleaned source text.
        title: Source title.
        source_type: paper, arxiv, article, video, podcast.
        url: Source URL.
        authors: Author/participant names.
        published_at: ISO-8601 publication date string.
        library_path: Path to library/ parent directory (source_id appended by extractors).
        category_hints: Pre-mapped theme hints (e.g. arXiv categories).
        show_name: Channel/podcast name for media sources.
        executor: ClaudeExecutor instance; created if None.
        get_conn_fn: DB connection factory; uses default if None.
        merge_prompts: If True (default), merge compatible extraction steps
            into fewer subprocess calls for reduced startup overhead.
        skip_landscape: If True, skip landscape extraction and implications
            (Merge B branch). Anticipation matching is also skipped.
        skip_summary: If True, skip summary generation. Claims are still
            extracted. When used with merge_prompts=True, falls back to
            claims-only extraction (no merged call).
        pre_classified_themes: If provided, skip Step 0 (theme classification)
            and use these themes directly. Each entry should have theme_id,
            relevance, and level keys.

    Returns:
        dict with keys: themes, theme_proposal, claims, concepts, summary,
        landscape_signals, landscape_delta, anticipation_matches,
        belief_updates, implications, timings, errors.
    """
    t0 = time.monotonic()
    timings: dict[str, float] = {}
    errors: list[str] = []
    quality_assessment: dict | None = None

    # Ensure library_path is a Path
    if library_path is not None:
        library_path = Path(library_path)

    # Create executor if not provided
    if executor is None:
        from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
        executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    # Ensure DB pool is initialized (auto-init from env if needed)
    if get_conn_fn is None:
        try:
            from reading_app.db import ensure_pool, get_conn
            ensure_pool()
            get_conn_fn = get_conn
        except Exception:
            logger.warning("DB pool not available; persistence steps will be skipped")

    tracked_steps = ["themes", "claims", "beliefs", "anticipation_matches"]
    if not skip_summary:
        tracked_steps.append("summary")
    if not skip_landscape:
        tracked_steps.extend(["landscape", "implications"])

    # ── Ensure source row exists (idempotent upsert) ─────────────────
    if get_conn_fn is not None:
        try:
            from reading_app.db import insert_source
            insert_source(
                id=source_id,
                source_type=source_type,
                title=title,
                url=url,
                authors=authors,
                published_at=published_at,
                library_path=str(library_path) if library_path else None,
                processing_status="processing",
                abstract=abstract,
                metadata=metadata,
            )
            ensure_step_rows(source_id, tracked_steps, get_conn_fn)
        except Exception:
            logger.debug("Source upsert skipped (may already exist)", exc_info=True)

    def _notify(step: str, status: str):
        if on_step:
            try:
                on_step(step, status)
            except Exception:
                pass

    # ── Step 0: Theme classification (Sonnet) ─────────────────────────
    t_themes = time.monotonic()
    themes_raw: list[dict] = []
    theme_proposal = None
    source_themes: list[str] = []
    _notify("themes", "running")
    if get_conn_fn is not None:
        mark_step_running(source_id, "themes", get_conn_fn)

    if pre_classified_themes is not None:
        # Reuse themes from a previous /summarise call — skip LLM + DB work.
        for t in pre_classified_themes:
            if "_proposal" in t:
                theme_proposal = t["_proposal"]
            elif "theme_id" in t:
                themes_raw.append(t)
                source_themes.append(t["theme_id"])
        logger.info("Using %d pre-classified themes (skipped classification)", len(themes_raw))
    else:
        try:
            from ingest.theme_classifier import classify_themes
            themes_raw = classify_themes(
                clean_text,
                source_id,
                category_hints=category_hints,
                executor=executor,
                get_conn_fn=get_conn_fn,
            )
            # Separate theme proposal from actual themes
            themes_for_extraction = []
            for t in themes_raw:
                if "_proposal" in t:
                    theme_proposal = t["_proposal"]
                elif "theme_id" in t:
                    themes_for_extraction.append(t)
                    source_themes.append(t["theme_id"])
            themes_raw = themes_for_extraction
        except Exception as e:
            logger.warning("Theme classification failed: %s", e, exc_info=True)
            errors.append(f"themes: {e}")

    timings["themes"] = time.monotonic() - t_themes
    _notify("themes", "completed" if source_themes else "failed")
    if get_conn_fn is not None:
        if source_themes:
            mark_step_completed(
                source_id,
                "themes",
                get_conn_fn,
                result={
                    "theme_count": len(source_themes),
                    "theme_ids": source_themes,
                    "proposed_theme": bool(theme_proposal),
                },
            )
        else:
            mark_step_failed(
                source_id,
                "themes",
                "No themes classified",
                get_conn_fn,
                result={"theme_count": 0, "proposed_theme": bool(theme_proposal)},
            )
    logger.info(
        "Themes classified in %.1fs: %s", timings["themes"],
        [t.get("theme_id") for t in themes_raw],
    )

    # ── Phase 1: Parallel extraction ────────────────────────────────────
    # With merge_prompts=True (default): 2 merged subprocess calls
    #   Merge A: claims + summary  |  Merge B: landscape + implications
    # With merge_prompts=False: 3 separate subprocess calls (original behavior)
    t_phase1 = time.monotonic()

    claims_result: dict = {"claims": [], "concepts": []}
    summary_result: str = ""
    landscape_signals: dict = {}
    implications: list[dict] = []
    merged_implication_error: str | None = None
    merged_implication_persist_error: str | None = None
    if get_conn_fn is not None:
        mark_step_running(source_id, "claims", get_conn_fn)
        if not skip_summary:
            mark_step_running(source_id, "summary", get_conn_fn)
        if not skip_landscape:
            mark_step_running(source_id, "landscape", get_conn_fn)
            if merge_prompts:
                mark_step_running(source_id, "implications", get_conn_fn)

    _notify("claims", "running")
    if not skip_landscape:
        _notify("landscape", "running")

    if merge_prompts:
        from ingest.http_retry import with_retry

        def _extract_claims_and_summary():
            if skip_summary:
                # Extract claims only (no merged call — summary skipped)
                from ingest.extractor import extract_claims
                return with_retry(
                    lambda: extract_claims(
                        source_id=source_id,
                        clean_text=clean_text,
                        source_type=source_type,
                        executor=executor,
                        library_path=library_path,
                        themes=themes_raw or None,
                    ),
                    max_attempts=2, base_delay=5.0,
                    label=f"claims_{source_id}",
                )
            from ingest.merged_extractor import extract_claims_and_summary
            return with_retry(
                lambda: extract_claims_and_summary(
                    source_id=source_id,
                    clean_text=clean_text,
                    source_type=source_type,
                    title=title,
                    url=url,
                    authors=authors,
                    published_at=published_at,
                    themes=themes_raw or None,
                    show_name=show_name,
                    executor=executor,
                    library_path=library_path,
                ),
                max_attempts=2, base_delay=5.0,
                label=f"claims_summary_{source_id}",
            )

        def _extract_landscape_and_implications():
            from ingest.merged_extractor import extract_landscape_and_implications
            return with_retry(
                lambda: extract_landscape_and_implications(
                    clean_text=clean_text,
                    source_id=source_id,
                    source_themes=source_themes or None,
                    published_at=published_at,
                    executor=executor,
                    source_type=source_type,
                    get_conn_fn=get_conn_fn,
                ),
                max_attempts=2, base_delay=5.0,
                label=f"landscape_impl_{source_id}",
            )

        # Determine how many parallel workers we need
        run_landscape = not skip_landscape
        futures = {}
        max_workers = (1 if not run_landscape else 2)

        with ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="phase1") as pool:
            futures["claims_summary"] = pool.submit(_extract_claims_and_summary)
            if run_landscape:
                futures["landscape_impl"] = pool.submit(_extract_landscape_and_implications)

        try:
            cs_result = futures["claims_summary"].result()
            claims_result = {"claims": cs_result.get("claims", []), "concepts": cs_result.get("concepts", [])}
            if not skip_summary:
                summary_result = cs_result.get("summary", "")
            _notify("claims", "completed")
            if not skip_summary:
                _notify("summary", "completed")
        except Exception as e:
            logger.warning("Merged claims+summary failed: %s", e, exc_info=True)
            errors.append(f"claims_summary: {e}")
            _notify("claims", "failed")
            if not skip_summary:
                _notify("summary", "failed")

        if "landscape_impl" in futures:
            try:
                li_result = futures["landscape_impl"].result()
                landscape_signals = li_result.get("landscape", {})
                implications = li_result.get("implications", [])
                _notify("landscape", "completed")
                _notify("implications", "completed")
            except Exception as e:
                logger.warning("Merged landscape+implications failed: %s", e, exc_info=True)
                errors.append(f"landscape_implications: {e}")
                merged_implication_error = str(e)
                _notify("landscape", "failed")
                _notify("implications", "failed")

    else:
        # Original 3-way parallel extraction
        from ingest.http_retry import with_retry as _with_retry

        def _extract_claims():
            from ingest.extractor import extract_claims
            return _with_retry(
                lambda: extract_claims(
                    source_id=source_id,
                    clean_text=clean_text,
                    source_type=source_type,
                    executor=executor,
                    library_path=library_path,
                    themes=themes_raw or None,
                ),
                max_attempts=2, base_delay=5.0,
                label=f"claims_{source_id}",
            )

        def _generate_summary():
            from ingest.deep_summarizer import generate_deep_summary
            return _with_retry(
                lambda: generate_deep_summary(
                    source_id=source_id,
                    clean_text=clean_text,
                    title=title,
                    source_type=source_type,
                    url=url,
                    authors=authors,
                    published_at=published_at,
                    executor=executor,
                    library_path=library_path,
                    themes=themes_raw or None,
                    show_name=show_name,
                ),
                max_attempts=2, base_delay=5.0,
                label=f"summary_{source_id}",
            )

        def _extract_landscape():
            from ingest.landscape_extractor import extract_landscape_signals
            return _with_retry(
                lambda: extract_landscape_signals(
                    clean_text=clean_text,
                    source_id=source_id,
                    source_themes=source_themes or None,
                    published_at=published_at,
                    executor=executor,
                    source_type=source_type,
                ),
                max_attempts=2, base_delay=5.0,
                label=f"landscape_{source_id}",
            )

        with ThreadPoolExecutor(max_workers=3, thread_name_prefix="phase1") as pool:
            fut_claims = pool.submit(_extract_claims)
            fut_summary = pool.submit(_generate_summary) if not skip_summary else None
            fut_landscape = pool.submit(_extract_landscape) if not skip_landscape else None

        try:
            claims_result = fut_claims.result()
            _notify("claims", "completed")
        except Exception as e:
            logger.warning("Claim extraction failed: %s", e, exc_info=True)
            errors.append(f"claims: {e}")
            _notify("claims", "failed")

        if fut_summary:
            try:
                summary_result = fut_summary.result()
                _notify("summary", "completed")
            except Exception as e:
                logger.warning("Deep summary failed: %s", e, exc_info=True)
                errors.append(f"summary: {e}")
                _notify("summary", "failed")

        if fut_landscape:
            try:
                landscape_signals = fut_landscape.result()
                _notify("landscape", "completed")
            except Exception as e:
                logger.warning("Landscape extraction failed: %s", e, exc_info=True)
                errors.append(f"landscape: {e}")
                _notify("landscape", "failed")

    timings["phase1"] = time.monotonic() - t_phase1
    claims_count = len(claims_result.get("claims", []))
    summary_issue = None if skip_summary else get_summary_issue(summary_result)
    landscape_issue = None if skip_landscape else get_landscape_issue(landscape_signals)

    if get_conn_fn is not None:
        if claims_count <= 0:
            mark_step_failed(
                source_id,
                "claims",
                "No claims extracted",
                get_conn_fn,
                result={"claim_count": 0, "concept_count": len(claims_result.get("concepts", []))},
            )

        if not skip_summary:
            if summary_issue is None:
                mark_step_completed(
                    source_id,
                    "summary",
                    get_conn_fn,
                    result={"summary_chars": len(summary_result)},
                )
            else:
                mark_step_failed(
                    source_id,
                    "summary",
                    f"Invalid summary output: {summary_issue}",
                    get_conn_fn,
                    result={"summary_chars": len(summary_result), "issue": summary_issue},
                )

        if not skip_landscape:
            if landscape_issue is not None:
                mark_step_failed(
                    source_id,
                    "landscape",
                    f"Invalid landscape output: {landscape_issue}",
                    get_conn_fn,
                    result={"issue": landscape_issue},
                )

            if merge_prompts and merged_implication_error:
                mark_step_failed(
                    source_id,
                    "implications",
                    merged_implication_error,
                    get_conn_fn,
                    result={"implication_count": len(implications)},
                )

    if claims_count == 0:
        errors.append("claims: no usable claims extracted")
    if summary_issue is not None:
        errors.append(f"summary: {summary_issue}")
    if landscape_issue is not None:
        errors.append(f"landscape: {landscape_issue}")

    logger.info(
        "Phase 1 complete in %.1fs (merged=%s): %d claims, summary=%d chars, landscape=%s, implications=%d",
        timings["phase1"], merge_prompts,
        claims_count,
        len(summary_result),
        bool(landscape_signals),
        len(implications),
    )

    # ── Persist Phase 1 results ──────────────────────────────────────

    # Persist claims to DB
    claims_persisted = 0
    if claims_result.get("claims") and get_conn_fn:
        try:
            from ingest.claim_persistence import persist_extractions_to_db
            claims_persisted = persist_extractions_to_db(source_id, claims_result)
            if claims_persisted > 0:
                mark_step_completed(
                    source_id,
                    "claims",
                    get_conn_fn,
                    result={
                        "claim_count": claims_persisted,
                        "extracted_claim_count": claims_count,
                        "concept_count": len(claims_result.get("concepts", [])),
                    },
                )
            else:
                mark_step_failed(
                    source_id,
                    "claims",
                    "No claims persisted (embedding or insert failed)",
                    get_conn_fn,
                    result={
                        "extracted_claim_count": claims_count,
                        "concept_count": len(claims_result.get("concepts", [])),
                    },
                )
        except Exception as e:
            logger.error("Claim persistence failed: %s", e, exc_info=True)
            errors.append(f"claims_persist: {e}")
            mark_step_failed(
                source_id,
                "claims",
                f"Persistence failed: {e}",
                get_conn_fn,
                result={
                    "extracted_claim_count": claims_count,
                    "concept_count": len(claims_result.get("concepts", [])),
                },
            )

    # Persist landscape signals
    landscape_delta = None
    if landscape_signals and landscape_issue is None and get_conn_fn:
        try:
            from ingest.landscape_extractor import (
                persist_landscape_signals,
                save_landscape_json,
            )
            landscape_delta = persist_landscape_signals(
                landscape_signals, source_id, get_conn_fn=get_conn_fn,
            )
            if library_path:
                save_landscape_json(landscape_signals, library_path / source_id)
            mark_step_completed(
                source_id,
                "landscape",
                get_conn_fn,
                result={
                    "signal_counts": {
                        "capabilities": len(landscape_signals.get("capabilities", [])),
                        "limitations": len(landscape_signals.get("limitations", [])),
                        "bottlenecks": len(landscape_signals.get("bottlenecks", [])),
                        "breakthroughs": len(landscape_signals.get("breakthroughs", [])),
                    },
                },
            )
        except Exception as e:
            logger.warning("Landscape persistence failed: %s", e, exc_info=True)
            errors.append(f"landscape_persist: {e}")
            mark_step_failed(
                source_id,
                "landscape",
                f"Persistence failed: {e}",
                get_conn_fn,
            )

    # Persist implications from merged Phase 1 extraction
    merged_implications_persisted = False
    if implications and get_conn_fn:
        try:
            from ingest.implication_extractor import persist_cross_theme_implications
            persist_cross_theme_implications(implications, source_id, get_conn_fn=get_conn_fn)
            merged_implications_persisted = True
        except Exception as e:
            logger.warning("Implication persistence failed: %s", e, exc_info=True)
            errors.append(f"implications_persist: {e}")
            merged_implication_persist_error = str(e)
            if merge_prompts:
                mark_step_failed(
                    source_id,
                    "implications",
                    f"Persistence failed: {e}",
                    get_conn_fn,
                    result={"implication_count": len(implications)},
                )
    elif merge_prompts and get_conn_fn and not merged_implication_error:
        merged_implications_persisted = True

    if (
        merge_prompts
        and get_conn_fn
        and not skip_landscape
        and not merged_implication_error
        and not merged_implication_persist_error
    ):
        mark_step_completed(
            source_id,
            "implications",
            get_conn_fn,
            result={
                "implication_count": len(implications),
                "persisted": merged_implications_persisted,
            },
        )

    # ── Phase 2: Best-effort checks (parallel) ───────────────────────
    # When merge_prompts=True, implications are already extracted in Phase 1.
    # Phase 2 handles: anticipation matching, belief checking, and
    # implications extraction only if not already done.
    t_phase2 = time.monotonic()

    anticipation_matches: list[dict] = []
    belief_updates: dict = {}
    anticipation_error: str | None = None
    belief_error: str | None = None
    implication_error: str | None = None

    # Early-exit: check if there's anything to do before spawning threads
    has_anticipations = False
    has_beliefs = False
    needs_implications = not merge_prompts and bool(source_themes)

    if source_themes and get_conn_fn:
        try:
            from reading_app.db import get_open_anticipations_for_themes
            has_anticipations = bool(get_open_anticipations_for_themes(source_themes))
        except Exception:
            pass

    if claims_result.get("claims") and get_conn_fn:
        try:
            from reading_app.db import get_active_beliefs
            has_beliefs = bool(get_active_beliefs())
        except Exception:
            pass

    def _match_anticipations():
        from ingest.anticipation_matcher import (
            match_anticipations,
            persist_anticipation_matches,
        )
        # Use landscape signals if available, else build minimal signals from claims
        signals = landscape_signals
        if not signals:
            claims = claims_result.get("claims", [])
            if not claims:
                return []
            signals = {
                "claims_text": "\n".join(
                    c.get("claim_text", "")[:200] for c in claims[:20]
                ),
            }
        matches = match_anticipations(
            extracted_signals=signals,
            source_themes=source_themes,
            source_id=source_id,
            published_at=published_at,
            executor=executor,
        )
        if matches:
            persist_anticipation_matches(matches, source_id)
        return matches

    def _check_beliefs():
        claims = claims_result.get("claims", [])
        if not claims:
            return {}
        from reading_app.db import get_active_beliefs
        from ingest.belief_relevance_checker import (
            check_belief_relevance,
            persist_belief_updates,
        )
        beliefs = get_active_beliefs()
        if not beliefs:
            return {}
        hits = check_belief_relevance(
            claims, beliefs, source_id,
            published_at=published_at,
            executor=executor,
        )
        result = {}
        if hits:
            result = persist_belief_updates(hits, source_id)
        return result

    def _extract_implications():
        if not source_themes:
            return []
        from ingest.implication_extractor import (
            extract_cross_theme_implications,
            persist_cross_theme_implications,
        )
        imps = extract_cross_theme_implications(
            clean_text, source_id, source_themes,
            published_at=published_at,
            executor=executor,
            get_conn_fn=get_conn_fn,
        )
        if imps:
            persist_cross_theme_implications(imps, source_id, get_conn_fn=get_conn_fn)
        return imps

    if has_anticipations or has_beliefs or needs_implications:
        if get_conn_fn is not None:
            if has_anticipations:
                mark_step_running(source_id, "anticipation_matches", get_conn_fn)
            if has_beliefs:
                mark_step_running(source_id, "beliefs", get_conn_fn)
            if needs_implications:
                mark_step_running(source_id, "implications", get_conn_fn)
        max_workers = sum([has_anticipations, has_beliefs, needs_implications])
        with ThreadPoolExecutor(max_workers=max(1, max_workers), thread_name_prefix="phase2") as pool:
            fut_anticipation = pool.submit(_match_anticipations) if has_anticipations else None
            fut_beliefs = pool.submit(_check_beliefs) if has_beliefs else None
            fut_implications = pool.submit(_extract_implications) if needs_implications else None

        if fut_anticipation:
            try:
                anticipation_matches = fut_anticipation.result()
            except Exception as e:
                logger.warning("Anticipation matching failed (best-effort): %s", e, exc_info=True)
                errors.append(f"anticipations: {e}")
                anticipation_error = str(e)

        if fut_beliefs:
            try:
                belief_updates = fut_beliefs.result()
            except Exception as e:
                logger.warning("Belief checking failed (best-effort): %s", e, exc_info=True)
                errors.append(f"beliefs: {e}")
                belief_error = str(e)

        if fut_implications:
            try:
                implications = fut_implications.result()
            except Exception as e:
                logger.warning("Implication extraction failed (best-effort): %s", e, exc_info=True)
                errors.append(f"implications: {e}")
                implication_error = str(e)
    else:
        logger.info("Phase 2 early-exit: no anticipations, beliefs, or pending implications to check")

    timings["phase2"] = time.monotonic() - t_phase2
    timings["total"] = time.monotonic() - t0

    if get_conn_fn is not None:
        if anticipation_error:
            mark_step_failed(
                source_id,
                "anticipation_matches",
                anticipation_error,
                get_conn_fn,
                result={"match_count": len(anticipation_matches)},
            )
        elif has_anticipations:
            mark_step_completed(
                source_id,
                "anticipation_matches",
                get_conn_fn,
                result={"match_count": len(anticipation_matches)},
            )
        else:
            mark_step_completed(
                source_id,
                "anticipation_matches",
                get_conn_fn,
                result={"skipped": True, "reason": "no_open_anticipations"},
            )

        if belief_error:
            mark_step_failed(
                source_id,
                "beliefs",
                belief_error,
                get_conn_fn,
                result={"update_count": len(belief_updates.get("hits", [])) if isinstance(belief_updates, dict) else 0},
            )
        elif has_beliefs:
            belief_count = len(belief_updates.get("hits", [])) if isinstance(belief_updates, dict) else 0
            mark_step_completed(
                source_id,
                "beliefs",
                get_conn_fn,
                result={"update_count": belief_count},
            )
        else:
            mark_step_completed(
                source_id,
                "beliefs",
                get_conn_fn,
                result={"skipped": True, "reason": "no_active_beliefs"},
            )

        if not skip_landscape and not merge_prompts:
            if implication_error:
                mark_step_failed(
                    source_id,
                    "implications",
                    implication_error,
                    get_conn_fn,
                    result={"implication_count": len(implications)},
                )
            else:
                mark_step_completed(
                    source_id,
                    "implications",
                    get_conn_fn,
                    result={
                        "implication_count": len(implications),
                        "skipped": not needs_implications,
                    },
                )

    logger.info(
        "Pipeline complete in %.1fs (themes=%.1fs, phase1=%.1fs, phase2=%.1fs). "
        "Claims=%d, landscape=%s, anticipations=%d, beliefs=%s, implications=%d, errors=%d",
        timings["total"], timings["themes"], timings["phase1"], timings["phase2"],
        claims_count,
        landscape_delta.counts if landscape_delta else "none",
        len(anticipation_matches),
        bool(belief_updates),
        len(implications),
        len(errors),
    )

    # ── Mark source status based on extraction quality ──────────────────
    if get_conn_fn is not None:
        try:
            quality_assessment = refresh_source_processing_status(
                source_id,
                get_conn_fn,
                library_path=library_path,
                require_summary=not skip_summary,
                require_landscape=not skip_landscape,
            )

            for issue in quality_assessment["issues"]:
                if issue not in errors:
                    errors.append(issue)
            if quality_assessment["status"] != "complete":
                logger.warning("Source %s marked incomplete: %s", source_id, quality_assessment["issues"])

            # Persist extraction quality for trend analysis
            try:
                from reading_app.quality_store import log_quality_metric
                log_quality_metric(
                    "source_extraction", "source", source_id,
                    {
                        k: v for k, v in quality_assessment.items()
                        if k not in ("issues", "status")
                    },
                    skill="save",
                )
            except Exception:
                logger.debug("Failed to log extraction quality metric", exc_info=True)

        except Exception:
            logger.debug("Failed to update source status", exc_info=True)

    return {
        "themes": themes_raw,
        "theme_proposal": theme_proposal,
        "claims": claims_result.get("claims", []),
        "concepts": claims_result.get("concepts", []),
        "summary": summary_result,
        "landscape_signals": landscape_signals,
        "landscape_delta": landscape_delta,
        "anticipation_matches": anticipation_matches,
        "belief_updates": belief_updates,
        "implications": implications,
        "timings": timings,
        "errors": errors,
        "processing_status": quality_assessment["status"] if quality_assessment else None,
        "quality_assessment": quality_assessment,
    }
