"""Tests for skills registry."""

from pathlib import Path

import yaml

from skills import SkillRegistry, Skill


def _create_registry(tmp_path):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    (prompts_dir / "save.md").write_text(
        "---\nname: save\ndescription: Save a URL\n---\n\n# Save Skill\nInstructions here.",
        encoding="utf-8",
    )
    (prompts_dir / "ask.md").write_text(
        "---\nname: ask\ndescription: Ask a question\n---\n\n# Ask Skill\nQuery instructions.",
        encoding="utf-8",
    )
    registry_yaml = {
        "skills": {
            "save": {
                "trigger_pattern": r"^/save\s+(\S+)",
                "prompt": "prompts/save.md",
                "description": "Save a URL",
                "tools_allowed": ["Read", "Write"],
                "tools_denied": [],
            },
            "ask": {
                "trigger_pattern": r"^/ask\s+(.+)",
                "prompt": "prompts/ask.md",
                "description": "Ask a question",
                "tools_allowed": ["Read"],
                "tools_denied": ["Write"],
            },
        }
    }
    registry_path = tmp_path / "registry.yaml"
    registry_path.write_text(yaml.dump(registry_yaml), encoding="utf-8")
    return SkillRegistry(registry_path)


def test_load_skills(tmp_path):
    reg = _create_registry(tmp_path)
    assert "save" in reg.skills
    assert "ask" in reg.skills


def test_match_save(tmp_path):
    reg = _create_registry(tmp_path)
    result = reg.match("/save https://example.com")
    assert result is not None
    skill, match = result
    assert skill.name == "save"
    assert match.group(1) == "https://example.com"


def test_match_ask(tmp_path):
    reg = _create_registry(tmp_path)
    result = reg.match("/ask what is RLHF?")
    assert result is not None
    skill, match = result
    assert skill.name == "ask"


def test_no_match(tmp_path):
    reg = _create_registry(tmp_path)
    assert reg.match("just a regular message") is None


def test_skill_prompt_text(tmp_path):
    reg = _create_registry(tmp_path)
    skill = reg.skills["save"]
    text = skill.prompt_text(strip_frontmatter=True)
    assert "Save Skill" in text
    assert "---" not in text


def test_skill_metadata(tmp_path):
    reg = _create_registry(tmp_path)
    skill = reg.skills["save"]
    meta = skill.metadata()
    assert meta["name"] == "save"
    assert meta["description"] == "Save a URL"


def test_ineligible_skill_excluded(tmp_path):
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir(exist_ok=True)
    (prompts_dir / "special.md").write_text("---\nname: special\n---\nSpecial", encoding="utf-8")
    registry_yaml = {
        "skills": {
            "special": {
                "trigger_pattern": r"^/special",
                "prompt": "prompts/special.md",
                "description": "Needs missing binary",
                "requires": {"bins": ["nonexistent_binary_xyz"]},
            }
        }
    }
    registry_path = tmp_path / "registry.yaml"
    registry_path.write_text(yaml.dump(registry_yaml), encoding="utf-8")
    reg = SkillRegistry(registry_path)
    assert "special" not in reg.skills
