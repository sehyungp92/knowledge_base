"""Backfill anticipation matching on existing library sources.

Sources ingested before anticipations existed have landscape.json files
but were never checked against open anticipations. This script runs
match_anticipations() + persist_anticipation_matches() on each source
using the already-extracted landscape signals on disk.

Processes newest-first (post-anticipation sources are highest value).

Usage:
    python -m scripts.backfill_anticipation_matching [--limit N] [--delay SECS]
           [--resume] [--theme THEME] [--dry-run] [--verbose]
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from pathlib import Path

logger = logging.getLogger(__name__)

PROGRESS_FILE = Path(__file__).parent / "anticipation_match_progress.json"


def _load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {"processed": [], "matched": 0, "total_evidence": 0}


def _save_progress(progress: dict):
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2), encoding="utf-8")


def backfill(
    limit: int | None = None,
    delay: float = 2.0,
    resume: bool = False,
    theme_filter: str | None = None,
    dry_run: bool = False,
):
    from reading_app.config import Config
    from reading_app.db import init_pool, get_conn

    config = Config()
    init_pool(config.postgres_dsn)

    progress = _load_progress() if resume else {"processed": [], "matched": 0, "total_evidence": 0}
    already_done = set(progress["processed"])

    # Get sources with landscape.json, newest first
    with get_conn() as conn:
        query = """
            SELECT s.id, s.library_path, s.published_at, s.ingested_at
            FROM sources s
            WHERE s.library_path IS NOT NULL
            ORDER BY s.ingested_at DESC NULLS LAST
        """
        sources = conn.execute(query).fetchall()

    # Filter to those with landscape.json on disk
    # library_path is typically just "library"; actual files are at library/{source_id}/
    base_dir = Path(__file__).resolve().parent.parent
    eligible = []
    for s in sources:
        lib_path = s.get("library_path")
        if not lib_path:
            continue
        source_dir = base_dir / lib_path / s["id"]
        landscape_file = source_dir / "landscape.json"
        if not landscape_file.exists():
            continue
        if s["id"] in already_done:
            continue
        eligible.append({**s, "_landscape_file": str(landscape_file)})

    logger.info(
        "Found %d eligible sources (%d already processed, %d total with landscape.json)",
        len(eligible), len(already_done), len(eligible) + len(already_done),
    )

    if theme_filter:
        # Filter to sources matching a specific theme
        with get_conn() as conn:
            theme = conn.execute(
                "SELECT id FROM themes WHERE id = %s OR name ILIKE %s LIMIT 1",
                (theme_filter, f"%{theme_filter}%"),
            ).fetchone()
        if not theme:
            logger.error("Theme not found: %s", theme_filter)
            return
        theme_id = theme["id"]
        with get_conn() as conn:
            themed_source_ids = {
                r["source_id"] for r in conn.execute(
                    "SELECT source_id FROM source_themes WHERE theme_id = %s",
                    (theme_id,),
                ).fetchall()
            }
        eligible = [s for s in eligible if s["id"] in themed_source_ids]
        logger.info("Filtered to %d sources for theme %s", len(eligible), theme_id)

    if limit:
        eligible = eligible[:limit]

    processed = 0
    matched_total = 0

    for i, source in enumerate(eligible):
        source_id = source["id"]
        landscape_file = Path(source["_landscape_file"])

        if dry_run:
            logger.info("[DRY RUN] [%d/%d] Would process: %s", i + 1, len(eligible), source_id)
            processed += 1
            continue

        try:
            signals = json.loads(landscape_file.read_text(encoding="utf-8"))
        except Exception:
            logger.warning("Failed to read landscape.json for %s", source_id, exc_info=True)
            continue

        # Get source themes
        with get_conn() as conn:
            theme_rows = conn.execute(
                "SELECT theme_id FROM source_themes WHERE source_id = %s",
                (source_id,),
            ).fetchall()
        source_themes = [r["theme_id"] for r in theme_rows]

        if not source_themes:
            logger.debug("Skipping %s: no themes", source_id)
            progress["processed"].append(source_id)
            continue

        published_at = source.get("published_at")
        if published_at:
            published_at = str(published_at)[:10]

        try:
            from ingest.anticipation_matcher import match_anticipations, persist_anticipation_matches

            matches = match_anticipations(
                extracted_signals=signals,
                source_themes=source_themes,
                source_id=source_id,
                published_at=published_at,
            )

            if matches:
                count = persist_anticipation_matches(matches, source_id)
                matched_total += count
                logger.info(
                    "[%d/%d] %s: %d matches persisted",
                    i + 1, len(eligible), source_id, count,
                )
            else:
                logger.info(
                    "[%d/%d] %s: no matches",
                    i + 1, len(eligible), source_id,
                )

            processed += 1
            progress["processed"].append(source_id)
            progress["matched"] += len(matches)
            progress["total_evidence"] += len(matches)
            _save_progress(progress)

        except Exception:
            logger.error("Failed to process %s", source_id, exc_info=True)

        if delay and i < len(eligible) - 1:
            time.sleep(delay)

    logger.info(
        "Backfill complete: %d processed, %d evidence matches persisted",
        processed, matched_total,
    )


def main():
    parser = argparse.ArgumentParser(description="Backfill anticipation matching on existing sources")
    parser.add_argument("--limit", type=int, default=None, help="Max sources to process")
    parser.add_argument("--delay", type=float, default=2.0, help="Seconds between sources")
    parser.add_argument("--resume", action="store_true", help="Resume from progress file")
    parser.add_argument("--theme", type=str, default=None, help="Filter to a specific theme")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    backfill(
        limit=args.limit,
        delay=args.delay,
        resume=args.resume,
        theme_filter=args.theme,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
