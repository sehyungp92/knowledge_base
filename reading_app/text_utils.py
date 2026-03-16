"""Intelligent text truncation and context budgeting for LLM prompts.

Provides word-boundary truncation, sentence-boundary truncation, and
priority-based context budgeting that replaces naive [:N] character slicing.
"""

from __future__ import annotations


def truncate(text: str, limit: int, ellipsis: str = "...") -> str:
    """Truncate text at the last word boundary within *limit* chars.

    Use for short fields (titles, labels, brief descriptions) where
    sentence structure doesn't matter.
    """
    if len(text) <= limit:
        return text
    # Reserve space for ellipsis
    cut = limit - len(ellipsis)
    if cut <= 0:
        return text[:limit]
    last_space = text.rfind(" ", 0, cut + 1)
    if last_space > cut // 2:
        return text[:last_space] + ellipsis
    return text[:cut] + ellipsis


def truncate_sentences(text: str, limit: int, ellipsis: str = "...") -> str:
    """Truncate text at the last sentence boundary within *limit* chars.

    Finds the last `.`, `!`, or `?` that is followed by whitespace or end-of-string,
    skipping common abbreviations (e.g., Dr., vs., etc.). Falls back to word-boundary
    truncation if no sentence boundary is found in the trailing portion.

    Use for multi-sentence text (claims, summaries, implications) where
    preserving complete sentences matters.
    """
    if len(text) <= limit:
        return text

    # Look for the last sentence-ending punctuation within limit
    search_start = max(0, limit - 200)
    candidate = text[:limit]

    # Common abbreviations to skip (lowercase check)
    _ABBREVS = {"dr.", "mr.", "mrs.", "ms.", "vs.", "etc.", "e.g.", "i.e.",
                "prof.", "sr.", "jr.", "inc.", "ltd.", "fig.", "eq.", "approx."}

    best = -1
    for i in range(len(candidate) - 1, search_start - 1, -1):
        if candidate[i] in ".!?":
            # Check it's followed by whitespace or is the last char
            if i + 1 >= len(candidate) or candidate[i + 1] in " \n\t\r":
                # Check it's not an abbreviation
                # Find the start of the word containing this period
                word_start = candidate.rfind(" ", max(0, i - 10), i)
                word = candidate[word_start + 1:i + 1].lower().strip() if word_start >= 0 else candidate[:i + 1].lower().strip()
                if word not in _ABBREVS:
                    best = i + 1
                    break

    if best > search_start:
        result = text[:best].rstrip()
        if ellipsis and best < len(text):
            # Avoid "sentence...." (4 dots) — use 3 dots total
            if result and result[-1] == ".":
                result += ".."
            else:
                result += ellipsis
        return result

    # Fall back to word boundary
    return truncate(text, limit, ellipsis=ellipsis)


def budget_context(
    sections: list[tuple[int, str, str]],
    total_limit: int,
) -> str:
    """Allocate a character budget across labelled sections by priority.

    Args:
        sections: List of ``(priority, label, text)`` tuples.
                  Higher priority number = more important (10 is top).
        total_limit: Total character budget for the combined output.

    Returns:
        Concatenated text within budget, with section headers.

    Algorithm:
        1. If everything fits, return it all.
        2. Allocate minimum budgets proportional to priority.
        3. Fill top-down: highest-priority sections get their full text first,
           remainder flows to lower-priority sections.
        4. Apply ``truncate_sentences`` to any section exceeding its allocation.
    """
    if not sections:
        return ""

    # Filter out empty sections
    sections = [(p, label, text) for p, label, text in sections if text and text.strip()]
    if not sections:
        return ""

    # Sort by priority descending (highest first)
    sections = sorted(sections, key=lambda s: s[0], reverse=True)

    # Calculate total size including labels
    def _section_size(label: str, text: str) -> int:
        # "## Label\ntext\n\n"
        return len(f"## {label}\n{text}\n\n")

    total_needed = sum(_section_size(label, text) for _, label, text in sections)
    if total_needed <= total_limit:
        # Everything fits
        parts = []
        for _, label, text in sections:
            parts.append(f"## {label}\n{text}")
        return "\n\n".join(parts)

    # Budget allocation
    total_priority = sum(p for p, _, _ in sections)
    if total_priority == 0:
        total_priority = len(sections)

    # First pass: allocate minimum budgets proportional to priority
    # Each section gets at least (priority / total_priority) * total_limit
    label_overhead = sum(len(f"## {label}\n\n") for _, label, _ in sections)
    available = total_limit - label_overhead

    allocations: list[int] = []
    for priority, _, text in sections:
        share = int((priority / total_priority) * available)
        allocations.append(share)

    # Second pass: top-down fill
    # High-priority sections that need less than their share donate to others
    surplus = 0
    needs_more: list[int] = []
    for i, (_, _, text) in enumerate(sections):
        text_len = len(text)
        if text_len <= allocations[i]:
            # This section fits — donate surplus
            surplus += allocations[i] - text_len
            allocations[i] = text_len
        else:
            needs_more.append(i)

    # Distribute surplus to sections that need more (in priority order — they're already sorted)
    for i in needs_more:
        if surplus <= 0:
            break
        _, _, text = sections[i]
        deficit = len(text) - allocations[i]
        give = min(surplus, deficit)
        allocations[i] += give
        surplus -= give

    # Build output with truncation
    parts = []
    for i, (_, label, text) in enumerate(sections):
        budget = allocations[i]
        if len(text) > budget:
            text = truncate_sentences(text, budget)
        parts.append(f"## {label}\n{text}")

    return "\n\n".join(parts)
