"""Full database + filesystem reset for the knowledge base.

Truncates all data tables (preserves schema and _migrations), resets
sequences, clears library/ contents, and re-seeds the theme taxonomy.

Usage:
    python -m scripts.reset_db --yes          # no confirmation prompt
    python -m scripts.reset_db                 # interactive confirmation
"""

from __future__ import annotations

import argparse
import logging
import shutil
from pathlib import Path

import psycopg

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROGRESS_FILE = PROJECT_ROOT / "scripts" / "bulk_progress.json"

# Tables to truncate (CASCADE handles FK-dependent tables like claims,
# source_themes, capabilities, limitations, bottlenecks, breakthroughs,
# cross_theme_implications, anticipations, theme_edges, theme_proposals,
# source_edges, source_concepts, etc.)
TRUNCATE_TABLES = [
    "themes",
    "sources",
    "ideas",
    "landscape_history",
    "challenge_log",
    "notifications",
    "graph_metrics",
    "beliefs",
    "concepts",
    "theme_proposals",
    "theme_edge_proposals",
]

# Sequences to reset (from SERIAL columns)
RESET_SEQUENCES = [
    "landscape_history_id_seq",
    "notifications_id_seq",
    "graph_metrics_id_seq",
]


def _count_rows(conn, table: str) -> int:
    """Count rows in a table, returning 0 if it doesn't exist."""
    try:
        row = conn.execute(f"SELECT count(*) AS n FROM {table}").fetchone()
        return row["n"] if row else 0
    except Exception:
        return 0


def reset_db(dsn: str, library_path: Path) -> dict:
    """Perform full reset: truncate tables, reset sequences, clear files, re-seed.

    Returns dict with before/after counts.
    """
    before = {}
    after = {}

    with psycopg.connect(dsn, row_factory=psycopg.rows.dict_row) as conn:
        # Collect before-counts
        for table in TRUNCATE_TABLES:
            before[table] = _count_rows(conn, table)
        before["claims"] = _count_rows(conn, "claims")
        before["source_themes"] = _count_rows(conn, "source_themes")

        logger.info("Before reset: %s", before)

        # Truncate all data tables with CASCADE
        tables_csv = ", ".join(TRUNCATE_TABLES)
        conn.execute(f"TRUNCATE {tables_csv} CASCADE")
        logger.info("Truncated tables: %s", tables_csv)

        # Reset sequences
        for seq in RESET_SEQUENCES:
            try:
                conn.execute(f"ALTER SEQUENCE {seq} RESTART")
            except Exception:
                logger.debug("Sequence %s not found, skipping", seq)

        conn.commit()

    # Clear library/ contents
    if library_path.exists():
        cleared = 0
        for child in library_path.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
                cleared += 1
            elif child.is_file():
                child.unlink()
                cleared += 1
        logger.info("Cleared %d items from %s", cleared, library_path)
    else:
        library_path.mkdir(parents=True, exist_ok=True)
        logger.info("Created library directory: %s", library_path)

    # Delete progress file
    if PROGRESS_FILE.exists():
        PROGRESS_FILE.unlink()
        logger.info("Deleted %s", PROGRESS_FILE)

    # Re-seed themes
    from db.seed_themes import seed_themes
    seed_themes(dsn)
    logger.info("Re-seeded themes")

    # Collect after-counts
    with psycopg.connect(dsn, row_factory=psycopg.rows.dict_row) as conn:
        for table in TRUNCATE_TABLES:
            after[table] = _count_rows(conn, table)
        after["claims"] = _count_rows(conn, "claims")
        after["source_themes"] = _count_rows(conn, "source_themes")

    logger.info("After reset: %s", after)
    return {"before": before, "after": after}


def main():
    parser = argparse.ArgumentParser(description="Full database + filesystem reset")
    parser.add_argument(
        "--yes", action="store_true",
        help="Skip confirmation prompt",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    from reading_app.config import Config
    config = Config()

    if not args.yes:
        answer = input(
            "This will DELETE all data from the knowledge base "
            "(tables, library files, progress). Continue? [y/N] "
        )
        if answer.strip().lower() not in ("y", "yes"):
            print("Aborted.")
            return

    counts = reset_db(config.postgres_dsn, config.library_path)
    print(f"\nReset complete.")
    print(f"  Before: {counts['before']}")
    print(f"  After:  {counts['after']}")


if __name__ == "__main__":
    main()
