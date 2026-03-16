"""Configuration loader for the knowledge_base system."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from gateway.model_preferences import normalize_model_tier
from gateway.providers import normalize_provider_id


class Config:
    """Loads configuration from .env file and environment variables."""

    def __init__(self, env_path: Path | str | None = None):
        if env_path:
            load_dotenv(env_path, override=True)
        else:
            load_dotenv()

    @property
    def postgres_dsn(self) -> str:
        user = os.getenv("POSTGRES_USER", "kb_user")
        password = os.getenv("POSTGRES_PASSWORD", "kb_pass")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        db = os.getenv("POSTGRES_DB", "knowledge_base")
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"

    @property
    def ollama_base_url(self) -> str:
        return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    @property
    def telegram_bot_token(self) -> str:
        return os.getenv("TELEGRAM_BOT_TOKEN", "")

    @property
    def telegram_allowed_chat_id(self) -> str:
        return os.getenv("TELEGRAM_ALLOWED_CHAT_ID", "")

    @property
    def discord_bot_token(self) -> str:
        return os.getenv("DISCORD_BOT_TOKEN", "")

    @property
    def discord_allowed_user_id(self) -> str:
        return os.getenv("DISCORD_ALLOWED_USER_ID", "")

    @property
    def heartbeat_timezone(self) -> str:
        return os.getenv("HEARTBEAT_TIMEZONE", "America/New_York")

    @property
    def api_host(self) -> str:
        return os.getenv("KB_API_HOST", "127.0.0.1")

    @property
    def api_port(self) -> int:
        return int(os.getenv("KB_API_PORT", "8000"))

    @property
    def web_origins(self) -> list[str]:
        raw = os.getenv("KB_WEB_ORIGINS", "")
        return [
            origin.strip().rstrip("/")
            for origin in raw.split(",")
            if origin.strip()
        ]

    @property
    def default_provider(self) -> str:
        return normalize_provider_id(os.getenv("KB_DEFAULT_PROVIDER"))

    @property
    def default_model(self) -> str:
        return normalize_model_tier(os.getenv("KB_DEFAULT_MODEL"))

    @property
    def codex_cli_path(self) -> str:
        return os.getenv("CODEX_CLI_PATH", "")

    @property
    def zai_api_key(self) -> str:
        return os.getenv("ZAI_API_KEY", "")

    @property
    def zai_base_url(self) -> str:
        return os.getenv("ZAI_BASE_URL", "https://api.z.ai/api/anthropic")

    @property
    def zai_model_fast(self) -> str:
        return os.getenv("ZAI_MODEL_FAST", "GLM-4.5-Air")

    @property
    def zai_model_balanced(self) -> str:
        return os.getenv("ZAI_MODEL_BALANCED", "GLM-4.7")

    @property
    def zai_model_deep(self) -> str:
        return os.getenv("ZAI_MODEL_DEEP", "GLM-4.7")

    @property
    def openrouter_api_key(self) -> str:
        return os.getenv("OPENROUTER_API_KEY", "")

    @property
    def openrouter_base_url(self) -> str:
        return os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api")

    @property
    def openrouter_model_fast(self) -> str:
        return os.getenv("OPENROUTER_MODEL_FAST", "minimax/minimax-m2.5")

    @property
    def openrouter_model_balanced(self) -> str:
        return os.getenv("OPENROUTER_MODEL_BALANCED", "minimax/minimax-m2.5")

    @property
    def openrouter_model_deep(self) -> str:
        return os.getenv("OPENROUTER_MODEL_DEEP", "minimax/minimax-m2.5")

    @property
    def library_path(self) -> Path:
        return Path(os.getenv("LIBRARY_PATH", "./library"))

    @property
    def memory_path(self) -> Path:
        return Path(os.getenv("MEMORY_PATH", "./memory"))

    # AgentMail settings
    @property
    def agentmail_api_key(self) -> str:
        return os.getenv("AGENTMAIL_API_KEY", "")

    @property
    def agentmail_inbox_id(self) -> str:
        return os.getenv("AGENTMAIL_INBOX_ID", "")

    @property
    def monitor_email_to(self) -> str:
        return os.getenv("MONITOR_EMAIL_TO", "")

    # YouTube monitor
    @property
    def youtube_monitor_enabled(self) -> bool:
        return os.getenv("YOUTUBE_MONITOR_ENABLED", "false").lower() in ("true", "1", "yes")

    # News digest
    @property
    def news_digest_enabled(self) -> bool:
        return os.getenv("NEWS_DIGEST_ENABLED", "false").lower() in ("true", "1", "yes")

    @property
    def runtime_log_dir(self) -> Path:
        return Path(os.getenv("RUNTIME_LOG_DIR", "./var/runtime/logs"))

    @property
    def runtime_db_path(self) -> Path:
        return Path(os.getenv("RUNTIME_DB_PATH", "./var/runtime/runtime.db"))

    @property
    def runtime_db_wait_seconds(self) -> int:
        return int(os.getenv("RUNTIME_DB_WAIT_SECONDS", "60"))

    @property
    def scheduler_replay_days(self) -> int:
        return int(os.getenv("SCHEDULER_REPLAY_DAYS", "3"))

    @property
    def youtube_startup_backlog_cap(self) -> int:
        return int(os.getenv("YOUTUBE_STARTUP_BACKLOG_CAP", "10"))
