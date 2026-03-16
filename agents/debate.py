"""DebateAgent: two-tier pairwise selection."""

from __future__ import annotations

import json
import logging
import re

from agents.base import BaseAgent
from agents.generate import TournamentGoal

logger = logging.getLogger(__name__)

DEBATE_PROMPT = """You are judging a debate between two research ideas.

{goal_section}

## Idea A
{idea_a}
Critique scores: novelty={a_novelty:.2f}, testability={a_testability:.2f}, impact={a_impact:.2f}

## Idea B
{idea_b}
Critique scores: novelty={b_novelty:.2f}, testability={b_testability:.2f}, impact={b_impact:.2f}

## Instructions
Compare these ideas head-to-head. Consider:
1. Which is more novel and non-obvious?
2. Which is more actionable/testable?
3. Which would have greater impact if validated?
4. Which is better grounded in evidence?

Return JSON:
{{
  "winner": "A" or "B",
  "reasoning": "...",
  "loser_weaknesses": "Key weakness of the losing idea"
}}
"""

DEEP_DEBATE_PROMPT = """You are a panel of 3 experts debating the top research ideas from a tournament.

{goal_section}

## Ideas Under Debate
{ideas_json}

## Round {round_num} of 3

## Instructions
Each panelist should:
1. Argue for their preferred idea
2. Identify critical flaws in other ideas
3. Suggest improvements

After discussion, vote on ranking. Return JSON:
{{
  "discussion": "...",
  "rankings": [{{"idea_index": 0, "rank": 1, "justification": "..."}}],
  "eliminated_indices": [indices of ideas to eliminate this round],
  "loser_weaknesses": "Weaknesses of eliminated ideas"
}}
"""


class DebateAgent(BaseAgent):
    """Runs single-turn and deep debates between ideas."""

    def __init__(self, executor, model: str | None = None):
        super().__init__(executor, model=model, session_prefix="debate")

    def debate(
        self,
        idea_a: dict,
        idea_b: dict,
        goal: TournamentGoal | None = None,
    ) -> dict:
        """Single-turn pairwise debate. Returns winner dict + reasoning."""
        goal_section = f"## Tournament Goal\n{goal.description}" if goal else ""

        prompt = DEBATE_PROMPT.format(
            idea_a=idea_a.get("idea_text", ""),
            idea_b=idea_b.get("idea_text", ""),
            a_novelty=idea_a.get("novelty_score", 0.5),
            a_testability=idea_a.get("feasibility_score", 0.5),
            a_impact=idea_a.get("impact_score", 0.5),
            b_novelty=idea_b.get("novelty_score", 0.5),
            b_testability=idea_b.get("feasibility_score", 0.5),
            b_impact=idea_b.get("impact_score", 0.5),
            goal_section=goal_section,
        )

        result = self._run(prompt, session_id="debate_pair")
        parsed = _parse_debate_result(result.text)

        winner_key = parsed.get("winner", "A")
        winner = idea_a if winner_key == "A" else idea_b
        loser = idea_b if winner_key == "A" else idea_a

        return {
            "winner": winner,
            "loser": loser,
            "reasoning": parsed.get("reasoning", ""),
            "loser_weaknesses": parsed.get("loser_weaknesses", ""),
        }

    def deep_debate(
        self,
        ideas: list[dict],
        rounds: int = 3,
        goal: TournamentGoal | None = None,
    ) -> list[dict]:
        """Multi-round panel debate for top ideas.

        Args:
            ideas: Top ideas (typically top 40% by critique score)
            rounds: Number of debate rounds
            goal: Optional tournament goal

        Returns: Ranked ideas after elimination
        """
        remaining = list(ideas)
        goal_section = f"## Tournament Goal\n{goal.description}" if goal else ""

        for round_num in range(1, rounds + 1):
            if len(remaining) <= 2:
                break

            ideas_json = json.dumps(
                [{"index": i, "idea_text": idea.get("idea_text", ""),
                  "overall_score": idea.get("overall_score", 0),
                  "strengths": idea.get("critique_strengths", ""),
                  "weaknesses": idea.get("critique_weaknesses", "")}
                 for i, idea in enumerate(remaining)],
                indent=2,
            )

            prompt = DEEP_DEBATE_PROMPT.format(
                ideas_json=ideas_json[:15000],
                round_num=round_num,
                goal_section=goal_section,
            )

            result = self._run(prompt, session_id=f"deep_debate_r{round_num}")
            parsed = _parse_deep_debate(result.text)

            # Eliminate bottom 30%
            eliminated = set(parsed.get("eliminated_indices", []))
            if not eliminated:
                # If no explicit elimination, remove bottom 30% by ranking
                rankings = parsed.get("rankings", [])
                if rankings:
                    rankings.sort(key=lambda r: r.get("rank", 999))
                    n_elim = max(1, len(remaining) * 30 // 100)
                    for r in rankings[-n_elim:]:
                        eliminated.add(r.get("idea_index", -1))

            remaining = [idea for i, idea in enumerate(remaining) if i not in eliminated]

            # Append loser weaknesses to reviews
            loser_weaknesses = parsed.get("loser_weaknesses", "")
            if loser_weaknesses:
                for idea in remaining:
                    idea.setdefault("debate_notes", "")
                    idea["debate_notes"] += f"\nRound {round_num}: {loser_weaknesses}"

        return remaining


def _parse_debate_result(text: str) -> dict:
    json_match = re.search(r"\{[^{}]*\"winner\"[^{}]*\}", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
    return {"winner": "A", "reasoning": "Parse failed"}


def _parse_deep_debate(text: str) -> dict:
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
    return {"rankings": [], "eliminated_indices": []}
