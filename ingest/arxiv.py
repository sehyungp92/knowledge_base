"""ArXiv ingestion: Atom API metadata + PDF -> markitdown + backmatter strip."""

from __future__ import annotations

import logging
import re
import tempfile
from pathlib import Path
from xml.etree import ElementTree

import httpx
from ulid import ULID

from ingest.section_slicer import strip_backmatter
from ingest.source_utils import normalize_date, write_meta_yaml

logger = logging.getLogger(__name__)

ATOM_NS = "http://www.w3.org/2005/Atom"
ARXIV_NS = "http://arxiv.org/schemas/atom"

# Maps arXiv category codes to theme_id slugs for theme_classifier hints.
CATEGORY_THEME_HINTS: dict[str, str] = {
    "cs.LG": "training_paradigms",
    "cs.CL": "language_and_communication",
    "cs.CV": "multimodality",
    "cs.AI": "reasoning_and_planning",
    "cs.RO": "robotics",
    "cs.NE": "scaling_and_architecture",
    "cs.IR": "memory_and_context",
    "cs.CR": "safety_and_alignment",
    "cs.SE": "code_and_software",
    "cs.HC": "personal_assistants",
    "cs.MA": "autonomous_agents",
    "stat.ML": "training_paradigms",
    "eess.AS": "multimodality",
    "eess.IV": "multimodality",
    "q-bio": "genomics_and_proteins",
    "q-bio.BM": "drug_discovery",
    "cs.LO": "reasoning_and_planning",
    "cs.PF": "compute_and_hardware",
    "cs.DC": "compute_and_hardware",
    "cs.CY": "governance_and_regulation",
    "econ": "economic_impact",
    "physics.med-ph": "medical_ai",
}


def _parse_arxiv_id(url: str) -> str:
    """Extract arXiv ID from URL (supports abs/ and pdf/ with versions)."""
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]+\.[0-9]+(?:v\d+)?)", url)
    if m:
        return m.group(1)
    # Try bare ID
    m = re.search(r"(\d{4}\.\d{4,5}(?:v\d+)?)", url)
    if m:
        return m.group(1)
    raise ValueError(f"Cannot parse arXiv ID from URL: {url}")


def _fetch_metadata(arxiv_id: str) -> dict:
    """Fetch structured metadata from arXiv Atom API."""
    from ingest.http_retry import with_retry

    # Strip version for API query
    base_id = re.sub(r"v\d+$", "", arxiv_id)
    api_url = f"http://export.arxiv.org/api/query?id_list={base_id}"

    def _do_fetch():
        resp = httpx.get(api_url, timeout=30, follow_redirects=True)
        resp.raise_for_status()
        return resp

    resp = with_retry(_do_fetch, max_attempts=4, base_delay=5.0, label=f"arxiv_metadata({arxiv_id})")

    root = ElementTree.fromstring(resp.text)
    entry = root.find(f"{{{ATOM_NS}}}entry")
    if entry is None:
        raise ValueError(f"No arXiv entry found for {arxiv_id}")

    title_el = entry.find(f"{{{ATOM_NS}}}title")
    title = title_el.text.strip().replace("\n", " ") if title_el is not None and title_el.text else "Untitled"

    summary_el = entry.find(f"{{{ATOM_NS}}}summary")
    abstract = summary_el.text.strip() if summary_el is not None and summary_el.text else ""

    authors = []
    for author_el in entry.findall(f"{{{ATOM_NS}}}author"):
        name_el = author_el.find(f"{{{ATOM_NS}}}name")
        if name_el is not None and name_el.text:
            authors.append(name_el.text.strip())

    published_el = entry.find(f"{{{ATOM_NS}}}published")
    published_at = published_el.text[:10] if published_el is not None and published_el.text else None

    categories = []
    for cat_el in entry.findall(f"{{{ATOM_NS}}}category"):
        term = cat_el.get("term")
        if term:
            categories.append(term)

    doi_el = entry.find(f"{{{ARXIV_NS}}}doi")
    doi = doi_el.text.strip() if doi_el is not None and doi_el.text else None

    journal_el = entry.find(f"{{{ARXIV_NS}}}journal_ref")
    journal_ref = journal_el.text.strip() if journal_el is not None and journal_el.text else None

    return {
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "published_at": published_at,
        "categories": categories,
        "doi": doi,
        "journal_ref": journal_ref,
    }


def _get_theme_hints(categories: list[str]) -> list[str]:
    """Map arXiv categories to theme_id slugs."""
    hints = set()
    for cat in categories:
        # Exact match first
        if cat in CATEGORY_THEME_HINTS:
            hints.add(CATEGORY_THEME_HINTS[cat])
        else:
            # Prefix fallback (e.g., q-bio.BM -> q-bio)
            prefix = cat.split(".")[0] if "." in cat else cat
            if prefix in CATEGORY_THEME_HINTS:
                hints.add(CATEGORY_THEME_HINTS[prefix])
    return sorted(hints)


def _download_pdf(arxiv_id: str, dest: Path, max_size_mb: int = 50) -> Path:
    """Download PDF from arXiv."""
    from ingest.http_retry import with_retry

    base_id = re.sub(r"v\d+$", "", arxiv_id)
    pdf_url = f"https://arxiv.org/pdf/{base_id}.pdf"
    pdf_path = dest / "raw.pdf"

    def _do_download():
        with httpx.stream("GET", pdf_url, timeout=60, follow_redirects=True) as resp:
            resp.raise_for_status()
            content_length = resp.headers.get("content-length")
            if content_length and int(content_length) > max_size_mb * 1024 * 1024:
                raise ValueError(f"PDF too large: {int(content_length)} bytes")

            with open(pdf_path, "wb") as f:
                for chunk in resp.iter_bytes(chunk_size=8192):
                    f.write(chunk)
        return pdf_path

    return with_retry(_do_download, max_attempts=3, base_delay=5.0, label=f"arxiv_pdf({arxiv_id})")


def _pdf_to_markdown(pdf_path: Path) -> str:
    """Convert PDF to markdown using markitdown, fallback to PyMuPDF."""
    # Try markitdown first
    try:
        from markitdown import MarkItDown
        mid = MarkItDown()
        result = mid.convert(str(pdf_path))
        if result and result.text_content:
            return result.text_content
    except Exception as e:
        logger.warning("markitdown failed, trying PyMuPDF: %s", e)

    # Fallback to PyMuPDF
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text())
        doc.close()
        return "\n\n".join(text_parts)
    except Exception as e:
        logger.error("PyMuPDF also failed: %s", e)
        raise ValueError(f"Could not extract text from PDF: {e}")


def fetch(url: str, library_path: Path) -> dict:
    """Ingest an arXiv paper.

    Returns a dict with source metadata and clean text.
    """
    arxiv_id = _parse_arxiv_id(url)
    source_id = str(ULID())

    # Step 1: Fetch metadata
    meta = _fetch_metadata(arxiv_id)

    # Step 2: Download PDF
    source_dir = library_path / source_id
    source_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = _download_pdf(arxiv_id, source_dir)

    # Step 3: Convert PDF to markdown
    raw_text = _pdf_to_markdown(pdf_path)

    # Step 4: Strip backmatter
    clean_text = strip_backmatter(raw_text)

    # Step 5: Prepend abstract if not in body
    if meta["abstract"] and "abstract" not in clean_text.lower()[:500]:
        clean_text = f"## Abstract\n\n{meta['abstract']}\n\n{clean_text}"

    # Save clean text
    (source_dir / "clean.md").write_text(clean_text, encoding="utf-8")

    # Get theme hints
    theme_hints = _get_theme_hints(meta["categories"])

    # Write metadata
    meta_file = {
        "id": source_id,
        "source_type": "paper",
        "url": url,
        "title": meta["title"],
        "authors": meta["authors"],
        "abstract": meta["abstract"],
        "published_at": normalize_date(meta["published_at"]),
        "arxiv_id": arxiv_id,
        "categories": meta["categories"],
        "category_theme_hints": theme_hints,
    }
    write_meta_yaml(source_dir, meta_file)

    return {
        "id": source_id,
        "source_type": "paper",
        "url": url,
        "title": meta["title"],
        "authors": meta["authors"],
        "abstract": meta["abstract"],
        "published_at": normalize_date(meta["published_at"]),
        "clean_text": clean_text,
        "library_path": str(source_dir),
        "processing_status": "ingested",
        "metadata": {
            "arxiv_id": arxiv_id,
            "categories": meta["categories"],
            "doi": meta["doi"],
            "journal_ref": meta["journal_ref"],
            "category_theme_hints": theme_hints,
        },
    }
