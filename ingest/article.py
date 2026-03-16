"""Article ingestion: trafilatura primary, BeautifulSoup4 fallback."""

from __future__ import annotations

import json as _json
import logging
import re
from pathlib import Path
from urllib.parse import urlparse

import httpx
from ulid import ULID

from ingest.source_utils import normalize_date, write_meta_yaml

logger = logging.getLogger(__name__)


def _extract_published_at(html: str) -> str | None:
    """Extract publication date from HTML meta tags.

    Tries (in order): article:published_time, og:published_time,
    datePublished in JSON-LD, <time datetime="..."> inside <article>.
    Returns an ISO-8601 date string or None.
    """
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # 1. OpenGraph meta tags
        for prop in ("article:published_time", "og:published_time"):
            tag = soup.find("meta", property=prop)
            if tag and tag.get("content"):
                return tag["content"].strip()[:25]

        # 2. <meta name="date" ...> or <meta name="pubdate" ...>
        for name in ("date", "pubdate", "publish_date", "DC.date.issued"):
            tag = soup.find("meta", attrs={"name": name})
            if tag and tag.get("content"):
                return tag["content"].strip()[:25]

        # 3. JSON-LD datePublished
        for script_tag in soup.find_all("script", type="application/ld+json"):
            try:
                ld = _json.loads(script_tag.string or "")
                # Could be a list of objects
                items = ld if isinstance(ld, list) else [ld]
                for item in items:
                    if isinstance(item, dict):
                        dp = item.get("datePublished")
                        if dp:
                            return str(dp).strip()[:25]
            except (ValueError, TypeError):
                continue

        # 4. <time> element inside <article>
        article = soup.find("article")
        container = article or soup
        time_tag = container.find("time", datetime=True)
        if time_tag and time_tag.get("datetime"):
            return time_tag["datetime"].strip()[:25]

    except Exception as e:
        logger.debug("Failed to extract published_at from HTML: %s", e)
    return None


def _fetch_html(url: str, timeout: int = 30) -> str:
    """Fetch HTML from a URL with retry, falling back to stealth browser."""
    from ingest.http_retry import with_retry

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    def _do_fetch() -> str:
        resp = httpx.get(url, timeout=timeout, follow_redirects=True, headers=headers)
        resp.raise_for_status()
        return resp.text

    try:
        return with_retry(_do_fetch, max_attempts=3, base_delay=2.0, label=f"fetch_html({url})")
    except httpx.HTTPStatusError as e:
        if e.response.status_code in (403, 503):
            logger.info("Got %d for %s, trying stealth browser", e.response.status_code, url)
            from ingest.stealth_fetch import fetch_html_stealth
            return fetch_html_stealth(url)
        raise
    except Exception:
        # Connection errors exhausted retries — try stealth browser as last resort
        logger.info("All retries exhausted for %s, trying stealth browser", url)
        from ingest.stealth_fetch import fetch_html_stealth
        return fetch_html_stealth(url)


def _extract_trafilatura(html: str, url: str) -> str | None:
    """Extract main text using trafilatura."""
    try:
        import trafilatura
        result = trafilatura.extract(
            html,
            url=url,
            include_comments=False,
            include_tables=True,
            favor_recall=True,
            output_format="txt",
        )
        return result
    except Exception as e:
        logger.warning("trafilatura extraction failed: %s", e)
        return None


def _extract_bs4(html: str) -> str | None:
    """Fallback extraction using BeautifulSoup4."""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # Remove script, style, nav, footer, header elements
        for tag in soup.find_all(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        # Try to find the main content area
        main = soup.find("main") or soup.find("article") or soup.find("body")
        if not main:
            return None

        text = main.get_text(separator="\n", strip=True)
        return text if text else None
    except Exception as e:
        logger.warning("BS4 extraction failed: %s", e)
        return None


def _normalize_text(text: str) -> str:
    """Normalize whitespace and clean up text."""
    # Collapse multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip trailing whitespace per line
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def _extract_title_from_html(html: str) -> str:
    """Extract title from HTML."""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        # Try og:title first
        og = soup.find("meta", property="og:title")
        if og and og.get("content"):
            return og["content"].strip()
        # Try <title> tag
        if soup.title and soup.title.string:
            return soup.title.string.strip()
    except Exception:
        pass
    return "Untitled Article"


def _extract_authors_and_sitename(html: str, url: str) -> tuple[list[str] | None, str | None]:
    """Extract authors and site name using trafilatura's bare_extraction."""
    try:
        import trafilatura
        doc = trafilatura.bare_extraction(html, url=url, only_with_metadata=False)
        if not doc:
            return None, None

        authors = None
        raw_author = doc.get("author")
        if raw_author:
            # Split on semicolons and commas
            parts = re.split(r"[;,]", raw_author)
            names = [n.strip() for n in parts if n.strip()]
            if names:
                authors = names

        sitename = doc.get("sitename")
        return authors, sitename
    except Exception as e:
        logger.debug("bare_extraction for authors failed: %s", e)
        return None, None


def fetch(url: str, library_path: Path) -> dict:
    """Ingest an article from a URL.

    Returns a dict with source metadata and clean text.
    """
    # Delegate PDFs to the PDF fetcher
    if urlparse(url).path.lower().endswith(".pdf"):
        from ingest.pdf import fetch as pdf_fetch
        result = pdf_fetch(url, library_path)
        result["source_type"] = "article"
        return result

    source_id = str(ULID())

    html = _fetch_html(url)
    title = _extract_title_from_html(html)
    published_at = normalize_date(_extract_published_at(html))

    # Extract author/sitename metadata
    authors, sitename = _extract_authors_and_sitename(html, url)

    # Fallback: if no published_at from HTML meta, try trafilatura's date
    if not published_at:
        try:
            import trafilatura
            doc = trafilatura.bare_extraction(html, url=url, only_with_metadata=False)
            if doc and doc.get("date"):
                published_at = normalize_date(doc["date"])
        except Exception:
            pass

    # Try trafilatura first, then BS4
    clean_text = _extract_trafilatura(html, url)
    if not clean_text:
        logger.info("Falling back to BS4 for %s", url)
        clean_text = _extract_bs4(html)

    # Last resort: re-fetch with stealth browser (handles JS-rendered pages)
    if not clean_text:
        logger.info("No text extracted, trying stealth browser for %s", url)
        try:
            from ingest.stealth_fetch import fetch_html_stealth
            stealth_html = fetch_html_stealth(url)
            clean_text = _extract_trafilatura(stealth_html, url)
            if not clean_text:
                clean_text = _extract_bs4(stealth_html)
        except Exception as e:
            logger.warning("Stealth browser fallback failed for %s: %s", url, e)

    # Tier 4: PinchTab Readability extraction (handles JS SPAs)
    if not clean_text:
        try:
            from ingest.pinchtab_fetch import fetch_text_pinchtab, PinchTabUnavailable
            logger.info("Trying PinchTab for %s", url)
            pt_text, pt_title = fetch_text_pinchtab(url)
            if pt_text and len(pt_text) >= 100:
                clean_text = pt_text
                if not title or title == "Untitled Article":
                    title = pt_title
        except PinchTabUnavailable:
            logger.debug("PinchTab not available, skipping")
        except Exception as e:
            logger.warning("PinchTab fallback failed for %s: %s", url, e)

    if not clean_text:
        raise ValueError(f"Could not extract text from {url}")

    clean_text = _normalize_text(clean_text)

    # Save to library
    source_dir = library_path / source_id
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "raw.html").write_text(html, encoding="utf-8")
    (source_dir / "clean.md").write_text(clean_text, encoding="utf-8")

    # Write metadata
    meta = {
        "id": source_id,
        "source_type": "article",
        "url": url,
        "title": title,
        "authors": authors,
        "published_at": published_at,
    }
    write_meta_yaml(source_dir, meta)

    metadata = {}
    if sitename:
        metadata["sitename"] = sitename

    return {
        "id": source_id,
        "source_type": "article",
        "url": url,
        "title": title,
        "authors": authors,
        "published_at": published_at,
        "clean_text": clean_text,
        "library_path": str(source_dir),
        "processing_status": "ingested",
        "metadata": metadata,
    }
