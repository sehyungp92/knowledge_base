"""Claim/concept extraction with evidence tracing via Claude CLI."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from ingest.section_slicer import budget_for_source_type, prioritized_slice, timeout_for_text

logger = logging.getLogger(__name__)


def extract_claims(
    source_id: str,
    clean_text: str,
    source_type: str,
    executor=None,
    library_path: Path | None = None,
    budget: int | None = None,
    themes: list[dict] | None = None,
) -> dict:
    """Extract claims, concepts, and methods from clean text.

    Uses Claude CLI subprocess via executor for extraction.
    Returns dict with claims, concepts, and methods lists.

    Args:
        themes: Optional list of {theme_id, relevance} dicts from theme
                classification. When provided, guides extraction toward
                the most relevant domains.
    """
    # Resolve budget from source_type if not provided
    if budget is None:
        budget = budget_for_source_type(source_type)

    # For very long text, use chunked parallel extraction
    if len(clean_text) > 2 * budget:
        from ingest.chunked_extractor import chunked_extract_claims
        logger.info("Text exceeds 2x budget (%d > %d), using chunked extraction", len(clean_text), 2 * budget)
        return chunked_extract_claims(
            source_id, clean_text, source_type, executor,
            library_path=library_path, budget=budget,
            themes=themes,
        )

    # Section-aware budgeting
    sliced_text = prioritized_slice(clean_text, budget=budget)
    dynamic_timeout = timeout_for_text(len(sliced_text))

    # Build theme context if available
    theme_context = ""
    if themes:
        theme_ids = [t["theme_id"] for t in sorted(themes, key=lambda t: t.get("relevance", 0), reverse=True)]
        theme_context = f"\n\nThis source has been classified into these AI themes (by relevance): {', '.join(theme_ids)}. Prioritize extracting claims and concepts most relevant to these themes, but do not ignore significant findings in other areas.\n"

    def _build_prompt(text_slice: str) -> str:
        return f"""Extract structured knowledge from this {source_type}.{theme_context}

## Instructions
1. Extract atomic claims (statements that can be true/false)
2. Extract concepts (methods, datasets, metrics, theories, entities)
3. For each claim, provide a verbatim evidence_snippet from the source text
4. If no evidence can be found for a claim, DO NOT include it
5. For each claim, classify its temporal_scope:
   - "current_state": describes the present state at time of writing
   - "historical": describes a past state (e.g., "in 2022, transformers were limited to...")
   - "future_prediction": predicts a future state (e.g., "will likely enable...")

## Claim Type Guidance
Actively seek all four types -- do not default everything to "finding":
- **finding**: a specific result, measurement, or observation from THIS source
- **limitation**: what the approach CANNOT do or where it struggles. Extract BOTH explicit and implicit signals.
  Explicit: stated in "Limitations", "Future work", caveats, or error analysis sections.
  Implicit (MORE VALUABLE -- look carefully):
  - Performance cliffs: where results degrade or fail (e.g., accuracy drops on longer inputs, out-of-distribution)
  - Controlled conditions: unstated assumptions success depends on (lab vs real-world, specific datasets, hardware)
  - Conspicuous absences: what is NOT discussed but should be (security, fairness, real-world deployment, contamination)
  - Hedging language: "preliminary results suggest...", "under certain conditions...", "we leave X to future work"
  - Scale and cost: training cost, inference latency, data requirements buried in method sections or appendices
  Limitations are the most valuable signal. A good extraction has at least 10% limitation claims.
- **method**: how something was done, architectural choices, training procedures, evaluation protocols
- **assumption**: what must be true for the findings to hold, unstated premises, scope constraints

## Confidence Calibration
Use the FULL range -- a good extraction has meaningful spread, not everything at 0.9+.
- 0.95-1.0: Precise quantitative evidence with specific numbers (e.g., "achieves 94.2% on MMLU"). Reserve strictly for hard measurements.
- 0.85-0.94: Directly stated qualitative claims well-supported by evidence, or quantitative claims with incomplete methodology
- 0.70-0.84: Requires interpretation, or evidence is indirect/analogical. Includes well-grounded qualitative observations.
- 0.50-0.69: Author opinion, hedged language ("may", "could", "suggests"), extrapolation, or implicit signals inferred from context
- Below 0.50: Contradicted by other evidence, highly uncertain, or unsubstantiated

## Quality Filter
Only extract claims that represent THIS SOURCE's contribution. Skip:
- Background knowledge or textbook definitions restated for context (BUT keep limitations that constrain this work -- e.g., "current systems still require X" is a valid limitation even if commonly known)
- Autobiographical trivia unrelated to the technical content
- Generic truisms or unfalsifiable opinions

## Source Text
{text_slice}

## Output Format
Return a JSON object with this structure:
```json
{{{{
  "claims": [
    {{{{
      "claim_text": "...",
      "claim_type": "finding|method|limitation|assumption",
      "section": "...",
      "confidence": 0.0-1.0,
      "evidence_snippet": "exact quote from text",
      "evidence_location": "section name or page",
      "evidence_type": "quote|table|figure|citation",
      "temporal_scope": "current_state|historical|future_prediction"
    }}}}
  ],
  "concepts": [
    {{{{
      "canonical_name": "...",
      "concept_type": "method|dataset|metric|theory|entity",
      "description": "...",
      "aliases": ["..."]
    }}}}
  ]
}}}}
```

Return ONLY the JSON object, no other text."""

    if executor is None:
        logger.warning("No executor provided, returning empty extractions")
        return {"claims": [], "concepts": []}

    prompt = _build_prompt(sliced_text)
    result = executor.run_raw(prompt, session_id=f"extract_{source_id}", timeout=dynamic_timeout)

    # Timeout fallback: retry with halved budget to prevent silent data loss
    if result.is_timeout:
        reduced_budget = budget // 2
        logger.warning(
            "Claim extraction timed out for %s, retrying with reduced budget (%d -> %d)",
            source_id, budget, reduced_budget,
        )
        sliced_text = prioritized_slice(clean_text, budget=reduced_budget)
        dynamic_timeout = timeout_for_text(len(sliced_text))
        prompt = _build_prompt(sliced_text)
        result = executor.run_raw(prompt, session_id=f"extract_{source_id}_retry", timeout=dynamic_timeout)

    extractions = _parse_extractions(result.text)

    # Validate evidence snippets exist in source text
    extractions["claims"] = validate_claims_evidence(
        extractions.get("claims", []), clean_text, source_id,
    )

    # Save extractions to library
    if library_path:
        extractions_path = library_path / source_id / "extractions.json"
        if extractions_path.parent.exists():
            extractions_path.write_text(
                json.dumps(extractions, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

    return extractions


def _parse_extractions(text: str) -> dict:
    """Parse extraction output, handling code blocks and embedded JSON."""
    if not text:
        return {"claims": [], "concepts": []}

    # Strip code block markers
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = lines[1:]  # Remove opening ```json
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines)

    # Find JSON object
    try:
        return _normalize_extractions(json.loads(cleaned))
    except json.JSONDecodeError:
        pass

    # Try to find embedded JSON object
    start = cleaned.find("{")
    if start >= 0:
        depth = 0
        for i in range(start, len(cleaned)):
            if cleaned[i] == "{":
                depth += 1
            elif cleaned[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return _normalize_extractions(json.loads(cleaned[start:i + 1]))
                    except json.JSONDecodeError:
                        break

    logger.warning(
        "Could not parse extractions output (len=%d, has_json_start=%s, has_codeblock=%s): %.500s",
        len(text), cleaned.startswith("{"), "```" in text, text[:500],
    )
    return {"claims": [], "concepts": []}


def _normalize_extractions(payload: object) -> dict:
    """Normalize extractor output into a stable claims/concepts shape."""
    if isinstance(payload, dict):
        claims = payload.get("claims", [])
        concepts = payload.get("concepts", [])
        return {
            "claims": claims if isinstance(claims, list) else [],
            "concepts": concepts if isinstance(concepts, list) else [],
        }

    if isinstance(payload, list):
        dict_items = [item for item in payload if isinstance(item, dict)]
        if any("claim_text" in item for item in dict_items):
            return {"claims": dict_items, "concepts": []}
        if any("canonical_name" in item for item in dict_items):
            return {"claims": [], "concepts": dict_items}

    logger.warning("Extraction payload was not a claims/concepts object")
    return {"claims": [], "concepts": []}


def _validate_evidence(snippet: str, source_text: str, relaxed: bool = False) -> bool:
    """Check that evidence snippet exists in source text.

    Uses fuzzy matching: checks if a substantial portion of the snippet
    words appear in sequence in the source.

    When relaxed=True (for degraded PDF text), lowers the word-order
    threshold and adds character trigram similarity as a fallback.
    """
    # Normalize whitespace
    snippet_lower = " ".join(snippet.lower().split())
    source_lower = " ".join(source_text.lower().split())

    # Exact match
    if snippet_lower in source_lower:
        return True

    # Fuzzy: check if words appear in order
    snippet_words = snippet_lower.split()
    if len(snippet_words) < 3:
        return snippet_lower in source_lower

    # Check for substantial overlap
    match_count = 0
    search_start = 0
    first_match_pos = -1
    last_match_pos = 0
    for word in snippet_words:
        idx = source_lower.find(word, search_start)
        if idx >= 0:
            if first_match_pos < 0:
                first_match_pos = idx
            last_match_pos = idx
            match_count += 1
            search_start = idx + len(word)

    threshold = 0.55 if relaxed else 0.8
    if match_count / len(snippet_words) >= threshold:
        return True

    # Character trigram fallback (only in relaxed mode)
    if relaxed:
        hint = (first_match_pos + last_match_pos) // 2 if first_match_pos >= 0 else 0
        return _trigram_similarity(snippet_lower, source_lower, hint) >= 0.6

    return False


def _trigram_similarity(snippet: str, source: str, hint_pos: int = 0) -> float:
    """Character-level trigram Jaccard similarity over a local window.

    To avoid O(n^2) on large texts, computes trigrams only over a window
    of 3 * len(snippet) chars centered at hint_pos in the source.
    """
    if len(snippet) < 3:
        return 0.0

    snippet_trigrams = set()
    for i in range(len(snippet) - 2):
        snippet_trigrams.add(snippet[i:i + 3])

    if not snippet_trigrams:
        return 0.0

    # Window around the best word-match region (ensure full window at boundaries)
    window_size = len(snippet) * 3
    win_end = min(len(source), hint_pos + window_size // 2)
    win_start = max(0, win_end - window_size)
    window = source[win_start:win_end]

    window_trigrams = set()
    for i in range(len(window) - 2):
        window_trigrams.add(window[i:i + 3])

    if not window_trigrams:
        return 0.0

    intersection = snippet_trigrams & window_trigrams
    union = snippet_trigrams | window_trigrams
    return len(intersection) / len(union)


def validate_claims_evidence(
    claims: list[dict], source_text: str, source_id: str,
) -> list[dict]:
    """Validate evidence snippets, auto-retrying with relaxed matching if all fail."""
    validated = []
    for claim in claims:
        snippet = claim.get("evidence_snippet", "")
        if snippet and _validate_evidence(snippet, source_text):
            validated.append(claim)
        elif not snippet:
            logger.debug("Dropping claim without evidence: %s", claim.get("claim_text", "")[:50])
        else:
            logger.debug("Evidence not found in source: %s", snippet[:50])

    total = len(claims)
    if not validated and total > 0:
        logger.warning(
            "All %d claims failed evidence validation for %s, retrying with relaxed matching",
            total, source_id,
        )
        for claim in claims:
            snippet = claim.get("evidence_snippet", "")
            if snippet and _validate_evidence(snippet, source_text, relaxed=True):
                claim["evidence_validation"] = "relaxed"
                validated.append(claim)
        logger.info("Relaxed validation recovered %d/%d claims for %s",
                     len(validated), total, source_id)

    dropped = total - len(validated)
    if dropped:
        logger.info("Evidence validation for %s: %d/%d kept, %d dropped",
                     source_id, len(validated), total, dropped)
    return validated
