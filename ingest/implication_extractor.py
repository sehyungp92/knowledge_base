"""Cross-theme implication extraction and persistence."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

from agents.base import BaseAgent
from ingest.json_parser import parse_json_from_llm
from ingest.theme_validator import load_valid_theme_ids

logger = logging.getLogger(__name__)

IMPLICATION_PROMPT = """Analyze the following source text and identify cross-theme implications.

A cross-theme implication is when progress in one AI research area affects another area.
For example, a breakthrough in scaling might imply changes for alignment research.

**Source publication date: {published_at}**
Consider whether implications are emerging (newly demonstrated), established (well-known by publication date), or historical.

{theme_block}

Source themes: {source_themes}

IMPORTANT: Use ONLY theme IDs from the list above. Do NOT invent theme IDs.

Return JSON array (max {cap} implications, only confidence >= 0.4):
[{{
  "source_theme_id": "...",
  "target_theme_id": "...",
  "trigger_type": "breakthrough|bottleneck_resolved|capability_matured",
  "trigger_id": "...",
  "implication": "...",
  "confidence": 0.0-1.0,
  "evidence_sources": [{{"source_id": "...", "snippet": "..."}}]
}}]

SOURCE TEXT (truncated):
{text}
"""

# Fallback theme block if DB is unavailable
_FALLBACK_THEME_BLOCK = "Available themes: (use only theme IDs from the source_themes list)"


def _get_theme_block(get_conn_fn=None) -> str:
    """Get formatted theme list from DB, falling back to static block."""
    try:
        from ingest.theme_classifier import get_available_themes
        block = get_available_themes(get_conn_fn)
        if block:
            return f"Available themes (use ONLY these IDs):\n{block}"
    except Exception:
        pass
    return _FALLBACK_THEME_BLOCK


def extract_cross_theme_implications(
    clean_text: str,
    source_id: str,
    source_themes: list[str],
    published_at: str | None = None,
    executor=None,
    get_conn_fn=None,
) -> list[dict]:
    """Extract cross-theme implications from source text.

    Uses adaptive cap: min(4 + (n_themes - 1) * 2, 12)
    """
    n_themes = len(source_themes)
    cap = min(4 + max(0, n_themes - 1) * 2, 12)

    if executor is None:
        from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
        executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    # Resolve published_at if not provided
    if not published_at:
        try:
            from reading_app.db import get_source
            source = get_source(source_id)
            if source and source.get("published_at"):
                published_at = str(source["published_at"])[:10]
        except Exception:
            pass

    prompt = IMPLICATION_PROMPT.format(
        theme_block=_get_theme_block(get_conn_fn),
        source_themes=", ".join(source_themes),
        cap=cap,
        text=clean_text[:8000],
        published_at=published_at or "unknown",
    )

    result = executor.run_raw(
        prompt,
        session_id=f"implications_{source_id}",
        timeout=180,
    )

    implications = _parse_implications(result.text)

    # Filter by confidence
    implications = [imp for imp in implications if imp.get("confidence", 0) >= 0.4]

    return implications[:cap]


def persist_cross_theme_implications(
    implications: list[dict],
    source_id: str,
    get_conn_fn=None,
):
    """Persist implications to database with dedup via trigram similarity.

    For each implication, checks if a similar one already exists for the same
    (source_theme, target_theme) pair. If similarity >= 0.7, merges evidence
    and averages confidence. Otherwise inserts new.
    """
    if not get_conn_fn or not implications:
        return

    try:
        from reading_app.db import find_similar_implication, merge_implication
    except ImportError:
        find_similar_implication = None
        merge_implication = None

    try:
        from ulid import ULID
        valid_ids = load_valid_theme_ids(get_conn_fn)
        with get_conn_fn() as conn:
            persisted = 0
            merged = 0
            for imp in implications:
                src_id = imp.get("source_theme_id", "")
                tgt_id = imp.get("target_theme_id", "")
                if valid_ids is not None and (src_id not in valid_ids or tgt_id not in valid_ids):
                    logger.warning("Skipping implication with invalid theme ID: %s -> %s", src_id, tgt_id)
                    continue

                evidence = imp.get("evidence_sources", [])
                if source_id and not any(e.get("source_id") == source_id for e in evidence):
                    evidence.append({"source_id": source_id})
                confidence = imp.get("confidence", 0.5)

                # Dedup: check for similar existing implication on same theme pair
                existing = None
                if find_similar_implication:
                    try:
                        existing = find_similar_implication(src_id, tgt_id, imp["implication"])
                    except Exception:
                        logger.debug("Similarity search failed, inserting new", exc_info=True)

                if existing and merge_implication:
                    merge_implication(existing["id"], evidence, confidence)
                    merged += 1
                    logger.debug(
                        "Merged implication into %s (sim=%.2f): %s",
                        existing["id"], existing.get("sim", 0), imp["implication"][:80],
                    )
                else:
                    impl_id = f"impl_{ULID()}"
                    conn.execute(
                        """INSERT INTO cross_theme_implications
                           (id, source_theme_id, target_theme_id, trigger_type, trigger_id,
                            implication, confidence, evidence_sources)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                        (impl_id, src_id, tgt_id,
                         imp.get("trigger_type", "capability_matured"),
                         imp.get("trigger_id", ""),
                         imp["implication"],
                         confidence,
                         json.dumps(evidence)),
                    )
                    persisted += 1
            conn.commit()
            logger.info(
                "Implications for %s: %d new, %d merged (of %d total)",
                source_id, persisted, merged, len(implications),
            )
    except Exception:
        logger.error("Failed to persist implications", exc_info=True)


def _parse_implications(text: str) -> list[dict]:
    result = parse_json_from_llm(text, expect=list)
    return result if result is not None else []
