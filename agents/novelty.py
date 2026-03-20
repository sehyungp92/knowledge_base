"""NoveltyGate: cosine similarity hard gate for idea deduplication.

Three-stage filtering:
1. Embedding cosine similarity (primary) — catches paraphrases and near-duplicates.
2. Jaccard word-overlap (fallback) — when embeddings unavailable.
3. LLM-judged trivial implication check — catches intellectually obvious ideas
   that are semantically distant from existing ideas but follow as direct
   implications of concepts already in the library.
"""

from __future__ import annotations

import json
import logging
import math
import re

logger = logging.getLogger(__name__)

NOVELTY_THRESHOLD = 0.85


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class NoveltyGate:
    """Hard gate: rejects ideas too similar to existing ones."""

    def __init__(self, threshold: float = NOVELTY_THRESHOLD):
        self.threshold = threshold

    def check(self, idea_text: str, existing_texts: list[str]) -> tuple[bool, float, str | None]:
        """Check novelty using text overlap (fallback when no embeddings).

        Returns: (passes, max_similarity, most_similar_text)
        """
        max_sim = 0.0
        most_similar = None
        idea_words = set(idea_text.lower().split())

        for existing in existing_texts:
            existing_words = set(existing.lower().split())
            if not idea_words or not existing_words:
                continue
            jaccard = len(idea_words & existing_words) / len(idea_words | existing_words)
            if jaccard > max_sim:
                max_sim = jaccard
                most_similar = existing

        passes = max_sim < self.threshold
        return passes, max_sim, most_similar

    def check_with_embed(
        self,
        idea_embedding: list[float],
        existing_embeddings: list[tuple[str, list[float]]],
    ) -> tuple[bool, float, str | None]:
        """Check novelty using pre-computed embeddings.

        Args:
            idea_embedding: Embedding of the new idea
            existing_embeddings: List of (idea_text, embedding) tuples

        Returns: (passes, max_similarity, most_similar_text)
        """
        max_sim = 0.0
        most_similar = None

        for text, emb in existing_embeddings:
            sim = cosine_similarity(idea_embedding, emb)
            if sim > max_sim:
                max_sim = sim
                most_similar = text

        passes = max_sim < self.threshold
        return passes, max_sim, most_similar

    def filter_batch(
        self,
        ideas: list[dict],
        existing_texts: list[str],
        executor=None,
        library_claims: list[str] | None = None,
    ) -> list[dict]:
        """Filter a batch of ideas, keeping only novel ones.

        Three stages:
        1. Embedding-based cosine similarity (or Jaccard fallback)
        2. LLM-judged trivial implication filter (if executor provided)

        Args:
            ideas: Candidate ideas with 'idea_text' key.
            existing_texts: Texts of existing ideas for dedup.
            executor: Optional ClaudeExecutor for LLM trivial-implication check.
            library_claims: Optional list of claim texts from the library
                for the LLM to judge obviousness against.
        """
        try:
            stage1 = self._filter_batch_embedded(ideas, existing_texts)
        except Exception:
            logger.warning("Embedding-based novelty gate failed, falling back to Jaccard", exc_info=True)
            stage1 = self._filter_batch_jaccard(ideas, existing_texts)

        if not stage1 or not executor:
            return stage1

        # Stage 2: LLM trivial-implication filter
        try:
            return self._filter_trivial_implications(stage1, executor, library_claims or existing_texts)
        except Exception:
            logger.warning("LLM trivial-implication filter failed, returning stage-1 results", exc_info=True)
            return stage1

    def _filter_batch_embedded(
        self,
        ideas: list[dict],
        existing_texts: list[str],
    ) -> list[dict]:
        """Embedding-based novelty filtering."""
        from reading_app.embeddings import embed_batch

        idea_texts = [idea.get("idea_text", "") for idea in ideas]
        all_texts = list(existing_texts) + idea_texts
        all_embeddings = embed_batch(all_texts)

        n_existing = len(existing_texts)
        existing_embs = [
            (text, emb)
            for text, emb in zip(existing_texts, all_embeddings[:n_existing])
            if emb is not None
        ]
        idea_embs = all_embeddings[n_existing:]

        if not any(e is not None for e in idea_embs):
            raise RuntimeError("All idea embeddings failed")

        novel = []
        for idea, emb in zip(ideas, idea_embs):
            text = idea.get("idea_text", "")
            if emb is None:
                # Can't embed this idea — fall back to Jaccard for it
                passes, sim, _ = self.check(text, [t for t, _ in existing_embs])
            else:
                passes, sim, _ = self.check_with_embed(emb, existing_embs)

            if passes:
                idea["novelty_score"] = 1.0 - sim
                novel.append(idea)
                existing_embs.append((text, emb))
            else:
                logger.info("Idea rejected (sim=%.2f): %s", sim, text[:80])
        return novel

    def _filter_trivial_implications(
        self,
        ideas: list[dict],
        executor,
        reference_texts: list[str],
    ) -> list[dict]:
        """LLM-judged filter: reject ideas that are trivially obvious implications.

        For each batch of ideas, ask the LLM whether each follows as a direct,
        trivially obvious implication from concepts already in the library.
        """
        if not ideas:
            return ideas

        # Build concise reference context (top claims the LLM can judge against)
        ref_sample = reference_texts[:30]
        ref_block = "\n".join(f"- {t[:200]}" for t in ref_sample)

        ideas_block = "\n".join(
            f"{i+1}. {idea.get('idea_text', '')[:300]}"
            for i, idea in enumerate(ideas)
        )

        prompt = f"""You are a novelty judge for a research idea tournament.

## Existing knowledge in the library
{ref_block}

## Candidate ideas
{ideas_block}

## Task
For each candidate idea, determine whether it is a **trivially obvious implication** \
of the existing knowledge above — something anyone reading those claims would \
immediately infer without creative thought.

Return ONLY a JSON array. For each idea, output:
- "id": the idea number (1-indexed)
- "trivial": true if the idea is an obvious/direct implication, false if it requires genuine creative connection
- "reason": brief explanation (1 sentence)

```json
[{{"id": 1, "trivial": false, "reason": "Connects two unrelated domains in a non-obvious way"}}]
```
"""

        result = executor.run_raw(
            prompt,
            session_id="novelty_trivial_check",
            timeout=90,
        )

        # Parse response
        json_match = re.search(r"\[.*\]", result.text, re.DOTALL)
        if not json_match:
            logger.warning("Trivial-implication filter: no JSON parsed, keeping all ideas")
            return ideas

        try:
            judgments = json.loads(json_match.group(0))
        except json.JSONDecodeError:
            logger.warning("Trivial-implication filter: JSON parse failed, keeping all ideas")
            return ideas

        trivial_ids = set()
        for j in judgments:
            if j.get("trivial") is True:
                trivial_ids.add(j.get("id", 0))

        novel = []
        for i, idea in enumerate(ideas):
            if (i + 1) in trivial_ids:
                reason = next(
                    (j.get("reason", "") for j in judgments if j.get("id") == i + 1),
                    "",
                )
                logger.info(
                    "Idea rejected (trivial implication): %s — %s",
                    idea.get("idea_text", "")[:80],
                    reason,
                )
                idea["novelty_trivial_rejected"] = True
                idea["novelty_trivial_reason"] = reason
            else:
                novel.append(idea)

        logger.info(
            "Trivial-implication filter: %d/%d ideas passed",
            len(novel), len(ideas),
        )
        return novel

    def _filter_batch_jaccard(
        self,
        ideas: list[dict],
        existing_texts: list[str],
    ) -> list[dict]:
        """Jaccard word-overlap novelty filtering (fallback)."""
        novel = []
        all_texts = list(existing_texts)
        for idea in ideas:
            text = idea.get("idea_text", "")
            passes, sim, _ = self.check(text, all_texts)
            if passes:
                idea["novelty_score"] = 1.0 - sim
                novel.append(idea)
                all_texts.append(text)
            else:
                logger.info("Idea rejected (sim=%.2f): %s", sim, text[:80])
        return novel
