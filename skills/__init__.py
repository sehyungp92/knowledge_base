"""Skills registry for matching user commands to skill prompts."""

from __future__ import annotations

import logging
import os
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


@dataclass
class Skill:
    """A single registered skill."""

    name: str
    trigger_pattern: str
    prompt_path: Path
    description: str = ""
    timeout: int = 300
    stream_progress: bool = False
    tools_allowed: list[str] = field(default_factory=list)
    tools_denied: list[str] = field(default_factory=list)
    requires: dict[str, Any] = field(default_factory=dict)
    _compiled_pattern: re.Pattern | None = field(default=None, repr=False)

    def __post_init__(self):
        self._compiled_pattern = re.compile(self.trigger_pattern)

    def match(self, text: str) -> re.Match | None:
        return self._compiled_pattern.match(text)

    def metadata(self) -> dict[str, str]:
        """Parse YAML frontmatter from the prompt file."""
        raw = self.prompt_path.read_text(encoding="utf-8")
        if raw.startswith("---"):
            parts = raw.split("---", 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1]) or {}
        return {}

    def prompt_text(self, strip_frontmatter: bool = True) -> str:
        """Read prompt file content, optionally stripping YAML frontmatter."""
        raw = self.prompt_path.read_text(encoding="utf-8")
        if strip_frontmatter and raw.startswith("---"):
            parts = raw.split("---", 2)
            if len(parts) >= 3:
                return parts[2].lstrip("\n")
        return raw


class SkillRegistry:
    """Loads skills from registry.yaml and checks eligibility."""

    def __init__(self, registry_path: Path | None = None):
        if registry_path is None:
            registry_path = Path(__file__).parent / "registry.yaml"
        self.registry_path = registry_path
        self.skills_dir = registry_path.parent
        self.skills: dict[str, Skill] = {}
        self._load()

    def _load(self):
        raw = yaml.safe_load(self.registry_path.read_text(encoding="utf-8"))
        for name, defn in raw.get("skills", {}).items():
            requires = defn.get("requires", {})
            if not self._check_eligible(name, requires):
                continue
            prompt_path = self.skills_dir / defn["prompt"]
            if not prompt_path.exists():
                logger.warning("Skill %s: prompt file %s not found, skipping", name, prompt_path)
                continue
            self.skills[name] = Skill(
                name=name,
                trigger_pattern=defn["trigger_pattern"],
                prompt_path=prompt_path,
                description=defn.get("description", ""),
                timeout=defn.get("timeout", 300),
                stream_progress=defn.get("stream_progress", False),
                tools_allowed=defn.get("tools_allowed", []),
                tools_denied=defn.get("tools_denied", []),
                requires=requires,
            )

    def _check_eligible(self, name: str, requires: dict) -> bool:
        for binary in requires.get("bins", []):
            if shutil.which(binary) is None:
                logger.warning("Skill %s: required binary '%s' not found, skipping", name, binary)
                return False
        for env_var in requires.get("env", []):
            if not os.environ.get(env_var):
                logger.warning("Skill %s: required env var '%s' not set, skipping", name, env_var)
                return False
        return True

    def match(self, text: str) -> tuple[Skill, re.Match] | None:
        """Find the first skill whose trigger pattern matches the text."""
        for skill in self.skills.values():
            m = skill.match(text)
            if m:
                return skill, m
        return None
