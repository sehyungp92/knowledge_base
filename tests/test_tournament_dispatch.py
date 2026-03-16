"""Test that the dispatcher can route /reflect to tournament pipeline."""

from pathlib import Path

from skills import SkillRegistry

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "skills" / "registry.yaml"


def test_reflect_skill_registered():
    """The reflect skill should be loadable from the real registry."""
    registry = SkillRegistry(REGISTRY_PATH)
    assert "reflect" in registry.skills


def test_reflect_matches_deep_command():
    """A /reflect deep command should match the reflect skill."""
    registry = SkillRegistry(REGISTRY_PATH)
    result = registry.match("/reflect deep src_001")
    assert result is not None
    skill, match = result
    assert skill.name == "reflect"


def test_reflect_matches_bare_command():
    """A bare /reflect should also match."""
    registry = SkillRegistry(REGISTRY_PATH)
    result = registry.match("/reflect")
    assert result is not None
    skill, match = result
    assert skill.name == "reflect"


def test_reflect_prompt_references_tournament():
    """The reflect skill prompt should reference the tournament pipeline."""
    registry = SkillRegistry(REGISTRY_PATH)
    skill = registry.skills["reflect"]
    text = skill.prompt_text(strip_frontmatter=True)
    # The prompt should mention connections/ideas/generation
    assert any(word in text.lower() for word in ["tournament", "ideas", "generate", "connections"])


def test_landscape_skills_registered():
    """All 6 new landscape skills should be loadable from the real registry."""
    registry = SkillRegistry(REGISTRY_PATH)
    for name in ["landscape", "bottlenecks", "anticipate", "implications", "enrich", "themes"]:
        assert name in registry.skills, f"Skill '{name}' should be registered"
        skill = registry.skills[name]
        # Each skill should have a valid prompt file
        assert skill.prompt_text() is not None


def test_landscape_skills_match_patterns():
    """Landscape skills should match their trigger patterns."""
    registry = SkillRegistry(REGISTRY_PATH)
    test_commands = {
        "landscape": "/landscape robotics",
        "bottlenecks": "/bottlenecks",
        "anticipate": "/anticipate robotics",
        "implications": "/implications src_001",
        "enrich": "/enrich src_001",
        "themes": "/themes approve quantum_ml",
    }
    for expected_skill, command in test_commands.items():
        result = registry.match(command)
        assert result is not None, f"Command '{command}' should match a skill"
        skill, match = result
        assert skill.name == expected_skill, f"'{command}' should match '{expected_skill}', got '{skill.name}'"
