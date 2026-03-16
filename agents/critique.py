"""CritiqueAgent: 5-dimension scoring for ideas."""

from __future__ import annotations

import json
import logging
import re

from agents.base import BaseAgent

logger = logging.getLogger(__name__)

CRITIQUE_PROMPT = """You are critiquing research ideas on 5 dimensions.

For each idea, score on these dimensions (0.0 to 1.0):
1. **novelty** — Is this genuinely new? (weight: 0.3)
2. **testability** — Can this be tested or validated? (weight: 0.2)
3. **impact** — How significant would this be if true? (weight: 0.3)
4. **grounding** — Is this well-supported by evidence? (weight: 0.2)
5. **domain_specificity** — How domain-specific vs general? (not weighted in overall)

overall_score = 0.3*novelty + 0.2*testability + 0.3*impact + 0.2*grounding

{goal_section}

## Ideas to Critique
{ideas_json}

Return JSON array:
[{{
  "idea_index": 0,
  "novelty": 0.0-1.0,
  "testability": 0.0-1.0,
  "impact": 0.0-1.0,
  "grounding": 0.0-1.0,
  "domain_specificity": 0.0-1.0,
  "overall_score": 0.0-1.0,
  "strengths": "...",
  "weaknesses": "...",
  "suggestions": "..."
}}]
"""


class CritiqueAgent(BaseAgent):
    """Scores ideas on 5 dimensions."""

    def __init__(self, executor, model: str | None = None):
        super().__init__(executor, model=model, session_prefix="critique")

    def critique(self, ideas: list[dict], goal_text: str = "") -> list[dict]:
        """Critique a batch of ideas.

        Returns list of critique dicts aligned by idea_index.
        """
        goal_section = f"## Tournament Goal\n{goal_text}" if goal_text else ""
        ideas_json = json.dumps(
            [{"index": i, "idea_text": idea.get("idea_text", ""),
              "idea_type": idea.get("idea_type", ""),
              "grounding": idea.get("grounding", []),
              "testability": idea.get("testability", "")}
             for i, idea in enumerate(ideas)],
            indent=2,
        )

        prompt = CRITIQUE_PROMPT.format(
            ideas_json=ideas_json[:15000],
            goal_section=goal_section,
        )
        result = self._run(prompt, session_id="critique_batch")
        critiques = _parse_critiques(result.text)

        # Merge critiques back into ideas
        critique_map = {c.get("idea_index", i): c for i, c in enumerate(critiques)}
        for i, idea in enumerate(ideas):
            if i in critique_map:
                c = critique_map[i]
                idea["novelty_score"] = c.get("novelty", 0.5)
                idea["feasibility_score"] = c.get("testability", 0.5)
                idea["impact_score"] = c.get("impact", 0.5)
                idea["grounding_score"] = c.get("grounding", 0.5)
                idea["domain_specificity"] = c.get("domain_specificity", 0.5)
                idea["overall_score"] = c.get("overall_score",
                    0.3 * idea["novelty_score"] + 0.2 * idea["feasibility_score"] +
                    0.3 * idea["impact_score"] + 0.2 * idea["grounding_score"])
                idea["critique_strengths"] = c.get("strengths", "")
                idea["critique_weaknesses"] = c.get("weaknesses", "")
                idea["critique_suggestions"] = c.get("suggestions", "")

        return ideas


def _parse_critiques(text: str) -> list[dict]:
    """Parse JSON array of critiques from LLM output."""
    json_match = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    bracket = text.find("[")
    if bracket >= 0:
        depth = 0
        for i in range(bracket, len(text)):
            if text[i] == "[":
                depth += 1
            elif text[i] == "]":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[bracket : i + 1])
                    except json.JSONDecodeError:
                        break
    return []
