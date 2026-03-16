"""Activity API router -- job queue status, DB stats, data health."""

from __future__ import annotations

import json
import time as _time
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from agents.executor import ClaudeExecutor
from gateway.model_preferences import get_config_default_model_tier, list_model_tier_metadata
from gateway.providers import WEBAPP_CHAT_ID, build_chat_session_key, get_default_provider_id
from gateway.queue import DEFAULT_QUEUE_DB_PATH
from reading_app import db
from reading_app.runtime import get_process_files, read_live_pid

router = APIRouter(prefix="/api/activity", tags=["activity"])

_JOBS_DB_PATH = DEFAULT_QUEUE_DB_PATH

# TTL cache for the /health file-scan loop (truncated summaries + missing landscape)
_health_fs_cache: tuple[list, list] | None = None
_health_fs_cache_ts: float = 0.0
_HEALTH_FS_CACHE_TTL = 300  # 5 minutes


def _iso_from_unix_timestamp(value: float | int | None) -> str | None:
    """Convert a unix timestamp into an ISO-8601 string."""
    if value in (None, ""):
        return None
    try:
        return datetime.fromtimestamp(float(value), tz=timezone.utc).isoformat()
    except (TypeError, ValueError, OSError):
        return None


def _parse_json_field(value):
    """Decode JSON payloads when they are stored as strings."""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    return value


def _serialize_job_row(row) -> dict[str, object]:
    """Normalize queue job rows for frontend consumption."""
    payload = dict(row)

    for field in ("result", "event_payload"):
        if field in payload:
            payload[field] = _parse_json_field(payload.get(field))

    payload["created_at_iso"] = _iso_from_unix_timestamp(payload.get("created_at"))
    payload["updated_at_iso"] = _iso_from_unix_timestamp(payload.get("updated_at"))

    result = payload.get("result")
    if isinstance(result, dict):
        error = result.get("error") or result.get("last_error")
        if isinstance(error, str) and error.strip():
            payload["error"] = error

        progress = result.get("progress")
        if isinstance(progress, str) and progress.strip():
            payload["progress"] = progress

        stages = result.get("stages")
        if isinstance(stages, list):
            payload["stages"] = stages

    payload.setdefault("error", None)
    payload.setdefault("progress", None)
    payload.setdefault("stages", None)

    return payload


def _gateway_runtime_status() -> dict[str, object]:
    """Return the local gateway worker state from runtime marker files."""
    files = get_process_files("gateway")
    pid = read_live_pid(files.pid_file)
    ready = pid is not None and files.ready_file.exists()
    ready_at = None

    if files.ready_file.exists():
        try:
            ready_at = _iso_from_unix_timestamp(float(files.ready_file.read_text(encoding="utf-8").strip()))
        except (TypeError, ValueError, OSError):
            ready_at = None

    state = "ready" if ready else "starting" if pid is not None else "offline"

    return {
        "state": state,
        "running": pid is not None,
        "ready": ready,
        "pid": pid,
        "ready_at": ready_at,
        "log_path": str(files.log_file),
    }


@router.get("/jobs")
def list_jobs(
    status: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
):
    """List jobs from the SQLite queue."""
    from gateway.queue import Queue

    q = Queue(db_path=_JOBS_DB_PATH)
    conditions = []
    params: list = []

    if status:
        conditions.append("j.status = ?")
        params.append(status)

    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    params.append(limit)

    cur = q._conn.execute(
        f"""SELECT j.*, e.type AS event_type, e.payload AS event_payload, e.source AS event_source
            FROM jobs j
            JOIN events e ON j.event_id = e.id
            {where}
            ORDER BY j.created_at DESC
            LIMIT ?""",
        params,
    )
    rows = [_serialize_job_row(row) for row in cur.fetchall()]
    return rows


@router.get("/jobs/{job_id}")
def get_job(job_id: int):
    """Get a single job with its event context."""
    from gateway.queue import Queue

    q = Queue(db_path=_JOBS_DB_PATH)
    cur = q._conn.execute(
        """SELECT j.*, e.type AS event_type, e.payload AS event_payload, e.source AS event_source
            FROM jobs j
            JOIN events e ON j.event_id = e.id
            WHERE j.id = ?""",
        [job_id],
    )
    row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Job not found")
    return _serialize_job_row(row)


@router.get("/runtime")
def runtime():
    """Runtime status for the web app, including gateway readiness and queue health."""
    from gateway.queue import Queue

    gateway_status = _gateway_runtime_status()
    q = Queue(db_path=_JOBS_DB_PATH)
    current_provider = q.get_chat_provider(build_chat_session_key(WEBAPP_CHAT_ID)) or get_default_provider_id()
    current_model = q.get_global_model() or get_config_default_model_tier()
    providers = ClaudeExecutor.get_backend_statuses()

    count_rows = q._conn.execute(
        """SELECT j.status, COUNT(*) AS cnt
           FROM jobs j
           JOIN events e ON j.event_id = e.id
           WHERE e.source = 'webapp'
           GROUP BY j.status"""
    ).fetchall()
    counts = {row["status"]: row["cnt"] for row in count_rows}

    last_completed = q._conn.execute(
        """SELECT j.id, j.skill, j.status, j.updated_at, j.result
           FROM jobs j
           JOIN events e ON j.event_id = e.id
           WHERE e.source = 'webapp'
             AND j.status = 'complete'
           ORDER BY j.updated_at DESC
           LIMIT 1"""
    ).fetchone()

    last_failed = q._conn.execute(
        """SELECT j.id, j.skill, j.status, j.updated_at, j.result
           FROM jobs j
           JOIN events e ON j.event_id = e.id
           WHERE e.source = 'webapp'
             AND j.status IN ('failed', 'dead_letter', 'interrupted')
           ORDER BY j.updated_at DESC
           LIMIT 1"""
    ).fetchone()

    def _serialize_job(row):
        if not row:
            return None
        serialized = _serialize_job_row(row)
        return {
            "id": serialized["id"],
            "skill": serialized["skill"],
            "status": serialized["status"],
            "updated_at": serialized["updated_at_iso"],
            "result": serialized["result"],
            "error": serialized.get("error"),
            "progress": serialized.get("progress"),
        }

    queue_status = {
        "pending": counts.get("pending", 0),
        "running": counts.get("running", 0),
        "failed": counts.get("failed", 0) + counts.get("dead_letter", 0) + counts.get("interrupted", 0),
        "complete": counts.get("complete", 0),
        "attention_required": counts.get("pending", 0) + counts.get("running", 0),
        "last_completed": _serialize_job(last_completed),
        "last_failed": _serialize_job(last_failed),
    }

    return {
        "gateway": gateway_status,
        "queue": queue_status,
        "chat": {
            "can_queue": bool(gateway_status["ready"]),
            "direct_commands": ["/ask", "/landscape", "/provider", "/model"],
            "providers": providers,
            "current_provider": current_provider,
            "model_options": list_model_tier_metadata(),
            "current_model": current_model,
        },
    }


@router.get("/stats")
def stats():
    """Count of rows in each major table."""
    tables = [
        "sources", "claims", "concepts", "source_edges",
        "source_concepts", "themes", "capabilities", "limitations",
        "bottlenecks", "breakthroughs", "anticipations", "beliefs",
        "ideas", "challenge_log", "cross_theme_implications",
    ]
    counts: dict[str, int] = {}
    with db.get_conn() as conn:
        for table in tables:
            try:
                row = conn.execute(f"SELECT COUNT(*) AS cnt FROM {table}").fetchone()
                counts[table] = row["cnt"] if row else 0
            except Exception:
                counts[table] = -1
    return counts


@router.get("/health")
def health():
    """Data quality health check — sources with missing claims, summaries, themes, landscape."""
    from reading_app.config import Config

    config = Config()
    library_path = Path(config.library_path)

    with db.get_conn() as conn:
        total_sources = conn.execute("SELECT count(*) AS cnt FROM sources").fetchone()["cnt"]

        # Sources with zero claims
        zero_claims = conn.execute("""
            SELECT s.id, s.title
            FROM sources s
            WHERE NOT EXISTS (SELECT 1 FROM claims c WHERE c.source_id = s.id)
            ORDER BY s.ingested_at DESC
        """).fetchall()

        # Sources with no themes
        no_themes = conn.execute("""
            SELECT s.id, s.title
            FROM sources s
            WHERE NOT EXISTS (SELECT 1 FROM source_themes st WHERE st.source_id = s.id)
            ORDER BY s.ingested_at DESC
        """).fetchall()

        # Sources marked incomplete
        incomplete = conn.execute("""
            SELECT s.id, s.title
            FROM sources s
            WHERE s.processing_status = 'incomplete'
            ORDER BY s.ingested_at DESC
        """).fetchall()

    # Truncated summaries + missing landscape (file scan, TTL-cached)
    global _health_fs_cache, _health_fs_cache_ts
    now_mono = _time.monotonic()
    if _health_fs_cache is not None and (now_mono - _health_fs_cache_ts) < _HEALTH_FS_CACHE_TTL:
        truncated_summaries, missing_landscape = _health_fs_cache
    else:
        truncated_summaries = []
        missing_landscape = []
        for source_dir in sorted(library_path.iterdir()):
            if not source_dir.is_dir():
                continue
            sid = source_dir.name
            # Check summary
            summary_path = source_dir / "deep_summary.md"
            if summary_path.exists():
                try:
                    content = summary_path.read_text(encoding="utf-8")
                    if "hit your limit" in content.lower() or len(content.strip()) < 200:
                        truncated_summaries.append(sid)
                except Exception:
                    truncated_summaries.append(sid)
            else:
                truncated_summaries.append(sid)

            # Check landscape
            landscape_path = source_dir / "landscape.json"
            if landscape_path.exists():
                try:
                    import json as _json
                    data = _json.loads(landscape_path.read_text(encoding="utf-8"))
                    if all(
                        len(data.get(k, [])) == 0
                        for k in ("capabilities", "limitations", "bottlenecks", "breakthroughs")
                    ):
                        missing_landscape.append(sid)
                except Exception:
                    missing_landscape.append(sid)
            else:
                missing_landscape.append(sid)
        _health_fs_cache = (truncated_summaries, missing_landscape)
        _health_fs_cache_ts = now_mono

    # Post-processing status
    pp_stats = {"pending": 0, "running": 0, "failed": 0, "completed": 0}
    pp_last_completed = None
    pp_step_failures = {}
    try:
        with db.get_conn() as pp_conn:
            pp_rows = pp_conn.execute(
                "SELECT status, COUNT(*) AS cnt FROM post_processing_status GROUP BY status"
            ).fetchall()
            for r in pp_rows:
                pp_stats[r["status"]] = r["cnt"]

            pp_last = pp_conn.execute(
                "SELECT MAX(completed_at) AS last_completed FROM post_processing_status WHERE status = 'completed'"
            ).fetchone()
            if pp_last and pp_last["last_completed"]:
                pp_last_completed = pp_last["last_completed"].isoformat()

            pp_failures = pp_conn.execute(
                "SELECT step, COUNT(*) AS cnt FROM post_processing_status WHERE status = 'failed' GROUP BY step"
            ).fetchall()
            pp_step_failures = {r["step"]: r["cnt"] for r in pp_failures}
    except Exception:
        pass  # Table may not exist yet (pre-migration)

    return {
        "total_sources": total_sources,
        "post_processing": {
            "pending": pp_stats["pending"],
            "running": pp_stats["running"],
            "failed": pp_stats["failed"],
            "completed": pp_stats["completed"],
            "last_completed_at": pp_last_completed,
            "step_failures": pp_step_failures,
        },
        "metrics": [
            {
                "label": "Zero claims",
                "count": len(zero_claims),
                "total": total_sources,
                "sample_ids": [r["id"] for r in zero_claims[:5]],
            },
            {
                "label": "Truncated summaries",
                "count": len(truncated_summaries),
                "total": total_sources,
                "sample_ids": truncated_summaries[:5],
            },
            {
                "label": "Missing themes",
                "count": len(no_themes),
                "total": total_sources,
                "sample_ids": [r["id"] for r in no_themes[:5]],
            },
            {
                "label": "Empty landscape",
                "count": len(missing_landscape),
                "total": total_sources,
                "sample_ids": missing_landscape[:5],
            },
            {
                "label": "Incomplete processing",
                "count": len(incomplete),
                "total": total_sources,
                "sample_ids": [r["id"] for r in incomplete[:5]],
            },
        ],
    }
