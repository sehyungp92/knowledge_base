"""Shared JSON-from-LLM-output parsing utility.

Claude outputs often wrap JSON in ```json code blocks or include
preamble/postamble text. This module provides a single parser that
handles all common patterns, replacing 11 duplicate implementations.
"""

from __future__ import annotations

import json
import logging
import re

logger = logging.getLogger(__name__)

# Matches ```json ... ``` or ``` ... ``` fenced code blocks
_CODE_BLOCK_RE = re.compile(r"```(?:json)?\s*\n(.*?)\n```", re.DOTALL)


def parse_json_from_llm(text: str, *, expect: type = list) -> list | dict | None:
    """Parse JSON from Claude output. Handles ```json blocks and raw JSON.

    Strategy: code-block regex -> raw bracket/brace scanning -> None.

    Args:
        text: Raw LLM output text.
        expect: Expected top-level type (list or dict). Defaults to list.

    Returns:
        Parsed JSON matching the expected type, or None if parsing fails.
    """
    if not text:
        return None

    opener, closer = ("[", "]") if expect is list else ("{", "}")

    # 1. Try fenced code block
    m = _CODE_BLOCK_RE.search(text)
    if m:
        try:
            parsed = json.loads(m.group(1))
            if isinstance(parsed, expect):
                return parsed
        except json.JSONDecodeError:
            pass

    # 2. Try raw bracket/brace scanning (string-aware)
    start = text.find(opener)
    if start >= 0:
        depth = 0
        in_string = False
        escape = False
        for i in range(start, len(text)):
            c = text[i]
            if escape:
                escape = False
                continue
            if c == '\\' and in_string:
                escape = True
                continue
            if c == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if c == opener:
                depth += 1
            elif c == closer:
                depth -= 1
                if depth == 0:
                    try:
                        parsed = json.loads(text[start : i + 1])
                        if isinstance(parsed, expect):
                            return parsed
                    except json.JSONDecodeError:
                        break

    return None
