"""Podcast ingestion: RSS feed parsing, audio download, Whisper transcription."""

from __future__ import annotations

import logging
import subprocess
import tempfile
from pathlib import Path

import httpx
from ulid import ULID

from ingest.source_utils import normalize_date, write_meta_yaml

logger = logging.getLogger(__name__)


def _parse_rss_feed(url: str) -> tuple[str | None, list[dict]]:
    """Parse RSS feed and return (podcast_name, episodes)."""
    import feedparser
    feed = feedparser.parse(url)
    podcast_name = feed.feed.get("title")
    episodes = []
    for entry in feed.entries:
        episode = {
            "title": entry.get("title", "Untitled Episode"),
            "url": None,
            "published": entry.get("published"),
            "author": entry.get("author"),
        }
        # Find audio enclosure
        for enc in entry.get("enclosures", []):
            if enc.get("type", "").startswith("audio/"):
                episode["url"] = enc["href"]
                break
        # Fallback to links
        if not episode["url"]:
            for link in entry.get("links", []):
                if link.get("type", "").startswith("audio/"):
                    episode["url"] = link["href"]
                    break
        if episode["url"]:
            episodes.append(episode)
    return podcast_name, episodes


def _download_audio(url: str, dest: Path, timeout: int = 300) -> Path:
    """Download audio file from URL."""
    audio_path = dest / "raw.mp3"
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "-x", "--audio-format", "mp3",
                "-o", str(audio_path),
                url,
            ],
            capture_output=True, text=True, timeout=timeout,
        )
        if audio_path.exists():
            return audio_path
    except Exception as e:
        logger.info("yt-dlp download failed, trying direct download: %s", e)

    # Direct download fallback
    with httpx.stream("GET", url, timeout=timeout, follow_redirects=True) as resp:
        resp.raise_for_status()
        with open(audio_path, "wb") as f:
            for chunk in resp.iter_bytes(chunk_size=8192):
                f.write(chunk)
    return audio_path


def _transcribe_whisper(audio_path: Path) -> str:
    """Transcribe audio using faster-whisper."""
    from faster_whisper import WhisperModel
    model = WhisperModel("base", compute_type="int8")
    segments, _ = model.transcribe(str(audio_path))
    return " ".join(seg.text.strip() for seg in segments)


def fetch(url: str, library_path: Path, episode_index: int = 0) -> dict:
    """Ingest a podcast episode from RSS feed URL or direct audio URL.

    Returns a dict with source metadata and clean text.
    """
    source_id = str(ULID())
    source_dir = library_path / source_id
    source_dir.mkdir(parents=True, exist_ok=True)

    title = "Podcast Episode"
    audio_url = url
    published_at = None
    podcast_name = None
    rss_author = None

    # Check if this is an RSS feed
    if any(url.endswith(ext) for ext in [".xml", "/rss", "/feed"]) or "feed" in url.lower():
        podcast_name, episodes = _parse_rss_feed(url)
        if not episodes:
            raise ValueError(f"No episodes found in RSS feed: {url}")
        if episode_index >= len(episodes):
            raise ValueError(f"Episode index {episode_index} out of range (found {len(episodes)})")
        episode = episodes[episode_index]
        title = episode["title"]
        audio_url = episode["url"]
        published_at = normalize_date(episode.get("published"))
        rss_author = episode.get("author")

    # Download audio
    audio_path = _download_audio(audio_url, source_dir)

    # Transcribe
    clean_text = _transcribe_whisper(audio_path)

    # Save clean text
    (source_dir / "clean.md").write_text(clean_text, encoding="utf-8")

    # Write metadata
    meta = {
        "id": source_id,
        "source_type": "podcast",
        "url": url,
        "title": title,
        "published_at": published_at,
        "podcast_name": podcast_name,
    }
    write_meta_yaml(source_dir, meta)

    metadata = {"whisper_used": True}
    if podcast_name:
        metadata["podcast_name"] = podcast_name

    return {
        "id": source_id,
        "source_type": "podcast",
        "url": url,
        "title": title,
        "published_at": published_at,
        "clean_text": clean_text,
        "library_path": str(source_dir),
        "processing_status": "ingested",
        "metadata": metadata,
    }
