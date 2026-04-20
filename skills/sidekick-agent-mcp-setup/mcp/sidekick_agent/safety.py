"""Path safety layer for sidekick-agent.

Enforces workspace whitelist + blacklist patterns + size limits.
All checks are defense-in-depth: callers should still validate input.
"""
from __future__ import annotations

import fnmatch
import os
from pathlib import Path

from . import config

DEFAULT_BLACKLIST_GLOBS = [
    "**/.env",
    "**/.env.*",
    "**/*token*",
    "**/*secret*",
    "**/*credential*",
    "**/*.key",
    "**/*.pem",
    "**/.git/**",
    "**/node_modules/**",
    "**/__pycache__/**",
]

BLACKLIST_GLOBS = DEFAULT_BLACKLIST_GLOBS + config.EXTRA_BLACKLIST_PATTERNS


def to_rel_str(abs_path: Path) -> str:
    """Return workspace-relative path with forward slashes (posix style).

    Falls back to `abs_path.name` when path is outside workspace — caller
    should have already validated containment via `resolve_in_workspace`.
    """
    try:
        rel = abs_path.relative_to(config.WORKSPACE_ROOT)
    except ValueError:
        return abs_path.name
    return str(rel).replace("\\", "/")


def match_blacklist(rel_path_posix: str) -> str | None:
    """Return the matching blacklist pattern (or None) for a workspace-relative path."""
    normalized = rel_path_posix.lower()
    for pattern in BLACKLIST_GLOBS:
        if fnmatch.fnmatch(normalized, pattern.lower()):
            return pattern
    return None


def resolve_in_workspace(path_str: str) -> tuple[Path | None, str | None]:
    """Resolve a path against workspace. Accepts relative (rooted at workspace)
    or absolute paths. Returns (abs_path, error_reason).

    Checks workspace containment + symlink-escape. Does NOT check existence,
    blacklist, or size — callers add those based on read/write intent.
    """
    if not path_str:
        return None, "empty_path"
    try:
        candidate = Path(path_str)
        if not candidate.is_absolute():
            candidate = config.WORKSPACE_ROOT / candidate
        abs_path = candidate.resolve()
    except (OSError, RuntimeError) as exc:
        return None, f"resolve_failed: {exc}"

    try:
        abs_path.relative_to(config.WORKSPACE_ROOT)
    except ValueError:
        return None, "outside_whitelist"

    # Symlink escape check (covers Windows junctions too)
    real = Path(os.path.realpath(abs_path))
    try:
        real.relative_to(config.WORKSPACE_ROOT)
    except ValueError:
        return None, "symlink_escapes_workspace"

    return abs_path, None


def is_safe(path_str: str) -> tuple[bool, str | None, float]:
    """Validate a single existing file path for reads.

    Returns (ok, reason_or_None, size_kb). size_kb is 0.0 when ok=False.
    Reason codes: empty_path, resolve_failed, outside_whitelist,
    symlink_escapes_workspace, blacklist:<pattern>, not_found, not_a_file,
    symlink_rejected, oversized:<kb>KB.
    """
    abs_path, err = resolve_in_workspace(path_str)
    if err:
        return False, err, 0.0

    rel_str = to_rel_str(abs_path)
    blacklisted = match_blacklist(rel_str)
    if blacklisted:
        return False, f"blacklist:{blacklisted}", 0.0

    if not abs_path.exists():
        return False, "not_found", 0.0
    if abs_path.is_symlink():
        return False, "symlink_rejected", 0.0
    if not abs_path.is_file():
        return False, "not_a_file", 0.0

    size_kb = abs_path.stat().st_size / 1024
    if size_kb > config.FILE_SIZE_KB:
        return False, f"oversized:{int(size_kb)}KB", size_kb

    return True, None, size_kb


def validate_paths(paths: list[str]) -> tuple[list[Path], list[dict]]:
    """Validate a list of paths for reads. Returns (accepted_paths, rejected_entries).

    Also enforces MAX_FILES and TOTAL_KB limits.
    """
    rejected: list[dict] = []
    accepted: list[Path] = []

    if len(paths) > config.MAX_FILES:
        rejected.append({
            "path": "<batch>",
            "reason": f"too_many_files:{len(paths)}>max_{config.MAX_FILES}",
        })
        return [], rejected

    total_kb = 0.0
    for p in paths:
        ok, reason, size_kb = is_safe(p)
        if not ok:
            rejected.append({"path": p, "reason": reason})
            continue
        total_kb += size_kb
        if total_kb > config.TOTAL_KB:
            rejected.append({
                "path": p,
                "reason": f"total_size_exceeded:{int(total_kb)}KB>max_{config.TOTAL_KB}",
            })
            break
        abs_p, _ = resolve_in_workspace(p)
        if abs_p is not None:
            accepted.append(abs_p)

    return accepted, rejected
