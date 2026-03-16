"""Tests for agents.evolve."""

from agents.evolve import EvolveAgent, MUTATIONS, _parse_evolved


def test_mutations_defined():
    assert "TIGHTEN" in MUTATIONS
    assert "INVERT" in MUTATIONS
    assert "TRANSFER" in MUTATIONS
    assert "BROADEN" in MUTATIONS


def test_choose_mutation_low_testability():
    agent = EvolveAgent.__new__(EvolveAgent)
    idea = {"feasibility_score": 0.3, "novelty_score": 0.7, "domain_specificity": 0.5}
    assert agent._choose_mutation(idea) == "TIGHTEN"


def test_choose_mutation_low_novelty():
    agent = EvolveAgent.__new__(EvolveAgent)
    idea = {"feasibility_score": 0.6, "novelty_score": 0.3, "domain_specificity": 0.5}
    assert agent._choose_mutation(idea) == "INVERT"


def test_choose_mutation_high_domain():
    agent = EvolveAgent.__new__(EvolveAgent)
    idea = {"feasibility_score": 0.6, "novelty_score": 0.6, "domain_specificity": 0.8}
    assert agent._choose_mutation(idea) == "TRANSFER"


def test_choose_mutation_default():
    agent = EvolveAgent.__new__(EvolveAgent)
    idea = {"feasibility_score": 0.6, "novelty_score": 0.6, "domain_specificity": 0.5}
    assert agent._choose_mutation(idea) == "BROADEN"


def test_parse_evolved():
    text = '{"evolved_idea_text": "Improved idea", "mutation_applied": "TIGHTEN", "what_changed": "More specific"}'
    result = _parse_evolved(text)
    assert result["evolved_idea_text"] == "Improved idea"


def test_parse_evolved_code_block():
    text = '```json\n{"evolved_idea_text": "Better idea"}\n```'
    result = _parse_evolved(text)
    assert result["evolved_idea_text"] == "Better idea"


def test_parse_evolved_failure():
    result = _parse_evolved("no json")
    assert result == {}
