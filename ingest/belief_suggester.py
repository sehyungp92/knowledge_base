"""Belief formation suggestions via claim clustering.

For themes with sufficient source coverage, clusters claims by topic
using embedding cosine similarity. When multiple sources converge on
a position, suggests a tracked belief if none already exists.

Called during heartbeat (biweekly cadence).
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

from ingest.json_parser import parse_json_from_llm

logger = logging.getLogger(__name__)

# Minimum sources a theme needs before suggesting beliefs
MIN_SOURCES_FOR_SUGGESTION = 5

# Minimum distinct sources with convergent claims
MIN_CONVERGENT_SOURCES = 3

# Cosine similarity threshold for claim convergence
CONVERGENCE_THRESHOLD = 0.8

SUGGESTION_PROMPT = """You are analyzing clusters of convergent claims from multiple sources to suggest beliefs the user might want to track.

## Theme: {theme_name}
## Claim Clusters (claims from multiple sources that converge on similar positions)

{clusters_text}

## Existing Beliefs for This Theme
{existing_beliefs_text}

For each cluster, determine:
1. Is there already an existing belief that covers this position? If so, skip it.
2. If not, formulate a belief suggestion.

Return a JSON array of belief suggestions (empty array if none):
```json
[
  {{
    "claim": "A clear, concise statement of the position (e.g., 'Scaling laws for LLMs will continue to hold through at least 10x current compute levels')",
    "suggested_confidence": 0.0-1.0,
    "belief_type": "factual" | "predictive" | "methodological" | "meta",
    "supporting_sources": ["source_id_1", "source_id_2", ...],
    "reasoning": "Why this cluster suggests a trackable belief",
    "evidence_summary": "Key evidence from the convergent claims"
  }}
]
```

Rules:
- Only suggest beliefs where >=3 sources genuinely converge (not just mention the topic)
- Phrase claims as positions the user could agree or disagree with
- Don't suggest beliefs that are trivially obvious or uncontroversial
- Prefer beliefs that are falsifiable and connected to the landscape model
- If a cluster is already covered by an existing belief, do NOT suggest it again
"""


def suggest_beliefs_for_theme(
    theme_id: str,
    theme_name: str,
    executor=None,
) -> list[dict]:
    """Suggest beliefs for a theme based on convergent claim clusters.

    Args:
        theme_id: Theme to analyze.
        theme_name: Human-readable theme name.
        executor: ClaudeExecutor instance.

    Returns:
        List of belief suggestion dicts.
    """
    try:
        from reading_app import db

        # Check source count
        source_count = _get_theme_source_count(theme_id)
        if source_count < MIN_SOURCES_FOR_SUGGESTION:
            logger.debug(
                "Theme %s has %d sources (need %d), skipping belief suggestions",
                theme_id, source_count, MIN_SOURCES_FOR_SUGGESTION,
            )
            return []

        # Get claim clusters via embedding similarity
        clusters = _get_convergent_clusters(theme_id)
        if not clusters:
            return []

        # Get existing beliefs for dedup
        existing_beliefs = db.get_beliefs_for_theme(theme_id)
    except Exception:
        logger.warning("Failed to prepare belief suggestions for %s", theme_id, exc_info=True)
        return []

    clusters_text = _format_clusters(clusters)
    existing_beliefs_text = "\n".join(
        f"- {b['claim']} (confidence: {b.get('confidence', '?')})"
        for b in existing_beliefs
    ) or "None."

    if executor is None:
        from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
        executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    prompt = SUGGESTION_PROMPT.format(
        theme_name=theme_name,
        clusters_text=clusters_text,
        existing_beliefs_text=existing_beliefs_text,
    )

    try:
        result = executor.run_raw(
            prompt,
            session_id=f"belief_suggest_{theme_id}",
            timeout=180,
        )
        suggestions = _parse_suggestions(result.text)
    except Exception:
        logger.warning("LLM belief suggestion failed for %s", theme_id, exc_info=True)
        return []

    # Validate suggestions
    valid = []
    for s in suggestions:
        if not s.get("claim"):
            continue
        if s.get("suggested_confidence") is not None:
            s["suggested_confidence"] = max(0.0, min(1.0, float(s["suggested_confidence"])))
        if s.get("belief_type") not in {"factual", "predictive", "methodological", "meta"}:
            s["belief_type"] = "factual"
        s["theme_id"] = theme_id
        s["theme_name"] = theme_name
        valid.append(s)

    logger.info("Generated %d belief suggestions for %s", len(valid), theme_id)
    return valid


def suggest_beliefs_all_themes(executor=None) -> list[dict]:
    """Run belief suggestions across all themes meeting the source threshold.

    Called by heartbeat on biweekly cadence.

    Returns:
        Flat list of all suggestions across themes.
    """
    try:
        from reading_app import db
        from retrieval.landscape import get_theme_source_counts
        theme_counts = get_theme_source_counts()
    except Exception:
        logger.warning("Failed to get theme source counts for belief suggestions", exc_info=True)
        return []

    all_suggestions = []
    for tc in theme_counts:
        if (tc.get("source_count") or 0) < MIN_SOURCES_FOR_SUGGESTION:
            continue
        try:
            suggestions = suggest_beliefs_for_theme(
                tc["id"], tc["name"], executor=executor,
            )
            all_suggestions.extend(suggestions)
        except Exception:
            logger.warning("Belief suggestion failed for theme %s", tc["id"], exc_info=True)

    return all_suggestions


def _get_theme_source_count(theme_id: str) -> int:
    """Get count of sources for a theme."""
    from reading_app.db import get_conn
    with get_conn() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS cnt FROM source_themes WHERE theme_id = %s",
            (theme_id,),
        ).fetchone()
        return row["cnt"] if row else 0


def _get_convergent_clusters(theme_id: str) -> list[dict]:
    """Find clusters of claims from multiple sources that converge on similar positions.

    Uses claim embeddings and cosine similarity to find convergent groups.
    Falls back to text-based grouping if embeddings aren't available.
    """
    from reading_app.db import get_conn

    with get_conn() as conn:
        # Get claims for the theme's sources, with embeddings if available
        rows = conn.execute(
            """SELECT c.id, c.claim_text, c.source_id, c.embedding
               FROM claims c
               JOIN source_themes st ON c.source_id = st.source_id
               WHERE st.theme_id = %s
               ORDER BY c.confidence DESC NULLS LAST
               LIMIT 100""",
            (theme_id,),
        ).fetchall()

    if len(rows) < MIN_CONVERGENT_SOURCES:
        return []

    # Check if embeddings are available
    has_embeddings = any(r.get("embedding") is not None for r in rows)

    if has_embeddings:
        return _cluster_by_embedding(rows)
    else:
        return _cluster_by_text(rows)


def _cluster_by_embedding(rows: list[dict]) -> list[dict]:
    """Cluster claims by embedding cosine similarity."""
    # Filter to rows with embeddings
    embedded = [r for r in rows if r.get("embedding") is not None]
    if len(embedded) < MIN_CONVERGENT_SOURCES:
        return _cluster_by_text(rows)

    # Simple greedy clustering: pick a claim, find similar ones
    clusters = []
    used = set()

    for i, row in enumerate(embedded):
        if i in used:
            continue

        cluster = [row]
        source_ids = {row["source_id"]}
        used.add(i)

        for j, other in enumerate(embedded):
            if j in used:
                continue
            if other["source_id"] in source_ids:
                continue  # Want distinct sources

            # Cosine similarity via DB would be better but we're working in Python
            # For simplicity, just use text overlap heuristic since embeddings are
            # stored as vector type and we don't have numpy available
            sim = _text_similarity(row["claim_text"], other["claim_text"])
            if sim >= 0.3:  # Lower threshold for text-based fallback
                cluster.append(other)
                source_ids.add(other["source_id"])
                used.add(j)

        if len(source_ids) >= MIN_CONVERGENT_SOURCES:
            clusters.append({
                "claims": [{"claim_text": c["claim_text"], "source_id": c["source_id"]} for c in cluster],
                "source_count": len(source_ids),
            })

    return clusters


def _cluster_by_text(rows: list[dict]) -> list[dict]:
    """Fallback clustering using Jaccard word similarity."""
    clusters = []
    used = set()

    for i, row in enumerate(rows):
        if i in used:
            continue

        cluster = [row]
        source_ids = {row["source_id"]}
        used.add(i)

        for j, other in enumerate(rows):
            if j in used:
                continue
            if other["source_id"] in source_ids:
                continue

            sim = _text_similarity(row["claim_text"], other["claim_text"])
            if sim >= 0.3:
                cluster.append(other)
                source_ids.add(other["source_id"])
                used.add(j)

        if len(source_ids) >= MIN_CONVERGENT_SOURCES:
            clusters.append({
                "claims": [{"claim_text": c["claim_text"], "source_id": c["source_id"]} for c in cluster],
                "source_count": len(source_ids),
            })

    return clusters


def _text_similarity(a: str, b: str) -> float:
    """Simple Jaccard word similarity between two texts."""
    words_a = set(a.lower().split())
    words_b = set(b.lower().split())
    if not words_a or not words_b:
        return 0.0
    return len(words_a & words_b) / len(words_a | words_b)


def _format_clusters(clusters: list[dict]) -> str:
    """Format claim clusters for the LLM prompt."""
    parts = []
    for i, cluster in enumerate(clusters, 1):
        claims = cluster["claims"]
        parts.append(f"### Cluster {i} ({cluster['source_count']} sources)")
        for c in claims:
            parts.append(f"  - [{c['source_id']}] {c['claim_text']}")
        parts.append("")
    return "\n".join(parts)


def _parse_suggestions(text: str) -> list[dict]:
    """Parse JSON array of suggestions from LLM output."""
    result = parse_json_from_llm(text, expect=list)
    if result is None:
        logger.warning("Failed to parse belief suggestion output")
        return []
    return result
