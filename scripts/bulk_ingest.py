"""Bulk ingestion of reference sources into the knowledge base.

Calls Python ingestion functions directly (not Claude CLI subprocess per source),
which is dramatically faster and cheaper.

Usage:
    python -m scripts.bulk_ingest [--dry-run] [--limit N] [--offset N]
        [--type article|paper|video] [--resume] [--warmup]
        [--skip-landscape] [--skip-summary] [--verbose]
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = PROJECT_ROOT / "_references" / "data" / "sources"
SUMMARIES_DIR = PROJECT_ROOT / "_references" / "data" / "summaries"
SUMMARIES_SPLIT_DIR = PROJECT_ROOT / "_references" / "data" / "summaries_split"
PROGRESS_FILE = PROJECT_ROOT / "scripts" / "bulk_progress.json"

# CSV file -> source_type mapping
CSV_TYPE_MAP = {
    "ai_paper.csv": "paper",
    "other_blog.csv": "article",
    "vc_blog.csv": "article",
    "ai_youtube.csv": "video",
    "vc_youtube.csv": "video",
    "bg2_youtube.csv": "video",
}


@dataclass
class SourceEntry:
    """A source from a reference CSV."""
    title: str
    date: str
    url: str
    source_type: str
    csv_file: str
    row_num: int


@dataclass
class IngestResult:
    """Result of a single source ingestion."""
    url: str
    source_id: str | None = None
    status: str = "pending"  # pending, success, fetch_error, extract_error, skipped
    error: str | None = None
    claims_count: int = 0
    landscape_counts: dict = field(default_factory=dict)
    used_presummary: bool = False


def load_progress() -> dict:
    """Load progress from JSON file, deduplicating errors by URL."""
    if PROGRESS_FILE.exists():
        data = json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
        # Deduplicate errors: keep last occurrence per URL
        errors = data.get("errors", [])
        if errors:
            seen: dict[str, dict] = {}
            for err in errors:
                url = err.get("url", "")
                seen[url] = err
            data["errors"] = list(seen.values())
        return data
    return {"completed": [], "errors": [], "last_index": -1}


def save_progress(progress: dict):
    """Save progress to JSON file."""
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2, default=str), encoding="utf-8")


def parse_csvs(type_filter: str | None = None) -> list[SourceEntry]:
    """Parse all reference CSVs into a unified source list."""
    entries = []
    for csv_file, source_type in CSV_TYPE_MAP.items():
        if type_filter and source_type != type_filter:
            continue
        csv_path = SOURCES_DIR / csv_file
        if not csv_path.exists():
            logger.warning("CSV not found: %s", csv_path)
            continue
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = (row.get("url") or "").strip()
                if not url:
                    continue
                entries.append(SourceEntry(
                    title=(row.get("title") or "").strip(),
                    date=(row.get("date") or "").strip(),
                    url=url,
                    source_type=source_type,
                    csv_file=csv_file,
                    row_num=int(row.get("#", 0)),
                ))
    logger.info("Parsed %d sources from CSVs (filter=%s)", len(entries), type_filter)
    return entries


def parse_presummaries() -> dict[str, str]:
    """Load pre-written summaries from split one-per-file format.

    Reads individual markdown files from SUMMARIES_SPLIT_DIR (organised as
    youtube/, articles/, papers/ subdirectories). Each file has a simple header:

        url: https://...
        title: ...
        date: ...
        ---
        Content paragraphs...

    If a manifest.json exists, uses it for fast URL lookup. Otherwise scans
    all .md files and reads the first line for the URL.

    Falls back to the legacy multi-entry parser if the split directory
    doesn't exist (for backwards compatibility during migration).

    Returns dict mapping URL -> summary markdown text.
    """
    url_to_summary: dict[str, str] = {}

    if not SUMMARIES_SPLIT_DIR.exists():
        logger.warning(
            "Split summaries directory not found: %s. "
            "Run 'python -m scripts.split_summaries' to convert multi-entry files. "
            "Falling back to legacy parser.",
            SUMMARIES_SPLIT_DIR,
        )
        return _parse_presummaries_legacy()

    # Fast path: use manifest if available
    manifest_path = SUMMARIES_SPLIT_DIR / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for url, rel_path in manifest.items():
            filepath = SUMMARIES_SPLIT_DIR / rel_path
            if filepath.exists():
                content = _read_split_summary_content(filepath)
                if content:
                    url_to_summary[url] = content
        logger.info("Loaded %d pre-written summaries from manifest", len(url_to_summary))
        return url_to_summary

    # Slow path: scan all .md files
    for md_file in sorted(SUMMARIES_SPLIT_DIR.rglob("*.md")):
        try:
            text = md_file.read_text(encoding="utf-8")
            first_line = text.split("\n", 1)[0].strip()
            if first_line.startswith("url: "):
                url = first_line[5:].strip()
                content = _read_split_summary_content(md_file)
                if content:
                    url_to_summary[url] = content
        except Exception:
            logger.debug("Failed to read %s", md_file, exc_info=True)

    logger.info("Loaded %d pre-written summaries (no manifest)", len(url_to_summary))
    return url_to_summary


def _read_split_summary_content(filepath: Path) -> str:
    """Read the content portion of a split summary file (after --- separator)."""
    text = filepath.read_text(encoding="utf-8")
    sep_idx = text.find("\n---\n")
    if sep_idx == -1:
        return ""
    return text[sep_idx + 5:].strip()


def _parse_presummaries_legacy() -> dict[str, str]:
    """Legacy parser for multi-entry summary files (articles_part_*.md).

    Kept for backwards compatibility. Prefer split format via split_summaries.py.
    """
    url_to_summary: dict[str, str] = {}
    url_pattern = re.compile(r"\[https?://[^\]]+\]\((https?://[^\)]+)\)")

    for md_file in sorted(SUMMARIES_DIR.glob("articles_part_*.md")):
        text = md_file.read_text(encoding="utf-8")
        lines = text.split("\n")

        url_positions = []
        for i, line in enumerate(lines):
            m = url_pattern.search(line)
            if m:
                url_positions.append((i, m.group(1)))

        for idx, (line_num, url) in enumerate(url_positions):
            content_start = None
            for j in range(line_num + 1, min(line_num + 5, len(lines))):
                if lines[j].strip() == "---":
                    content_start = j + 1
                    break
                elif lines[j].strip() and not lines[j].strip().startswith("<a "):
                    content_start = j
                    break
            if content_start is None:
                content_start = line_num + 1

            if idx + 1 < len(url_positions):
                next_url_line = url_positions[idx + 1][0]
                scan = next_url_line - 1
                while scan > content_start and not lines[scan].strip():
                    scan -= 1
                if scan > content_start:
                    scan -= 1
                while scan > content_start and not lines[scan].strip():
                    scan -= 1
                if scan > content_start:
                    scan -= 1
                while scan > content_start and (not lines[scan].strip() or lines[scan].strip().startswith("<a ")):
                    scan -= 1
                content_end = scan + 1
            else:
                content_end = len(lines)
                while content_end > content_start and not lines[content_end - 1].strip():
                    content_end -= 1

            content = "\n".join(lines[content_start:content_end]).strip()
            if content:
                url_to_summary[url] = content

    logger.info("Parsed %d pre-written summaries (legacy parser)", len(url_to_summary))
    return url_to_summary


def normalize_url(url: str) -> str:
    """Normalize a URL for matching (strip www., trailing slash, escapes)."""
    url = url.strip().rstrip("/")
    url = url.replace("www.", "")
    url = url.replace("\\.", ".")  # Unescape markdown dots
    url = url.replace("\\_", "_")
    url = url.replace("\\-", "-")
    return url


def detect_source_type_from_url(url: str, csv_type: str) -> str:
    """Refine source type based on URL patterns."""
    if "arxiv.org" in url:
        return "paper"
    if "youtube.com" in url or "youtu.be" in url:
        return "video"
    return csv_type


def _is_direct_pdf_url(url: str) -> bool:
    """Check if URL points directly to a PDF file."""
    path = urlparse(url).path.lower()
    return path.endswith(".pdf")


def _github_blob_to_raw(url: str) -> str:
    """Convert GitHub blob URLs to raw.githubusercontent.com URLs."""
    m = re.match(
        r"https?://github\.com/([^/]+/[^/]+)/blob/(.+)",
        url,
    )
    if m:
        return f"https://raw.githubusercontent.com/{m.group(1)}/{m.group(2)}"
    return url


def _validate_url(url: str) -> str | None:
    """Return an error message if URL is invalid, else None."""
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        return f"Invalid URL scheme: {parsed.scheme!r} (expected http or https)"
    if not parsed.netloc:
        return "Invalid URL: no hostname"
    return None


def fetch_source(entry: SourceEntry, library_path: Path) -> dict:
    """Fetch a single source using the appropriate ingestion module.

    Returns the result dict from the fetch function.
    """
    url = _github_blob_to_raw(entry.url)
    source_type = detect_source_type_from_url(url, entry.source_type)

    if source_type == "paper":
        if "arxiv.org" in url:
            from ingest.arxiv import fetch
            return fetch(url, library_path)
        elif _is_direct_pdf_url(url) or "/pdf/" in url:
            from ingest.pdf import fetch
            result = fetch(url, library_path)
            result["source_type"] = "paper"
            return result
        else:
            # HTML paper page (e.g. nature.com)
            from ingest.article import fetch
            result = fetch(url, library_path)
            result["source_type"] = "paper"
            return result
    elif source_type == "video":
        from ingest.youtube import fetch
        return fetch(url, library_path)
    elif source_type == "podcast":
        from ingest.podcast import fetch
        return fetch(url, library_path)
    else:
        from ingest.article import fetch
        return fetch(url, library_path)


def ingest_one(
    entry: SourceEntry,
    library_path: Path,
    executor,
    get_conn_fn,
    presummaries: dict[str, str],
    skip_landscape: bool = False,
    skip_summary: bool = False,
) -> IngestResult:
    """Run the full ingestion pipeline for a single source.

    Delegates extraction to ``run_save_pipeline()`` which runs claims+summary
    and landscape+implications in parallel (Phase 1), then anticipation
    matching and belief checking (Phase 2).

    Steps handled here: fetch → presummary handling → pipeline delegation.
    """
    result = IngestResult(url=entry.url)

    # 0. Validate URL
    url_err = _validate_url(entry.url)
    if url_err:
        result.status = "fetch_error"
        result.error = url_err
        logger.error("Invalid URL for %s: %s", entry.title[:60], url_err)
        return result

    # 1. Fetch
    try:
        fetch_result = fetch_source(entry, library_path)
    except Exception as e:
        result.status = "fetch_error"
        result.error = str(e)[:200]
        logger.error("Fetch failed for %s: %s", entry.url, e)
        return result

    source_id = fetch_result["id"]
    result.source_id = source_id
    source_type = fetch_result.get("source_type", entry.source_type)
    clean_text = fetch_result.get("clean_text", "")
    metadata = fetch_result.get("metadata", {})
    published_at = fetch_result.get("published_at")

    if not clean_text or len(clean_text) < 100:
        result.status = "fetch_error"
        result.error = f"Clean text too short ({len(clean_text)} chars)"
        logger.warning("Skipping %s: clean text too short", entry.url)
        return result

    # 2. Handle pre-written summary: write to disk so pipeline skips generation
    presummary = presummaries.get(normalize_url(entry.url))
    pipeline_skip_summary = skip_summary
    if presummary:
        try:
            source_dir = Path(fetch_result.get("library_path", library_path / source_id))
            summary_path = source_dir / "deep_summary.md"
            summary_path.write_text(presummary, encoding="utf-8")
            result.used_presummary = True
            pipeline_skip_summary = True  # No need to generate — already on disk
            logger.info("Wrote pre-written summary for %s", source_id)
        except Exception:
            logger.warning("Failed to write presummary for %s, pipeline will generate", source_id, exc_info=True)

    # 3. Delegate to parallel save pipeline
    try:
        from ingest.save_pipeline import run_save_pipeline

        show_name = metadata.get("channel") or metadata.get("podcast_name")
        category_hints = metadata.get("category_theme_hints")

        pipeline_result = run_save_pipeline(
            source_id=source_id,
            clean_text=clean_text,
            title=fetch_result.get("title", entry.title),
            source_type=source_type,
            url=entry.url,
            authors=fetch_result.get("authors"),
            published_at=str(published_at) if published_at else None,
            library_path=library_path,
            category_hints=category_hints,
            show_name=show_name,
            executor=executor,
            get_conn_fn=get_conn_fn,
            merge_prompts=True,
            skip_landscape=skip_landscape,
            skip_summary=pipeline_skip_summary,
            abstract=fetch_result.get("abstract"),
            metadata=metadata,
        )

        result.claims_count = len(pipeline_result.get("claims", []))
        landscape_delta = pipeline_result.get("landscape_delta")
        if landscape_delta:
            result.landscape_counts = landscape_delta.counts
    except Exception as e:
        result.status = "extract_error"
        result.error = f"Pipeline failed: {str(e)[:200]}"
        logger.error("Pipeline failed for %s: %s", source_id, e, exc_info=True)
        return result

    # 4. Enqueue post-processing (source_edges, graph_metrics, state_summaries, anticipations)
    try:
        theme_ids = [t["theme_id"] for t in pipeline_result.get("themes", []) if "theme_id" in t]
        if theme_ids:
            from ingest.post_processor import enqueue_post_processing
            enqueue_post_processing(source_id, theme_ids, get_conn_fn)
    except Exception:
        logger.debug("Post-processing enqueue failed for %s (non-critical)", source_id, exc_info=True)

    # 5. Post-pipeline participant extraction for video/podcast
    try:
        if source_type in ("video", "podcast") and not fetch_result.get("authors"):
            summary_text = pipeline_result.get("summary", "")
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
                    logger.info("Extracted participants for %s: %s", source_id, participants)
    except Exception:
        logger.debug("Participant extraction failed for %s (non-critical)", source_id, exc_info=True)

    result.status = "success"
    return result


def bulk_ingest(
    type_filter: str | None = None,
    limit: int | None = None,
    offset: int = 0,
    resume: bool = False,
    dry_run: bool = False,
    skip_landscape: bool = False,
    skip_summary: bool = False,
    warmup: bool = False,
    workers: int = 3,
    reset: bool = False,
    delay: float = 3.0,
):
    """Run bulk ingestion across reference sources.

    When workers > 1, sources are processed concurrently using a
    ThreadPoolExecutor.  API call concurrency is governed by the global
    semaphore in ``agents.executor`` (default 5 slots), so even with many
    workers the system won't saturate the API.
    """
    from reading_app.config import Config
    from reading_app.db import init_pool, get_conn
    from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE

    config = Config()
    init_pool(config.postgres_dsn)
    library_path = config.library_path

    if reset:
        from scripts.reset_db import reset_db
        logger.info("Running full database + filesystem reset...")
        reset_db(config.postgres_dsn, library_path)
        resume = False  # Force fresh start after reset

    executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    # Sync classifier theme cache with DB so static fallback stays current
    try:
        from ingest.theme_classifier import refresh_static_theme_block
        refresh_static_theme_block(get_conn)
    except Exception:
        logger.debug("Failed to refresh static theme block at startup", exc_info=True)

    # Parse inputs
    entries = parse_csvs(type_filter)
    raw_presummaries = parse_presummaries()

    # Build normalized URL lookup for presummary matching
    presummaries: dict[str, str] = {}
    for url, content in raw_presummaries.items():
        presummaries[normalize_url(url)] = content

    # Apply ordering: articles first, then papers, then videos
    type_order = {"article": 0, "paper": 1, "video": 2}
    entries.sort(key=lambda e: (type_order.get(e.source_type, 99), e.csv_file, e.row_num))

    # Warmup mode: select 9 sources (3 articles, 3 papers, 3 videos)
    if warmup:
        warmup_entries = []
        type_counts = {"article": 0, "paper": 0, "video": 0}
        type_limits = {"article": 3, "paper": 3, "video": 3}
        for e in entries:
            if type_counts.get(e.source_type, 0) < type_limits.get(e.source_type, 0):
                warmup_entries.append(e)
                type_counts[e.source_type] = type_counts.get(e.source_type, 0) + 1
            if len(warmup_entries) >= 9:
                break
        entries = warmup_entries
        logger.info("Warmup mode: selected %d sources", len(entries))

    # Apply offset/limit
    entries = entries[offset:]
    if limit:
        entries = entries[:limit]

    # Resume from progress
    progress = load_progress() if resume else {"completed": [], "errors": [], "last_index": -1}
    completed_urls = set(progress.get("completed", []))

    if resume and completed_urls:
        before = len(entries)
        entries = [e for e in entries if e.url not in completed_urls]
        logger.info("Resuming: skipped %d already-completed sources", before - len(entries))

    logger.info(
        "Starting bulk ingestion: %d sources (%s), workers=%d, dry_run=%s",
        len(entries), type_filter or "all types", workers, dry_run,
    )

    if dry_run:
        for i, entry in enumerate(entries):
            presummary = "YES" if entry.url in presummaries else "no"
            logger.info(
                "[%d/%d] [DRY RUN] %s (%s) — presummary: %s — %s",
                i + 1, len(entries), entry.title[:60], entry.source_type,
                presummary, entry.url,
            )
        return {"success": 0, "fetch_error": 0, "extract_error": 0, "skipped": 0}

    stats = {"success": 0, "fetch_error": 0, "extract_error": 0, "skipped": 0}
    progress_lock = threading.Lock()
    stats_lock = threading.Lock()
    total = len(entries)
    completed_count = 0

    def _process_one(index: int, entry: SourceEntry) -> None:
        nonlocal completed_count

        logger.info(
            "[%d/%d] Processing: %s (%s) — %s",
            index + 1, total, entry.title[:60], entry.source_type, entry.url,
        )

        t_source = time.monotonic()
        try:
            from ingest.http_retry import with_retry
            result = with_retry(
                lambda: ingest_one(
                    entry=entry,
                    library_path=library_path,
                    executor=executor,
                    get_conn_fn=get_conn,
                    presummaries=presummaries,
                    skip_landscape=skip_landscape,
                    skip_summary=skip_summary,
                ),
                max_attempts=2,
                base_delay=10.0,
                label=f"ingest_{entry.url[:60]}",
            )
        except Exception:
            elapsed = time.monotonic() - t_source
            logger.error("Unhandled error for %s (%.1fs)", entry.url, elapsed, exc_info=True)
            with progress_lock:
                progress["errors"] = [
                    e for e in progress["errors"] if e.get("url") != entry.url
                ]
                progress["errors"].append({
                    "url": entry.url,
                    "status": "unhandled_error",
                    "timestamp": datetime.now().isoformat(),
                })
                save_progress(progress)
            return

        elapsed = time.monotonic() - t_source

        with stats_lock:
            stats[result.status] = stats.get(result.status, 0) + 1

        with progress_lock:
            completed_count += 1
            if result.status == "success":
                progress["completed"].append(entry.url)
                logger.info(
                    "  OK [%d/%d]: %s — %d claims, landscape=%s, presummary=%s (%.1fs)",
                    completed_count, total,
                    result.source_id, result.claims_count,
                    result.landscape_counts, result.used_presummary, elapsed,
                )
            else:
                progress["errors"] = [
                    e for e in progress["errors"] if e.get("url") != entry.url
                ]
                progress["errors"].append({
                    "url": entry.url,
                    "status": result.status,
                    "error": result.error,
                    "timestamp": datetime.now().isoformat(),
                })
                logger.warning(
                    "  FAILED [%d/%d]: %s — %s: %s (%.1fs)",
                    completed_count, total,
                    result.source_id or "?", result.status, result.error, elapsed,
                )

            progress["last_index"] = offset + index
            save_progress(progress)

    if workers <= 1:
        # Sequential with inter-source delay
        for i, entry in enumerate(entries):
            _process_one(i, entry)
            if delay > 0 and i < len(entries) - 1:
                time.sleep(delay)
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {}
            for i, entry in enumerate(entries):
                futures[pool.submit(_process_one, i, entry)] = entry
                # Stagger submissions to avoid burst rate-limiting
                if delay > 0 and i < len(entries) - 1:
                    time.sleep(delay / workers)
            for future in as_completed(futures):
                # Exceptions are already handled inside _process_one,
                # but guard against unexpected failures
                exc = future.exception()
                if exc:
                    entry = futures[future]
                    logger.error(
                        "Worker crashed for %s: %s", entry.url, exc, exc_info=True,
                    )

    logger.info(
        "Bulk ingestion complete: %d success, %d fetch errors, %d extract errors, %d skipped",
        stats["success"], stats["fetch_error"], stats["extract_error"], stats["skipped"],
    )
    return stats


def main():
    parser = argparse.ArgumentParser(description="Bulk ingest reference sources")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed")
    parser.add_argument("--limit", type=int, default=None, help="Max sources to process")
    parser.add_argument("--offset", type=int, default=0, help="Skip first N sources")
    parser.add_argument("--type", dest="type_filter", choices=["article", "paper", "video"],
                        help="Only process sources of this type")
    parser.add_argument("--resume", action="store_true", help="Resume from last progress checkpoint")
    parser.add_argument("--warmup", action="store_true", help="Run 9-source warmup batch (3 articles, 3 papers, 3 videos)")
    parser.add_argument("--skip-landscape", action="store_true", help="Skip landscape extraction")
    parser.add_argument("--skip-summary", action="store_true", help="Skip deep summary generation")
    parser.add_argument("--workers", type=int, default=3,
                        help="Number of concurrent source workers (default 3)")
    parser.add_argument("--reset", action="store_true",
                        help="Full DB + filesystem reset before ingestion")
    parser.add_argument("--delay", type=float, default=3.0,
                        help="Seconds between source submissions (default 3.0)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Debug logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )

    bulk_ingest(
        type_filter=args.type_filter,
        limit=args.limit,
        offset=args.offset,
        resume=args.resume,
        dry_run=args.dry_run,
        skip_landscape=args.skip_landscape,
        skip_summary=args.skip_summary,
        warmup=args.warmup,
        workers=args.workers,
        reset=args.reset,
        delay=args.delay,
    )


if __name__ == "__main__":
    main()
