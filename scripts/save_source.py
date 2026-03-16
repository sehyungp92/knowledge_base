"""Save a single URL into the knowledge base via CLI.

Usage:
    python -m scripts.save_source <url>
    python -m scripts.save_source https://arxiv.org/abs/2303.08774
    python -m scripts.save_source https://www.youtube.com/watch?v=abc123

    # YouTube with timestamp ranges (only transcribe specific segments):
    python -m scripts.save_source "https://www.youtube.com/watch?v=abc123 8:55-27:04, 2:34:58-2:46:17"

    # Manual content for paywalled/truncated articles:
    python -m scripts.save_source https://example.com/article -f content.md --title "Article Title"

Initialises the DB pool, fetches the source, runs the full extraction
pipeline, and persists everything to PostgreSQL — without needing the
gateway or a nested Claude Code session.

With --content-file (-f), the URL is stored as metadata but the text is
read from the given file instead of fetching. Useful for paywalled articles
where you can paste the full content manually.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from pathlib import Path

# Ensure UTF-8 on Windows
os.environ.setdefault("PYTHONUTF8", "1")
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description="Save a URL into the knowledge base")
    parser.add_argument("url", help="URL to ingest (used as metadata even with --content-file)")
    parser.add_argument("--content-file", "-f", help="Read clean text from this file instead of fetching the URL")
    parser.add_argument("--title", help="Override title (required with --content-file)")
    parser.add_argument("--source-type", default=None, help="Override source type (article, paper, video, podcast)")
    parser.add_argument("--no-landscape", action="store_true", help="Skip landscape extraction")
    parser.add_argument("--no-merge", action="store_true", help="Use separate extraction calls (slower, easier to debug)")
    args = parser.parse_args()

    url = args.url
    t0 = time.monotonic()

    # ── 1. Init DB pool ──────────────────────────────────────────────
    from reading_app.db import ensure_pool, get_conn, insert_source
    ensure_pool()
    logger.info("DB pool ready")

    # ── 1b. Check for duplicate URL ─────────────────────────────────
    from reading_app.db import find_source_by_url

    existing = find_source_by_url(url)
    if existing:
        logger.error(
            "Duplicate URL: already saved as '%s' (ID: %s, status: %s)",
            existing["title"], existing["id"], existing["processing_status"],
        )
        sys.exit(1)

    # ── 2. Load config ───────────────────────────────────────────────
    from reading_app.config import Config
    config = Config()
    library_path = config.library_path

    # ── 3. Refresh theme classifier cache from DB ────────────────────
    from ingest.theme_classifier import refresh_static_theme_block
    try:
        refresh_static_theme_block(get_conn)
        logger.info("Theme block refreshed from DB")
    except Exception as e:
        logger.warning("Could not refresh theme block: %s", e)

    # ── 4. Detect source type and fetch ──────────────────────────────
    from scripts.bulk_ingest import SourceEntry, detect_source_type_from_url, fetch_source

    if args.content_file:
        # Manual content mode: read from file, skip fetch
        from ulid import ULID
        content_path = Path(args.content_file)
        if not content_path.exists():
            logger.error("Content file not found: %s", content_path)
            sys.exit(1)
        clean_text = content_path.read_text(encoding="utf-8")
        source_id = str(ULID())
        title = args.title or content_path.stem
        source_type = args.source_type or detect_source_type_from_url(url, "article")
        published_at = None
        metadata = {}
        # Create library dir and save clean.md
        source_dir = library_path / source_id
        source_dir.mkdir(parents=True, exist_ok=True)
        (source_dir / "clean.md").write_text(clean_text, encoding="utf-8")
        logger.info("Manual content: %s (%d chars) -> %s", title, len(clean_text), source_id)
        fetch_result = {
            "id": source_id, "clean_text": clean_text, "title": title,
            "source_type": source_type, "published_at": published_at,
            "metadata": metadata, "library_path": str(source_dir),
        }
    else:
        # Parse YouTube timestamp ranges from URL arg (e.g. "URL 8:55-27:04, 2:34:58-2:46:17")
        time_ranges = None
        if "youtube.com" in url or "youtu.be" in url:
            from ingest.youtube import parse_youtube_input
            url, time_ranges = parse_youtube_input(url)

        source_type = args.source_type or detect_source_type_from_url(url, "article")

        if source_type == "video" and time_ranges:
            # Call youtube.fetch directly with time_ranges
            from ingest.youtube import fetch as yt_fetch
            logger.info("Fetching %s (type=%s, ranges=%s)...", url, source_type, time_ranges)
            fetch_result = yt_fetch(url, library_path, time_ranges=time_ranges)
        else:
            entry = SourceEntry(title="", date="", url=url, source_type=source_type, csv_file="cli", row_num=0)
            logger.info("Fetching %s (type=%s)...", url, source_type)
            fetch_result = fetch_source(entry, library_path)

    source_id = fetch_result["id"]
    clean_text = fetch_result.get("clean_text", "")
    title = fetch_result.get("title", "Untitled")
    published_at = fetch_result.get("published_at")
    metadata = fetch_result.get("metadata", {})

    if not clean_text or len(clean_text) < 100:
        logger.error("Fetched text too short (%d chars) — aborting", len(clean_text))
        sys.exit(1)

    logger.info("Fetched: %s (%d chars)", title, len(clean_text))

    # ── 5. Insert source record ──────────────────────────────────────
    insert_source(
        id=source_id,
        source_type=fetch_result.get("source_type", source_type),
        title=title,
        url=url,
        authors=fetch_result.get("authors"),
        published_at=published_at,
        abstract=fetch_result.get("abstract"),
        library_path=fetch_result.get("library_path"),
        processing_status="ingested",
        metadata=metadata,
    )
    logger.info("Source record inserted: %s", source_id)

    # ── 6. Strip CLAUDECODE env var for nested CLI calls ─────────────
    os.environ.pop("CLAUDECODE", None)

    # ── 7. Run extraction pipeline ───────────────────────────────────
    from ingest.save_pipeline import run_save_pipeline

    category_hints = metadata.get("category_theme_hints")
    show_name = metadata.get("channel") or metadata.get("podcast_name")

    logger.info("Running extraction pipeline...")
    result = run_save_pipeline(
        source_id=source_id,
        clean_text=clean_text,
        title=title,
        source_type=fetch_result.get("source_type", source_type),
        url=url,
        authors=fetch_result.get("authors"),
        published_at=str(published_at) if published_at else None,
        library_path=library_path,
        category_hints=category_hints,
        show_name=show_name,
        get_conn_fn=get_conn,
        merge_prompts=not args.no_merge,
    )

    # ── 8. Post-pipeline participant extraction for video/podcast ────
    try:
        actual_type = fetch_result.get("source_type", source_type)
        if actual_type in ("video", "podcast") and not fetch_result.get("authors"):
            summary_text = result.get("summary", "")
            if summary_text:
                from ingest.source_utils import parse_participants_from_summary, write_meta_yaml
                from reading_app.db import update_source_authors
                participants = parse_participants_from_summary(summary_text)
                if participants:
                    update_source_authors(source_id, participants)
                    import yaml
                    source_dir = Path(fetch_result.get("library_path", library_path / source_id))
                    meta_path = source_dir / "meta.yaml"
                    if meta_path.exists():
                        existing = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
                        existing["authors"] = participants
                        write_meta_yaml(source_dir, existing)
                    logger.info("Extracted participants: %s", participants)
    except Exception:
        logger.debug("Participant extraction failed (non-critical)", exc_info=True)

    # ── 9. Mark complete ─────────────────────────────────────────────
    elapsed = time.monotonic() - t0

    # ── 10. Print summary ────────────────────────────────────────────
    claims = result.get("claims", [])
    themes = [t.get("theme_id", "") for t in result.get("themes", [])]
    landscape = result.get("landscape_signals", {})
    errors = result.get("errors", [])
    timings = result.get("timings", {})
    processing_status = result.get("processing_status") or "unknown"
    quality_issues = (result.get("quality_assessment") or {}).get("issues", [])

    caps = len(landscape.get("capabilities", []))
    lims = len(landscape.get("limitations", []))
    bots = len(landscape.get("bottlenecks", []))
    bkts = len(landscape.get("breakthroughs", []))

    print(f"\n{'='*60}")
    print(f"Saved: {title}")
    print(f"{'='*60}")
    print(f"  Source ID:    {source_id}")
    print(f"  Type:         {fetch_result.get('source_type', source_type)}")
    print(f"  Status:       {processing_status}")
    print(f"  Themes:       {', '.join(themes) if themes else '(none)'}")
    print(f"  Claims:       {len(claims)}")
    print(f"  Capabilities: {caps}")
    print(f"  Limitations:  {lims}")
    print(f"  Bottlenecks:  {bots}")
    print(f"  Breakthrus:   {bkts}")
    if result.get("theme_proposal"):
        print(f"  New theme:    {result['theme_proposal']}")
    if errors:
        print(f"  Warnings:     {', '.join(errors)}")
    if quality_issues:
        print(f"  Quality:      {', '.join(quality_issues)}")
    print(f"  Timing:       {elapsed:.0f}s total (themes={timings.get('themes',0):.0f}s, "
          f"phase1={timings.get('phase1',0):.0f}s, phase2={timings.get('phase2',0):.0f}s)")
    print()


if __name__ == "__main__":
    main()
