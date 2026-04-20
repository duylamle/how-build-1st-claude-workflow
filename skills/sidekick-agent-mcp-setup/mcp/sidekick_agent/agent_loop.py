"""Agent loop: let the LLM call read/write tools autonomously.

Callers invoke `run_agent(task, ...)`. The loop:
  1. Send task + tool schemas to the LLM
  2. If the LLM emits tool_use blocks → execute locally → append tool_result → repeat
  3. If the LLM stops with text → return text to caller
  4. Hit max_iterations or a repeated-failure circuit breaker → force stop

Read-only tool calls emitted in the same turn execute in parallel (small
threadpool). Writes run sequentially so two writes to the same path in one
turn don't race.
"""
from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from . import agent_tools, client, config


# Circuit breaker: if the same (tool_name, error_prefix) fires this many times
# in a row, stop the loop instead of burning iterations on the same mistake.
_SAME_ERROR_STOP_THRESHOLD = 3

# Parallel executor width for read-only tool batches. Small — we're bandwidth-
# bound on disk I/O, not CPU.
_PARALLEL_READ_WORKERS = 4

_TRACE_ARGS_LIMIT = 200
_TRACE_RESULT_LIMIT = 400


def _extract_tool_uses(raw_content: list[dict]) -> list[dict]:
    return [b for b in raw_content if b.get("type") == "tool_use"]


def _extract_text(raw_content: list[dict]) -> str:
    parts = [b.get("text", "") for b in raw_content if b.get("type") == "text"]
    return "\n".join(p for p in parts if p).strip()


def _truncate_for_log(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"... [truncated, total {len(text)} chars]"


def _error_prefix(output: str) -> str:
    # Agent tool errors are "ERROR: <reason>". Extract the reason token for
    # circuit-breaker comparison; non-error outputs yield empty prefix.
    if not output.startswith("ERROR:"):
        return ""
    reason = output[6:].strip()
    # Normalize the first token (everything before ':' or space), so
    # "blacklist:**/*.env" and "blacklist:**/*.key" both collapse to "blacklist".
    for sep in (":", " "):
        idx = reason.find(sep)
        if idx > 0:
            return reason[:idx]
    return reason


def _execute_tool_batch(
    tool_uses: list[dict],
    write_allowlist: list[str],
) -> list[tuple[dict, str]]:
    """Execute all tool_use blocks from a single turn.

    Read-only tools (read_file, list_dir, grep_files) run in parallel;
    writes run sequentially to keep deterministic ordering when the LLM
    emits multiple writes to overlapping paths in one turn.
    Returns list of (tool_use_dict, output_str) in the original order.
    """
    results: list[tuple[dict, str]] = [(tu, "") for tu in tool_uses]

    read_indices: list[int] = []
    write_indices: list[int] = []
    for i, tu in enumerate(tool_uses):
        if agent_tools.is_read_only_tool(tu.get("name", "")):
            read_indices.append(i)
        else:
            write_indices.append(i)

    def _run(idx: int) -> tuple[int, str]:
        tu = tool_uses[idx]
        return idx, agent_tools.execute_tool(
            tu.get("name", ""),
            tu.get("input") or {},
            write_allowlist=write_allowlist,
        )

    # Parallel reads
    if read_indices:
        with ThreadPoolExecutor(max_workers=_PARALLEL_READ_WORKERS) as ex:
            for idx, output in ex.map(_run, read_indices):
                results[idx] = (tool_uses[idx], output)

    # Sequential writes
    for idx in write_indices:
        _, output = _run(idx)
        results[idx] = (tool_uses[idx], output)

    return results


def run_agent(
    *,
    task: str,
    system_prompt: str,
    write_allowlist: list[str],
    max_iterations: int,
    max_tokens: int | None = None,
) -> dict[str, Any]:
    """Drive the agent loop until it stops or hits the iteration cap.

    Returns:
        {
          "text": final text from the LLM (may be empty if it only used tools),
          "iterations": number of LLM calls made,
          "trace": list of {iter, tool, args_preview, result_preview} entries,
          "usage": {prompt_tokens, completion_tokens} (summed across iterations),
          "duration_ms": total wall-clock time,
          "stop_reason": last stop_reason or synthetic "iteration_cap" /
                         "repeated_tool_failure",
          "error": optional error string if something went wrong mid-loop.
        }
    """
    tools = agent_tools.get_tool_schemas(
        include_write=bool(write_allowlist),
        allowlist_patterns=write_allowlist,
    )

    history: list[dict] = []
    user_prompt: str | None = task
    total_prompt_tokens = 0
    total_completion_tokens = 0
    trace: list[dict] = []
    started = time.time()
    last_stop_reason = ""
    error: str | None = None
    final_text = ""
    iteration = 0

    # Circuit-breaker state: track the last (tool, error_prefix) and its streak
    last_error_key: tuple[str, str] | None = None
    streak = 0
    broke_on_repeated_failure = False

    for iteration in range(1, max_iterations + 1):
        try:
            result = client.call_llm(
                system_prompt,
                user_prompt,
                thinking=config.THINKING,
                history=history,
                max_tokens=max_tokens,
                tools=tools,
            )
        except client.SidekickError as exc:
            error = f"llm_call_failed_at_iter_{iteration}: {exc}"
            break

        raw_content = result.get("raw_content") or []
        last_stop_reason = result.get("stop_reason") or ""
        usage = result.get("usage") or {}
        total_prompt_tokens += int(usage.get("prompt_tokens", 0) or 0)
        total_completion_tokens += int(usage.get("completion_tokens", 0) or 0)

        if user_prompt is not None:
            history.append({"role": "user", "content": user_prompt})
        history.append({"role": "assistant", "content": raw_content})
        user_prompt = None  # subsequent iterations continue via tool_result

        tool_uses = _extract_tool_uses(raw_content)

        if not tool_uses:
            # No tool calls — the LLM gave a final answer (or empty output).
            final_text = _extract_text(raw_content)
            break

        executed = _execute_tool_batch(tool_uses, write_allowlist)

        tool_result_blocks: list[dict] = []
        turn_error_keys: list[tuple[str, str]] = []
        for tu, output in executed:
            tool_name = tu.get("name", "")
            tool_result_blocks.append({
                "type": "tool_result",
                "tool_use_id": tu.get("id", ""),
                "content": output,
            })
            trace.append({
                "iter": iteration,
                "tool": tool_name,
                "args_preview": _truncate_for_log(str(tu.get("input") or {}), _TRACE_ARGS_LIMIT),
                "result_preview": _truncate_for_log(output, _TRACE_RESULT_LIMIT),
            })
            prefix = _error_prefix(output)
            if prefix:
                turn_error_keys.append((tool_name, prefix))

        # Update circuit-breaker streak. All tools in this turn must produce the
        # same error key for the streak to continue; any success resets it.
        if turn_error_keys and len(turn_error_keys) == len(executed):
            # Use the first error key as representative for the turn
            turn_key = turn_error_keys[0]
            if all(k == turn_key for k in turn_error_keys) and turn_key == last_error_key:
                streak += 1
            else:
                last_error_key = turn_key if all(k == turn_key for k in turn_error_keys) else None
                streak = 1 if last_error_key else 0
        else:
            last_error_key = None
            streak = 0

        if streak >= _SAME_ERROR_STOP_THRESHOLD:
            last_stop_reason = "repeated_tool_failure"
            broke_on_repeated_failure = True
            # Salvage any text the LLM produced in this turn alongside the failing calls
            final_text = _extract_text(raw_content)
            break

        history.append({"role": "user", "content": tool_result_blocks})

    else:
        last_stop_reason = "iteration_cap"
        if history and history[-1].get("role") == "assistant":
            final_text = _extract_text(history[-1].get("content") or [])

    return {
        "text": final_text,
        "iterations": iteration,
        "trace": trace,
        "usage": {
            "prompt_tokens": total_prompt_tokens,
            "completion_tokens": total_completion_tokens,
        },
        "duration_ms": int((time.time() - started) * 1000),
        "stop_reason": last_stop_reason,
        "error": error,
        "broke_on_repeated_failure": broke_on_repeated_failure,
    }
