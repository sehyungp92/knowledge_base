"""Tests for the notification emitter."""

from unittest.mock import patch, MagicMock

from ingest.notification_emitter import emit_notification


def test_emit_notification_inserts():
    with patch("ingest.notification_emitter.db") as mock_db:
        conn = MagicMock()
        conn.__enter__ = MagicMock(return_value=conn)
        conn.__exit__ = MagicMock(return_value=False)
        mock_db.get_conn.return_value = conn

        emit_notification("test_type", "source", "s1", "Test notification")

        conn.execute.assert_called_once()
        call_args = conn.execute.call_args
        assert "INSERT INTO notifications" in call_args[0][0]
        assert call_args[0][1][0] == "test_type"
        assert call_args[0][1][2] == "s1"
        conn.commit.assert_called_once()


def test_emit_notification_with_detail():
    with patch("ingest.notification_emitter.db") as mock_db:
        conn = MagicMock()
        conn.__enter__ = MagicMock(return_value=conn)
        conn.__exit__ = MagicMock(return_value=False)
        mock_db.get_conn.return_value = conn

        emit_notification(
            "anticipation_match", "anticipation", "a1",
            "Evidence found for prediction",
            detail={"match_confidence": 0.85},
            source_id="src_123",
        )

        call_args = conn.execute.call_args[0][1]
        assert call_args[0] == "anticipation_match"
        assert '"match_confidence": 0.85' in call_args[4]
        assert call_args[5] == "src_123"


def test_emit_notification_swallows_errors():
    with patch("ingest.notification_emitter.db") as mock_db:
        mock_db.get_conn.side_effect = RuntimeError("no pool")
        # Should not raise
        emit_notification("test", "source", "s1", "Test notification")
