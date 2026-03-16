"""Tests for shared source quality helpers."""

from ingest.source_quality import (
    assess_source_quality,
    get_landscape_issue,
    get_summary_issue,
    read_source_artifact_text,
)


def test_read_source_artifact_text_resolves_library_root(tmp_path):
    library_path = tmp_path / "library"
    source_dir = library_path / "src_123"
    source_dir.mkdir(parents=True)
    (source_dir / "deep_summary.md").write_text("Summary content", encoding="utf-8")

    assert read_source_artifact_text(library_path, "src_123", "deep_summary.md") == "Summary content"


def test_get_summary_issue_detects_placeholder_output():
    summary = "Summary generation failed because you've hit your limit."

    assert get_summary_issue(summary) == "placeholder"


def test_get_landscape_issue_detects_empty_output():
    signals = {
        "capabilities": [],
        "limitations": [],
        "bottlenecks": [],
        "breakthroughs": [],
    }

    assert get_landscape_issue(signals) == "empty"


def test_assess_source_quality_marks_missing_outputs_incomplete():
    assessment = assess_source_quality(
        theme_count=0,
        claim_count=0,
        summary_text="summary pending",
        landscape_signals={
            "capabilities": [],
            "limitations": [],
            "bottlenecks": [],
            "breakthroughs": [],
        },
        require_summary=True,
        require_landscape=True,
    )

    assert assessment["status"] == "incomplete"
    assert assessment["issues"] == [
        "no_themes",
        "no_claims",
        "summary:placeholder",
        "landscape:empty",
    ]
