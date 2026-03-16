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
    # For long texts, cap the budget to avoid timeout-then-retry cycles: the
    # original budget (e.g. 50K for video) produces prompts that push against
    # the CLI timeout, wasting ~300s before retrying at half budget anyway.
    # The cap must also avoid accidentally triggering chunked extraction
    # (which fires when text_len > 2*budget), so we ensure the budget stays
    # at least ceil(text_len/2) when text is near that boundary.
    if len(clean_text) > 15_000:
        cap = 35_000
        # Don't let the cap push us into chunked extraction unnecessarily
        min_for_single_call = (len(clean_text) + 1) // 2 + 1
        long_text_budget = min(budget, max(cap, min_for_single_call))
        if long_text_budget != budget:
            logger.info(
                "Text too long for merged call (%d chars > 15K), using individual calls for %s (budget %d -> %d)",
                len(clean_text), source_id, budget, long_text_budget,
            )
        else:
            logger.info(
                "Text too long for merged call (%d chars > 15K), using individual calls for %s",
                len(clean_text), source_id,
            )
        return _fallback_individual(
            source_id, clean_text, source_type, title, url, authors,
            published_at, themes, show_name, executor, library_path, long_text_budget,
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
      "evidence_type": "quote|table|figure|citation"
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
            from ingest.extractor import _validate_evidence
            validated_claims = []
            total_claims = len(claims_data.get("claims", []))
            for claim in claims_data.get("claims", []):
                snippet = claim.get("evidence_snippet", "")
                if snippet and _validate_evidence(snippet, clean_text):
                    validated_claims.append(claim)
                elif not snippet:
                    logger.debug("Dropping claim without evidence: %s", claim.get("claim_text", "")[:50])
                else:
                    logger.debug("Evidence snippet not found in source: %s", snippet[:50])
            dropped = total_claims - len(validated_claims)
            logger.info(
                "Evidence validation (merged) for %s: %d/%d claims kept, %d dropped",
                source_id, len(validated_claims), total_claims, dropped,
            )
            claims_data["claims"] = validated_claims

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
