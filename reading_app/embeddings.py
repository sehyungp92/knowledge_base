"""Embedding generation via Ollama nomic-embed-text (768-dim)."""

from __future__ import annotations

import logging
import os

import httpx

logger = logging.getLogger(__name__)

_OLLAMA_BASE_URL = None
_MODEL = "nomic-embed-text"


def _base_url() -> str:
    global _OLLAMA_BASE_URL
    if _OLLAMA_BASE_URL is None:
        _OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    return _OLLAMA_BASE_URL


def configure(base_url: str | None = None, model: str | None = None):
    """Configure the embedding client."""
    global _OLLAMA_BASE_URL, _MODEL
    if base_url:
        _OLLAMA_BASE_URL = base_url
    if model:
        _MODEL = model


def embed_sync(text: str) -> list[float] | None:
    """Embed a single text. Returns None on connection failure (graceful degradation)."""
    try:
        resp = httpx.post(
            f"{_base_url()}/api/embeddings",
            json={"model": _MODEL, "prompt": text},
            timeout=30.0,
        )
        resp.raise_for_status()
        return resp.json()["embedding"]
    except Exception:
        logger.warning("Embedding failed for text (len=%d), returning None", len(text), exc_info=True)
        return None


def embed_batch(texts: list[str]) -> list[list[float] | None]:
    """Embed multiple texts in a single API call via Ollama /api/embed.

    Uses the batch ``input`` parameter so all texts are embedded in one
    HTTP round-trip.  Falls back to sequential ``embed_sync`` calls if
    the batch endpoint is unavailable (older Ollama versions).

    Returns a list parallel to *texts*: each entry is the embedding
    vector or ``None`` on failure.
    """
    if not texts:
        return []

    try:
        resp = httpx.post(
            f"{_base_url()}/api/embed",
            json={"model": _MODEL, "input": texts},
            timeout=max(30.0, len(texts) * 2.0),
        )
        resp.raise_for_status()
        embeddings = resp.json().get("embeddings", [])
        # Pad with None if the response is shorter than expected
        while len(embeddings) < len(texts):
            embeddings.append(None)
        return embeddings
    except Exception:
        logger.warning(
            "Batch embedding failed for %d texts, falling back to sequential",
            len(texts), exc_info=True,
        )
        return [embed_sync(t) for t in texts]
