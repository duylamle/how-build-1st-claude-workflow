"""Read + write tools exposed to the MiniMax agent loop.

Philosophy: sidekick stays text-in/text-out from Claude's perspective.
Internally the agent loop lets MiniMax read the workspace (and optionally
write inside a per-run allowlist) on its own instead of forcing Claude to
pre-stage every file path.

All tools funnel through `safety.py` primitives for path resolution +
blacklist + size checks. Writes additionally require the caller-supplied
allowlist.
"""
from __future__ import annotations

import fnmatch
import os
from pathlib import Path
from typing import Any

from . import config, safety


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_GREP_MATCHES = 50
MAX_LIST_ENTRIES = 200
GREP_SNIPPET_CHARS = 200

# File extensions the agent considers "text" for grep / read. We treat dotfiles
# (no suffix) via an explicit filename list since `Path.suffix` returns empty.
TEXT_EXTENSIONS = {
    ".md", ".txt", ".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".yaml",
    ".yml", ".toml", ".ini", ".cfg", ".sh", ".bash", ".sql", ".html", ".css",
    ".xml", ".csv", ".log",
}
TEXT_FILENAMES = {".gitignore", ".dockerignore", ".editorconfig", ".env.example"}

# Directories pruned from `os.walk` — these rarely contain user-authored text
# and scanning them burns I/O + hits blacklist anyway. Hidden dirs (starting
# with '.') are skipped blanket because they're usually tooling state.
BLACKLISTED_WALK_DIRS = {"node_modules", "__pycache__", ".venv", "venv"}


# ---------------------------------------------------------------------------
# Tool schemas (Anthropic tool_use format)
# ---------------------------------------------------------------------------

def _read_tool_schemas() -> list[dict[str, Any]]:
    return [
        {
            "name": "read_file",
            "description": (
                "Read a text file from the workspace. Optional offset/max_bytes "
                "for paginated reads of large files. Path must be inside the "
                "allowed workspace root, not match the blacklist, and not "
                "exceed the per-file size limit."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Workspace-relative or absolute path.",
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Byte offset to start reading from (default 0).",
                    },
                    "max_bytes": {
                        "type": "integer",
                        "description": (
                            "Max bytes to return. Default "
                            f"{config.READ_FILE_MAX_BYTES_DEFAULT}. "
                            "Set to 0 for 'no limit' (full file)."
                        ),
                    },
                },
                "required": ["path"],
            },
        },
        {
            "name": "list_dir",
            "description": (
                "List entries in a workspace directory. Returns file and folder "
                "names (not recursive). Use to discover what's available before "
                "calling read_file."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Workspace-relative or absolute directory path. Empty = workspace root.",
                    }
                },
                "required": ["path"],
            },
        },
        {
            "name": "grep_files",
            "description": (
                "Search for a literal string across files in a workspace folder. "
                f"Returns matching lines with file path and line number. Max "
                f"{MAX_GREP_MATCHES} matches per call. Use for locating where "
                "a term appears before deciding which file to read in full."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Literal string to search for (case-insensitive).",
                    },
                    "path": {
                        "type": "string",
                        "description": "Folder to search in. Empty = workspace root.",
                    },
                    "file_glob": {
                        "type": "string",
                        "description": "Optional glob filter (e.g. '*.md'). Default: all text files.",
                    },
                },
                "required": ["pattern"],
            },
        },
    ]


def _write_tool_schemas(allowlist_preview: str) -> list[dict[str, Any]]:
    return [
        {
            "name": "write_file",
            "description": (
                "Create or overwrite a text file. Path MUST match one of the "
                "allowed write patterns for this agent run. Writes outside "
                "the allowlist are rejected. Content is written as UTF-8. "
                f"Allowed patterns: {allowlist_preview}. "
                f"Max file size: {config.WRITE_FILE_SIZE_KB} KB."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Workspace-relative or absolute path inside an allowed pattern.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Full UTF-8 content to write. Overwrites if file exists.",
                    },
                },
                "required": ["path", "content"],
            },
        },
        {
            "name": "append_file",
            "description": (
                "Append text to an existing file (or create if missing). Same "
                "allowlist rules as write_file. Use for incremental logs or "
                "adding sections to a draft without overwriting prior content."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Workspace-relative or absolute path inside an allowed pattern.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Text to append. Prepends a newline if file is non-empty and does not end in one.",
                    },
                },
                "required": ["path", "content"],
            },
        },
    ]


def get_tool_schemas(include_write: bool, allowlist_patterns: list[str]) -> list[dict[str, Any]]:
    """Assemble the tool list for the agent loop.

    include_write: enable write_file + append_file only when caller allows.
    allowlist_patterns: the effective patterns (already resolved from env +
    per-call override) — embedded into the write tool descriptions so MiniMax
    knows what paths it may target.
    """
    schemas = _read_tool_schemas()
    if include_write and allowlist_patterns:
        preview = ", ".join(allowlist_patterns[:5])
        if len(allowlist_patterns) > 5:
            preview += f", ... (+{len(allowlist_patterns)-5} more)"
        schemas.extend(_write_tool_schemas(preview))
    return schemas


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_blacklisted_walk_dir(name: str) -> bool:
    # Hidden dirs (starting with '.') are skipped to avoid leaking tooling
    # state (.git, .venv, .idea, etc.). Keep an explicit allow in TEXT_FILENAMES
    # only for individual hidden files the user may intentionally target.
    return name in BLACKLISTED_WALK_DIRS or name.startswith(".")


def _is_text_file(path: Path) -> bool:
    if path.name in TEXT_FILENAMES:
        return True
    return path.suffix.lower() in TEXT_EXTENSIONS


def _resolve_dir_or_root(raw: str) -> tuple[Path | None, str | None]:
    """Resolve a directory arg (empty = workspace root)."""
    if not raw:
        return config.WORKSPACE_ROOT, None
    return safety.resolve_in_workspace(raw)


def _check_write_size(content: str) -> str | None:
    size_kb = len(content.encode("utf-8")) / 1024
    if size_kb > config.WRITE_FILE_SIZE_KB:
        return f"oversized: {int(size_kb)}KB > max_{config.WRITE_FILE_SIZE_KB}"
    return None


def _match_write_allowlist(rel_path_posix: str, patterns: list[str]) -> bool:
    normalized = rel_path_posix.lower()
    for pattern in patterns:
        if fnmatch.fnmatch(normalized, pattern.lower()):
            return True
    return False


def _validate_write_path(raw: str, allowlist: list[str]) -> tuple[Path | None, str | None]:
    """Resolve a write target and verify workspace + blacklist + allowlist.

    Write paths may point at a file that does not exist yet, so existence is
    NOT required. Everything else (containment, symlink escape, blacklist,
    allowlist) is enforced.
    """
    if not allowlist:
        return None, "write_disabled_no_allowlist"

    abs_path, err = safety.resolve_in_workspace(raw)
    if err:
        return None, err

    rel_str = safety.to_rel_str(abs_path)

    blacklisted = safety.match_blacklist(rel_str)
    if blacklisted:
        return None, f"blacklist:{blacklisted}"

    if not _match_write_allowlist(rel_str, allowlist):
        return None, "not_in_write_allowlist"

    # If the path already exists, reject symlinks explicitly; resolve_in_workspace
    # already blocked escaping symlinks but a same-workspace symlink would still
    # be silently followed by `write_text`.
    if abs_path.exists():
        if abs_path.is_symlink():
            return None, "symlink_rejected"
        if not abs_path.is_file():
            return None, "not_a_file"

    return abs_path, None


# ---------------------------------------------------------------------------
# Read tools
# ---------------------------------------------------------------------------

def _tool_read_file(args: dict) -> str:
    raw = args.get("path", "")
    if not raw:
        return "ERROR: empty_path"

    try:
        offset = max(0, int(args.get("offset") or 0))
    except (TypeError, ValueError):
        return "ERROR: invalid_offset"
    try:
        max_bytes_arg = int(args.get("max_bytes") if args.get("max_bytes") is not None else config.READ_FILE_MAX_BYTES_DEFAULT)
    except (TypeError, ValueError):
        return "ERROR: invalid_max_bytes"
    # max_bytes=0 means no cap (full file)
    max_bytes = None if max_bytes_arg <= 0 else max_bytes_arg

    accepted, rejected = safety.validate_paths([raw])
    if rejected:
        return f"ERROR: {rejected[0]['reason']}"
    if not accepted:
        return "ERROR: no_valid_path"
    path = accepted[0]

    try:
        with open(path, "rb") as fp:
            if offset:
                fp.seek(offset)
            raw_bytes = fp.read() if max_bytes is None else fp.read(max_bytes)
        content = raw_bytes.decode("utf-8", errors="replace")
    except OSError as exc:
        return f"ERROR: read_failed: {exc}"

    header = f"=== {safety.to_rel_str(path)} ==="
    if offset or max_bytes is not None:
        total_size = path.stat().st_size
        end = offset + len(raw_bytes)
        truncated = "" if end >= total_size else f" (truncated; {total_size - end} more bytes — call again with offset={end})"
        header += f" [bytes {offset}-{end} / {total_size}]{truncated}"
    return f"{header}\n{content}"


def _tool_list_dir(args: dict) -> str:
    raw = args.get("path", "")
    abs_path, err = _resolve_dir_or_root(raw)
    if err:
        return f"ERROR: {err}"
    if not abs_path.exists():
        return "ERROR: not_found"
    if not abs_path.is_dir():
        return "ERROR: not_a_directory"

    entries: list[str] = []
    try:
        for item in sorted(abs_path.iterdir()):
            if len(entries) >= MAX_LIST_ENTRIES:
                entries.append(f"... (truncated at {MAX_LIST_ENTRIES} entries)")
                break
            suffix = "/" if item.is_dir() else ""
            entries.append(f"{item.name}{suffix}")
    except OSError as exc:
        return f"ERROR: list_failed: {exc}"

    rel_label = safety.to_rel_str(abs_path) or "."
    header = f"=== {rel_label}/ ==="
    body = "\n".join(entries) if entries else "(empty)"
    return f"{header}\n{body}"


def _tool_grep_files(args: dict) -> str:
    raw_pattern = args.get("pattern")
    pattern = str(raw_pattern or "").lower()
    if not pattern:
        return "ERROR: empty_pattern"
    raw_path = args.get("path", "")
    file_glob = str(args.get("file_glob") or "")

    root, err = _resolve_dir_or_root(raw_path)
    if err:
        return f"ERROR: {err}"
    if not root.exists() or not root.is_dir():
        return "ERROR: root_not_a_directory"

    matches: list[str] = []
    scanned = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not _is_blacklisted_walk_dir(d)]
        for fname in filenames:
            if file_glob and not fnmatch.fnmatch(fname, file_glob):
                continue
            fpath = Path(dirpath) / fname
            if not _is_text_file(fpath):
                continue
            ok, _reason, _size = safety.is_safe(str(fpath))
            if not ok:
                continue
            scanned += 1
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as fp:
                    for lineno, line in enumerate(fp, 1):
                        if pattern in line.lower():
                            snippet = line.rstrip()[:GREP_SNIPPET_CHARS]
                            matches.append(
                                f"{safety.to_rel_str(fpath)}:{lineno}: {snippet}"
                            )
                            if len(matches) >= MAX_GREP_MATCHES:
                                matches.append(
                                    f"... (truncated at {MAX_GREP_MATCHES} matches)"
                                )
                                return "\n".join(matches)
            except OSError:
                continue
    if not matches:
        return f"(no matches for '{raw_pattern}' in {scanned} files)"
    return "\n".join(matches)


# ---------------------------------------------------------------------------
# Write tools (gated by per-run allowlist)
# ---------------------------------------------------------------------------

def _tool_write_file(args: dict, *, allowlist: list[str]) -> str:
    raw = args.get("path", "")
    content = args.get("content", "")
    if not isinstance(content, str):
        return "ERROR: content_must_be_string"

    size_err = _check_write_size(content)
    if size_err:
        return f"ERROR: {size_err}"

    abs_path, err = _validate_write_path(raw, allowlist)
    if err:
        return f"ERROR: {err}"

    try:
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        abs_path.write_text(content, encoding="utf-8")
    except OSError as exc:
        return f"ERROR: write_failed: {exc}"

    return f"OK: wrote {len(content)} chars to {safety.to_rel_str(abs_path)}"


def _tool_append_file(args: dict, *, allowlist: list[str]) -> str:
    raw = args.get("path", "")
    content = args.get("content", "")
    if not isinstance(content, str):
        return "ERROR: content_must_be_string"

    size_err = _check_write_size(content)
    if size_err:
        return f"ERROR: {size_err}"

    abs_path, err = _validate_write_path(raw, allowlist)
    if err:
        return f"ERROR: {err}"

    try:
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        prefix = ""
        if abs_path.exists() and abs_path.stat().st_size > 0:
            # Ensure a newline separator when the existing file doesn't end in one.
            with open(abs_path, "rb") as fp:
                fp.seek(-1, os.SEEK_END)
                last = fp.read(1)
            if last not in (b"\n", b"\r"):
                prefix = "\n"
        with open(abs_path, "a", encoding="utf-8") as fp:
            fp.write(prefix + content)
    except OSError as exc:
        return f"ERROR: append_failed: {exc}"

    return f"OK: appended {len(content)} chars to {safety.to_rel_str(abs_path)}"


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------

_READ_TOOLS = {"read_file", "list_dir", "grep_files"}
_WRITE_TOOLS = {"write_file", "append_file"}


def is_read_only_tool(name: str) -> bool:
    return name in _READ_TOOLS


def execute_tool(name: str, args: dict, *, write_allowlist: list[str] | None = None) -> str:
    """Execute a tool call by name. Always returns a string (never raises).

    Errors are returned as 'ERROR: <reason>' so MiniMax sees them as tool_result
    content and can course-correct.

    write_allowlist: glob patterns (workspace-relative) allowed for write_file
    / append_file in this agent run. None/empty = writes disabled.
    """
    args = args or {}
    wl = write_allowlist or []
    try:
        if name == "read_file":
            return _tool_read_file(args)
        if name == "list_dir":
            return _tool_list_dir(args)
        if name == "grep_files":
            return _tool_grep_files(args)
        if name in _WRITE_TOOLS:
            if not wl:
                return "ERROR: write_disabled_for_this_run"
            if name == "write_file":
                return _tool_write_file(args, allowlist=wl)
            return _tool_append_file(args, allowlist=wl)
        return f"ERROR: unknown_tool: {name}"
    except Exception as exc:
        return f"ERROR: tool_crashed: {type(exc).__name__}: {exc}"
