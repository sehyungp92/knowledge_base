"""EvolveAgent: critique-guided mutation of ideas."""

from __future__ import annotations

import json
import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor

from agents.base import BaseAgent
from agents.generate import TournamentGoal

logger = logging.getLogger(__name__)

MUTATIONS = {
    "TIGHTEN": "Make the idea more specific and testable",
    "INVERT": "Flip an assumption to generate a contrarian variant",
    "TRANSFER": "Apply this idea to a completely different domain",
    "BROADEN": "Generalize the idea to a wider scope",
}

EVOLVE_PROMPT = """You are evolving a research idea using the {mutation} mutation.

## Mutation: {mutation_description}

## Original Idea
{idea_text}

## Critique Feedback
Strengths: {strengths}
Weaknesses: {weaknesses}
Suggestions: {suggestions}

{goal_section}

## Instructions
Apply the {mutation} mutation to improve this idea. Address the weaknesses identified
in the critique while preserving the strengths.

Return JSON:
{{
  "evolved_idea_text": "...",
  "mutation_applied": "{mutation}",
  "what_changed": "...",
  "grounding": [{{"source_id": "...", "claim_id": "...", "snippet": "..."}}],
  "testability": "..."
}}
"""


class EvolveAgent(BaseAgent):
    """Evolves ideas through critique-guided mutation."""

    def __init__(self, executor, model: str | None = None):
        super().__init__(executor, model=model, session_prefix="evolve")

    def _choose_mutation(self, idea: dict) -> str:
        """Choose mutation based on critique scores."""
        testability = idea.get("feasibility_score", 0.5)
        novelty = idea.get("novelty_score", 0.5)
        domain_spec = idea.get("domain_specificity", 0.5)

        if testability < 0.4:
            return "TIGHTEN"
        if novelty < 0.5:
            return "INVERT"
        if domain_spec > 0.7:
            return "TRANSFER"
        return "BROADEN"

    def evolve(
        self,
        idea: dict,
        mutation: str | None = None,
        goal: TournamentGoal | None = None,
        deadline: float | None = None,
    ) -> dict:
        """Evolve a single idea. Returns a new idea dict (non-destructive)."""
        if mutation is None:
            mutation = self._choose_mutation(idea)

        goal_section = ""
        if goal and goal.description:
            goal_section = f"## Tournament Goal\n{goal.description}"
            if goal.preferences:
                goal_section += f"\nPreferences: {json.dumps(goal.preferences)}"

        prompt = EVOLVE_PROMPT.format(
            mutation=mutation,
            mutation_description=MUTATIONS.get(mutation, mutation),
            idea_text=idea.get("idea_text", ""),
            strengths=idea.get("critique_strengths", "N/A"),
            weaknesses=idea.get("critique_weaknesses", "N/A"),
            suggestions=idea.get("critique_suggestions", "N/A"),
            goal_section=goal_section,
        )

        result = self._run(prompt, session_id=f"evolve_{mutation.lower()}", deadline=deadline)
        parsed = _parse_evolved(result.text)

        # Create new idea (non-destructive merge)
        evolved = dict(idea)
        if parsed.get("evolved_idea_text"):
            evolved["idea_text"] = parsed["evolved_idea_text"]
        evolved["mutation_applied"] = mutation
        evolved["what_changed"] = parsed.get("what_changed", "")
        evolved["parent_idea_id"] = idea.get("id")
        evolved["idea_type"] = f"evolved_{mutation.lower()}"
        if parsed.get("grounding"):
            evolved["grounding"] = parsed["grounding"]
        if parsed.get("testability"):
            evolved["testability"] = parsed["testability"]

        return evolved

    def evolve_batch(
        self,
        ideas: list[dict],
        goal: TournamentGoal | None = None,
        deadline: float | None = None,
    ) -> list[dict]:
        """Evolve a batch of ideas in parallel, choosing mutation per idea."""

        def _evolve_one(idea: dict) -> dict:
            if deadline and time.monotonic() >= deadline:
                logger.warning("Skipping evolution — deadline reached")
                return idea
            try:
                return self.evolve(idea, goal=goal, deadline=deadline)
            except Exception:
                logger.warning(
                    "Evolution failed for idea: %s",
                    idea.get("idea_text", "")[:80],
                    exc_info=True,
                )
                return idea  # Keep original on failure

        with ThreadPoolExecutor(max_workers=len(ideas)) as pool:
            evolved = list(pool.map(_evolve_one, ideas))
        return evolved


def _parse_evolved(text: str) -> dict:
    brace = text.find("{")
    if brace >= 0:
        depth = 0
        for i in range(brace, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[brace : i + 1])
                    except json.JSONDecodeError:
                        break
    json_match = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    return {}
