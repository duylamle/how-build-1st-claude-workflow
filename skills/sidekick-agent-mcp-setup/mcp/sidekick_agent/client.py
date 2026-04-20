"""HTTP client for Anthropic-compatible endpoint.

Calls POST {API_BASE}/messages. Targets MiniMax via LiteLLM proxy or any
Anthropic-compatible gateway.
"""
from __future__ import annotations

import atexit
import time
from typing import Any

import httpx

from . import config


class SidekickError(Exception):
    """Raised when the upstream LLM call fails in a non-retryable way."""


# Module-level HTTP client — reuses TCP/TLS across calls. MCP stdio lifecycle
# is one process per session, so we keep this alive for the session and close
# via atexit.
_CLIENT: httpx.Client | None = None


def _get_client() -> httpx.Client:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = httpx.Client(timeout=config.TIMEOUT)
        atexit.register(_close_client)
    return _CLIENT


def _close_client() -> None:
    global _CLIENT
    if _CLIENT is not None:
        try:
            _CLIENT.close()
        except Exception:
            pass
        _CLIENT = None


# Retry constants
_RETRY_5XX_MAX = 2
_RETRY_5XX_BACKOFFS = (1.0, 3.0)
_RETRY_429_MAX = 2
_RETRY_429_DEFAULT_WAIT = 2.0
_RETRY_429_MAX_WAIT = 30.0


def _build_payload(
    system_prompt: str,
    user_prompt: str | None,
    *,
    thinking: bool = False,
    history: list[dict] | None = None,
    max_tokens: int | None = None,
    tools: list[dict] | None = None,
) -> dict[str, Any]:
    messages: list[dict] = list(history) if history else []
    if user_prompt is not None:
        messages.append({"role": "user", "content": user_prompt})

    if not messages:
        raise SidekickError("empty_messages: need either user_prompt or non-empty history")

    effective_max = config.resolve_max_tokens(max_tokens)

    payload: dict[str, Any] = {
        "model": config.MODEL,
        "max_tokens": effective_max,
        "system": system_prompt,
        "messages": messages,
        "temperature": config.TEMPERATURE,
        "stream": False,
    }
    if config.TOP_P != 1.0:
        payload["top_p"] = config.TOP_P
    if thinking:
        budget = max(1024, effective_max // 2)
        payload["thinking"] = {"type": "enabled", "budget_tokens": budget}
    if tools:
        payload["tools"] = tools
    return payload


def _parse_response(data: dict[str, Any]) -> tuple[str, dict[str, int], str, str]:
    base_resp = data.get("base_resp") or {}
    status_code = base_resp.get("status_code", 0)
    if status_code and status_code != 0:
        status_msg = base_resp.get("status_msg") or "unknown"
        raise SidekickError(f"upstream_error: base_resp.status_code={status_code}: {status_msg}")

    content = data.get("content") or []
    if not content:
        raise SidekickError(f"no_content_in_response: {data}")

    text_parts = [
        block.get("text", "")
        for block in content
        if block.get("type") == "text"
    ]
    text = "\n".join(text_parts).strip()

    stop_reason = data.get("stop_reason") or ""
    finish_reason = "length" if stop_reason == "max_tokens" else "stop"

    usage = data.get("usage") or {}
    tokens = {
        "prompt_tokens": int(usage.get("input_tokens", 0) or 0),
        "completion_tokens": int(usage.get("output_tokens", 0) or 0),
    }
    return text, tokens, finish_reason, stop_reason


def call_llm(
    system_prompt: str,
    user_prompt: str | None,
    *,
    thinking: bool = False,
    history: list[dict] | None = None,
    max_tokens: int | None = None,
    tools: list[dict] | None = None,
) -> dict[str, Any]:
    """Call the configured Anthropic-compatible LLM.

    Returns {text, usage, duration_ms, finish_reason, stop_reason, raw_content}.

    history: prior messages for multi-turn. user_prompt appended as latest
    turn; pass user_prompt=None to send history as-is (agent loop case after
    tool_result).
    raw_content: full response content array (needed to persist thinking
    blocks back into history — Anthropic requires returning them verbatim).
    max_tokens: optional per-call override. Falls back to config.MAX_TOKENS.
    tools: optional tool schema list (Anthropic format). Enables tool_use output.

    Retry policy:
      - Timeout: fail fast, no retry
      - 5xx: up to 2 retries, backoff 1s then 3s
      - 429: up to 2 retries, respecting Retry-After (capped 30s) with exponential fallback
      - 4xx other: fail fast
    """
    url = f"{config.API_BASE}/messages"
    headers = {
        "x-api-key": config.API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }
    payload = _build_payload(
        system_prompt, user_prompt,
        thinking=thinking, history=history, max_tokens=max_tokens, tools=tools,
    )

    attempts_5xx = 0
    attempts_429 = 0
    started = time.time()
    http = _get_client()

    while True:
        try:
            response = http.post(url, json=payload, headers=headers)
        except httpx.TimeoutException as exc:
            raise SidekickError(f"timeout_after_{config.TIMEOUT}s: {exc}") from exc
        except httpx.HTTPError as exc:
            raise SidekickError(f"http_error: {exc}") from exc

        status = response.status_code
        if status == 200:
            duration_ms = int((time.time() - started) * 1000)
            data = response.json()
            text, tokens, finish_reason, stop_reason = _parse_response(data)
            raw_content = data.get("content") or []
            return {
                "text": text,
                "usage": tokens,
                "duration_ms": duration_ms,
                "finish_reason": finish_reason,
                "stop_reason": stop_reason,
                "raw_content": raw_content,
            }

        if status == 429 and attempts_429 < _RETRY_429_MAX:
            retry_after = response.headers.get("Retry-After")
            base_wait = float(retry_after) if retry_after else _RETRY_429_DEFAULT_WAIT
            wait = min(base_wait * (2 ** attempts_429), _RETRY_429_MAX_WAIT)
            time.sleep(wait)
            attempts_429 += 1
            continue

        if 500 <= status < 600 and attempts_5xx < _RETRY_5XX_MAX:
            time.sleep(_RETRY_5XX_BACKOFFS[attempts_5xx])
            attempts_5xx += 1
            continue

        body_preview = response.text[:500]
        raise SidekickError(f"http_{status}: {body_preview}")
