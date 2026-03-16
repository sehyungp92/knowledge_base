from gateway.provider_latency import run_latency_harness


def test_provider_latency_harness_emits_json_report(tmp_path):
    sample_map = {
        "claude": {"success": True, "total_ms": 120, "ttft_ms": 70, "resume_success": True},
        "openrouter": {"success": True, "total_ms": 80, "ttft_ms": 30, "resume_success": False},
    }

    report = run_latency_harness(
        output_path=tmp_path / "report.json",
        providers=["claude", "openrouter"],
        samples_per_provider=2,
        measure=lambda provider_id: sample_map[provider_id],
    )

    assert report["providers"]
    assert "median_ttft_ms" in report["providers"][0]
    assert (tmp_path / "report.json").exists()


def test_provider_latency_harness_skips_executor_probe_when_measure_and_providers_supplied(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "gateway.provider_latency.ClaudeExecutor",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("executor should not be created")),
    )

    report = run_latency_harness(
        output_path=tmp_path / "report.json",
        providers=["openrouter"],
        measure=lambda _provider_id: {"success": True, "total_ms": 50, "ttft_ms": 20},
    )

    assert report["providers"][0]["id"] == "openrouter"
