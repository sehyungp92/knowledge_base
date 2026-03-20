"""Generate a 3-level AI taxonomy grounded in curated sources (pre-ingestion).

Two-pass approach:
  Pass 1 — Title clustering: feed all 629 source titles grouped by source type
           to identify thematic clusters with frequency and cross-type presence.
  Pass 2 — Summary-enriched synthesis: feed clusters + full summary texts to
           produce the final 3-level taxonomy JSON.

Reads:
  - _references/data/summaries/articles_part_*.md (57 files) — full texts for depth
  - _references/data/sources/*.csv (6 files) — 629 source titles for breadth

Note: For post-ingestion taxonomy regeneration grounded in actual DB data
(claims, landscape signals, deep summaries), use ``scripts/regenerate_taxonomy.py``.

Usage:
    python -m scripts.generate_taxonomy > /tmp/taxonomy_proposal.json
    python -m scripts.generate_taxonomy --pass1-only   # inspect clusters
    python -m scripts.generate_taxonomy --legacy        # original single-pass
    python -m scripts.generate_taxonomy --output /tmp/taxonomy.json
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).parent.parent
SUMMARIES_DIR = REPO_ROOT / "_references" / "data" / "summaries"
SOURCES_DIR = REPO_ROOT / "_references" / "data" / "sources"


# ---------------------------------------------------------------------------
# Data extraction
# ---------------------------------------------------------------------------

def extract_summary_digest(summaries_dir: Path) -> str:
    """Extract section headers + first 3 bullets from each summary file.

    Reduces ~2,200 lines to ~400-token structural digest that preserves
    the thematic structure without overwhelming the LLM context.
    Used only by --legacy mode.
    """
    digest_lines = []

    for path in sorted(summaries_dir.glob("articles_part_*.md")):
        content = path.read_text(encoding="utf-8")
        lines = content.splitlines()
        digest_lines.append(f"\n=== {path.name} ===")

        current_header = None
        bullet_count = 0

        for line in lines:
            stripped = line.strip()
            # Headers (## or ###)
            if stripped.startswith("##"):
                current_header = stripped
                digest_lines.append(stripped)
                bullet_count = 0
            # Bullets (- or *)
            elif stripped.startswith(("-", "*")) and current_header and bullet_count < 3:
                digest_lines.append(f"  {stripped}")
                bullet_count += 1

    return "\n".join(digest_lines)


def extract_full_summaries(summaries_dir: Path) -> list[str]:
    """Read all summary files in full for Pass 2.

    Returns list of full text contents (one per file).
    Globs articles_part_*.md to pick up all 57 files.
    """
    summaries = []
    for path in sorted(summaries_dir.glob("articles_part_*.md")):
        content = path.read_text(encoding="utf-8")
        summaries.append(f"=== {path.name} ===\n{content}")
    if not summaries:
        logger.warning("No articles_part_*.md files found in %s", summaries_dir)
    return summaries


def extract_source_titles(sources_dir: Path) -> list[str]:
    """Extract all source titles from CSV files in the sources directory."""
    titles = []

    for csv_path in sorted(sources_dir.glob("*.csv")):
        try:
            with csv_path.open(encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Try common title column names
                    title = (
                        row.get("title")
                        or row.get("Title")
                        or row.get("name")
                        or row.get("Name")
                    )
                    if title and title.strip():
                        titles.append(title.strip())
        except Exception as e:
            logger.warning("Failed to read %s: %s", csv_path, e)

    return titles


def extract_titles_by_type(sources_dir: Path) -> dict[str, list[str]]:
    """Extract source titles grouped by source type (CSV filename stem).

    Returns e.g. {"ai_paper": ["title1", ...], "vc_blog": [...], ...}
    """
    titles_by_type: dict[str, list[str]] = {}

    for csv_path in sorted(sources_dir.glob("*.csv")):
        source_type = csv_path.stem  # e.g. "ai_paper", "vc_blog"
        type_titles = []
        try:
            with csv_path.open(encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    title = (
                        row.get("title")
                        or row.get("Title")
                        or row.get("name")
                        or row.get("Name")
                    )
                    if title and title.strip():
                        type_titles.append(title.strip())
        except Exception as e:
            logger.warning("Failed to read %s: %s", csv_path, e)

        if type_titles:
            titles_by_type[source_type] = type_titles

    return titles_by_type


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------

def build_clustering_prompt(titles_by_type: dict[str, list[str]]) -> str:
    """Pass 1 prompt: cluster all titles by thematic similarity."""
    sections = []
    total = 0
    for source_type, titles in sorted(titles_by_type.items()):
        total += len(titles)
        title_list = "\n".join(f"  - {t}" for t in titles)
        sections.append(f"### {source_type} ({len(titles)} titles)\n{title_list}")

    titles_block = "\n\n".join(sections)

    return f"""You are analysing a personal AI reading library to identify thematic clusters.

Below are {total} source titles grouped by source type (papers, blogs, podcasts, YouTube).

{titles_block}

=== TASK ===
Identify 30-60 thematic topic clusters from these titles. For each cluster:
1. Give it a snake_case ID and a short human-readable name
2. List 3-5 representative titles from across source types
3. Note how many titles fit this cluster (approximate)
4. Note which source types it appears in (cross-type presence)

Group related clusters under broader categories (5-7 categories).

Think about what a researcher tracking the AI field would want as analytical units:
- Technical research areas (reasoning, RL, architectures, etc.)
- Applied domains (code, robotics, science, etc.)
- Infrastructure/economics (compute, business models, etc.)
- Evaluation/safety (benchmarks, alignment, interpretability, etc.)

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
          "source_types": ["ai_paper", "ai_youtube"],
          "representative_titles": ["Title 1", "Title 2", "Title 3"]
        }}
      ]
    }}
  ]
}}

Be exhaustive — capture every distinct topic area represented in the titles."""


def build_synthesis_prompt(clusters_json: dict, summaries: list[str]) -> str:
    """Pass 2 prompt: synthesise clusters + full summaries into 3-level taxonomy."""
    clusters_str = json.dumps(clusters_json, indent=2)
    summaries_block = "\n\n".join(summaries)

    return f"""You are designing a 3-level taxonomy for a personal AI knowledge base.

=== PASS 1 CLUSTERS (from 629 source titles) ===
{clusters_str}

=== DEEP SUMMARIES (57 articles, full text for depth/nuance) ===
{summaries_block}

=== TASK ===
Synthesise the clusters and summaries into a 3-level taxonomy:

- Level 0 (meta, 5-7 nodes): broad organisational groupings — like "Intelligence Foundations", "AI Capabilities"
- Level 1 (subthemes, 16-22 nodes): primary analytical units — what researchers ask "what's the state of X?" about. These are the units for landscape state summaries, bottleneck tracking, and capability tracking.
- Level 2 (subsubthemes, 35-55 nodes): leaf classification targets — specific enough to attach to individual sources

Design principles:
1. Every level-2 node must be evidenced by at least one cluster or summary topic above
2. Level-1 nodes map to landscape state summaries, bottlenecks, and capabilities tracking
3. Use snake_case IDs; names under 40 chars; descriptions 1 sentence
4. Exclude topics not represented in the source material
5. Merge clusters that are too similar; split clusters that are too broad
6. The summaries reveal sub-topic distinctions and cross-domain connections that titles alone cannot — use them to refine level-2 granularity
7. Include cross-cutting semantic edges between level-1 nodes (enables, constrains, related)

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

Be thorough — include all three levels completely. Every level-1 node needs at least one level-2 child. Every level-2 node needs a contains edge from its level-1 parent. Every level-1 node needs a contains edge from its level-0 meta parent."""


def build_extraction_prompt(digest: str, titles: list[str]) -> str:
    """Legacy single-pass prompt (original approach)."""
    titles_block = "\n".join(f"- {t}" for t in titles[:800])  # cap at 800

    return f"""You are building a 3-level taxonomy of AI topics grounded in a specific reading library.

Below are section headers and key bullets extracted from curated summaries, followed by source titles.

=== SUMMARY DIGEST ===
{digest}

=== SOURCE TITLES ({len(titles)} total, first 800 shown) ===
{titles_block}

=== TASK ===
Design a 3-level taxonomy grounded exclusively in the content above:
- Level 0 (meta, 5-6 nodes): broad organisational groupings only — like "Intelligence Foundations"
- Level 1 (subthemes, 16-20 nodes): primary analytical units — what researchers ask "what's the state of X?" about. These are the units for landscape state summaries, bottleneck tracking, and capability tracking.
- Level 2 (subsubthemes, 35-50 nodes): leaf classification targets — specific enough to attach to individual sources

Rules:
1. Every level-2 node must be evidenced by at least one source title or header above
2. Level-1 nodes map to landscape state summaries, bottlenecks, and capabilities tracking
3. Use snake_case IDs; names under 40 chars; descriptions 1 sentence
4. Exclude topics not represented in the source material
5. Output BOTH hierarchy edges (relationship="contains") AND cross-cutting semantic edges between level-1 nodes

Return a JSON object with this structure:
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

Be thorough — include all three levels completely. The taxonomy will replace the current static 27-theme flat list."""


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------

def call_claude(prompt: str, model: str = "sonnet") -> str:
    """Call Claude via the agent executor and return the text response."""
    try:
        from agents.executor import ClaudeExecutor, DEFAULT_WORKSPACE
        executor = ClaudeExecutor(DEFAULT_WORKSPACE)
        result = executor.run_raw(
            prompt,
            session_id="generate_taxonomy",
            model=model,
            timeout=300,
        )
        return result.text
    except Exception as e:
        logger.error("Failed to call Claude: %s", e)
        raise


def parse_taxonomy_json(text: str) -> dict:
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
# Main flows
# ---------------------------------------------------------------------------

def _run_legacy(args):
    """Original single-pass flow."""
    logger.info("Extracting summary digest from %s", SUMMARIES_DIR)
    digest = extract_summary_digest(SUMMARIES_DIR)
    logger.info("Digest: %d lines", len(digest.splitlines()))

    logger.info("Extracting source titles from %s", SOURCES_DIR)
    titles = extract_source_titles(SOURCES_DIR)
    logger.info("Titles: %d total", len(titles))

    prompt = build_extraction_prompt(digest, titles)
    logger.info("Prompt length: %d chars", len(prompt))

    if args.dry_run:
        print(prompt)
        return

    logger.info("Calling Claude Sonnet (legacy single-pass)...")
    response_text = call_claude(prompt)
    return _parse_and_output(response_text, args)


def _run_two_pass(args):
    """Two-pass flow: title clustering → summary-enriched synthesis."""
    # --- Pass 1: Title clustering ---
    logger.info("Extracting source titles grouped by type from %s", SOURCES_DIR)
    titles_by_type = extract_titles_by_type(SOURCES_DIR)
    total = sum(len(t) for t in titles_by_type.values())
    for st, titles in sorted(titles_by_type.items()):
        logger.info("  %s: %d titles", st, len(titles))
    logger.info("Total: %d titles across %d source types", total, len(titles_by_type))

    clustering_prompt = build_clustering_prompt(titles_by_type)
    logger.info("Pass 1 prompt length: %d chars", len(clustering_prompt))

    if args.dry_run:
        print("=== PASS 1 PROMPT ===")
        print(clustering_prompt)
        print("\n=== PASS 2 would follow with clusters + full summaries ===")
        return

    logger.info("Pass 1: Calling Claude Sonnet for title clustering...")
    pass1_response = call_claude(clustering_prompt)

    try:
        clusters = parse_taxonomy_json(pass1_response)
    except (ValueError, json.JSONDecodeError) as e:
        logger.error("Failed to parse Pass 1 clusters: %s", e)
        logger.error("Raw response:\n%s", pass1_response)
        sys.exit(1)

    categories = clusters.get("categories", [])
    cluster_count = sum(len(c.get("clusters", [])) for c in categories)
    logger.info("Pass 1 result: %d categories, %d clusters", len(categories), cluster_count)

    if args.pass1_only:
        output = json.dumps(clusters, indent=2)
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            logger.info("Pass 1 clusters written to %s", args.output)
        else:
            print(output)
        return

    # --- Pass 2: Summary-enriched synthesis ---
    logger.info("Extracting full summaries from %s", SUMMARIES_DIR)
    summaries = extract_full_summaries(SUMMARIES_DIR)
    logger.info("Loaded %d summary files", len(summaries))

    synthesis_prompt = build_synthesis_prompt(clusters, summaries)
    logger.info("Pass 2 prompt length: %d chars", len(synthesis_prompt))

    logger.info("Pass 2: Calling Claude Sonnet for taxonomy synthesis...")
    pass2_response = call_claude(synthesis_prompt)
    return _parse_and_output(pass2_response, args)


def _parse_and_output(response_text: str, args) -> dict | None:
    """Parse taxonomy JSON from response and write output."""
    try:
        taxonomy = parse_taxonomy_json(response_text)
    except (ValueError, json.JSONDecodeError) as e:
        logger.error("Failed to parse taxonomy JSON: %s", e)
        logger.error("Raw response:\n%s", response_text)
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

    output = json.dumps(taxonomy, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        logger.info("Written to %s", args.output)
    else:
        print(output)

    return taxonomy


def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stderr)
    parser = argparse.ArgumentParser(description="Generate 3-level AI taxonomy from curated sources")
    parser.add_argument("--output", "-o", help="Output JSON file (default: stdout)")
    parser.add_argument("--dry-run", action="store_true", help="Print prompt(s) only, no LLM call")
    parser.add_argument("--pass1-only", action="store_true", help="Output intermediate clusters only (no synthesis)")
    parser.add_argument("--legacy", action="store_true", help="Use original single-pass approach")
    args = parser.parse_args()

    if args.legacy:
        _run_legacy(args)
    else:
        _run_two_pass(args)


if __name__ == "__main__":
    main()
