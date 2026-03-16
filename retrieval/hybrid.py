"""Hybrid retrieval: vector + keyword search with RRF fusion, optional MMR and temporal decay."""

from __future__ import annotations

import json
import logging
import math
import re
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# Recommended temporal decay settings by use case.
# Callers should pass temporal_decay=True and half_life_days from these constants.
DECAY_LANDSCAPE = 730.0       # Landscape queries: long half-life, things change slowly
DECAY_ANTICIPATION = 365.0    # Anticipation matching: predictions are time-sensitive
DECAY_DEFAULT = 365.0         # General use
# Note: Reflect/tournament should NOT enable temporal decay — idea generation
# benefits from combining old foundational work with new results.
# User search should default to temporal_decay=False with an opt-in flag.

# Stop words to strip from keyword queries (preserving hyphenated terms)
_STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "dare", "ought",
    "used", "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "as", "into", "through", "during", "before", "after", "above", "below",
    "between", "out", "off", "over", "under", "again", "further", "then",
    "once", "here", "there", "when", "where", "why", "how", "all", "each",
    "every", "both", "few", "more", "most", "other", "some", "such", "no",
    "nor", "not", "only", "own", "same", "so", "than", "too", "very",
    "and", "but", "if", "or", "because", "until", "while", "about", "what",
    "which", "who", "whom", "this", "that", "these", "those", "i", "me",
    "my", "we", "our", "you", "your", "he", "him", "his", "she", "her",
    "it", "its", "they", "them", "their",
}


def _expand_query(query: str) -> str:
    """Strip stop words, preserve hyphenated terms like GPT-4, LLaMA-3."""
    tokens = query.split()
    kept = []
    for t in tokens:
        # Preserve hyphenated terms
        if "-" in t and not t.startswith("-"):
            kept.append(t)
        elif t.lower() not in _STOP_WORDS:
            kept.append(t)
    return " ".join(kept) if kept else query


def _jaccard_similarity(text_a: str, text_b: str) -> float:
    """Word-level Jaccard similarity."""
    words_a = set(text_a.lower().split())
    words_b = set(text_b.lower().split())
    if not words_a or not words_b:
        return 0.0
    return len(words_a & words_b) / len(words_a | words_b)


def hybrid_retrieve(
    query: str,
    get_conn_fn,
    embedding: list[float] | None = None,
    k: int = 10,
    source_type: str | None = None,
    mmr: bool = False,
    mmr_lambda: float = 0.7,
    temporal_decay: bool = False,
    half_life_days: float = 365.0,
    min_rrf_score: float = 0.005,
) -> list[dict]:
    """Hybrid retrieval combining vector search + keyword search with RRF fusion.

    Args:
        query: Search query text
        get_conn_fn: Callable returning context manager for DB connection
        embedding: Pre-computed query embedding (if None, keyword-only)
        k: Number of results to return
        source_type: Optional filter by source type
        mmr: Whether to apply MMR reranking for diversity
        mmr_lambda: Balance between relevance and diversity (0-1)
        temporal_decay: Whether to apply recency bias
        half_life_days: Half-life for temporal decay in days
        min_rrf_score: Minimum RRF score threshold

    Returns:
        List of claim dicts with scores
    """
    pool_size = k * 4
    vector_results = []
    keyword_results = []

    # Build filter clause
    filters = []
    filter_params = []
    if source_type:
        filters.append("s.source_type = %s")
        filter_params.append(source_type)
    filter_clause = " AND ".join(filters) if filters else "TRUE"

    with get_conn_fn() as conn:
        # Stage 1: Vector search
        if embedding:
            emb_str = str(embedding)
            query_params = [emb_str] + filter_params + [emb_str, pool_size]
            vector_results = conn.execute(f"""
                SELECT c.id, c.claim_text, c.source_id, c.section,
                       c.evidence_snippet, c.confidence AS claim_confidence,
                       c.provenance_type,
                       s.title AS source_title, s.published_at,
                       1 - (c.embedding <=> %s::vector) AS score
                FROM claims c
                JOIN sources s ON c.source_id = s.id
                WHERE c.embedding IS NOT NULL AND {filter_clause}
                ORDER BY c.embedding <=> %s::vector
                LIMIT %s
            """, query_params).fetchall()

        # Stage 2: Keyword search
        kw_query = _expand_query(query)
        if kw_query.strip():
            kw_params = [kw_query] + filter_params + [kw_query, pool_size]
            keyword_results = conn.execute(f"""
                SELECT c.id, c.claim_text, c.source_id, c.section,
                       c.evidence_snippet, c.confidence AS claim_confidence,
                       c.provenance_type,
                       s.title AS source_title, s.published_at,
                       ts_rank_cd(c.fts_vector, websearch_to_tsquery('english', %s)) AS score
                FROM claims c
                JOIN sources s ON c.source_id = s.id
                WHERE c.fts_vector @@ websearch_to_tsquery('english', %s)
                  AND {filter_clause}
                LIMIT %s
            """, kw_params).fetchall()

            # Fallback to OR if AND returned nothing and query has multiple words
            if not keyword_results and " " in kw_query:
                or_terms = " OR ".join(kw_query.split())
                or_params = [or_terms] + filter_params + [or_terms, pool_size]
                keyword_results = conn.execute(f"""
                    SELECT c.id, c.claim_text, c.source_id, c.section,
                           c.evidence_snippet, c.confidence AS claim_confidence,
                           c.provenance_type,
                           s.title AS source_title, s.published_at,
                           ts_rank_cd(c.fts_vector, websearch_to_tsquery('english', %s)) AS score
                    FROM claims c
                    JOIN sources s ON c.source_id = s.id
                    WHERE c.fts_vector @@ websearch_to_tsquery('english', %s)
                      AND {filter_clause}
                    LIMIT %s
                """, or_params).fetchall()

    # Stage 3: RRF fusion
    scores: dict[str, float] = {}
    claim_data: dict[str, dict] = {}
    rrf_k = 60

    for rank, row in enumerate(vector_results):
        cid = row["id"]
        scores[cid] = scores.get(cid, 0) + 1.0 / (rank + rrf_k)
        claim_data[cid] = dict(row)

    for rank, row in enumerate(keyword_results):
        cid = row["id"]
        scores[cid] = scores.get(cid, 0) + 1.0 / (rank + rrf_k)
        if cid not in claim_data:
            claim_data[cid] = dict(row)

    # Stage 3b: Provenance weighting — primary sources rank higher
    # Only demote generated/synthesis claims; user-enriched claims are kept at full weight
    _demoted_provenance = {"generated", "synthesis"}
    for cid in scores:
        prov = claim_data[cid].get("provenance_type")
        if prov in _demoted_provenance:
            scores[cid] *= 0.7

    # Filter by min score
    scored = [(cid, score) for cid, score in scores.items() if score >= min_rrf_score]
    scored.sort(key=lambda x: -x[1])

    # Stage 4: Temporal decay (optional)
    if temporal_decay:
        now = datetime.now(timezone.utc)
        decayed = []
        for cid, score in scored:
            pub = claim_data[cid].get("published_at")
            if pub and isinstance(pub, datetime):
                age_days = (now - pub.replace(tzinfo=timezone.utc)).days
                decay = math.exp(-math.log(2) / half_life_days * age_days)
                score *= decay
            decayed.append((cid, score))
        scored = sorted(decayed, key=lambda x: -x[1])

    # Stage 5: MMR reranking (optional)
    if mmr and len(scored) > k:
        selected = []
        remaining = list(scored)
        while remaining and len(selected) < k:
            best_idx = 0
            best_score = -float("inf")
            for i, (cid, rrf_score) in enumerate(remaining):
                # Max similarity to already-selected
                max_sim = 0.0
                for sel_cid, _ in selected:
                    sim = _jaccard_similarity(
                        claim_data[cid]["claim_text"],
                        claim_data[sel_cid]["claim_text"],
                    )
                    max_sim = max(max_sim, sim)
                mmr_score = mmr_lambda * rrf_score - (1 - mmr_lambda) * max_sim
                if mmr_score > best_score:
                    best_score = mmr_score
                    best_idx = i
            selected.append(remaining.pop(best_idx))
        scored = selected

    # Build results
    results = []
    for cid, score in scored[:k]:
        data = claim_data[cid]
        data["rrf_score"] = score
        results.append(data)

    return results


def decompose_and_retrieve(
    query: str,
    get_conn_fn,
    executor,
    embedding: list[float] | None = None,
    k: int = 15,
    max_sub_queries: int = 4,
) -> list[dict]:
    """Decompose a complex query into sub-queries and merge results via RRF.

    1. LLM decomposes the query into 2-4 focused sub-queries
    2. hybrid_retrieve() runs for each sub-query in parallel
    3. Results are merged via a second RRF pass across all sub-query result sets

    Falls back to plain hybrid_retrieve() on decomposition failure.
    """
    from concurrent.futures import ThreadPoolExecutor

    # Step 1: Decompose query via LLM
    sub_queries = _decompose_query(query, executor, max_sub_queries)
    if not sub_queries or len(sub_queries) < 2:
        # Decomposition failed or trivial — fall back to direct retrieval
        return hybrid_retrieve(query, get_conn_fn, embedding=embedding, k=k, mmr=True)

    logger.info("Decomposed query into %d sub-queries: %s", len(sub_queries), sub_queries)

    # Step 2: Run hybrid_retrieve for each sub-query in parallel
    sub_results: list[list[dict]] = []

    def _retrieve_sub(sq: str) -> list[dict]:
        # Generate sub-query embedding
        sub_emb = None
        try:
            from reading_app.embeddings import embed_batch
            sub_emb = embed_batch([sq])[0]
        except Exception:
            pass
        return hybrid_retrieve(sq, get_conn_fn, embedding=sub_emb, k=k)

    with ThreadPoolExecutor(max_workers=min(len(sub_queries), 4)) as pool:
        futures = [pool.submit(_retrieve_sub, sq) for sq in sub_queries]
        for future in futures:
            try:
                sub_results.append(future.result())
            except Exception:
                logger.debug("sub-query retrieval failed", exc_info=True)

    if not sub_results:
        return hybrid_retrieve(query, get_conn_fn, embedding=embedding, k=k, mmr=True)

    # Step 3: Merge via second RRF pass
    merged_scores: dict[str, float] = {}
    merged_data: dict[str, dict] = {}
    rrf_k = 60

    for result_set in sub_results:
        for rank, claim in enumerate(result_set):
            cid = claim["id"]
            merged_scores[cid] = merged_scores.get(cid, 0) + 1.0 / (rank + rrf_k)
            if cid not in merged_data:
                merged_data[cid] = claim

    scored = sorted(merged_scores.items(), key=lambda x: -x[1])

    results = []
    for cid, score in scored[:k]:
        data = merged_data[cid]
        data["rrf_score"] = score
        results.append(data)

    return results


def _decompose_query(query: str, executor, max_sub_queries: int = 4) -> list[str]:
    """Use LLM to decompose a complex query into focused sub-queries."""
    prompt = f"""Decompose this complex research question into {max_sub_queries} focused sub-questions
that together cover all facets of the original question.

Question: {query}

Return ONLY a JSON array of strings, no other text.
Example: ["What are the current capabilities of X?", "What limitations does X face?"]"""

    try:
        result = executor.run_raw(prompt, session_id="query_decompose", timeout=30)
        if not result.text:
            return []
        json_match = re.search(r"\[.*\]", result.text, re.DOTALL)
        if json_match:
            sub_queries = json.loads(json_match.group(0))
            if isinstance(sub_queries, list) and all(isinstance(s, str) for s in sub_queries):
                return sub_queries[:max_sub_queries]
    except Exception:
        logger.debug("query decomposition failed", exc_info=True)
    return []
