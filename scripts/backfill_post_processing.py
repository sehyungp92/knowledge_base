"""Backfill post-processing tracking rows for existing sources.

Finds all 'complete' sources that don't yet have post_processing_status rows
and enqueues them for the post-processing worker to pick up.

Usage:
    python -m scripts.backfill_post_processing [--dry-run] [--limit N]
"""

from __future__ import annotations

import argparse
import logging

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Backfill post-processing status for existing sources",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would be enqueued")
    parser.add_argument("--limit", type=int, default=0, help="Max sources to backfill (0 = all)")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    from reading_app.config import Config
    from reading_app.db import init_pool, get_conn

    config = Config()
    init_pool(config.postgres_dsn)

    # Run migration first to ensure table exists
    from db.migrate import migrate
    migrate(config.postgres_dsn)

    from ingest.post_processor import enqueue_post_processing

    with get_conn() as conn:
        # Find complete sources without post-processing rows
        query = """
            SELECT s.id
            FROM sources s
            WHERE s.processing_status = 'complete'
              AND NOT EXISTS (
                  SELECT 1 FROM post_processing_status pp
                  WHERE pp.source_id = s.id
              )
            ORDER BY s.ingested_at DESC
        """
        if args.limit > 0:
            query += f" LIMIT {args.limit}"

        sources = conn.execute(query).fetchall()

    logger.info("Found %d sources without post-processing status", len(sources))

    if not sources:
        logger.info("Nothing to backfill.")
        return

    enqueued = 0
    for row in sources:
        source_id = row["id"]

        if args.dry_run:
            logger.info("[DRY-RUN] Would enqueue: %s", source_id)
            enqueued += 1
            continue

        # Get themes for this source
        with get_conn() as conn:
            themes = conn.execute(
                "SELECT theme_id FROM source_themes WHERE source_id = %s",
                (source_id,),
            ).fetchall()
        theme_ids = [t["theme_id"] for t in themes]

        if enqueue_post_processing(source_id, theme_ids, get_conn):
            enqueued += 1

    mode = "[DRY-RUN] " if args.dry_run else ""
    logger.info("%sBackfill complete: %d/%d sources enqueued", mode, enqueued, len(sources))


if __name__ == "__main__":
    main()
