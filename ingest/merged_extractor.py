"""Merged extraction: combine compatible extraction steps into single subprocess calls.

Merge A: Claims + Summary → single Sonnet call
Merge B: Landscape + Implications → single Sonnet call

Each merge function falls back to individual calls on parse failure.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from ingest.json_parser import parse_json_from_llm
from ingest.section_slicer import budget_for_source_type, prioritized_slice, timeout_for_text

logger = logging.getLogger(__name__)

# Delimiter separating JSON claims block from markdown summary block
_CLAIMS_SUMMARY_DELIMITER = "---SUMMARY---"


def extract_claims_and_summary(
    source_id: str,
    clean_text: str,
    source_type: str,
    title: str,
    url: str | None = None,
    authors: list[str] | None = None,
    published_at: str | None = None,
    themes: list[dict] | None = None,
    show_name: str | None = None,
    executor=None,
    library_path: Path | None = None,
    budget: int | None = None,
) -> dict:
    """Extract claims and generate deep summary in a single LLM call.

    Returns dict with keys: claims, concepts, summary.
    Falls back to individual calls if merged parsing fails.
    """
    # Resolve budget from source_type if not provided
    if budget is None:
        budget = budget_for_source_type(source_type)

    # Merged call generates BOTH claims JSON + full summary in one response.
    # For text > 15K chars the combined output exceeds what Claude CLI subprocess
    # can reliably produce within timeout. Fall back to parallel individual calls.
    # Individual calls use their own timeout management via timeout_for_text(),
    # so the full budget is passed through — extract_claims will route to
    # chunked extraction if text exceeds 2x budget.
    if len(clean_text) > 15_000:
        logger.info(
            "Text too long for merged call (%d chars > 15K), using individual calls for %s",
            len(clean_text), source_id,
        )
        return _fallback_individual(
            source_id, clean_text, source_type, title, url, authors,
            published_at, themes, show_name, executor, library_path, budget,
        )

    if executor is None:
        logger.warning("No executor provided, returning empty results")
        return {"claims": [], "concepts": [], "summary": f"# {title}\n\nSummary pending."}

    sliced_text = prioritized_slice(clean_text, budget=budget)
    # Merged call does TWO tasks; give it 50% more time than a single extraction
    dynamic_timeout = int(timeout_for_text(len(sliced_text)) * 1.5)

    # Build theme context
    theme_context = ""
    if themes:
        theme_ids = [t["theme_id"] for t in sorted(themes, key=lambda t: t.get("relevance", 0), reverse=True)]
        theme_context = f"\n\nThis source has been classified into these AI themes (by relevance): {', '.join(theme_ids)}. Prioritize extraction toward these themes while still covering all significant content.\n"

    # Build the summary prompt portion using the existing template builder
    from ingest.deep_summarizer import build_summary_prompt
    summary_prompt_body = build_summary_prompt(
        sliced_text, title, source_type, url=url,
        authors=authors, published_at=published_at, themes=themes,
        show_name=show_name,
    )

    prompt = f"""You will perform TWO extraction tasks on the same source text in a single response.

## TASK 1: Claim & Concept Extraction{theme_context}

Extract structured knowledge from this {source_type}.

### Instructions
1. Extract atomic claims (statements that can be true/false)
2. Extract concepts (methods, datasets, metrics, theories, entities)
3. For each claim, provide a verbatim evidence_snippet from the source text
4. If no evidence can be found for a claim, DO NOT include it

### Claim Type Guidance
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

### Confidence Calibration
Use the FULL range -- a good extraction has meaningful spread, not everything at 0.9+.
- 0.95-1.0: Precise quantitative evidence with specific numbers (e.g., "achieves 94.2% on MMLU"). Reserve strictly for hard measurements.
- 0.85-0.94: Directly stated qualitative claims well-supported by evidence, or quantitative claims with incomplete methodology
- 0.70-0.84: Requires interpretation, or evidence is indirect/analogical. Includes well-grounded qualitative observations.
- 0.50-0.69: Author opinion, hedged language ("may", "could", "suggests"), extrapolation, or implicit signals inferred from context
- Below 0.50: Contradicted by other evidence, highly uncertain, or unsubstantiated

### Quality Filter
Only extract claims that represent THIS SOURCE's contribution. Skip background knowledge (except limitations that constrain the work), autobiographical trivia, generic truisms, or unfalsifiable opinions.

### Output Format for Task 1
Return a JSON object:
```json
{{
  "claims": [
    {{
      "claim_text": "...",
      "claim_type": "finding|method|limitation|assumption",
      "section": "...",
      "confidence": 0.0-1.0,
      "evidence_snippet": "exact quote from text",
      "evidence_location": "section name or page",
      "evidence_type": "quote|table|figure|citation",
      "temporal_scope": "current_state|historical|future_prediction"
    }}
  ],
  "concepts": [
    {{
      "canonical_name": "...",
      "concept_type": "method|dataset|metric|theory|entity",
      "description": "...",
      "aliases": ["..."]
    }}
  ]
}}
```

## TASK 2: Deep Summary

{summary_prompt_body}

## RESPONSE FORMAT

Output Task 1 (JSON) first, then the delimiter line, then Task 2 (markdown summary).
The delimiter MUST be exactly this line on its own:

{_CLAIMS_SUMMARY_DELIMITER}

## Source Text
{sliced_text}

Begin your response with the JSON object for Task 1, followed by the delimiter, followed by the markdown summary."""

    try:
        result = executor.run_raw(
            prompt,
            session_id=f"merged_claims_summary_{source_id}",
            timeout=dynamic_timeout,
        )

        parsed = _parse_claims_and_summary(result.text, clean_text)
        if parsed is not None:
            claims_data, summary_text = parsed

            # Validate evidence snippets
            from ingest.extractor import validate_claims_evidence
            claims_data["claims"] = validate_claims_evidence(
                claims_data.get("claims", []), clean_text, source_id,
            )

            # Save artifacts to library
            if library_path:
                _save_artifacts(library_path, source_id, claims_data, summary_text)

            logger.info(
                "Merged claims+summary for %s: %d claims, %d concepts, %d chars summary",
                source_id, len(claims_data.get("claims", [])),
                len(claims_data.get("concepts", [])), len(summary_text),
            )
            return {
                "claims": claims_data.get("claims", []),
                "concepts": claims_data.get("concepts", []),
                "summary": summary_text,
            }

    except Exception:
        logger.warning("Merged claims+summary call failed for %s, falling back to individual calls", source_id, exc_info=True)

    # Fallback to individual calls
    logger.info("Falling back to separate claims + summary calls for %s", source_id)
    return _fallback_individual(
        source_id, clean_text, source_type, title, url, authors,
        published_at, themes, show_name, executor, library_path, budget,
    )


def extract_landscape_and_implications(
    clean_text: str,
    source_id: str,
    source_themes: list[str] | None = None,
    published_at: str | None = None,
    executor=None,
    source_type: str | None = None,
    get_conn_fn=None,
) -> dict:
    """Extract landscape signals and cross-theme implications in parallel.

    Runs individual landscape and implication extractors concurrently via
    ThreadPoolExecutor, avoiding the merged-prompt approach that always
    timed out (~300s wasted before fallback).

    Returns dict with keys: landscape (the signals dict), implications (list).
    """
    if executor is None:
        from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
        executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    from concurrent.futures import ThreadPoolExecutor
    from ingest.landscape_extractor import extract_landscape_signals
    from ingest.implication_extractor import extract_cross_theme_implications

    def _landscape():
        return extract_landscape_signals(
            clean_text=clean_text,
            source_id=source_id,
            source_themes=source_themes,
            published_at=published_at,
            executor=executor,
            source_type=source_type,
        )

    def _implications():
        if not source_themes:
            return []
        return extract_cross_theme_implications(
            clean_text, source_id, source_themes,
            published_at=published_at,
            executor=executor,
            get_conn_fn=get_conn_fn,
        )

    logger.info("Running landscape + implications in parallel for %s", source_id)
    with ThreadPoolExecutor(max_workers=2) as pool:
        fut_l = pool.submit(_landscape)
        fut_i = pool.submit(_implications)

    landscape, implications = {}, []
    try:
        landscape = fut_l.result()
    except Exception:
        logger.warning("Landscape extraction failed for %s", source_id, exc_info=True)
    try:
        implications = fut_i.result()
    except Exception:
        logger.warning("Implication extraction failed for %s", source_id, exc_info=True)

    return {"landscape": landscape, "implications": implications}


# ── Parsing helpers ──────────────────────────────────────────────────────


def _parse_claims_and_summary(text: str, clean_text: str) -> tuple[dict, str] | None:
    """Parse merged claims+summary response. Returns (claims_dict, summary_str) or None."""
    if not text or _CLAIMS_SUMMARY_DELIMITER not in text:
        logger.warning("Merged response missing delimiter, will fall back")
        return None

    parts = text.split(_CLAIMS_SUMMARY_DELIMITER, 1)
    if len(parts) != 2:
        return None

    json_part = parts[0].strip()
    summary_part = parts[1].strip()

    # Parse claims JSON
    claims_data = _extract_json_object(json_part)
    if claims_data is None:
        logger.warning("Failed to parse claims JSON from merged response")
        return None

    if not summary_part:
        logger.warning("Empty summary in merged response")
        return None

    return claims_data, summary_part


def _parse_landscape_and_implications(text: str) -> tuple[dict, list[dict]] | None:
    """Parse merged landscape+implications JSON. Returns (landscape, implications) or None."""
    if not text:
        return None

    parsed = _extract_json_object(text)
    if parsed is None:
        return None

    landscape = parsed.get("landscape")
    implications = parsed.get("implications")

    if not isinstance(landscape, dict):
        logger.warning("Merged response missing 'landscape' key")
        return None

    if not isinstance(implications, list):
        # Implications are optional — if missing, treat as empty
        implications = []

    # Ensure landscape has expected keys
    for key in ("capabilities", "limitations", "bottlenecks", "breakthroughs"):
        if key not in landscape:
            landscape[key] = []

    return landscape, implications


def _extract_json_object(text: str) -> dict | None:
    """Extract a JSON object from text, handling code blocks."""
    return parse_json_from_llm(text, expect=dict)


# ── Fallback: individual calls ───────────────────────────────────────────


def _fallback_individual(
    source_id, clean_text, source_type, title, url, authors,
    published_at, themes, show_name, executor, library_path, budget,
) -> dict:
    """Fall back to separate claim extraction and summary generation.

    Each call is wrapped with retry logic and a delay is inserted between
    calls to let rate-limit windows pass.
    """
    import time
    from ingest.http_retry import with_retry

    logger.info("Falling back to individual claims + summary calls for %s", source_id)

    from ingest.extractor import extract_claims
    from ingest.deep_summarizer import generate_deep_summary

    claims_result = with_retry(
        lambda: extract_claims(
            source_id=source_id,
            clean_text=clean_text,
            source_type=source_type,
            executor=executor,
            library_path=library_path,
            budget=budget,
            themes=themes,
        ),
        max_attempts=2,
        base_delay=5.0,
        label=f"fallback_claims_{source_id}",
    )

    # Delay between calls to avoid hitting the same rate limit window
    time.sleep(5)

    summary_result = with_retry(
        lambda: generate_deep_summary(
            source_id=source_id,
            clean_text=clean_text,
            title=title,
            source_type=source_type,
            url=url,
            authors=authors,
            published_at=published_at,
            executor=executor,
            library_path=library_path,
            budget=budget,
            themes=themes,
            show_name=show_name,
        ),
        max_attempts=2,
        base_delay=5.0,
        label=f"fallback_summary_{source_id}",
    )

    return {
        "claims": claims_result.get("claims", []),
        "concepts": claims_result.get("concepts", []),
        "summary": summary_result,
    }



# ── Artifact saving ──────────────────────────────────────────────────────


def _save_artifacts(library_path: Path, source_id: str, claims_data: dict, summary_text: str):
    """Save extraction artifacts to library directory."""
    source_dir = library_path / source_id
    if not source_dir.exists():
        return

    # Save extractions.json
    extractions_path = source_dir / "extractions.json"
    try:
        extractions_path.write_text(
            json.dumps(claims_data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception:
        logger.warning("Failed to save extractions.json for %s", source_id, exc_info=True)

    # Save deep_summary.md
    summary_path = source_dir / "deep_summary.md"
    try:
        summary_path.write_text(summary_text, encoding="utf-8")
    except Exception:
        logger.warning("Failed to save deep_summary.md for %s", source_id, exc_info=True)
