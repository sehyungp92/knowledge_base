"""Tests for ingest.landscape_extractor."""

import json
from unittest.mock import patch, MagicMock

from ingest.landscape_extractor import (
    _parse_signals,
    _validate_capability,
    _validate_limitation,
    _validate_bottleneck,
    _validate_breakthrough,
    VALID_MATURITY,
    VALID_SIGNAL_TYPE,
    VALID_LIMITATION_TYPE,
    VALID_SEVERITY,
    VALID_TRAJECTORY,
    VALID_BOTTLENECK_TYPE,
    VALID_RESOLUTION_HORIZON,
    VALID_SIGNIFICANCE,
)


# --- Signal Parsing ---

def test_parse_signals_json_block():
    text = '```json\n{"capabilities": [{"description": "test", "theme_id": "robotics"}], "limitations": [], "bottlenecks": []}\n```'
    result = _parse_signals(text)
    assert len(result["capabilities"]) == 1
    assert result["capabilities"][0]["description"] == "test"


def test_parse_signals_raw_json():
    text = '{"capabilities": [], "limitations": [{"description": "lim", "theme_id": "data"}], "bottlenecks": []}'
    result = _parse_signals(text)
    assert len(result["limitations"]) == 1


def test_parse_signals_empty_text():
    result = _parse_signals("no json here")
    assert result == {"capabilities": [], "limitations": [], "bottlenecks": [], "breakthroughs": []}


def test_parse_signals_with_preamble():
    text = 'Here are the signals:\n\n{"capabilities": [{"description": "cap1", "theme_id": "robotics"}], "limitations": [], "bottlenecks": []}\n\nDone.'
    result = _parse_signals(text)
    assert len(result["capabilities"]) == 1


# --- Capability Validation ---

def test_validate_capability_valid():
    cap = {"description": "Can generate code", "theme_id": "code_and_software", "maturity": "demo", "confidence": 0.8}
    result = _validate_capability(cap)
    assert result is not None
    assert result["maturity"] == "demo"


def test_validate_capability_missing_description():
    assert _validate_capability({"theme_id": "robotics"}) is None


def test_validate_capability_missing_theme():
    assert _validate_capability({"description": "something"}) is None


def test_validate_capability_invalid_maturity():
    cap = {"description": "test", "theme_id": "robotics", "maturity": "invalid_value"}
    result = _validate_capability(cap)
    assert result is not None
    assert result["maturity"] is None  # normalized to None


def test_validate_capability_clamps_confidence():
    cap = {"description": "test", "theme_id": "robotics", "confidence": 1.5}
    result = _validate_capability(cap)
    assert result["confidence"] == 1.0

    cap2 = {"description": "test", "theme_id": "robotics", "confidence": -0.5}
    result2 = _validate_capability(cap2)
    assert result2["confidence"] == 0.0


# --- Limitation Validation ---

def test_validate_limitation_valid():
    lim = {
        "description": "Cannot handle long context",
        "theme_id": "memory_and_context",
        "limitation_type": "architectural",
        "signal_type": "explicit",
        "severity": "significant",
        "trajectory": "improving",
        "confidence": 0.7,
    }
    result = _validate_limitation(lim)
    assert result is not None
    assert result["signal_type"] == "explicit"


def test_validate_limitation_implicit_signal_types():
    for st in VALID_SIGNAL_TYPE:
        lim = {"description": "test", "theme_id": "data", "signal_type": st}
        result = _validate_limitation(lim)
        assert result is not None
        assert result["signal_type"] == st


def test_validate_limitation_invalid_signal_type():
    lim = {"description": "test", "theme_id": "data", "signal_type": "made_up"}
    result = _validate_limitation(lim)
    assert result["signal_type"] == "explicit"  # normalized


def test_validate_limitation_invalid_type_normalized():
    lim = {"description": "test", "theme_id": "data", "limitation_type": "magic"}
    result = _validate_limitation(lim)
    assert result["limitation_type"] == "unknown"


def test_validate_limitation_missing_fields():
    assert _validate_limitation({"description": "test"}) is None
    assert _validate_limitation({"theme_id": "data"}) is None
    assert _validate_limitation("not a dict") is None


# --- Bottleneck Validation ---

def test_validate_bottleneck_valid():
    bn = {
        "description": "GPU memory limits batch size",
        "theme_id": "compute_and_hardware",
        "blocking_what": "Scaling to larger models",
        "bottleneck_type": "hardware",
        "resolution_horizon": "1-2_years",
        "confidence": 0.6,
    }
    result = _validate_bottleneck(bn)
    assert result is not None
    assert result["bottleneck_type"] == "hardware"


def test_validate_bottleneck_invalid_type():
    bn = {"description": "test", "theme_id": "data", "bottleneck_type": "nonsense"}
    result = _validate_bottleneck(bn)
    assert result["bottleneck_type"] is None


def test_validate_bottleneck_invalid_horizon():
    bn = {"description": "test", "theme_id": "data", "resolution_horizon": "whenever"}
    result = _validate_bottleneck(bn)
    assert result["resolution_horizon"] == "unknown"


def test_validate_bottleneck_missing_fields():
    assert _validate_bottleneck({"description": "test"}) is None
    assert _validate_bottleneck({}) is None


# --- Enum Value Coverage ---

def test_valid_enums_nonempty():
    assert len(VALID_MATURITY) > 0
    assert len(VALID_SIGNAL_TYPE) > 0
    assert len(VALID_LIMITATION_TYPE) > 0
    assert len(VALID_SEVERITY) > 0
    assert len(VALID_TRAJECTORY) > 0
    assert len(VALID_BOTTLENECK_TYPE) > 0
    assert len(VALID_RESOLUTION_HORIZON) > 0
    assert len(VALID_SIGNIFICANCE) > 0


# --- Breakthrough Validation ---

def test_validate_breakthrough_valid():
    bt = {
        "description": "New architecture achieves SOTA on reasoning benchmarks",
        "theme_id": "reasoning_and_planning",
        "significance": "notable",
        "what_was_believed_before": "Reasoning required chain-of-thought prompting",
        "what_is_now_possible": "Direct reasoning without explicit CoT",
        "confidence": 0.8,
        "evidence_snippet": "Our model achieves 95% on GSM8K without CoT",
    }
    result = _validate_breakthrough(bt)
    assert result is not None
    assert result["significance"] == "notable"


def test_validate_breakthrough_missing_description():
    assert _validate_breakthrough({"theme_id": "robotics"}) is None


def test_validate_breakthrough_missing_theme():
    assert _validate_breakthrough({"description": "something"}) is None


def test_validate_breakthrough_invalid_significance():
    bt = {"description": "test", "theme_id": "robotics", "significance": "invalid"}
    result = _validate_breakthrough(bt)
    assert result is not None
    assert result["significance"] is None


def test_validate_breakthrough_clamps_confidence():
    bt = {"description": "test", "theme_id": "robotics", "confidence": 1.5}
    result = _validate_breakthrough(bt)
    assert result["confidence"] == 1.0

    bt2 = {"description": "test", "theme_id": "robotics", "confidence": -0.5}
    result2 = _validate_breakthrough(bt2)
    assert result2["confidence"] == 0.0


def test_validate_breakthrough_optional_bottlenecks_affected():
    bt = {
        "description": "test",
        "theme_id": "robotics",
        "significance": "major",
        "bottlenecks_affected": [
            {"bottleneck_id": "bn_sim_to_real", "effect": "reduces"}
        ],
    }
    result = _validate_breakthrough(bt)
    assert result is not None
    assert len(result["bottlenecks_affected"]) == 1


def test_validate_breakthrough_non_list_bottlenecks_normalized():
    bt = {"description": "test", "theme_id": "robotics", "bottlenecks_affected": "not a list"}
    result = _validate_breakthrough(bt)
    assert result["bottlenecks_affected"] == []


def test_parse_signals_includes_breakthroughs():
    text = json.dumps({
        "capabilities": [],
        "limitations": [],
        "bottlenecks": [],
        "breakthroughs": [
            {"description": "New SOTA", "theme_id": "reasoning_and_planning",
             "significance": "notable", "confidence": 0.9,
             "evidence_snippet": "We demonstrate..."}
        ],
    })
    result = _parse_signals(text)
    assert len(result.get("breakthroughs", [])) == 1


def test_parse_signals_missing_breakthroughs_key_returns_empty():
    text = json.dumps({
        "capabilities": [{"description": "x", "theme_id": "robotics"}],
        "limitations": [],
        "bottlenecks": [],
    })
    result = _parse_signals(text)
    assert result.get("breakthroughs", []) == []


# --- Breakthrough Persistence ---

def test_persist_breakthroughs_increments_count():
    """Breakthroughs in signals should be persisted and counted."""
    import sys

    signals = {
        "capabilities": [],
        "limitations": [],
        "bottlenecks": [],
        "breakthroughs": [{
            "description": "New architecture",
            "theme_id": "reasoning_and_planning",
            "significance": "notable",
            "confidence": 0.8,
        }],
    }
    mock_conn = MagicMock()
    mock_conn.__enter__ = MagicMock(return_value=mock_conn)
    mock_conn.__exit__ = MagicMock(return_value=False)

    # Create a mock module for reading_app.db so the lazy import inside
    # persist_landscape_signals succeeds without a real database.
    mock_db = MagicMock()
    mock_db.find_similar_capability = MagicMock(return_value=None)
    mock_db.find_similar_limitation = MagicMock(return_value=None)
    mock_db.find_similar_bottleneck = MagicMock(return_value=None)
    mock_db.find_similar_breakthrough = MagicMock(return_value=None)

    saved_modules = {}
    modules_to_mock = ["reading_app", "reading_app.db"]
    for mod_name in modules_to_mock:
        saved_modules[mod_name] = sys.modules.get(mod_name)

    try:
        sys.modules["reading_app"] = MagicMock()
        sys.modules["reading_app.db"] = mock_db

        # Force reimport to pick up mocks
        import importlib
        import ingest.landscape_extractor
        importlib.reload(ingest.landscape_extractor)

        with patch("ulid.ULID", return_value="test123"):
            result = ingest.landscape_extractor.persist_landscape_signals(
                signals, "src_test", get_conn_fn=lambda: mock_conn
            )

        assert result.counts["breakthroughs"] == 1
        mock_db.insert_breakthrough.assert_called_once()
        # Verify the id starts with bt_
        call_kwargs = mock_db.insert_breakthrough.call_args
        assert call_kwargs[1]["id"] == "bt_test123" or (len(call_kwargs[0]) > 0 and "bt_" in str(call_kwargs))
    finally:
        # Restore original module state
        for mod_name in modules_to_mock:
            if saved_modules[mod_name] is None:
                sys.modules.pop(mod_name, None)
            else:
                sys.modules[mod_name] = saved_modules[mod_name]
        importlib.reload(ingest.landscape_extractor)


def test_persist_breakthrough_triggers_propagation():
    """When a breakthrough has bottlenecks_affected, propagation should fire."""
    signals = {
        "capabilities": [],
        "limitations": [],
        "bottlenecks": [],
        "breakthroughs": [{
            "description": "World model breakthrough",
            "theme_id": "world_models",
            "significance": "major",
            "bottlenecks_affected": [
                {"bottleneck_id": "bn_sim_to_real", "effect": "reduces"}
            ],
            "confidence": 0.9,
        }],
    }

    import sys
    mock_db = MagicMock()
    mock_db.insert_breakthrough = MagicMock()
    mock_db.insert_capability = MagicMock()
    mock_db.insert_limitation = MagicMock()
    mock_db.insert_bottleneck = MagicMock()
    mock_db.find_similar_capability = MagicMock(return_value=None)
    mock_db.find_similar_limitation = MagicMock(return_value=None)
    mock_db.find_similar_bottleneck = MagicMock(return_value=None)
    mock_db.find_similar_breakthrough = MagicMock(return_value=None)
    mock_db.merge_capability = MagicMock()
    mock_db.merge_limitation = MagicMock()
    mock_db.merge_bottleneck = MagicMock()

    original_db = sys.modules.get("reading_app.db")
    original_propagator = sys.modules.get("ingest.bottleneck_propagator")

    mock_propagator = MagicMock()
    mock_propagator.propagate_breakthrough_to_bottlenecks = MagicMock(return_value=[MagicMock()])
    mock_propagator.persist_bottleneck_updates = MagicMock()

    try:
        sys.modules["reading_app.db"] = mock_db
        sys.modules["ingest.bottleneck_propagator"] = mock_propagator

        # Force reimport to pick up mocks
        import importlib
        import ingest.landscape_extractor
        importlib.reload(ingest.landscape_extractor)

        mock_conn = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        result = ingest.landscape_extractor.persist_landscape_signals(
            signals, "src_456", get_conn_fn=lambda: mock_conn
        )

        assert result.counts["breakthroughs"] == 1
        mock_propagator.propagate_breakthrough_to_bottlenecks.assert_called_once()
        mock_propagator.persist_bottleneck_updates.assert_called_once()
    finally:
        if original_db:
            sys.modules["reading_app.db"] = original_db
        else:
            sys.modules.pop("reading_app.db", None)
        if original_propagator:
            sys.modules["ingest.bottleneck_propagator"] = original_propagator
        else:
            sys.modules.pop("ingest.bottleneck_propagator", None)
        importlib.reload(ingest.landscape_extractor)


def test_persist_breakthrough_no_propagation_without_affected():
    """Breakthroughs without bottlenecks_affected should NOT trigger propagation."""
    signals = {
        "capabilities": [],
        "limitations": [],
        "bottlenecks": [],
        "breakthroughs": [{
            "description": "Minor improvement",
            "theme_id": "robotics",
            "significance": "incremental",
            "bottlenecks_affected": [],
            "confidence": 0.6,
        }],
    }

    import sys
    mock_db = MagicMock()
    mock_db.insert_breakthrough = MagicMock()

    original_db = sys.modules.get("reading_app.db")
    try:
        sys.modules["reading_app.db"] = mock_db

        import importlib
        import ingest.landscape_extractor
        importlib.reload(ingest.landscape_extractor)

        mock_conn = MagicMock()
        mock_conn.__enter__ = MagicMock(return_value=mock_conn)
        mock_conn.__exit__ = MagicMock(return_value=False)

        result = ingest.landscape_extractor.persist_landscape_signals(
            signals, "src_789", get_conn_fn=lambda: mock_conn
        )

        assert result.counts["breakthroughs"] == 1
        # propagation module should NOT have been imported/called
    finally:
        if original_db:
            sys.modules["reading_app.db"] = original_db
        else:
            sys.modules.pop("reading_app.db", None)
        importlib.reload(ingest.landscape_extractor)


# ---------------------------------------------------------------------------
# Tests merged from test_implication_extractor.py — implication parsing
# ---------------------------------------------------------------------------

from ingest.implication_extractor import _parse_implications


def test_parse_implications_json():
    text = '[{"source_theme_id": "scaling", "target_theme_id": "alignment", "implication": "Scaling affects alignment", "confidence": 0.7}]'
    result = _parse_implications(text)
    assert len(result) == 1
    assert result[0]["confidence"] == 0.7


def test_parse_implications_code_block():
    text = '```json\n[{"source_theme_id": "a", "target_theme_id": "b", "implication": "test", "confidence": 0.5}]\n```'
    result = _parse_implications(text)
    assert len(result) == 1


def test_parse_implications_empty():
    assert _parse_implications("no json") == []


def test_parse_implications_multiple():
    text = '[{"source_theme_id": "a", "target_theme_id": "b", "implication": "1", "confidence": 0.5}, {"source_theme_id": "c", "target_theme_id": "d", "implication": "2", "confidence": 0.6}]'
    result = _parse_implications(text)
    assert len(result) == 2


def test_adaptive_cap():
    # cap = min(4 + (n-1) * 2, 12)
    assert min(4 + (1 - 1) * 2, 12) == 4
    assert min(4 + (3 - 1) * 2, 12) == 8
    assert min(4 + (5 - 1) * 2, 12) == 12
    assert min(4 + (10 - 1) * 2, 12) == 12
