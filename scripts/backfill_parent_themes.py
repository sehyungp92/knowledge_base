"""One-time backfill: propagate level-2 source_themes entries to their level-1 parents.

For all existing source_themes rows where the classified theme is level=2,
finds the level-1 parent via theme_edges (relationship='contains') and
upserts it with relevance = subtheme_relevance * 0.85, using GREATEST so
any explicit level-1 classification wins.

Safe to re-run — fully idempotent.

Usage:
    python -m scripts.backfill_parent_themes
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logger = logging.getLogger(__name__)


def backfill(dsn: str) -> tuple[int, int]:
    """Run the backfill. Returns (rows_checked, rows_upserted)."""
    import psycopg
    from psycopg.rows import dict_row

    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        # Get all source_themes for level-2 themes, joined to their level-1 parent
        rows = conn.execute(
            """SELECT st.source_id,
                      st.theme_id AS child_id,
                      st.relevance AS child_relevance,
                      te.parent_id,
                      t_parent.level AS parent_level
               FROM source_themes st
               JOIN themes t_child ON t_child.id = st.theme_id AND t_child.level = 2
               JOIN theme_edges te
                 ON te.child_id = st.theme_id AND te.relationship = 'contains'
               JOIN themes t_parent ON t_parent.id = te.parent_id AND t_parent.level = 1"""
        ).fetchall()

        logger.info("Found %d source_theme rows with level-2 themes", len(rows))

        upserted = 0
        for row in rows:
            propagated_relevance = round(row["child_relevance"] * 0.85, 4)
            result = conn.execute(
                """INSERT INTO source_themes (source_id, theme_id, relevance)
                   VALUES (%s, %s, %s)
                   ON CONFLICT (source_id, theme_id) DO UPDATE SET
                     relevance = GREATEST(source_themes.relevance, EXCLUDED.relevance)
                   RETURNING (xmax = 0) AS inserted""",
                (row["source_id"], row["parent_id"], propagated_relevance),
            ).fetchone()
            if result:
                upserted += 1

        conn.commit()

    return len(rows), upserted


def main():
    logging.basicConfig(level=logging.INFO)
    from reading_app.config import Config
    config = Config()

    logger.info("Starting parent theme backfill...")
    checked, upserted = backfill(config.postgres_dsn)
    logger.info("Done: checked %d rows, upserted %d parent entries", checked, upserted)


if __name__ == "__main__":
    main()
