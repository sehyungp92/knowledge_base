"""Tests for source type detection and common ingest utilities."""

import re

from ingest.youtube import _extract_video_id, parse_youtube_input, _parse_timestamp
from ingest.arxiv import _parse_arxiv_id, _get_theme_hints, CATEGORY_THEME_HINTS


def test_detect_youtube_url():
    assert _extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_detect_youtube_short_url():
    assert _extract_video_id("https://youtu.be/dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_detect_youtube_embed():
    assert _extract_video_id("https://youtube.com/embed/dQw4w9WgXcQ") == "dQw4w9WgXcQ"


def test_parse_arxiv_abs():
    assert _parse_arxiv_id("https://arxiv.org/abs/2310.01234") == "2310.01234"


def test_parse_arxiv_pdf():
    assert _parse_arxiv_id("https://arxiv.org/pdf/2310.01234") == "2310.01234"


def test_parse_arxiv_versioned():
    assert _parse_arxiv_id("https://arxiv.org/abs/2310.01234v2") == "2310.01234v2"


def test_parse_timestamp_mmss():
    assert _parse_timestamp("40:08") == 2408


def test_parse_timestamp_hmmss():
    assert _parse_timestamp("1:58:11") == 7091


def test_parse_youtube_input_no_ranges():
    url, ranges = parse_youtube_input("https://youtube.com/watch?v=X")
    assert url == "https://youtube.com/watch?v=X"
    assert ranges is None


def test_parse_youtube_input_with_ranges():
    url, ranges = parse_youtube_input("https://youtube.com/watch?v=X 40:08-1:58:11, 2:28:46-3:06:47")
    assert url == "https://youtube.com/watch?v=X"
    assert len(ranges) == 2
    assert ranges[0] == (2408, 7091)


def test_category_theme_hints_exact():
    hints = _get_theme_hints(["cs.LG"])
    assert "training_paradigms" in hints


def test_category_theme_hints_prefix():
    hints = _get_theme_hints(["q-bio.BM"])
    assert "drug_discovery" in hints


def test_category_theme_hints_multiple():
    hints = _get_theme_hints(["cs.LG", "cs.CL", "stat.ML"])
    assert "training_paradigms" in hints
    assert "language_and_communication" in hints
