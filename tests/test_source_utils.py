"""Tests for ingest.source_utils: normalize_date, write_meta_yaml, parse_participants_from_summary."""

import yaml
from pathlib import Path

import pytest

from ingest.source_utils import normalize_date, write_meta_yaml, parse_participants_from_summary


# ---------------------------------------------------------------------------
# normalize_date
# ---------------------------------------------------------------------------

class TestNormalizeDate:
    def test_none(self):
        assert normalize_date(None) is None

    def test_empty(self):
        assert normalize_date("") is None
        assert normalize_date("   ") is None

    def test_already_clean(self):
        assert normalize_date("2025-01-23") == "2025-01-23"

    def test_yyyymmdd_bare(self):
        """yt-dlp upload_date format."""
        assert normalize_date("20250123") == "2025-01-23"

    def test_pdf_d_prefix(self):
        """PDF D:YYYYMMDD... format."""
        assert normalize_date("D:20230615120000") == "2023-06-15"

    def test_pdf_d_prefix_short(self):
        assert normalize_date("D:20230615") == "2023-06-15"

    def test_iso8601_with_time(self):
        assert normalize_date("2025-01-23T14:30:00Z") == "2025-01-23"

    def test_iso8601_with_timezone(self):
        assert normalize_date("2025-01-23T14:30:00+05:00") == "2025-01-23"

    def test_iso8601_with_space(self):
        assert normalize_date("2025-01-23 14:30:00") == "2025-01-23"

    def test_rfc2822(self):
        """RSS feed date format."""
        assert normalize_date("Mon, 23 Jan 2025 14:30:00 GMT") == "2025-01-23"

    def test_rfc2822_no_day(self):
        assert normalize_date("23 Jan 2025 14:30:00 +0000") == "2025-01-23"

    def test_truncated_iso(self):
        """Article meta tags often truncate to 25 chars."""
        assert normalize_date("2025-01-23T14:30:00+05:00") == "2025-01-23"

    def test_unparseable(self):
        assert normalize_date("not a date") is None

    def test_whitespace_handling(self):
        assert normalize_date("  2025-01-23  ") == "2025-01-23"


# ---------------------------------------------------------------------------
# write_meta_yaml
# ---------------------------------------------------------------------------

class TestWriteMetaYaml:
    def test_basic_write(self, tmp_path):
        data = {
            "id": "ABC123",
            "source_type": "article",
            "url": "https://example.com",
            "title": "Test Article",
            "published_at": "2025-01-23",
        }
        write_meta_yaml(tmp_path, data)
        content = (tmp_path / "meta.yaml").read_text(encoding="utf-8")
        loaded = yaml.safe_load(content)
        assert loaded["id"] == "ABC123"
        assert loaded["title"] == "Test Article"
        assert loaded["published_at"] == "2025-01-23"

    def test_skips_none_values(self, tmp_path):
        data = {
            "id": "ABC123",
            "source_type": "article",
            "url": "https://example.com",
            "title": "Test",
            "authors": None,
            "published_at": None,
        }
        write_meta_yaml(tmp_path, data)
        content = (tmp_path / "meta.yaml").read_text(encoding="utf-8")
        loaded = yaml.safe_load(content)
        assert "authors" not in loaded
        assert "published_at" not in loaded

    def test_skips_empty_lists(self, tmp_path):
        data = {
            "id": "ABC123",
            "source_type": "paper",
            "title": "Test",
            "authors": [],
            "categories": [],
        }
        write_meta_yaml(tmp_path, data)
        loaded = yaml.safe_load((tmp_path / "meta.yaml").read_text(encoding="utf-8"))
        assert "authors" not in loaded
        assert "categories" not in loaded

    def test_excludes_internal_fields(self, tmp_path):
        data = {
            "id": "ABC123",
            "source_type": "article",
            "title": "Test",
            "clean_text": "should not appear",
            "library_path": "/some/path",
            "processing_status": "complete",
            "metadata": {"key": "val"},
            "ingested_at": "2025-01-23",
            "fts_vector": "tsvector",
        }
        write_meta_yaml(tmp_path, data)
        loaded = yaml.safe_load((tmp_path / "meta.yaml").read_text(encoding="utf-8"))
        assert "clean_text" not in loaded
        assert "library_path" not in loaded
        assert "processing_status" not in loaded
        assert "metadata" not in loaded
        assert "ingested_at" not in loaded
        assert "fts_vector" not in loaded

    def test_field_order_preserved(self, tmp_path):
        data = {
            "title": "Test",
            "id": "ABC123",
            "source_type": "paper",
            "authors": ["Alice"],
            "url": "https://example.com",
        }
        write_meta_yaml(tmp_path, data)
        content = (tmp_path / "meta.yaml").read_text(encoding="utf-8")
        lines = [l for l in content.strip().split("\n") if l.strip()]
        keys = [l.split(":")[0] for l in lines if ":" in l]
        # id should come before source_type which comes before url
        assert keys.index("id") < keys.index("source_type")
        assert keys.index("source_type") < keys.index("url")

    def test_includes_type_specific_fields(self, tmp_path):
        data = {
            "id": "ABC123",
            "source_type": "video",
            "title": "Test Video",
            "video_id": "dQw4w9WgXcQ",
            "channel": "TestChannel",
        }
        write_meta_yaml(tmp_path, data)
        loaded = yaml.safe_load((tmp_path / "meta.yaml").read_text(encoding="utf-8"))
        assert loaded["video_id"] == "dQw4w9WgXcQ"
        assert loaded["channel"] == "TestChannel"


# ---------------------------------------------------------------------------
# parse_participants_from_summary
# ---------------------------------------------------------------------------

class TestParseParticipantsFromSummary:
    def test_empty(self):
        assert parse_participants_from_summary("") == []
        assert parse_participants_from_summary(None) == []

    def test_no_participants_line(self):
        summary = "# Title\n2025-01-23\nhttps://example.com\n\n---\nContent here."
        assert parse_participants_from_summary(summary) == []

    def test_basic_participants(self):
        summary = (
            "# Interview Title\n"
            "2025-01-23 · Host Name\n"
            "https://youtube.com/watch?v=abc\n"
            "\n"
            "Participants: Alice, Bob, Charlie\n"
            "\n"
            "---\n"
            "Content here."
        )
        assert parse_participants_from_summary(summary) == ["Alice", "Bob", "Charlie"]

    def test_participants_with_affiliations(self):
        summary = (
            "# Title\n"
            "2025-01-23\n"
            "https://youtube.com/watch?v=abc\n"
            "\n"
            "Participants: Demis Hassabis (CEO, Google DeepMind), Alex Kantrowitz (host, Big Technology Podcast)\n"
            "\n"
            "---\n"
            "Content."
        )
        result = parse_participants_from_summary(summary)
        assert result == ["Demis Hassabis", "Alex Kantrowitz"]

    def test_bold_participants_label(self):
        summary = (
            "# Title\n\n"
            "**Participants:** John Smith (CEO), Jane Doe (CTO)\n"
            "\n---\n"
            "Content."
        )
        result = parse_participants_from_summary(summary)
        assert result == ["John Smith", "Jane Doe"]

    def test_participants_with_nested_parens(self):
        """Parenthetical with commas inside should not split."""
        summary = (
            "# Title\n\n"
            "Participants: Demis Hassabis (CEO, Google DeepMind; Nobel laureate), Alex Kantrowitz (host)\n"
            "\n---\nContent."
        )
        result = parse_participants_from_summary(summary)
        assert result == ["Demis Hassabis", "Alex Kantrowitz"]

    def test_only_searches_header(self):
        """Participants line after --- should be ignored."""
        summary = (
            "# Title\n\n---\n"
            "Participants: Should Not Match\n"
            "Content here."
        )
        assert parse_participants_from_summary(summary) == []

    def test_single_participant(self):
        summary = "# Title\n\nParticipants: Solo Speaker\n\n---\nContent."
        assert parse_participants_from_summary(summary) == ["Solo Speaker"]
