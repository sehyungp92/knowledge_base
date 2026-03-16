"""Tests for ingest modules: article, pdf, bulk_ingest helpers."""

import re

from ingest.article import _normalize_text, _extract_title_from_html
from scripts.bulk_ingest import _is_direct_pdf_url, _github_blob_to_raw, _validate_url


def test_normalize_text_collapses_blank_lines():
    text = "line1\n\n\n\n\nline2"
    result = _normalize_text(text)
    assert "\n\n\n" not in result
    assert "line1\n\nline2" == result


def test_normalize_text_strips_trailing():
    text = "line1   \nline2  "
    result = _normalize_text(text)
    assert result == "line1\nline2"


def test_extract_title_from_html_og():
    html = '<html><head><meta property="og:title" content="Test Title"/></head><body></body></html>'
    assert _extract_title_from_html(html) == "Test Title"


def test_extract_title_from_html_title_tag():
    html = "<html><head><title>Fallback Title</title></head><body></body></html>"
    assert _extract_title_from_html(html) == "Fallback Title"


def test_extract_title_from_html_none():
    html = "<html><head></head><body></body></html>"
    assert _extract_title_from_html(html) == "Untitled Article"


# --- bulk_ingest helpers ---


def test_is_direct_pdf_url_true():
    assert _is_direct_pdf_url("https://example.com/paper.pdf")
    assert _is_direct_pdf_url("https://example.com/dir/paper.PDF")


def test_is_direct_pdf_url_false():
    assert not _is_direct_pdf_url("https://arxiv.org/abs/2401.12345")
    assert not _is_direct_pdf_url("https://example.com/page.html")
    assert not _is_direct_pdf_url("https://example.com/pdf/viewer")


def test_github_blob_to_raw():
    url = "https://github.com/user/repo/blob/main/paper.pdf"
    assert _github_blob_to_raw(url) == "https://raw.githubusercontent.com/user/repo/main/paper.pdf"


def test_github_blob_to_raw_passthrough():
    url = "https://example.com/paper.pdf"
    assert _github_blob_to_raw(url) == url


def test_validate_url_valid():
    assert _validate_url("https://example.com/article") is None
    assert _validate_url("http://example.com") is None


def test_validate_url_no_scheme():
    err = _validate_url("GPT-5 Hands-On Review")
    assert err is not None
    assert "scheme" in err.lower() or "hostname" in err.lower()


def test_validate_url_no_host():
    err = _validate_url("https://")
    assert err is not None
