"""Tests for ingest.http_retry module."""

import time
from unittest.mock import MagicMock

import httpx
import pytest

from ingest.http_retry import with_retry


def test_with_retry_succeeds_first_attempt():
    fn = MagicMock(return_value="ok")
    result = with_retry(fn, max_attempts=3, base_delay=0.01)
    assert result == "ok"
    assert fn.call_count == 1


def test_with_retry_succeeds_after_transient_failure():
    fn = MagicMock(side_effect=[httpx.ConnectError("fail"), "ok"])
    result = with_retry(fn, max_attempts=3, base_delay=0.01)
    assert result == "ok"
    assert fn.call_count == 2


def test_with_retry_raises_after_exhaustion():
    fn = MagicMock(side_effect=httpx.ConnectTimeout("timeout"))
    with pytest.raises(httpx.ConnectTimeout):
        with_retry(fn, max_attempts=2, base_delay=0.01)
    assert fn.call_count == 2


def test_with_retry_non_retryable_status_raises_immediately():
    resp = httpx.Response(404, request=httpx.Request("GET", "http://example.com"))
    fn = MagicMock(side_effect=httpx.HTTPStatusError("not found", request=resp.request, response=resp))
    with pytest.raises(httpx.HTTPStatusError):
        with_retry(fn, max_attempts=3, base_delay=0.01)
    assert fn.call_count == 1


def test_with_retry_retryable_status_retries():
    resp_429 = httpx.Response(429, request=httpx.Request("GET", "http://example.com"))
    resp_ok = "ok"
    fn = MagicMock(side_effect=[
        httpx.HTTPStatusError("rate limit", request=resp_429.request, response=resp_429),
        resp_ok,
    ])
    result = with_retry(fn, max_attempts=3, base_delay=0.01)
    assert result == "ok"
    assert fn.call_count == 2


def test_with_retry_respects_retry_after_header():
    resp_429 = httpx.Response(
        429,
        request=httpx.Request("GET", "http://example.com"),
        headers={"Retry-After": "0.05"},
    )
    fn = MagicMock(side_effect=[
        httpx.HTTPStatusError("rate limit", request=resp_429.request, response=resp_429),
        "ok",
    ])
    t0 = time.monotonic()
    result = with_retry(fn, max_attempts=3, base_delay=0.01, max_delay=1.0)
    elapsed = time.monotonic() - t0
    assert result == "ok"
    assert elapsed >= 0.04  # Should have waited ~0.05s


def test_with_retry_retryable_exceptions_catches_runtime_error():
    """with_retry should retry RuntimeError when passed as retryable_exceptions."""
    fn = MagicMock(side_effect=[RuntimeError("CLI failed"), "ok"])
    result = with_retry(
        fn, max_attempts=3, base_delay=0.01,
        retryable_exceptions=(RuntimeError,),
    )
    assert result == "ok"
    assert fn.call_count == 2


def test_with_retry_retryable_exceptions_raises_after_exhaustion():
    """with_retry should raise after exhausting attempts for custom exceptions."""
    fn = MagicMock(side_effect=RuntimeError("CLI failed"))
    with pytest.raises(RuntimeError):
        with_retry(
            fn, max_attempts=2, base_delay=0.01,
            retryable_exceptions=(RuntimeError,),
        )
    assert fn.call_count == 2


def test_with_retry_without_retryable_exceptions_does_not_catch_runtime():
    """RuntimeError should NOT be caught without retryable_exceptions."""
    fn = MagicMock(side_effect=RuntimeError("CLI failed"))
    with pytest.raises(RuntimeError):
        with_retry(fn, max_attempts=3, base_delay=0.01)
    assert fn.call_count == 1
