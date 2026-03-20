"""Merge duplicate concepts and remap source_concepts.

Finds concept groups with the same lower(canonical_name) and concept_type,
picks the oldest ID as canonical, remaps all source_concepts to it, and
deletes the duplicate rows.

Usage:
    python -m scripts.dedup_concepts [--dry-run]
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logger = logging.getLogger(__name__)


def dedup_concepts(dry_run: bool = False) -> dict:
    """Merge duplicate concepts. Returns stats dict."""
    from reading_app.config import Config
    from reading_app.db import init_pool, get_conn

    config = Config()
    init_pool(config.postgres_dsn)

    stats = {"groups": 0, "duplicates_removed": 0, "source_concepts_remapped": 0}

    with get_conn() as conn:
        # Find duplicate groups
        groups = conn.execute("""
            SELECT lower(canonical_name) AS lname,
                   COALESCE(concept_type, '') AS ctype,
                   array_agg(id ORDER BY id) AS ids,
                   count(*) AS cnt
            FROM concepts
            GROUP BY lower(canonical_name), COALESCE(concept_type, '')
            HAVING count(*) > 1
            ORDER BY count(*) DESC
        """).fetchall()

    logger.info("Found %d duplicate concept groups", len(groups))

    for group in groups:
        lname = group["lname"]
        ctype = group["ctype"]
        ids = group["ids"]
        canonical_id = ids[0]  # oldest ID as canonical
        duplicate_ids = ids[1:]

        logger.info(
            "Group '%s' (type=%s): keeping %s, merging %d duplicates",
            lname, ctype or "(none)", canonical_id, len(duplicate_ids),
        )

        if dry_run:
            stats["groups"] += 1
            stats["duplicates_removed"] += len(duplicate_ids)
            continue

        with get_conn() as conn:
            # Remap source_concepts from duplicates to canonical
            for dup_id in duplicate_ids:
                # Get source_concepts pointing to the duplicate
                sc_rows = conn.execute(
                    "SELECT source_id, relationship, confidence FROM source_concepts WHERE concept_id = %s",
                    (dup_id,),
                ).fetchall()

                for sc in sc_rows:
                    # Try to insert/update the canonical mapping
                    conn.execute("""
                        INSERT INTO source_concepts (source_id, concept_id, relationship, confidence)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (source_id, concept_id, relationship) DO NOTHING
                    """, (sc["source_id"], canonical_id, sc["relationship"], sc["confidence"]))
                    stats["source_concepts_remapped"] += 1

                # Delete old source_concepts for the duplicate
                conn.execute(
                    "DELETE FROM source_concepts WHERE concept_id = %s",
                    (dup_id,),
                )

                # Delete the duplicate concept
                conn.execute(
                    "DELETE FROM concepts WHERE id = %s",
                    (dup_id,),
                )
                stats["duplicates_removed"] += 1

            conn.commit()
        stats["groups"] += 1

    logger.info(
        "Dedup complete: %d groups, %d duplicates removed, %d source_concepts remapped",
        stats["groups"], stats["duplicates_removed"], stats["source_concepts_remapped"],
    )
    return stats


def main():
    parser = argparse.ArgumentParser(description="Deduplicate concepts")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be merged")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    t0 = time.monotonic()
    stats = dedup_concepts(dry_run=args.dry_run)
    elapsed = time.monotonic() - t0
    prefix = "[DRY RUN] " if args.dry_run else ""
    logger.info("%sDone in %.1fs — %s", prefix, elapsed, stats)


if __name__ == "__main__":
    main()
