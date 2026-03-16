"""Reports API router -- synthesis and merge reports."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

import yaml
from fastapi import APIRouter, HTTPException, Query

from reading_app.config import Config

router = APIRouter(prefix="/api/reports", tags=["reports"])


def _library_path() -> Path:
    return Config().library_path


def _parse_synthesis(path: Path) -> dict:
    """Parse a synthesis markdown file into a report entry."""
    text = path.read_text(encoding="utf-8")
    # Extract title from first # heading
    title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    topic = title_match.group(1).strip() if title_match else path.stem.replace("_", " ").title()
    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return {
        "type": "synthesis",
        "slug": path.stem,
        "topic": topic,
        "generated_at": mtime.isoformat(),
        "sources": [],
        "path": f"syntheses/{path.name}",
    }


def _parse_merge(path: Path) -> dict:
    """Parse a merge markdown file (YAML front-matter) into a report entry."""
    text = path.read_text(encoding="utf-8")
    meta: dict = {}
    body = text

    # Parse YAML front-matter (--- delimited)
    fm_match = re.match(r"^---\n(.+?)\n---", text, re.DOTALL)
    if fm_match:
        try:
            meta = yaml.safe_load(fm_match.group(1)) or {}
        except yaml.YAMLError:
            pass
        body = text[fm_match.end():]

    # Infer topic from front-matter or first heading
    topic = meta.get("inferred_topic", "")
    if not topic:
        title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        topic = title_match.group(1).strip() if title_match else path.stem

    generated_at = meta.get("generated_at")
    if generated_at and isinstance(generated_at, str):
        pass  # already ISO string
    elif generated_at and isinstance(generated_at, datetime):
        generated_at = generated_at.isoformat()
    else:
        generated_at = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat()

    source_ids = meta.get("source_ids", [])
    titles = meta.get("titles", [])
    sources = [
        {"id": sid, "title": titles[i] if i < len(titles) else sid}
        for i, sid in enumerate(source_ids)
    ]

    return {
        "type": "merge",
        "slug": path.stem,
        "topic": topic,
        "generated_at": generated_at,
        "sources": sources,
        "path": f"merges/{path.name}",
    }


@router.get("")
def list_reports(limit: int = Query(50, ge=1, le=200)):
    """List all synthesis and merge reports, newest first."""
    lib = _library_path()
    reports: list[dict] = []

    syntheses_dir = lib / "syntheses"
    if syntheses_dir.is_dir():
        for p in syntheses_dir.glob("*.md"):
            reports.append(_parse_synthesis(p))

    merges_dir = lib / "merges"
    if merges_dir.is_dir():
        for p in merges_dir.glob("*.md"):
            reports.append(_parse_merge(p))

    reports.sort(key=lambda r: r["generated_at"], reverse=True)
    return reports[:limit]


@router.get("/{report_type}/{slug}")
def get_report(report_type: str, slug: str):
    """Get a single report's markdown and metadata."""
    if report_type not in ("synthesis", "merge"):
        raise HTTPException(status_code=400, detail="report_type must be 'synthesis' or 'merge'")

    lib = _library_path()
    subdir = "syntheses" if report_type == "synthesis" else "merges"
    path = lib / subdir / f"{slug}.md"

    if not path.is_file():
        raise HTTPException(status_code=404, detail=f"Report '{report_type}/{slug}' not found")

    text = path.read_text(encoding="utf-8")
    meta: dict = {}
    body = text

    # Strip YAML front-matter for merges
    if report_type == "merge":
        fm_match = re.match(r"^---\n(.+?)\n---", text, re.DOTALL)
        if fm_match:
            try:
                meta = yaml.safe_load(fm_match.group(1)) or {}
            except yaml.YAMLError:
                pass
            body = text[fm_match.end():].lstrip("\n")

    return {"markdown": body, "meta": meta}


# ---------------------------------------------------------------------------
# Tournament trace (Phase 5: Visible Tournament Reasoning)
# ---------------------------------------------------------------------------

@router.get("/ideas/{idea_id}/tournament")
def get_idea_tournament_trace(idea_id: str):
    """Return the full tournament trace for an idea, if available."""
    from reading_app import db

    with db.get_conn() as conn:
        row = conn.execute(
            """SELECT id, idea_text, idea_type, novelty_score, feasibility_score,
                      impact_score, overall_score, generation_context, created_at
               FROM ideas WHERE id = %s""",
            (idea_id,),
        ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Idea not found")

    generation_context = row.get("generation_context") or {}
    if isinstance(generation_context, str):
        import json as _json
        try:
            generation_context = _json.loads(generation_context)
        except (ValueError, TypeError):
            generation_context = {}

    tournament_metadata = generation_context.get("tournament_metadata", {})

    # Build tournament trace timeline
    stages = []
    if tournament_metadata.get("generation_strategy"):
        stages.append({
            "stage": "generation",
            "label": "Generated",
            "detail": f"Strategy: {tournament_metadata['generation_strategy']}",
            "passed": True,
        })

    if tournament_metadata.get("novelty_score") is not None:
        stages.append({
            "stage": "novelty",
            "label": "Novelty Gate",
            "detail": f"Score: {tournament_metadata['novelty_score']}",
            "passed": tournament_metadata.get("novelty_check_passed", True),
        })

    if tournament_metadata.get("critique_verdict"):
        stages.append({
            "stage": "critique",
            "label": "Critique",
            "detail": tournament_metadata.get("critique_summary", ""),
            "passed": tournament_metadata["critique_verdict"] != "cut",
        })

    if tournament_metadata.get("debate_tier"):
        stages.append({
            "stage": "debate",
            "label": f"Debate ({tournament_metadata['debate_tier']})",
            "detail": tournament_metadata.get("debate_outcome", ""),
            "passed": True,
        })

    if tournament_metadata.get("evolution_delta"):
        stages.append({
            "stage": "evolution",
            "label": "Evolution",
            "detail": tournament_metadata["evolution_delta"],
            "passed": True,
        })

    if tournament_metadata.get("final_rank") is not None:
        stages.append({
            "stage": "ranking",
            "label": "Final Ranking",
            "detail": f"Rank #{tournament_metadata['final_rank']} "
                      f"(score: {tournament_metadata.get('final_score', 0):.2f})",
            "passed": True,
        })

    return {
        "idea_id": idea_id,
        "idea_text": row.get("idea_text", ""),
        "idea_type": row.get("idea_type"),
        "scores": {
            "novelty": row.get("novelty_score"),
            "feasibility": row.get("feasibility_score"),
            "impact": row.get("impact_score"),
            "overall": row.get("overall_score"),
        },
        "tournament_metadata": tournament_metadata,
        "stages": stages,
        "is_tournament": generation_context.get("tournament", False),
    }
