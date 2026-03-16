"""Taxonomy health check — meso-level evolution system.

Analyses theme distribution, proposal patterns, and recent summaries to
propose structural taxonomy changes (splits, merges, new nodes, renames).

Usage:
    python -m scripts.taxonomy_health              # run health check
    python -m scripts.taxonomy_health --apply ID   # apply approved proposal
    python -m scripts.taxonomy_health --dry-run    # preview prompt only
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data gathering
# ---------------------------------------------------------------------------

def _gather_health_data(dsn: str, library_path: Path) -> dict:
    """Collect all inputs needed for the health check LLM call."""
    from reading_app.db import get_taxonomy_health_stats

    stats = get_taxonomy_health_stats()

    # Sample 20 recent deep summaries
    summaries = _sample_recent_summaries(dsn, library_path, count=20)

    return {**stats, "recent_summaries": summaries}


def _sample_recent_summaries(dsn: str, library_path: Path, count: int = 20) -> list[str]:
    """Read the most recent deep summaries."""
    from reading_app.db import get_conn

    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, title FROM sources ORDER BY ingested_at DESC LIMIT %s",
            (count * 2,),  # over-fetch in case some lack summaries
        ).fetchall()

    from reading_app.text_utils import truncate_sentences

    summaries = []
    for r in rows:
        if len(summaries) >= count:
            break
        path = library_path / r["id"] / "deep_summary.md"
        if path.exists():
            text = path.read_text(encoding="utf-8").strip()
            if text:
                summaries.append(
                    f"=== {r['title']} ===\n{truncate_sentences(text, 1500)}"
                )
    return summaries


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------

def build_health_check_prompt(data: dict) -> str:
    """Build the LLM prompt for taxonomy health analysis."""
    # Theme distribution
    dist_lines = []
    for t in data["theme_distribution"]:
        avg_rel = f"{t['avg_relevance']:.2f}" if t.get("avg_relevance") else "n/a"
        dist_lines.append(
            f"  {t['id']} (L{t['level']}): {t['source_count']} sources, "
            f"avg_relevance={avg_rel} — {t['name']}"
        )
    dist_block = "\n".join(dist_lines)

    # Recent proposals
    prop_lines = []
    for p in data.get("recent_proposals", []):
        prop_lines.append(
            f"  [{p['status']}] L{p['level']} {p['proposed_theme_id']}: "
            f"{p['name']} — {p.get('description', '')[:80]}"
        )
    prop_block = "\n".join(prop_lines) if prop_lines else "(none)"

    # Recent summaries
    summaries_block = "\n\n".join(data.get("recent_summaries", [])[:20])

    # Hierarchy for context — build compact parent→children view
    parent_map: dict[str, list[str]] = {}
    for e in data.get("hierarchy_edges", []):
        parent_map.setdefault(e["parent_id"], []).append(e["child_id"])
    hier_lines = []
    for parent, children in sorted(parent_map.items()):
        hier_lines.append(f"  {parent} → {', '.join(sorted(children))}")
    hier_block = "\n".join(hier_lines) if hier_lines else "(none)"

    return f"""You are reviewing a taxonomy's health for a personal AI knowledge base.
The knowledge base has {data.get('total_sources', '?')} sources.
Sources since last health check: {data.get('sources_since_check', '?')}.

=== THEME HIERARCHY (parent → children) ===
{hier_block}

=== THEME DISTRIBUTION (id, level, source_count, avg_relevance, name) ===
{dist_block}

=== RECENT THEME PROPOSALS (last 30 days) ===
{prop_block}

=== RECENT DEEP SUMMARIES (newest sources) ===
{summaries_block}

=== TASK ===
Identify taxonomy structural issues. For each issue, propose ONE specific change.

Types of changes:
- split_l2: Split an overloaded L2 into 2-3 new L2s under the same L1 parent
- merge_l2: Merge an underused L2 into a related L2
- new_l2: Add a new L2 under an existing L1 (for coverage gaps)
- new_l1: Propose a new L1 theme (requires human approval of L0 parent)
- rename: Rename a theme for clarity
- reparent: Move a theme to a different parent

Rules:
- Only propose changes with clear evidence (source counts, proposal patterns, summary topics)
- Prefer conservative changes: adding an L2 is cheaper than restructuring an L1
- Max 5 proposals per run
- Each proposal must include: change_type, target_theme_id (null for new), rationale, and proposed_changes

For proposed_changes, use this structure:
- split_l2: {{"new_themes": [{{"id": "...", "name": "...", "description": "..."}}], "parent_id": "..."}}
- merge_l2: {{"merge_into": "target_l2_id"}}
- new_l2: {{"id": "...", "name": "...", "description": "...", "parent_id": "..."}}
- new_l1: {{"id": "...", "name": "...", "description": "...", "suggested_l0_parent": "..."}}
- rename: {{"new_name": "...", "new_description": "..."}}
- reparent: {{"new_parent_id": "..."}}

Return a JSON array of proposals. Each element:
{{
  "change_type": "...",
  "target_theme_id": "..." or null,
  "proposed_changes": {{...}},
  "rationale": "Evidence-based explanation",
  "evidence": {{"source_count": N, "sample_titles": ["..."]}}
}}

If the taxonomy is healthy, return an empty array: []"""


# ---------------------------------------------------------------------------
# Health check execution
# ---------------------------------------------------------------------------

def run_health_check(dsn: str, library_path: Path, dry_run: bool = False) -> list[dict]:
    """Run the taxonomy health check and store proposals."""
    from reading_app.db import ensure_pool, insert_evolution_proposal

    ensure_pool()
    data = _gather_health_data(dsn, library_path)

    prompt = build_health_check_prompt(data)
    logger.info("Health check prompt: %d chars", len(prompt))

    if dry_run:
        preview = prompt[:5000].encode("utf-8", errors="replace").decode("utf-8")
        sys.stdout.buffer.write(f"=== HEALTH CHECK PROMPT ===\n{preview}\n\n... ({len(prompt)} chars total)\n".encode("utf-8"))
        return []

    # Call LLM
    from scripts.regenerate_taxonomy import call_llm, parse_json_response

    logger.info("Calling LLM for taxonomy health analysis...")
    response_text = call_llm(prompt, "taxonomy_health", model="sonnet")

    try:
        proposals = parse_json_response(response_text)
        # Handle both direct array and wrapped object
        if isinstance(proposals, dict):
            proposals = proposals.get("proposals", proposals.get("changes", []))
        if not isinstance(proposals, list):
            proposals = [proposals]
    except (ValueError, json.JSONDecodeError) as e:
        logger.error("Failed to parse health check response: %s", e)
        logger.error("Raw response:\n%s", response_text[:2000])
        return []

    if not proposals:
        logger.info("Taxonomy is healthy — no proposals generated")
        return []

    # Store proposals
    stored = []
    for p in proposals[:5]:  # Cap at 5
        row = insert_evolution_proposal(
            change_type=p["change_type"],
            target_theme_id=p.get("target_theme_id"),
            proposed_changes=p["proposed_changes"],
            rationale=p["rationale"],
            evidence=p.get("evidence"),
        )
        stored.append(row)
        logger.info(
            "Stored proposal #%d: %s on %s — %s",
            row["id"], p["change_type"],
            p.get("target_theme_id", "(new)"),
            p["rationale"][:80],
        )

    logger.info("Health check complete: %d proposals stored", len(stored))
    return stored


# ---------------------------------------------------------------------------
# Apply approved proposals
# ---------------------------------------------------------------------------

def apply_evolution_proposal(dsn: str, proposal_id: int):
    """Apply a single approved evolution proposal."""
    from reading_app.db import (
        ensure_pool, resolve_evolution_proposal, get_conn,
    )
    from ingest.theme_classifier import refresh_static_theme_block

    ensure_pool()

    with get_conn() as conn:
        proposal = conn.execute(
            "SELECT * FROM taxonomy_evolution_proposals WHERE id = %s",
            (proposal_id,),
        ).fetchone()

    if not proposal:
        raise ValueError(f"Proposal {proposal_id} not found")
    if proposal["status"] not in ("pending", "approved"):
        raise ValueError(
            f"Proposal {proposal_id} is '{proposal['status']}', cannot apply"
        )

    changes = proposal["proposed_changes"]
    if isinstance(changes, str):
        changes = json.loads(changes)

    change_type = proposal["change_type"]
    logger.info("Applying proposal #%d: %s", proposal_id, change_type)

    with get_conn() as conn:
        if change_type == "new_l2":
            _apply_new_l2(conn, changes)
        elif change_type == "new_l1":
            _apply_new_l1(conn, changes)
        elif change_type == "split_l2":
            _apply_split_l2(conn, proposal["target_theme_id"], changes)
        elif change_type == "merge_l2":
            _apply_merge_l2(conn, proposal["target_theme_id"], changes)
        elif change_type == "rename":
            _apply_rename(conn, proposal["target_theme_id"], changes)
        elif change_type == "reparent":
            _apply_reparent(conn, proposal["target_theme_id"], changes)
        else:
            raise ValueError(f"Unknown change_type: {change_type}")
        conn.commit()

    # Mark as applied (resolved_at set by DB function)
    resolve_evolution_proposal(proposal_id, "approved")

    # Refresh classifier's static theme block
    refresh_static_theme_block(get_conn)
    logger.info("Proposal #%d applied and theme block refreshed", proposal_id)


def _apply_new_l2(conn, changes: dict):
    """Insert a new L2 theme with parent edge."""
    conn.execute(
        """INSERT INTO themes (id, name, description, level)
           VALUES (%s, %s, %s, 2)
           ON CONFLICT (id) DO NOTHING""",
        (changes["id"], changes["name"], changes.get("description", "")),
    )
    conn.execute(
        """INSERT INTO theme_edges (parent_id, child_id, relationship, strength)
           VALUES (%s, %s, 'contains', 1.0)
           ON CONFLICT (parent_id, child_id) DO NOTHING""",
        (changes["parent_id"], changes["id"]),
    )
    logger.info("Inserted new L2: %s under %s", changes["id"], changes["parent_id"])


def _apply_new_l1(conn, changes: dict):
    """Insert a new L1 theme with parent edge to L0."""
    conn.execute(
        """INSERT INTO themes (id, name, description, level)
           VALUES (%s, %s, %s, 1)
           ON CONFLICT (id) DO NOTHING""",
        (changes["id"], changes["name"], changes.get("description", "")),
    )
    if changes.get("suggested_l0_parent"):
        conn.execute(
            """INSERT INTO theme_edges (parent_id, child_id, relationship, strength)
               VALUES (%s, %s, 'contains', 1.0)
               ON CONFLICT (parent_id, child_id) DO NOTHING""",
            (changes["suggested_l0_parent"], changes["id"]),
        )
    logger.info("Inserted new L1: %s", changes["id"])


def _apply_split_l2(conn, target_theme_id: str, changes: dict):
    """Split an L2 into multiple new L2s, remap sources, remove old."""
    parent_id = changes.get("parent_id")
    for new in changes.get("new_themes", []):
        conn.execute(
            """INSERT INTO themes (id, name, description, level)
               VALUES (%s, %s, %s, 2)
               ON CONFLICT (id) DO NOTHING""",
            (new["id"], new["name"], new.get("description", "")),
        )
        conn.execute(
            """INSERT INTO theme_edges (parent_id, child_id, relationship, strength)
               VALUES (%s, %s, 'contains', 1.0)
               ON CONFLICT (parent_id, child_id) DO NOTHING""",
            (parent_id, new["id"]),
        )

    # Move source_themes from old to first new theme (conservative; reclassify later)
    # Delete duplicates first to avoid PK violation on (source_id, theme_id)
    new_ids = [n["id"] for n in changes.get("new_themes", [])]
    if new_ids:
        conn.execute(
            """DELETE FROM source_themes
               WHERE theme_id = %s
                 AND source_id IN (
                     SELECT source_id FROM source_themes WHERE theme_id = %s
                 )""",
            (target_theme_id, new_ids[0]),
        )
        conn.execute(
            "UPDATE source_themes SET theme_id = %s WHERE theme_id = %s",
            (new_ids[0], target_theme_id),
        )

    # Remove old theme and its edges
    conn.execute("DELETE FROM theme_edges WHERE child_id = %s OR parent_id = %s",
                 (target_theme_id, target_theme_id))
    conn.execute("DELETE FROM themes WHERE id = %s", (target_theme_id,))
    logger.info("Split L2 %s into %s", target_theme_id, new_ids)


def _apply_merge_l2(conn, target_theme_id: str, changes: dict):
    """Merge target L2 into another L2."""
    merge_into = changes["merge_into"]

    # Move source_themes — delete duplicates first to avoid PK violation
    conn.execute(
        """DELETE FROM source_themes
           WHERE theme_id = %s
             AND source_id IN (
                 SELECT source_id FROM source_themes WHERE theme_id = %s
             )""",
        (target_theme_id, merge_into),
    )
    conn.execute(
        "UPDATE source_themes SET theme_id = %s WHERE theme_id = %s",
        (merge_into, target_theme_id),
    )

    # Move landscape FKs (ON CONFLICT safe — these tables use serial PKs)
    for table in ("capabilities", "limitations", "bottlenecks", "breakthroughs"):
        try:
            conn.execute(
                f"UPDATE {table} SET theme_id = %s WHERE theme_id = %s",
                (merge_into, target_theme_id),
            )
        except Exception:
            logger.debug("Could not remap %s for merge", table, exc_info=True)

    # Remove old theme and its edges
    conn.execute("DELETE FROM theme_edges WHERE child_id = %s OR parent_id = %s",
                 (target_theme_id, target_theme_id))
    conn.execute("DELETE FROM themes WHERE id = %s", (target_theme_id,))
    logger.info("Merged L2 %s into %s", target_theme_id, merge_into)


def _apply_rename(conn, target_theme_id: str, changes: dict):
    """Rename a theme."""
    sets = []
    params = []
    if "new_name" in changes:
        sets.append("name = %s")
        params.append(changes["new_name"])
    if "new_description" in changes:
        sets.append("description = %s")
        params.append(changes["new_description"])
    if sets:
        params.append(target_theme_id)
        conn.execute(
            f"UPDATE themes SET {', '.join(sets)} WHERE id = %s", params
        )
    logger.info("Renamed theme %s", target_theme_id)


def _apply_reparent(conn, target_theme_id: str, changes: dict):
    """Move a theme to a different parent."""
    new_parent = changes["new_parent_id"]
    # Remove old contains edge
    conn.execute(
        """DELETE FROM theme_edges
           WHERE child_id = %s AND relationship = 'contains'""",
        (target_theme_id,),
    )
    # Insert new contains edge
    conn.execute(
        """INSERT INTO theme_edges (parent_id, child_id, relationship, strength)
           VALUES (%s, %s, 'contains', 1.0)
           ON CONFLICT (parent_id, child_id) DO NOTHING""",
        (new_parent, target_theme_id),
    )
    logger.info("Reparented %s under %s", target_theme_id, new_parent)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )
    parser = argparse.ArgumentParser(description="Taxonomy health check")
    parser.add_argument(
        "--apply", type=int, metavar="PROPOSAL_ID",
        help="Apply an approved evolution proposal",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the health check prompt without calling LLM",
    )
    args = parser.parse_args()

    from reading_app.config import Config
    from reading_app.db import init_pool

    config = Config()
    init_pool(config.postgres_dsn)

    if args.apply:
        apply_evolution_proposal(config.postgres_dsn, args.apply)
    else:
        run_health_check(config.postgres_dsn, config.library_path, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
