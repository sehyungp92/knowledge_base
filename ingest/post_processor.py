"""Post-processing orchestrator for /save.

Runs 5 downstream steps after source ingestion completes:
  1. source_edges    — LLM-classified edges between the new source and neighbours
  2. concept_edges   — Typed concept-level relationships for co-occurring concepts
  3. graph_metrics   — Incremental betweenness + debounced full recomputation
  4. state_summaries — temporal narrative for the source's themes
  5. anticipations   — generate predictions for underpopulated themes

Steps 1-2 run first. Step 3 depends on 1-2. Steps 4-5 are independent.
"""

from __future__ import annotations

import json
import logging
import re
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
    "concept_edges",
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

    # Phase 1b: concept_edges (selective concept-level relationships)
    status = step_status.get("concept_edges", {}).get("status")
    if status == "completed":
        results["concept_edges"] = {"skipped": True, "reason": "already_completed"}
    else:
        results["concept_edges"] = _run_step(
            source_id, "concept_edges", _step_concept_edges,
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


def _step_concept_edges(*, source_id, executor, get_conn_fn, theme_ids) -> dict:
    """Extract selective concept-level edges for high-confidence co-occurring concepts.

    Only creates edges between concepts that co-occur in this source with high
    frequency, using LLM classification for relationship type.
    """
    with get_conn_fn() as conn:
        # Find concept pairs that co-occur in this source with at least 3 shared sources total
        pairs = conn.execute(
            """WITH source_concepts_here AS (
                   SELECT concept_id FROM source_concepts WHERE source_id = %s
               )
               SELECT c1.id AS id_a, c1.canonical_name AS name_a,
                      c2.id AS id_b, c2.canonical_name AS name_b,
                      COUNT(DISTINCT sc1.source_id) AS cooccurrence_count
               FROM source_concepts_here sch1
               JOIN source_concepts_here sch2 ON sch1.concept_id < sch2.concept_id
               JOIN concepts c1 ON sch1.concept_id = c1.id
               JOIN concepts c2 ON sch2.concept_id = c2.id
               JOIN source_concepts sc1 ON sc1.concept_id = c1.id
               JOIN source_concepts sc2 ON sc2.concept_id = c2.id
                    AND sc1.source_id = sc2.source_id
               GROUP BY c1.id, c1.canonical_name, c2.id, c2.canonical_name
               HAVING COUNT(DISTINCT sc1.source_id) >= 3
               ORDER BY cooccurrence_count DESC
               LIMIT 20""",
            (source_id,),
        ).fetchall()

        if not pairs:
            return {"edges_created": 0, "candidates": 0}

        # Filter out existing concept edges
        existing = set()
        for p in pairs:
            row = conn.execute(
                """SELECT 1 FROM concept_edges
                   WHERE (concept_a_id = %s AND concept_b_id = %s)
                      OR (concept_a_id = %s AND concept_b_id = %s)""",
                (p["id_a"], p["id_b"], p["id_b"], p["id_a"]),
            ).fetchone()
            if row:
                existing.add((p["id_a"], p["id_b"]))

        new_pairs = [p for p in pairs if (p["id_a"], p["id_b"]) not in existing]
        if not new_pairs:
            return {"edges_created": 0, "candidates": len(pairs), "all_exist": True}

    # LLM classification for relationship types
    pair_descriptions = "\n".join(
        f"- {p['name_a']} <-> {p['name_b']} (co-occur in {p['cooccurrence_count']} sources)"
        for p in new_pairs[:15]
    )

    prompt = f"""Classify the relationship between each concept pair. Use ONLY these types:
- alternative_to: competing approaches to the same problem
- builds_on: one concept extends or requires the other
- contrasts_with: fundamentally different approaches or perspectives
- enables: one concept makes the other possible
- specializes: one is a specific instance of the other
- component_of: one is a part or ingredient of the other
- NONE: no meaningful direct relationship

Return a JSON array with objects: {{"a": "name_a", "b": "name_b", "type": "edge_type", "confidence": 0.0-1.0}}
Only include pairs with confidence >= 0.6. Omit NONE relationships.

Concept pairs:
{pair_descriptions}"""

    try:
        result = executor.run_raw(prompt, session_id="concept_edges", timeout=60)
        if not result.text:
            return {"edges_created": 0, "candidates": len(new_pairs), "llm_empty": True}

        json_match = re.search(r"\[.*\]", result.text, re.DOTALL)
        if not json_match:
            return {"edges_created": 0, "candidates": len(new_pairs), "parse_failed": True}

        edges = json.loads(json_match.group(0))
        if not isinstance(edges, list):
            return {"edges_created": 0, "parse_failed": True}

        # Map names back to IDs
        name_to_pair = {(p["name_a"], p["name_b"]): p for p in new_pairs}
        name_to_pair.update({(p["name_b"], p["name_a"]): p for p in new_pairs})

        valid_types = {"alternative_to", "builds_on", "contrasts_with", "enables", "specializes", "component_of"}
        edges_created = 0

        with get_conn_fn() as conn:
            for edge in edges:
                etype = edge.get("type", "")
                if etype not in valid_types:
                    continue
                conf = edge.get("confidence", 0.5)
                if conf < 0.6:
                    continue

                pair = name_to_pair.get((edge.get("a", ""), edge.get("b", "")))
                if not pair:
                    continue

                conn.execute(
                    """INSERT INTO concept_edges
                           (concept_a_id, concept_b_id, edge_type, confidence, evidence_source)
                       VALUES (%s, %s, %s, %s, %s)
                       ON CONFLICT (concept_a_id, concept_b_id, edge_type) DO UPDATE
                       SET confidence = GREATEST(concept_edges.confidence, EXCLUDED.confidence)""",
                    (pair["id_a"], pair["id_b"], etype, conf, source_id),
                )
                edges_created += 1
            conn.commit()

        return {"edges_created": edges_created, "candidates": len(new_pairs)}
    except Exception:
        logger.debug("Concept edge classification failed", exc_info=True)
        return {"edges_created": 0, "error": "classification_failed"}


def _step_graph_metrics(*, source_id, executor, get_conn_fn, theme_ids) -> dict:
    """Recompute graph metrics — incremental for affected neighborhood, full if stale.

    Incremental mode: recompute betweenness only for concepts co-occurring with
    the new source's concepts (the affected neighborhood). Full PageRank, communities,
    and theme influence are debounced to every 5 minutes.
    """
    result = {}

    # Always run incremental betweenness for affected concepts
    try:
        result["incremental"] = _incremental_betweenness(source_id, get_conn_fn)
    except Exception:
        logger.debug("Incremental betweenness failed", exc_info=True)
        result["incremental"] = {"error": "failed"}

    # Debounce full recomputation (PageRank, communities, theme influence)
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
                    result["full"] = {"skipped": True, "reason": "debounce", "elapsed_s": round(elapsed)}
                    return result
    except Exception:
        pass

    from retrieval.graph_algorithms import KnowledgeGraphAnalyzer

    analyzer = KnowledgeGraphAnalyzer(get_conn_fn)
    result["full"] = {"materialize_result": analyzer.materialize()}
    return result


def _incremental_betweenness(source_id: str, get_conn_fn) -> dict:
    """Recompute betweenness centrality for concepts in the new source's neighborhood."""
    try:
        import networkx as nx
    except ImportError:
        return {"skipped": True, "reason": "networkx_unavailable"}

    with get_conn_fn() as conn:
        # Get concepts for this source
        source_concepts = conn.execute(
            "SELECT concept_id FROM source_concepts WHERE source_id = %s",
            (source_id,),
        ).fetchall()

        if not source_concepts:
            return {"skipped": True, "reason": "no_concepts"}

        concept_ids = [r["concept_id"] for r in source_concepts]

        # Get neighborhood: concepts that co-occur with any of this source's concepts
        neighbor_rows = conn.execute(
            """SELECT DISTINCT sc2.concept_id
               FROM source_concepts sc1
               JOIN source_concepts sc2 ON sc1.source_id = sc2.source_id
               WHERE sc1.concept_id = ANY(%s)""",
            (concept_ids,),
        ).fetchall()

        neighborhood = set(r["concept_id"] for r in neighbor_rows)
        if len(neighborhood) < 2:
            return {"skipped": True, "reason": "neighborhood_too_small"}

        # Build subgraph for the neighborhood
        edges = conn.execute(
            """SELECT sc1.concept_id AS c1, sc2.concept_id AS c2, COUNT(*) AS weight
               FROM source_concepts sc1
               JOIN source_concepts sc2 ON sc1.source_id = sc2.source_id
                    AND sc1.concept_id < sc2.concept_id
               WHERE sc1.concept_id = ANY(%s) AND sc2.concept_id = ANY(%s)
               GROUP BY sc1.concept_id, sc2.concept_id""",
            (list(neighborhood), list(neighborhood)),
        ).fetchall()

    G = nx.Graph()
    for e in edges:
        G.add_edge(e["c1"], e["c2"], weight=e["weight"])

    if G.number_of_nodes() < 2:
        return {"skipped": True, "reason": "subgraph_too_small"}

    # Compute betweenness on subgraph
    if G.number_of_nodes() > 500:
        scores = nx.betweenness_centrality(G, k=min(100, G.number_of_nodes()))
    else:
        scores = nx.betweenness_centrality(G)

    # Upsert only the affected concepts
    now = datetime.now(timezone.utc)
    updated = 0
    with get_conn_fn() as conn:
        for node, score in scores.items():
            if score > 0:
                conn.execute(
                    """INSERT INTO graph_metrics
                           (metric_type, entity_type, entity_id, score, metadata, computed_at)
                       VALUES ('betweenness', 'concept', %s, %s, %s, %s)
                       ON CONFLICT (metric_type, entity_type, entity_id)
                       DO UPDATE SET score = EXCLUDED.score, computed_at = EXCLUDED.computed_at""",
                    (str(node), score, json.dumps({"incremental": True}), now),
                )
                updated += 1
        conn.commit()

    return {"nodes": G.number_of_nodes(), "edges": G.number_of_edges(), "updated": updated}


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
