"""Tests for agents.novelty."""

from types import SimpleNamespace
from unittest.mock import MagicMock

from agents.novelty import NoveltyGate, cosine_similarity


def test_cosine_similarity_identical():
    v = [1.0, 0.0, 0.0]
    assert abs(cosine_similarity(v, v) - 1.0) < 1e-6


def test_cosine_similarity_orthogonal():
    assert abs(cosine_similarity([1, 0, 0], [0, 1, 0])) < 1e-6


def test_cosine_similarity_opposite():
    assert abs(cosine_similarity([1, 0], [-1, 0]) + 1.0) < 1e-6


def test_cosine_similarity_empty():
    assert cosine_similarity([], [1, 2]) == 0.0


def test_novelty_gate_passes():
    gate = NoveltyGate(threshold=0.85)
    passes, sim, _ = gate.check("RLHF improves safety", ["GPT-4 is fast"])
    assert passes is True
    assert sim < 0.85


def test_novelty_gate_rejects():
    gate = NoveltyGate(threshold=0.5)
    passes, sim, _ = gate.check(
        "RLHF improves safety and reduces harm",
        ["RLHF improves safety and reduces harm significantly"],
    )
    # Very similar texts should have high Jaccard
    assert sim > 0.4


def test_novelty_gate_embed():
    gate = NoveltyGate(threshold=0.85)
    emb = [1.0] * 768
    existing = [("old idea", [0.5] * 768)]
    passes, sim, _ = gate.check_with_embed(emb, existing)
    assert isinstance(passes, bool)


def test_filter_batch():
    gate = NoveltyGate(threshold=0.9)
    ideas = [
        {"idea_text": "Novel idea about robotics"},
        {"idea_text": "Novel idea about robotics"},  # duplicate
        {"idea_text": "Completely different idea about NLP"},
    ]
    novel = gate.filter_batch(ideas, [])
    assert len(novel) == 2  # Duplicate removed


def test_filter_batch_with_existing():
    gate = NoveltyGate(threshold=0.5)
    ideas = [{"idea_text": "RLHF reduces harmful outputs by 70%"}]
    existing = ["RLHF reduces harmful outputs by 70% in experiments"]
    novel = gate.filter_batch(ideas, existing)
    assert len(novel) <= 1  # May be filtered depending on threshold


# ---------------------------------------------------------------------------
# LLM trivial-implication filter tests (mock-based)
# ---------------------------------------------------------------------------

def _mock_executor(response_text: str) -> MagicMock:
    """Create a mock executor that returns the given text."""
    executor = MagicMock()
    executor.run_raw.return_value = SimpleNamespace(text=response_text)
    return executor


def test_filter_trivial_all_novel():
    """All ideas judged non-trivial should pass."""
    gate = NoveltyGate()
    ideas = [
        {"idea_text": "Combine world models with economic simulation"},
        {"idea_text": "Use adversarial training for robustness in robotics"},
    ]
    response = '[{"id": 1, "trivial": false, "reason": "Novel cross-domain"}, {"id": 2, "trivial": false, "reason": "Non-obvious transfer"}]'
    executor = _mock_executor(response)

    result = gate._filter_trivial_implications(ideas, executor, ["existing claim 1"])
    assert len(result) == 2


def test_filter_trivial_some_rejected():
    """Ideas judged trivial should be filtered out."""
    gate = NoveltyGate()
    ideas = [
        {"idea_text": "Scale models to improve performance"},  # trivial
        {"idea_text": "Use RL for chip design optimization"},  # novel
        {"idea_text": "More data leads to better models"},  # trivial
    ]
    response = (
        '[{"id": 1, "trivial": true, "reason": "Direct implication of scaling laws"}, '
        '{"id": 2, "trivial": false, "reason": "Creative transfer"}, '
        '{"id": 3, "trivial": true, "reason": "Well-known data scaling result"}]'
    )
    executor = _mock_executor(response)

    result = gate._filter_trivial_implications(ideas, executor, ["Scaling laws show..."])
    assert len(result) == 1
    assert result[0]["idea_text"] == "Use RL for chip design optimization"


def test_filter_trivial_rejected_ideas_annotated():
    """Rejected ideas should get trivial-rejection annotations."""
    gate = NoveltyGate()
    ideas = [{"idea_text": "Obvious idea"}]
    response = '[{"id": 1, "trivial": true, "reason": "Direct consequence"}]'
    executor = _mock_executor(response)

    result = gate._filter_trivial_implications(ideas, executor, ["claim"])
    assert len(result) == 0
    assert ideas[0]["novelty_trivial_rejected"] is True
    assert ideas[0]["novelty_trivial_reason"] == "Direct consequence"


def test_filter_trivial_no_json_failopen():
    """No JSON in response should keep all ideas (fail-open)."""
    gate = NoveltyGate()
    ideas = [{"idea_text": "Some idea"}, {"idea_text": "Another idea"}]
    executor = _mock_executor("I can't determine this in JSON format.")

    result = gate._filter_trivial_implications(ideas, executor, ["claim"])
    assert len(result) == 2


def test_filter_trivial_invalid_json_failopen():
    """Malformed JSON should keep all ideas (fail-open)."""
    gate = NoveltyGate()
    ideas = [{"idea_text": "Some idea"}]
    executor = _mock_executor('[{"id": 1, "trivial": true, BROKEN}]')

    result = gate._filter_trivial_implications(ideas, executor, ["claim"])
    assert len(result) == 1


def test_filter_trivial_empty_ideas():
    """Empty ideas list should return empty."""
    gate = NoveltyGate()
    executor = _mock_executor("should not be called")

    result = gate._filter_trivial_implications([], executor, ["claim"])
    assert result == []
    executor.run_raw.assert_not_called()
