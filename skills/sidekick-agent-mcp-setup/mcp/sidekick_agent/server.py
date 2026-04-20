"""Sidekick-Agent MCP server.

Exposes file-aware junior-LLM tools over stdio transport. The calling client
(Claude Code, another MCP host, etc.) shifts tokens from the senior to the
junior on narrow, framed tasks, and verifies output before persisting.

Backend: Anthropic-compatible endpoint (POST /messages).

Run standalone:
    python -m sidekick_agent.server
Register with Claude Code:
    claude mcp add sidekick-agent -- python <path>/server.py
"""
from __future__ import annotations

import os
import sys
import threading
from collections import OrderedDict
from pathlib import Path

# Allow running as both `python server.py` and `python -m sidekick_agent.server`.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from sidekick_agent import agent_loop, audit, client, config, prompts, safety  # type: ignore
else:
    from . import agent_loop, audit, client, config, prompts, safety

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sidekick-agent")


# ---------------------------------------------------------------------------
# Conversation store (for 3 narrow tools with conversation_id)
#
# LRU-capped so a long-lived MCP session with many unique conversation_ids
# doesn't grow without bound. Per-conversation turn count is also capped;
# oldest user+assistant pairs are dropped when the cap is exceeded.
#
# A module-level lock guards mutations. FastMCP stdio tends to serialize
# requests but the guarantee isn't documented, so the lock is cheap insurance.
# ---------------------------------------------------------------------------

_conversations: "OrderedDict[str, list[dict]]" = OrderedDict()
_conversations_lock = threading.Lock()


def _conv_load(conversation_id: str) -> list[dict]:
    with _conversations_lock:
        history = _conversations.get(conversation_id)
        if history is None:
            return []
        _conversations.move_to_end(conversation_id)
        return list(history)


def _conv_append(conversation_id: str, user_prompt: str, assistant_content: list[dict]) -> None:
    with _conversations_lock:
        conv = _conversations.get(conversation_id)
        if conv is None:
            if len(_conversations) >= config.MAX_CONVERSATIONS:
                _conversations.popitem(last=False)
            conv = []
            _conversations[conversation_id] = conv
        conv.append({"role": "user", "content": user_prompt})
        conv.append({"role": "assistant", "content": assistant_content})
        max_messages = config.MAX_TURNS_PER_CONVERSATION * 2
        if len(conv) > max_messages:
            del conv[: len(conv) - max_messages]
        _conversations.move_to_end(conversation_id)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _format_rejections(rejected: list[dict]) -> str:
    if not rejected:
        return ""
    lines = ["REJECTED_PATHS:"]
    for r in rejected:
        lines.append(f"  - {r['path']}: {r['reason']}")
    return "\n".join(lines)


def _log_rejection(tool_name: str, reason: str, session_id: str, files: list[str] | None = None, rejected: list[dict] | None = None) -> str:
    """Log a rejection to audit and return the user-visible reply string.

    The return value starts with either `REJECTED_PATHS:` (when `rejected` is
    provided) or `REJECTED: <reason>` for simpler cases.
    """
    audit.log_call(
        tool=tool_name,
        files=files or [],
        input_chars=0, output_chars=0, duration_ms=0,
        prompt_tokens=0, completion_tokens=0,
        status="rejected",
        error=reason,
        rejected=rejected,
        session_id=session_id,
    )
    if rejected:
        return _format_rejections(rejected)
    return f"REJECTED: {reason}"


def _run_tool(
    tool_name: str,
    file_paths: list[str],
    build_prompt,
    prompt_kwargs: dict,
    *,
    session_id: str = "",
    conversation_id: str = "",
    max_tokens: int | None = None,
) -> str:
    if not file_paths:
        return _log_rejection(tool_name, "no_file_paths_provided", session_id)

    accepted, rejected = safety.validate_paths(file_paths)
    if not accepted:
        return _log_rejection(
            tool_name,
            _format_rejections(rejected) or "no_valid_inputs",
            session_id,
            files=file_paths,
            rejected=rejected,
        )

    file_blocks = prompts.read_files(accepted)
    input_chars = sum(len(c) for _, c in file_blocks)

    user_prompt = build_prompt(file_blocks, **prompt_kwargs)
    system_prompt = prompts.BASE_SYSTEM

    history: list[dict] | None = _conv_load(conversation_id) if conversation_id else None

    try:
        result = client.call_llm(
            system_prompt, user_prompt,
            thinking=config.THINKING,
            history=history,
            max_tokens=max_tokens,
        )
    except client.SidekickError as exc:
        audit.log_call(
            tool=tool_name,
            files=[str(p) for p in accepted],
            input_chars=input_chars,
            output_chars=0,
            duration_ms=0,
            prompt_tokens=0,
            completion_tokens=0,
            status="error",
            error=str(exc),
            rejected=rejected or None,
            session_id=session_id,
        )
        return f"SIDEKICK_ERROR: {exc}"

    text = result["text"]
    finish_reason = result.get("finish_reason", "")
    usage = result.get("usage") or {"prompt_tokens": 0, "completion_tokens": 0}
    raw_content = result.get("raw_content") or []

    if conversation_id and raw_content:
        _conv_append(conversation_id, user_prompt, raw_content)

    status = "ok"
    error: str | None = None
    return_text = text

    if not text:
        status = "empty"
        if finish_reason == "length":
            error = (
                f"empty_output: finish_reason=length, "
                f"completion_tokens={usage['completion_tokens']}. "
                f"Increase SIDEKICK_MAX_TOKENS (currently "
                f"{os.environ.get('SIDEKICK_MAX_TOKENS', str(config.MAX_TOKENS))})."
            )
        else:
            error = f"empty_output: finish_reason={finish_reason or 'unknown'}"
        return_text = f"SIDEKICK_ERROR: {error}"
    elif finish_reason == "length":
        status = "truncated"
        error = (
            f"output_truncated: finish_reason=length. "
            f"Output cut at {usage['completion_tokens']} tokens. "
            f"Bump SIDEKICK_MAX_TOKENS or split input."
        )
        return_text = f"{text}\n\n---\nSIDEKICK_WARNING: {error}"
    elif text.startswith("INSUFFICIENT_INPUT:"):
        status = "insufficient"
        error = text

    audit.log_call(
        tool=tool_name,
        files=[str(p) for p in accepted],
        input_chars=input_chars,
        output_chars=len(text),
        duration_ms=result["duration_ms"],
        prompt_tokens=usage["prompt_tokens"],
        completion_tokens=usage["completion_tokens"],
        status=status,
        error=error,
        rejected=rejected or None,
        session_id=session_id,
    )

    if rejected:
        return f"{return_text}\n\n---\n{_format_rejections(rejected)}"
    return return_text


# ---------------------------------------------------------------------------
# MCP tools
# ---------------------------------------------------------------------------

@mcp.tool()
def sidekick_summarize(
    file_paths: list[str],
    max_bullets: int = 5,
    focus: str = "",
    session_id: str = "",
    conversation_id: str = "",
    max_tokens: int = 0,
) -> str:
    """Summarize one or more files into a fixed number of bullets.

    Use for compacting long content (notes, PRDs, research) before the caller
    reviews. Output is a markdown bullet list with exactly max_bullets items.

    Args:
        file_paths: Workspace-relative or absolute paths. Must be inside
            SIDEKICK_WORKSPACE_ROOT and not match blacklist.
        max_bullets: Exact number of bullets to produce (1-20).
        focus: Optional hook to bias what to keep (e.g., "decisions only",
            "risks and blockers").
        session_id: Client session ID for audit log correlation.
        conversation_id: Optional stable string to continue the same
            conversation. The store remembers prior turns including thinking
            blocks. Leave empty for single-shot mode.
        max_tokens: Per-call output cap override. 0 = use env default
            (SIDEKICK_MAX_TOKENS). Summaries are short — 2000-4000 is usually
            plenty.
    """
    max_bullets = max(1, min(int(max_bullets), 20))
    return _run_tool(
        "sidekick_summarize",
        file_paths,
        prompts.build_summarize_prompt,
        {"max_bullets": max_bullets, "focus": focus},
        session_id=session_id,
        conversation_id=conversation_id,
        max_tokens=max_tokens or None,
    )


@mcp.tool()
def sidekick_translate(
    file_paths: list[str],
    target_language: str = "en",
    tone: str = "neutral",
    session_id: str = "",
    conversation_id: str = "",
    max_tokens: int = 0,
) -> str:
    """Translate file content into the target language, preserving markdown.

    Use for bulk translation where junior-level quality suffices before
    senior review. Keeps headings, lists, tables, code blocks intact.

    Args:
        file_paths: Workspace-relative or absolute paths. Inside workspace,
            not blacklisted.
        target_language: ISO code or plain name ("en", "vi", "English",
            "Tiếng Việt").
        tone: "neutral", "formal", "casual", or a short description.
        session_id: Client session ID for audit log correlation.
        conversation_id: Optional ID for multi-turn refinement. See
            sidekick_summarize docs.
        max_tokens: Per-call output cap override. 0 = use env default.
            Translation output length ≈ input length — bump for files
            > 20KB (e.g. 24000 or 32000).
    """
    return _run_tool(
        "sidekick_translate",
        file_paths,
        prompts.build_translate_prompt,
        {"target_language": target_language, "tone": tone},
        session_id=session_id,
        conversation_id=conversation_id,
        max_tokens=max_tokens or None,
    )


@mcp.tool()
def sidekick_task(
    file_paths: list[str],
    task: str,
    output_format: str = "auto",
    reader: str = "",
    constraints: list[str] | None = None,
    safeguards: bool = True,
    session_id: str = "",
    conversation_id: str = "",
    max_tokens: int = 0,
) -> str:
    """Generic sidekick tool: describe any narrow, framed task in natural language.

    Covers extract, transform, draft, classify, rewrite, outline, diff-summary,
    q&a, and similar narrow tasks. The caller (senior) frames the task; the
    junior executes within strict constraints and surfaces gaps.

    No native JSON strict mode. If you need JSON, add explicit constraints in
    `task` or `constraints` (e.g. "Return valid JSON, no markdown fences")
    and parse/validate on the caller side.

    Args:
        file_paths: Workspace-relative or absolute paths.
        task: Natural-language description of what to do. Be specific:
            "Extract action items with owner and deadline", not "extract stuff".
        output_format: "auto" (compact for another LLM), "markdown"
            (human-readable), or "plain" (no formatting). Hint only — shapes
            the prompt, no strict-mode enforcement.
        reader: "claude" hints compact output; "human" hints readable. Empty
            keeps the default for the chosen format.
        constraints: Extra task-specific constraints (e.g. ["Max 10 items",
            "English output", "Preserve code fences"]).
        safeguards: When True (default), the junior marks [ASSUMPTION: ...]
            and [TBD: ...] inline for uncertain or missing pieces.
        session_id: Client session ID for audit log correlation.
        conversation_id: Optional ID for multi-turn refinement.
        max_tokens: Per-call output cap override. 0 = use env default.
            Bump for long drafts (24000-32000).
    """
    if isinstance(constraints, str):
        constraints = [constraints]
    elif constraints is None:
        constraints = []
    else:
        constraints = [str(c) for c in constraints]

    if not task or not task.strip():
        return _log_rejection("sidekick_task", "empty_task_description", session_id, files=list(file_paths or []))

    return _run_tool(
        "sidekick_task",
        file_paths,
        prompts.build_task_prompt,
        {
            "task": task,
            "output_format": output_format,
            "reader": reader,
            "constraints": constraints,
            "safeguards": safeguards,
        },
        session_id=session_id,
        conversation_id=conversation_id,
        max_tokens=max_tokens or None,
    )


_AGENT_SYSTEM_PROMPT = (
    "You are a junior research assistant with read (and optionally write) "
    "access to a scoped workspace. Approach the task step by step: use "
    "list_dir and grep_files to discover relevant files, read_file to load "
    "content you actually need, and only call write_file / append_file when "
    "the task clearly asks you to persist output. Stop calling tools once "
    "you have enough to produce the final answer. Do not guess or invent "
    "facts; if the workspace lacks the information you need, say so "
    "explicitly in your final answer."
)


@mcp.tool()
def sidekick_agent_run(
    task: str,
    write_allowlist: list[str] | None = None,
    max_iterations: int = 0,
    max_tokens: int = 0,
    session_id: str = "",
) -> str:
    """Run the junior LLM as a bounded autonomous agent with file tools.

    The agent receives the task + a small tool set and loops:
      - read_file, list_dir, grep_files (always available, read-only)
      - write_file, append_file (only if write_allowlist is non-empty)

    The loop stops when the agent produces a final text answer, hits the
    iteration cap, repeatedly fails the same tool, or errors out. The caller
    sees only the final text plus a compact trace appended for review.

    Args:
        task: Natural-language task. Be specific.
        write_allowlist: Optional list of glob patterns (workspace-relative)
            the agent may write to during this run. None = use env default.
            Empty list = force read-only regardless of env. Example:
            ["inworking/**", "_logs/sidekick-out/**"]. Blacklist patterns
            (secrets, .git, etc.) still apply on top.
        max_iterations: Cap on LLM turns. 0 = use env default.
        max_tokens: Per-LLM-call output cap. 0 = use env default.
        session_id: Client session ID for audit log correlation.

    Returns:
        Final text from the agent, followed by a '--- TRACE' section listing
        every tool call. If the loop errored, returns 'SIDEKICK_ERROR: ...'.
    """
    if not task or not task.strip():
        return _log_rejection("sidekick_agent_run", "empty_task_description", session_id)

    if write_allowlist is None:
        effective_allowlist = list(config.WRITE_ALLOWLIST_PATTERNS)
    else:
        effective_allowlist = [p.strip() for p in write_allowlist if p and p.strip()]

    iter_cap = max_iterations if max_iterations and max_iterations > 0 else config.AGENT_MAX_ITERATIONS

    result = agent_loop.run_agent(
        task=task,
        system_prompt=_AGENT_SYSTEM_PROMPT,
        write_allowlist=effective_allowlist,
        max_iterations=iter_cap,
        max_tokens=(max_tokens or None),
    )

    text = result["text"] or ""
    trace = result["trace"]
    usage = result["usage"]
    stop_reason = result["stop_reason"]
    error = result["error"]

    parts: list[str] = []
    if text:
        parts.append(text)
    if trace:
        trace_lines = ["--- TRACE (tool calls)"]
        for entry in trace:
            trace_lines.append(
                f"[iter {entry['iter']}] {entry['tool']}({entry['args_preview']})"
                f"\n  -> {entry['result_preview']}"
            )
        parts.append("\n".join(trace_lines))
    if error:
        parts.append(f"SIDEKICK_ERROR: {error}")
    elif stop_reason == "iteration_cap":
        parts.append(
            f"SIDEKICK_WARNING: hit iteration cap ({iter_cap}). Agent did not "
            "reach a natural stop — result may be partial."
        )
    elif stop_reason == "repeated_tool_failure":
        parts.append(
            "SIDEKICK_WARNING: stopped early because the same tool error "
            "repeated 3+ turns. Check the trace and refine the task."
        )

    return_text = "\n\n".join(parts) if parts else "SIDEKICK_ERROR: empty_output"

    status = "ok"
    if error:
        status = "error"
    elif stop_reason in ("iteration_cap", "repeated_tool_failure"):
        status = "truncated"
    elif not text:
        status = "empty"

    audit.log_call(
        tool="sidekick_agent_run",
        files=[],
        input_chars=len(task),
        output_chars=len(return_text),
        duration_ms=result["duration_ms"],
        prompt_tokens=usage["prompt_tokens"],
        completion_tokens=usage["completion_tokens"],
        status=status,
        error=error,
        session_id=session_id,
    )

    return return_text


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
