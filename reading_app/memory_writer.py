"""Structured writer for memory/memory.md with bounded sections.

Parses markdown sections (## Header), manages list entries (- item),
enforces per-section size limits, and writes atomically.
"""

from __future__ import annotations

import logging
import os
import re
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


class MemoryWriter:
    SECTIONS = {
        "User Profile": {"max_entries": 10, "max_chars": 800},
        "Research Focus": {"max_entries": 15, "max_chars": 1200},
        "Learned Preferences": {"max_entries": 20, "max_chars": 1000},
        "Standing Instructions": {"max_entries": 10, "max_chars": 600},
    }

    def __init__(self, memory_path: Path | str):
        self.memory_path = Path(memory_path)

    def _parse(self) -> dict[str, list[str]]:
        """Parse memory.md into {section_name: [entries]}."""
        if not self.memory_path.exists():
            return {s: [] for s in self.SECTIONS}

        text = self.memory_path.read_text(encoding="utf-8")
        sections: dict[str, list[str]] = {s: [] for s in self.SECTIONS}
        current_section = None

        for line in text.splitlines():
            header_match = re.match(r"^##\s+(.+)$", line)
            if header_match:
                name = header_match.group(1).strip()
                current_section = name if name in self.SECTIONS else None
                continue

            if current_section is None:
                continue

            # Skip HTML comments
            stripped = line.strip()
            if stripped.startswith("<!--") or stripped.startswith("-->") or not stripped:
                continue

            # Parse list items
            entry_match = re.match(r"^-\s+(.+)$", stripped)
            if entry_match:
                sections[current_section].append(entry_match.group(1).strip())

        return sections

    def _normalize(self, text: str) -> str:
        """Normalize for duplicate detection: lowercase, collapse whitespace."""
        return re.sub(r"\s+", " ", text.lower().strip())

    def _is_duplicate(self, entry: str, existing: list[str]) -> bool:
        """Check if entry is a duplicate of any existing entry."""
        norm = self._normalize(entry)
        return any(self._normalize(e) == norm for e in existing)

    def read_section(self, section: str) -> list[str]:
        """Read entries from a section."""
        if section not in self.SECTIONS:
            return []
        return self._parse().get(section, [])

    def add_entry(self, section: str, entry: str) -> bool:
        """Add an entry to a section. Returns True if added, False if duplicate or invalid."""
        if section not in self.SECTIONS:
            logger.debug("Unknown section: %s", section)
            return False

        entry = entry.strip()
        if not entry:
            return False

        sections = self._parse()
        entries = sections[section]

        if self._is_duplicate(entry, entries):
            return False

        entries.append(entry)

        # Enforce limits — drop oldest entries
        config = self.SECTIONS[section]
        while len(entries) > config["max_entries"]:
            entries.pop(0)

        # Enforce char limit — drop oldest until under limit
        while sum(len(e) for e in entries) > config["max_chars"] and len(entries) > 1:
            entries.pop(0)

        sections[section] = entries
        self._write(sections)
        return True

    def remove_entry(self, section: str, pattern: str) -> bool:
        """Remove entries matching pattern (case-insensitive substring). Returns True if any removed."""
        if section not in self.SECTIONS:
            return False

        sections = self._parse()
        entries = sections[section]
        pattern_lower = pattern.lower()
        new_entries = [e for e in entries if pattern_lower not in e.lower()]

        if len(new_entries) == len(entries):
            return False

        sections[section] = new_entries
        self._write(sections)
        return True

    def _write(self, sections: dict[str, list[str]]) -> None:
        """Atomically write sections back to memory.md."""
        lines = ["# Memory", ""]
        for section_name in self.SECTIONS:
            lines.append(f"## {section_name}")
            entries = sections.get(section_name, [])
            if entries:
                for entry in entries:
                    lines.append(f"- {entry}")
            lines.append("")

        content = "\n".join(lines)

        # Atomic write: write to temp file then rename
        tmp_path = None
        try:
            dir_path = self.memory_path.parent
            fd, tmp_path = tempfile.mkstemp(dir=str(dir_path), suffix=".md.tmp")
            try:
                os.write(fd, content.encode("utf-8"))
            finally:
                os.close(fd)
            os.replace(tmp_path, str(self.memory_path))
        except Exception:
            logger.error("Failed to write memory file", exc_info=True)
            if tmp_path:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
