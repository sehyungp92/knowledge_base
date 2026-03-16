"""Integration tests for save_pipeline orchestration.

Tests that the pipeline creates source rows and marks them complete,
exercising the persistence path that caused FK violations.
"""

import json
import pytest
from unittest.mock import MagicMock


_SAMPLE_TEXT = "Test content about AI reasoning and planning in complex systems. " * 50


def _make_pipeline_side_effect():
    """Return a side_effect function that inspects prompts to return
    appropriate mock responses for each pipeline stage."""

    def _run_raw(*args, **kwargs):
        prompt = args[0] if args else kwargs.get("prompt", "")
        prompt_lower = prompt.lower() if isinstance(prompt, str) else ""

        result = MagicMock(
            cost_usd=0.001,
            usage={"input_tokens": 100, "output_tokens": 50},
            success=True,
            return_code=0,
            is_timeout=False,
        )

        if "classify" in prompt_lower or (
            "theme" in prompt_lower and "claim" not in prompt_lower
        ):
            # Theme classification
            result.text = '[{"theme_id": "reasoning_and_planning", "relevance": 0.8, "level": 1}]'
        elif "claim" in prompt_lower or "extract" in prompt_lower:
            # Claims + summary merged
            claims_json = json.dumps({
                "claims": [{
                    "claim": "AI systems show improved reasoning capabilities",
                    "type": "capability",
                    "confidence": 0.8,
                    "evidence_snippet": "Test content about AI reasoning and planning",
                }],
                "concepts": [],
            })
            summary_lines = (
                "# Deep Summary\n\n"
                "This source examines advances in AI reasoning and planning capabilities. "
                "The research demonstrates that modern systems can handle complex multi-step "
                "planning tasks with improved accuracy. Experiments show promising results "
                "across a range of benchmarks measuring logical deduction and strategic "
                "decision-making in open-ended environments."
            )
            result.text = f"{claims_json}\n---SUMMARY---\n{summary_lines}"
        elif "landscape" in prompt_lower or "capabilit" in prompt_lower or "limitation" in prompt_lower:
            # Landscape extraction
            result.text = json.dumps({
                "capabilities": [{
                    "name": "multi-step reasoning",
                    "description": "Improved reasoning in AI planning systems",
                    "maturity": "emerging",
                }],
                "limitations": [],
                "bottlenecks": [],
                "breakthroughs": [],
            })
        elif "implication" in prompt_lower:
            # Cross-theme implications
            result.text = "[]"
        else:
            # Fallback: return theme-classification format
            result.text = '[{"theme_id": "reasoning_and_planning", "relevance": 0.8, "level": 1}]'

        return result

    return _run_raw


@pytest.mark.integration
class TestSavePipelineIntegration:
    """Test run_save_pipeline with real Postgres."""

    def test_source_row_created_if_missing(self, pg_conn):
        """Pipeline creates source row via idempotent upsert."""
        get_conn, _, theme_ids = pg_conn

        new_source_id = "src_integ_pipeline_001"

        # Ensure it doesn't exist yet
        with get_conn() as conn:
            conn.execute("DELETE FROM sources WHERE id = %s", (new_source_id,))
            conn.commit()

        try:
            from ingest.save_pipeline import run_save_pipeline

            # Use a mock executor to avoid actual LLM calls
            mock_executor = MagicMock()
            mock_result = MagicMock(
                text='[{"theme_id": "reasoning_and_planning", "relevance": 0.8, "level": 1}]',
                cost_usd=0.001,
                usage={"input_tokens": 100, "output_tokens": 50},
                success=True,
                return_code=0,
                is_timeout=False,
            )
            mock_executor.run_raw.return_value = mock_result

            run_save_pipeline(
                clean_text="Test text about reasoning and planning in AI systems. " * 50,
                source_id=new_source_id,
                source_type="article",
                title="Integration Test Pipeline Source",
                executor=mock_executor,
                get_conn_fn=get_conn,
            )

            # Verify source row was created
            with get_conn() as conn:
                row = conn.execute(
                    "SELECT id, processing_status FROM sources WHERE id = %s",
                    (new_source_id,),
                ).fetchone()

            assert row is not None
            assert row["id"] == new_source_id
        finally:
            # Cleanup
            with get_conn() as conn:
                conn.execute(
                    "DELETE FROM source_themes WHERE source_id = %s", (new_source_id,)
                )
                conn.execute(
                    "DELETE FROM sources WHERE id = %s", (new_source_id,)
                )
                conn.commit()

    def test_pipeline_marks_source_complete(self, pg_conn):
        """Pipeline sets processing_status to 'complete' at the end."""
        get_conn, source_id, theme_ids = pg_conn

        from ingest.save_pipeline import run_save_pipeline

        mock_executor = MagicMock()
        mock_executor.run_raw.side_effect = _make_pipeline_side_effect()

        run_save_pipeline(
            clean_text=_SAMPLE_TEXT,
            source_id=source_id,
            source_type="article",
            title="Integration Test Source",
            executor=mock_executor,
            get_conn_fn=get_conn,
        )

        with get_conn() as conn:
            row = conn.execute(
                "SELECT processing_status FROM sources WHERE id = %s",
                (source_id,),
            ).fetchone()

        assert row is not None
        assert row["processing_status"] == "complete"

    def test_pipeline_returns_valid_structure(self, pg_conn):
        """Pipeline returns dict with expected keys even with mock executor."""
        get_conn, source_id, theme_ids = pg_conn

        from ingest.save_pipeline import run_save_pipeline

        mock_executor = MagicMock()
        mock_executor.run_raw.side_effect = _make_pipeline_side_effect()

        result = run_save_pipeline(
            clean_text=_SAMPLE_TEXT,
            source_id=source_id,
            source_type="article",
            title="Integration Test Source",
            executor=mock_executor,
            get_conn_fn=get_conn,
        )

        assert isinstance(result, dict)
        assert "themes" in result
        assert "errors" in result
        assert "timings" in result
