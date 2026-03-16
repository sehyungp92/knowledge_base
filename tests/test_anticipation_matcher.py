"""Tests for anticipation matching against extracted landscape signals."""

import json
import sys
import pytest
from unittest.mock import patch, MagicMock

from ingest.anticipation_matcher import match_anticipations, persist_anticipation_matches, _parse_matches


class TestParseMatches:
    """Test JSON parsing of LLM match output."""

    def test_parse_fenced_json(self):
        text = '```json\n[{"anticipation_id": "a1", "match_type": "confirming", "evidence": "test", "reasoning": "because", "confidence": 0.8}]\n```'
        result = _parse_matches(text)
        assert len(result) == 1
        assert result[0]["anticipation_id"] == "a1"
        assert result[0]["match_type"] == "confirming"

    def test_parse_raw_json(self):
        text = 'Here are the matches: [{"anticipation_id": "a2", "match_type": "disconfirming", "evidence": "test", "reasoning": "why", "confidence": 0.6}]'
        result = _parse_matches(text)
        assert len(result) == 1
        assert result[0]["match_type"] == "disconfirming"

    def test_parse_empty_array(self):
        text = "No matches found.\n```json\n[]\n```"
        result = _parse_matches(text)
        assert result == []

    def test_parse_invalid_json(self):
        text = "This is not valid JSON at all"
        result = _parse_matches(text)
        assert result == []


class TestMatchAnticipations:
    """Test the anticipation matching logic."""

    def test_no_themes_returns_empty(self):
        result = match_anticipations({"capabilities": []}, [], "src_1")
        assert result == []

    def test_no_anticipations_returns_empty(self):
        mock_db = MagicMock()
        mock_db.get_open_anticipations_for_themes = MagicMock(return_value=[])
        saved = sys.modules.get("reading_app.db")
        try:
            sys.modules["reading_app.db"] = mock_db
            result = match_anticipations({"capabilities": []}, ["robotics"], "src_1")
            assert result == []
        finally:
            if saved is None:
                sys.modules.pop("reading_app.db", None)
            else:
                sys.modules["reading_app.db"] = saved

    def test_no_signals_returns_empty(self):
        mock_db = MagicMock()
        mock_db.get_open_anticipations_for_themes = MagicMock(
            return_value=[{"id": "a1", "prediction": "test", "theme_id": "robotics"}]
        )
        saved = sys.modules.get("reading_app.db")
        try:
            sys.modules["reading_app.db"] = mock_db
            result = match_anticipations(
                {"capabilities": [], "limitations": [], "bottlenecks": []},
                ["robotics"],
                "src_1",
            )
            assert result == []
        finally:
            if saved is None:
                sys.modules.pop("reading_app.db", None)
            else:
                sys.modules["reading_app.db"] = saved


class TestPersistAnticipationMatches:
    """Test persisting anticipation matches."""

    def test_empty_matches_returns_zero(self):
        assert persist_anticipation_matches([], "src_1") == 0

    def test_persists_matches(self):
        mock_db = MagicMock()
        mock_db.append_anticipation_evidence = MagicMock(return_value={"id": "a1"})
        saved = sys.modules.get("reading_app.db")
        try:
            sys.modules["reading_app.db"] = mock_db
            matches = [
                {"anticipation_id": "a1", "match_type": "confirming", "evidence": "test", "reasoning": "why", "confidence": 0.8},
            ]
            count = persist_anticipation_matches(matches, "src_1")
            assert count == 1
            mock_db.append_anticipation_evidence.assert_called_once()
        finally:
            if saved is None:
                sys.modules.pop("reading_app.db", None)
            else:
                sys.modules["reading_app.db"] = saved

    def test_handles_persist_failure(self):
        mock_db = MagicMock()
        mock_db.append_anticipation_evidence = MagicMock(side_effect=Exception("DB error"))
        saved = sys.modules.get("reading_app.db")
        try:
            sys.modules["reading_app.db"] = mock_db
            matches = [
                {"anticipation_id": "a1", "match_type": "confirming", "evidence": "test", "reasoning": "why", "confidence": 0.8},
            ]
            count = persist_anticipation_matches(matches, "src_1")
            assert count == 0
        finally:
            if saved is None:
                sys.modules.pop("reading_app.db", None)
            else:
                sys.modules["reading_app.db"] = saved
