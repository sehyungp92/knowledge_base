"""Post-processing orchestrator for /save.

Runs 4 downstream steps after source ingestion completes:
  1. source_edges    — LLM-classified edges between the new source and neighbours
  2. graph_metrics   — NetworkX PageRank, communities, betweenness, influence
  3. state_summaries — temporal narrative for the source's themes
  4. anticipations   — generate predictions for underpopulated themes

Step 2 depends on 1. Steps 3-4 are independent.
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone

from ingest.source_quality import is_valid_summary, read_source_artifact_text
from ingest.step_status import (
    ensure_step_rows,
    load_step_status,
    mark_step_completed,
    mark_step_failed,
    mark_step_running,
)

logger = logging.getLogger(__name__)

STEPS = [
    "source_edges",
    "graph_metrics",
    "state_summaries",
    "anticipations",
]

# graph_metrics debounce: skip if last run was < 5 minutes ago
_GRAPH_METRICS_DEBOUNCE_S = 300

# Max source-edge candidates (expanded from save_pipeline's 5)
_MAX_EDGE_CANDIDATES = 30
_EDGE_BATCH_SIZE = 5

# Anticipation thresholds
_MIN_SOURCES_FOR_ANTICIPATIONS = 5
_MAX_ANTICIPATIONS_PER_THEME = 10


def enqueue_post_processing(
    source_id: str,
    theme_ids: list[str],
    get_conn_fn,
) -> bool:
    """Insert tracking rows into PostgreSQL for the post-processing worker to pick up.

    Args:
        source_id: The source that just completed ingestion.
        theme_ids: Theme IDs associated with this source.
        get_conn_fn: DB connection factory (PostgreSQL).

    Returns:
        True if rows inserted successfully.
    """
    ok = ensure_step_rows(source_id, STEPS, get_conn_fn)
    if ok:
        logger.info("Post-processing enqueued for %s (themes: %s)", source_id, theme_ids)
    else:
        logger.warning("Failed to insert post_processing_status rows", exc_info=True)
    return ok


def poll_pending_source(get_conn_fn) -> tuple[str, list[str]] | None:
    """Find the next source with pending post-processing steps.

    Returns (source_id, theme_ids) or None if nothing pending.
    """
    try:
        with get_conn_fn() as conn:
            row = conn.execute(
                """SELECT DISTINCT pp.source_id
                   FROM post_processing_status pp
                   WHERE pp.status = 'pending'
                   ORDER BY pp.source_id
                   LIMIT 1"""
            ).fetchone()

            if not row:
                return None

            source_id = row["source_id"]

            # Get theme_ids for this source
            themes = conn.execute(
                "SELECT theme_id FROM source_themes WHERE source_id = %s",
                (source_id,),
            ).fetchall()
            theme_ids = [t["theme_id"] for t in themes]

            return (source_id, theme_ids)
    except Exception:
        logger.debug("Failed to poll pending post-processing", exc_info=True)
        return None


def run_post_processing(
    source_id: str,
    theme_ids: list[str],
    executor,
    get_conn_fn,
) -> dict:
    """Run all post-processing steps for a source in dependency order.

    Skips already-completed steps. Updates status per step.

    Returns:
        dict with step names as keys and result/error info as values.
    """
    results = {}

    # Load current status
    step_status = _load_step_status(source_id, get_conn_fn)

    # Phase 1: source_edges
    status = step_status.get("source_edges", {}).get("status")
    if status == "completed":
        results["source_edges"] = {"skipped": True, "reason": "already_completed"}
    else:
        results["source_edges"] = _run_step(
            source_id, "source_edges", _step_source_edges,
            executor=executor, get_conn_fn=get_conn_fn,
            theme_ids=theme_ids,
        )

    # Phase 2: graph_metrics (depends on source_edges)
    status = step_status.get("graph_metrics", {}).get("status")
    if status == "completed":
        results["graph_metrics"] = {"skipped": True, "reason": "already_completed"}
    else:
        results["graph_metrics"] = _run_step(
            source_id, "graph_metrics", _step_graph_metrics,
            executor=executor, get_conn_fn=get_conn_fn,
            theme_ids=theme_ids,
        )

    # Phase 3: state_summaries and anticipations (independent)
    for step_name, step_fn in [
        ("state_summaries", _step_state_summaries),
        ("anticipations", _step_anticipations),
    ]:
        status = step_status.get(step_name, {}).get("status")
        if status == "completed":
            results[step_name] = {"skipped": True, "reason": "already_completed"}
            continue
        results[step_name] = _run_step(
            source_id, step_name, step_fn,
            executor=executor, get_conn_fn=get_conn_fn,
            theme_ids=theme_ids,
        )

    logger.info(
        "Post-processing complete for %s: %s",
        source_id,
        {k: "ok" if not v.get("error") else "error" for k, v in results.items()},
    )

    # Check if taxonomy health check is due (every 50 new sources)
    _maybe_trigger_taxonomy_health(get_conn_fn)

    return results


def _load_step_status(source_id: str, get_conn_fn) -> dict:
    """Load current status of all steps for a source."""
    return load_step_status(source_id, get_conn_fn)


def _run_step(
    source_id: str,
    step_name: str,
    step_fn,
    *,
    executor,
    get_conn_fn,
    theme_ids: list[str],
) -> dict:
    """Execute a single step with status tracking."""
    mark_step_running(source_id, step_name, get_conn_fn)

    try:
        result = step_fn(
            source_id=source_id,
            executor=executor,
            get_conn_fn=get_conn_fn,
            theme_ids=theme_ids,
        )
        result = result or {}

        mark_step_completed(source_id, step_name, get_conn_fn, result=result)

        return result

    except Exception as e:
        error_msg = str(e)[:500]
        logger.warning("Post-processing step %s failed for %s: %s",
                       step_name, source_id, error_msg, exc_info=True)

        mark_step_failed(source_id, step_name, error_msg, get_conn_fn)

        return {"error": error_msg}


# ── Taxonomy health trigger ──────────────────────────────────────────

# Threshold: run taxonomy health check every N new sources
_TAXONOMY_HEALTH_THRESHOLD = 50


def _maybe_trigger_taxonomy_health(get_conn_fn):
    """Run taxonomy health check if enough new sources have accumulated."""
    try:
        with get_conn_fn() as conn:
            last_check = conn.execute(
                "SELECT max(created_at) AS ts FROM taxonomy_evolution_proposals"
            ).fetchone()["ts"]

            sources_since = conn.execute(
                "SELECT count(*) AS cnt FROM sources WHERE ingested_at > %s",
                (last_check or datetime(1970, 1, 1, tzinfo=timezone.utc),),
            ).fetchone()["cnt"]

        if sources_since < _TAXONOMY_HEALTH_THRESHOLD:
            return

        logger.info(
            "Taxonomy health threshold reached (%d sources since last check), "
            "triggering health check",
            sources_since,
        )
        from reading_app.config import Config
        from scripts.taxonomy_health import run_health_check

        config = Config()
        proposals = run_health_check(config.postgres_dsn, config.library_path)
        if proposals:
            logger.info(
                "Taxonomy health check generated %d proposals — "
                "run '/themes review-evolution' to review",
                len(proposals),
            )
    except Exception:
        # Health check is best-effort; never block post-processing
        logger.debug("Taxonomy health check skipped", exc_info=True)


# ── Step implementations ─────────────────────────────────────────────


def _step_source_edges(*, source_id, executor, get_conn_fn, theme_ids) -> dict:
    """Compute source-level edges for the new source against its closest neighbours."""
    from ingest.edge_extractor import classify_edge_batch

    with get_conn_fn() as conn:
        # Find top candidates sharing concepts with this source
        candidates = conn.execute(
            """SELECT sc2.source_id AS other_id, COUNT(*) AS overlap
               FROM source_concepts sc1
               JOIN source_concepts sc2 ON sc1.concept_id = sc2.concept_id
               WHERE sc1.source_id = %s
                 AND sc2.source_id != %s
               GROUP BY sc2.source_id
               HAVING COUNT(*) >= 2
               ORDER BY COUNT(*) DESC
               LIMIT %s""",
            (source_id, source_id, _MAX_EDGE_CANDIDATES),
        ).fetchall()

        if not candidates:
            return {"edges_created": 0, "candidates": 0}

        # Filter out existing edges
        other_ids = [r["other_id"] for r in candidates]
        existing = conn.execute(
            """SELECT source_a, source_b FROM source_edges
               WHERE (source_a = %s AND source_b = ANY(%s))
                  OR (source_b = %s AND source_a = ANY(%s))""",
            (source_id, other_ids, source_id, other_ids),
        ).fetchall()
        existing_pairs = set()
        for r in existing:
            existing_pairs.add((r["source_a"], r["source_b"]))
            existing_pairs.add((r["source_b"], r["source_a"]))

        new_pairs = [
            (source_id, r["other_id"])
            for r in candidates
            if (source_id, r["other_id"]) not in existing_pairs
        ]

        if not new_pairs:
            return {"edges_created": 0, "candidates": len(candidates), "all_exist": True}

        # Get summaries for all involved sources
        all_ids = list({source_id} | {p[1] for p in new_pairs})
        sources = conn.execute(
            "SELECT id, title, library_path FROM sources WHERE id = ANY(%s)",
            (all_ids,),
        ).fetchall()
        summary_map = {}
        for row in sources:
            summary_text = read_source_artifact_text(
                row.get("library_path"),
                row["id"],
                "deep_summary.md",
            )
            if summary_text and is_valid_summary(summary_text):
                summary_map[row["id"]] = {
                    "id": row["id"],
                    "title": row.get("title", ""),
                    "deep_summary": summary_text,
                }

    # Classify in batches
    edges_created = 0
    for batch_start in range(0, len(new_pairs), _EDGE_BATCH_SIZE):
        batch = new_pairs[batch_start:batch_start + _EDGE_BATCH_SIZE]
        batch_input = []
        batch_pairs = []
        for src_a, src_b in batch:
            sa = summary_map.get(src_a)
            sb = summary_map.get(src_b)
            if not sa or not sb:
                continue
            batch_input.append({
                "title_a": sa.get("title", ""),
                "summary_a": (sa.get("deep_summary") or "")[:1200],
                "title_b": sb.get("title", ""),
                "summary_b": (sb.get("deep_summary") or "")[:1200],
                "shared_concepts": [],
            })
            batch_pairs.append((src_a, src_b))

        if not batch_input:
            continue

        try:
            results = classify_edge_batch(
                batch_input,
                executor=executor,
                batch_id=batch_start // _EDGE_BATCH_SIZE,
            )
            with get_conn_fn() as conn:
                for edge, (src_a, src_b) in zip(results, batch_pairs):
                    if edge and edge.get("edge_type") and edge["edge_type"] != "NONE" and "error" not in edge:
                        conn.execute(
                            """INSERT INTO source_edges
                                   (source_a, source_b, edge_type, confidence,
                                    explanation, evidence_a, evidence_b)
                               VALUES (%s, %s, %s, %s, %s, %s, %s)
                               ON CONFLICT DO NOTHING""",
                            (src_a, src_b, edge["edge_type"],
                             edge.get("confidence", 0.5),
                             edge.get("explanation", ""),
                             edge.get("evidence_a", ""),
                             edge.get("evidence_b", "")),
                        )
                        edges_created += 1
                conn.commit()
        except Exception:
            logger.debug("Edge batch classification failed at offset %d", batch_start, exc_info=True)

    return {"edges_created": edges_created, "candidates": len(candidates), "new_pairs": len(new_pairs)}


def _step_graph_metrics(*, source_id, executor, get_conn_fn, theme_ids) -> dict:
    """Recompute graph metrics (PageRank, communities, betweenness, influence)."""
    # Debounce: skip if last run was < 5 minutes ago
    try:
        with get_conn_fn() as conn:
            last_run = conn.execute(
                """SELECT MAX(completed_at) AS last_completed
                   FROM post_processing_status
                   WHERE step = 'graph_metrics' AND status = 'completed'"""
            ).fetchone()
            if last_run and last_run["last_completed"]:
                elapsed = (datetime.now(timezone.utc) - last_run["last_completed"]).total_seconds()
                if elapsed < _GRAPH_METRICS_DEBOUNCE_S:
                    return {"skipped": True, "reason": "debounce", "elapsed_s": round(elapsed)}
    except Exception:
        pass

    from retrieval.graph_algorithms import KnowledgeGraphAnalyzer

    analyzer = KnowledgeGraphAnalyzer(get_conn_fn)
    result = analyzer.materialize()
    return {"materialize_result": result}


def _step_state_summaries(*, source_id, executor, get_conn_fn, theme_ids) -> dict:
    """Regenerate state summaries for this source's themes if stale or missing."""
    from retrieval.state_summary import generate_theme_state_summary, should_regenerate

    if not theme_ids:
        return {"themes_updated": 0, "reason": "no_themes"}

    updated = []
    skipped = []

    with get_conn_fn() as conn:
        for theme_id in theme_ids:
            theme = conn.execute(
                """SELECT id, name, state_summary, state_summary_updated_at, velocity
                   FROM themes WHERE id = %s""",
                (theme_id,),
            ).fetchone()
            if not theme:
                skipped.append(theme_id)
                continue

            source_count = conn.execute(
                "SELECT COUNT(*) AS cnt FROM source_themes WHERE theme_id = %s",
                (theme_id,),
            ).fetchone()["cnt"]

            if not should_regenerate(dict(theme), source_count):
                skipped.append(theme_id)
                continue

            try:
                summary = generate_theme_state_summary(
                    theme_id=theme_id,
                    executor=executor,
                )
                if summary:
                    conn.execute(
                        """UPDATE themes
                           SET state_summary = %s,
                               state_summary_updated_at = %s
                           WHERE id = %s""",
                        (summary, datetime.now(timezone.utc), theme_id),
                    )
                    conn.commit()
                    updated.append(theme_id)
                else:
                    skipped.append(theme_id)
            except Exception:
                logger.debug("State summary failed for %s", theme_id, exc_info=True)
                skipped.append(theme_id)

    return {"themes_updated": len(updated), "updated": updated, "skipped": skipped}


def _step_anticipations(*, source_id, executor, get_conn_fn, theme_ids) -> dict:
    """Generate anticipations for underpopulated themes."""
    if not theme_ids:
        return {"themes_processed": 0, "reason": "no_themes"}

    generated = []
    skipped = []

    with get_conn_fn() as conn:
        for theme_id in theme_ids:
            # Check source count
            source_count = conn.execute(
                "SELECT COUNT(*) AS cnt FROM source_themes WHERE theme_id = %s",
                (theme_id,),
            ).fetchone()["cnt"]

            if source_count < _MIN_SOURCES_FOR_ANTICIPATIONS:
                skipped.append({"theme": theme_id, "reason": "too_few_sources",
                                "count": source_count})
                continue

            # Check existing anticipation count
            ant_count = conn.execute(
                "SELECT COUNT(*) AS cnt FROM anticipations WHERE theme_id = %s AND status = 'open'",
                (theme_id,),
            ).fetchone()["cnt"]

            if ant_count >= _MAX_ANTICIPATIONS_PER_THEME:
                skipped.append({"theme": theme_id, "reason": "enough_anticipations",
                                "count": ant_count})
                continue

            # Generate anticipations using the handler's logic
            try:
                from gateway.anticipate_handler import _handle_generate
                _handle_generate(
                    theme_filter=theme_id,
                    executor=executor,
                    on_progress=None,
                    log=logger,
                )
                generated.append(theme_id)
            except Exception:
                logger.debug("Anticipation generation failed for %s", theme_id, exc_info=True)
                skipped.append({"theme": theme_id, "reason": "error"})

    return {
        "themes_processed": len(generated),
        "generated": generated,
        "skipped": skipped,
    }
