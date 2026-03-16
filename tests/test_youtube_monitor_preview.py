from __future__ import annotations

import json
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

from gateway.digest_context import maybe_trigger_auto_reflect
from gateway.models import Event, Job
from gateway.preview_flow import create_summary_preview
from gateway.save_confirmed_handler import handle_save_confirmed_job
from gateway.save_handler import handle_save_job
from gateway.youtube_monitor_handler import handle_youtube_monitor_job

SOURCE_ID = "01KABCDE1234567890FGHIJKLM"
NEWER_SOURCE_ID = "01KZZZZZ1234567890FGHIJKLM"


class DummyConn:
    def __init__(self, fetchone_result=None):
        self.executed: list[tuple[str, tuple | None]] = []
        self.fetchone_result = fetchone_result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.executed.append((sql, params))
        return self

    def commit(self):
        return None

    def fetchone(self):
        return self.fetchone_result


def _make_config(tmp_path: Path):
    library_path = tmp_path / "library"
    library_path.mkdir(parents=True, exist_ok=True)
    return SimpleNamespace(library_path=library_path)


def _patch_db(monkeypatch, conn: DummyConn):
    import reading_app.db

    monkeypatch.setattr(reading_app.db, "ensure_pool", lambda: None)
    monkeypatch.setattr(reading_app.db, "get_conn", lambda: conn)


def test_youtube_monitor_stages_preview_and_notifies(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    config = _make_config(tmp_path)
    conn = DummyConn()
    _patch_db(monkeypatch, conn)

    source_dir = config.library_path / SOURCE_ID
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "clean.md").write_text("A" * 200, encoding="utf-8")

    import ingest.deep_summarizer
    import ingest.save_pipeline
    import ingest.theme_classifier
    import reading_app.db
    import scripts.bulk_ingest

    insert_calls = []

    monkeypatch.setattr(
        scripts.bulk_ingest,
        "fetch_source",
        lambda entry, library_path: {
            "id": SOURCE_ID,
            "source_type": "video",
            "url": entry.url,
            "title": "Watched Video",
            "published_at": "2026-03-09T10:00:00+00:00",
            "clean_text": "A" * 200,
            "library_path": str(source_dir),
            "metadata": {"channel": "Tracked Channel"},
            "authors": ["Host"],
        },
    )
    monkeypatch.setattr(
        reading_app.db,
        "insert_source",
        lambda **kwargs: insert_calls.append(kwargs),
    )
    monkeypatch.setattr(
        ingest.theme_classifier,
        "classify_themes",
        lambda *args, **kwargs: [{"theme_id": "autonomous_agents", "relevance": 0.91}],
    )

    def fake_generate_deep_summary(**kwargs):
        summary_path = kwargs["library_path"] / kwargs["source_id"] / "deep_summary.md"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text("# Deep Summary\n\nUseful details.", encoding="utf-8")
        return "# Deep Summary\n\nUseful details."

    monkeypatch.setattr(
        ingest.deep_summarizer,
        "generate_deep_summary",
        fake_generate_deep_summary,
    )
    monkeypatch.setattr(
        ingest.save_pipeline,
        "run_save_pipeline",
        lambda *args, **kwargs: pytest.fail("run_save_pipeline should not be called"),
    )

    sent = {}

    def fake_send_monitor_preview_notifications(**kwargs):
        sent.update(kwargs)
        return {"email": True, "telegram": True, "discord": False}

    monkeypatch.setattr(
        "gateway.youtube_monitor_handler.send_monitor_preview_notifications",
        fake_send_monitor_preview_notifications,
    )

    response = handle_youtube_monitor_job(
        Event(
            type="youtube_monitor",
            payload={
                "url": "https://www.youtube.com/watch?v=test123",
                "title": "Watched Video",
                "channel": "Tracked Channel",
            },
            source="youtube_monitor",
        ),
        Job(event_id=1, skill="youtube_monitor", id=1),
        config,
        executor=SimpleNamespace(),
    )

    staging_path = tmp_path / "var" / "summarise_staging" / f"{SOURCE_ID}.json"
    staging = json.loads(staging_path.read_text(encoding="utf-8"))

    assert insert_calls[0]["processing_status"] == "monitor_preview"
    assert staging["origin"] == "youtube_monitor"
    assert "pipeline_complete" not in staging
    assert (source_dir / "deep_summary.md").exists()
    assert sent["source_id"] == SOURCE_ID
    assert sent["theme_names"] == ["autonomous_agents"]
    assert "/save_confirmed" in response


def test_save_confirmed_reuses_monitor_preview_and_triggers_followups(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    config = _make_config(tmp_path)
    conn = DummyConn()
    _patch_db(monkeypatch, conn)

    source_dir = config.library_path / SOURCE_ID
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "clean.md").write_text("B" * 200, encoding="utf-8")
    (source_dir / "deep_summary.md").write_text("# Deep Summary\n\nSaved earlier.", encoding="utf-8")

    staging_dir = tmp_path / "var" / "summarise_staging"
    staging_dir.mkdir(parents=True, exist_ok=True)
    (staging_dir / f"{SOURCE_ID}.json").write_text(
        json.dumps(
            {
                "source_id": SOURCE_ID,
                "url": "https://www.youtube.com/watch?v=test123",
                "title": "Watched Video",
                "source_type": "video",
                "authors": ["Host"],
                "published_at": "2026-03-09T10:00:00+00:00",
                "metadata": {"channel": "Tracked Channel"},
                "themes": [{"theme_id": "autonomous_agents", "relevance": 0.91}],
                "theme_proposal": {"name": "agent_swarms"},
                "library_path": str(source_dir),
                "created_at": time.time(),
                "origin": "youtube_monitor",
            }
        ),
        encoding="utf-8",
    )

    import gateway.digest_context
    import ingest.post_processor
    import ingest.save_pipeline

    pipeline_calls = {}
    postprocess_calls = []
    auto_reflect_calls = []

    def fake_run_save_pipeline(**kwargs):
        pipeline_calls.update(kwargs)
        return {
            "themes": [{"theme_id": "autonomous_agents", "relevance": 0.91}],
            "claims": [{"claim_text": "A claim"}],
            "errors": [],
            "landscape_signals": {"breakthroughs": [{"theme_id": "autonomous_agents"}]},
            "implications": [{"target_theme_id": "autonomous_agents"}],
        }

    monkeypatch.setattr(ingest.save_pipeline, "run_save_pipeline", fake_run_save_pipeline)
    monkeypatch.setattr(
        ingest.post_processor,
        "enqueue_post_processing",
        lambda source_id, theme_ids, get_conn: postprocess_calls.append((source_id, theme_ids)),
    )
    monkeypatch.setattr(
        gateway.digest_context,
        "maybe_trigger_auto_reflect",
        lambda result: auto_reflect_calls.append(result) or True,
    )

    response = handle_save_confirmed_job(
        Event(
            type="human_message",
            payload={"text": f"/save_confirmed {SOURCE_ID}"},
            source="telegram",
        ),
        Job(event_id=1, skill="save_confirmed", id=1),
        config,
        executor=SimpleNamespace(),
    )

    assert pipeline_calls["skip_summary"] is True
    assert pipeline_calls["pre_classified_themes"] == [
        {"theme_id": "autonomous_agents", "relevance": 0.91},
        {"_proposal": {"name": "agent_swarms"}},
    ]
    assert postprocess_calls == [(SOURCE_ID, ["autonomous_agents"])]
    assert auto_reflect_calls
    assert not (staging_dir / f"{SOURCE_ID}.json").exists()
    assert "summary + themes skipped" in response


def test_save_autopromotes_monitor_preview_without_changing_save_behavior(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    config = _make_config(tmp_path)

    staging_dir = tmp_path / "var" / "summarise_staging"
    staging_dir.mkdir(parents=True, exist_ok=True)
    (staging_dir / f"{SOURCE_ID}.json").write_text(
        json.dumps(
            {
                "source_id": SOURCE_ID,
                "url": "https://www.youtube.com/watch?v=test123",
                "created_at": time.time(),
                "origin": "youtube_monitor",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "gateway.save_confirmed_handler.handle_save_confirmed_job",
        lambda event, job, config, executor, on_progress=None: "reused monitor preview",
    )

    event = Event(
        type="human_message",
        payload={"text": "/save https://www.youtube.com/watch?v=test123"},
        source="telegram",
    )
    response = handle_save_job(
        event,
        Job(event_id=1, skill="save", id=1),
        config,
        executor=SimpleNamespace(),
    )

    assert response == "reused monitor preview"
    assert event.payload["text"] == f"/save_confirmed {SOURCE_ID}"


def test_save_autopromotes_regular_summary_preview(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    config = _make_config(tmp_path)

    staging_dir = tmp_path / "var" / "summarise_staging"
    staging_dir.mkdir(parents=True, exist_ok=True)
    (staging_dir / f"{SOURCE_ID}.json").write_text(
        json.dumps(
            {
                "source_id": SOURCE_ID,
                "url": "https://example.com/article",
                "created_at": time.time(),
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "gateway.save_confirmed_handler.handle_save_confirmed_job",
        lambda event, job, config, executor, on_progress=None: "reused staged preview",
    )

    event = Event(
        type="human_message",
        payload={"text": "/save https://example.com/article"},
        source="telegram",
    )
    response = handle_save_job(
        event,
        Job(event_id=1, skill="save", id=1),
        config,
        executor=SimpleNamespace(),
    )

    assert response == "reused staged preview"
    assert event.payload["text"] == f"/save_confirmed {SOURCE_ID}"


def test_save_uses_newest_matching_preview_for_same_url(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    config = _make_config(tmp_path)

    staging_dir = tmp_path / "var" / "summarise_staging"
    staging_dir.mkdir(parents=True, exist_ok=True)
    shared_url = "https://www.youtube.com/watch?v=test123"
    (staging_dir / f"{SOURCE_ID}.json").write_text(
        json.dumps(
            {
                "source_id": SOURCE_ID,
                "url": shared_url,
                "created_at": time.time() - 60,
                "origin": "youtube_monitor",
            }
        ),
        encoding="utf-8",
    )
    (staging_dir / f"{NEWER_SOURCE_ID}.json").write_text(
        json.dumps(
            {
                "source_id": NEWER_SOURCE_ID,
                "url": shared_url,
                "created_at": time.time(),
                "origin": "youtube_monitor",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "gateway.save_confirmed_handler.handle_save_confirmed_job",
        lambda event, job, config, executor, on_progress=None: "used newest preview",
    )

    event = Event(
        type="human_message",
        payload={"text": f"/save {shared_url}"},
        source="telegram",
    )
    response = handle_save_job(
        event,
        Job(event_id=1, skill="save", id=1),
        config,
        executor=SimpleNamespace(),
    )

    assert response == "used newest preview"
    assert event.payload["text"] == f"/save_confirmed {NEWER_SOURCE_ID}"


def test_youtube_monitor_reuses_existing_preview_without_reprocessing(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    config = _make_config(tmp_path)

    source_dir = config.library_path / SOURCE_ID
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "clean.md").write_text("A" * 200, encoding="utf-8")
    (source_dir / "deep_summary.md").write_text("# Deep Summary\n\nUseful details.", encoding="utf-8")

    staging_dir = tmp_path / "var" / "summarise_staging"
    staging_dir.mkdir(parents=True, exist_ok=True)
    (staging_dir / f"{SOURCE_ID}.json").write_text(
        json.dumps(
            {
                "source_id": SOURCE_ID,
                "url": "https://www.youtube.com/watch?v=test123",
                "title": "Watched Video",
                "source_type": "video",
                "metadata": {"channel": "Tracked Channel"},
                "themes": [{"theme_id": "autonomous_agents", "relevance": 0.91}],
                "library_path": str(source_dir),
                "created_at": time.time(),
                "origin": "youtube_monitor",
                "notifications": {
                    "email": True,
                    "telegram": True,
                    "discord": False,
                    "last_attempt_at": time.time(),
                },
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "gateway.youtube_monitor_handler.create_summary_preview",
        lambda *args, **kwargs: pytest.fail("existing monitor preview should be reused"),
    )
    sent = {}

    def fake_send_monitor_preview_notifications(**kwargs):
        sent.update(kwargs)
        return {"email": False, "telegram": False, "discord": False}

    monkeypatch.setattr(
        "gateway.youtube_monitor_handler.send_monitor_preview_notifications",
        fake_send_monitor_preview_notifications,
    )

    response = handle_youtube_monitor_job(
        Event(
            type="youtube_monitor",
            payload={
                "url": "https://www.youtube.com/watch?v=test123",
                "title": "Watched Video",
                "channel": "Tracked Channel",
            },
            source="youtube_monitor",
        ),
        Job(event_id=1, skill="youtube_monitor", id=1),
        config,
        executor=SimpleNamespace(),
    )

    assert f"/save_confirmed {SOURCE_ID}" in response
    assert sent["channels"] == ("discord",)
    assert "Email: sent" in response
    assert "Telegram: sent" in response


def test_youtube_monitor_retries_only_unsent_notification_channels(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    config = _make_config(tmp_path)

    source_dir = config.library_path / SOURCE_ID
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "clean.md").write_text("A" * 200, encoding="utf-8")
    (source_dir / "deep_summary.md").write_text("# Deep Summary\n\nUseful details.", encoding="utf-8")

    staging_dir = tmp_path / "var" / "summarise_staging"
    staging_dir.mkdir(parents=True, exist_ok=True)
    staging_path = staging_dir / f"{SOURCE_ID}.json"
    staging_path.write_text(
        json.dumps(
            {
                "source_id": SOURCE_ID,
                "url": "https://www.youtube.com/watch?v=test123",
                "title": "Watched Video",
                "source_type": "video",
                "metadata": {"channel": "Tracked Channel"},
                "themes": [{"theme_id": "autonomous_agents", "relevance": 0.91}],
                "library_path": str(source_dir),
                "created_at": time.time(),
                "origin": "youtube_monitor",
                "notifications": {
                    "email": True,
                    "telegram": False,
                    "discord": False,
                    "last_attempt_at": time.time() - 60,
                },
            }
        ),
        encoding="utf-8",
    )

    sent = {}
    monkeypatch.setattr(
        "gateway.youtube_monitor_handler.create_summary_preview",
        lambda *args, **kwargs: pytest.fail("existing monitor preview should be reused"),
    )

    def fake_send_monitor_preview_notifications(**kwargs):
        sent.update(kwargs)
        return {"email": False, "telegram": True, "discord": False}

    monkeypatch.setattr(
        "gateway.youtube_monitor_handler.send_monitor_preview_notifications",
        fake_send_monitor_preview_notifications,
    )

    response = handle_youtube_monitor_job(
        Event(
            type="youtube_monitor",
            payload={
                "url": "https://www.youtube.com/watch?v=test123",
                "title": "Watched Video",
                "channel": "Tracked Channel",
            },
            source="youtube_monitor",
        ),
        Job(event_id=1, skill="youtube_monitor", id=1),
        config,
        executor=SimpleNamespace(),
    )

    updated_staging = json.loads(staging_path.read_text(encoding="utf-8"))
    assert sent["channels"] == ("telegram", "discord")
    assert updated_staging["notifications"]["email"] is True
    assert updated_staging["notifications"]["telegram"] is True
    assert updated_staging["notifications"]["discord"] is False
    assert "Email: sent" in response
    assert "Telegram: sent" in response
    assert "Discord: skipped" in response


def test_youtube_monitor_discards_invalid_preview_before_rebuilding(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    config = _make_config(tmp_path)

    source_dir = config.library_path / SOURCE_ID
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "clean.md").write_text("A" * 200, encoding="utf-8")

    staging_dir = tmp_path / "var" / "summarise_staging"
    staging_dir.mkdir(parents=True, exist_ok=True)
    (staging_dir / f"{SOURCE_ID}.json").write_text(
        json.dumps(
            {
                "source_id": SOURCE_ID,
                "url": "https://www.youtube.com/watch?v=test123",
                "title": "Broken Preview",
                "source_type": "video",
                "metadata": {"channel": "Tracked Channel"},
                "themes": [{"theme_id": "autonomous_agents", "relevance": 0.91}],
                "library_path": str(source_dir),
                "created_at": time.time(),
                "origin": "youtube_monitor",
            }
        ),
        encoding="utf-8",
    )

    discarded = []
    monkeypatch.setattr(
        "gateway.youtube_monitor_handler.discard_staging_preview",
        lambda staging_path, staging, config: discarded.append(staging["source_id"]),
    )
    monkeypatch.setattr(
        "gateway.youtube_monitor_handler.create_summary_preview",
        lambda **kwargs: {
            "source_id": NEWER_SOURCE_ID,
            "title": "Recovered Preview",
            "summary_text": "# Deep Summary\n\nRecovered.",
            "metadata": {"channel": "Tracked Channel"},
            "themes": [{"theme_id": "autonomous_agents", "relevance": 0.91}],
            "staging_path": staging_dir / f"{NEWER_SOURCE_ID}.json",
        },
    )
    monkeypatch.setattr(
        "gateway.youtube_monitor_handler.send_monitor_preview_notifications",
        lambda **kwargs: {"email": True, "telegram": True, "discord": False},
    )
    monkeypatch.setattr(
        "gateway.youtube_monitor_handler.update_staging_metadata",
        lambda *args, **kwargs: None,
    )

    response = handle_youtube_monitor_job(
        Event(
            type="youtube_monitor",
            payload={
                "url": "https://www.youtube.com/watch?v=test123",
                "title": "Recovered Preview",
                "channel": "Tracked Channel",
            },
            source="youtube_monitor",
        ),
        Job(event_id=1, skill="youtube_monitor", id=1),
        config,
        executor=SimpleNamespace(),
    )

    assert discarded == [SOURCE_ID]
    assert f"/save_confirmed {NEWER_SOURCE_ID}" in response


def test_create_summary_preview_cleans_up_partial_preview_on_failure(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    config = _make_config(tmp_path)

    source_dir = config.library_path / SOURCE_ID
    source_dir.mkdir(parents=True, exist_ok=True)
    (source_dir / "clean.md").write_text("A" * 200, encoding="utf-8")

    import ingest.deep_summarizer
    import ingest.theme_classifier
    import reading_app.db
    import scripts.bulk_ingest

    cleanup_calls = []

    monkeypatch.setattr(
        scripts.bulk_ingest,
        "fetch_source",
        lambda entry, library_path: {
            "id": SOURCE_ID,
            "source_type": "video",
            "url": entry.url,
            "title": "Watched Video",
            "published_at": "2026-03-09T10:00:00+00:00",
            "clean_text": "A" * 200,
            "library_path": str(source_dir),
            "metadata": {"channel": "Tracked Channel"},
        },
    )
    monkeypatch.setattr(reading_app.db, "ensure_pool", lambda: None)
    monkeypatch.setattr(reading_app.db, "get_conn", lambda: DummyConn())
    monkeypatch.setattr(reading_app.db, "insert_source", lambda **kwargs: None)
    monkeypatch.setattr(
        ingest.theme_classifier,
        "classify_themes",
        lambda *args, **kwargs: [{"theme_id": "autonomous_agents", "relevance": 0.91}],
    )
    monkeypatch.setattr(
        ingest.deep_summarizer,
        "generate_deep_summary",
        lambda **kwargs: (_ for _ in ()).throw(RuntimeError("summary failed")),
    )
    monkeypatch.setattr(
        "gateway.preview_flow.remove_preview_source",
        lambda source_id, config: cleanup_calls.append(source_id),
    )

    with pytest.raises(RuntimeError, match="summary failed"):
        create_summary_preview(
            config=config,
            executor=SimpleNamespace(),
            url="https://www.youtube.com/watch?v=test123",
            title_hint="Watched Video",
            source_type="video",
            csv_file="youtube_monitor",
            processing_status="monitor_preview",
            staging_origin="youtube_monitor",
            show_name_hint="Tracked Channel",
        )

    assert cleanup_calls == [SOURCE_ID]
    assert not (tmp_path / "var" / "summarise_staging" / f"{SOURCE_ID}.json").exists()


def test_save_confirmed_discards_expired_staging(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    config = _make_config(tmp_path)

    staging_dir = tmp_path / "var" / "summarise_staging"
    staging_dir.mkdir(parents=True, exist_ok=True)
    staging_path = staging_dir / f"{SOURCE_ID}.json"
    staging_path.write_text(
        json.dumps(
            {
                "source_id": SOURCE_ID,
                "url": "https://www.youtube.com/watch?v=test123",
                "title": "Expired Preview",
                "source_type": "video",
                "created_at": time.time() - (8 * 24 * 60 * 60),
                "origin": "youtube_monitor",
            }
        ),
        encoding="utf-8",
    )

    discarded = []
    monkeypatch.setattr(
        "gateway.save_confirmed_handler.discard_staging_preview",
        lambda path, staging, config: discarded.append((path.name, staging["source_id"])),
    )

    with pytest.raises(ValueError, match="expired"):
        handle_save_confirmed_job(
            Event(
                type="human_message",
                payload={"text": f"/save_confirmed {SOURCE_ID}"},
                source="telegram",
            ),
            Job(event_id=1, skill="save_confirmed", id=1),
            config,
            executor=SimpleNamespace(),
        )

    assert discarded == [(staging_path.name, SOURCE_ID)]


def test_auto_reflect_enqueues_event_and_job(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    import gateway.queue

    inserted = {"events": [], "jobs": []}

    class DummyQueueForReflect:
        def insert_event(self, event):
            inserted["events"].append(event)
            return 7

        def insert_job(self, job):
            inserted["jobs"].append(job)
            return 11

    monkeypatch.setattr(gateway.queue, "Queue", lambda: DummyQueueForReflect())

    result = maybe_trigger_auto_reflect(
        {
            "landscape_signals": {"breakthroughs": [{"theme_id": "autonomous_agents"}]},
            "implications": [],
        }
    )

    assert result is True
    assert inserted["events"]
    assert inserted["jobs"]
    assert inserted["events"][0].payload["text"] == '/reflect topic "autonomous_agents"'
    assert inserted["jobs"][0].skill == "reflect"
