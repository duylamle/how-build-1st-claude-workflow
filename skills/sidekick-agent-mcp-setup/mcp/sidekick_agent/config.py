"""Environment variable loading for sidekick-agent MCP server.

All settings are read from env vars with sensible defaults.
Required: SIDEKICK_API_KEY, SIDEKICK_API_BASE.

Backend: Anthropic-compatible endpoint only (POST {API_BASE}/messages).
Target deployment: MiniMax via VNG LiteLLM proxy.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def _require(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        print(f"ERROR: Missing required env var: {name}", file=sys.stderr)
        sys.exit(1)
    return value


def _get(name: str, default: str) -> str:
    return os.environ.get(name, default).strip() or default


def _get_int(name: str, default: int) -> int:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _get_float(name: str, default: float) -> float:
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _get_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name, "").strip().lower()
    if not raw:
        return default
    return raw not in ("0", "false", "no", "off")


def _parse_list(raw: str) -> list[str]:
    return [p.strip() for p in raw.split(",") if p.strip()]


API_KEY = _require("SIDEKICK_API_KEY")
API_BASE = _require("SIDEKICK_API_BASE").rstrip("/")
MODEL = _get("SIDEKICK_MODEL", "minimax/MiniMax-M2.7-highspeed")

WORKSPACE_ROOT = Path(_get("SIDEKICK_WORKSPACE_ROOT", os.getcwd())).resolve()
LOG_DIR = Path(
    _get("SIDEKICK_LOG_DIR", str(WORKSPACE_ROOT / "_logs" / "_sidekick-pending"))
).resolve()

EXTRA_BLACKLIST_PATTERNS = _parse_list(_get("SIDEKICK_EXTRA_BLACKLIST", ""))

TIMEOUT = _get_int("SIDEKICK_TIMEOUT", 60)
# MiniMax temperature range: (0.0, 1.0]. Clamp 0.01 lower bound because MiniMax
# rejects 0.0; upper bound enforced to match API contract.
TEMPERATURE = max(0.01, min(1.0, _get_float("SIDEKICK_TEMPERATURE", 0.2)))
MAX_TOKENS = _get_int("SIDEKICK_MAX_TOKENS", 8000)

# MiniMax M2.x context window: 204,800 tokens — raise file limits accordingly
FILE_SIZE_KB = _get_int("SIDEKICK_FILE_SIZE_KB", 500)
TOTAL_KB = _get_int("SIDEKICK_TOTAL_KB", 2000)
MAX_FILES = _get_int("SIDEKICK_MAX_FILES", 10)

TOP_P = _get_float("SIDEKICK_TOP_P", 1.0)
THINKING = _get_bool("SIDEKICK_THINKING", True)

# Agent loop config
WRITE_ALLOWLIST_PATTERNS = _parse_list(_get("SIDEKICK_WRITE_ALLOWLIST", ""))
AGENT_MAX_ITERATIONS = _get_int("SIDEKICK_AGENT_MAX_ITERATIONS", 15)
WRITE_FILE_SIZE_KB = _get_int("SIDEKICK_WRITE_FILE_SIZE_KB", 200)

# Conversation store caps (3 narrow tools). Prevents unbounded growth in long sessions.
MAX_CONVERSATIONS = _get_int("SIDEKICK_MAX_CONVERSATIONS", 32)
MAX_TURNS_PER_CONVERSATION = _get_int("SIDEKICK_MAX_TURNS_PER_CONVERSATION", 20)

# Read-file pagination default — agent tool trims output if larger than this.
READ_FILE_MAX_BYTES_DEFAULT = _get_int("SIDEKICK_READ_FILE_MAX_BYTES", 100_000)

SESSION_ID = os.environ.get("CLAUDE_SESSION_ID", "").strip()


def resolve_max_tokens(override: int | None) -> int:
    """Return a positive max_tokens value, using override if set, else default."""
    if override and override > 0:
        return override
    return MAX_TOKENS
