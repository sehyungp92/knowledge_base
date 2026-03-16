"""Shared follow-up command extraction from response text."""

from __future__ import annotations

import re

# Matches lines like:
#   - /landscape SaaS & Service-as-Software
#   - `/ask what is the strongest counter-evidence?`
#   * /reflect autonomous agents
#   - /reflect autonomous agents — generate novel ideas
_COMMAND_RE = re.compile(
    r"^[-*]\s+"                               # list marker
    r'(?:Run\s+|")?'                          # optional "Run " or opening quote
    r"`?(\/\w+(?:\s+[^`\n]+?)?)`?"            # "/cmd args" or "`/cmd args`"
    r"(?:"
    r"\s+[-—]{2,}\s+.+"                       # " -- description"
    r"|"
    r'\s+(?:for|to|if)\s+.+'                  # " for ..." / " to ..." description
    r"|"
    r'"'                                      # closing quote
    r")?$",
)

# Header patterns that signal a follow-up section
_FOLLOWUP_HEADER_RE = re.compile(
    r"^(?:#{1,4}\s+)?(?:follow[\s-]?up|next\s+steps?|suggested\s+commands?|try\s+next|you\s+(?:can|could)\s+also)",
    re.IGNORECASE,
)


def extract_followups(text: str) -> list[dict]:
    """Extract follow-up commands from response text.

    Returns list of {"command": "/reflect autonomous agents",
                      "label": "reflect autonomous agents"}
    Only extracts from lines that appear after a follow-up header.
    """
    lines = text.split("\n")
    in_followup_section = False
    results = []

    for line in lines:
        stripped = line.strip()

        # Detect follow-up section header
        if _FOLLOWUP_HEADER_RE.search(stripped):
            in_followup_section = True
            continue

        # A blank line after commands ends the section
        if in_followup_section and not stripped:
            if results:
                break
            continue

        if not in_followup_section:
            continue

        m = _COMMAND_RE.match(stripped)
        if m:
            command = m.group(1).strip().strip("`")
            # Label: everything after the slash-command name
            label_parts = command.split(None, 1)
            label = label_parts[1] if len(label_parts) > 1 else label_parts[0].lstrip("/")
            results.append({"command": command, "label": label})

    return results


def strip_followups_section(text: str) -> str:
    """Remove the follow-up options section from response text.

    For Telegram/Discord, we render these as buttons instead,
    so the text section is redundant.
    """
    lines = text.split("\n")
    section_start = None

    for i, line in enumerate(lines):
        if _FOLLOWUP_HEADER_RE.search(line.strip()):
            section_start = i
            break

    if section_start is None:
        return text

    # Walk backwards from section_start to trim any preceding blank lines
    while section_start > 0 and not lines[section_start - 1].strip():
        section_start -= 1

    return "\n".join(lines[:section_start]).rstrip()
