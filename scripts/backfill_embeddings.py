"""Backfill embeddings for all claims with NULL embeddings.

Usage:
    python -m scripts.backfill_embeddings [--batch-size 50] [--dry-run]
"""

from __future__ import annotations

import argparse
import logging
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logger = logging.getLogger(__name__)


def backfill_embeddings(batch_size: int = 50, dry_run: bool = False) -> int:
    """Backfill NULL embeddings for all claims.

    Returns number of claims updated.
    """
    from reading_app.config import Config
    from reading_app.db import init_pool, get_conn
    from reading_app.embeddings import embed_batch

    config = Config()
    init_pool(config.postgres_dsn)

    with get_conn() as conn:
        total = conn.execute(
            "SELECT count(*) AS cnt FROM claims WHERE embedding IS NULL"
        ).fetchone()["cnt"]

    logger.info("Found %d claims with NULL embeddings", total)
    if total == 0:
        return 0

    if dry_run:
        logger.info("[DRY RUN] Would backfill %d claims", total)
        return 0

    updated = 0
    failed = 0

    while True:
        with get_conn() as conn:
            rows = conn.execute(
                "SELECT id, claim_text FROM claims WHERE embedding IS NULL ORDER BY id LIMIT %s",
                (batch_size,),
            ).fetchall()

        if not rows:
            break

        ids = [row["id"] for row in rows]
        texts = [row["claim_text"] for row in rows]

        embeddings = embed_batch(texts)

        with get_conn() as conn:
            for claim_id, embedding in zip(ids, embeddings):
                if embedding is None:
                    logger.warning("Embedding failed for claim %s", claim_id)
                    failed += 1
                    continue
                conn.execute(
                    "UPDATE claims SET embedding = %s WHERE id = %s",
                    (str(embedding), claim_id),
                )
                updated += 1
            conn.commit()

        logger.info("Progress: %d/%d updated (%d failed)", updated, total, failed)

    logger.info("Backfill complete: %d updated, %d failed out of %d total", updated, failed, total)
    return updated


def main():
    parser = argparse.ArgumentParser(description="Backfill claim embeddings")
    parser.add_argument("--batch-size", type=int, default=50, help="Batch size (default 50)")
    parser.add_argument("--dry-run", action="store_true", help="Show counts without updating")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    t0 = time.monotonic()
    count = backfill_embeddings(batch_size=args.batch_size, dry_run=args.dry_run)
    elapsed = time.monotonic() - t0
    logger.info("Done in %.1fs — %d claims updated", elapsed, count)


if __name__ == "__main__":
    main()
