"""Generate theme state summaries for all L1 themes with sufficient data.

Usage:
    python -m scripts.generate_state_summaries [--force] [--delay SECS]
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Generate theme state summaries")
    parser.add_argument("--force", action="store_true", help="Regenerate even if fresh")
    parser.add_argument("--delay", type=float, default=3.0, help="Seconds between themes")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    from reading_app.config import Config
    from reading_app.db import init_pool, get_conn
    from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
    from retrieval.state_summary import generate_theme_state_summary, should_regenerate

    config = Config()
    init_pool(config.postgres_dsn)
    executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    # Get all L1 themes with source counts
    with get_conn() as conn:
        themes = conn.execute("""
            SELECT t.id, t.name, t.level, t.state_summary, t.state_summary_updated_at,
                   count(DISTINCT st.source_id) AS source_count
            FROM themes t
            LEFT JOIN source_themes st ON st.theme_id = t.id
            WHERE t.level = 1
            GROUP BY t.id, t.name, t.level, t.state_summary, t.state_summary_updated_at
            ORDER BY t.name
        """).fetchall()

    themes = [dict(t) for t in themes]
    logger.info("Found %d L1 themes", len(themes))

    generated = 0
    skipped = 0

    for i, theme in enumerate(themes):
        theme_id = theme["id"]
        source_count = theme["source_count"]

        if not args.force and not should_regenerate(theme, source_count):
            logger.info(
                "[%d/%d] Skipping %s: %d sources, summary %s",
                i + 1, len(themes), theme["name"], source_count,
                "exists" if theme.get("state_summary") else "none",
            )
            skipped += 1
            continue

        logger.info(
            "[%d/%d] Generating state summary for %s (%d sources)...",
            i + 1, len(themes), theme["name"], source_count,
        )

        try:
            summary = generate_theme_state_summary(theme_id, executor=executor)
            if summary:
                generated += 1
                logger.info("  Generated %d chars for %s", len(summary), theme["name"])
            else:
                logger.warning("  No summary generated for %s", theme["name"])
        except Exception as e:
            logger.error("  Failed for %s: %s", theme["name"], e)

        if args.delay > 0 and i < len(themes) - 1:
            time.sleep(args.delay)

    logger.info(
        "State summary generation complete: %d generated, %d skipped",
        generated, skipped,
    )


if __name__ == "__main__":
    main()
