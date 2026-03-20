"""Generate anticipations (trackable predictions) for L1 themes.

Reuses the anticipation generation logic from the /anticipate handler.

Usage:
    python -m scripts.generate_anticipations [--min-sources N] [--delay SECS]
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import structlog

logger = logging.getLogger(__name__)
_slog = structlog.get_logger("generate_anticipations")


def main():
    parser = argparse.ArgumentParser(description="Generate anticipations per theme")
    parser.add_argument("--min-sources", type=int, default=5,
                        help="Min sources in theme to generate anticipations")
    parser.add_argument("--delay", type=float, default=5.0, help="Seconds between themes")
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
    executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    # Get L1 themes with source counts and existing anticipation counts
    with get_conn() as conn:
        themes = conn.execute("""
            SELECT t.id, t.name,
                   count(DISTINCT st.source_id) AS source_count,
                   (SELECT count(*) FROM anticipations a WHERE a.theme_id = t.id) AS antic_count
            FROM themes t
            LEFT JOIN source_themes st ON st.theme_id = t.id
            WHERE t.level = 1
            GROUP BY t.id, t.name
            HAVING count(DISTINCT st.source_id) >= %s
            ORDER BY count(DISTINCT st.source_id) DESC
        """, (args.min_sources,)).fetchall()

    themes = [dict(t) for t in themes]
    logger.info("Found %d eligible themes (>= %d sources)", len(themes), args.min_sources)

    # Import the generation logic from the anticipate handler
    from gateway.anticipate_handler import _handle_generate

    generated_total = 0

    for i, theme in enumerate(themes):
        if theme["antic_count"] >= 10:
            logger.info(
                "[%d/%d] Skipping %s: already has %d anticipations",
                i + 1, len(themes), theme["name"], theme["antic_count"],
            )
            continue

        logger.info(
            "[%d/%d] Generating anticipations for %s (%d sources, %d existing)...",
            i + 1, len(themes), theme["name"], theme["source_count"], theme["antic_count"],
        )

        try:
            result = _handle_generate(
                theme_filter=theme["id"],
                executor=executor,
                on_progress=None,
                log=_slog.bind(theme_id=theme["id"]),
            )
            if result:
                count = result.count("ant_")
                generated_total += count
                logger.info("  Generated %d anticipations for %s", count, theme["name"])
                if count == 0:
                    logger.warning(
                        "Zero anticipations for %s. Result: %s",
                        theme["name"], result[:300] if result else "(empty)",
                    )
        except Exception as e:
            logger.error("  Failed for %s: %s", theme["name"], e)

        if args.delay > 0 and i < len(themes) - 1:
            time.sleep(args.delay)

    logger.info("Anticipation generation complete: ~%d total generated", generated_total)


if __name__ == "__main__":
    main()
