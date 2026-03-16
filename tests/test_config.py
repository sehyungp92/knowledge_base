"""Tests for reading_app.config."""

from pathlib import Path

from reading_app.config import Config


def test_config_defaults(tmp_path, monkeypatch):
    monkeypatch.delenv("POSTGRES_USER", raising=False)
    monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)
    monkeypatch.delenv("POSTGRES_HOST", raising=False)
    monkeypatch.delenv("POSTGRES_PORT", raising=False)
    monkeypatch.delenv("POSTGRES_DB", raising=False)
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_ALLOWED_CHAT_ID", raising=False)
    monkeypatch.delenv("HEARTBEAT_TIMEZONE", raising=False)
    monkeypatch.delenv("LIBRARY_PATH", raising=False)
    monkeypatch.delenv("MEMORY_PATH", raising=False)

    env_file = tmp_path / ".env"
    env_file.write_text("")
    cfg = Config(env_file)

    assert cfg.postgres_dsn == "postgresql://kb_user:kb_pass@localhost:5432/knowledge_base"
    assert cfg.ollama_base_url == "http://localhost:11434"
    assert cfg.telegram_bot_token == ""
    assert cfg.heartbeat_timezone == "America/New_York"
    assert cfg.library_path == Path("./library")
    assert cfg.memory_path == Path("./memory")
    assert cfg.api_host == "127.0.0.1"
    assert cfg.api_port == 8000
    assert cfg.default_provider == "claude"
    assert cfg.default_model == "sonnet"
    assert cfg.codex_cli_path == ""
    assert cfg.zai_api_key == ""
    assert cfg.zai_base_url == "https://api.z.ai/api/anthropic"
    assert cfg.zai_model_fast == "GLM-4.5-Air"
    assert cfg.zai_model_balanced == "GLM-4.7"
    assert cfg.zai_model_deep == "GLM-4.7"
    assert cfg.openrouter_api_key == ""
    assert cfg.openrouter_base_url == "https://openrouter.ai/api"
    assert cfg.openrouter_model_fast == "openrouter/anthropic/claude-3.5-haiku"
    assert cfg.openrouter_model_balanced == "openrouter/anthropic/claude-sonnet-4.5"
    assert cfg.openrouter_model_deep == "openrouter/anthropic/claude-sonnet-4.5"
    assert cfg.runtime_log_dir == Path("./var/runtime/logs")
    assert cfg.runtime_db_path == Path("./var/runtime/runtime.db")
    assert cfg.runtime_db_wait_seconds == 60
    assert cfg.scheduler_replay_days == 3
    assert cfg.youtube_startup_backlog_cap == 10


def test_config_from_env(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "POSTGRES_USER=testuser\n"
        "POSTGRES_PASSWORD=testpass\n"
        "POSTGRES_HOST=db.local\n"
        "POSTGRES_PORT=5433\n"
        "POSTGRES_DB=testdb\n"
        "OLLAMA_BASE_URL=http://gpu:11434\n"
        "TELEGRAM_BOT_TOKEN=bot123\n"
        "TELEGRAM_ALLOWED_CHAT_ID=42\n"
        "KB_API_HOST=0.0.0.0\n"
        "KB_API_PORT=8100\n"
        "KB_DEFAULT_PROVIDER=codex\n"
        "KB_DEFAULT_MODEL=deep\n"
        "CODEX_CLI_PATH=C:/tools/codex.exe\n"
        "ZAI_API_KEY=zai-key\n"
        "ZAI_BASE_URL=https://proxy.example.test/anthropic\n"
        "ZAI_MODEL_FAST=GLM-FAST\n"
        "ZAI_MODEL_BALANCED=GLM-BALANCED\n"
        "ZAI_MODEL_DEEP=GLM-DEEP\n"
        "OPENROUTER_API_KEY=or-key\n"
        "OPENROUTER_BASE_URL=https://openrouter.example.test/api\n"
        "OPENROUTER_MODEL_FAST=openrouter/fast\n"
        "OPENROUTER_MODEL_BALANCED=openrouter/balanced\n"
        "OPENROUTER_MODEL_DEEP=openrouter/deep\n"
        "LIBRARY_PATH=/data/library\n"
        "MEMORY_PATH=/data/memory\n"
        "RUNTIME_LOG_DIR=/data/runtime/logs\n"
        "RUNTIME_DB_PATH=/data/runtime/runtime.db\n"
        "RUNTIME_DB_WAIT_SECONDS=120\n"
        "SCHEDULER_REPLAY_DAYS=5\n"
        "YOUTUBE_STARTUP_BACKLOG_CAP=12\n"
    )
    cfg = Config(env_file)

    assert "testuser:testpass@db.local:5433/testdb" in cfg.postgres_dsn
    assert cfg.ollama_base_url == "http://gpu:11434"
    assert cfg.telegram_bot_token == "bot123"
    assert cfg.telegram_allowed_chat_id == "42"
    assert cfg.api_host == "0.0.0.0"
    assert cfg.api_port == 8100
    assert cfg.default_provider == "codex"
    assert cfg.default_model == "opus"
    assert cfg.codex_cli_path == "C:/tools/codex.exe"
    assert cfg.zai_api_key == "zai-key"
    assert cfg.zai_base_url == "https://proxy.example.test/anthropic"
    assert cfg.zai_model_fast == "GLM-FAST"
    assert cfg.zai_model_balanced == "GLM-BALANCED"
    assert cfg.zai_model_deep == "GLM-DEEP"
    assert cfg.openrouter_api_key == "or-key"
    assert cfg.openrouter_base_url == "https://openrouter.example.test/api"
    assert cfg.openrouter_model_fast == "openrouter/fast"
    assert cfg.openrouter_model_balanced == "openrouter/balanced"
    assert cfg.openrouter_model_deep == "openrouter/deep"
    assert cfg.library_path == Path("/data/library")
    assert cfg.runtime_log_dir == Path("/data/runtime/logs")
    assert cfg.runtime_db_path == Path("/data/runtime/runtime.db")
    assert cfg.runtime_db_wait_seconds == 120
    assert cfg.scheduler_replay_days == 5
    assert cfg.youtube_startup_backlog_cap == 12
