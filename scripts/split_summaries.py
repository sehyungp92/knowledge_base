"""Split multi-entry markdown summary files into one-per-file format.

Reads multi-entry markdown files where each entry has a title, date, URL,
and content. Splits them into individual files under a target directory
organised by source type (youtube/, articles/, papers/).

Usage:
    # Split the default _references/data/summaries/articles_part_*.md files:
    python -m scripts.split_summaries

    # Split additional files from another directory:
    python -m scripts.split_summaries --input /path/to/notes/ --glob "*.md"

    # Dry run (show what would be created without writing):
    python -m scripts.split_summaries --dry-run

    # Custom output directory:
    python -m scripts.split_summaries --output _references/data/summaries_split

Input format (per entry in a multi-entry file):
    <optional HTML anchors>
    Title Text
    <optional blank>
    Date (various formats)
    <optional blank>
    [URL](URL)    or    URL (bare)
    <optional --->
    Content paragraphs...

Output format (one file per entry):
    url: https://...
    title: Title Text
    date: 2025-01-23
    ---
    Content paragraphs...
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = PROJECT_ROOT / "_references" / "data" / "summaries"
DEFAULT_OUTPUT = PROJECT_ROOT / "_references" / "data" / "summaries_split"

# Matches markdown-style [text](url) links
MD_URL_PATTERN = re.compile(r"\[https?://[^\]]+\]\((https?://[^\)]+)\)")
# Matches bare URLs
BARE_URL_PATTERN = re.compile(r"^(https?://\S+)\s*$")
# HTML anchor tags to strip
HTML_ANCHOR_PATTERN = re.compile(r"<a\s+id=\"[^\"]*\"\s*>\s*</a>")


def extract_url(line: str) -> str | None:
    """Extract a URL from a line (markdown link or bare URL)."""
    m = MD_URL_PATTERN.search(line)
    if m:
        return m.group(1)
    m = BARE_URL_PATTERN.match(line.strip())
    if m:
        return m.group(1)
    return None


def classify_url(url: str) -> tuple[str, str]:
    """Return (subdirectory, filename_stem) for a URL.

    Returns:
        ("youtube", "VIDEO_ID") for YouTube URLs
        ("papers", "ARXIV_ID") for arXiv URLs
        ("articles", "domain-slug") for everything else
    """
    # YouTube
    yt_match = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)", url)
    if yt_match:
        return "youtube", yt_match.group(1)

    # arXiv
    arxiv_match = re.search(r"arxiv\.org/(?:abs|pdf|html)/(\d+\.\d+)", url)
    if arxiv_match:
        return "papers", arxiv_match.group(1)

    # Articles: use domain + path slug
    from urllib.parse import urlparse
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "").replace(".", "-")
    path = parsed.path.strip("/").replace("/", "-")[:60]
    slug = f"{domain}-{path}" if path else domain
    # Clean slug
    slug = re.sub(r"[^a-zA-Z0-9_-]", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return "articles", slug


def clean_title(title: str) -> str:
    """Remove HTML anchors and markdown formatting from title."""
    title = HTML_ANCHOR_PATTERN.sub("", title)
    title = title.replace("\\", "")  # Remove markdown escapes
    title = re.sub(r"__(.+?)__", r"\1", title)  # Remove bold markers
    return title.strip()


def split_file(filepath: Path) -> list[dict]:
    """Parse a multi-entry markdown file into individual entries.

    Returns list of dicts with keys: url, title, date, content, source_file.
    """
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")

    # Find all URL line positions
    url_positions: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        url = extract_url(line)
        if url:
            url_positions.append((i, url))

    if not url_positions:
        logger.warning("No URLs found in %s", filepath)
        return []

    entries = []

    for idx, (url_line_num, url) in enumerate(url_positions):
        # --- Extract title and date from lines BEFORE the URL ---
        title = ""
        date = ""

        # Scan backwards from URL line to find title and date
        # Expect: [blanks/anchors] Title [blank] Date [blank] URL
        scan = url_line_num - 1

        # Skip blanks before URL
        while scan >= 0 and not lines[scan].strip():
            scan -= 1

        # This line should be the date (or title if no date)
        if scan >= 0:
            candidate = lines[scan].strip()
            candidate = HTML_ANCHOR_PATTERN.sub("", candidate).strip()
            # Check if it looks like a date
            if re.match(r"^\d{1,2}\s+\w{3}\s+\d{4}$", candidate) or \
               re.match(r"^\w{3}\s+\d{1,2},?\s+\d{4}$", candidate) or \
               re.match(r"^\d{4}-\d{2}-\d{2}$", candidate) or \
               re.match(r"^\w+\s+\d{4}$", candidate):
                date = candidate
                scan -= 1
                # Skip blanks before date
                while scan >= 0 and not lines[scan].strip():
                    scan -= 1

        # This line should be the title
        if scan >= 0:
            candidate = lines[scan].strip()
            candidate = HTML_ANCHOR_PATTERN.sub("", candidate).strip()
            if candidate and not candidate.startswith("---"):
                title = clean_title(candidate)

        # --- Extract content from lines AFTER the URL ---
        content_start = url_line_num + 1

        # Skip blank lines and --- separator after URL
        while content_start < len(lines):
            stripped = lines[content_start].strip()
            if stripped == "---" or stripped == "" or stripped.startswith("<a "):
                content_start += 1
            else:
                break

        # Content ends before the header block of the next entry
        if idx + 1 < len(url_positions):
            next_url_line = url_positions[idx + 1][0]
            # Walk backwards from next URL to skip its header block
            content_end = next_url_line
            # Skip URL line
            content_end -= 1
            # Skip blanks before URL
            while content_end > content_start and not lines[content_end].strip():
                content_end -= 1
            # Skip date line
            if content_end > content_start:
                candidate = lines[content_end].strip()
                candidate = HTML_ANCHOR_PATTERN.sub("", candidate).strip()
                if re.match(r"^\d{1,2}\s+\w{3}\s+\d{4}$", candidate) or \
                   re.match(r"^\w{3}\s+\d{1,2},?\s+\d{4}$", candidate) or \
                   re.match(r"^\d{4}-\d{2}-\d{2}$", candidate) or \
                   re.match(r"^\w+\s+\d{4}$", candidate):
                    content_end -= 1
                    # Skip blanks before date
                    while content_end > content_start and not lines[content_end].strip():
                        content_end -= 1
            # Skip title line
            if content_end > content_start:
                candidate = lines[content_end].strip()
                candidate = HTML_ANCHOR_PATTERN.sub("", candidate).strip()
                if candidate and not candidate.startswith("-"):
                    content_end -= 1
            # Skip HTML anchors and blanks before title
            while content_end > content_start and (
                not lines[content_end].strip() or
                lines[content_end].strip().startswith("<a ")
            ):
                content_end -= 1
            content_end += 1  # Make it exclusive
        else:
            content_end = len(lines)
            # Trim trailing blanks
            while content_end > content_start and not lines[content_end - 1].strip():
                content_end -= 1

        content = "\n".join(lines[content_start:content_end]).strip()

        entries.append({
            "url": url,
            "title": title,
            "date": date,
            "content": content,
            "source_file": str(filepath),
        })

    return entries


def write_entry(entry: dict, output_dir: Path, dry_run: bool = False) -> Path | None:
    """Write a single entry to its own file. Returns the output path."""
    url = entry["url"]
    content = entry["content"]

    if not content:
        logger.warning("Skipping empty entry: %s", url)
        return None

    subdir, stem = classify_url(url)
    target_dir = output_dir / subdir
    target_path = target_dir / f"{stem}.md"

    # Handle filename collisions
    if target_path.exists():
        i = 2
        while (target_dir / f"{stem}_{i}.md").exists():
            i += 1
        target_path = target_dir / f"{stem}_{i}.md"

    # Build output content
    header_lines = [f"url: {url}"]
    if entry.get("title"):
        header_lines.append(f"title: {entry['title']}")
    if entry.get("date"):
        header_lines.append(f"date: {entry['date']}")
    header = "\n".join(header_lines)
    output = f"{header}\n---\n{content}\n"

    if dry_run:
        logger.info("[DRY RUN] Would write: %s (%d chars)", target_path, len(content))
        return target_path

    target_dir.mkdir(parents=True, exist_ok=True)
    target_path.write_text(output, encoding="utf-8")
    logger.info("Wrote: %s (%d chars)", target_path, len(content))
    return target_path


def build_manifest(output_dir: Path) -> dict[str, str]:
    """Scan output directory and build URL→file manifest.

    Returns dict mapping URL to relative file path.
    """
    manifest: dict[str, str] = {}
    for md_file in sorted(output_dir.rglob("*.md")):
        first_line = ""
        with open(md_file, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
        if first_line.startswith("url: "):
            url = first_line[5:].strip()
            rel_path = str(md_file.relative_to(output_dir))
            manifest[url] = rel_path
    return manifest


def main():
    parser = argparse.ArgumentParser(
        description="Split multi-entry summary files into one-per-file format"
    )
    parser.add_argument(
        "--input", "-i", type=Path, default=DEFAULT_INPUT,
        help=f"Input directory to scan (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--glob", "-g", default="articles_part_*.md",
        help="Glob pattern for input files (default: articles_part_*.md)",
    )
    parser.add_argument(
        "--output", "-o", type=Path, default=DEFAULT_OUTPUT,
        help=f"Output directory for split files (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be created without writing",
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
    )

    input_files = sorted(args.input.glob(args.glob))
    if not input_files:
        logger.error("No files matched %s/%s", args.input, args.glob)
        return

    logger.info("Found %d input files", len(input_files))

    all_entries = []
    for filepath in input_files:
        entries = split_file(filepath)
        logger.info("  %s: %d entries", filepath.name, len(entries))
        all_entries.extend(entries)

    logger.info("Total entries parsed: %d", len(all_entries))

    # Check for duplicate URLs
    url_counts: dict[str, int] = {}
    for e in all_entries:
        url_counts[e["url"]] = url_counts.get(e["url"], 0) + 1
    dupes = {u: c for u, c in url_counts.items() if c > 1}
    if dupes:
        logger.warning("Duplicate URLs found: %s", dupes)

    # Write individual files
    written = 0
    for entry in all_entries:
        path = write_entry(entry, args.output, dry_run=args.dry_run)
        if path:
            written += 1

    logger.info("Wrote %d files to %s", written, args.output)

    # Build and write manifest
    if not args.dry_run:
        manifest = build_manifest(args.output)
        manifest_path = args.output / "manifest.json"
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        logger.info("Manifest: %d entries -> %s", len(manifest), manifest_path)
    else:
        logger.info("[DRY RUN] Would build manifest with %d entries", written)


if __name__ == "__main__":
    main()
