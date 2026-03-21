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


# ---------------------------------------------------------------------------
# Tests merged from test_source_quality.py — source quality helpers
# ---------------------------------------------------------------------------

from ingest.source_quality import (
    assess_source_quality,
    get_landscape_issue,
    get_summary_issue,
    read_source_artifact_text,
)


def test_read_source_artifact_text_resolves_library_root(tmp_path):
    library_path = tmp_path / "library"
    source_dir = library_path / "src_123"
    source_dir.mkdir(parents=True)
    (source_dir / "deep_summary.md").write_text("Summary content", encoding="utf-8")

    assert read_source_artifact_text(library_path, "src_123", "deep_summary.md") == "Summary content"


def test_get_summary_issue_detects_placeholder_output():
    summary = "Summary generation failed because you've hit your limit."

    assert get_summary_issue(summary) == "placeholder"


def test_get_landscape_issue_detects_empty_output():
    signals = {
        "capabilities": [],
        "limitations": [],
        "bottlenecks": [],
        "breakthroughs": [],
    }

    assert get_landscape_issue(signals) == "empty"


def test_assess_source_quality_marks_missing_outputs_incomplete():
    assessment = assess_source_quality(
        theme_count=0,
        claim_count=0,
        summary_text="summary pending",
        landscape_signals={
            "capabilities": [],
            "limitations": [],
            "bottlenecks": [],
            "breakthroughs": [],
        },
        require_summary=True,
        require_landscape=True,
    )

    assert assessment["status"] == "incomplete"
    assert assessment["issues"] == [
        "no_themes",
        "no_claims",
        "summary:placeholder",
        "landscape:empty",
    ]
