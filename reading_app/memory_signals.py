"""Extract memory-worthy signals from user interactions and persist to memory.md.

Fire-and-forget: called in a daemon thread after response is sent.
Uses Haiku for cheap/fast signal extraction.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from reading_app.memory_writer import MemoryWriter

logger = logging.getLogger(__name__)

SIGNAL_EXTRACTION_PROMPT = """Analyze this user interaction and extract memory-worthy signals.

**Skill used:** {skill_name}
**User input:** {user_input}
**System response (truncated):** {response_excerpt}

Extract signals that would help personalize future interactions. Return a JSON object with these keys (each is an array of short strings, or empty array if none):

- "research_focus": themes/topics the user is actively engaging with (inferred from what they save, ask about, enrich)
- "preferences": depth preferences, formatting requests, response length signals, value signals
- "standing_instructions": explicit directives ("always...", "never...", "skip...", "prioritize...")
- "profile": domain expertise indicators, background signals

Rules:
- Each entry must be a single concise line (under 100 chars)
- Only extract CLEAR signals — don't speculate
- For research_focus: note the specific AI theme/topic, not generic "AI"
- For preferences: only if the user's behavior clearly signals a preference
- For standing_instructions: only if the user explicitly states a directive
- Return empty arrays for categories with no clear signal

Return ONLY valid JSON, no explanation.
"""


def extract_and_persist_signals(
    skill_name: str,
    user_input: str,
    response_text: str,
    memory_path: Path | str,
    executor,
) -> None:
    """Extract memory signals via Haiku and write to memory.md.

    Args:
        skill_name: The skill that was invoked (save, enrich, ask, etc.)
        user_input: The user's original input text
        response_text: The system's response
        memory_path: Path to memory/memory.md
        executor: ClaudeExecutor or provider executor with run_raw()
    """
    try:
        # Truncate inputs to keep prompt small
        user_excerpt = user_input[:500]
        response_excerpt = response_text[:800]

        prompt = SIGNAL_EXTRACTION_PROMPT.format(
            skill_name=skill_name,
            user_input=user_excerpt,
            response_excerpt=response_excerpt,
        )

        session_id = f"memory_signal_{skill_name}"
        result = executor.run_raw(
            prompt,
            session_id=session_id,
            model="haiku",
            timeout=15,
        )

        # Parse JSON response
        text = result.text.strip()
        # Handle markdown code blocks
        if text.startswith("```"):
            text = text.split("\n", 1)[-1].rsplit("```", 1)[0].strip()

        signals = json.loads(text)

        writer = MemoryWriter(memory_path)

        section_map = {
            "research_focus": "Research Focus",
            "preferences": "Learned Preferences",
            "standing_instructions": "Standing Instructions",
            "profile": "User Profile",
        }

        added = 0
        for key, section in section_map.items():
            for entry in signals.get(key, []):
                if isinstance(entry, str) and entry.strip():
                    if writer.add_entry(section, entry.strip()):
                        added += 1

        if added:
            logger.info("memory_signals_persisted", count=added, skill=skill_name)

        # Cleanup session
        try:
            executor.cleanup_session(session_id)
        except Exception:
            pass

    except json.JSONDecodeError:
        logger.debug("memory_signal_json_parse_failed", exc_info=True)
    except Exception:
        logger.debug("memory_signal_extraction_failed", exc_info=True)
