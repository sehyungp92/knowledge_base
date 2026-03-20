"""Reprocess sources that have valid clean.md content but 0 claims in the DB.

Finds ~119 sources where the claims extraction step failed or was skipped
during initial ingestion, but the source has real (non-stub, non-paywall)
content on disk. Re-runs claims extraction + landscape extraction for each.

Usage:
    python -m scripts.reprocess_claimless --dry-run          # List what would be processed
    python -m scripts.reprocess_claimless --limit 5          # Process first 5
    python -m scripts.reprocess_claimless                    # Process all
    python -m scripts.reprocess_claimless --skip-landscape   # Claims only
    python -m scripts.reprocess_claimless --resume           # Skip already-completed
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import threading
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LIBRARY_PATH = PROJECT_ROOT / "library"
PROGRESS_FILE = PROJECT_ROOT / "scripts" / "reprocess_claimless_progress.json"

# Minimum char count for clean.md to be considered valid content.
# The bulk_ingest pipeline uses 100; we use a slightly higher threshold
# to also skip borderline stubs.
MIN_CONTENT_LENGTH = 200

# Patterns that indicate paywall-blocked, stub, or failed fetch content.
# If any pattern matches (case-insensitive), the clean.md is considered invalid.
STUB_PATTERNS = [
    r"subscribe to (continue|read|unlock|access)",
    r"this (content|article|story) is (only )?available (to|for) (paid )?subscribers",
    r"you('ve| have) (reached|hit) your (free )?(article )?limit",
    r"sign in to (continue|read|access)",
    r"create (a free |an )?account to (continue|read)",
    r"please (log|sign) in",
    r"members[- ]only",
    r"premium (content|article|subscribers)",
    r"paywall",
    r"403 forbidden",
    r"404 not found",
    r"access denied",
    r"page not found",
    r"javascript is (required|not enabled|disabled)",
    r"enable javascript",
    r"this page requires javascript",
    r"we noticed you('re| are) using an ad.?blocker",
    r"summary (generation failed|pending)",
    r"failed to fetch",
    r"error fetching",
    r"cloudflare",
    r"just a moment\.\.\.",  # Cloudflare challenge page
    r"checking your browser",
    r"verify you are human",
    r"captcha",
]
_STUB_RE = re.compile("|".join(STUB_PATTERNS), re.IGNORECASE)


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        try:
            text = PROGRESS_FILE.read_text(encoding="utf-8").strip()
            if text:
                return json.loads(text)
        except (json.JSONDecodeError, OSError):
            logger.warning("Corrupted progress file, resetting")
    return {"completed": [], "errors": []}


def save_progress(progress: dict):
    tmp = PROGRESS_FILE.with_suffix(".tmp")
    tmp.write_text(
        json.dumps(progress, indent=2, default=str), encoding="utf-8",
    )
    tmp.replace(PROGRESS_FILE)


# ── Discovery ─────────────────────────────────────────────────────────


def find_claimless_sources(get_conn_fn) -> list[dict]:
    """Find sources in the DB that have 0 claims."""
    with get_conn_fn() as conn:
        rows = conn.execute("""
            SELECT s.id, s.title, s.source_type, s.url, s.authors, s.published_at
            FROM sources s
            WHERE NOT EXISTS (SELECT 1 FROM claims c WHERE c.source_id = s.id)
            ORDER BY s.ingested_at
        """).fetchall()
    return [dict(r) for r in rows]


def is_valid_content(clean_text: str) -> tuple[bool, str]:
    """Check whether clean.md content is real (not a stub/paywall/error page).

    Returns (is_valid, reason) where reason explains rejection.
    """
    if len(clean_text.strip()) < MIN_CONTENT_LENGTH:
        return False, f"too short ({len(clean_text.strip())} chars)"

    # Check for stub/paywall patterns in the first 2000 chars
    # (paywall notices are usually at the top)
    head = clean_text[:2000]
    match = _STUB_RE.search(head)
    if match:
        return False, f"stub pattern matched: '{match.group()[:60]}'"

    # If the content is almost entirely non-alphabetic (e.g. garbled encoding),
    # skip it
    alpha_ratio = sum(1 for c in clean_text if c.isalpha()) / max(len(clean_text), 1)
    if alpha_ratio < 0.3:
        return False, f"low alpha ratio ({alpha_ratio:.2f})"

    return True, "ok"


def discover_reprocessable_sources(get_conn_fn) -> list[dict]:
    """Find sources with 0 claims AND valid clean.md on disk.

    Returns list of source dicts augmented with 'clean_text_length' and
    'library_dir' keys.
    """
    claimless = find_claimless_sources(get_conn_fn)
    logger.info("Found %d sources with 0 claims in DB", len(claimless))

    valid = []
    skipped_no_file = 0
    skipped_invalid = 0

    for source in claimless:
        source_id = source["id"]
        clean_path = LIBRARY_PATH / source_id / "clean.md"

        if not clean_path.exists():
            skipped_no_file += 1
            continue

        try:
            clean_text = clean_path.read_text(encoding="utf-8")
        except Exception:
            skipped_no_file += 1
            continue

        is_ok, reason = is_valid_content(clean_text)
        if not is_ok:
            skipped_invalid += 1
            logger.debug(
                "Skipping %s (%s): %s",
                source_id, source.get("title", "?")[:50], reason,
            )
            continue

        source["clean_text_length"] = len(clean_text)
        source["library_dir"] = str(LIBRARY_PATH / source_id)
        valid.append(source)

    logger.info(
        "Reprocessable: %d valid / %d total claimless "
        "(skipped: %d no file, %d invalid content)",
        len(valid), len(claimless), skipped_no_file, skipped_invalid,
    )
    return valid


# ── Helpers ───────────────────────────────────────────────────────────


def _get_source_themes(source_id: str, get_conn_fn) -> list[dict]:
    """Get theme assignments for a source."""
    with get_conn_fn() as conn:
        rows = conn.execute(
            "SELECT theme_id, relevance FROM source_themes WHERE source_id = %s",
            (source_id,),
        ).fetchall()
    return [dict(r) for r in rows]


# ── Reprocessor ───────────────────────────────────────────────────────


def reprocess_claimless(
    get_conn_fn,
    executor,
    *,
    limit: int | None = None,
    dry_run: bool = False,
    resume: bool = False,
    skip_landscape: bool = False,
    delay: float = 1.0,
    workers: int = 2,
):
    """Reprocess claims + landscape for sources with 0 claims but valid content."""
    from ingest.extractor import extract_claims
    from ingest.landscape_extractor import (
        extract_landscape_signals,
        persist_landscape_signals,
        save_landscape_json,
    )
    from ingest.http_retry import with_retry
    from ingest.claim_persistence import persist_extractions_to_db
    from agents.executor import get_circuit_breaker

    cb = get_circuit_breaker()
    progress = load_progress() if resume else {"completed": [], "errors": []}
    done = set(progress.get("completed", []))

    # Discover sources
    sources = discover_reprocessable_sources(get_conn_fn)

    if resume:
        before = len(sources)
        sources = [s for s in sources if s["id"] not in done]
        if before != len(sources):
            logger.info("Resuming: skipped %d already-completed", before - len(sources))

    if limit:
        sources = sources[:limit]

    # ── Dry run ───────────────────────────────────────────────────────
    if dry_run:
        print(f"\n{'='*70}")
        print(f"  DRY RUN: {len(sources)} sources to reprocess")
        print(f"{'='*70}\n")
        for i, s in enumerate(sources):
            themes = _get_source_themes(s["id"], get_conn_fn)
            theme_ids = [t["theme_id"] for t in themes] if themes else []
            print(
                f"  [{i+1:3d}] {s['id']}  "
                f"{s.get('title', '?')[:55]:55s}  "
                f"{s['clean_text_length']:>6d} chars  "
                f"type={s.get('source_type', '?'):8s}  "
                f"themes={','.join(theme_ids) or '(none)'}"
            )
        print(f"\nRun without --dry-run to process these sources.\n")
        return

    # ── Process ───────────────────────────────────────────────────────
    total = len(sources)
    logger.info(
        "Starting reprocessing: %d sources (skip_landscape=%s, delay=%.1fs, workers=%d)",
        total, skip_landscape, delay, workers,
    )

    total_claims = 0
    total_landscape = 0
    completed_count = 0
    progress_lock = threading.Lock()

    def _process_one(i: int, source: dict) -> tuple[int, int]:
        """Process a single source. Returns (claims_count, landscape_count)."""
        if cb.is_open():
            return 0, 0

        source_id = source["id"]
        title = source.get("title", "?")[:60]

        clean_path = LIBRARY_PATH / source_id / "clean.md"
        clean_text = clean_path.read_text(encoding="utf-8")

        themes = _get_source_themes(source_id, get_conn_fn)
        theme_ids = [t["theme_id"] for t in themes] if themes else None

        logger.info(
            "[%d/%d] Processing %s — %s (%d chars, %s)",
            i + 1, total, source_id, title,
            len(clean_text), source.get("source_type", "?"),
        )

        # ── Claims extraction ─────────────────────────────────────
        claims_count = 0
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
                max_attempts=3,
                base_delay=5.0,
                label=f"claims_{source_id}",
                retryable_exceptions=(RuntimeError,),
            )
            claims_count = persist_extractions_to_db(source_id, result)
            logger.info("  [%s] Claims: %d extracted", source_id[:8], claims_count)
        except Exception as e:
            logger.error("  [%s] Claims extraction FAILED: %s", source_id[:8], e)
            with progress_lock:
                progress["errors"].append({
                    "source_id": source_id,
                    "step": "claims",
                    "error": str(e)[:200],
                })
            return 0, 0

        if claims_count == 0:
            logger.warning("  [%s] Zero claims extracted", source_id[:8])
            with progress_lock:
                progress["errors"].append({
                    "source_id": source_id,
                    "step": "claims",
                    "error": "0 claims extracted",
                })

        # ── Landscape extraction ──────────────────────────────────
        landscape_count = 0
        if not skip_landscape:
            try:
                signals = with_retry(
                    lambda sid=source_id, ct=clean_text, ti=theme_ids, s=source: extract_landscape_signals(
                        clean_text=ct,
                        source_id=sid,
                        source_themes=ti,
                        published_at=str(s["published_at"]) if s.get("published_at") else None,
                        executor=executor,
                        source_type=s.get("source_type"),
                    ),
                    max_attempts=3,
                    base_delay=5.0,
                    label=f"landscape_{source_id}",
                    retryable_exceptions=(RuntimeError,),
                )

                if signals:
                    delta = persist_landscape_signals(signals, source_id, get_conn_fn=get_conn_fn)
                    save_landscape_json(signals, LIBRARY_PATH / source_id)
                    counts = delta.counts if delta else {}
                    landscape_count = sum(
                        counts.get(k, 0)
                        for k in ("capabilities", "limitations", "bottlenecks", "breakthroughs")
                    )
                    logger.info("  [%s] Landscape: %s", source_id[:8], counts)

            except Exception as e:
                logger.error("  [%s] Landscape extraction FAILED: %s", source_id[:8], e)
                with progress_lock:
                    progress["errors"].append({
                        "source_id": source_id,
                        "step": "landscape",
                        "error": str(e)[:200],
                    })

        # ── Update source processing status ───────────────────────
        if claims_count > 0:
            try:
                with get_conn_fn() as conn:
                    conn.execute(
                        "UPDATE sources SET processing_status = 'complete' WHERE id = %s",
                        (source_id,),
                    )
                    conn.commit()
            except Exception:
                logger.debug("Failed to update processing status for %s", source_id, exc_info=True)

        # ── Track progress ────────────────────────────────────────
        with progress_lock:
            if claims_count > 0:
                progress["completed"].append(source_id)
            completed_so_far = len(progress["completed"])

        if completed_so_far % 5 == 0:
            with progress_lock:
                save_progress(progress)

        return claims_count, landscape_count

    # ── Parallel execution ────────────────────────────────────────
    if workers <= 1:
        for i, source in enumerate(sources):
            if cb.is_open():
                logger.warning("Circuit breaker open at %d/%d, stopping.", i, total)
                break
            c, l = _process_one(i, source)
            total_claims += c
            total_landscape += l
            if delay > 0 and i < total - 1:
                time.sleep(delay)
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {}
            for i, source in enumerate(sources):
                if cb.is_open():
                    break
                fut = pool.submit(_process_one, i, source)
                futures[fut] = source
                # Stagger submissions to avoid API saturation
                if delay > 0 and i < total - 1:
                    time.sleep(delay)

            for fut in as_completed(futures):
                try:
                    c, l = fut.result()
                    total_claims += c
                    total_landscape += l
                    completed_count += 1
                except Exception as e:
                    logger.error("Worker exception: %s", e)

    save_progress(progress)

    print(f"\n{'='*60}")
    print(f"  Reprocessing complete")
    print(f"{'='*60}")
    print(f"  Processed:        {total}")
    print(f"  Completed:        {len(progress['completed'])}")
    print(f"  Total claims:     {total_claims}")
    print(f"  Total landscape:  {total_landscape}")
    print(f"  Errors:           {len(progress['errors'])}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Reprocess sources with 0 claims but valid clean.md content",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="List sources that would be processed, without running extraction",
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Max number of sources to process",
    )
    parser.add_argument(
        "--resume", action="store_true",
        help="Skip sources already completed in a previous run",
    )
    parser.add_argument(
        "--skip-landscape", action="store_true",
        help="Only extract claims, skip landscape signals",
    )
    parser.add_argument(
        "--delay", type=float, default=1.0,
        help="Seconds between sources (default 1.0)",
    )
    parser.add_argument(
        "--workers", type=int, default=2,
        help="Number of parallel workers (default 2)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true",
        help="Enable debug logging",
    )
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

    # Refresh theme classifier cache so extraction prompts use current taxonomy
    try:
        from ingest.theme_classifier import refresh_static_theme_block
        refresh_static_theme_block(get_conn)
        logger.info("Theme block refreshed from DB")
    except Exception as e:
        logger.warning("Could not refresh theme block: %s", e)

    if args.dry_run:
        # Dry run does not need an executor
        reprocess_claimless(
            get_conn_fn=get_conn,
            executor=None,
            limit=args.limit,
            dry_run=True,
        )
        return

    executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    reprocess_claimless(
        get_conn_fn=get_conn,
        executor=executor,
        limit=args.limit,
        dry_run=False,
        resume=args.resume,
        skip_landscape=args.skip_landscape,
        delay=args.delay,
        workers=args.workers,
    )


if __name__ == "__main__":
    main()
