"""Re-run landscape extraction for sources that have claims but missing landscape.

These sources were ingested successfully for claims but landscape extraction
failed or was skipped. This script runs only the landscape extraction step.

Usage:
    python -m scripts.reprocess_landscape_only --dry-run
    python -m scripts.reprocess_landscape_only
"""

from __future__ import annotations

import argparse
import logging
import sys
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LIBRARY_PATH = PROJECT_ROOT / "library"

# Sources with claims but missing landscape outputs
TARGET_IDS = [
    "01KJT16GQ76PXYZ4T9H93ND4RD",
    "01KJVK1H1AAMMZ39G04CH7AJRV",
    "01KJVMK38DSVMQMZP6B1W5XF0W",
    "01KJVMPA780CXJ7HK9S3E6C4M9",
    "01KJVQ5NWGHF76T3NCYBH5MPQG",
    "01KJVRMEQFED9A5NCRZHQCDB2J",
]


def main():
    parser = argparse.ArgumentParser(description="Re-run landscape extraction for specific sources")
    parser.add_argument("--dry-run", action="store_true", help="List sources without processing")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    from reading_app.config import Config
    from reading_app.db import init_pool, get_conn
    from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
    from ingest.landscape_extractor import (
        extract_landscape_signals,
        persist_landscape_signals,
        save_landscape_json,
    )
    from ingest.theme_classifier import refresh_static_theme_block

    config = Config()
    init_pool(config.postgres_dsn)

    try:
        refresh_static_theme_block(get_conn)
        logger.info("Theme block refreshed from DB")
    except Exception as e:
        logger.warning("Could not refresh theme block: %s", e)

    # Validate sources exist and have clean.md
    sources = []
    for sid in TARGET_IDS:
        lib_dir = LIBRARY_PATH / sid
        clean_path = lib_dir / "clean.md"
        meta_path = lib_dir / "meta.yaml"

        if not clean_path.exists():
            logger.warning("Skipping %s: no clean.md", sid)
            continue

        clean_text = clean_path.read_text(encoding="utf-8")
        if len(clean_text) < 200:
            logger.warning("Skipping %s: clean.md too short (%d chars)", sid, len(clean_text))
            continue

        meta = {}
        if meta_path.exists():
            with open(meta_path, encoding="utf-8") as f:
                meta = yaml.safe_load(f) or {}

        # Get theme assignments from DB
        with get_conn() as conn:
            theme_rows = conn.execute(
                "SELECT theme_id FROM source_themes WHERE source_id = %s", (sid,)
            ).fetchall()
        theme_ids = [r["theme_id"] for r in theme_rows] if theme_rows else None

        sources.append({
            "id": sid,
            "title": meta.get("title", "(unknown)"),
            "source_type": meta.get("source_type", "article"),
            "published_at": meta.get("published_at"),
            "clean_text": clean_text,
            "theme_ids": theme_ids,
            "chars": len(clean_text),
        })

    if not sources:
        print("No valid sources found.")
        return

    if args.dry_run:
        print(f"\n{'=' * 70}")
        print(f"  DRY RUN: {len(sources)} sources to process")
        print(f"{'=' * 70}\n")
        for i, s in enumerate(sources, 1):
            print(f"  [{i:3d}] {s['id']}  {s['title'][:55]:55s}  {s['chars']:>6d} chars  type={s['source_type']}")
        print(f"\nRun without --dry-run to process these sources.")
        return

    executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    success = 0
    failed = 0

    for i, s in enumerate(sources, 1):
        sid = s["id"]
        print(f"\n[{i}/{len(sources)}] Processing {sid}: {s['title'][:60]}")

        try:
            signals = extract_landscape_signals(
                clean_text=s["clean_text"],
                source_id=sid,
                source_themes=s["theme_ids"],
                published_at=str(s["published_at"]) if s.get("published_at") else None,
                executor=executor,
                source_type=s["source_type"],
            )

            if signals:
                delta = persist_landscape_signals(signals, sid, get_conn_fn=get_conn)
                save_landscape_json(signals, LIBRARY_PATH / sid)
                counts = delta.counts if delta else {}
                total = sum(
                    counts.get(k, 0)
                    for k in ("capabilities", "limitations", "bottlenecks", "breakthroughs")
                )
                print(f"  -> Landscape: {total} signals ({counts})")
                success += 1
            else:
                print(f"  -> No signals extracted")
                failed += 1

        except Exception as e:
            logger.error("Failed %s: %s", sid, e, exc_info=True)
            print(f"  -> ERROR: {e}")
            failed += 1

    print(f"\n{'=' * 70}")
    print(f"  Done: {success} succeeded, {failed} failed out of {len(sources)}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
