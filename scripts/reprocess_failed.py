"""Reprocess sources that failed during bulk ingestion.

Identifies and fixes sources with missing claims, truncated summaries,
empty landscape signals, or missing theme assignments.

Usage:
    python -m scripts.reprocess_failed --claims     # Re-extract claims
    python -m scripts.reprocess_failed --summaries   # Re-generate summaries
    python -m scripts.reprocess_failed --landscape   # Re-extract landscape signals
    python -m scripts.reprocess_failed --themes      # Classify missing themes
    python -m scripts.reprocess_failed --all         # Run all modes sequentially
    python -m scripts.reprocess_failed --scan        # Scan only, report counts
"""

from __future__ import annotations

import argparse
import json
import logging
import time
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

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LIBRARY_PATH = PROJECT_ROOT / "library"
PROGRESS_FILE = PROJECT_ROOT / "scripts" / "reprocess_progress.json"


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        try:
            text = PROGRESS_FILE.read_text(encoding="utf-8").strip()
            if text:
                return json.loads(text)
        except (json.JSONDecodeError, OSError):
            logger.warning("Corrupted progress file, resetting")
    return {"claims": [], "summaries": [], "landscape": [], "themes": [], "errors": []}


def save_progress(progress: dict):
    tmp = PROGRESS_FILE.with_suffix(".tmp")
    tmp.write_text(
        json.dumps(progress, indent=2, default=str), encoding="utf-8",
    )
    tmp.replace(PROGRESS_FILE)


def _failed_step_source_ids(step: str, get_conn_fn) -> set[str]:
    """Return source IDs with an explicit failed status for a tracked step."""
    try:
        with get_conn_fn() as conn:
            rows = conn.execute(
                """SELECT source_id
                   FROM post_processing_status
                   WHERE step = %s AND status = 'failed'""",
                (step,),
            ).fetchall()
        return {row["source_id"] for row in rows}
    except Exception:
        return set()


# ── Scanners ──────────────────────────────────────────────────────────


def scan_missing_claims(get_conn_fn) -> list[dict]:
    """Find sources with zero claims in DB."""
    failed_ids = _failed_step_source_ids("claims", get_conn_fn)
    with get_conn_fn() as conn:
        rows = conn.execute("""
            SELECT s.id, s.title, s.source_type, s.url, s.authors, s.published_at
            FROM sources s
            WHERE s.id = ANY(%s)
               OR NOT EXISTS (SELECT 1 FROM claims c WHERE c.source_id = s.id)
            ORDER BY s.ingested_at
        """, (list(failed_ids),)).fetchall()
    return [dict(r) for r in rows]


def scan_truncated_summaries(get_conn_fn) -> list[str]:
    """Find sources with truncated or failed deep summaries."""
    needs_fix = set(_failed_step_source_ids("summary", get_conn_fn))
    for source_dir in sorted(LIBRARY_PATH.iterdir()):
        if not source_dir.is_dir():
            continue
        summary_path = source_dir / "deep_summary.md"
        if not summary_path.exists():
            needs_fix.add(source_dir.name)
            continue
        try:
            content = summary_path.read_text(encoding="utf-8")
            if get_summary_issue(content) is not None:
                needs_fix.add(source_dir.name)
        except Exception:
            needs_fix.add(source_dir.name)
    return sorted(needs_fix)


def scan_empty_landscape(get_conn_fn) -> list[str]:
    """Find sources with empty landscape.json."""
    needs_fix = set(_failed_step_source_ids("landscape", get_conn_fn))
    for source_dir in sorted(LIBRARY_PATH.iterdir()):
        if not source_dir.is_dir():
            continue
        landscape_path = source_dir / "landscape.json"
        if not landscape_path.exists():
            needs_fix.add(source_dir.name)
            continue
        try:
            data = json.loads(landscape_path.read_text(encoding="utf-8"))
            if get_landscape_issue(data) is not None:
                needs_fix.add(source_dir.name)
        except Exception:
            needs_fix.add(source_dir.name)
    return sorted(needs_fix)


def scan_missing_themes(get_conn_fn) -> list[dict]:
    """Find sources with no theme assignments."""
    failed_ids = _failed_step_source_ids("themes", get_conn_fn)
    with get_conn_fn() as conn:
        rows = conn.execute("""
            SELECT s.id, s.title, s.source_type
            FROM sources s
            WHERE s.id = ANY(%s)
               OR NOT EXISTS (SELECT 1 FROM source_themes st WHERE st.source_id = s.id)
            ORDER BY s.ingested_at
        """, (list(failed_ids),)).fetchall()
    return [dict(r) for r in rows]


# ── Reprocessors ──────────────────────────────────────────────────────


def reprocess_claims(
    get_conn_fn, executor, delay: float = 3.0, limit: int | None = None,
):
    """Re-extract claims for sources that have zero."""
    from ingest.extractor import extract_claims
    from ingest.http_retry import with_retry
    from ingest.claim_persistence import persist_extractions_to_db
    from agents.executor import get_circuit_breaker

    cb = get_circuit_breaker()
    progress = load_progress()
    done = set(progress.get("claims", []))

    sources = scan_missing_claims(get_conn_fn)
    sources = [s for s in sources if s["id"] not in done]
    if limit:
        sources = sources[:limit]

    logger.info("Reprocessing claims for %d sources", len(sources))
    total_claims = 0
    consecutive_failures = 0
    adaptive_delay = delay

    for i, source in enumerate(sources):
        if cb.is_open():
            logger.warning("Circuit breaker open, stopping claims reprocessing at %d/%d", i, len(sources))
            save_progress(progress)
            break

        source_id = source["id"]
        clean_path = LIBRARY_PATH / source_id / "clean.md"
        if not clean_path.exists():
            logger.warning("No clean.md for %s, skipping", source_id)
            progress["errors"].append({"source_id": source_id, "mode": "claims", "error": "no clean.md"})
            save_progress(progress)
            continue

        clean_text = clean_path.read_text(encoding="utf-8")
        if len(clean_text) < 100:
            logger.warning("Clean text too short for %s (%d chars)", source_id, len(clean_text))
            continue

        # Load themes for this source
        themes = _get_source_themes(source_id, get_conn_fn)
        ensure_step_rows(source_id, ["claims"], get_conn_fn)
        mark_step_running(source_id, "claims", get_conn_fn)

        try:
            result = with_retry(
                lambda sid=source_id, ct=clean_text, st=source["source_type"], th=themes: extract_claims(
                    source_id=sid,
                    clean_text=ct,
                    source_type=st,
                    executor=executor,
                    library_path=LIBRARY_PATH,
                    themes=th or None,
                ),
                max_attempts=3, base_delay=5.0,
                label=f"reprocess_claims_{source_id}",
                retryable_exceptions=(RuntimeError,),
            )

            claims_count = persist_extractions_to_db(source_id, result)
            total_claims += claims_count
            logger.info(
                "[%d/%d] Claims for %s: %d claims persisted",
                i + 1, len(sources), source_id, claims_count,
            )

            if claims_count == 0:
                logger.warning("Zero claims extracted for %s — not marking as done", source_id)
                mark_step_failed(
                    source_id,
                    "claims",
                    "0 claims extracted",
                    get_conn_fn,
                    result={"claim_count": 0},
                )
                progress["errors"].append({"source_id": source_id, "mode": "claims", "error": "0 claims extracted"})
                save_progress(progress)
                continue

            mark_step_completed(
                source_id,
                "claims",
                get_conn_fn,
                result={
                    "claim_count": claims_count,
                    "concept_count": len(result.get("concepts", [])),
                },
            )
            refresh_source_processing_status(source_id, get_conn_fn, library_path=LIBRARY_PATH)
            progress["claims"].append(source_id)
            consecutive_failures = 0
            adaptive_delay = delay
            if (i + 1) % 5 == 0:
                save_progress(progress)

        except Exception as e:
            logger.error("Claims extraction failed for %s: %s", source_id, e)
            mark_step_failed(source_id, "claims", str(e), get_conn_fn)
            progress["errors"].append({"source_id": source_id, "mode": "claims", "error": str(e)[:200]})
            save_progress(progress)
            consecutive_failures += 1
            adaptive_delay = min(delay * (2 ** consecutive_failures), 60.0)

        if adaptive_delay > 0 and i < len(sources) - 1:
            time.sleep(adaptive_delay)

    save_progress(progress)
    logger.info("Claims reprocessing complete: %d total claims extracted", total_claims)


def reprocess_summaries(
    get_conn_fn, executor, delay: float = 3.0, limit: int | None = None,
):
    """Re-generate truncated deep summaries."""
    from ingest.deep_summarizer import generate_deep_summary
    from ingest.http_retry import with_retry
    from agents.executor import get_circuit_breaker

    cb = get_circuit_breaker()
    progress = load_progress()
    done = set(progress.get("summaries", []))

    source_ids = scan_truncated_summaries(get_conn_fn)
    source_ids = [sid for sid in source_ids if sid not in done]
    if limit:
        source_ids = source_ids[:limit]

    logger.info("Reprocessing summaries for %d sources", len(source_ids))
    consecutive_failures = 0
    adaptive_delay = delay

    for i, source_id in enumerate(source_ids):
        if cb.is_open():
            logger.warning("Circuit breaker open, stopping summary reprocessing at %d/%d", i, len(source_ids))
            save_progress(progress)
            break

        clean_path = LIBRARY_PATH / source_id / "clean.md"
        if not clean_path.exists():
            logger.warning("No clean.md for %s, skipping", source_id)
            ensure_step_rows(source_id, ["landscape"], get_conn_fn)
            mark_step_failed(source_id, "landscape", "no clean.md", get_conn_fn)
            progress["errors"].append({"source_id": source_id, "mode": "landscape", "error": "no clean.md"})
            save_progress(progress)
            continue

        clean_text = clean_path.read_text(encoding="utf-8")
        meta = _get_source_meta(source_id, get_conn_fn)
        themes = _get_source_themes(source_id, get_conn_fn)
        ensure_step_rows(source_id, ["summary"], get_conn_fn)
        mark_step_running(source_id, "summary", get_conn_fn)

        try:
            summary = with_retry(
                lambda sid=source_id, ct=clean_text, m=meta, th=themes: generate_deep_summary(
                    source_id=sid,
                    clean_text=ct,
                    title=m.get("title", ""),
                    source_type=m.get("source_type", "article"),
                    url=m.get("url"),
                    authors=m.get("authors"),
                    published_at=str(m["published_at"]) if m.get("published_at") else None,
                    executor=executor,
                    library_path=LIBRARY_PATH,
                    themes=th or None,
                ),
                max_attempts=3, base_delay=5.0,
                label=f"reprocess_summary_{source_id}",
                retryable_exceptions=(RuntimeError,),
            )

            logger.info(
                "[%d/%d] Summary for %s: %d chars",
                i + 1, len(source_ids), source_id, len(summary),
            )

            summary_issue = get_summary_issue(summary)
            if summary_issue is not None:
                mark_step_failed(
                    source_id,
                    "summary",
                    f"Invalid summary output: {summary_issue}",
                    get_conn_fn,
                    result={"summary_chars": len(summary), "issue": summary_issue},
                )
                progress["errors"].append({"source_id": source_id, "mode": "summaries", "error": summary_issue})
                save_progress(progress)
                continue

            mark_step_completed(
                source_id,
                "summary",
                get_conn_fn,
                result={"summary_chars": len(summary)},
            )
            refresh_source_processing_status(source_id, get_conn_fn, library_path=LIBRARY_PATH)
            progress["summaries"].append(source_id)
            consecutive_failures = 0
            adaptive_delay = delay
            if (i + 1) % 5 == 0:
                save_progress(progress)

        except Exception as e:
            logger.error("Summary generation failed for %s: %s", source_id, e)
            mark_step_failed(source_id, "summary", str(e), get_conn_fn)
            progress["errors"].append({"source_id": source_id, "mode": "summaries", "error": str(e)[:200]})
            save_progress(progress)
            consecutive_failures += 1
            adaptive_delay = min(delay * (2 ** consecutive_failures), 60.0)

        if adaptive_delay > 0 and i < len(source_ids) - 1:
            time.sleep(adaptive_delay)

    save_progress(progress)
    logger.info("Summary reprocessing complete")


def reprocess_landscape(
    get_conn_fn, executor, delay: float = 3.0, limit: int | None = None,
):
    """Re-extract landscape signals for sources with empty landscape."""
    from ingest.landscape_extractor import (
        extract_landscape_signals,
        persist_landscape_signals,
        save_landscape_json,
    )
    from ingest.http_retry import with_retry
    from agents.executor import get_circuit_breaker

    cb = get_circuit_breaker()
    progress = load_progress()
    done = set(progress.get("landscape", []))

    source_ids = scan_empty_landscape(get_conn_fn)
    source_ids = [sid for sid in source_ids if sid not in done]
    if limit:
        source_ids = source_ids[:limit]

    logger.info("Reprocessing landscape for %d sources", len(source_ids))
    consecutive_failures = 0
    adaptive_delay = delay

    for i, source_id in enumerate(source_ids):
        if cb.is_open():
            logger.warning("Circuit breaker open, stopping landscape reprocessing at %d/%d", i, len(source_ids))
            save_progress(progress)
            break

        clean_path = LIBRARY_PATH / source_id / "clean.md"
        if not clean_path.exists():
            logger.warning("No clean.md for %s, skipping", source_id)
            ensure_step_rows(source_id, ["landscape"], get_conn_fn)
            mark_step_failed(source_id, "landscape", "no clean.md", get_conn_fn)
            progress["errors"].append({"source_id": source_id, "mode": "landscape", "error": "no clean.md"})
            save_progress(progress)
            continue

        clean_text = clean_path.read_text(encoding="utf-8")
        meta = _get_source_meta(source_id, get_conn_fn)
        themes = _get_source_themes(source_id, get_conn_fn)
        theme_ids = [t["theme_id"] for t in themes] if themes else None
        ensure_step_rows(source_id, ["landscape"], get_conn_fn)
        mark_step_running(source_id, "landscape", get_conn_fn)

        try:
            signals = with_retry(
                lambda sid=source_id, ct=clean_text, ti=theme_ids, m=meta: extract_landscape_signals(
                    clean_text=ct,
                    source_id=sid,
                    source_themes=ti,
                    published_at=str(m["published_at"]) if m.get("published_at") else None,
                    executor=executor,
                    source_type=m.get("source_type"),
                ),
                max_attempts=3, base_delay=5.0,
                label=f"reprocess_landscape_{source_id}",
                retryable_exceptions=(RuntimeError,),
            )

            if signals:
                delta = persist_landscape_signals(signals, source_id, get_conn_fn=get_conn_fn)
                save_landscape_json(signals, LIBRARY_PATH / source_id)
                counts = delta.counts if delta else {}
            else:
                counts = {}

            logger.info(
                "[%d/%d] Landscape for %s: %s",
                i + 1, len(source_ids), source_id, counts,
            )

            landscape_issue = get_landscape_issue(signals)
            if landscape_issue is not None:
                mark_step_failed(
                    source_id,
                    "landscape",
                    f"Invalid landscape output: {landscape_issue}",
                    get_conn_fn,
                    result={"signal_counts": counts, "issue": landscape_issue},
                )
                progress["errors"].append({"source_id": source_id, "mode": "landscape", "error": landscape_issue})
                save_progress(progress)
                continue

            # Don't mark as done if all signal types are empty
            total_signals = sum(counts.get(k, 0) for k in ("capabilities", "limitations", "bottlenecks", "breakthroughs"))
            if total_signals == 0:
                logger.warning("Zero landscape signals for %s — not marking as done", source_id)
                progress["errors"].append({"source_id": source_id, "mode": "landscape", "error": "0 signals extracted"})
                save_progress(progress)
                continue

            mark_step_completed(
                source_id,
                "landscape",
                get_conn_fn,
                result={"signal_counts": counts},
            )
            refresh_source_processing_status(source_id, get_conn_fn, library_path=LIBRARY_PATH)
            progress["landscape"].append(source_id)
            consecutive_failures = 0
            adaptive_delay = delay
            if (i + 1) % 5 == 0:
                save_progress(progress)

        except Exception as e:
            logger.error("Landscape extraction failed for %s: %s", source_id, e)
            mark_step_failed(source_id, "landscape", str(e), get_conn_fn)
            progress["errors"].append({"source_id": source_id, "mode": "landscape", "error": str(e)[:200]})
            save_progress(progress)
            consecutive_failures += 1
            adaptive_delay = min(delay * (2 ** consecutive_failures), 60.0)

        if adaptive_delay > 0 and i < len(source_ids) - 1:
            time.sleep(adaptive_delay)

    save_progress(progress)
    logger.info("Landscape reprocessing complete")


def reprocess_themes(
    get_conn_fn, executor, delay: float = 3.0, limit: int | None = None,
):
    """Classify themes for sources missing theme assignments."""
    from ingest.theme_classifier import classify_themes
    from ingest.http_retry import with_retry
    from agents.executor import get_circuit_breaker

    cb = get_circuit_breaker()
    progress = load_progress()
    done = set(progress.get("themes", []))

    sources = scan_missing_themes(get_conn_fn)
    sources = [s for s in sources if s["id"] not in done]
    if limit:
        sources = sources[:limit]

    logger.info("Reprocessing themes for %d sources", len(sources))
    consecutive_failures = 0
    adaptive_delay = delay

    for i, source in enumerate(sources):
        if cb.is_open():
            logger.warning("Circuit breaker open, stopping theme reprocessing at %d/%d", i, len(sources))
            save_progress(progress)
            break

        source_id = source["id"]
        clean_path = LIBRARY_PATH / source_id / "clean.md"
        if not clean_path.exists():
            logger.warning("No clean.md for %s, skipping", source_id)
            ensure_step_rows(source_id, ["themes"], get_conn_fn)
            mark_step_failed(source_id, "themes", "no clean.md", get_conn_fn)
            progress["errors"].append({"source_id": source_id, "mode": "themes", "error": "no clean.md"})
            save_progress(progress)
            continue

        clean_text = clean_path.read_text(encoding="utf-8")
        ensure_step_rows(source_id, ["themes"], get_conn_fn)
        mark_step_running(source_id, "themes", get_conn_fn)

        try:
            themes = with_retry(
                lambda sid=source_id, ct=clean_text: classify_themes(
                    ct, sid, executor=executor, get_conn_fn=get_conn_fn,
                ),
                max_attempts=2, base_delay=5.0,
                label=f"reprocess_themes_{source_id}",
                retryable_exceptions=(RuntimeError,),
            )

            theme_ids = [t.get("theme_id") for t in themes if "theme_id" in t]
            logger.info(
                "[%d/%d] Themes for %s: %s",
                i + 1, len(sources), source_id, theme_ids,
            )

            if not theme_ids:
                mark_step_failed(
                    source_id,
                    "themes",
                    "No themes classified",
                    get_conn_fn,
                    result={"theme_count": 0},
                )
                progress["errors"].append({"source_id": source_id, "mode": "themes", "error": "No themes classified"})
                save_progress(progress)
                continue

            mark_step_completed(
                source_id,
                "themes",
                get_conn_fn,
                result={"theme_count": len(theme_ids), "theme_ids": theme_ids},
            )
            refresh_source_processing_status(source_id, get_conn_fn, library_path=LIBRARY_PATH)
            progress["themes"].append(source_id)
            consecutive_failures = 0
            adaptive_delay = delay
            if (i + 1) % 5 == 0:
                save_progress(progress)

        except Exception as e:
            logger.error("Theme classification failed for %s: %s", source_id, e)
            mark_step_failed(source_id, "themes", str(e), get_conn_fn)
            progress["errors"].append({"source_id": source_id, "mode": "themes", "error": str(e)[:200]})
            save_progress(progress)
            consecutive_failures += 1
            adaptive_delay = min(delay * (2 ** consecutive_failures), 60.0)

        if adaptive_delay > 0 and i < len(sources) - 1:
            time.sleep(adaptive_delay)

    save_progress(progress)
    logger.info("Theme reprocessing complete")


# ── Helpers ───────────────────────────────────────────────────────────


def _get_source_meta(source_id: str, get_conn_fn) -> dict:
    """Get source metadata from DB."""
    with get_conn_fn() as conn:
        row = conn.execute(
            "SELECT title, source_type, url, authors, published_at FROM sources WHERE id = %s",
            (source_id,),
        ).fetchone()
    return dict(row) if row else {}


def _get_source_themes(source_id: str, get_conn_fn) -> list[dict]:
    """Get theme assignments for a source."""
    with get_conn_fn() as conn:
        rows = conn.execute(
            "SELECT theme_id, relevance FROM source_themes WHERE source_id = %s",
            (source_id,),
        ).fetchall()
    return [dict(r) for r in rows]


# ── Scan mode ─────────────────────────────────────────────────────────


def scan_report(get_conn_fn):
    """Print a report of what needs reprocessing."""
    missing_claims = scan_missing_claims(get_conn_fn)
    truncated_summaries = scan_truncated_summaries(get_conn_fn)
    empty_landscape = scan_empty_landscape(get_conn_fn)
    missing_themes = scan_missing_themes(get_conn_fn)

    print("\n=== Reprocess Scan Report ===\n")
    print(f"  Sources with 0 claims:       {len(missing_claims)}")
    print(f"  Truncated/failed summaries:  {len(truncated_summaries)}")
    print(f"  Empty landscape signals:     {len(empty_landscape)}")
    print(f"  Missing theme assignments:   {len(missing_themes)}")
    print()

    if missing_claims:
        print("Sample sources needing claims:")
        for s in missing_claims[:5]:
            print(f"    {s['id']}  {s.get('title', '')[:60]}")

    if truncated_summaries:
        print("Sample sources needing summaries:")
        for sid in truncated_summaries[:5]:
            print(f"    {sid}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Reprocess failed ingestions")
    parser.add_argument("--claims", action="store_true", help="Re-extract claims")
    parser.add_argument("--summaries", action="store_true", help="Re-generate summaries")
    parser.add_argument("--landscape", action="store_true", help="Re-extract landscape signals")
    parser.add_argument("--themes", action="store_true", help="Classify missing themes")
    parser.add_argument("--all", action="store_true", help="Run all modes")
    parser.add_argument("--scan", action="store_true", help="Scan and report only")
    parser.add_argument("--delay", type=float, default=3.0, help="Seconds between API calls")
    parser.add_argument("--limit", type=int, default=None, help="Max sources per mode")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    from reading_app.config import Config
    from reading_app.db import init_pool, get_conn
    from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE

    config = Config()
    init_pool(config.postgres_dsn)

    if args.scan:
        scan_report(get_conn)
        return

    if not any([args.claims, args.summaries, args.landscape, args.themes, args.all]):
        parser.print_help()
        return

    executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    if args.all or args.themes:
        reprocess_themes(get_conn, executor, delay=args.delay, limit=args.limit)

    if args.all or args.claims:
        reprocess_claims(get_conn, executor, delay=args.delay, limit=args.limit)

    if args.all or args.summaries:
        reprocess_summaries(get_conn, executor, delay=args.delay, limit=args.limit)

    if args.all or args.landscape:
        reprocess_landscape(get_conn, executor, delay=args.delay, limit=args.limit)

    print("\nReprocessing complete. Run --scan to verify results.")


if __name__ == "__main__":
    main()
