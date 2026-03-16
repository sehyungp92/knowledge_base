"""Tests for ingest.arxiv module."""

from ingest.arxiv import (
    _parse_arxiv_id,
    _get_theme_hints,
    CATEGORY_THEME_HINTS,
)
from ingest.section_slicer import strip_backmatter


def test_parse_arxiv_id_abs():
    assert _parse_arxiv_id("https://arxiv.org/abs/2310.01234") == "2310.01234"


def test_parse_arxiv_id_pdf():
    assert _parse_arxiv_id("https://arxiv.org/pdf/2310.01234") == "2310.01234"


def test_parse_arxiv_id_versioned():
    assert _parse_arxiv_id("https://arxiv.org/abs/2310.01234v2") == "2310.01234v2"


def test_parse_arxiv_id_invalid():
    try:
        _parse_arxiv_id("https://example.com")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_category_hints_cs_lg():
    assert CATEGORY_THEME_HINTS["cs.LG"] == "training_paradigms"


def test_category_hints_cs_cl():
    assert CATEGORY_THEME_HINTS["cs.CL"] == "language_and_communication"


def test_get_theme_hints_exact():
    hints = _get_theme_hints(["cs.LG", "cs.CL"])
    assert "training_paradigms" in hints
    assert "language_and_communication" in hints


def test_get_theme_hints_prefix_fallback():
    hints = _get_theme_hints(["q-bio.BM"])
    assert "drug_discovery" in hints


def test_get_theme_hints_unknown():
    hints = _get_theme_hints(["xx.YY"])
    assert len(hints) == 0


def test_strip_backmatter_removes_references():
    text = "## Introduction\nContent here.\n\n## References\n[1] Foo\n[2] Bar"
    result = strip_backmatter(text)
    assert "Content here" in result
    assert "[1] Foo" not in result


def test_strip_backmatter_preserves_content():
    text = "## Introduction\nContent here.\n\n## Results\nGood results."
    result = strip_backmatter(text)
    assert "Good results" in result
