"""Batch edge computation between sources.

Finds candidate source pairs via shared concepts/themes, classifies
relationships with LLM (in batches), and persists edges to the database.

Usage:
    python -m scripts.compute_edges [--limit N] [--delay SECS] [--batch-size N]
"""

from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LIBRARY_PATH = PROJECT_ROOT / "library"
PROGRESS_FILE = PROJECT_ROOT / "scripts" / "edge_progress.json"


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        data.setdefault("failed", 0)
        data.setdefault("skipped_pairs", [])
        data.setdefault("failed_pairs", [])
        return data
    return {"completed_pairs": [], "skipped_pairs": [], "failed_pairs": [], "edges_created": 0, "skipped": 0, "failed": 0}


def save_progress(progress: dict):
    tmp = PROGRESS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(progress, indent=2), encoding="utf-8")
    tmp.replace(PROGRESS_FILE)


def cleanup_session_dir(workspace: Path, session_id: str):
    """Remove a per-batch session directory to prevent accumulation."""
    d = workspace / session_id
    if d.exists():
        try:
            shutil.rmtree(d)
        except Exception:
            logger.debug("Failed to clean up session dir %s", d, exc_info=True)


def main():
    parser = argparse.ArgumentParser(description="Compute source edges")
    parser.add_argument("--limit", type=int, default=500, help="Max pairs to process")
    parser.add_argument("--delay", type=float, default=0.2, help="Seconds between LLM calls")
    parser.add_argument("--batch-size", type=int, default=10, help="Pairs per LLM invocation")
    parser.add_argument("--min-concepts", type=int, default=2, help="Min shared concepts for candidate pair")
    parser.add_argument("--resume", action="store_true", help="Resume from progress")
    parser.add_argument("--retry-failed", action="store_true", help="Retry only previously failed pairs")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    from reading_app.config import Config
    from reading_app.db import init_pool, get_conn, insert_source_edge
    from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
    from ingest.edge_extractor import (
        find_candidate_pairs, classify_edge_batch, classify_edge, get_source_summary,
    )

    config = Config()
    init_pool(config.postgres_dsn)
    executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    # Find candidate pairs
    logger.info("Finding candidate source pairs (min_shared_concepts=%d)...", args.min_concepts)
    candidates = find_candidate_pairs(get_conn, min_shared_concepts=args.min_concepts)
    logger.info("Found %d candidate pairs", len(candidates))

    # Load progress
    progress = load_progress() if (args.resume or args.retry_failed) else {
        "completed_pairs": [], "skipped_pairs": [], "failed_pairs": [], "edges_created": 0, "skipped": 0, "failed": 0,
    }
    done = set(tuple(p) for p in progress.get("completed_pairs", []))
    done |= set(tuple(p) for p in progress.get("skipped_pairs", []))

    if args.retry_failed:
        # Only process previously failed pairs
        failed_set = set(tuple(p) for p in progress.get("failed_pairs", []))
        candidates = [c for c in candidates if (c["source_a"], c["source_b"]) in failed_set]
        # Remove them from failed_pairs so they get fresh tracking
        progress["failed_pairs"] = []
        progress["failed"] = 0
        logger.info("Retrying %d previously failed pairs", len(candidates))
    else:
        # Filter already-processed pairs (but NOT failed ones — those stay retryable)
        failed_set = set(tuple(p) for p in progress.get("failed_pairs", []))
        candidates = [c for c in candidates if (c["source_a"], c["source_b"]) not in done
                      and (c["source_a"], c["source_b"]) not in failed_set]

    if args.limit:
        candidates = candidates[:args.limit]

    logger.info("Processing %d pairs (after filtering done=%d)", len(candidates), len(done))

    # Load source titles from DB
    titles = {}
    with get_conn() as conn:
        rows = conn.execute("SELECT id, title FROM sources").fetchall()
        for row in rows:
            titles[row["id"]] = row["title"]

    # Pre-load all needed summaries to avoid repeated disk I/O
    needed_ids = set()
    for c in candidates:
        needed_ids.add(c["source_a"])
        needed_ids.add(c["source_b"])
    summary_cache = {}
    for sid in needed_ids:
        summary_cache[sid] = get_source_summary(sid, LIBRARY_PATH)
    logger.info("Pre-loaded %d summaries (%d non-null)", len(summary_cache), sum(1 for v in summary_cache.values() if v))

    edges_created = progress.get("edges_created", 0)
    skipped = progress.get("skipped", 0)
    failed = progress.get("failed", 0)

    batch_size = max(1, args.batch_size)
    batch_id = 0

    # Process in batches
    for batch_start in range(0, len(candidates), batch_size):
        batch_candidates = candidates[batch_start:batch_start + batch_size]

        # Build batch input, skipping pairs without summaries
        batch_pairs = []
        batch_candidate_map = []  # tracks which candidates have summaries
        for candidate in batch_candidates:
            source_a = candidate["source_a"]
            source_b = candidate["source_b"]
            summary_a = summary_cache.get(source_a)
            summary_b = summary_cache.get(source_b)

            if not summary_a or not summary_b:
                skipped += 1
                progress["skipped_pairs"].append([source_a, source_b])
                continue

            batch_pairs.append({
                "title_a": titles.get(source_a, source_a),
                "summary_a": summary_a,
                "title_b": titles.get(source_b, source_b),
                "summary_b": summary_b,
                "shared_concepts": candidate.get("shared_concepts", []),
            })
            batch_candidate_map.append(candidate)

        if not batch_pairs:
            continue

        # Run batch classification
        session_name = f"edge_batch_{batch_id}"
        results = classify_edge_batch(batch_pairs, executor, batch_id=batch_id)
        batch_id += 1

        # Detect full-batch failure (all results have errors)
        all_failed = all(isinstance(r, dict) and "error" in r for r in results)

        if all_failed and len(batch_pairs) > 1:
            # Fallback: retry each pair individually
            logger.info("Batch %d failed entirely, retrying %d pairs individually", batch_id - 1, len(batch_pairs))
            individual_results = []
            for i, (pair, candidate) in enumerate(zip(batch_pairs, batch_candidate_map)):
                single = classify_edge(
                    pair["title_a"], pair["summary_a"],
                    pair["title_b"], pair["summary_b"],
                    pair.get("shared_concepts", []),
                    executor, pair_index=batch_id * 1000 + i,
                )
                individual_results.append(single)
                if args.delay > 0:
                    time.sleep(args.delay)
            results = individual_results

        for idx, (result, candidate) in enumerate(zip(results, batch_candidate_map)):
            source_a = candidate["source_a"]
            source_b = candidate["source_b"]
            title_a = titles.get(source_a, source_a)
            title_b = titles.get(source_b, source_b)
            pair_num = batch_start + idx + 1

            if result is None:
                # No relationship
                skipped += 1
                progress["completed_pairs"].append([source_a, source_b])
            elif "error" in result:
                # CLI or parse failure — track separately for retry
                failed += 1
                progress["failed_pairs"].append([source_a, source_b])
                logger.warning(
                    "[%d/%d] FAILED: %s <-> %s: %s",
                    pair_num, len(candidates),
                    title_a[:40], title_b[:40], result["error"],
                )
            else:
                # Success
                insert_source_edge(
                    source_a=source_a,
                    source_b=source_b,
                    edge_type=result["edge_type"],
                    explanation=result["explanation"],
                    evidence_a=result.get("evidence_a"),
                    evidence_b=result.get("evidence_b"),
                    confidence=result["confidence"],
                )
                edges_created += 1
                progress["completed_pairs"].append([source_a, source_b])
                logger.info(
                    "[%d/%d] Edge: %s -[%s]-> %s (%.2f)",
                    pair_num, len(candidates),
                    title_a[:40], result["edge_type"], title_b[:40],
                    result["confidence"],
                )

        progress["edges_created"] = edges_created
        progress["skipped"] = skipped
        progress["failed"] = failed

        # Save progress after each batch
        save_progress(progress)

        # Clean up batch session directory
        cleanup_session_dir(DEFAULT_WORKSPACE, session_name)

        if args.delay > 0 and batch_start + batch_size < len(candidates):
            time.sleep(args.delay)

    save_progress(progress)
    logger.info(
        "Edge computation complete: %d edges created, %d skipped (no relationship), "
        "%d failed (retryable via --retry-failed), %d total pairs",
        edges_created, skipped, failed, len(candidates),
    )


if __name__ == "__main__":
    main()
