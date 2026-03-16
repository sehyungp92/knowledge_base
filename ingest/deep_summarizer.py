"""Deep summarizer: structured summary generation via Claude Sonnet.

Three-way dispatch based on source type:
- **paper/arxiv** → academic template (motivation → approach → results →
  implications → limitations)
- **video/podcast** → unified template: briefing (thesis + key takeaways +
  open questions) then comprehensive topic sections with conversation arc
- **article/other** → unified template: briefing then topic sections
"""

from __future__ import annotations

import logging
from pathlib import Path


logger = logging.getLogger(__name__)


def _is_paper(source_type: str) -> bool:
    """Check if source type is a research paper."""
    return source_type in ("paper", "arxiv")


def _is_media(source_type: str) -> bool:
    """Check if source type is video or podcast."""
    return source_type in ("video", "podcast")


def _format_people(authors: list[str] | None) -> str:
    if not authors:
        return ""
    if len(authors) <= 5:
        return ", ".join(authors)
    return f"{', '.join(authors[:5])} et al. ({len(authors)} total)"


def _format_theme_context(themes: list[dict] | None) -> str:
    if not themes:
        return ""
    theme_ids = [t["theme_id"] for t in sorted(themes, key=lambda t: t.get("relevance", 0), reverse=True)]
    return f"\n\nThis source has been classified into these AI themes (by relevance): {', '.join(theme_ids)}. Frame the summary through these lenses — emphasize what matters most to these domains while still covering all significant content.\n"


def _build_header(
    title: str, published_at: str | None, source_type: str,
    people_line: str, url: str | None,
    show_name: str | None = None,
) -> str:
    """Build the markdown header block for a deep summary.

    For videos/podcasts: shows channel/podcast name and labels people as
    "Participants" rather than authors. For papers: standard author line.
    """
    parts = [published_at or '']

    if show_name:
        parts.append(show_name)
    else:
        parts.append(source_type)

    meta_line = " · ".join(p for p in parts if p)

    if people_line:
        if _is_media(source_type):
            meta_line += f"\nParticipants: {people_line}"
        else:
            meta_line += f" · {people_line}"

    return f"""# {title}
{meta_line}
{url or ''}

---"""


def _paper_prompt(
    sliced_text: str, title: str, source_type: str, url: str | None,
    people_line: str, published_at: str | None, theme_context: str,
) -> str:
    header = _build_header(title, published_at, source_type, people_line, url)
    return f"""Generate a structured deep summary of this research paper.{theme_context}

## Source Text
{sliced_text}

## Output Format
Write a structured summary in markdown following this exact format:

{header}

### Motivation & Prior Limitations
What limitations, bottlenecks, or open problems does this paper address? What was the state of the art before this work, and why was it insufficient?
- [Complete sentence describing the problem or limitation]
  - [Specific evidence: prior method's failure mode, benchmark gap, scaling wall, etc.]

---

### Proposed Approach
What does the paper propose, and how does it differ from prior work addressing the same problem? Describe the core technical contribution — the mechanism, architecture, algorithm, or method — not just the claim that it works.
- [Complete sentence describing the approach]
  - [How it differs from or builds on related work]
  - [Key technical detail or design choice]

---

### Results & Capabilities
What does the approach achieve? Include specific numbers, benchmarks, comparisons, and qualitative capabilities. Distinguish between the paper's central claims and secondary findings.
- [Complete sentence stating a result]
  - [Specific metric, comparison, or demonstrated capability]

---

### Implications
What does this work mean for the broader field? How might it affect downstream research, applications, or the trajectory of the themes it touches?
- [Complete sentence on a broader implication]

---

### Remaining Limitations & Next Steps
What does the paper acknowledge it does NOT solve? What are the explicit caveats, failure modes, scalability concerns, or stated future work? Also note any implicit limitations (controlled evaluation conditions, narrow benchmarks, missing comparisons, cost/compute requirements).
- [Complete sentence describing a limitation or open question]
  - [Evidence: author caveat, benchmark scope, failure case, etc.]

## Rules
- Each bullet must be 1-4 complete sentences, never a fragment
- Preserve exact names, numbers, model names, and technical terms
- Include author caveats and uncertainties — do not oversell results
- Nested sub-bullets add specific evidence for the parent point
- If a section genuinely has no content in the paper (e.g., no limitations stated), write "Not explicitly addressed in the paper." and move on
- Do NOT add a summary/conclusion section at the end
- Do NOT repeat the title, URL, or date in the body

Return ONLY the markdown summary."""


def _general_prompt(
    sliced_text: str, title: str, source_type: str, url: str | None,
    people_line: str, published_at: str | None, theme_context: str,
) -> str:
    header = _build_header(title, published_at, source_type, people_line, url)

    return f"""Generate a structured deep summary of this {source_type}.{theme_context}

## Source Text
{sliced_text}

## Output Format
Write a structured summary in markdown following this exact format:

{header}

## Briefing

**[2-3 sentence core argument or thesis of the source. What is the single most important thing this source is saying and why does it matter?]**

### Key Takeaways
1. **[Atomic insight]** — [one-sentence elaboration with specific evidence or context]
2. **[Atomic insight]** — [one-sentence elaboration]
...
[8-12 takeaways total. Each must be a genuinely distinct insight, not a restatement.]

---

### [Topic 1: Descriptive Title]
- [Complete sentence main point]
  - [Specific example, evidence, or elaboration]
    - [Further detail when needed — use 2-3 levels of nesting freely]

### [Topic 2: ...]
...

(Continue with as many topic sections as needed to comprehensively cover the source.)

## Rules
- The Briefing section is a **summary of the summary** — optimized for scanning months later. The thesis should be opinionated and specific, not generic.
- Key Takeaways should be the **8-12 highest-signal insights** distilled to one bold phrase + one sentence each. They should stand alone without reading the full body.
- **Organize body by natural topic clusters.** Each section title should be descriptive (e.g., "The Economics of Scaling", "Why Current Tokenization Fails"), not generic labels.
- **Be comprehensive within each topic section**, typically 5-15+ bullets per section. Capture the substance, not just headlines.
- **Use 2-3 levels of bullet nesting freely.** Sub-bullets for evidence, examples, analogies, caveats.
- **Use **bold** to highlight particularly important insights, quotable statements, or key conclusions** within bullets.
- Each bullet must be 1-4 complete sentences, never a fragment.
- Preserve exact names, numbers, model names, and technical terms.
- Include author caveats and uncertainties — do not oversell claims.
- Do NOT add a summary/conclusion section at the end.
- Do NOT repeat the title, URL, or date in the body.

Return ONLY the markdown summary."""


def _media_prompt(
    sliced_text: str, title: str, source_type: str, url: str | None,
    people_line: str, published_at: str | None, theme_context: str,
    show_name: str | None = None,
) -> str:
    header = _build_header(title, published_at, source_type, people_line, url, show_name=show_name)

    # For video/podcast: ask the LLM to identify participants from the transcript
    participant_instruction = ""
    if not people_line:
        participant_instruction = """
**Participant identification:** Look through the transcript for introductions, name mentions, and affiliations (e.g., "I'm X, researcher at Y" or "today we're joined by X from Y"). In the header, fill in the Participants line with the names and affiliations you find. If no participants can be identified, omit the Participants line.

"""

    return f"""Generate a comprehensive deep summary of this {source_type}.{theme_context}
{participant_instruction}
## Source Text
{sliced_text}

## Output Format
Write a structured summary in markdown following this exact format:

{header}

## Briefing

**[2-3 sentence core argument or thesis of the conversation. What is the single most important thing discussed and why does it matter?]**

### Key Takeaways
1. **[Atomic insight]** — [one-sentence elaboration with specific evidence or context]
2. **[Atomic insight]** — [one-sentence elaboration]
...
[8-12 takeaways total. Each must be a genuinely distinct insight, not a restatement.]

---

### [Descriptive Title Following Conversation Arc]
- [Point as a single focused sentence, or 2-3 sentences when needed]
  - [Sub-point with specific evidence, example, or elaboration]
    - [Further detail when needed — use 2-3 levels of nesting freely]

### [Next Topic Section]
...

(Continue with as many topic sections as needed to cover the full conversation.)

## Voice and Tone — THIS IS CRITICAL
Write as a **professional analytical report**, not a meeting recap or transcript summary.

- **NEVER attribute statements to speakers.** Do not write "Hassabis argues", "the speaker states", "according to X", "X believes", "X's view is". Instead, state the point directly as a declarative claim. Write "AGI is approximately 3-5 years away" not "Hassabis believes AGI is approximately 3-5 years away".
- **NEVER quote verbatim phrases or sentences from the transcript.** Paraphrase all points in your own analytical voice. The only exception is a short term or coined phrase that would lose meaning if paraphrased (e.g., "Move 37", "jagged intelligence").
- **Bullets should be detailed and information-dense**, typically 1-3 full sentences each. Capture the complete reasoning — the *why* or *how* behind each point, not just the *what*. Do not compress points into terse fragments. Example of good detail level: "Most mutations to the DNA are harmless, but some are pathogenic, and so it is important to know which ones are harmful."
- **Only include details present in the transcript.** Do not add outside context, common knowledge, or assumptions. If the transcript does not explain *why* something is the case, do not invent a reason.
- **Interviewer questions** may be included as context bullets where they frame a topic shift, but should be paraphrased concisely, not quoted.

## Rules
- The Briefing section is a **summary of the summary** — optimized for scanning months later. The thesis should be opinionated and specific, not generic.
- Key Takeaways should be the **8-12 highest-signal insights** distilled to one bold phrase + one sentence each. They should stand alone without reading the full body.
- **Organize body by natural conversation topic clusters.** Each section title should be descriptive of the topic discussed (e.g., "Building World Models for AI", "The Economics of Scaling"), not generic labels.
- **Be exhaustively comprehensive within each topic section**, typically 5-15+ bullets per section. Capture ALL substantive points made in the discussion — every distinct argument, sub-argument, qualifying statement, and supporting example. Do not compress or merge points to save space.
- **Use 2-3 levels of bullet nesting to preserve argument structure.** Structure as: claim → reasoning/mechanism → specific example or evidence.
- Use **bold** sparingly to highlight the single most important insight per section, not every other bullet.
- **Preserve specific analogies, examples, and thought experiments** by reference (e.g., the tomato-chopping example for Veo 2, Move 37 in AlphaGo). Name the example but do not quote the surrounding sentences.
- **Preserve exact product names, model names, company names, and proper nouns.** Auto-generated captions often garble names — use your knowledge to correct obvious transcription errors (e.g., "alpha fold" → "AlphaFold", "veo" → "Veo 2", "deep seek" → "DeepSeek").
- Preserve exact numbers, metrics, timelines, and technical terms.
- Include caveats, hedging, and uncertainties — do not oversell claims.
- Do NOT add a summary/conclusion section at the end.
- Do NOT repeat the title, URL, or date in the body.

Return ONLY the markdown summary."""


def build_summary_prompt(
    sliced_text: str, title: str, source_type: str, url: str | None = None,
    authors: list[str] | None = None, published_at: str | None = None,
    themes: list[dict] | None = None, show_name: str | None = None,
) -> str:
    """Build the appropriate summary prompt based on source type.

    Exported so chunked_extractor can use the same templates.

    Args:
        show_name: Channel name (video) or podcast name. When present,
                   replaces source_type in the header and authors are
                   labelled "Participants".
    """
    people_line = _format_people(authors)
    theme_context = _format_theme_context(themes)

    if _is_paper(source_type):
        return _paper_prompt(sliced_text, title, source_type, url, people_line, published_at, theme_context)
    if _is_media(source_type):
        return _media_prompt(sliced_text, title, source_type, url, people_line, published_at, theme_context, show_name=show_name)
    return _general_prompt(sliced_text, title, source_type, url, people_line, published_at, theme_context)


def build_merge_prompt(
    chunk_summaries: list[tuple[int, str]], title: str, source_type: str,
    url: str | None = None, authors: list[str] | None = None,
    published_at: str | None = None, show_name: str | None = None,
) -> str:
    """Build the merge prompt for chunked summaries.

    Uses the paper-specific structure for papers, general structure otherwise.
    Exported so chunked_extractor can use the same templates.
    """
    people_line = _format_people(authors)
    header = _build_header(title, published_at, source_type, people_line, url, show_name=show_name)

    combined = "\n\n---\n\n".join(
        f"## Part {i + 1} of {len(chunk_summaries)}\n{s}"
        for i, (_, s) in enumerate(chunk_summaries)
    )

    if _is_paper(source_type):
        output_format = f"""{header}

### Motivation & Prior Limitations
- [What problem/limitation the paper addresses, with evidence of prior insufficiency]

---

### Proposed Approach
- [Core technical contribution and how it differs from prior work]

---

### Results & Capabilities
- [Specific outcomes with numbers and comparisons]

---

### Implications
- [Broader field impact]

---

### Remaining Limitations & Next Steps
- [Explicit caveats, failure modes, stated future work, and implicit limitations]"""

        merge_rules = """## Rules
- Each bullet must be 1-4 complete sentences, never a fragment
- Preserve exact names, numbers, model names, and technical terms
- Include author caveats and uncertainties
- Integrate content from all parts — no part should be ignored
- Do NOT add a summary/conclusion section at the end"""

    elif _is_media(source_type):
        output_format = f"""{header}

## Briefing

**[2-3 sentence core thesis of the conversation.]**

### Key Takeaways
1. **[Atomic insight]** — [one-sentence elaboration]
...
[8-12 takeaways drawn from ALL parts]

---

### [Descriptive Title Following Conversation Arc]
- [Point as a single focused sentence, or 2-3 sentences when needed]
  - [Sub-point with specific evidence, example, or elaboration]
    - [Further detail when needed]

### [Next Topic Section]
..."""

        merge_rules = """## Voice and Tone — THIS IS CRITICAL
Write as a professional analytical report, not a meeting recap.
- NEVER attribute statements to speakers ("X argues", "the speaker states", "according to X"). State points directly as declarative claims.
- NEVER quote verbatim phrases or sentences. Paraphrase in your own analytical voice. Exception: coined terms that lose meaning if paraphrased (e.g., "Move 37").
- Bullets should be detailed and information-dense (1-3 full sentences each), capturing the complete reasoning — the why or how behind each point. Do not compress into terse fragments.
- Only include details present in the transcript — no outside context or assumptions.

## Rules
- The Briefing is a summary of the summary — thesis should be opinionated and specific
- Key Takeaways: 8-12 highest-signal insights, each as bold phrase + one sentence, drawn from ALL parts
- Organize body by natural conversation topic clusters — merge overlapping topics from different parts into unified sections
- Be exhaustively comprehensive within each topic section, typically 5-15+ bullets per section. Capture ALL substantive points.
- Use 2-3 levels of bullet nesting: claim → reasoning/mechanism → specific example or evidence
- Use **bold** sparingly — highlight the single most important insight per section
- Preserve specific analogies and examples by reference (name them, don't quote surrounding sentences)
- Preserve exact product names, model names, company names, proper nouns. Correct obvious transcription errors.
- Preserve exact numbers, metrics, timelines, and technical terms
- Include caveats and uncertainties — do not oversell claims
- Integrate content from all parts — no part should be ignored
- Do NOT add a summary/conclusion section at the end"""

    else:
        output_format = f"""{header}

## Briefing

**[2-3 sentence core thesis of the source.]**

### Key Takeaways
1. **[Atomic insight]** — [one-sentence elaboration]
...
[8-12 takeaways drawn from ALL parts]

---

### [Topic 1: Descriptive Title]
- [Complete sentence main point]
  - [Specific example, evidence, or elaboration]

### [Topic 2: ...]
..."""

        merge_rules = """## Rules
- The Briefing is a summary of the summary — thesis should be opinionated and specific
- Key Takeaways: 8-12 highest-signal insights, each as bold phrase + one sentence, drawn from ALL parts
- Be comprehensive within each topic section, typically 5-15+ bullets per section
- Use 2-3 levels of bullet nesting freely
- Use **bold** to highlight important insights within bullets
- Each bullet must be 1-4 complete sentences, never a fragment
- Preserve exact names, numbers, model names, and technical terms
- Include author caveats and uncertainties
- Integrate content from all parts — no part should be ignored
- Do NOT add a summary/conclusion section at the end"""

    return f"""You are merging {len(chunk_summaries)} partial summaries of a {source_type} into one coherent deep summary.

The partial summaries were generated from consecutive chunks of the full document. Synthesize them — don't just concatenate.

## Partial Summaries
{combined}

## Output Format
Write a single unified summary in markdown following this exact format:

{output_format}

{merge_rules}

Return ONLY the markdown summary."""


def generate_deep_summary(
    source_id: str,
    clean_text: str,
    title: str,
    source_type: str,
    url: str | None = None,
    authors: list[str] | None = None,
    published_at: str | None = None,
    executor=None,
    library_path: Path | None = None,
    budget: int | None = None,
    themes: list[dict] | None = None,
    show_name: str | None = None,
) -> str:
    """Generate a structured deep_summary.md for a source.

    Uses claude-sonnet for quality on Max subscription.
    Returns the summary text.

    Always uses the FULL source text (after backmatter stripping) — never
    budgeted or chunked.  The summary is the primary human-readable artifact
    and must capture every substantive point in the source.  The ``budget``
    parameter is accepted for backward compatibility but ignored.

    Uses a paper-specific template for research papers that follows
    academic argumentative structure (motivation → approach → results →
    implications → limitations), and a general template for other sources.

    Args:
        themes: Optional list of {theme_id, relevance} dicts from theme
                classification. When provided, guides summary emphasis
                toward the most relevant domains.
        show_name: Channel name (video) or podcast name. When present,
                   replaces source_type in the header and authors are
                   labelled "Participants".
        budget: Ignored. Kept for API compatibility.
    """
    from ingest.section_slicer import strip_backmatter

    # Use the full text, only stripping references/appendices
    full_text = strip_backmatter(clean_text)

    # Generous timeout: summary output length is bounded regardless of input
    # length, but the model still needs time to read longer inputs.
    # 480s base + 30s per 10K chars beyond 50K, capped at 600s.
    text_len = len(full_text)
    summary_timeout = min(480 + max(0, (text_len - 50_000) // 10_000) * 30, 600)

    logger.info(
        "Generating deep summary for %s: %d chars (full text), timeout=%ds",
        source_id, text_len, summary_timeout,
    )

    prompt = build_summary_prompt(
        full_text, title, source_type, url=url,
        authors=authors, published_at=published_at, themes=themes,
        show_name=show_name,
    )

    if executor is None:
        logger.warning("No executor provided, returning placeholder summary")
        return f"# {title}\n\nSummary pending."

    result = executor.run_raw(
        prompt,
        session_id=f"summary_{source_id}",
        timeout=summary_timeout,
    )

    if result.is_timeout:
        logger.warning(
            "Summary generation timed out for %s (%ds on %d chars), no fallback — returning partial or failed",
            source_id, summary_timeout, text_len,
        )

    summary = result.text.strip() if result.text else f"# {title}\n\nSummary generation failed."

    # Save to library
    if library_path:
        summary_path = library_path / source_id / "deep_summary.md"
        if summary_path.parent.exists():
            summary_path.write_text(summary, encoding="utf-8")

    return summary
