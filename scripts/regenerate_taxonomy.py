"""Post-ingestion taxonomy regeneration grounded in all ingested data.

Two modes:
  Generate: two-pass LLM pipeline using titles, theme stats, landscape
            signals, and sampled deep summaries → taxonomy JSON proposal.
  Apply:    backup current seed_themes.py, write new taxonomy, truncate
            themes + re-seed, reclassify all sources, remap landscape FKs.

Usage:
    python -m scripts.regenerate_taxonomy -o scripts/taxonomy_v2.json        # generate
    python -m scripts.regenerate_taxonomy --apply scripts/taxonomy_v2.json   # apply
    python -m scripts.regenerate_taxonomy --dry-run                  # preview prompts
"""

from __future__ import annotations

import argparse
import json
import logging
import random
import re
import shutil
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import psycopg
from psycopg.rows import dict_row

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Data queries
# ---------------------------------------------------------------------------

def query_source_titles_by_type(dsn: str) -> dict[str, list[str]]:
    """Query all source titles (with URL domain hint) grouped by source_type."""
    titles: dict[str, list[str]] = {}
    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        rows = conn.execute(
            "SELECT title, source_type, url FROM sources ORDER BY source_type, title"
        ).fetchall()
    from urllib.parse import urlparse

    for r in rows:
        st = r["source_type"] or "unknown"
        title = r["title"] or "(untitled)"
        # Append URL domain hint so the LLM can detect VC/business sources
        url = r.get("url") or ""
        if url:
            try:
                domain = urlparse(url).netloc.removeprefix("www.")
                if domain:
                    title = f"{title} ({domain})"
            except Exception:
                pass
        titles.setdefault(st, []).append(title)
    return titles


def query_theme_usage_stats(dsn: str) -> list[dict]:
    """Theme usage stats: id, name, level, source count."""
    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        return conn.execute("""
            SELECT t.id, t.name, t.level, count(st.source_id) AS source_count
            FROM themes t
            LEFT JOIN source_themes st ON t.id = st.theme_id
            GROUP BY t.id, t.name, t.level
            ORDER BY t.level, source_count DESC
        """).fetchall()


def query_landscape_digest(dsn: str) -> dict:
    """Top capabilities, limitations, and bottlenecks (descriptions only, capped)."""
    digest = {}
    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        digest["capabilities"] = [
            r["description"][:200] for r in conn.execute(
                "SELECT description FROM capabilities ORDER BY maturity DESC NULLS LAST LIMIT 30"
            ).fetchall()
        ]
        digest["limitations"] = [
            r["description"][:200] for r in conn.execute(
                "SELECT description FROM limitations ORDER BY signal_strength DESC NULLS LAST LIMIT 30"
            ).fetchall()
        ]
        digest["bottlenecks"] = [
            r["description"][:200] for r in conn.execute(
                """SELECT DISTINCT ON (theme_id) description
                   FROM bottlenecks
                   ORDER BY theme_id, confidence DESC NULLS LAST"""
            ).fetchall()
        ]
    return digest


def query_cross_theme_implications(dsn: str, limit: int = 30) -> list[dict]:
    """Top cross-theme implications by confidence."""
    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        return conn.execute(
            """SELECT source_theme_id, target_theme_id, implication, confidence
               FROM cross_theme_implications
               ORDER BY confidence DESC NULLS LAST
               LIMIT %s""",
            (limit,),
        ).fetchall()


def sample_deep_summaries(
    library_path: Path,
    dsn: str,
    target: int = 80,
) -> list[str]:
    """Sample ~target deep summaries stratified by claim count and theme diversity.

    Strategy: 30 from high-claim sources, 30 from diverse themes, 20 random.
    """
    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        # High-claim sources
        high_claim = conn.execute("""
            SELECT s.id, count(c.id) AS claim_count
            FROM sources s
            LEFT JOIN claims c ON c.source_id = s.id
            GROUP BY s.id
            ORDER BY claim_count DESC
            LIMIT 30
        """).fetchall()

        # Diverse themes: sources from themes with fewest sources
        diverse = conn.execute("""
            SELECT DISTINCT ON (st.theme_id) s.id
            FROM source_themes st
            JOIN sources s ON s.id = st.source_id
            ORDER BY st.theme_id, random()
            LIMIT 30
        """).fetchall()

        # All source IDs for random sampling
        all_ids = [
            r["id"] for r in conn.execute("SELECT id FROM sources").fetchall()
        ]

    selected_ids = set()
    for r in high_claim:
        selected_ids.add(r["id"])
    for r in diverse:
        selected_ids.add(r["id"])

    # Fill remaining with random
    remaining = [sid for sid in all_ids if sid not in selected_ids]
    random.shuffle(remaining)
    for sid in remaining[:max(0, target - len(selected_ids))]:
        selected_ids.add(sid)

    # Read summaries
    summaries = []
    from reading_app.text_utils import truncate_sentences
    for sid in selected_ids:
        summary_path = library_path / sid / "deep_summary.md"
        if summary_path.exists():
            text = summary_path.read_text(encoding="utf-8").strip()
            if text:
                # Cap each summary to ~2000 chars
                summaries.append(
                    f"=== Source {sid} ===\n{truncate_sentences(text, 2000)}"
                )
    return summaries


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------

def build_pass1_prompt(
    titles_by_type: dict[str, list[str]],
    theme_stats: list[dict],
    landscape_digest: dict,
) -> str:
    """Pass 1: enriched clustering from titles + current theme stats + landscape."""
    # Titles block
    sections = []
    total = 0
    for st, titles in sorted(titles_by_type.items()):
        total += len(titles)
        title_list = "\n".join(f"  - {t}" for t in titles)
        sections.append(f"### {st} ({len(titles)} titles)\n{title_list}")
    titles_block = "\n\n".join(sections)

    # Theme stats block
    stats_lines = []
    for s in theme_stats:
        stats_lines.append(
            f"  {s['id']} (L{s['level']}): {s['source_count']} sources — {s['name']}"
        )
    stats_block = "\n".join(stats_lines)

    # Landscape block
    caps = "\n".join(f"  - {c}" for c in landscape_digest.get("capabilities", [])[:30])
    lims = "\n".join(f"  - {l}" for l in landscape_digest.get("limitations", [])[:30])
    bots = "\n".join(f"  - {b}" for b in landscape_digest.get("bottlenecks", []))

    return f"""You are analysing a personal AI reading library to identify thematic clusters.
The library has been fully ingested — below is data from the actual database.

=== SOURCE TITLES ({total} sources) ===
{titles_block}

=== CURRENT THEME TAXONOMY (usage stats) ===
{stats_block}

=== LANDSCAPE SIGNALS ===
Top capabilities:
{caps}

Top limitations:
{lims}

All bottlenecks:
{bots}

=== DOMAIN LENSES (ensure coverage) ===
The taxonomy must cover the FULL AI landscape, including:
- Technical foundations (architectures, training, inference)
- Applied capabilities (code, agents, science, creative)
- Reliability & safety (alignment, evaluation, interpretability)
- Infrastructure & compute (hardware, efficiency, energy)
- Business & investment ecosystem (venture capital, startup formation,
  funding rounds, competitive moats, market structure, exits/IPOs,
  valuations, business model innovation, vertical AI companies,
  AI-native vs AI-augmented businesses, open source vs proprietary dynamics)

Do NOT collapse the business/investment dimension into a single cluster.
VC funding patterns, startup ecosystem dynamics, and market structure
are analytically distinct from model pricing or SaaS disruption.

=== TASK ===
Identify 30-60 thematic topic clusters from these titles and landscape signals.
For each cluster:
1. Give it a snake_case ID and a short human-readable name
2. List 3-5 representative titles from across source types
3. Note how many titles fit this cluster (approximate)
4. Note which source types it appears in (cross-type presence)

Flag gaps, merges, or splits vs the current taxonomy:
- GAPS: topics well-represented in sources but missing from current themes
- MERGES: current themes that are too similar and should be combined
- SPLITS: current themes that are too broad and should be split

Group related clusters under broader categories (5-7 categories).

Return JSON:
{{
  "categories": [
    {{
      "name": "Category Name",
      "clusters": [
        {{
          "id": "snake_case_id",
          "name": "Human Name",
          "title_count": 25,
          "source_types": ["paper", "video"],
          "representative_titles": ["Title 1", "Title 2", "Title 3"]
        }}
      ]
    }}
  ],
  "taxonomy_changes": {{
    "gaps": ["description of gap 1", ...],
    "merges": ["merge X and Y because...", ...],
    "splits": ["split Z into A and B because...", ...]
  }}
}}

Be exhaustive — capture every distinct topic area represented in the data."""


def build_pass2_prompt(
    clusters_json: dict,
    summaries: list[str],
    theme_stats: list[dict],
    landscape_digest: dict,
    implications: list[dict],
) -> str:
    """Pass 2: summary-enriched synthesis into final 3-level taxonomy."""
    clusters_str = json.dumps(clusters_json, indent=2)

    from reading_app.text_utils import budget_context
    summary_sections = [(5, f"Summary {i+1}", s) for i, s in enumerate(summaries)]
    summaries_block = budget_context(summary_sections, 150_000)

    # Current taxonomy stats
    stats_lines = []
    for s in theme_stats:
        stats_lines.append(
            f"  {s['id']} (L{s['level']}): {s['source_count']} sources"
        )
    stats_block = "\n".join(stats_lines)

    # Implications
    impl_lines = []
    for imp in implications:
        impl_lines.append(
            f"  {imp['source_theme_id']} → {imp['target_theme_id']}: "
            f"{imp['implication']} (conf={imp.get('confidence', '?')})"
        )
    impl_block = "\n".join(impl_lines) if impl_lines else "(none)"

    caps = "\n".join(f"  - {c}" for c in landscape_digest.get("capabilities", [])[:50])
    lims = "\n".join(f"  - {l}" for l in landscape_digest.get("limitations", [])[:50])
    bots = "\n".join(f"  - {b}" for b in landscape_digest.get("bottlenecks", []))

    return f"""You are designing a 3-level taxonomy for a personal AI knowledge base.
All data below comes from the actual ingested library.

=== PASS 1 CLUSTERS (from ingested source titles) ===
{clusters_str}

=== SAMPLED DEEP SUMMARIES (from library) ===
{summaries_block}

=== CURRENT TAXONOMY WITH USAGE STATS ===
{stats_block}

=== CROSS-THEME IMPLICATIONS (top 30) ===
{impl_block}

=== LANDSCAPE SIGNALS ===
Top capabilities:
{caps}

Top limitations:
{lims}

All bottlenecks:
{bots}

=== TASK ===
Synthesise the clusters, summaries, and landscape signals into a 3-level taxonomy:

- Level 0 (meta, 5-7 nodes): broad organisational groupings
- Level 1 (subthemes, 16-22 nodes): primary analytical units — what researchers ask
  "what's the state of X?" about. Units for landscape state summaries, bottleneck
  tracking, and capability tracking.
- Level 2 (subsubthemes, 35-55 nodes): leaf classification targets — specific enough
  to attach to individual sources

Design principles:
1. Every level-2 node must be evidenced by at least one cluster or summary topic
2. Level-1 nodes map to landscape state summaries, bottlenecks, and capabilities tracking
3. Use snake_case IDs; names under 40 chars; descriptions 1 sentence
4. Exclude topics not represented in the source material
5. Merge clusters that are too similar; split clusters that are too broad
6. The summaries reveal sub-topic distinctions and cross-domain connections
7. Include cross-cutting semantic edges between level-1 nodes (enables, constrains, related)
8. Preserve well-populated themes from current taxonomy; rename/merge poorly populated ones
9. The business/investment ecosystem of AI (VC, startups, market dynamics,
   competitive moats, exits) must be represented as first-class analytical
   units at L1, not collapsed into a single catch-all theme
10. L1 themes should be things you'd write a "State of X" report about —
    if a theme is too broad for a single coherent state summary, split it
11. Preserve the existing theme proposal auto-materialization contract:
    L2 nodes with valid L1 parents can be auto-added; L1 requires human review

Return JSON:
{{
  "nodes": [
    {{"id": "snake_case_id", "name": "Human Name", "description": "One sentence.", "level": 0}},
    ...
  ],
  "edges": [
    {{"parent_id": "meta_foundations", "child_id": "reasoning_and_planning", "relationship": "contains", "strength": 1.0}},
    {{"parent_id": "world_models", "child_id": "robotics", "relationship": "enables", "strength": 0.8}},
    ...
  ]
}}

Be thorough — include all three levels completely. Every level-1 node needs at least
one level-2 child. Every level-2 node needs a contains edge from its level-1 parent.
Every level-1 node needs a contains edge from its level-0 meta parent."""


# ---------------------------------------------------------------------------
# LLM calls
# ---------------------------------------------------------------------------

def call_llm(prompt: str, session_id: str, model: str = "sonnet") -> str:
    """Call Claude via ClaudeExecutor and return text response."""
    from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
    executor = ClaudeExecutor(DEFAULT_WORKSPACE)
    result = executor.run_raw(
        prompt,
        session_id=session_id,
        model=model,
        timeout=1200,
    )
    if not result.success:
        raise RuntimeError(f"LLM call failed: {result.stderr[:300]}")
    return result.text


def parse_json_response(text: str) -> dict:
    """Extract and parse JSON from LLM response."""
    # Try code block first
    match = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))

    # Try raw JSON object
    brace_start = text.find("{")
    if brace_start >= 0:
        depth = 0
        for i in range(brace_start, len(text)):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(text[brace_start : i + 1])

    raise ValueError("No JSON found in LLM response")


# ---------------------------------------------------------------------------
# Generate mode
# ---------------------------------------------------------------------------

def generate_taxonomy(dsn: str, library_path: Path, output_path: Path, dry_run: bool = False):
    """Two-pass taxonomy generation grounded in ingested data."""
    logger.info("=== Pass 1: Enriched clustering ===")

    titles_by_type = query_source_titles_by_type(dsn)
    total = sum(len(t) for t in titles_by_type.values())
    for st, titles in sorted(titles_by_type.items()):
        logger.info("  %s: %d titles", st, len(titles))
    logger.info("Total: %d sources", total)

    theme_stats = query_theme_usage_stats(dsn)
    landscape_digest = query_landscape_digest(dsn)

    pass1_prompt = build_pass1_prompt(titles_by_type, theme_stats, landscape_digest)
    logger.info("Pass 1 prompt: %d chars", len(pass1_prompt))

    if dry_run:
        print("=== PASS 1 PROMPT ===")
        print(pass1_prompt[:5000])
        print(f"\n... ({len(pass1_prompt)} chars total)")
        print("\n=== PASS 2 would follow with clusters + deep summaries ===")
        return

    logger.info("Pass 1: Calling LLM for title clustering...")
    pass1_text = call_llm(pass1_prompt, "regen_taxonomy_pass1")

    try:
        clusters = parse_json_response(pass1_text)
    except (ValueError, json.JSONDecodeError) as e:
        logger.error("Failed to parse Pass 1: %s", e)
        logger.error("Raw response:\n%s", pass1_text[:2000])
        sys.exit(1)

    categories = clusters.get("categories", [])
    cluster_count = sum(len(c.get("clusters", [])) for c in categories)
    logger.info("Pass 1: %d categories, %d clusters", len(categories), cluster_count)

    # --- Pass 2: Summary-enriched synthesis ---
    logger.info("=== Pass 2: Summary-enriched synthesis ===")
    summaries = sample_deep_summaries(library_path, dsn)
    logger.info("Sampled %d deep summaries", len(summaries))

    implications = query_cross_theme_implications(dsn)
    logger.info("Loaded %d cross-theme implications", len(implications))

    pass2_prompt = build_pass2_prompt(
        clusters, summaries, theme_stats, landscape_digest, implications,
    )
    logger.info("Pass 2 prompt: %d chars", len(pass2_prompt))

    logger.info("Pass 2: Calling LLM for taxonomy synthesis...")
    pass2_text = call_llm(pass2_prompt, "regen_taxonomy_pass2")

    try:
        taxonomy = parse_json_response(pass2_text)
    except (ValueError, json.JSONDecodeError) as e:
        logger.error("Failed to parse Pass 2: %s", e)
        logger.error("Raw response:\n%s", pass2_text[:2000])
        sys.exit(1)

    nodes = taxonomy.get("nodes", [])
    edges = taxonomy.get("edges", [])
    meta = [n for n in nodes if n.get("level") == 0]
    subthemes = [n for n in nodes if n.get("level") == 1]
    subsubthemes = [n for n in nodes if n.get("level") == 2]
    logger.info(
        "Taxonomy: %d meta + %d subthemes + %d subsubthemes, %d edges",
        len(meta), len(subthemes), len(subsubthemes), len(edges),
    )

    # Write output
    output = json.dumps(taxonomy, indent=2)
    output_path.write_text(output, encoding="utf-8")
    logger.info("Written taxonomy to %s", output_path)

    # Also generate seed_themes.py code
    code = _generate_seed_themes_code(taxonomy)
    code_path = output_path.with_suffix(".py")
    code_path.write_text(code, encoding="utf-8")
    logger.info("Written seed_themes.py code to %s", code_path)


# ---------------------------------------------------------------------------
# Code generation
# ---------------------------------------------------------------------------

def _generate_seed_themes_code(taxonomy: dict) -> str:
    """Generate seed_themes.py Python code from taxonomy JSON."""
    nodes = taxonomy.get("nodes", [])
    edges = taxonomy.get("edges", [])

    # Separate hierarchy and cross-cutting edges
    hierarchy_edges = [e for e in edges if e.get("relationship") == "contains"]
    cross_edges = [e for e in edges if e.get("relationship") != "contains"]

    # Build ALL_NODES
    node_lines = []
    for level in (0, 1, 2):
        level_nodes = [n for n in nodes if n.get("level") == level]
        if not level_nodes:
            continue
        level_names = {0: "Level 0 — Meta", 1: "Level 1 — Subthemes", 2: "Level 2 — Subsubthemes"}
        node_lines.append(f"    # {level_names.get(level, f'Level {level}')}")
        for n in level_nodes:
            desc = n.get("description", "").replace('"', '\\"')
            node_lines.append(
                f'    ("{n["id"]}", "{n["name"]}", "{desc}", {level}),'
            )
        node_lines.append("")

    # Build HIERARCHY_EDGES
    hier_lines = []
    for e in hierarchy_edges:
        hier_lines.append(
            f'    ("{e["parent_id"]}", "{e["child_id"]}", "contains", {e.get("strength", 1.0)}),'
        )

    # Build CROSS_CUTTING_EDGES
    cross_lines = []
    for e in cross_edges:
        cross_lines.append(
            f'    ("{e["parent_id"]}", "{e["child_id"]}", "{e.get("relationship", "related")}", {e.get("strength", 0.6)}),'
        )

    nodes_block = "\n".join(node_lines)
    hier_block = "\n".join(hier_lines)
    cross_block = "\n".join(cross_lines) if cross_lines else "    # (none)"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    return f'''"""Seed the 3-level AI taxonomy DAG. Idempotent (ON CONFLICT DO NOTHING).

Auto-generated by scripts/regenerate_taxonomy.py on {timestamp}.
"""

from __future__ import annotations

import logging

import psycopg
from psycopg.rows import dict_row

logger = logging.getLogger(__name__)

ALL_NODES = [
{nodes_block}
]

HIERARCHY_EDGES = [
{hier_block}
]

CROSS_CUTTING_EDGES = [
{cross_block}
]


def seed_themes(dsn: str):
    """Insert all themes and edges. Idempotent."""
    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        for theme_id, name, description, level in ALL_NODES:
            conn.execute(
                """INSERT INTO themes (id, name, description, level)
                   VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING""",
                (theme_id, name, description, level),
            )

        all_edges = HIERARCHY_EDGES + CROSS_CUTTING_EDGES
        for parent_id, child_id, relationship, strength in all_edges:
            conn.execute(
                """INSERT INTO theme_edges (parent_id, child_id, relationship, strength)
                   VALUES (%s, %s, %s, %s) ON CONFLICT (parent_id, child_id) DO NOTHING""",
                (parent_id, child_id, relationship, strength),
            )

        conn.commit()

    meta = [n for n in ALL_NODES if n[3] == 0]
    subthemes = [n for n in ALL_NODES if n[3] == 1]
    subsubthemes = [n for n in ALL_NODES if n[3] == 2]
    logger.info(
        "Seeded %d meta + %d subthemes + %d subsubthemes (%d total), %d edges",
        len(meta), len(subthemes), len(subsubthemes), len(ALL_NODES), len(all_edges),
    )


def main():
    logging.basicConfig(level=logging.INFO)
    from reading_app.config import Config
    config = Config()
    seed_themes(config.postgres_dsn)


if __name__ == "__main__":
    main()
'''


# ---------------------------------------------------------------------------
# Apply mode
# ---------------------------------------------------------------------------

def apply_taxonomy(dsn: str, library_path: Path, taxonomy_path: Path):
    """Apply a taxonomy JSON: backup, rewrite seed_themes.py, truncate, re-seed, reclassify."""
    taxonomy = json.loads(taxonomy_path.read_text(encoding="utf-8"))
    nodes = taxonomy.get("nodes", [])
    edges = taxonomy.get("edges", [])

    logger.info(
        "Applying taxonomy: %d nodes, %d edges",
        len(nodes), len(edges),
    )

    # 1. Backup current seed_themes.py
    seed_path = PROJECT_ROOT / "db" / "seed_themes.py"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = PROJECT_ROOT / "db" / f"seed_themes_backup_{timestamp}.py"
    if seed_path.exists():
        shutil.copy2(seed_path, backup_path)
        logger.info("Backed up seed_themes.py → %s", backup_path.name)

    # 2. Write new seed_themes.py
    code = _generate_seed_themes_code(taxonomy)
    seed_path.write_text(code, encoding="utf-8")
    logger.info("Wrote new seed_themes.py (%d chars)", len(code))

    # 3. Export landscape entity → old theme mappings before truncate
    landscape_mappings = _export_landscape_theme_mappings(dsn)

    # 4. Truncate themes CASCADE (clears themes, theme_edges, source_themes,
    #    capability/limitation/bottleneck/breakthrough theme FKs)
    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        conn.execute("TRUNCATE themes CASCADE")
        conn.commit()
    logger.info("Truncated themes CASCADE")

    # 5. Re-seed with new taxonomy
    # Import the freshly written module
    import importlib
    import db.seed_themes
    importlib.reload(db.seed_themes)
    db.seed_themes.seed_themes(dsn)
    logger.info("Re-seeded themes from new taxonomy")

    # 6. Remap landscape entity theme FKs
    _remap_landscape_themes(dsn, landscape_mappings)

    # 7. Reclassify all sources against new taxonomy
    _reclassify_all_sources(dsn, library_path)

    # 8. Refresh _STATIC_THEME_BLOCK
    from reading_app.db import get_conn
    from ingest.theme_classifier import refresh_static_theme_block
    refresh_static_theme_block(get_conn)
    logger.info("Refreshed _STATIC_THEME_BLOCK")

    logger.info("Taxonomy applied successfully")


def _export_landscape_theme_mappings(dsn: str) -> dict[str, list[dict]]:
    """Export {entity_type: [{id, old_theme_id, old_theme_name}, ...]}."""
    mappings: dict[str, list[dict]] = {}
    tables = ["capabilities", "limitations", "bottlenecks", "breakthroughs"]

    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        for table in tables:
            try:
                rows = conn.execute(f"""
                    SELECT e.id, e.theme_id, t.name AS theme_name
                    FROM {table} e
                    LEFT JOIN themes t ON t.id = e.theme_id
                    WHERE e.theme_id IS NOT NULL
                """).fetchall()
                mappings[table] = [dict(r) for r in rows]
            except Exception:
                logger.debug("Could not export %s theme mappings", table, exc_info=True)
                mappings[table] = []

    total = sum(len(v) for v in mappings.values())
    logger.info("Exported %d landscape entity → theme mappings", total)
    return mappings


def _remap_landscape_themes(dsn: str, mappings: dict[str, list[dict]]):
    """Attempt to map old theme names → new theme IDs using similarity."""
    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        # Build new theme name → id lookup
        new_themes = conn.execute(
            "SELECT id, name FROM themes WHERE level IN (1, 2)"
        ).fetchall()
        name_to_id: dict[str, str] = {}
        for t in new_themes:
            name_to_id[t["name"].lower()] = t["id"]
            # Also index by id for exact matches
            name_to_id[t["id"]] = t["id"]

        remapped = 0
        unmapped = []

        for table, entities in mappings.items():
            for entity in entities:
                old_theme_id = entity.get("theme_id")
                old_name = (entity.get("theme_name") or "").lower()
                new_id = None

                # Try exact ID match first (same theme ID in new taxonomy)
                if old_theme_id in name_to_id:
                    new_id = name_to_id[old_theme_id]
                # Try name match
                elif old_name and old_name in name_to_id:
                    new_id = name_to_id[old_name]
                # Try pg_trgm similarity if available
                elif old_name:
                    try:
                        match = conn.execute(
                            """SELECT id, name, similarity(lower(name), %s) AS sim
                               FROM themes
                               WHERE level IN (1, 2)
                                 AND similarity(lower(name), %s) > 0.3
                               ORDER BY sim DESC
                               LIMIT 1""",
                            (old_name, old_name),
                        ).fetchone()
                        if match:
                            new_id = match["id"]
                    except Exception:
                        # pg_trgm extension may not be available
                        pass

                if new_id:
                    try:
                        conn.execute(
                            f"UPDATE {table} SET theme_id = %s WHERE id = %s",
                            (new_id, entity["id"]),
                        )
                        remapped += 1
                    except Exception:
                        logger.debug("Failed to remap %s.%s", table, entity["id"], exc_info=True)
                else:
                    unmapped.append(f"{table}.{entity['id']} (was: {old_theme_id})")

        conn.commit()

    logger.info("Remapped %d landscape entity theme FKs", remapped)
    if unmapped:
        logger.warning("Unmapped entities (%d):", len(unmapped))
        for u in unmapped[:20]:
            logger.warning("  %s", u)
        if len(unmapped) > 20:
            logger.warning("  ... and %d more", len(unmapped) - 20)


def _reclassify_all_sources(dsn: str, library_path: Path):
    """Re-classify all sources against the new taxonomy."""
    from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
    from reading_app.db import init_pool, get_conn
    from ingest.theme_classifier import classify_themes

    init_pool(dsn)
    executor = ClaudeExecutor(DEFAULT_WORKSPACE)

    with psycopg.connect(dsn, row_factory=dict_row) as conn:
        sources = conn.execute("SELECT id FROM sources ORDER BY id").fetchall()

    total = len(sources)
    logger.info("Reclassifying %d sources against new taxonomy...", total)

    completed = 0
    lock = threading.Lock()

    def _classify_one(source_id: str):
        nonlocal completed
        clean_path = library_path / source_id / "clean.md"
        if not clean_path.exists():
            logger.debug("No clean.md for %s, skipping", source_id)
            return

        text = clean_path.read_text(encoding="utf-8")
        if len(text) < 100:
            logger.debug("Clean text too short for %s, skipping", source_id)
            return

        themes = classify_themes(
            clean_text=text,
            source_id=source_id,
            executor=executor,
            get_conn_fn=get_conn,
        )

        theme_ids = [t["theme_id"] for t in themes if "theme_id" in t]
        with lock:
            completed += 1
            logger.info("[%d/%d] Reclassified %s → %s", completed, total, source_id, theme_ids)

    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {
            pool.submit(_classify_one, r["id"]): r["id"]
            for r in sources
        }
        for future in as_completed(futures):
            exc = future.exception()
            if exc:
                sid = futures[future]
                logger.error("Reclassification failed for %s: %s", sid, exc)

    logger.info("Reclassification complete: %d/%d sources processed", completed, total)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )
    parser = argparse.ArgumentParser(
        description="Post-ingestion taxonomy regeneration",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output taxonomy JSON file (generate mode)",
    )
    parser.add_argument(
        "--apply",
        metavar="TAXONOMY_JSON",
        help="Apply a taxonomy JSON file (apply mode)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print prompts without calling LLM",
    )
    args = parser.parse_args()

    from reading_app.config import Config
    config = Config()

    if args.apply:
        from reading_app.db import init_pool
        init_pool(config.postgres_dsn)
        apply_taxonomy(
            config.postgres_dsn,
            config.library_path,
            Path(args.apply),
        )
    elif args.output:
        generate_taxonomy(
            config.postgres_dsn,
            config.library_path,
            Path(args.output),
            dry_run=args.dry_run,
        )
    else:
        parser.error("Specify either -o OUTPUT (generate) or --apply TAXONOMY_JSON (apply)")


if __name__ == "__main__":
    main()
