"""Theme classification via Claude CLI subprocess."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

from ingest.json_parser import parse_json_from_llm
from ingest.theme_validator import load_valid_theme_ids

logger = logging.getLogger(__name__)

# Hardcoded fallback when DB is unavailable — grouped by meta-domain.
# Only level-1 (subtheme) and level-2 (subsubtheme) nodes are listed;
# level-0 meta nodes are never classified into directly.
_STATIC_THEME_BLOCK = """\
agent_systems:
  subthemes: agent_self_evolution, computer_use_and_gui_agents, multi_agent_coordination, software_engineering_agents, tool_use_and_agent_protocols
ai_business_and_economics:
  subthemes: ai_pricing_and_business_models, vertical_ai_and_saas_disruption
ai_market_dynamics:
  subthemes: compute_and_hardware, frontier_lab_competition, model_commoditization_and_open_source
alignment_and_safety:
  subthemes: ai_governance, alignment_methods, hallucination_and_reliability
code_and_software_ai:
  subthemes: ai_software_engineering, code_generation
evaluation_and_benchmarks:
  subthemes: agent_evaluation, benchmark_design
generative_media:
  subthemes: creative_content_generation, image_generation_models, video_and_world_models
interpretability:
  subthemes: mechanistic_interpretability, model_behavior_analysis
knowledge_and_memory:
  subthemes: agent_memory_systems, context_engineering, retrieval_augmented_generation
model_architecture:
  subthemes: adaptive_computation, long_context_and_attention, representation_learning, transformer_alternatives
multimodal_models:
  subthemes: audio_and_speech_models, unified_multimodal_models, vision_language_models
post_training_methods:
  subthemes: finetuning_and_distillation, in_context_and_meta_learning, synthetic_data_generation, test_time_learning
pretraining_and_scaling:
  subthemes: continual_learning, pretraining_data, scaling_laws
reasoning_and_planning:
  subthemes: chain_of_thought, latent_reasoning, mathematical_and_formal_reasoning, search_and_tree_reasoning, test_time_compute_scaling
reinforcement_learning:
  subthemes: policy_optimization, reward_modeling, rl_for_llm_reasoning, rl_theory_and_dynamics
robotics_and_embodied_ai:
  subthemes: robot_learning, spatial_and_3d_intelligence, vision_language_action_models
scientific_and_medical_ai:
  subthemes: ai_for_scientific_discovery, medical_and_biology_ai
startup_and_investment:
  subthemes: startup_formation_and_gtm, vc_and_startup_ecosystem"""

CLASSIFICATION_PROMPT_TEMPLATE = """Classify the following text into relevant AI research themes.

Available themes (use the IDs exactly as written):
{theme_block}

Classification rules:
- Prefer level-2 (subsubtheme) IDs when the text is specifically about that subtopic
- When you assign a level-2 theme, also include its parent level-1 theme
- Maximum 6 theme entries total
- Only include themes with relevance >= 0.3
- level-0 meta themes (meta_foundations, meta_capabilities, etc.) must NEVER be used

Return JSON array of objects with these fields:
  theme_id: the snake_case ID
  relevance: float 0.0–1.0
  level: integer 1 or 2

Example:
[
  {{"theme_id": "chain_of_thought", "relevance": 0.9, "level": 2}},
  {{"theme_id": "reasoning_and_planning", "relevance": 0.75, "level": 1}}
]

TEXT (sampled from beginning, middle, and end — ~4000 chars total):
"""

THEME_PROPOSAL_PROMPT = """The following text was classified into AI research themes, but no theme scored above 0.5 relevance. This suggests the current taxonomy may not adequately cover this content.

Top classification results: {top_themes}

Text excerpt (first 2000 chars):
{text_excerpt}

Propose ONE new theme that would better capture this content.

Determine the appropriate level:
- level=2 (subsubtheme): specific subtopic under an existing level-1 subtheme — auto-approved if parent exists
- level=1 (subtheme): genuinely new analytical area with no existing parent — requires human review

Return JSON:
```json
{{
  "theme_id": "snake_case_id",
  "name": "Human Readable Name",
  "description": "One sentence describing what this theme covers",
  "level": 1 or 2,
  "parent_id": "closest_existing_subtheme_id_or_null",
  "suggested_edges": [
    {{"from": "this_theme_id", "to": "related_theme_id", "relationship": "influences|enables|constrains"}}
  ]
}}
```

Only propose a genuinely new theme — not a rename or subset of an existing one."""


def get_available_themes(get_conn_fn=None) -> str:
    """Query themes from DB and build a formatted theme block for the prompt.

    Falls back to static hardcoded list if DB is unavailable.
    Builds a hierarchical prompt showing level-1 subthemes first,
    then level-2 subsubthemes grouped under their level-1 parents.
    """
    if get_conn_fn is None:
        return _STATIC_THEME_BLOCK

    try:
        with get_conn_fn() as conn:
            rows = conn.execute(
                """SELECT t.id, t.name, t.description, t.level,
                          te.parent_id
                   FROM themes t
                   LEFT JOIN theme_edges te
                     ON te.child_id = t.id AND te.relationship = 'contains'
                   WHERE t.level IN (1, 2)
                   ORDER BY t.level, t.id"""
            ).fetchall()
        if not rows:
            return _STATIC_THEME_BLOCK

        # Build parent→children map for level-2 nodes
        subthemes = {}    # id → row
        subsubthemes = {} # parent_id → [row, ...]

        for r in rows:
            if r["level"] == 1:
                subthemes[r["id"]] = r
            elif r["level"] == 2:
                parent = r["parent_id"]
                if parent:
                    subsubthemes.setdefault(parent, []).append(r)

        lines = ["Subthemes (level-1) and their subsubthemes (level-2):"]
        for st_id, st in subthemes.items():
            desc = f" — {st['description']}" if st.get("description") else ""
            lines.append(f"\n  {st_id} ({st['name']}{desc})")
            children = subsubthemes.get(st_id, [])
            if children:
                for ch in children:
                    ch_desc = f" — {ch['description']}" if ch.get("description") else ""
                    lines.append(f"    - {ch['id']} ({ch['name']}{ch_desc})")

        # Orphaned level-2 nodes (no parent in DB yet)
        all_listed = {r["id"] for r in rows if r["level"] == 1}
        orphan_lines = []
        for r in rows:
            if r["level"] == 2 and (not r["parent_id"] or r["parent_id"] not in all_listed):
                desc = f" — {r['description']}" if r.get("description") else ""
                orphan_lines.append(f"  - {r['id']} ({r['name']}{desc})")
        if orphan_lines:
            lines.append("\nOther subsubthemes:")
            lines.extend(orphan_lines)

        return "\n".join(lines)
    except Exception:
        logger.debug("Failed to fetch themes from DB, using static fallback", exc_info=True)
        return _STATIC_THEME_BLOCK


def _propagate_parent_themes(
    themes: list[dict],
    source_id: str,
    get_conn_fn,
) -> list[dict]:
    """For each level-2 result, upsert its level-1 parent to source_themes.

    Returns an augmented list including propagated parent entries.
    """
    if not get_conn_fn or not themes:
        return themes

    level2_ids = [t["theme_id"] for t in themes if t.get("level") == 2]
    if not level2_ids:
        return themes

    try:
        with get_conn_fn() as conn:
            rows = conn.execute(
                """SELECT te.child_id, te.parent_id, t.level AS parent_level
                   FROM theme_edges te
                   JOIN themes t ON t.id = te.parent_id
                   WHERE te.child_id = ANY(%s)
                     AND te.relationship = 'contains'
                     AND t.level = 1""",
                (level2_ids,),
            ).fetchall()

        # Build child → parent map
        parent_map = {r["child_id"]: r["parent_id"] for r in rows}

        existing_ids = {t["theme_id"] for t in themes}
        new_entries = []

        for t in themes:
            if t.get("level") == 2:
                parent_id = parent_map.get(t["theme_id"])
                if parent_id and parent_id not in existing_ids:
                    propagated_relevance = round(t.get("relevance", 0.5) * 0.85, 4)
                    new_entries.append({
                        "theme_id": parent_id,
                        "relevance": propagated_relevance,
                        "level": 1,
                        "_propagated": True,
                    })
                    existing_ids.add(parent_id)

        if new_entries:
            with get_conn_fn() as conn:
                for entry in new_entries:
                    conn.execute(
                        """INSERT INTO source_themes (source_id, theme_id, relevance)
                           VALUES (%s, %s, %s)
                           ON CONFLICT (source_id, theme_id) DO UPDATE SET
                             relevance = GREATEST(source_themes.relevance, EXCLUDED.relevance)""",
                        (source_id, entry["theme_id"], entry["relevance"]),
                    )
                conn.commit()
            themes = themes + new_entries

    except Exception:
        logger.warning("Failed to propagate parent themes for %s", source_id, exc_info=True)

    return themes


def refresh_static_theme_block(get_conn_fn) -> str:
    """Regenerate _STATIC_THEME_BLOCK from the DB and update the module-level variable.

    Call at gateway startup and after theme materialization so the classifier
    prompt always reflects the current taxonomy.

    Returns the new theme block string.
    """
    global _STATIC_THEME_BLOCK
    try:
        new_block = get_available_themes(get_conn_fn)
        if new_block and new_block != _STATIC_THEME_BLOCK:
            _STATIC_THEME_BLOCK = new_block
            logger.info("Refreshed _STATIC_THEME_BLOCK from DB (%d chars)", len(new_block))
        return _STATIC_THEME_BLOCK
    except Exception:
        logger.warning("Failed to refresh theme block from DB", exc_info=True)
        return _STATIC_THEME_BLOCK


def _maybe_propose_theme(
    clean_text: str,
    source_id: str,
    themes: list[dict],
    executor,
    get_conn_fn,
) -> dict | None:
    """If max relevance < 0.5, propose a new theme via LLM.

    Level-2 proposals with a valid level-1 parent are auto-materialized.
    Level-1 proposals remain pending for human review.

    Returns the proposal dict if created, else None.
    """
    if not get_conn_fn:
        return None

    max_rel = max((t.get("relevance", 0) for t in themes), default=0) if themes else 0
    if max_rel >= 0.5:
        return None

    logger.info("Low theme coverage (max relevance=%.2f) for %s — proposing new theme", max_rel, source_id)

    top_str = ", ".join(
        f"{t['theme_id']}={t.get('relevance', 0):.2f}"
        for t in sorted(themes, key=lambda x: -x.get("relevance", 0))[:3]
    ) if themes else "(none matched)"

    prompt = THEME_PROPOSAL_PROMPT.format(
        top_themes=top_str,
        text_excerpt=clean_text[:2000],
    )

    try:
        result = executor.run_raw(
            prompt,
            session_id=f"propose_theme_{source_id}",
            timeout=180,
        )
        proposal = _parse_theme_proposal(result.text)
        if not proposal or not proposal.get("theme_id"):
            return None

        proposed_level = proposal.get("level", 2)

        from ulid import ULID
        from reading_app.db import insert_theme_proposal, materialize_theme_proposal

        proposal_id = str(ULID())
        row = insert_theme_proposal(
            id=proposal_id,
            proposed_theme_id=proposal["theme_id"],
            name=proposal.get("name", proposal["theme_id"]),
            description=proposal.get("description", ""),
            trigger_reason="low_coverage",
            parent_id=proposal.get("parent_id"),
            suggested_edges=proposal.get("suggested_edges"),
            source_id=source_id,
            level=proposed_level,
        )
        logger.info(
            "Created level-%d theme proposal: %s (%s)",
            proposed_level, proposal["theme_id"], proposal.get("name"),
        )

        # Auto-materialize level-2 proposals with a valid level-1 parent
        if proposed_level == 2 and proposal.get("parent_id"):
            try:
                # Verify parent is a valid level-1 theme
                with get_conn_fn() as conn:
                    parent = conn.execute(
                        "SELECT id, level FROM themes WHERE id = %s AND level = 1",
                        (proposal["parent_id"],),
                    ).fetchone()

                if parent:
                    materialize_theme_proposal(proposal_id)
                    logger.info(
                        "Auto-materialized level-2 theme: %s under %s",
                        proposal["theme_id"], proposal["parent_id"],
                    )
                    # Refresh the static theme block so subsequent classifications see it
                    refresh_static_theme_block(get_conn_fn)
                else:
                    logger.info(
                        "Level-2 proposal %s has invalid parent %s — left pending",
                        proposal["theme_id"], proposal["parent_id"],
                    )
            except Exception:
                logger.warning(
                    "Failed to auto-materialize level-2 proposal %s",
                    proposal["theme_id"], exc_info=True,
                )

        return row
    except Exception:
        logger.warning("Failed to generate theme proposal for %s", source_id, exc_info=True)
        return None


def _parse_theme_proposal(text: str) -> dict | None:
    """Parse a single JSON object from LLM output for theme proposal."""
    return parse_json_from_llm(text, expect=dict)


def classify_themes(
    clean_text: str,
    source_id: str,
    category_hints: list[str] | None = None,
    executor=None,
    get_conn_fn=None,
) -> list[dict]:
    """Classify a source into themes via Claude CLI.

    Args:
        clean_text: Source text
        source_id: Source ID for DB upsert
        category_hints: Pre-mapped theme hints (e.g., from arXiv categories)
        executor: ClaudeExecutor instance
        get_conn_fn: DB connection function for upserting source_themes

    Returns:
        List of {theme_id, relevance, level} dicts.
        Level-2 results automatically propagate to their level-1 parents.
        If a theme proposal was created, the list will contain a special
        entry with key '_proposal' in the last element.
    """
    # Multi-region sampling: begin + middle + end (1333 chars each)
    # For podcasts/videos, the first 4K chars are often intro banter that
    # matches no themes; sampling from three regions captures the real content.
    text_len = len(clean_text)
    region_size = 1333
    begin = clean_text[:region_size]
    mid_start = max(region_size, text_len // 2 - region_size // 2)
    middle = clean_text[mid_start : mid_start + region_size]
    end = clean_text[max(text_len - region_size, mid_start + region_size):]
    truncated = begin + "\n[...]\n" + middle + "\n[...]\n" + end

    theme_block = get_available_themes(get_conn_fn)
    prompt = CLASSIFICATION_PROMPT_TEMPLATE.format(theme_block=theme_block) + truncated
    if category_hints:
        prompt += f"\n\nHint: This content is likely related to: {', '.join(category_hints)}"

    if executor is None:
        from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
        executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    result = executor.run_raw(
        prompt,
        session_id=f"classify_{source_id}",
        timeout=180,
    )

    themes = _parse_theme_output(result.text)

    # Filter by min relevance
    themes = [t for t in themes if t.get("relevance", 0) >= 0.3]

    # Validate theme_ids against DB before insert
    valid_themes = load_valid_theme_ids(get_conn_fn)
    if valid_themes is not None:
        themes = [t for t in themes if t.get("theme_id") in valid_themes]

    # Upsert to DB (direct classifications only — propagated entries handled separately)
    if get_conn_fn and themes:
        with get_conn_fn() as conn:
            for theme in themes:
                conn.execute(
                    """INSERT INTO source_themes (source_id, theme_id, relevance)
                       VALUES (%s, %s, %s)
                       ON CONFLICT (source_id, theme_id) DO UPDATE SET
                         relevance = EXCLUDED.relevance""",
                    (source_id, theme["theme_id"], theme["relevance"]),
                )
            conn.commit()

    # Propagate level-2 results to their level-1 parents
    themes = _propagate_parent_themes(themes, source_id, get_conn_fn)

    # Propose new theme if coverage is low
    proposal = _maybe_propose_theme(clean_text, source_id, themes, executor, get_conn_fn)
    if proposal:
        themes.append({"_proposal": proposal})

    return themes


def _parse_theme_output(text: str) -> list[dict]:
    """Parse JSON array from Claude output."""
    result = parse_json_from_llm(text, expect=list)
    if result is None:
        logger.warning("Failed to parse theme classification output")
        return []
    return result
