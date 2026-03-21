"""Report generator: outline-first generation with section progress and lens tracing.

Produces structured reports with visible process: outline → per-section lens calls →
section generation → final artifact assembly.
"""

from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

logger = logging.getLogger(__name__)


@dataclass
class LensEvent:
    """Record of a lens call during report generation."""
    lens_id: str
    query: str
    result_summary: str
    citation_count: int
    evidence_count: int
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "lens_id": self.lens_id,
            "query": self.query,
            "result_summary": self.result_summary,
            "citation_count": self.citation_count,
            "evidence_count": self.evidence_count,
            "timestamp": self.timestamp,
        }


@dataclass
class ReportRunState:
    """Tracks the full state of a report generation run."""
    topic: str
    outline: list[str] = field(default_factory=list)
    section_states: dict[str, str] = field(default_factory=dict)  # title -> status
    section_content: dict[str, str] = field(default_factory=dict)  # title -> markdown
    lens_events: list[LensEvent] = field(default_factory=list)
    final_markdown: str | None = None
    artifact_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "topic": self.topic,
            "outline": self.outline,
            "section_states": self.section_states,
            "section_content": self.section_content,
            "lens_events": [e.to_dict() for e in self.lens_events],
            "final_markdown": self.final_markdown,
            "artifact_path": self.artifact_path,
        }


def generate_report_outline(topic: str, context_summary: str, executor) -> list[str]:
    """Generate a section outline for a report on a topic.

    Uses a fast model call to produce 3-6 section titles.
    """
    prompt = f"""Generate an outline of 4-6 section titles for a research report on:

Topic: {topic}

Available context: {context_summary[:1000]}

Tailor sections to the topic. For research/technical topics, consider:
Architecture & Design, Experimental Results, Limitations & Failure Modes, Open Problems.
For trend/landscape topics, consider:
Current State, Evidence For & Against, Key Tensions, What's Next.
Avoid generic headings like "Introduction" or "Key Findings" — be specific to {topic}.

Return ONLY a JSON array of section title strings, no other text."""

    try:
        result = executor.run_raw(
            prompt,
            session_id="report_outline",
            timeout=30,
        )
        # Parse JSON array from response
        json_match = re.search(r"\[.*\]", result.text, re.DOTALL)
        if json_match:
            sections = json.loads(json_match.group(0))
            if isinstance(sections, list) and all(isinstance(s, str) for s in sections):
                return sections[:6]
    except Exception:
        logger.warning("report_outline generation failed", exc_info=True)
    finally:
        try:
            executor.cleanup_session("report_outline")
        except Exception:
            pass

    # Fallback outline
    return [
        "Key Findings",
        "Evidence Analysis",
        "Limitations & Gaps",
        "Implications",
        "Open Questions",
    ]



def react_generate_section(
    title: str,
    topic: str,
    get_conn_fn,
    executor,
    embedding: list[float] | None = None,
    max_rounds: int = 3,
    min_lens_calls: int = 2,
    prior_summaries: str = "",
) -> tuple[str, list["LensEvent"]]:
    """ReACT-style section generation: plan lenses → gather evidence → write.

    Instead of pre-assembled, truncated context, the agent plans which lenses
    to call, gathers evidence iteratively, then writes with the full context.

    Returns (section_content, lens_events).
    """
    from retrieval.lenses import (
        run_lens_by_name, format_lens_results_for_prompt, LensResult,
    )

    all_lens_results: list[LensResult] = []
    lens_events: list[LensEvent] = []
    available_lenses = ["evidence", "theme_panorama", "bridge", "contradiction"]

    prior_context = f"\n## Prior Sections\n{prior_summaries}\n" if prior_summaries else ""

    # Round 1: Ask LLM which lenses to call for this section
    plan_prompt = f"""You are planning evidence gathering for a report section.

Section title: "{title}"
Report topic: {topic}
{prior_context}Available lenses: {json.dumps(available_lenses)}

Lens descriptions:
- evidence: Direct claim and snippet retrieval from the knowledge base
- theme_panorama: Landscape state — capabilities, limitations, bottlenecks, breakthroughs, anticipations
- bridge: Cross-theme connections and implications between research areas
- contradiction: Conflicting claims and coverage gaps

Select 2-4 lenses and specify the query for each. Choose lenses that are most relevant
to this section's purpose. For sections about limitations/gaps, include "contradiction".
For sections about implications/connections, include "bridge".

Return ONLY a JSON array: [{{"lens": "evidence", "query": "specific query"}}]"""

    # Use title slug for unique session IDs to avoid cross-section collisions
    _title_slug = re.sub(r"[^a-z0-9]+", "_", title.lower())[:30]

    planned_calls = []
    plan_sid = f"react_plan_{_title_slug}"
    try:
        result = executor.run_raw(plan_prompt, session_id=plan_sid, timeout=30)
        if result.text:
            json_match = re.search(r"\[.*\]", result.text, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group(0))
                if isinstance(parsed, list):
                    planned_calls = [
                        p for p in parsed
                        if isinstance(p, dict) and p.get("lens") in available_lenses
                    ]
    except Exception:
        logger.debug("react_plan failed, using defaults", exc_info=True)
    finally:
        try:
            executor.cleanup_session(plan_sid)
        except Exception:
            pass

    # Fallback: ensure minimum lens calls
    if len(planned_calls) < min_lens_calls:
        planned_calls = [
            {"lens": "evidence", "query": f"{topic} {title}"},
            {"lens": "theme_panorama", "query": topic},
        ]
        # Add contradiction for limitation/gap-related sections
        title_lower = title.lower()
        if any(kw in title_lower for kw in ("limitation", "gap", "challenge", "risk", "open question", "weakness")):
            planned_calls.append({"lens": "contradiction", "query": topic})
        # Add bridge for implication/connection sections
        if any(kw in title_lower for kw in ("implication", "connection", "bridge", "cross", "future")):
            planned_calls.append({"lens": "bridge", "query": topic})

    # Execute planned lens calls
    for call in planned_calls:
        lens_id = call["lens"]
        query = call.get("query", topic)
        try:
            lr = run_lens_by_name(lens_id, query, get_conn_fn, embedding=embedding)
            all_lens_results.append(lr)
            lens_events.append(LensEvent(
                lens_id=lens_id,
                query=query,
                result_summary=lr.summary[:200],
                citation_count=len(lr.citations),
                evidence_count=len(lr.evidence_items),
            ))
        except Exception:
            logger.debug("react lens call failed: %s", lens_id, exc_info=True)

    # Round 2 (optional): Check if we have enough evidence
    total_evidence = sum(len(lr.evidence_items) for lr in all_lens_results)
    rounds_used = 1

    while total_evidence < 3 and rounds_used < max_rounds:
        rounds_used += 1
        # Ask LLM for additional lens calls
        current_summary = "\n".join(lr.summary[:100] for lr in all_lens_results)
        used_lenses = {e.lens_id for e in lens_events}
        unused = [l for l in available_lenses if l not in used_lenses]

        if not unused:
            break

        refine_prompt = f"""Evidence gathered so far for section "{title}" (topic: {topic}):
{current_summary}

Total evidence items: {total_evidence}. This is insufficient.
Unused lenses: {unused}

Suggest 1-2 additional lens calls to fill gaps. Return JSON: [{{"lens": "...", "query": "..."}}]"""

        refine_sid = f"react_refine_{_title_slug}_{rounds_used}"
        try:
            result = executor.run_raw(refine_prompt, session_id=refine_sid, timeout=20)
            if result.text:
                json_match = re.search(r"\[.*\]", result.text, re.DOTALL)
                if json_match:
                    additional = json.loads(json_match.group(0))
                    for call in additional:
                        if isinstance(call, dict) and call.get("lens") in available_lenses:
                            lr = run_lens_by_name(
                                call["lens"], call.get("query", topic),
                                get_conn_fn, embedding=embedding,
                            )
                            all_lens_results.append(lr)
                            lens_events.append(LensEvent(
                                lens_id=call["lens"],
                                query=call.get("query", topic),
                                result_summary=lr.summary[:200],
                                citation_count=len(lr.citations),
                                evidence_count=len(lr.evidence_items),
                            ))
                            total_evidence += len(lr.evidence_items)
        except Exception:
            logger.debug("react refinement round %d failed", rounds_used, exc_info=True)
            break
        finally:
            try:
                executor.cleanup_session(refine_sid)
            except Exception:
                pass

    # Guard: if zero lens calls succeeded, fall back to a minimal evidence_lens call
    if not all_lens_results or all(not lr.evidence_items for lr in all_lens_results):
        try:
            fallback_lr = run_lens_by_name("evidence", topic, get_conn_fn, embedding=embedding)
            if fallback_lr.evidence_items:
                all_lens_results.append(fallback_lr)
                lens_events.append(LensEvent(
                    lens_id="evidence",
                    query=topic,
                    result_summary=fallback_lr.summary[:200],
                    citation_count=len(fallback_lr.citations),
                    evidence_count=len(fallback_lr.evidence_items),
                ))
        except Exception:
            logger.debug("react fallback evidence_lens also failed for %s", title)

    # Generate section with full (untruncated) lens context
    full_context = format_lens_results_for_prompt(all_lens_results)

    prior_ref = f"\n## Prior Sections\nDo not repeat findings already covered:\n{prior_summaries}\n" if prior_summaries else ""

    write_prompt = f"""Write the "{title}" section for a research report on: {topic}

Use ONLY the evidence provided below. Cite sources using [source_id] inline.

## Evidence
{full_context}
{prior_ref}
## Instructions
- Write 2-4 paragraphs of analytical prose for this section
- State findings as facts. Never reference sources meta-textually
- FORBIDDEN phrases: "according to", "one study found", "the authors argue", "research suggests"
- Name specific models, benchmarks, metrics, and timelines — not vague categories
- Do NOT defer to generic conclusions. When sources disagree, say so explicitly
- Limitations are the most valuable signal: foreground gaps, controlled conditions, and conspicuous absences
- For limitation/gap sections: lead with what doesn't work and why
- For implication/connection sections: surface non-obvious cross-domain connections
- Integrate findings from multiple lenses. Note contradictions and uncertainty where they exist
- Use markdown formatting

Write the section content now (no section heading needed):"""

    write_sid = f"react_write_{_title_slug}"
    try:
        result = executor.run_raw(write_prompt, session_id=write_sid, timeout=90)
        if result.text and len(result.text) > 20:
            return result.text, lens_events
    except Exception:
        logger.warning("react_write failed for %s", title, exc_info=True)
    finally:
        try:
            executor.cleanup_session(write_sid)
        except Exception:
            pass

    return f"*Section generation failed for: {title}*", lens_events


def _synthesize_across_sections(
    topic: str,
    section_content: dict[str, str],
    lens_events: list[LensEvent],
    executor,
    landscape_summary: str = "",
) -> str | None:
    """Generate a synthesis section that identifies cross-cutting themes.

    Reads all generated sections and produces 2-3 paragraphs identifying
    themes spanning multiple sections, contradictions, and emergent insights.

    Returns synthesis markdown, or None on failure.
    """
    section_summaries = []
    for title, content in section_content.items():
        if content and not content.startswith("*Section generation failed"):
            # Truncate long sections for the synthesis prompt
            truncated = content[:2000]
            if len(content) > 2000:
                truncated += "\n[...truncated]"
            section_summaries.append(f"### {title}\n{truncated}")

    if len(section_summaries) < 2:
        return None  # Not enough sections to synthesize across

    sections_text = "\n\n".join(section_summaries)

    lens_summary = ""
    if lens_events:
        lens_counts: dict[str, int] = {}
        for le in lens_events:
            lens_counts[le.lens_id] = lens_counts.get(le.lens_id, 0) + 1
        lens_summary = ", ".join(f"{lid}: {c} calls" for lid, c in lens_counts.items())

    landscape_block = f"\n## Landscape Context\n{landscape_summary}\n" if landscape_summary else ""

    prompt = f"""You've read a research report on "{topic}" with these sections:

{sections_text}

Lenses used: {lens_summary or "N/A"}
{landscape_block}
Write a "Synthesis" section (2-3 paragraphs) that:
1. Identifies themes that span multiple sections but weren't explicitly connected
2. Notes contradictions between sections — where one section's findings tension with another's
3. Surfaces emergent insights that no single section captures on its own
4. States the single most important takeaway from the entire report
5. Notes where section findings confirm, contradict, or extend active anticipations or bottleneck assessments

Be specific — reference findings from named sections. Do not repeat what sections already say.
Write the synthesis content now (no section heading needed):"""

    try:
        result = executor.run_raw(
            prompt,
            session_id="report_synthesis",
            timeout=60,
        )
        if result.text and len(result.text) > 50:
            return result.text.strip()
    except Exception:
        logger.warning("Cross-section synthesis failed for %s", topic, exc_info=True)
    finally:
        try:
            executor.cleanup_session("report_synthesis")
        except Exception:
            pass

    return None


def run_report(
    topic: str,
    get_conn_fn,
    executor,
    on_progress: Callable[[str], None] | None = None,
    library_path: Path | None = None,
) -> ReportRunState:
    """Orchestrate full report generation with outline-first flow.

    1. Generate outline → emit progress
    2. For each section: run relevant lenses → emit lens events → generate content
    3. Assemble final markdown → persist artifact
    """
    from retrieval.lenses import (
        evidence_lens, panorama_lens,
        format_lens_results_for_prompt, LensResult,
    )

    state = ReportRunState(topic=topic)

    # Get embedding for the topic
    embedding = None
    try:
        from reading_app.embeddings import embed_batch
        embedding = embed_batch([topic])[0]
    except Exception:
        pass

    # Step 1: Run initial lenses to get context for outline generation
    if on_progress:
        on_progress("Surveying topic for outline...")

    evidence_result = evidence_lens(topic, get_conn_fn, embedding=embedding, k=10)
    panorama_result = panorama_lens(topic, get_conn_fn)

    context_summary = format_lens_results_for_prompt([evidence_result, panorama_result])

    # Step 2: Generate outline
    if on_progress:
        on_progress("Planning report structure...")

    state.outline = generate_report_outline(topic, context_summary, executor)
    for title in state.outline:
        state.section_states[title] = "pending"

    if on_progress:
        on_progress(f"Outline: {len(state.outline)} sections planned")

    # Build landscape summary for cross-section synthesis
    landscape_summary = panorama_result.summary[:1500] if panorama_result.summary else ""

    # Step 3: Generate each section using ReACT agent
    prior_section_summaries: list[str] = []
    for i, section_title in enumerate(state.outline):
        state.section_states[section_title] = "generating"
        if on_progress:
            on_progress(f"Writing section {i+1}/{len(state.outline)}: {section_title}")

        prior_text = "\n".join(prior_section_summaries) if prior_section_summaries else ""
        content, section_lens_events = react_generate_section(
            title=section_title,
            topic=topic,
            get_conn_fn=get_conn_fn,
            executor=executor,
            embedding=embedding,
            prior_summaries=prior_text,
        )
        state.lens_events.extend(section_lens_events)

        state.section_content[section_title] = content
        state.section_states[section_title] = "complete"

        # Extract a brief summary for subsequent sections
        if content and not content.startswith("*Section generation failed"):
            sentences = content.split(". ")
            brief = ". ".join(sentences[:2]).strip()
            if brief and not brief.endswith("."):
                brief += "."
            prior_section_summaries.append(f"- {section_title}: {brief[:200]}")

        # Emit section content for progressive delivery (bold heading for Telegram)
        if on_progress and content and not content.startswith("*Section generation failed"):
            on_progress(f"**{section_title}**\n\n{content}")

    # Step 3.5: Cross-section synthesis
    synthesis_content = None
    if len(state.outline) >= 2:
        if on_progress:
            on_progress("Synthesizing across sections...")
        synthesis_content = _synthesize_across_sections(
            topic=topic,
            section_content=state.section_content,
            lens_events=state.lens_events,
            executor=executor,
            landscape_summary=landscape_summary,
        )
        if synthesis_content:
            if on_progress:
                on_progress(f"**Synthesis**\n\n{synthesis_content}")

    # Step 4: Assemble final markdown
    if on_progress:
        on_progress("Assembling final report...")

    parts = [f"# {topic}\n"]
    # Count unique lenses used across all sections
    unique_lenses = {le.lens_id for le in state.lens_events}
    parts.append(f"*{len(state.lens_events)} lens calls across {len(unique_lenses)} lens types*\n")

    for title in state.outline:
        parts.append(f"## {title}\n")
        parts.append(state.section_content.get(title, ""))
        parts.append("")

    if synthesis_content:
        parts.append("## Synthesis\n")
        parts.append(synthesis_content)
        parts.append("")

    state.final_markdown = "\n".join(parts)

    # Step 5: Persist artifact and state for follow-up
    slug = topic.lower().replace(" ", "_")[:50]
    if library_path:
        try:
            syntheses_dir = library_path / "syntheses"
            syntheses_dir.mkdir(parents=True, exist_ok=True)
            report_path = syntheses_dir / f"{slug}.md"
            report_path.write_text(state.final_markdown, encoding="utf-8")
            state.artifact_path = str(report_path)

            # Persist state for interactive follow-up
            state_path = syntheses_dir / f"{slug}_state.json"
            state_path.write_text(
                json.dumps(state.to_dict(), default=str), encoding="utf-8"
            )
        except Exception:
            logger.warning("report artifact persistence failed", exc_info=True)

    # Step 6: Extract key conclusions and persist as synthesis claims
    _persist_report_conclusions(state, get_conn_fn, executor)

    if on_progress:
        on_progress(f"Report complete: {len(state.outline)} sections")

    return state


def _persist_report_conclusions(
    state: ReportRunState,
    get_conn_fn,
    executor,
) -> None:
    """Extract 3-5 key conclusions from the report and persist as synthesis claims.

    These claims have provenance_type='synthesis' and become retrievable
    via hybrid_retrieve, feeding report insights back into the knowledge graph.
    """
    if not state.final_markdown or len(state.final_markdown) < 200:
        return

    try:
        from reading_app.db import insert_claim, ensure_pool
        from reading_app.embeddings import embed_batch
        from ulid import ULID

        ensure_pool()

        # Prefer the synthesis section for conclusion extraction (higher signal density)
        source_text = state.final_markdown[:6000]
        if "## Synthesis\n" in state.final_markdown:
            synth_start = state.final_markdown.index("## Synthesis\n")
            synth_text = state.final_markdown[synth_start:synth_start + 3000]
            # Include synthesis + non-overlapping earlier content
            pre_synth = state.final_markdown[:min(synth_start, 3000)]
            source_text = synth_text + "\n\n---\n\n" + pre_synth

        # Ask LLM to extract key conclusions
        prompt = f"""Extract 3-5 key conclusions from this report. Each conclusion should be
a standalone claim that captures a non-obvious insight from the analysis.
Prioritize insights from the Synthesis section if present.

Report:
{source_text}

Return ONLY a JSON array of objects with "claim" and "evidence" fields.
Example: [{{"claim": "...", "evidence": "..."}}]"""

        conclusions_sid = "report_conclusions"
        result = executor.run_raw(prompt, session_id=conclusions_sid, timeout=60)
        try:
            executor.cleanup_session(conclusions_sid)
        except Exception:
            pass
        if not result.text:
            return

        json_match = re.search(r"\[.*\]", result.text, re.DOTALL)
        if not json_match:
            return

        conclusions = json.loads(json_match.group(0))
        if not isinstance(conclusions, list):
            return

        # Use a synthetic source reference for the report
        report_source_id = f"report_{state.topic.lower().replace(' ', '_')[:30]}"

        # Check if a sources row exists; if not, create a minimal one
        with get_conn_fn() as conn:
            existing = conn.execute(
                "SELECT id FROM sources WHERE id = %s", (report_source_id,)
            ).fetchone()
            if not existing:
                conn.execute(
                    """INSERT INTO sources (id, source_type, title, processing_status)
                       VALUES (%s, 'synthesis', %s, 'complete')
                       ON CONFLICT (id) DO NOTHING""",
                    (report_source_id, f"Report: {state.topic}"),
                )
                conn.commit()

        # Filter valid conclusions first, then embed in parallel order
        valid_conclusions = [
            c for c in conclusions[:5]
            if c.get("claim") and len(c.get("claim", "")) >= 10
        ]
        texts = [c["claim"] for c in valid_conclusions]
        embeddings = embed_batch(texts) if texts else []

        for i, conclusion in enumerate(valid_conclusions):
            claim_text = conclusion["claim"]
            emb = embeddings[i] if i < len(embeddings) and embeddings[i] else None
            insert_claim(
                id=f"syn_{ULID()}",
                source_id=report_source_id,
                claim_text=claim_text,
                claim_type="synthesis_conclusion",
                section=f"report:{state.topic}",
                confidence=0.6,
                evidence_snippet=conclusion.get("evidence", "")[:500],
                evidence_type="synthesis",
                embedding=emb,
                provenance_type="synthesis",
            )

        logger.info("Persisted %d report conclusions as synthesis claims", len(valid_conclusions))
    except Exception:
        logger.warning("Failed to persist report conclusions", exc_info=True)
