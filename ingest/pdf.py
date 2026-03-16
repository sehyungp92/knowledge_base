"""PDF ingestion using PyMuPDF."""

from __future__ import annotations

import logging
import re
from pathlib import Path

import httpx
from ulid import ULID

from ingest.source_utils import normalize_date, write_meta_yaml

logger = logging.getLogger(__name__)


def _extract_pdf_metadata(pdf_path: Path) -> dict:
    """Extract date and author from PDF metadata.

    Returns dict with keys: published_at (YYYY-MM-DD or None), authors (list or None).
    """
    result = {"published_at": None, "authors": None}
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        meta = doc.metadata or {}
        doc.close()

        # Date: try creationDate, then modDate
        for key in ("creationDate", "modDate"):
            raw = meta.get(key, "")
            if raw:
                normalized = normalize_date(raw)
                if normalized:
                    result["published_at"] = normalized
                    break

        # Author
        raw_author = meta.get("author", "")
        if raw_author and raw_author.strip():
            parts = re.split(r"[;,]", raw_author)
            names = [n.strip() for n in parts if n.strip()]
            if names:
                result["authors"] = names
    except Exception as e:
        logger.debug("Failed to extract PDF metadata: %s", e)
    return result


def _extract_text_pymupdf(pdf_path: Path) -> str:
    """Extract text from PDF using PyMuPDF (fitz)."""
    import fitz
    doc = fitz.open(str(pdf_path))
    text_parts = []
    for page in doc:
        text_parts.append(page.get_text())
    doc.close()
    return "\n\n".join(text_parts)


def _detect_sections(text: str) -> str:
    """Add markdown section headings for detected PDF sections."""
    lines = text.split("\n")
    result = []
    for line in lines:
        stripped = line.strip()
        # Detect likely section headers: all-caps short lines, numbered sections
        if stripped and len(stripped) < 80:
            if re.match(r"^\d+\.?\s+[A-Z]", stripped):
                result.append(f"\n## {stripped}\n")
                continue
            if stripped.isupper() and len(stripped.split()) <= 8:
                result.append(f"\n## {stripped.title()}\n")
                continue
        result.append(line)
    return "\n".join(result)


def _extract_title(text: str) -> str:
    """Extract title from first non-empty lines of PDF text."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if lines:
        # First substantial line is often the title
        title = lines[0]
        if len(title) < 200:
            return title
    return "Untitled PDF"


def fetch(url_or_path: str, library_path: Path) -> dict:
    """Ingest a PDF file from URL or local path.

    Returns a dict with source metadata and clean text.
    """
    source_id = str(ULID())
    source_dir = library_path / source_id
    source_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = source_dir / "raw.pdf"

    # Download or copy
    if url_or_path.startswith(("http://", "https://")):
        from ingest.http_retry import with_retry

        _headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }

        def _download_pdf():
            try:
                with httpx.stream("GET", url_or_path, timeout=60,
                                  follow_redirects=True, headers=_headers) as resp:
                    resp.raise_for_status()
                    with open(pdf_path, "wb") as f:
                        for chunk in resp.iter_bytes(chunk_size=8192):
                            f.write(chunk)
            except httpx.ConnectError as e:
                if "SSL" in str(e) or "CERTIFICATE" in str(e).upper():
                    logger.warning("SSL error for %s, retrying without verification", url_or_path)
                    with httpx.stream("GET", url_or_path, timeout=60,
                                      follow_redirects=True, verify=False,
                                      headers=_headers) as resp:
                        resp.raise_for_status()
                        with open(pdf_path, "wb") as f:
                            for chunk in resp.iter_bytes(chunk_size=8192):
                                f.write(chunk)
                else:
                    raise

        with_retry(_download_pdf, max_attempts=3, base_delay=5.0,
                   label=f"pdf_download({url_or_path[:80]})")
        url = url_or_path
    else:
        # Local file
        import shutil
        shutil.copy2(url_or_path, pdf_path)
        url = None

    # Extract metadata (date + author) from PDF
    pdf_meta = _extract_pdf_metadata(pdf_path)
    published_at = pdf_meta["published_at"]
    authors = pdf_meta["authors"]

    # Extract text
    raw_text = _extract_text_pymupdf(pdf_path)
    clean_text = _detect_sections(raw_text)
    title = _extract_title(raw_text)

    # Save clean text
    (source_dir / "clean.md").write_text(clean_text, encoding="utf-8")

    # Write metadata
    meta = {
        "id": source_id,
        "source_type": "pdf",
        "url": url,
        "title": title,
        "authors": authors,
        "published_at": published_at,
    }
    write_meta_yaml(source_dir, meta)

    return {
        "id": source_id,
        "source_type": "pdf",
        "url": url,
        "title": title,
        "authors": authors,
        "published_at": published_at,
        "clean_text": clean_text,
        "library_path": str(source_dir),
        "processing_status": "ingested",
        "metadata": {},
    }
