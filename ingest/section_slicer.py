"""Section-aware text budgeting for LLM extractors.

Implements prioritized_slice() which selects sections by priority,
restores document order, and truncates at sentence boundaries.

For unstructured text (transcripts, articles without headings),
uses even-coverage sampling instead of head-truncation to preserve
signal from all parts of the document.
"""

from __future__ import annotations

import re

from reading_app.text_utils import truncate_sentences as _truncate_sentences

# ---------------------------------------------------------------------------
# Source-type-aware budgets and dynamic timeouts
# ---------------------------------------------------------------------------

_SOURCE_TYPE_BUDGETS = {
    "paper": 80_000,
    "arxiv": 80_000,
    "article": 70_000,
    "video": 50_000,
    "podcast": 50_000,
}


def budget_for_source_type(source_type: str | None, default: int = 80_000) -> int:
    """Return an appropriate character budget for the given source type."""
    if source_type is None:
        return default
    return _SOURCE_TYPE_BUDGETS.get(source_type, default)


def timeout_for_text(
    text_len: int,
    base: int = 270,
    per_10k: int = 30,
    ceiling: int = 480,
) -> int:
    """Dynamic timeout: 270s base + 30s per 10K chars, clamped to ceiling.

    Examples: 50K → 420s, 80K → 480s, 10K → 300s.
    """
    return min(base + (text_len // 10_000) * per_10k, ceiling)


SECTION_PRIORITIES = {
    "abstract": 1,
    "introduction": 2,
    "results": 3,
    "findings": 3,
    "discussion": 4,
    "methods": 5,
    "methodology": 5,
    "related work": 6,
    "background": 6,
    "conclusion": 7,
    "conclusions": 7,
    "appendix": 8,
    "references": 8,
    "acknowledgements": 8,
    "acknowledgments": 8,
}

BACKMATTER_PATTERNS = [
    r"^\s*references?\s*$",
    r"^\s*bibliography\s*$",
    r"^\s*acknowledgements?\s*$",
    r"^\s*acknowledgments?\s*$",
    r"^\s*appendix\s+[a-z]\s*[:.]",
    r"^\s*supplementary\s+materials?\s*$",
]


def _detect_sections(text: str) -> list[dict]:
    """Split text into sections based on markdown/academic headings."""
    lines = text.split("\n")
    sections = []
    current_title = "preamble"
    current_lines = []
    current_start = 0

    for i, line in enumerate(lines):
        heading_match = re.match(r"^#{1,3}\s+(.+)$", line.strip())
        if not heading_match:
            heading_match = re.match(r"^(?:\d+\.?\s+)?([A-Z][A-Z\s]{2,})$", line.strip())

        if heading_match and current_lines:
            sections.append({
                "title": current_title,
                "text": "\n".join(current_lines),
                "start": current_start,
                "order": len(sections),
            })
            current_title = heading_match.group(1).strip().lower()
            current_lines = []
            current_start = i
        else:
            current_lines.append(line)

    if current_lines:
        sections.append({
            "title": current_title,
            "text": "\n".join(current_lines),
            "start": current_start,
            "order": len(sections),
        })

    return sections


def _priority_for(title: str) -> int:
    """Return priority (1-8) for a section title, 5 as default."""
    title_lower = title.lower().strip()
    for key, priority in SECTION_PRIORITIES.items():
        if key in title_lower:
            return priority
    return 5


def _truncate_at_sentence(text: str, max_chars: int) -> str:
    """Truncate text at the last sentence boundary within max_chars."""
    return _truncate_sentences(text, max_chars, ellipsis="")


def strip_backmatter(text: str) -> str:
    """Remove references, acknowledgements, and appendices from text."""
    lines = text.split("\n")
    cut_at = len(lines)
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Strip markdown heading markers before matching
        heading_text = re.sub(r"^#{1,6}\s+", "", stripped)
        for pattern in BACKMATTER_PATTERNS:
            if re.match(pattern, heading_text, re.IGNORECASE) or re.match(pattern, stripped, re.IGNORECASE):
                cut_at = i
                break
        if cut_at < len(lines):
            break
    return "\n".join(lines[:cut_at]).rstrip()


def _chunk_by_paragraphs(text: str, target_size: int = 4000) -> list[str]:
    """Split text into chunks by paragraph breaks, merging small paragraphs.

    Paragraphs are joined until the accumulated size reaches target_size,
    then a new chunk starts. This keeps paragraph boundaries intact.
    """
    paragraphs = re.split(r"\n\s*\n", text)
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        para_len = len(para)
        if current and current_len + para_len + 2 > target_size:
            chunks.append("\n\n".join(current))
            current = [para]
            current_len = para_len
        else:
            current.append(para)
            current_len += para_len + 2  # account for \n\n join

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def _chunk_by_size(text: str, target_size: int = 4000) -> list[str]:
    """Split text into chunks by sentence boundaries when no paragraph breaks exist.

    Used for raw transcripts and other wall-of-text content.
    """
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + target_size
        if end >= len(text):
            chunk = text[start:]
        else:
            chunk = _truncate_at_sentence(text[start:end], target_size)
        chunk = chunk.strip()
        if chunk:
            chunks.append(chunk)
        start += len(chunk) if chunk else target_size  # avoid infinite loop on unchunkable text
        # Skip whitespace between chunks
        while start < len(text) and text[start] in " \t\n\r":
            start += 1

    return chunks


def _select_even_coverage(chunks: list[str], budget: int) -> str:
    """Select evenly spaced chunks to fill budget, always including first and last.

    Returns the selected chunks joined with ``[...]`` markers between gaps.
    """
    if not chunks:
        return ""

    if len(chunks) == 1:
        return _truncate_at_sentence(chunks[0], budget)

    total = sum(len(c) for c in chunks)
    if total <= budget:
        return "\n\n".join(chunks)

    # Determine how many chunks fit in budget
    # Sort by length to estimate, but select by position
    chunk_lengths = [len(c) for c in chunks]
    avg_len = total / len(chunks)
    # Account for [...] markers (~8 chars each)
    marker_overhead = 8
    max_k = max(2, int(budget / (avg_len + marker_overhead)))
    max_k = min(max_k, len(chunks))

    # Binary search for the right number of chunks that fit
    while max_k > 2:
        indices = _even_indices(len(chunks), max_k)
        size = sum(chunk_lengths[i] for i in indices) + marker_overhead * (max_k - 1)
        if size <= budget:
            break
        max_k -= 1
    else:
        indices = _even_indices(len(chunks), 2)

    # Build result with [...] markers between non-contiguous chunks
    selected = [chunks[i] for i in indices]
    parts: list[str] = [selected[0]]
    for j in range(1, len(selected)):
        if indices[j] == indices[j - 1] + 1:
            parts.append(selected[j])
        else:
            parts.append("[...]")
            parts.append(selected[j])

    result = "\n\n".join(parts)
    # Final truncation if still slightly over (rounding)
    if len(result) > budget:
        result = _truncate_at_sentence(result, budget)
    return result


def _even_indices(n: int, k: int) -> list[int]:
    """Return k evenly spaced indices from range(n), always including 0 and n-1."""
    if k >= n:
        return list(range(n))
    if k == 1:
        return [0]
    if k == 2:
        return [0, n - 1]
    indices = [0]
    for i in range(1, k - 1):
        indices.append(round(i * (n - 1) / (k - 1)))
    indices.append(n - 1)
    # Deduplicate while preserving order (can happen with small n)
    seen = set()
    result = []
    for idx in indices:
        if idx not in seen:
            seen.add(idx)
            result.append(idx)
    return result


def prioritized_slice(
    text: str,
    budget: int = 80000,
    priorities: dict[str, int] | None = None,
) -> str:
    """Select sections by priority, restore document order, truncate at sentence boundary.

    Args:
        text: Full source text.
        budget: Maximum character budget for the output.
        priorities: Optional priority overrides merged on top of SECTION_PRIORITIES.
                    Lower numbers = higher priority (1 = most important).
    """
    # Merge caller-provided priority overrides
    effective_priorities = {**SECTION_PRIORITIES, **(priorities or {})}

    def _effective_priority(title: str) -> int:
        title_lower = title.lower().strip()
        for key, priority in effective_priorities.items():
            if key in title_lower:
                return priority
        return 5

    # Always strip backmatter first
    text = strip_backmatter(text)

    if len(text) <= budget:
        return text

    sections = _detect_sections(text)
    if not sections:
        return _truncate_at_sentence(text, budget)

    # No headings detected — use even-coverage sampling
    if len(sections) == 1:
        paragraphs = re.split(r"\n\s*\n", text)
        non_empty = [p for p in paragraphs if p.strip()]
        if len(non_empty) >= 3:
            chunks = _chunk_by_paragraphs(text)
        else:
            chunks = _chunk_by_size(text)
        return _select_even_coverage(chunks, budget)

    # Filter out backmatter (priority 8)
    non_backmatter = [s for s in sections if _effective_priority(s["title"]) < 8]
    if not non_backmatter:
        non_backmatter = sections  # Keep everything if all sections are backmatter
    prioritized = sorted(non_backmatter, key=lambda s: (_effective_priority(s["title"]), s["order"]))

    selected = []
    remaining = budget
    for section in prioritized:
        section_len = len(section["text"])
        if section_len <= remaining:
            selected.append(section)
            remaining -= section_len
        elif remaining > 500:
            section = dict(section)
            section["text"] = _truncate_at_sentence(section["text"], remaining)
            selected.append(section)
            remaining = 0
            break

    selected.sort(key=lambda s: s["order"])
    return "\n\n".join(s["text"] for s in selected)
