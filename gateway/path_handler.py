"""Direct Python handler for /path jobs.

Finds and explains connection paths between two sources in the
knowledge graph. No LLM needed -- pure data retrieval and formatting.
"""

from __future__ import annotations

import re
import time
from typing import Callable

import structlog

from gateway.models import Event, Job

logger = structlog.get_logger(__name__)

_ID_RE = re.compile(r"[0-9A-Z]{26}")  # ULID pattern


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def handle_path_job(
    event: Event,
    job: Job,
    config,
    executor,
    *,
    on_progress: Callable[[str], None] | None = None,
) -> str:
    """Run /path directly."""
    text = event.payload.get("text", "")
    log = logger.bind(job_id=job.id)
    log.info("path_handler_start")
    t0 = time.monotonic()

    from reading_app.db import ensure_pool
    ensure_pool()

    parsed = _parse_command(text)
    if parsed is None:
        return (
            "Usage: `/path <source_a> <source_b>`\n\n"
            "Accepts source IDs (ULIDs) or partial title matches.\n\n"
            "Example: `/path 01H... 01H...`\n"
            "Example: `/path \"attention is all\" \"scaling laws\"`"
        )

    ref_a, ref_b = parsed
    log = log.bind(ref_a=ref_a[:40], ref_b=ref_b[:40])

    if on_progress:
        on_progress(f"Resolving sources and finding paths...")

    # Resolve both source references
    source_a = _resolve_source(ref_a)
    if not source_a:
        return f"Could not find a source matching: `{ref_a}`"

    source_b = _resolve_source(ref_b)
    if not source_b:
        return f"Could not find a source matching: `{ref_b}`"

    id_a = source_a["id"]
    id_b = source_b["id"]
    title_a = source_a.get("title", id_a)
    title_b = source_b.get("title", id_b)

    if id_a == id_b:
        return f"Both references resolve to the same source: **{title_a}** (`{id_a}`)"

    log = log.bind(source_a=id_a, source_b=id_b)

    if on_progress:
        on_progress(f"Finding paths between \"{_truncate(title_a, 40)}\" and \"{_truncate(title_b, 40)}\"...")

    # Find paths via source_edges (recursive CTE)
    edge_paths = _find_edge_paths(id_a, id_b)

    # Find connections via shared concepts
    shared_concepts = _find_shared_concepts(id_a, id_b)

    if not edge_paths and not shared_concepts:
        elapsed = time.monotonic() - t0
        log.info("path_handler_no_path", elapsed_s=round(elapsed, 1))
        return (
            f"**No path found** between:\n"
            f"- **{title_a}** (`{id_a[:12]}...`)\n"
            f"- **{title_b}** (`{id_b[:12]}...`)\n\n"
            "These sources are not connected through edges, shared concepts, "
            "or claim relationships in the current knowledge graph."
        )

    # Format the narrative
    result = _format_path_narrative(
        title_a, id_a, title_b, id_b,
        edge_paths, shared_concepts,
    )

    elapsed = time.monotonic() - t0
    log.info(
        "path_handler_complete",
        elapsed_s=round(elapsed, 1),
        edge_paths=len(edge_paths),
        shared_concepts=len(shared_concepts),
    )
    return result


# ---------------------------------------------------------------------------
# Command parser
# ---------------------------------------------------------------------------

def _parse_command(text: str) -> tuple[str, str] | None:
    """Parse '/path <source_a> <source_b>'.

    Accepts:
      /path ID1 ID2
      /path "partial title" "partial title"
      /path ID1 "partial title"

    Returns (ref_a, ref_b) or None if parsing fails.
    """
    cleaned = text.strip()
    for prefix in ("/path ", "/path"):
        if cleaned.lower().startswith(prefix):
            cleaned = cleaned[len(prefix):].strip()
            break

    if not cleaned:
        return None

    # Try to extract two quoted strings
    quoted = re.findall(r'"([^"]+)"', cleaned)
    if len(quoted) >= 2:
        return (quoted[0].strip(), quoted[1].strip())

    # Try mixed: one quoted, one bare token
    if len(quoted) == 1:
        # Remove the quoted part and take the remaining token
        remainder = re.sub(r'"[^"]*"', "", cleaned).strip()
        if remainder:
            tokens = remainder.split()
            if tokens:
                # Determine order: was the quote first or second?
                quote_pos = cleaned.index('"')
                bare_before = cleaned[:quote_pos].strip()
                if bare_before:
                    return (bare_before.split()[0], quoted[0])
                else:
                    return (quoted[0], tokens[0])

    # Try two bare tokens (space-separated, no quotes)
    tokens = cleaned.split()
    if len(tokens) >= 2:
        return (tokens[0], tokens[1])

    return None


# ---------------------------------------------------------------------------
# Source resolution
# ---------------------------------------------------------------------------

def _resolve_source(ref: str) -> dict | None:
    """Resolve a source reference by ID or partial title match."""
    from reading_app.db import get_conn

    with get_conn() as conn:
        # Try exact ID match
        if _ID_RE.fullmatch(ref):
            row = conn.execute(
                "SELECT id, title FROM sources WHERE id = %s", (ref,)
            ).fetchone()
            if row:
                return dict(row)

        # Try partial ID match (prefix)
        if len(ref) >= 6 and ref.replace("-", "").isalnum():
            row = conn.execute(
                "SELECT id, title FROM sources WHERE id LIKE %s LIMIT 1",
                (f"{ref}%",),
            ).fetchone()
            if row:
                return dict(row)

        # Try URL match
        if ref.startswith("http"):
            row = conn.execute(
                "SELECT id, title FROM sources WHERE url = %s", (ref,)
            ).fetchone()
            if row:
                return dict(row)

        # Try partial title match (case-insensitive)
        row = conn.execute(
            "SELECT id, title FROM sources WHERE title ILIKE %s LIMIT 1",
            (f"%{ref}%",),
        ).fetchone()
        if row:
            return dict(row)

    return None


# ---------------------------------------------------------------------------
# Path finding
# ---------------------------------------------------------------------------

def _find_edge_paths(source_a: str, source_b: str, max_hops: int = 3) -> list[dict]:
    """Find paths between two sources via source_edges using recursive CTE.

    Returns list of dicts with 'path' (list of source IDs) and 'depth'.
    """
    from reading_app.db import get_conn
    from retrieval.graph import GraphRetriever

    with get_conn() as conn:
        retriever = GraphRetriever(lambda: conn)
        rows = retriever.explain_path(source_a, source_b, max_hops=max_hops)

    # Enrich paths with source titles and edge details
    if not rows:
        return []

    enriched = []
    for row in rows:
        path_ids = row.get("path", [])
        depth = row.get("depth", 0)
        enriched.append({
            "path_ids": list(path_ids),
            "depth": depth,
        })

    # Resolve titles and edge details for all paths
    _enrich_paths(enriched)

    return enriched


def _enrich_paths(paths: list[dict]) -> None:
    """Add source titles and edge metadata to path results in-place."""
    from reading_app.db import get_conn

    # Collect all source IDs across all paths
    all_ids = set()
    all_edge_pairs = set()
    for p in paths:
        ids = p["path_ids"]
        all_ids.update(ids)
        for i in range(len(ids) - 1):
            all_edge_pairs.add((ids[i], ids[i + 1]))

    if not all_ids:
        return

    with get_conn() as conn:
        # Resolve titles
        placeholders = ",".join(["%s"] * len(all_ids))
        title_rows = conn.execute(
            f"SELECT id, title FROM sources WHERE id IN ({placeholders})",
            tuple(all_ids),
        ).fetchall()
        titles = {r["id"]: r["title"] for r in title_rows}

        # Resolve edge details (check both directions)
        edges_lookup: dict[tuple[str, str], dict] = {}
        for a, b in all_edge_pairs:
            edge_row = conn.execute(
                """SELECT edge_type, explanation, confidence
                   FROM source_edges
                   WHERE (source_a = %s AND source_b = %s)
                      OR (source_a = %s AND source_b = %s)
                   LIMIT 1""",
                (a, b, b, a),
            ).fetchone()
            if edge_row:
                edges_lookup[(a, b)] = dict(edge_row)

    # Attach to each path
    for p in paths:
        ids = p["path_ids"]
        p["titles"] = [titles.get(sid, sid) for sid in ids]
        hops = []
        for i in range(len(ids) - 1):
            edge_info = edges_lookup.get((ids[i], ids[i + 1]), {})
            hops.append({
                "from_id": ids[i],
                "from_title": titles.get(ids[i], ids[i]),
                "to_id": ids[i + 1],
                "to_title": titles.get(ids[i + 1], ids[i + 1]),
                "edge_type": edge_info.get("edge_type", "unknown"),
                "explanation": edge_info.get("explanation", ""),
                "confidence": edge_info.get("confidence"),
            })
        p["hops"] = hops


def _find_shared_concepts(source_a: str, source_b: str) -> list[dict]:
    """Find concepts shared between two sources."""
    from reading_app.db import get_conn

    with get_conn() as conn:
        rows = conn.execute("""
            SELECT c.id, c.canonical_name, c.concept_type,
                   sc1.relationship AS rel_a, sc2.relationship AS rel_b
            FROM source_concepts sc1
            JOIN source_concepts sc2 ON sc1.concept_id = sc2.concept_id
            JOIN concepts c ON sc1.concept_id = c.id
            WHERE sc1.source_id = %s AND sc2.source_id = %s
            ORDER BY c.canonical_name
        """, (source_a, source_b)).fetchall()

    return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def _format_path_narrative(
    title_a: str, id_a: str,
    title_b: str, id_b: str,
    edge_paths: list[dict],
    shared_concepts: list[dict],
) -> str:
    """Format path data as a readable narrative."""
    lines = [
        f"**Connection Path**\n",
        f"**From:** {title_a} (`{id_a[:12]}...`)",
        f"**To:** {title_b} (`{id_b[:12]}...`)\n",
    ]

    # Edge paths (source_edges traversal)
    if edge_paths:
        lines.append(f"**Direct Graph Paths** ({len(edge_paths)} found):\n")
        for i, path in enumerate(edge_paths, 1):
            depth = path.get("depth", 0)
            hops = path.get("hops", [])
            lines.append(f"**Path {i}** ({depth} hop{'s' if depth != 1 else ''}):")

            for j, hop in enumerate(hops, 1):
                edge_type = hop.get("edge_type", "related")
                explanation = hop.get("explanation", "")
                confidence = hop.get("confidence")

                from_label = _truncate(hop["from_title"], 50)
                to_label = _truncate(hop["to_title"], 50)

                conf_str = f" ({confidence:.0%})" if confidence is not None else ""
                lines.append(f"  {j}. {from_label} --[{edge_type}]{conf_str}--> {to_label}")

                if explanation:
                    lines.append(f"     {_truncate(explanation, 120)}")

            lines.append("")

    # Shared concepts
    if shared_concepts:
        lines.append(f"**Shared Concepts** ({len(shared_concepts)}):\n")
        for c in shared_concepts[:10]:
            name = c.get("canonical_name", "?")
            ctype = c.get("concept_type", "")
            rel_a = c.get("rel_a", "")
            rel_b = c.get("rel_b", "")
            type_str = f" [{ctype}]" if ctype else ""
            lines.append(f"- **{name}**{type_str}")
            if rel_a or rel_b:
                lines.append(f"  Source A: {rel_a or 'mentions'} | Source B: {rel_b or 'mentions'}")
        if len(shared_concepts) > 10:
            lines.append(f"  ... and {len(shared_concepts) - 10} more")
        lines.append("")

    # Summary
    connection_types = []
    if edge_paths:
        min_hops = min(p.get("depth", 99) for p in edge_paths)
        connection_types.append(f"{len(edge_paths)} graph path(s), shortest: {min_hops} hop(s)")
    if shared_concepts:
        connection_types.append(f"{len(shared_concepts)} shared concept(s)")
    lines.append(f"**Summary:** {' | '.join(connection_types)}")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _truncate(s: str, n: int) -> str:
    return s[:n] + "..." if len(s) > n else s
