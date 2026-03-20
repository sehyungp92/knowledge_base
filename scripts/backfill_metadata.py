"""One-time backfill to normalize existing library metadata.

Normalizes published_at dates, extracts participants from video/podcast summaries,
re-extracts article authors from raw.html, and rewrites all meta.yaml files
via the shared write_meta_yaml utility.

Usage:
    python -m scripts.backfill_metadata           # dry-run (default)
    python -m scripts.backfill_metadata --apply    # commit changes to DB + disk
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import yaml

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description="Backfill metadata for existing library sources")
    parser.add_argument("--apply", action="store_true", help="Actually write changes (default is dry-run)")
    parser.add_argument("--library", default=None, help="Override library path")
    args = parser.parse_args()

    dry_run = not args.apply

    if dry_run:
        logger.info("DRY RUN — no changes will be written. Use --apply to commit.")
    else:
        logger.info("APPLY MODE — changes will be written to DB and disk.")

    from ingest.source_utils import normalize_date, write_meta_yaml, parse_participants_from_summary

    # Init DB
    from reading_app.db import ensure_pool, get_conn, update_source_authors
    ensure_pool()

    library_path = Path(args.library) if args.library else PROJECT_ROOT / "library"
    if not library_path.exists():
        logger.error("Library path not found: %s", library_path)
        sys.exit(1)

    stats = {
        "total": 0,
        "date_normalized": 0,
        "participants_extracted": 0,
        "article_authors_extracted": 0,
        "meta_rewritten": 0,
        "errors": 0,
    }

    for meta_path in sorted(library_path.glob("*/meta.yaml")):
        source_dir = meta_path.parent
        stats["total"] += 1

        try:
            meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
        except Exception as e:
            logger.warning("Failed to read %s: %s", meta_path, e)
            stats["errors"] += 1
            continue

        source_id = meta.get("id")
        source_type = meta.get("source_type", "")
        changed = False

        # 1. Normalize published_at
        raw_date = meta.get("published_at")
        if raw_date:
            normalized = normalize_date(str(raw_date))
            if normalized and normalized != str(raw_date):
                logger.info("[%s] Date: %r -> %s", source_id, raw_date, normalized)
                meta["published_at"] = normalized
                changed = True

        # 2. Video/podcast: parse participants from deep_summary.md
        if source_type in ("video", "podcast") and not meta.get("authors"):
            summary_path = source_dir / "deep_summary.md"
            if summary_path.exists():
                summary = summary_path.read_text(encoding="utf-8")
                participants = parse_participants_from_summary(summary)
                if participants:
                    logger.info("[%s] Participants: %s", source_id, participants)
                    meta["authors"] = participants
                    changed = True
                    stats["participants_extracted"] += 1

        # 3. Articles: re-extract author from raw.html
        if source_type == "article" and not meta.get("authors"):
            html_path = source_dir / "raw.html"
            if html_path.exists():
                try:
                    import trafilatura
                    html = html_path.read_text(encoding="utf-8")
                    doc = trafilatura.bare_extraction(
                        html, url=meta.get("url", ""), only_with_metadata=False,
                    )
                    if doc and doc.get("author"):
                        import re
                        parts = re.split(r"[;,]", doc["author"])
                        names = [n.strip() for n in parts if n.strip()]
                        if names:
                            logger.info("[%s] Article authors: %s", source_id, names)
                            meta["authors"] = names
                            changed = True
                            stats["article_authors_extracted"] += 1
                except Exception as e:
                    logger.debug("Author re-extraction failed for %s: %s", source_id, e)

        # 4. Apply changes
        if changed:
            if dry_run:
                logger.info("[%s] Would update meta.yaml and DB", source_id)
            else:
                # Update DB
                try:
                    with get_conn() as conn:
                        updates = []
                        params = []
                        if "published_at" in meta and meta["published_at"]:
                            updates.append("published_at = %s")
                            params.append(meta["published_at"])
                        if meta.get("authors"):
                            import json
                            updates.append("authors = %s")
                            params.append(json.dumps(meta["authors"]))
                        if updates:
                            params.append(source_id)
                            conn.execute(
                                f"UPDATE sources SET {', '.join(updates)} WHERE id = %s",
                                params,
                            )
                            conn.commit()
                except Exception as e:
                    logger.warning("DB update failed for %s: %s", source_id, e)
                    stats["errors"] += 1

                # Rewrite meta.yaml
                try:
                    write_meta_yaml(source_dir, meta)
                    stats["meta_rewritten"] += 1
                except Exception as e:
                    logger.warning("meta.yaml rewrite failed for %s: %s", source_id, e)
                    stats["errors"] += 1

            stats["date_normalized"] += 1 if raw_date and normalize_date(str(raw_date)) != str(raw_date) else 0
        else:
            # Even unchanged sources get their meta.yaml rewritten for format consistency
            if not dry_run:
                try:
                    write_meta_yaml(source_dir, meta)
                    stats["meta_rewritten"] += 1
                except Exception as e:
                    logger.warning("meta.yaml rewrite failed for %s: %s", source_id, e)
                    stats["errors"] += 1

    # Print summary
    print(f"\n{'='*50}")
    print(f"Backfill {'(DRY RUN)' if dry_run else 'COMPLETE'}")
    print(f"{'='*50}")
    for key, val in stats.items():
        print(f"  {key}: {val}")
    print()


if __name__ == "__main__":
    main()
