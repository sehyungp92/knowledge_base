"""Backfill landscape extraction on existing library sources.

Runs landscape signal extraction on all sources that were ingested before
the landscape extractor existed. Skips sources that already have a
landscape.json file.

Usage:
    python -m scripts.backfill_landscape [--dry-run] [--limit N]
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logger = logging.getLogger(__name__)


def backfill(dry_run: bool = False, limit: int | None = None):
    """Run landscape extraction on existing library sources."""
    from reading_app.config import Config
    from reading_app.db import init_pool, get_conn, list_sources

    config = Config()
    init_pool(config.postgres_dsn)

    sources = list_sources(status="complete", limit=limit or 500)
    if not sources:
        sources = list_sources(status="ingested", limit=limit or 500)

    logger.info("Found %d sources to consider for backfill", len(sources))

    processed = 0
    skipped = 0
    errors = 0

    for source in sources:
        source_id = source["id"]
        library_path = source.get("library_path")

        if not library_path:
            logger.debug("Skipping %s: no library_path", source_id)
            skipped += 1
            continue

        lib_dir = Path(library_path)
        landscape_file = lib_dir / "landscape.json"
        clean_file = lib_dir / "clean.md"

        # Skip if already processed
        if landscape_file.exists():
            logger.debug("Skipping %s: landscape.json already exists", source_id)
            skipped += 1
            continue

        # Need clean.md to extract from
        if not clean_file.exists():
            logger.debug("Skipping %s: no clean.md", source_id)
            skipped += 1
            continue

        if dry_run:
            logger.info("[DRY RUN] Would process: %s (%s)", source_id, source.get("title", "?")[:60])
            processed += 1
            continue

        try:
            from ingest.landscape_extractor import (
                extract_landscape_signals,
                persist_landscape_signals,
                save_landscape_json,
            )

            clean_text = clean_file.read_text(encoding="utf-8")

            # Get existing theme classifications
            with get_conn() as conn:
                theme_rows = conn.execute(
                    "SELECT theme_id FROM source_themes WHERE source_id = %s",
                    (source_id,),
                ).fetchall()
            source_themes = [r["theme_id"] for r in theme_rows]

            # Get published_at for temporal context
            published_at = source.get("published_at")
            if published_at:
                published_at = str(published_at)

            signals = extract_landscape_signals(
                clean_text=clean_text,
                source_id=source_id,
                source_themes=source_themes,
                published_at=published_at,
            )

            persist_landscape_signals(signals, source_id, get_conn_fn=get_conn)
            save_landscape_json(signals, lib_dir)

            processed += 1
            logger.info(
                "Processed %s: %d cap, %d lim, %d bn, %d bt",
                source_id,
                len(signals.get("capabilities", [])),
                len(signals.get("limitations", [])),
                len(signals.get("bottlenecks", [])),
                len(signals.get("breakthroughs", [])),
            )

        except Exception:
            errors += 1
            logger.error("Failed to process %s", source_id, exc_info=True)

    logger.info(
        "Backfill complete: %d processed, %d skipped, %d errors",
        processed, skipped, errors,
    )


def main():
    parser = argparse.ArgumentParser(description="Backfill landscape extraction on existing sources")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed without doing it")
    parser.add_argument("--limit", type=int, default=None, help="Max number of sources to process")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    backfill(dry_run=args.dry_run, limit=args.limit)


if __name__ == "__main__":
    main()
