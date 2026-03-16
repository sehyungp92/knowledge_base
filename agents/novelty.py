"""NoveltyGate: cosine similarity hard gate for idea deduplication."""

from __future__ import annotations

import logging
import math

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
    ) -> list[dict]:
        """Filter a batch of ideas, keeping only novel ones.

        Uses embedding-based cosine similarity when available (more accurate
        semantic dedup), falling back to Jaccard word overlap if embeddings
        fail.
        """
        try:
            return self._filter_batch_embedded(ideas, existing_texts)
        except Exception:
            logger.warning("Embedding-based novelty gate failed, falling back to Jaccard", exc_info=True)
            return self._filter_batch_jaccard(ideas, existing_texts)

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
