"""Native OpenRouter streaming client helpers."""

from __future__ import annotations

import json
from typing import Any, Iterator

import httpx


class OpenRouterAPIError(RuntimeError):
    """Raised when the OpenRouter API returns an error response."""

    def __init__(self, message: str, *, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


def _chat_completions_url(base_url: str) -> str:
    normalized = (base_url or "https://openrouter.ai/api/v1").strip().rstrip("/")
    if normalized.endswith("/chat/completions"):
        return normalized
    if normalized.endswith("/v1"):
        return normalized + "/chat/completions"
    if normalized.endswith("/api"):
        return normalized + "/v1/chat/completions"
    return normalized + "/chat/completions"


def _delta_text(delta: Any) -> str:
    if isinstance(delta, str):
        return delta
    if isinstance(delta, list):
        return "".join(_delta_text(item) for item in delta)
    if not isinstance(delta, dict):
        return ""

    content = delta.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
            elif isinstance(item, str):
                parts.append(item)
        return "".join(parts)

    reasoning = delta.get("reasoning")
    if isinstance(reasoning, str):
        return reasoning
    return ""


def stream_chat(
    *,
    api_key: str,
    base_url: str,
    model: str,
    messages: list[dict[str, str]],
    timeout: int,
    fallback_models: list[str] | None = None,
    provider_order: list[str] | None = None,
    app_name: str | None = None,
    http_referer: str | None = None,
) -> Iterator[dict[str, Any]]:
    """Stream chat completion events from OpenRouter."""
    if not api_key.strip():
        raise OpenRouterAPIError("Missing OPENROUTER_API_KEY.")

    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }
    if app_name:
        headers["X-Title"] = app_name.strip()
    if http_referer:
        headers["HTTP-Referer"] = http_referer.strip()

    payload: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "stream": True,
        "stream_options": {"include_usage": True},
    }
    if fallback_models:
        payload["models"] = [model, *[candidate for candidate in fallback_models if candidate and candidate != model]]
    if provider_order:
        payload["provider"] = {"order": provider_order}

    yield {"type": "progress", "text": "Routing request..."}

    timeout_config = httpx.Timeout(connect=min(timeout, 20.0), read=timeout, write=min(timeout, 20.0), pool=min(timeout, 20.0))
    with httpx.Client(timeout=timeout_config) as client:
        with client.stream(
            "POST",
            _chat_completions_url(base_url),
            headers=headers,
            json=payload,
        ) as response:
            if response.status_code >= 400:
                try:
                    error_body = response.json()
                except ValueError:
                    error_body = response.text
                raise OpenRouterAPIError(
                    f"OpenRouter error ({response.status_code}): {str(error_body)[:400]}",
                    status_code=response.status_code,
                )

            for raw_line in response.iter_lines():
                line = (raw_line or "").strip()
                if not line or not line.startswith("data:"):
                    continue

                data = line[5:].strip()
                if not data:
                    continue
                if data == "[DONE]":
                    break

                try:
                    event = json.loads(data)
                except json.JSONDecodeError:
                    continue

                if not isinstance(event, dict):
                    continue

                error_data = event.get("error")
                if error_data:
                    raise OpenRouterAPIError(str(error_data)[:400], status_code=response.status_code)

                usage = event.get("usage")
                provider_name = event.get("provider")
                if usage or provider_name:
                    yield {
                        "type": "meta",
                        "usage": usage if isinstance(usage, dict) else None,
                        "provider": provider_name,
                    }

                choices = event.get("choices")
                if not isinstance(choices, list):
                    continue

                for choice in choices:
                    if not isinstance(choice, dict):
                        continue
                    delta = choice.get("delta")
                    text = _delta_text(delta)
                    if text:
                        yield {"type": "delta", "text": text}
