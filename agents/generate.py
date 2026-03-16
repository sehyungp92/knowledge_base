"""GenerateAgent: 6 strategies for idea generation, graph-seeded."""

from __future__ import annotations

import json
import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from agents.base import BaseAgent

logger = logging.getLogger(__name__)

STRATEGIES = [
    "synthesis",       # Combine insights from multiple sources
    "transfer",        # Apply method from one domain to another
    "contradiction",   # Resolve contradicting claims
    "extension",       # Push a finding further
    "bottleneck",      # Identify what's blocking progress
    "implications",    # Trace downstream effects
]

GENERATE_PROMPT = """You are generating novel research ideas using the {strategy} strategy.

## Strategy: {strategy_description}

## Available Context
Claims from the knowledge graph:
{claims_context}

Existing ideas (avoid duplicates):
{existing_ideas}

{landscape_section}

{goal_section}

{reviews_section}

## Instructions
Generate {count} ideas using the {strategy} strategy.
Each idea must be grounded in specific claims from the context.
{landscape_instruction}

Return JSON array:
[{{
  "idea_text": "...",
  "idea_type": "{strategy}",
  "grounding": [{{"source_id": "...", "claim_id": "...", "snippet": "..."}}],
  "testability": "How this could be tested or validated",
  "rationale": "Why this idea is interesting and non-obvious"
}}]
"""

# Strategy-specific instructions when landscape context is available
LANDSCAPE_INSTRUCTIONS = {
    "bottleneck": "Reference specific bottlenecks from the landscape data above. Propose concrete approaches to unblock them.",
    "implications": "Trace downstream effects from the recent breakthroughs and cross-theme implications listed above.",
    "synthesis": "Consider how the open anticipations above might connect to claims from multiple sources.",
    "contradiction": "Pay attention to low-confidence beliefs listed above — these represent areas of genuine uncertainty.",
    "extension": "Look at recent breakthroughs above and consider what they now make possible that wasn't before.",
    "transfer": "Use the cross-theme implications above to identify transfer opportunities between domains.",
}

STRATEGY_DESCRIPTIONS = {
    "synthesis": "Combine insights from 2+ sources to form a new understanding",
    "transfer": "Apply a method or finding from one domain to a different domain",
    "contradiction": "Find contradicting claims and propose a resolution or experiment",
    "extension": "Take a finding and push it to its logical extreme or next step",
    "bottleneck": "Identify what's blocking progress and propose how to unblock it",
    "implications": "Trace the downstream effects of a breakthrough or capability",
}


@dataclass
class TournamentGoal:
    """Optional goal/direction for the tournament."""
    description: str = ""
    focus_themes: list[str] | None = None
    preferences: dict | None = None


class GenerateAgent(BaseAgent):
    """Generates ideas using 6 strategies, seeded by graph context."""

    def __init__(self, executor, model: str | None = None):
        super().__init__(executor, model=model, session_prefix="generate")

    def generate(
        self,
        strategy: str,
        claims_context: str,
        existing_ideas: str = "",
        count: int = 3,
        goal: TournamentGoal | None = None,
        reviews_overview: str = "",
        landscape_context: dict | None = None,
        deadline: float | None = None,
    ) -> list[dict]:
        """Generate ideas using a specific strategy.

        Args:
            landscape_context: Optional dict with keys matching strategies:
                bottleneck, implications, synthesis, contradiction, extension, transfer.
                Each value is a formatted string of relevant landscape data.
            deadline: Optional monotonic timestamp; passed to _run() for
                dynamic timeout computation.
        """
        goal_section = ""
        if goal and goal.description:
            goal_section = f"## Tournament Goal\n{goal.description}"
            if goal.focus_themes:
                goal_section += f"\nFocus themes: {', '.join(goal.focus_themes)}"

        reviews_section = ""
        if reviews_overview:
            reviews_section = f"## Previous Reviews (learn from these)\n{reviews_overview}"

        # Build strategy-specific landscape section
        landscape_section = ""
        landscape_instruction = ""
        if landscape_context:
            ctx = landscape_context.get(strategy) or landscape_context.get("_all", "")
            if ctx:
                landscape_section = f"## Landscape Context\n{ctx}"
                landscape_instruction = LANDSCAPE_INSTRUCTIONS.get(strategy, "")

        prompt = GENERATE_PROMPT.format(
            strategy=strategy,
            strategy_description=STRATEGY_DESCRIPTIONS.get(strategy, strategy),
            claims_context=claims_context[:20000],
            existing_ideas=existing_ideas[:5000],
            count=count,
            goal_section=goal_section,
            reviews_section=reviews_section,
            landscape_section=landscape_section,
            landscape_instruction=landscape_instruction,
        )

        result = self._run(prompt, session_id=f"generate_{strategy}", deadline=deadline)
        return _parse_ideas(result.text)

    def generate_all_strategies(
        self,
        claims_context: str,
        existing_ideas: str = "",
        count_per_strategy: int = 2,
        goal: TournamentGoal | None = None,
        reviews_overview: str = "",
        landscape_context: dict | None = None,
        deadline: float | None = None,
    ) -> list[dict]:
        """Generate ideas across all 6 strategies in parallel.

        Uses ThreadPoolExecutor; concurrency is naturally throttled by the
        global API semaphore in ClaudeExecutor.
        """
        all_ideas = []

        def _run_strategy(strategy: str) -> list[dict]:
            if deadline and time.monotonic() >= deadline:
                logger.warning("Skipping strategy %s — deadline reached", strategy)
                return []
            return self.generate(
                strategy, claims_context, existing_ideas,
                count=count_per_strategy, goal=goal,
                reviews_overview=reviews_overview,
                landscape_context=landscape_context,
                deadline=deadline,
            )

        with ThreadPoolExecutor(max_workers=len(STRATEGIES)) as pool:
            futures = {pool.submit(_run_strategy, s): s for s in STRATEGIES}
            for future in as_completed(futures):
                strategy = futures[future]
                try:
                    ideas = future.result()
                    all_ideas.extend(ideas)
                except Exception:
                    logger.warning("Strategy %s failed", strategy, exc_info=True)

        return all_ideas


def _parse_ideas(text: str) -> list[dict]:
    """Parse JSON array of ideas from LLM output."""
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
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    return []
