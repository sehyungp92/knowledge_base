"""YouTube ingestion: 3-tier transcript fallback with time-range filtering.

Uses yt-dlp Python API for metadata and subtitle extraction, with PO Token
support for bypassing bot detection and hardened extractor args.
"""

from __future__ import annotations

import logging
import re
import subprocess
import tempfile
from pathlib import Path

from ulid import ULID

from ingest.source_utils import normalize_date, write_meta_yaml

logger = logging.getLogger(__name__)

# Try to import PO Token generator for bot detection bypass
try:
    from yt_dlp_get_pot import get_pot as _get_pot
except ImportError:
    _get_pot = None


def _get_po_token() -> str | None:
    """Generate a PO Token to bypass YouTube bot detection.

    Requires yt-dlp-get-pot package. Returns None if unavailable or fails.
    """
    if _get_pot is None:
        return None
    try:
        token = _get_pot()
        logger.info("PO Token generated successfully")
        return token
    except Exception as e:
        logger.debug("PO Token generation failed: %s", e)
        return None


def _base_ytdlp_opts() -> dict:
    """Base yt-dlp options shared across calls: user agent, player clients, PO token."""
    opts: dict = {
        "quiet": True,
        "no_warnings": True,
        "user_agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        ),
        "extractor_args": {},
    }
    po_token = _get_po_token()
    if po_token:
        opts["extractor_args"]["youtube"]["po_token"] = f"web+{po_token}"
    return opts


def parse_youtube_input(raw: str) -> tuple[str, list[tuple[int, int]] | None]:
    """Parse 'URL [ranges]' string into (url, time_ranges).

    Timestamps accept MM:SS or H:MM:SS / HH:MM:SS.
    Example: 'https://youtube.com/watch?v=X 40:08-1:58:11, 2:28:46-3:06:47'
    """
    parts = raw.strip().split(None, 1)
    url = parts[0]
    if len(parts) == 1:
        return url, None

    range_str = parts[1]
    ranges = []
    for segment in range_str.split(","):
        segment = segment.strip()
        m = re.match(r"(\d+(?::\d+)+)\s*-\s*(\d+(?::\d+)+)", segment)
        if m:
            start = _parse_timestamp(m.group(1))
            end = _parse_timestamp(m.group(2))
            ranges.append((start, end))

    return url, ranges if ranges else None


def _parse_timestamp(ts: str) -> int:
    """Parse a timestamp string to seconds."""
    parts = ts.split(":")
    parts = [int(p) for p in parts]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    elif len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return parts[0]


def _extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL."""
    patterns = [
        r"(?:v=|/v/)([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"embed/([a-zA-Z0-9_-]{11})",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    raise ValueError(f"Cannot extract video ID from URL: {url}")


def _get_video_metadata(video_id: str) -> dict:
    """Get video title, upload date, and channel in a single extract_info call.

    Returns dict with keys: title, published_at, channel (any may be None).
    """
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        import yt_dlp
        opts = _base_ytdlp_opts()
        opts["skip_download"] = True
        # Don't try to resolve formats — we only need metadata
        opts["extract_flat"] = False
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        title = info.get("title") or f"YouTube Video {video_id}"
        channel = info.get("channel") or info.get("uploader")
        published_at = normalize_date(info.get("upload_date"))

        return {"title": title, "published_at": published_at, "channel": channel}
    except Exception as e:
        logger.warning("yt-dlp extract_info failed for %s, falling back to CLI: %s", video_id, e)

    # Fallback: CLI calls if Python API fails
    title = f"YouTube Video {video_id}"
    try:
        result = subprocess.run(
            ["yt-dlp", "--get-title", video_url],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0 and result.stdout.strip():
            title = result.stdout.strip()
    except Exception:
        pass

    return {"title": title, "published_at": None, "channel": None}


def _provider1_transcript_api(
    video_id: str,
    time_ranges: list[tuple[int, int]] | None = None,
) -> str | None:
    """Provider 1: youtube-transcript-api (fastest, no download needed).

    If *time_ranges* is supplied, only entries whose start time falls within
    one of the (start_sec, end_sec) windows are kept.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        transcript_obj = api.fetch(video_id, languages=["en"])
        entries = list(transcript_obj)  # materialise once

        if time_ranges:
            total = len(entries)
            entries = [
                e for e in entries
                if any(rng_s <= e.start <= rng_e for rng_s, rng_e in time_ranges)
            ]
            logger.info(
                "Provider 1: time-range filter kept %d / %d entries for %s",
                len(entries), total, video_id,
            )

        lines = [entry.text for entry in entries]
        return "\n".join(lines)
    except Exception as e:
        logger.info("Provider 1 (transcript-api) failed for %s: %s", video_id, e)
        return None


def _provider2_ytdlp_subtitles(video_id: str, tmp_dir: Path) -> str | None:
    """Provider 2: yt-dlp subtitle extraction via Python API.

    Requests both manual and auto-generated subtitles in English,
    with fallback to Korean. Uses PO token and hardened extractor args.
    """
    try:
        import yt_dlp

        opts = _base_ytdlp_opts()
        opts.update({
            "writeautomaticsub": True,
            "writesubtitles": True,
            "skip_download": True,
            "subtitleslangs": ["en", "en-US", "en-GB", "en.*", "a.en", "a.en.*",
                               "ko", "ko.*", "a.ko", "a.ko.*"],
            "subtitlesformat": "vtt/srt/json3",
            "outtmpl": str(tmp_dir / "%(id)s.%(ext)s"),
            "ignoreerrors": True,
        })

        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}",
                download=True,
            )

        # Find subtitle files — check multiple naming patterns
        import glob
        sub_files = (glob.glob(str(tmp_dir / f"{video_id}*.vtt")) +
                     glob.glob(str(tmp_dir / f"{video_id}*.srt")) +
                     glob.glob(str(tmp_dir / f"{video_id}*.json3")))

        if not sub_files:
            logger.info("Provider 2: no subtitle file found for %s", video_id)
            return None

        # Prefer manual English subs, then auto English, then Korean, then any
        selected = None
        for lang_pattern in [".en.", ".en-", ".a.en", ".ko.", ".ko-", ".a.ko"]:
            for f in sub_files:
                if lang_pattern in Path(f).name.lower():
                    selected = f
                    break
            if selected:
                break
        selected = selected or sub_files[0]

        raw_text = Path(selected).read_text(encoding="utf-8")

        if selected.endswith(".json3"):
            return _parse_json3(raw_text)
        return _parse_vtt(raw_text)
    except Exception as e:
        logger.info("Provider 2 (yt-dlp subs) failed for %s: %s", video_id, e)
        return None


def _provider3_whisper(video_id: str, tmp_dir: Path) -> tuple[str | None, bool]:
    """Provider 3: yt-dlp audio download + faster-whisper.

    Uses Python API with hardened options for bot detection bypass.
    Returns (text, whisper_used).
    """
    try:
        import yt_dlp

        audio_path = tmp_dir / f"{video_id}.mp3"
        opts = _base_ytdlp_opts()
        opts.update({
            "extract_audio": True,
            "format": "bestaudio[ext=m4a]/bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }],
            "outtmpl": str(tmp_dir / f"{video_id}.%(ext)s"),
        })

        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])

        if not audio_path.exists():
            # yt-dlp may produce a slightly different filename
            import glob
            mp3_files = glob.glob(str(tmp_dir / f"{video_id}*.mp3"))
            if mp3_files:
                audio_path = Path(mp3_files[0])
            else:
                return None, False

        from faster_whisper import WhisperModel
        from ingest.podcast import _build_whisper_prompt
        model = WhisperModel("base", compute_type="int8")
        initial_prompt = _build_whisper_prompt()
        segments, _ = model.transcribe(str(audio_path), initial_prompt=initial_prompt)
        text = " ".join(seg.text.strip() for seg in segments)
        return text, True
    except Exception as e:
        logger.info("Provider 3 (whisper) failed for %s: %s", video_id, e)
        return None, False


def _parse_vtt(vtt_text: str) -> str:
    """Parse VTT content, dedup overlapping captions, collapse jitter."""
    lines = []
    seen = set()
    for line in vtt_text.split("\n"):
        line = line.strip()
        # Skip timestamps, WEBVTT header, empty lines
        if not line or line.startswith("WEBVTT") or "-->" in line:
            continue
        if re.match(r"^\d+$", line):
            continue
        # Strip HTML tags
        line = re.sub(r"<[^>]+>", "", line)
        if line and line not in seen:
            seen.add(line)
            lines.append(line)
    return " ".join(lines)


def _parse_json3(json_text: str) -> str | None:
    """Parse json3 subtitle format (YouTube's native format)."""
    import json
    try:
        data = json.loads(json_text)
        events = data.get("events", [])
        lines = []
        seen = set()
        for event in events:
            segs = event.get("segs", [])
            text = "".join(s.get("utf8", "") for s in segs).strip()
            text = text.replace("\n", " ")
            if text and text not in seen:
                seen.add(text)
                lines.append(text)
        return " ".join(lines) if lines else None
    except Exception:
        return None


def _filter_by_time_ranges(
    text: str, time_ranges: list[tuple[int, int]] | None, total_duration: int | None = None,
) -> str:
    """Approximate filter for providers that strip timestamp metadata.

    If we know the total video duration, we estimate the character position
    for each time range and extract those slices. This is a rough heuristic —
    Provider 1 applies exact filtering natively so this is only hit when
    falling back to Providers 2/3.
    """
    if not time_ranges or not total_duration or total_duration <= 0:
        return text
    chars_per_sec = len(text) / total_duration
    parts: list[str] = []
    for rng_start, rng_end in time_ranges:
        start_char = int(rng_start * chars_per_sec)
        end_char = int(rng_end * chars_per_sec)
        parts.append(text[start_char:end_char])
    filtered = "\n\n".join(parts)
    logger.info(
        "Approximate time-range filter: %d -> %d chars (%.0f%% kept)",
        len(text), len(filtered), 100 * len(filtered) / max(len(text), 1),
    )
    return filtered


def fetch(
    url: str,
    library_path: Path,
    time_ranges: list[tuple[int, int]] | None = None,
) -> dict:
    """Ingest a YouTube video transcript.

    Returns a dict with source metadata and clean text.
    """
    video_id = _extract_video_id(url)
    source_id = str(ULID())
    video_meta = _get_video_metadata(video_id)
    title = video_meta["title"]
    published_at = video_meta["published_at"]
    channel = video_meta["channel"]
    whisper_used = False
    processing_status = "ingested"

    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)

        # 3-tier fallback (Provider 1 applies time_ranges natively)
        clean_text = _provider1_transcript_api(video_id, time_ranges=time_ranges)
        if clean_text is None:
            clean_text = _provider2_ytdlp_subtitles(video_id, tmp_dir)
        if clean_text is None:
            clean_text, whisper_used = _provider3_whisper(video_id, tmp_dir)

        if clean_text is None:
            raise ValueError(f"Could not obtain transcript for {url}")

    # Auto-generated captions need punctuation
    if not whisper_used:
        # Heuristic: if very few periods/question marks, likely auto-generated
        punct_ratio = sum(1 for c in clean_text if c in ".?!") / max(len(clean_text), 1)
        if punct_ratio < 0.005:
            processing_status = "needs_punctuation"

    # Filter by time ranges
    clean_text = _filter_by_time_ranges(clean_text, time_ranges)

    # Adjust title for time ranges
    if time_ranges:
        range_strs = []
        for start, end in time_ranges:
            range_strs.append(f"{_format_time(start)}-{_format_time(end)}")
        title = f"{title} [{', '.join(range_strs)}]"

    # Save to library
    source_dir = library_path / source_id
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "clean.md").write_text(clean_text, encoding="utf-8")

    meta = {
        "id": source_id,
        "source_type": "video",
        "url": url,
        "title": title,
        "published_at": published_at,
        "video_id": video_id,
        "channel": channel,
    }
    write_meta_yaml(source_dir, meta)

    metadata = {
        "video_id": video_id,
        "whisper_used": whisper_used,
    }
    if channel:
        metadata["channel"] = channel
    if time_ranges:
        metadata["time_ranges"] = [[s, e] for s, e in time_ranges]

    return {
        "id": source_id,
        "source_type": "video",
        "url": url,
        "title": title,
        "published_at": published_at,
        "clean_text": clean_text,
        "library_path": str(source_dir),
        "processing_status": processing_status,
        "metadata": metadata,
    }


def _format_time(seconds: int) -> str:
    """Format seconds as H:MM:SS or MM:SS."""
    h, remainder = divmod(seconds, 3600)
    m, s = divmod(remainder, 60)
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"
