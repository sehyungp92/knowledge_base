"""Chunked parallel extraction for very long text.

When source text exceeds 2x the LLM budget (~160k chars), splitting into
overlapping chunks and extracting in parallel produces better coverage than
even-coverage sampling alone.

Each chunk is processed by the same extractor, then results are merged
with deduplication.
"""

from __future__ import annotations

import json
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import SequenceMatcher
from pathlib import Path

from reading_app.text_utils import truncate_sentences as _truncate_sentences

logger = logging.getLogger(__name__)

# Defaults
DEFAULT_CHUNK_SIZE = 80_000
DEFAULT_OVERLAP = 2_000
EVIDENCE_SIMILARITY_THRESHOLD = 0.75


def _truncate_at_sentence(text: str, max_chars: int) -> str:
    """Truncate text at the last sentence boundary within max_chars."""
    return _truncate_sentences(text, max_chars, ellipsis="")


def split_with_overlap(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> list[str]:
    """Split text into overlapping chunks, breaking at sentence boundaries."""
    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunk = text[start:]
        else:
            chunk = _truncate_at_sentence(text[start:end], chunk_size)
        chunk = chunk.strip()
        if chunk:
            chunks.append(chunk)
        advance = len(chunk) - overlap if chunk else chunk_size
        if advance <= 0:
            advance = chunk_size  # safety: always advance
        start += advance

    return chunks


def _evidence_similar(a: str, b: str) -> bool:
    """Check if two evidence snippets are similar enough to be duplicates."""
    if not a or not b:
        return False
    a_lower = " ".join(a.lower().split())
    b_lower = " ".join(b.lower().split())
    if a_lower == b_lower:
        return True
    # Use SequenceMatcher for fuzzy comparison
    ratio = SequenceMatcher(None, a_lower, b_lower).ratio()
    return ratio >= EVIDENCE_SIMILARITY_THRESHOLD


def _deduplicate_claims(all_claims: list[dict]) -> list[dict]:
    """Deduplicate claims by evidence snippet similarity."""
    unique: list[dict] = []
    for claim in all_claims:
        snippet = claim.get("evidence_snippet", "")
        is_dup = False
        for existing in unique:
            if _evidence_similar(snippet, existing.get("evidence_snippet", "")):
                is_dup = True
                # Keep the one with higher confidence
                if claim.get("confidence", 0) > existing.get("confidence", 0):
                    unique[unique.index(existing)] = claim
                break
        if not is_dup:
            unique.append(claim)
    return unique


def _deduplicate_concepts(all_concepts: list[dict]) -> list[dict]:
    """Deduplicate concepts by canonical name."""
    seen: dict[str, dict] = {}
    for concept in all_concepts:
        key = concept.get("canonical_name", "").lower().strip()
        if key not in seen:
            seen[key] = concept
        else:
            # Merge aliases
            existing = seen[key]
            existing_aliases = set(existing.get("aliases", []))
            new_aliases = set(concept.get("aliases", []))
            existing["aliases"] = list(existing_aliases | new_aliases)
    return list(seen.values())


def chunked_extract_claims(
    source_id: str,
    clean_text: str,
    source_type: str,
    executor,
    library_path: Path | None = None,
    budget: int = DEFAULT_CHUNK_SIZE,
    themes: list[dict] | None = None,
) -> dict:
    """Extract claims from each chunk in parallel, merge results.

    Delegates to extract_claims for each chunk, then deduplicates.
    Evidence snippets are validated against the full clean_text.
    """
    from ingest.extractor import extract_claims, _validate_evidence

    chunks = split_with_overlap(clean_text, chunk_size=budget)
    logger.info(
        "Chunked claim extraction for %s: %d chunks from %d chars",
        source_id, len(chunks), len(clean_text),
    )

    all_claims: list[dict] = []
    all_concepts: list[dict] = []

    with ThreadPoolExecutor(max_workers=min(len(chunks), 4)) as pool:
        futures = {
            pool.submit(
                extract_claims, source_id, chunk, source_type, executor,
                library_path=None,  # don't save per-chunk
                budget=budget,
                themes=themes,
            ): i
            for i, chunk in enumerate(chunks)
        }
        for future in as_completed(futures):
            chunk_idx = futures[future]
            try:
                result = future.result()
                all_claims.extend(result.get("claims", []))
                all_concepts.extend(result.get("concepts", []))
            except Exception:
                logger.warning(
                    "Chunk %d failed for %s", chunk_idx, source_id, exc_info=True,
                )

    # Re-validate evidence against full text (chunk extraction validated against chunk only)
    validated_claims = []
    for claim in all_claims:
        snippet = claim.get("evidence_snippet", "")
        if snippet and _validate_evidence(snippet, clean_text):
            validated_claims.append(claim)

    # Deduplicate
    merged = {
        "claims": _deduplicate_claims(validated_claims),
        "concepts": _deduplicate_concepts(all_concepts),
    }

    # Save merged result to library
    if library_path:
        extractions_path = library_path / source_id / "extractions.json"
        if extractions_path.parent.exists():
            extractions_path.write_text(
                json.dumps(merged, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    logger.info(
        "Chunked extraction merged for %s: %d claims, %d concepts",
        source_id, len(merged["claims"]), len(merged["concepts"]),
    )
    return merged


def chunked_deep_summary(
    source_id: str,
    clean_text: str,
    title: str,
    source_type: str,
    url: str | None = None,
    authors: list[str] | None = None,
    published_at: str | None = None,
    executor=None,
    library_path: Path | None = None,
    budget: int = DEFAULT_CHUNK_SIZE,
    themes: list[dict] | None = None,
    show_name: str | None = None,
) -> str:
    """Generate deep summary from chunks: per-chunk summaries then a merge pass.

    Unlike claims, summaries can't be concatenated — the final merge call
    synthesizes per-chunk summaries into one coherent document.
    Uses paper-specific or general template via shared prompt builders.
    """
    from ingest.deep_summarizer import generate_deep_summary, build_merge_prompt

    chunks = split_with_overlap(clean_text, chunk_size=budget)
    logger.info(
        "Chunked deep summary for %s: %d chunks from %d chars",
        source_id, len(chunks), len(clean_text),
    )

    # Phase 1: generate per-chunk summaries in parallel
    chunk_summaries: list[tuple[int, str]] = []

    with ThreadPoolExecutor(max_workers=min(len(chunks), 4)) as pool:
        futures = {
            pool.submit(
                generate_deep_summary,
                source_id, chunk, title, source_type,
                url=url, authors=authors, published_at=published_at,
                executor=executor,
                library_path=None,  # don't save per-chunk
                budget=budget,
                themes=themes, show_name=show_name,
            ): i
            for i, chunk in enumerate(chunks)
        }
        for future in as_completed(futures):
            chunk_idx = futures[future]
            try:
                summary = future.result()
                chunk_summaries.append((chunk_idx, summary))
            except Exception:
                logger.warning(
                    "Chunk %d summary failed for %s", chunk_idx, source_id, exc_info=True,
                )

    if not chunk_summaries:
        return f"# {title}\n\nSummary generation failed."

    # Sort by chunk order
    chunk_summaries.sort(key=lambda x: x[0])

    if len(chunk_summaries) == 1:
        final_summary = chunk_summaries[0][1]
    else:
        # Phase 2: merge summaries into one coherent document
        merge_prompt = build_merge_prompt(
            chunk_summaries, title, source_type,
            url=url, authors=authors, published_at=published_at,
            show_name=show_name,
        )

        if executor is None:
            final_summary = chunk_summaries[0][1]
        else:
            result = executor.run_raw(
                merge_prompt,
                session_id=f"summary_merge_{source_id}",
            )
            final_summary = result.text.strip() if result.text else chunk_summaries[0][1]

    # Save final result to library
    if library_path:
        summary_path = library_path / source_id / "deep_summary.md"
        if summary_path.parent.exists():
            summary_path.write_text(final_summary, encoding="utf-8")

    return final_summary


def _deduplicate_signals(signals_list: list[dict]) -> dict:
    """Merge multiple landscape signal dicts, deduplicating by evidence similarity."""
    merged = {
        "capabilities": [],
        "limitations": [],
        "bottlenecks": [],
        "breakthroughs": [],
    }

    for signals in signals_list:
        for key in merged:
            for item in signals.get(key, []):
                snippet = item.get("evidence_snippet", "")
                is_dup = False
                for existing in merged[key]:
                    if _evidence_similar(snippet, existing.get("evidence_snippet", "")):
                        # Keep higher confidence version
                        if item.get("confidence", 0) > existing.get("confidence", 0):
                            merged[key][merged[key].index(existing)] = item
                        is_dup = True
                        break
                if not is_dup:
                    merged[key].append(item)

    return merged


def chunked_landscape_signals(
    clean_text: str,
    source_id: str,
    source_themes: list[str] | None = None,
    published_at: str | None = None,
    executor=None,
    budget: int = DEFAULT_CHUNK_SIZE,
) -> dict:
    """Extract landscape signals from each chunk in parallel, merge results."""
    from ingest.landscape_extractor import extract_landscape_signals

    chunks = split_with_overlap(clean_text, chunk_size=budget)
    logger.info(
        "Chunked landscape extraction for %s: %d chunks from %d chars",
        source_id, len(chunks), len(clean_text),
    )

    chunk_signals: list[dict] = []

    with ThreadPoolExecutor(max_workers=min(len(chunks), 4)) as pool:
        futures = {
            pool.submit(
                extract_landscape_signals,
                chunk, source_id,
                source_themes=source_themes,
                published_at=published_at,
                executor=executor,
            ): i
            for i, chunk in enumerate(chunks)
        }
        for future in as_completed(futures):
            chunk_idx = futures[future]
            try:
                signals = future.result()
                chunk_signals.append(signals)
            except Exception:
                logger.warning(
                    "Chunk %d landscape extraction failed for %s",
                    chunk_idx, source_id, exc_info=True,
                )

    if not chunk_signals:
        return {"capabilities": [], "limitations": [], "bottlenecks": [], "breakthroughs": []}

    merged = _deduplicate_signals(chunk_signals)
    logger.info(
        "Chunked landscape merged for %s: %d cap, %d lim, %d bn, %d bt",
        source_id,
        len(merged["capabilities"]),
        len(merged["limitations"]),
        len(merged["bottlenecks"]),
        len(merged["breakthroughs"]),
    )
    return merged
