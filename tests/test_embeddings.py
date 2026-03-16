"""Tests for reading_app.embeddings."""

from unittest.mock import patch, MagicMock
import json

from reading_app.embeddings import embed_sync, embed_batch, configure


def test_embed_sync_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"embedding": [0.1] * 768}

    with patch("reading_app.embeddings.httpx.post", return_value=mock_response):
        result = embed_sync("test text")
        assert result is not None
        assert len(result) == 768


def test_embed_sync_failure():
    with patch("reading_app.embeddings.httpx.post", side_effect=Exception("Connection failed")):
        result = embed_sync("test text")
        assert result is None


def test_embed_batch():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"embedding": [0.1] * 768}

    with patch("reading_app.embeddings.httpx.post", return_value=mock_response):
        results = embed_batch(["text1", "text2"])
        assert len(results) == 2


def test_configure():
    configure(base_url="http://custom:11434", model="custom-model")
    # Should not raise
