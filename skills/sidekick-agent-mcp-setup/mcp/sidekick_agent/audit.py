"""Audit logger: append JSONL entries to pending log file.

Log structure: one file per session, one JSON line per sidekick call.
Downstream hooks can merge pending logs into a session audit trail.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from . import config


# Emit at most one stderr warning per process when the log file cannot be
# written — subsequent failures are silently dropped to avoid flooding stderr.
_WRITE_WARNED = False


def _resolve_session_id(override: str = "") -> str:
    if override:
        return override
    if config.SESSION_ID:
        return config.SESSION_ID
    return f"unknown-{os.getpid()}-{int(time.time())}"


def _log_path(session_id: str) -> Path:
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    return config.LOG_DIR / f"{session_id}.jsonl"


def log_call(
    *,
    tool: str,
    files: list[str],
    input_chars: int,
    output_chars: int,
    duration_ms: int,
    prompt_tokens: int,
    completion_tokens: int,
    status: str,
    error: str | None = None,
    rejected: list[dict] | None = None,
    session_id: str = "",
) -> None:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "tool": tool,
        "files": files,
        "input_chars": input_chars,
        "output_chars": output_chars,
        "duration_ms": duration_ms,
        "model": config.MODEL,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "status": status,
        "error": error,
    }
    if rejected:
        entry["rejected"] = rejected

    path = _log_path(_resolve_session_id(session_id))
    try:
        with open(path, "a", encoding="utf-8") as fp:
            fp.write(json.dumps(entry, ensure_ascii=False))
            fp.write("\n")
    except OSError as exc:
        global _WRITE_WARNED
        if not _WRITE_WARNED:
            _WRITE_WARNED = True
            print(
                f"[sidekick-agent] WARNING: could not write audit log to {path}: {exc}. "
                "Subsequent failures suppressed.",
                file=sys.stderr,
            )
