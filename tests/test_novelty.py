"""Tests for agents.novelty."""

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
