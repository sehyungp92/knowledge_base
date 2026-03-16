"""Tests for ingest.section_slicer."""

from ingest.section_slicer import (
    _chunk_by_paragraphs,
    _chunk_by_size,
    _even_indices,
    _select_even_coverage,
    prioritized_slice,
    strip_backmatter,
)


def test_prioritized_slice_fits():
    text = "## Abstract\nShort abstract.\n\n## Introduction\nShort intro."
    result = prioritized_slice(text, budget=10000)
    assert "Short abstract" in result
    assert "Short intro" in result


def test_prioritized_slice_priority_order():
    text = (
        "## Related Work\nLow priority content.\n\n"
        "## Abstract\nHigh priority content.\n\n"
        "## Results\nMedium priority content."
    )
    # Very small budget should prefer abstract
    result = prioritized_slice(text, budget=100)
    assert "High priority" in result


def test_prioritized_slice_drops_backmatter():
    text = (
        "## Abstract\nContent.\n\n"
        "## References\n[1] Should be dropped."
    )
    result = prioritized_slice(text, budget=10000)
    assert "[1] Should be dropped" not in result


def test_strip_backmatter():
    text = "## Introduction\nContent.\n\n## References\n[1] Ref"
    result = strip_backmatter(text)
    assert "Content" in result
    assert "[1] Ref" not in result


def test_strip_backmatter_bibliography():
    text = "Content.\n\n## Bibliography\nSome refs."
    result = strip_backmatter(text)
    assert "Some refs" not in result


def test_strip_backmatter_no_backmatter():
    text = "## Introduction\nContent.\n\n## Results\nGood."
    result = strip_backmatter(text)
    assert "Content" in result
    assert "Good" in result


def test_prioritized_slice_no_headings():
    text = "Just plain text without any markdown headings at all."
    result = prioritized_slice(text, budget=10000)
    assert "plain text" in result


def test_prioritized_slice_large_budget():
    sections = "\n\n".join(f"## Section {i}\nContent {i}." for i in range(10))
    result = prioritized_slice(sections, budget=100000)
    assert "Content 0" in result


# --- Even-coverage sampling tests ---


def test_even_coverage_transcript_no_paragraphs():
    """A long transcript with no paragraph breaks should use sentence-based chunking
    and include content from beginning, middle, and end."""
    # Build a 200k-char transcript (sentences, no paragraph breaks)
    sentences = [f"Sentence number {i} discusses topic {i % 50}." for i in range(5000)]
    text = " ".join(sentences)
    assert len(text) > 200_000

    result = prioritized_slice(text, budget=80000)
    assert len(result) <= 80000
    # Content from beginning
    assert "Sentence number 0" in result
    # Content from end (last sentence)
    assert "Sentence number 4999" in result
    # Content from middle (approximately)
    # With even sampling, some mid-range sentences should appear
    mid_found = any(f"Sentence number {i}" in result for i in range(2400, 2600))
    assert mid_found, "No content from middle of transcript found"


def test_even_coverage_article_with_paragraphs():
    """An article with paragraphs but no headings should use paragraph-based chunking."""
    paragraphs = [f"Paragraph {i}. " * 80 for i in range(200)]
    text = "\n\n".join(paragraphs)
    assert len(text) > 80_000

    result = prioritized_slice(text, budget=80000)
    assert len(result) <= 80000
    # First paragraph present
    assert "Paragraph 0" in result
    # Last paragraph present
    assert "Paragraph 199" in result


def test_even_coverage_markers():
    """Non-contiguous chunks should be joined with [...] markers."""
    paragraphs = [f"Paragraph {i}. " * 30 for i in range(50)]
    text = "\n\n".join(paragraphs)
    # Use a small budget to force gaps
    result = prioritized_slice(text, budget=5000)
    assert "[...]" in result


def test_headings_still_use_priority():
    """Text with headings should still use priority-based selection, not even-coverage."""
    text = (
        "## Abstract\nAbstract content here.\n\n"
        "## Methods\nMethods content here.\n\n"
        "## Results\nResults content here."
    )
    result = prioritized_slice(text, budget=100)
    # Should prefer abstract (priority 1) over methods (priority 5)
    assert "Abstract content" in result


def test_even_coverage_short_text():
    """Text without headings that fits in budget should be returned as-is."""
    text = "Short text without headings.\n\nSecond paragraph."
    result = prioritized_slice(text, budget=10000)
    assert "Short text" in result
    assert "Second paragraph" in result
    assert "[...]" not in result


def test_even_coverage_respects_budget():
    """Even-coverage result must not exceed budget."""
    sentences = [f"Word{i} " * 20 + "." for i in range(1000)]
    text = " ".join(sentences)
    for budget in [5000, 20000, 50000]:
        result = prioritized_slice(text, budget=budget)
        assert len(result) <= budget, f"Result {len(result)} exceeds budget {budget}"


# --- Helper function tests ---


def test_chunk_by_paragraphs():
    paragraphs = [f"Para {i}. " * 10 for i in range(10)]
    text = "\n\n".join(paragraphs)
    chunks = _chunk_by_paragraphs(text, target_size=500)
    assert len(chunks) >= 2
    # All content preserved
    rejoined = " ".join(chunks)
    for i in range(10):
        assert f"Para {i}" in rejoined


def test_chunk_by_size():
    text = ". ".join(f"Sentence {i}" for i in range(200)) + "."
    chunks = _chunk_by_size(text, target_size=500)
    assert len(chunks) >= 2
    # All content preserved
    rejoined = " ".join(chunks)
    assert "Sentence 0" in rejoined
    assert "Sentence 199" in rejoined


def test_even_indices():
    assert _even_indices(10, 2) == [0, 9]
    assert _even_indices(10, 10) == list(range(10))
    assert _even_indices(5, 5) == [0, 1, 2, 3, 4]
    # k=3 should produce 3 evenly spaced indices starting with 0 and ending with 9
    result_3 = _even_indices(10, 3)
    assert len(result_3) == 3
    assert result_3[0] == 0
    assert result_3[-1] == 9
    # Always includes first and last
    for n in range(2, 20):
        for k in range(2, n + 1):
            indices = _even_indices(n, k)
            assert indices[0] == 0
            assert indices[-1] == n - 1
            assert len(indices) == len(set(indices))  # no duplicates


def test_select_even_coverage_fits():
    chunks = ["chunk one", "chunk two", "chunk three"]
    result = _select_even_coverage(chunks, budget=10000)
    assert "chunk one" in result
    assert "chunk two" in result
    assert "chunk three" in result
    assert "[...]" not in result


def test_select_even_coverage_gaps():
    chunks = [f"Chunk {i} content here." for i in range(20)]
    result = _select_even_coverage(chunks, budget=200)
    assert "Chunk 0" in result
    assert "Chunk 19" in result
    assert "[...]" in result
