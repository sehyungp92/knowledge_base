"""Markdown-based memory context loader."""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class MemorySystem:
    """Loads and manages markdown memory files."""

    def __init__(self, memory_path: Path):
        self.memory_path = Path(memory_path)
        self.logs_dir = self.memory_path / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)

    def _read_file(self, path: Path) -> str:
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    def load_context(self) -> str:
        """Assemble full memory context from memory.md + soul.md + agents.md + today's log."""
        parts = []
        memory = self._read_file(self.memory_path / "memory.md")
        if memory:
            parts.append(f"## Memory\n{memory}")
        soul = self._read_file(self.memory_path / "soul.md")
        if soul:
            parts.append(f"## Soul\n{soul}")
        agents = self._read_file(self.memory_path / "agents.md")
        if agents:
            parts.append(f"## Agent Rules\n{agents}")
        today_log = self._read_file(self._today_log_path())
        if today_log:
            parts.append(f"## Today's Log\n{today_log}")
        return "\n\n---\n\n".join(parts)

    def append_to_log(self, section: str, content: str):
        """Append content under a section heading in today's log file."""
        log_path = self._today_log_path()
        existing = self._read_file(log_path)
        section_header = f"## {section}"
        if section_header in existing:
            lines = existing.split("\n")
            insert_idx = None
            for i, line in enumerate(lines):
                if line.strip() == section_header:
                    for j in range(i + 1, len(lines)):
                        if lines[j].startswith("## "):
                            insert_idx = j
                            break
                    if insert_idx is None:
                        insert_idx = len(lines)
                    break
            if insert_idx is not None:
                lines.insert(insert_idx, content)
                log_path.write_text("\n".join(lines), encoding="utf-8")
            else:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(f"\n{content}\n")
        else:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"\n{section_header}\n{content}\n")

    def load_voice(self) -> str:
        """Load just the soul.md content for narrative voice injection."""
        return self._read_file(self.memory_path / "soul.md")

    def get_heartbeat_instructions(self) -> str:
        """Read heartbeat.md for proactive task instructions."""
        return self._read_file(self.memory_path / "heartbeat.md")

    def _today_log_path(self) -> Path:
        return self.logs_dir / f"{datetime.now().strftime('%Y-%m-%d')}.md"
