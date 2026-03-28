"""TournamentPipeline: 11-step self-improving idea generation pipeline."""

from __future__ import annotations

import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

from agents.base import BaseAgent, DeadlineExceeded
from agents.generate import GenerateAgent, TournamentGoal
from agents.novelty import NoveltyGate
from agents.critique import CritiqueAgent
from agents.debate import DebateAgent
from agents.evolve import EvolveAgent
from agents.executor import ClaudeExecutor

logger = logging.getLogger(__name__)

# Call-count limits per depth mode (replaces USD budgets — Max subscription
# makes every call free, so we bound only by execution time).
DEPTH_CALL_LIMITS = {
    "quick": 15,
    "normal": 40,
    "deep": 80,
    "research": 150,
}

# Strategies per depth
DEPTH_STRATEGIES = {
    "quick": 3,
    "normal": 6,
    "deep": 6,
    "research": 6,
}

# Ideas per strategy per depth
DEPTH_COUNT = {
    "quick": 1,
    "normal": 2,
    "deep": 3,
    "research": 5,
}


@dataclass
class TournamentResult:
    """Result of a tournament run."""
    ideas: list[dict] = field(default_factory=list)
    total_calls: int = 0
    steps_completed: int = 0
    ideas_generated: int = 0
    ideas_after_novelty: int = 0
    ideas_after_debate: int = 0
    call_limit_hit: bool = False


class TournamentPipeline:
    """11-step self-improving idea generation pipeline.

    Steps:
    1. Load claims from DB
    2. Pre-fetch graph context + existing ideas
    3. Generate ideas (6 strategies x N)
    4. Validate grounding
    5. Embed + novelty gate
    6. Critique (5 dimensions)
    7. Debate (two-tier: pairwise + deep panel)
    8. MMR dedup
    9. Evolve top K
    10. Final MMR + rank
    11. Persist to DB
    """

    def __init__(
        self,
        executor: ClaudeExecutor,
        get_conn_fn=None,
        library_path: Path | None = None,
    ):
        self.executor = executor
        self._get_conn = get_conn_fn
        self.library_path = library_path

        self.generator = GenerateAgent(executor)
        self.novelty_gate = NoveltyGate()
        self.critic = CritiqueAgent(executor)
        self.debater = DebateAgent(executor)
        self.evolver = EvolveAgent(executor)

    def run(
        self,
        source_id: str | None = None,
        depth: str = "normal",
        goal: TournamentGoal | None = None,
        timeout: int | None = None,
        on_step: callable | None = None,
    ) -> TournamentResult:
        """Run the full 11-step tournament pipeline.

        Args:
            timeout: Optional wall-clock budget in seconds.  When set, a
                deadline is computed and threaded through generation, debate,
                and evolution steps so they can gracefully skip non-critical
                work when time is running out.
        """
        call_limit = DEPTH_CALL_LIMITS.get(depth, 40)
        n_strategies = DEPTH_STRATEGIES.get(depth, 6)
        count_per = DEPTH_COUNT.get(depth, 2)
        result = TournamentResult()

        # Compute deadline with 30s buffer for persist + response formatting
        deadline: float | None = None
        if timeout:
            deadline = time.monotonic() + timeout - 30

        def _check_deadline(step_name: str) -> bool:
            """Return True if deadline exceeded. Logs a warning."""
            if deadline is None:
                return False
            if time.monotonic() >= deadline:
                logger.warning("Deadline exceeded before %s — skipping", step_name)
                return True
            return False

        def _total_calls() -> int:
            return sum(
                agent.cost_tracker.calls
                for agent in [self.generator, self.critic, self.debater, self.evolver]
            )

        def warn_if_high():
            """Log a warning if call count exceeds the soft limit.
            Does NOT abort — on Max there are no costs to exceed."""
            total = _total_calls()
            result.total_calls = total
            if total > call_limit:
                result.call_limit_hit = True
                logger.warning("Tournament soft call limit %d exceeded: %d calls", call_limit, total)

        def _notify_step(step: int, name: str):
            if on_step:
                try:
                    on_step(step, name)
                except Exception:
                    pass

        try:
            # Step 1: Load claims (critical)
            _notify_step(1, "Loading claims")
            claims_context = self._load_claims(source_id)
            result.steps_completed = 1

            # Step 2: Pre-fetch graph + existing ideas + landscape context (critical)
            _notify_step(2, "Pre-fetching graph and landscape context")
            existing_ideas = self._load_existing_ideas(source_id)
            existing_texts = [i.get("idea_text", "") for i in existing_ideas]
            landscape_context = self._load_landscape_context(source_id, goal)
            result.steps_completed = 2

            # Step 3: Generate ideas — parallelized (critical)
            _notify_step(3, "Generating idea candidates")
            reviews_overview = ""
            all_ideas = self.generator.generate_all_strategies(
                claims_context=claims_context,
                existing_ideas="\n".join(existing_texts[:20]),
                count_per_strategy=count_per,
                goal=goal,
                reviews_overview=reviews_overview,
                landscape_context=landscape_context,
                deadline=deadline,
            )
            # Tag each idea with its generation strategy
            for idea in all_ideas:
                idea.setdefault("tournament_metadata", {})
                idea["tournament_metadata"]["generation_strategy"] = idea.get("strategy", "unknown")
            result.ideas_generated = len(all_ideas)
            result.steps_completed = 3
            warn_if_high()

            # Step 4: Validate grounding (critical, fast)
            _notify_step(4, "Validating grounding")
            validated = self._validate_grounding(all_ideas)
            result.steps_completed = 4

            # Step 5: Embed + novelty gate (critical, fast)
            # Stage 1: embedding/Jaccard dedup. Stage 2: LLM trivial-implication filter.
            _notify_step(5, "Running novelty gate")
            # Gather library claims as reference for LLM trivial-implication check
            library_claims = [
                line.lstrip("- ").split(" [section:")[0]
                for line in claims_context.split("\n") if line.strip()
            ][:30]
            novel = self.novelty_gate.filter_batch(
                validated, existing_texts,
                executor=self.executor,
                library_claims=library_claims,
            )
            # Record novelty scores
            for idea in novel:
                meta = idea.setdefault("tournament_metadata", {})
                meta["novelty_score"] = idea.get("novelty_score")
                meta["novelty_check_passed"] = True
            result.ideas_after_novelty = len(novel)
            result.steps_completed = 5
            warn_if_high()

            if not novel:
                logger.info("No novel ideas survived the novelty gate")
                result.ideas = []
                result.steps_completed = 11
                return result

            # Step 6: Critique (important but deadline-aware)
            _notify_step(6, "Critiquing candidates")
            if not _check_deadline("critique"):
                critiqued = self.critic.critique(novel, goal_text=goal.description if goal else "")
                # Record critique verdicts
                for idea in critiqued:
                    meta = idea.setdefault("tournament_metadata", {})
                    meta["critique_verdict"] = "survive"
                    strengths = idea.get("critique_strengths", "")
                    weaknesses = idea.get("critique_weaknesses", "")
                    meta["critique_summary"] = f"Strengths: {strengths[:150]}. Weaknesses: {weaknesses[:150]}"
                reviews_overview = self._build_reviews_overview(critiqued)
                result.steps_completed = 6
                warn_if_high()
            else:
                critiqued = novel
                for idea in critiqued:
                    meta = idea.setdefault("tournament_metadata", {})
                    meta["critique_verdict"] = "skipped"
                result.steps_completed = 6

            # Step 7: Debate (skippable — parallelized pairwise)
            _notify_step(7, "Running debate rounds")
            sorted_ideas = sorted(critiqued, key=lambda x: x.get("overall_score", 0), reverse=True)
            top_40_pct = max(2, len(sorted_ideas) * 40 // 100)
            top_ideas = sorted_ideas[:top_40_pct]
            bottom_ideas = sorted_ideas[top_40_pct:]

            # Record pre-debate scores and tag debate tier
            for idea in top_ideas:
                meta = idea.setdefault("tournament_metadata", {})
                meta["debate_tier"] = "deep_panel"
                meta["pre_debate_score"] = idea.get("overall_score", 0)
            for idea in bottom_ideas:
                meta = idea.setdefault("tournament_metadata", {})
                meta["debate_tier"] = "single_turn"
                meta["pre_debate_score"] = idea.get("overall_score", 0)

            if not _check_deadline("debate"):
                # Pairwise debate for bottom ideas — parallelized
                survivors = list(top_ideas)
                pairs = [(bottom_ideas[i], bottom_ideas[i + 1])
                         for i in range(0, len(bottom_ideas) - 1, 2)]

                def _debate_pair(pair):
                    a, b = pair
                    try:
                        debate_result = self.debater.debate(a, b, goal)
                        winner = debate_result["winner"]
                        loser_weaknesses = debate_result.get("loser_weaknesses", "")
                        # Record debate outcome on winner
                        meta = winner.setdefault("tournament_metadata", {})
                        delta = meta.get("debate_score_delta", 0.0)
                        meta["debate_outcome"] = (
                            f"Won pairwise debate (score delta: {delta:+.2f}). "
                            f"Loser weakness: {loser_weaknesses[:150]}"
                        )
                        return winner, loser_weaknesses
                    except Exception:
                        return a, ""  # Keep first on failure

                if pairs:
                    with ThreadPoolExecutor(max_workers=len(pairs)) as pool:
                        futures = {pool.submit(_debate_pair, p): p for p in pairs}
                        for future in as_completed(futures):
                            winner, weakness = future.result()
                            survivors.append(winner)
                            if weakness:
                                reviews_overview += f"\nEliminated: {weakness}"

                if len(bottom_ideas) % 2 == 1:
                    survivors.append(bottom_ideas[-1])

                # Tier 2: deep debate for top ideas
                if len(top_ideas) > 2 and depth in ("deep", "research") and not _check_deadline("deep_debate"):
                    try:
                        top_ideas = self.debater.deep_debate(top_ideas, rounds=3, goal=goal)
                        for idea in top_ideas:
                            meta = idea.setdefault("tournament_metadata", {})
                            delta = meta.get("debate_score_delta", 0.0)
                            meta["debate_outcome"] = (
                                f"Survived deep panel debate (3 rounds, score delta: {delta:+.2f})"
                            )
                        survivors = list(top_ideas) + [s for s in survivors if s not in top_ideas]
                    except Exception:
                        logger.warning("Deep debate failed", exc_info=True)
            else:
                survivors = sorted_ideas
                for idea in survivors:
                    idea.setdefault("tournament_metadata", {})["debate_outcome"] = "skipped"

            result.ideas_after_debate = len(survivors)
            result.steps_completed = 7
            warn_if_high()

            # Step 8: MMR dedup (fast, always run)
            _notify_step(8, "Deduplicating ideas")
            deduped = self._mmr_dedup(survivors, lambda_param=0.5, k=min(len(survivors), 15))
            result.steps_completed = 8

            # Step 9: Evolve top K (skippable — parallelized)
            _notify_step(9, "Evolving top candidates")
            if not _check_deadline("evolve"):
                top_k = min(5, len(deduped))
                to_evolve = deduped[:top_k]
                try:
                    evolved = self.evolver.evolve_batch(to_evolve, goal=goal, deadline=deadline)
                    # Median parent score as fallback for unscored evolved ideas
                    parent_scores = [p.get("overall_score", 0.5) for p in to_evolve if p.get("overall_score")]
                    fallback_score = sorted(parent_scores)[len(parent_scores) // 2] if parent_scores else 0.5
                    for idea in evolved:
                        meta = idea.setdefault("tournament_metadata", {})
                        meta["evolution_delta"] = "Evolved from weaker candidate"
                        if not idea.get("overall_score"):
                            idea["overall_score"] = fallback_score
                    deduped = deduped + evolved
                except (DeadlineExceeded, Exception):
                    logger.warning("Evolution step failed or deadline exceeded", exc_info=True)
            result.steps_completed = 9
            warn_if_high()

            # Step 10: Final MMR + rank + belief weighting (fast, always run)
            _notify_step(10, "Final ranking")
            final = self._mmr_dedup(deduped, lambda_param=0.7, k=min(len(deduped), 10))
            final = self._apply_belief_weighting(final)
            final.sort(key=lambda x: x.get("overall_score", 0), reverse=True)
            # Record final rank
            for rank, idea in enumerate(final, 1):
                meta = idea.setdefault("tournament_metadata", {})
                meta["final_rank"] = rank
                meta["final_score"] = idea.get("overall_score", 0)
            result.steps_completed = 10

            # Step 11: Persist (always run)
            _notify_step(11, "Persisting ideas")
            self._persist_ideas(final, source_id)
            result.ideas = final
            result.steps_completed = 11

        except Exception:
            logger.error("Tournament failed", exc_info=True)

        result.total_calls = _total_calls()
        return result

    def _load_claims(self, source_id: str | None) -> str:
        """Load claims from DB as context string."""
        if not self._get_conn:
            return "No database connection available."
        try:
            with self._get_conn() as conn:
                if source_id:
                    rows = conn.execute(
                        "SELECT claim_text, section, evidence_snippet FROM claims WHERE source_id = %s LIMIT 50",
                        (source_id,),
                    ).fetchall()
                else:
                    rows = conn.execute(
                        "SELECT claim_text, section, evidence_snippet FROM claims ORDER BY RANDOM() LIMIT 50"
                    ).fetchall()
            return "\n".join(
                f"- {r['claim_text']} [section: {r.get('section', '?')}]"
                for r in rows
            )
        except Exception:
            logger.warning("Failed to load claims", exc_info=True)
            return ""

    def _load_existing_ideas(self, source_id: str | None) -> list[dict]:
        if not self._get_conn:
            return []
        try:
            with self._get_conn() as conn:
                rows = conn.execute(
                    "SELECT id, idea_text FROM ideas ORDER BY created_at DESC LIMIT 100"
                ).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return []

    def _load_landscape_context(
        self,
        source_id: str | None,
        goal: TournamentGoal | None,
    ) -> dict | None:
        """Load landscape data and format per-strategy context slices.

        Returns dict keyed by strategy name with formatted landscape strings,
        or None if no landscape data is available.
        """
        if not self._get_conn:
            return None

        try:
            # Determine relevant themes
            theme_ids = []
            if goal and goal.focus_themes:
                theme_ids = goal.focus_themes
            elif source_id:
                with self._get_conn() as conn:
                    rows = conn.execute(
                        "SELECT theme_id FROM source_themes WHERE source_id = %s",
                        (source_id,),
                    ).fetchall()
                    theme_ids = [r["theme_id"] for r in rows]

            if not theme_ids:
                return None

            with self._get_conn() as conn:
                bottlenecks = conn.execute(
                    """SELECT id, description, resolution_horizon, bottleneck_type,
                              blocking_what, active_approaches
                       FROM bottlenecks WHERE theme_id = ANY(%s)
                       ORDER BY confidence DESC NULLS LAST LIMIT 20""",
                    (theme_ids,),
                ).fetchall()

                breakthroughs = conn.execute(
                    """SELECT description, significance, what_is_now_possible,
                              immediate_implications, downstream_implications
                       FROM breakthroughs WHERE theme_id = ANY(%s)
                       ORDER BY detected_at DESC LIMIT 10""",
                    (theme_ids,),
                ).fetchall()

                anticipations = conn.execute(
                    """SELECT prediction, confidence, timeline
                       FROM anticipations WHERE theme_id = ANY(%s) AND status = 'open'
                       ORDER BY confidence DESC LIMIT 15""",
                    (theme_ids,),
                ).fetchall()

                implications = conn.execute(
                    """SELECT implication, source_theme_id, target_theme_id
                       FROM cross_theme_implications
                       WHERE source_theme_id = ANY(%s) OR target_theme_id = ANY(%s)
                       LIMIT 15""",
                    (theme_ids, theme_ids),
                ).fetchall()

                beliefs = conn.execute(
                    """SELECT claim, confidence
                       FROM beliefs WHERE domain_theme_id = ANY(%s) AND status = 'active'
                         AND confidence < 0.5
                       LIMIT 10""",
                    (theme_ids,),
                ).fetchall()

            # Load graph edges for source (tensions and connections)
            graph_edges_text = ""
            if source_id:
                try:
                    from retrieval.graph import GraphRetriever
                    retriever = GraphRetriever(self._get_conn)
                    neighbours = retriever.one_hop(source_id)
                    if neighbours:
                        edge_lines = []
                        for n in neighbours[:10]:
                            etype = n.get("edge_type", "?")
                            title = n.get("title", "?")[:80]
                            expl = n.get("explanation", "")[:120]
                            edge_lines.append(f"- [{etype}] {title}: {expl}")
                        graph_edges_text = "\n".join(edge_lines)
                except Exception:
                    pass

            # Format per-strategy slices
            bn_text = "\n".join(
                f"- [{b['id']}] {b['description'][:120]} "
                f"(type: {b.get('bottleneck_type', '?')}, horizon: {b.get('resolution_horizon', '?')}, "
                f"blocking: {b.get('blocking_what', '?')[:60]})"
                for b in bottlenecks
            ) if bottlenecks else ""

            bt_text = "\n".join(
                f"- {b['description'][:120]} (significance: {b.get('significance', '?')})"
                f"\n  Now possible: {b.get('what_is_now_possible', '?')[:100]}"
                for b in breakthroughs
            ) if breakthroughs else ""

            ant_text = "\n".join(
                f"- {a['prediction'][:120]} (confidence: {a.get('confidence', '?')}, "
                f"timeline: {a.get('timeline', '?')})"
                for a in anticipations
            ) if anticipations else ""

            impl_text = "\n".join(
                f"- {i.get('source_theme_id', '?')} -> {i.get('target_theme_id', '?')}: "
                f"{i.get('implication', '?')[:120]}"
                for i in implications
            ) if implications else ""

            belief_text = "\n".join(
                f"- {b['claim'][:120]} (confidence: {b.get('confidence', '?')})"
                for b in beliefs
            ) if beliefs else ""

            context = {}
            if bn_text:
                context["bottleneck"] = f"**Active Bottlenecks:**\n{bn_text}"
            if bt_text and impl_text:
                context["implications"] = f"**Recent Breakthroughs:**\n{bt_text}\n\n**Cross-Theme Implications:**\n{impl_text}"
            contradiction_parts = []
            if belief_text:
                contradiction_parts.append(f"**Low-Confidence Beliefs (areas of uncertainty):**\n{belief_text}")
            if graph_edges_text:
                contradiction_parts.append(f"**Graph Connections (intellectual tensions and links):**\n{graph_edges_text}")
            if contradiction_parts:
                context["contradiction"] = "\n\n".join(contradiction_parts)
            if bt_text:
                context["extension"] = f"**Recent Breakthroughs:**\n{bt_text}"
            if impl_text:
                context["transfer"] = f"**Cross-Theme Implications:**\n{impl_text}"
            if graph_edges_text and ant_text:
                context["synthesis"] = f"**Open Anticipations:**\n{ant_text}\n\n**Graph Connections:**\n{graph_edges_text}"
            elif ant_text:
                context["synthesis"] = f"**Open Anticipations:**\n{ant_text}"

            return context if context else None

        except Exception:
            logger.debug("Failed to load landscape context for tournament", exc_info=True)
            return None

    def _validate_grounding(self, ideas: list[dict]) -> list[dict]:
        """Validate that ideas have proper grounding."""
        validated = []
        for idea in ideas:
            grounding = idea.get("grounding", [])
            if grounding and isinstance(grounding, list):
                validated.append(idea)
            else:
                # Keep ideas even without perfect grounding, just flag them
                idea["grounding_validated"] = False
                validated.append(idea)
        return validated

    def _build_reviews_overview(self, ideas: list[dict]) -> str:
        """Build a summary of critique results for future rounds."""
        lines = []
        for idea in ideas[:10]:
            score = idea.get("overall_score", 0)
            strengths = idea.get("critique_strengths", "")
            weaknesses = idea.get("critique_weaknesses", "")
            lines.append(f"Score {score:.2f}: {strengths[:100]}. Weakness: {weaknesses[:100]}")
        return "\n".join(lines)

    def _mmr_dedup(self, ideas: list[dict], lambda_param: float = 0.5, k: int = 10) -> list[dict]:
        """Maximal Marginal Relevance deduplication using Jaccard similarity."""
        if len(ideas) <= k:
            return ideas

        selected = []
        remaining = list(ideas)
        while remaining and len(selected) < k:
            best_idx = 0
            best_score = -float("inf")
            for i, idea in enumerate(remaining):
                relevance = idea.get("overall_score", 0.5)
                max_sim = 0.0
                for sel in selected:
                    words_a = set(idea.get("idea_text", "").lower().split())
                    words_b = set(sel.get("idea_text", "").lower().split())
                    if words_a and words_b:
                        sim = len(words_a & words_b) / len(words_a | words_b)
                        max_sim = max(max_sim, sim)
                mmr = lambda_param * relevance - (1 - lambda_param) * max_sim
                if mmr > best_score:
                    best_score = mmr
                    best_idx = i
            selected.append(remaining.pop(best_idx))
        return selected

    def _apply_belief_weighting(self, ideas: list[dict]) -> list[dict]:
        """Apply belief-based ranking boost to ideas using two-stage matching.

        Stage 1: Keyword pre-filter (2+ word overlap) to identify candidates.
        Stage 2: LLM batch classification of (idea, belief) pairs into
                 addresses_directly (+0.15), tangentially_related (+0.05), unrelated (0).
        """
        if not self._get_conn:
            return ideas

        try:
            from reading_app.db import get_low_confidence_beliefs
            open_beliefs = get_low_confidence_beliefs(threshold=0.5)
        except Exception:
            logger.debug("Could not load beliefs for weighting", exc_info=True)
            return ideas

        if not open_beliefs:
            return ideas

        STOP_WORDS = {"the", "a", "an", "is", "are", "was", "were", "will", "be",
                       "that", "this", "it", "in", "on", "of", "for", "to", "and",
                       "or", "not", "with", "from", "by", "at", "as", "but", "can",
                       "do", "does", "has", "have", "had", "been", "being", "would",
                       "could", "should", "may", "might", "more", "most", "than"}

        # Stage 1: Keyword pre-filter (lowered threshold to 2 words)
        belief_words = {}
        for i, b in enumerate(open_beliefs):
            bid = b.get("id", f"_belief_{i}")
            words = set(b.get("claim", "").lower().split()) - STOP_WORDS
            belief_words[bid] = words
            b["_bid"] = bid  # stash for later lookup

        candidates = []  # (idea_idx, belief_id) pairs that pass pre-filter
        for idx, idea in enumerate(ideas):
            idea_words = set(idea.get("idea_text", "").lower().split()) - STOP_WORDS
            for b in open_beliefs:
                bid = b["_bid"]
                overlap = len(idea_words & belief_words[bid])
                if overlap >= 2:
                    candidates.append((idx, bid))

        if not candidates:
            return ideas

        # Stage 2: LLM batch classification (free on Max)
        belief_map = {b["_bid"]: b["claim"] for b in open_beliefs}
        pairs_text = "\n".join(
            f"Pair {i+1}: IDEA: \"{ideas[idx].get('idea_text', '')[:200]}\" | "
            f"BELIEF: \"{belief_map[bid][:200]}\""
            for i, (idx, bid) in enumerate(candidates[:30])  # Cap at 30 pairs
        )

        classify_prompt = f"""Classify each (idea, belief) pair. For each pair, output ONE of:
- "addresses_directly" — the idea meaningfully addresses the belief's open question
- "tangentially_related" — the idea touches on the belief's domain but doesn't directly address it
- "unrelated" — false positive from keyword matching

Return JSON array:
```json
[{{"pair": 1, "classification": "addresses_directly"}}, ...]
```

{pairs_text}"""

        try:
            result = self.executor.run_raw(
                classify_prompt,
                session_id="belief_classify",
                timeout=60,
            )

            # Parse classifications
            import re as _re
            json_match = _re.search(r"\[.*\]", result.text, _re.DOTALL)
            if json_match:
                classifications = json.loads(json_match.group(0))
            else:
                classifications = []

            # Apply boosts based on classifications
            for cls in classifications:
                pair_idx = cls.get("pair", 0) - 1
                if 0 <= pair_idx < len(candidates):
                    idea_idx, _ = candidates[pair_idx]
                    classification = cls.get("classification", "unrelated")
                    current_score = ideas[idea_idx].get("overall_score", 0.5)
                    if classification == "addresses_directly":
                        ideas[idea_idx]["overall_score"] = min(1.0, current_score + 0.15)
                        ideas[idea_idx]["belief_boost_applied"] = True
                        ideas[idea_idx]["belief_boost_type"] = "direct"
                    elif classification == "tangentially_related":
                        ideas[idea_idx]["overall_score"] = min(1.0, current_score + 0.05)
                        ideas[idea_idx]["belief_boost_applied"] = True
                        ideas[idea_idx]["belief_boost_type"] = "tangential"

        except Exception:
            # Fall back to keyword-only boost on LLM failure
            logger.debug("LLM belief classification failed, falling back to keyword matching", exc_info=True)
            boosted = set()
            for idx, _bid in candidates:
                if idx not in boosted:
                    current_score = ideas[idx].get("overall_score", 0.5)
                    ideas[idx]["overall_score"] = min(1.0, current_score + 0.1)
                    ideas[idx]["belief_boost_applied"] = True
                    ideas[idx]["belief_boost_type"] = "keyword_fallback"
                    boosted.add(idx)

        return ideas

    def _persist_ideas(self, ideas: list[dict], source_id: str | None):
        """Persist ideas to the database with tournament metadata.

        Winning ideas (overall_score >= 0.7) are also written back as claims
        with provenance_type='generated' so they become retrievable via
        hybrid_retrieve, closing the feedback loop between generation and retrieval.
        """
        if not self._get_conn:
            return
        try:
            from reading_app.db import insert_idea
            from ulid import ULID
            ideas_as_claims = []
            for idea in ideas:
                # Skip ideas with effectively zero scores (scoring failures)
                score = idea.get("overall_score") or 0
                if score < 0.1:
                    continue
                idea_id = idea.get("id") or f"idea_{ULID()}"
                tournament_meta = idea.get("tournament_metadata", {})
                generation_context = {
                    "source_id": source_id,
                    "tournament": True,
                    "tournament_metadata": tournament_meta,
                }
                insert_idea(
                    id=idea_id,
                    idea_text=idea.get("idea_text", ""),
                    idea_type=idea.get("idea_type"),
                    grounding=idea.get("grounding"),
                    testability=idea.get("testability"),
                    novelty_score=idea.get("novelty_score"),
                    feasibility_score=idea.get("feasibility_score"),
                    impact_score=idea.get("impact_score"),
                    overall_score=idea.get("overall_score"),
                    novelty_check_passed=True,
                    generation_context=generation_context,
                    parent_idea_id=idea.get("parent_idea_id"),
                )
                idea["id"] = idea_id

                # Promote winning ideas to retrievable claims
                score = idea.get("overall_score") or 0
                if score >= 0.7 and source_id:
                    ideas_as_claims.append((idea_id, idea))

            # Batch-embed and persist winning ideas as claims
            if ideas_as_claims:
                self._persist_ideas_as_claims(ideas_as_claims, source_id)

            # Log per-strategy quality metrics
            try:
                from reading_app.quality_store import log_quality_metric
                strategy_stats: dict[str, dict] = {}
                for idea in ideas:
                    strat = (idea.get("tournament_metadata") or {}).get("generation_strategy", "unknown")
                    if strat not in strategy_stats:
                        strategy_stats[strat] = {"ideas_generated": 0, "scores": [], "novelty_passed": 0}
                    strategy_stats[strat]["ideas_generated"] += 1
                    score = idea.get("overall_score") or 0
                    if score >= 0.1:
                        strategy_stats[strat]["scores"].append(score)
                    if idea.get("novelty_check_passed"):
                        strategy_stats[strat]["novelty_passed"] += 1
                for strat, stats in strategy_stats.items():
                    avg_score = sum(stats["scores"]) / len(stats["scores"]) if stats["scores"] else 0
                    n_gen = stats["ideas_generated"]
                    log_quality_metric(
                        "tournament_strategy", "strategy", strat,
                        {
                            "ideas_generated": n_gen,
                            "avg_score": round(avg_score, 3),
                            "novelty_pass_rate": round(stats["novelty_passed"] / n_gen, 3) if n_gen else 0,
                        },
                        aggregate_score=avg_score,
                        skill="reflect",
                    )
            except Exception:
                logger.debug("Failed to log tournament strategy metrics", exc_info=True)

        except Exception:
            logger.error("Failed to persist ideas", exc_info=True)

    def _persist_ideas_as_claims(
        self, ideas_with_ids: list[tuple[str, dict]], source_id: str
    ):
        """Write high-scoring ideas as claims with provenance_type='generated'."""
        try:
            from reading_app.db import insert_claim
            from reading_app.embeddings import embed_batch

            texts = [idea.get("idea_text", "") for _, idea in ideas_with_ids]
            embeddings = embed_batch(texts) if texts else []

            for i, (idea_id, idea) in enumerate(ideas_with_ids):
                grounding = idea.get("grounding")
                if isinstance(grounding, list) and grounding:
                    evidence = "; ".join(
                        g.get("snippet", "") or g.get("key_evidence", "")
                        for g in grounding if isinstance(g, dict)
                    )[:500]
                elif isinstance(grounding, dict):
                    evidence = grounding.get("key_evidence", "")
                else:
                    evidence = str(grounding)[:500] if grounding else ""
                emb = embeddings[i] if i < len(embeddings) and embeddings[i] else None
                insert_claim(
                    id=f"gen_{idea_id}",
                    source_id=source_id,
                    claim_text=idea.get("idea_text", ""),
                    claim_type="generated_idea",
                    section="tournament",
                    confidence=idea.get("overall_score"),
                    evidence_snippet=evidence[:500] if evidence else None,
                    evidence_type="generated",
                    embedding=emb,
                    provenance_type="generated",
                )
            logger.info(
                "Persisted %d ideas as generated claims", len(ideas_with_ids)
            )
        except Exception:
            logger.warning("Failed to persist ideas as claims", exc_info=True)
