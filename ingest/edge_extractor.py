"""Edge extraction: identify relationships between sources.

Uses shared concepts and themes to find candidate source pairs,
then classifies the relationship type via LLM.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Callable

logger = logging.getLogger(__name__)

# Valid edge types from the schema
EDGE_TYPES = ("extends", "supports", "contradicts", "challenges", "applies", "inspires")


def find_candidate_pairs(
    get_conn_fn: Callable,
    min_shared_concepts: int = 2,
) -> list[dict]:
    """Find source pairs that likely have a relationship.

    Returns pairs sharing >= min_shared_concepts concepts OR sharing a theme.
    """
    with get_conn_fn() as conn:
        # Sources sharing concepts
        concept_pairs = conn.execute("""
            SELECT
                sc1.source_id AS source_a,
                sc2.source_id AS source_b,
                count(*) AS shared_concepts,
                array_agg(DISTINCT c.canonical_name) AS concept_names
            FROM source_concepts sc1
            JOIN source_concepts sc2
                ON sc1.concept_id = sc2.concept_id
                AND sc1.source_id < sc2.source_id
            JOIN concepts c ON c.id = sc1.concept_id
            GROUP BY sc1.source_id, sc2.source_id
            HAVING count(*) >= %s
            ORDER BY count(*) DESC
            LIMIT 2000
        """, (min_shared_concepts,)).fetchall()

        # Sources sharing themes
        theme_pairs = conn.execute("""
            SELECT
                st1.source_id AS source_a,
                st2.source_id AS source_b,
                count(*) AS shared_themes,
                array_agg(DISTINCT st1.theme_id) AS theme_ids
            FROM source_themes st1
            JOIN source_themes st2
                ON st1.theme_id = st2.theme_id
                AND st1.source_id < st2.source_id
            WHERE st1.relevance >= 0.5 AND st2.relevance >= 0.5
            GROUP BY st1.source_id, st2.source_id
            HAVING count(*) >= 2
            ORDER BY count(*) DESC
            LIMIT 2000
        """).fetchall()

    # Merge and deduplicate
    seen = set()
    candidates = []
    for row in concept_pairs:
        pair_key = (row["source_a"], row["source_b"])
        if pair_key not in seen:
            seen.add(pair_key)
            candidates.append({
                "source_a": row["source_a"],
                "source_b": row["source_b"],
                "shared_concepts": row["concept_names"],
                "shared_themes": [],
                "score": row["shared_concepts"],
            })

    for row in theme_pairs:
        pair_key = (row["source_a"], row["source_b"])
        if pair_key in seen:
            # Update with theme info
            for c in candidates:
                if c["source_a"] == row["source_a"] and c["source_b"] == row["source_b"]:
                    c["shared_themes"] = row["theme_ids"]
                    c["score"] += row["shared_themes"]
                    break
        else:
            seen.add(pair_key)
            candidates.append({
                "source_a": row["source_a"],
                "source_b": row["source_b"],
                "shared_concepts": [],
                "shared_themes": row["theme_ids"],
                "score": row["shared_themes"],
            })

    # Sort by score (most shared concepts/themes first)
    candidates.sort(key=lambda c: c["score"], reverse=True)
    return candidates


def classify_edge(
    source_a_title: str,
    source_a_summary: str,
    source_b_title: str,
    source_b_summary: str,
    shared_concepts: list[str],
    executor,
    pair_index: int = 0,
) -> dict | None:
    """Use LLM to classify the relationship between two sources.

    Returns dict with edge_type, explanation, confidence, evidence_a, evidence_b,
    or None if no relationship.  Returns ``{"error": ...}`` on CLI/parse failure.
    """
    concepts_str = ", ".join(shared_concepts[:10]) if shared_concepts else "none"

    prompt = f"""Analyze the relationship between these two sources.

## Source A: {source_a_title}
{source_a_summary[:1500]}

## Source B: {source_b_title}
{source_b_summary[:1500]}

## Shared concepts: {concepts_str}

## Task
Classify the primary relationship between Source A and Source B.

Valid relationship types (from A's perspective toward B):
- extends: A builds upon or extends the work in B
- supports: A provides evidence supporting B's claims
- contradicts: A presents findings that contradict B
- challenges: A questions or critiques B's approach/assumptions
- applies: A applies methods or ideas from B to a new domain
- inspires: A draws inspiration from B but in a different direction

If there is no meaningful relationship beyond surface-level topic overlap, respond with: NONE

Otherwise respond with exactly one JSON object:
```json
{{
  "edge_type": "extends|supports|contradicts|challenges|applies|inspires",
  "explanation": "One sentence explaining the relationship",
  "confidence": 0.0-1.0,
  "evidence_a": "Brief quote or paraphrase from Source A that grounds this relationship",
  "evidence_b": "Brief quote or paraphrase from Source B that grounds this relationship"
}}
```"""

    try:
        result = executor.run_raw(
            prompt,
            session_id=f"edge_{pair_index}",
            timeout=90,
        )

        if not result.success:
            return {"error": f"rc={result.return_code}", "stderr": result.stderr[:200]}

        text = result.text.strip()
        if not text:
            return {"error": "empty_response"}

        if "NONE" in text and len(text) < 20:
            return None

        from ingest.json_parser import parse_json_from_llm
        parsed = parse_json_from_llm(text, expect=dict)
        if not parsed or parsed.get("edge_type") not in EDGE_TYPES:
            return None

        return {
            "edge_type": parsed["edge_type"],
            "explanation": parsed.get("explanation", ""),
            "confidence": min(1.0, max(0.0, float(parsed.get("confidence", 0.5)))),
            "evidence_a": parsed.get("evidence_a", ""),
            "evidence_b": parsed.get("evidence_b", ""),
        }
    except Exception:
        logger.debug("Edge classification failed", exc_info=True)
        return {"error": "exception"}


def _salvage_individual_objects(text: str) -> list[dict] | None:
    """Try to extract individual JSON objects when array parsing fails.

    Sometimes the LLM outputs objects separated by newlines or commas
    instead of a proper JSON array.
    """
    results = []
    for m in re.finditer(r'\{[^{}]*"edge_type"[^{}]*\}', text):
        try:
            obj = json.loads(m.group())
            if isinstance(obj, dict) and "pair" in obj:
                results.append(obj)
        except json.JSONDecodeError:
            continue
    return results if results else None


def classify_edge_batch(
    pairs: list[dict],
    executor,
    batch_id: int = 0,
) -> list[dict | None]:
    """Classify up to 5 source pairs in a single CLI invocation.

    Each element in *pairs* must have keys:
        title_a, summary_a, title_b, summary_b, shared_concepts

    Returns a list parallel to *pairs* where each element is:
        - dict with edge_type, explanation, confidence, evidence_a, evidence_b (success)
        - None (no meaningful relationship)
        - {"error": ...} (CLI or parse failure)
    """
    from ingest.json_parser import parse_json_from_llm

    # Build numbered pair descriptions
    pair_blocks = []
    for idx, p in enumerate(pairs, 1):
        concepts_str = ", ".join(p["shared_concepts"][:10]) if p.get("shared_concepts") else "none"
        pair_blocks.append(
            f"### Pair {idx}\n"
            f"**Source A:** {p['title_a']}\n{p['summary_a'][:1200]}\n\n"
            f"**Source B:** {p['title_b']}\n{p['summary_b'][:1200]}\n\n"
            f"**Shared concepts:** {concepts_str}"
        )

    pairs_text = "\n\n".join(pair_blocks)

    prompt = f"""Analyze the relationships between these {len(pairs)} source pairs.

{pairs_text}

## Task
For each pair, classify the primary relationship from Source A's perspective toward B.

Valid relationship types:
- extends: A builds upon or extends the work in B
- supports: A provides evidence supporting B's claims
- contradicts: A presents findings that contradict B
- challenges: A questions or critiques B's approach/assumptions
- applies: A applies methods or ideas from B to a new domain
- inspires: A draws inspiration from B but in a different direction

Respond with a JSON array of {len(pairs)} objects, one per pair in order.
For pairs with no meaningful relationship, use {{"pair": N, "edge_type": "NONE"}}.
For pairs with a relationship:
```json
{{
  "pair": N,
  "edge_type": "extends|supports|contradicts|challenges|applies|inspires",
  "explanation": "One sentence explaining the relationship",
  "confidence": 0.0-1.0,
  "evidence_a": "Brief quote or paraphrase from Source A grounding this relationship",
  "evidence_b": "Brief quote or paraphrase from Source B grounding this relationship"
}}
```

Return ONLY the JSON array, no other text."""

    # Scale timeout with batch size (base 30s + 15s per pair)
    timeout = 30 + 15 * len(pairs)

    session_id = f"edge_batch_{batch_id}"
    try:
        result = executor.run_raw(
            prompt,
            session_id=session_id,
            timeout=timeout,
        )
        executor.cleanup_session(session_id)

        if not result.success:
            error = {"error": f"rc={result.return_code}", "stderr": result.stderr[:200]}
            return [error] * len(pairs)

        text = result.text.strip()
        if not text:
            return [{"error": "empty_response"}] * len(pairs)

        parsed = parse_json_from_llm(text, expect=list)
        if not parsed:
            # Try salvaging individual JSON objects from the text
            parsed = _salvage_individual_objects(text)
        if not parsed:
            return [{"error": "parse_failed"}] * len(pairs)

        # Map pair numbers to results
        results_by_pair: dict[int, dict] = {}
        for item in parsed:
            if not isinstance(item, dict):
                continue
            pair_num = item.get("pair")
            if pair_num is not None:
                results_by_pair[int(pair_num)] = item

        # Build parallel result list
        results = []
        for idx in range(1, len(pairs) + 1):
            item = results_by_pair.get(idx)
            if not item or item.get("edge_type") == "NONE":
                results.append(None)
            elif item.get("edge_type") in EDGE_TYPES:
                results.append({
                    "edge_type": item["edge_type"],
                    "explanation": item.get("explanation", ""),
                    "confidence": min(1.0, max(0.0, float(item.get("confidence", 0.5)))),
                    "evidence_a": item.get("evidence_a", ""),
                    "evidence_b": item.get("evidence_b", ""),
                })
            else:
                results.append(None)

        # Pad if LLM returned fewer items than expected
        while len(results) < len(pairs):
            results.append({"error": "missing_from_batch"})

        return results

    except Exception:
        logger.debug("Batch edge classification failed", exc_info=True)
        return [{"error": "exception"}] * len(pairs)


def get_source_summary(source_id: str, library_path) -> str:
    """Load source summary for edge classification context."""
    summary_path = library_path / source_id / "deep_summary.md"
    if summary_path.exists():
        try:
            return summary_path.read_text(encoding="utf-8")[:2000]
        except Exception:
            pass
    return ""
