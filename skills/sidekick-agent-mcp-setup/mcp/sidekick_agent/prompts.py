"""Prompt templates for sidekick tools.

All prompts are in English for model quality + portability. Sections are
rigid so the junior LLM cannot drift: role, task, focus, inputs, output
format, constraints.
"""
from __future__ import annotations

from pathlib import Path

BASE_SYSTEM = (
    "You are a junior assistant. Do not reason beyond the task scope. "
    "Do not guess. If the input is insufficient to complete the task, "
    "return exactly: \"INSUFFICIENT_INPUT: <one-line reason>\" and nothing else."
)

BASE_CONSTRAINTS = [
    "No opinion, no recommendation.",
    "No preamble (\"Here's...\", \"Sure,...\", \"Đây là...\").",
    "No postamble (\"Hope this helps...\", \"Let me know if...\").",
    "Preserve literally: proper nouns, numbers, acronyms, code snippets.",
    "Output language matches input language unless explicitly told otherwise.",
]


def _render_files(files: list[tuple[str, str]]) -> str:
    blocks = []
    for idx, (path, content) in enumerate(files, 1):
        blocks.append(f"=== File {idx}: {path} ===\n{content}")
    return "\n\n".join(blocks)


def _render_constraints(extra: list[str] | None = None) -> str:
    items = BASE_CONSTRAINTS + (extra or [])
    return "\n".join(f"- {c}" for c in items)


def build_summarize_prompt(
    files: list[tuple[str, str]],
    *,
    max_bullets: int,
    focus: str,
) -> str:
    focus_line = focus.strip() or "(no specific focus)"
    output_format = (
        f"Markdown bullet list with exactly {max_bullets} bullets. "
        "Each bullet is one line, no sub-bullets, no numbering."
    )
    extra_constraints = [
        "Do not invent facts not present in the source.",
        f"Exactly {max_bullets} bullets — not fewer, not more.",
    ]
    return (
        f"[TASK]\nSummarize the content below into {max_bullets} bullet points.\n\n"
        f"[FOCUS]\n{focus_line}\n\n"
        f"[INPUT FILES]\n{_render_files(files)}\n\n"
        f"[OUTPUT FORMAT]\n{output_format}\n\n"
        f"[CONSTRAINTS]\n{_render_constraints(extra_constraints)}"
    )


def build_translate_prompt(
    files: list[tuple[str, str]],
    *,
    target_language: str,
    tone: str,
) -> str:
    output_format = (
        "Plain translated text. Preserve original markdown structure exactly "
        "(headings, lists, tables, code blocks). No commentary."
    )
    extra_constraints = [
        f"Target language: {target_language}.",
        f"Tone: {tone}.",
        "Keep acronyms unchanged; on first occurrence only, add a brief "
        "parenthetical expansion if the target language lacks a common equivalent.",
        "Do not translate code, identifiers, file paths, or URLs.",
    ]
    return (
        f"[TASK]\nTranslate the content below to {target_language}.\n\n"
        f"[FOCUS]\n(no specific focus)\n\n"
        f"[INPUT FILES]\n{_render_files(files)}\n\n"
        f"[OUTPUT FORMAT]\n{output_format}\n\n"
        f"[CONSTRAINTS]\n{_render_constraints(extra_constraints)}"
    )


def build_task_prompt(
    files: list[tuple[str, str]],
    *,
    task: str,
    output_format: str,
    reader: str,
    constraints: list[str],
    safeguards: bool,
) -> str:
    """Generic task prompt. The task string describes what to do; output_format
    is picked to match the downstream reader.
    """
    if not task.strip():
        task_line = "(no task specified)"
    else:
        task_line = task.strip()

    # Resolve output format based on reader hint.
    # Note: no native JSON strict mode — caller must request JSON explicitly
    # via constraints and validate output themselves.
    fmt_map = {
        "auto": (
            "Compact plain text or minimal markdown optimized for machine reading. "
            "No extra formatting beyond what the task requires."
        ),
        "markdown": (
            "Well-structured markdown readable by a human. Use headings and lists "
            "where it aids scanning. No preamble."
        ),
        "plain": (
            "Plain text. No markdown, no formatting, no commentary."
        ),
    }
    reader_note = {
        "claude": " (Reader: another LLM — optimize for compactness.)",
        "human": " (Reader: human — optimize for readability.)",
        "": "",
    }.get(reader.lower(), "")
    chosen_fmt = fmt_map.get(output_format.lower(), fmt_map["auto"])
    output_block = chosen_fmt + reader_note

    extra = list(constraints or [])
    extra.append("Stay strictly within the task; do not add scope.")
    extra.append("Every claim in the output must be traceable to the source.")
    if safeguards:
        extra.append(
            "For any claim you are unsure about, mark inline with [ASSUMPTION: ...]."
        )
        extra.append(
            "For any missing piece the task needs but the source does not provide, "
            "mark inline with [TBD: ...]."
        )

    return (
        f"[TASK]\n{task_line}\n\n"
        f"[INPUT FILES]\n{_render_files(files)}\n\n"
        f"[OUTPUT FORMAT]\n{output_block}\n\n"
        f"[CONSTRAINTS]\n{_render_constraints(extra)}"
    )


def read_files(paths: list[Path]) -> list[tuple[str, str]]:
    """Read accepted paths into (relative_path_str, content) tuples.

    Uses workspace-relative paths in the prompt so the model never sees
    absolute paths or drive letters.
    """
    from . import config

    out: list[tuple[str, str]] = []
    for p in paths:
        try:
            rel = p.relative_to(config.WORKSPACE_ROOT)
            label = str(rel).replace("\\", "/")
        except ValueError:
            label = p.name
        try:
            content = p.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            content = f"[READ_ERROR: {exc}]"
        out.append((label, content))
    return out
