"""Chunked parallel extraction for very long text.

When source text exceeds 2x the LLM budget (~400k chars), splitting into
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

# Defaults — aligned with section_slicer._SOURCE_TYPE_BUDGETS default
DEFAULT_CHUNK_SIZE = 200_000

# ---------------------------------------------------------------------------
# Cross-chunk context injection (P2)
# ---------------------------------------------------------------------------


def _compute_document_overview(text: str) -> str:
    """Compute the document overview body (section outline or topic markers).

    Returns the overview body WITHOUT the per-chunk header.  Call once per
    document, then use ``_build_chunk_context()`` to prepend the header for
    each chunk.  This avoids re-running ``_detect_sections()`` per chunk.
    """
    from ingest.section_slicer import _detect_sections

    sections = _detect_sections(text)

    if len(sections) >= 2:
        outline_parts = ["Document structure:"]
        for sec in sections:
            title = sec["title"]
            size = len(sec["text"])
            first_sent = _first_sentence(sec["text"])
            outline_parts.append(f"- {title} (~{size:,} chars): {first_sent}")
        return "\n".join(outline_parts)

    markers = _extract_topic_markers(text, n=5)
    if not markers:
        return ""
    parts = ["Document topic markers (evenly spaced):"]
    for pct, sentence in markers:
        parts.append(f"- [{pct}%] {sentence}")
    return "\n".join(parts)


def _build_chunk_context(
    chunk_idx: int, total_chunks: int, overview: str,
) -> str:
    """Build per-chunk context by combining chunk header with precomputed overview."""
    header = f"[Document context: Chunk {chunk_idx + 1} of {total_chunks}]"
    if not overview:
        return header
    return f"{header}\n\n{overview}"


def _first_sentence(text: str) -> str:
    """Extract the first non-empty sentence from text, truncated to 200 chars."""
    text = text.strip()
    if not text:
        return ""
    # Try to find sentence boundary
    match = re.match(r"(.+?[.!?])\s", text[:500])
    if match:
        sent = match.group(1).strip()
    else:
        # No sentence boundary found, take first 200 chars
        sent = text[:200]
    return sent[:200]


def _extract_topic_markers(text: str, n: int = 5) -> list[tuple[int, str]]:
    """Extract n evenly-spaced 'topic marker' sentences from text.

    Takes the first sentence of the paragraph nearest to each percentage
    position (0%, 25%, 50%, 75%, 100%).
    """
    paragraphs = re.split(r"\n\s*\n", text)
    non_empty = [(i, p.strip()) for i, p in enumerate(paragraphs) if p.strip()]
    if not non_empty:
        return []

    total = len(non_empty)
    markers = []
    positions = [0, 25, 50, 75, 100] if n >= 5 else [0, 50, 100]

    for pct in positions[:n]:
        idx = min(int(pct / 100 * (total - 1)), total - 1)
        _, para = non_empty[idx]
        sent = _first_sentence(para)
        if sent:
            markers.append((pct, sent))

    return markers


DEFAULT_OVERLAP = 2_000
EVIDENCE_SIMILARITY_THRESHOLD = 0.75


def _truncate_at_sentence(text: str, max_chars: int) -> str:
    """Truncate text at the last sentence boundary within max_chars."""
    return _truncate_sentences(text, max_chars, ellipsis="")


def _split_by_sections(text: str, budget: int) -> list[str] | None:
    """Split text at section boundaries, grouping consecutive sections into chunks.

    Returns None if the text has fewer than 2 detected sections (caller should
    fall back to character-based splitting).

    Sections are grouped greedily: consecutive sections are accumulated until
    adding the next would exceed the budget. Overlap is achieved by repeating
    the last paragraph of each group as the first content of the next.
    """
    from ingest.section_slicer import _detect_sections

    sections = _detect_sections(text)
    if len(sections) < 2:
        return None

    chunks: list[str] = []
    current_parts: list[str] = []
    current_len = 0

    for sec in sections:
        sec_text = sec["text"]
        sec_len = len(sec_text)

        # Oversized section: flush current group, then split at sentence boundaries
        if sec_len > budget:
            if current_parts:
                chunks.append("\n\n".join(current_parts))
                current_parts = []
                current_len = 0
            sub_start = 0
            while sub_start < sec_len:
                sub_end = sub_start + budget
                if sub_end >= sec_len:
                    sub_chunk = sec_text[sub_start:]
                else:
                    sub_chunk = _truncate_at_sentence(sec_text[sub_start:sub_end], budget)
                sub_chunk = sub_chunk.strip()
                if sub_chunk:
                    chunks.append(sub_chunk)
                advance = len(sub_chunk) if sub_chunk else budget
                sub_start += advance
                while sub_start < sec_len and sec_text[sub_start] in " \t\n\r":
                    sub_start += 1
            continue

        if current_len + sec_len + 2 > budget and current_parts:
            # Adding this section would exceed budget — flush current group
            group_text = "\n\n".join(current_parts)
            chunks.append(group_text)

            # Semantic overlap: last paragraph of previous group
            last_part = current_parts[-1]
            paragraphs = last_part.rsplit("\n\n", 1)
            overlap_text = paragraphs[-1] if len(paragraphs) > 1 else ""

            current_parts = []
            current_len = 0
            if overlap_text:
                current_parts.append(overlap_text)
                current_len = len(overlap_text) + 2

        current_parts.append(sec_text)
        current_len += sec_len + 2

    if current_parts:
        chunks.append("\n\n".join(current_parts))

    return chunks if len(chunks) > 1 else [text]


def split_with_overlap(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> list[str]:
    """Split text into overlapping chunks.

    Tries section-aware splitting first (preserves semantic boundaries for
    structured documents). Falls back to character-based sentence-boundary
    splitting for unstructured text or when section detection fails.
    """
    if len(text) <= chunk_size:
        return [text]

    # Try section-aware splitting first (P4)
    section_chunks = _split_by_sections(text, chunk_size)
    if section_chunks is not None:
        logger.info(
            "Section-aware splitting: %d chunks from %d chars",
            len(section_chunks), len(text),
        )
        return section_chunks

    # Fallback: character-based splitting at sentence boundaries
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


# ---------------------------------------------------------------------------
# Boundary cross-validation (P5)
# ---------------------------------------------------------------------------

BOUNDARY_REGION_SIZE = 5_000  # chars from each side of boundary to check
BOUNDARY_REEXTRACT_SIZE = 10_000  # chars from each side for re-extraction


def _find_boundary_claims(
    claims: list[dict],
    chunks: list[str],
) -> list[tuple[int, list[dict]]]:
    """Identify chunk boundaries that have claims with evidence in the overlap region.

    Returns list of (boundary_index, claims_in_boundary) tuples.
    boundary_index i means the boundary between chunk i and chunk i+1.
    """
    # Build a map of where each chunk's boundary regions are in terms of content
    boundaries_with_claims: list[tuple[int, list[dict]]] = []

    for i in range(len(chunks) - 1):
        # The overlap region: tail of chunk i and head of chunk i+1
        tail_lower = chunks[i][-BOUNDARY_REGION_SIZE:].lower()
        head_lower = chunks[i + 1][:BOUNDARY_REGION_SIZE].lower()

        boundary_claims = []
        for claim in claims:
            snippet = claim.get("evidence_snippet", "")
            if not snippet:
                continue
            # Check if evidence falls in either boundary region
            snippet_lower = snippet.lower()
            if snippet_lower in tail_lower or snippet_lower in head_lower:
                boundary_claims.append(claim)

        if boundary_claims:
            boundaries_with_claims.append((i, boundary_claims))

    return boundaries_with_claims


def _cross_validate_boundary_claims(
    claims: list[dict],
    chunks: list[str],
    full_text: str,
    source_id: str,
    source_type: str,
    executor,
    budget: int,
    themes: list[dict] | None,
) -> list[dict]:
    """Re-extract claims at chunk boundaries with wider context.

    For each boundary with claims, constructs a targeted re-extraction prompt
    with ~20K chars spanning the boundary. Improved claims (higher confidence)
    replace the originals.
    """
    from ingest.extractor import extract_claims, _validate_evidence

    boundary_info = _find_boundary_claims(claims, chunks)
    if not boundary_info:
        return claims

    logger.info(
        "Boundary cross-validation for %s: %d boundaries with claims",
        source_id, len(boundary_info),
    )

    # Build boundary regions for re-extraction
    def _reextract_boundary(boundary_idx: int):
        tail = chunks[boundary_idx][-BOUNDARY_REEXTRACT_SIZE:]
        head = chunks[boundary_idx + 1][:BOUNDARY_REEXTRACT_SIZE]
        boundary_text = f"{tail}\n\n[...chunk boundary...]\n\n{head}"
        return extract_claims(
            source_id, boundary_text, source_type, executor,
            library_path=None,
            budget=budget,
            themes=themes,
        )

    # Run boundary re-extractions in parallel
    improved_claims: list[dict] = []
    with ThreadPoolExecutor(max_workers=min(len(boundary_info), 4)) as pool:
        futures = {
            pool.submit(_reextract_boundary, b_idx): (b_idx, b_claims)
            for b_idx, b_claims in boundary_info
        }
        for future in as_completed(futures):
            b_idx, original_boundary_claims = futures[future]
            try:
                result = future.result()
                new_claims = result.get("claims", [])
                # Validate against full text
                for claim in new_claims:
                    snippet = claim.get("evidence_snippet", "")
                    if snippet and _validate_evidence(snippet, full_text):
                        improved_claims.append(claim)
            except Exception:
                logger.warning(
                    "Boundary %d re-extraction failed for %s",
                    b_idx, source_id, exc_info=True,
                )

    if not improved_claims:
        return claims

    # Merge: for each improved claim, replace original if confidence is higher
    result_claims = list(claims)
    for new_claim in improved_claims:
        new_snippet = new_claim.get("evidence_snippet", "")
        replaced = False
        for i, existing in enumerate(result_claims):
            if _evidence_similar(new_snippet, existing.get("evidence_snippet", "")):
                if new_claim.get("confidence", 0) > existing.get("confidence", 0):
                    result_claims[i] = new_claim
                replaced = True
                break
        if not replaced:
            # Genuinely new claim from boundary context
            result_claims.append(new_claim)

    logger.info(
        "Boundary cross-validation for %s: %d improved claims merged",
        source_id, len(improved_claims),
    )
    return _deduplicate_claims(result_claims)


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
    from ingest.extractor import extract_claims

    chunks = split_with_overlap(clean_text, chunk_size=budget)
    total_chunks = len(chunks)
    logger.info(
        "Chunked claim extraction for %s: %d chunks from %d chars",
        source_id, total_chunks, len(clean_text),
    )

    # Build document overview once for all chunks (P2)
    overview = _compute_document_overview(clean_text) if total_chunks > 1 else ""

    all_claims: list[dict] = []
    all_concepts: list[dict] = []

    def _extract_with_context(chunk: str, idx: int):
        """Wrap chunk with document context before extraction."""
        if overview:
            ctx = _build_chunk_context(idx, total_chunks, overview)
            contextualized = (
                f"{ctx}\n\n"
                "If a claim references content not in this chunk (visible in the document overview), "
                "note the cross-reference but only extract evidence from the current chunk text.\n\n"
                "---\n\n"
                f"{chunk}"
            )
        else:
            contextualized = chunk
        return extract_claims(
            source_id, contextualized, source_type, executor,
            library_path=None,
            budget=budget,
            themes=themes,
        )

    with ThreadPoolExecutor(max_workers=min(total_chunks, 4)) as pool:
        futures = {
            pool.submit(_extract_with_context, chunk, i): i
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
    from ingest.extractor import validate_claims_evidence
    validated_claims = validate_claims_evidence(all_claims, clean_text, source_id)

    # Deduplicate
    deduped_claims = _deduplicate_claims(validated_claims)

    # Boundary cross-validation (P5): re-extract claims near chunk boundaries
    # with wider context to catch split-evidence issues
    if total_chunks > 1:
        deduped_claims = _cross_validate_boundary_claims(
            deduped_claims, chunks, clean_text, source_id, source_type,
            executor, budget, themes,
        )

    merged = {
        "claims": deduped_claims,
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

    # Build document overview once for context injection (P2)
    overview = _compute_document_overview(clean_text) if len(chunks) > 1 else ""

    def _contextualize_chunk(chunk: str, idx: int) -> str:
        if not overview:
            return chunk
        ctx = _build_chunk_context(idx, len(chunks), overview)
        return (
            f"{ctx}\n\n"
            "Note: The above is document context for orientation. "
            "Summarize only the content below.\n\n"
            "---\n\n"
            f"{chunk}"
        )

    # Phase 1: generate per-chunk summaries in parallel
    chunk_summaries: list[tuple[int, str]] = []

    with ThreadPoolExecutor(max_workers=min(len(chunks), 4)) as pool:
        futures = {
            pool.submit(
                generate_deep_summary,
                source_id, _contextualize_chunk(chunk, i), title, source_type,
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
    total_chunks = len(chunks)
    logger.info(
        "Chunked landscape extraction for %s: %d chunks from %d chars",
        source_id, total_chunks, len(clean_text),
    )

    chunk_signals: list[dict] = []

    # Build document overview once for all chunks (P2)
    overview = _compute_document_overview(clean_text) if total_chunks > 1 else ""

    def _landscape_with_context(chunk: str, idx: int):
        """Wrap chunk with document context before landscape extraction."""
        if overview:
            ctx = _build_chunk_context(idx, total_chunks, overview)
            contextualized = f"{ctx}\n\n---\n\n{chunk}"
        else:
            contextualized = chunk
        return extract_landscape_signals(
            contextualized, source_id,
            source_themes=source_themes,
            published_at=published_at,
            executor=executor,
        )

    with ThreadPoolExecutor(max_workers=min(total_chunks, 4)) as pool:
        futures = {
            pool.submit(_landscape_with_context, chunk, i): i
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
