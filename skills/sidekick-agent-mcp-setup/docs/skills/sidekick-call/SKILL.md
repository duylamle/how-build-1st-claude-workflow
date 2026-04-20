---
name: sidekick-call
description: >
  Shift tokens from the expensive senior (Claude) to a cheaper junior LLM
  in a controlled way — narrow scope framed by the senior, output verified
  by the senior before persist. Four tools on the sidekick-agent MCP:
  summarize (N bullets), translate (language), task (generic —
  extract/transform/draft/classify/q&a), agent_run (autonomous file
  exploration + optional writes). Use when the user asks to summarize,
  translate, extract, classify, draft, or scan files via sidekick — or
  more broadly when moving repetitive, narrow-scope work off the senior
  so the senior can focus on judgment. Trigger: "gọi sidekick", "delegate
  sidekick", "dùng đệ", "nhờ sidekick", "sidekick tóm tắt", "sidekick
  dịch", "sidekick làm", "shift sang sidekick", "sidekick_summarize",
  "sidekick_translate", "sidekick_task", "sidekick_agent_run", "use
  sidekick", "ask sidekick", "hand off to sidekick", "shift to junior
  LLM".
metadata:
  type: skill
  tools: [mcp__sidekick-agent__sidekick_summarize, mcp__sidekick-agent__sidekick_translate, mcp__sidekick-agent__sidekick_task, mcp__sidekick-agent__sidekick_agent_run]
---

# Skill: Sidekick Call

Using `sidekick-agent-mcp` from a senior LLM harness (Claude Code or
another MCP client). This skill covers **day-to-day usage** — calling
the four MCP tools, multi-turn patterns, and verifying output. For
**installing / configuring** the MCP, use the `sidekick-agent-mcp-setup` skill
instead.

Adjust example paths to match your workspace layout.

## Input

- `file_paths[]` — paths to process. Must resolve inside the workspace
  configured via `SIDEKICK_WORKSPACE_ROOT` and must not match the blacklist
  (`SIDEKICK_EXTRA_BLACKLIST` + built-in defaults)
- Per-tool params (below)

## Output

Plain text from the junior LLM. Senior verifies, then decides whether to
persist to a file or relay to the user.

## Tools

### `sidekick_summarize(file_paths, max_bullets=5, focus="", session_id="", conversation_id="", max_tokens=0)`
Narrow: compact files into exactly `max_bullets` bullets (1-20). Optional
`focus` biases what to keep.

### `sidekick_translate(file_paths, target_language="en", tone="neutral", session_id="", conversation_id="", max_tokens=0)`
Narrow: translate while preserving markdown structure. `target_language`
ISO code or plain name; `tone` short description.

### `sidekick_task(file_paths, task, output_format="auto", reader="", constraints=[], safeguards=True, session_id="", conversation_id="", max_tokens=0)`
Generic — covers extract, transform, draft, classify, rewrite, outline,
diff-summary, q&a. Use when the 2 narrow tools don't fit.

- `task`: natural-language, specific ("Extract action items with owner and
  deadline" not "extract stuff")
- `output_format`: `"auto"` (compact for another LLM), `"markdown"`
  (human-readable), `"plain"` (no formatting). **No native JSON strict
  mode** — for JSON, write the constraint in `task` or `constraints`
  (e.g. "Return valid JSON only, no markdown fences") and parse/validate
  on the senior side
- `reader`: `"claude"` = LLM reader (compact) | `"human"` = human reader
  (readable). Empty = default for chosen format
- `constraints`: task-specific list (e.g. `["Max 10 items",
  "English output"]`)
- `safeguards`: when True, junior marks `[ASSUMPTION: ...]` and
  `[TBD: ...]` inline for uncertain/missing pieces
- `session_id`: pass the senior's current session ID for log correlation
- `conversation_id`: stable string (e.g. `"sum-<slug>"`) enables multi-turn
  — sidekick remembers prior turns including thinking blocks. Empty =
  single-shot

### `sidekick_agent_run(task, write_allowlist=[], max_iterations=0, max_tokens=0, session_id="")`
Agentic — junior uses internal tools (`read_file`, `list_dir`, `grep_files`,
+ `write_file`/`append_file` if allowlist set) to explore the workspace and
complete the task autonomously. Senior receives final text + trace.

- `task`: specific description + (for multi-turn) compacted context from
  the previous turn
- `write_allowlist`: glob patterns the junior may write to. Empty =
  read-only. Blacklist always wins (secrets, `.git`, etc. are never
  writable, even if allowlisted)
- `max_iterations`: LLM-turn cap. 0 = env default (typically 15)
- `max_tokens`: output cap per LLM turn. 0 = env default

## Which tool when

| Situation | Tool |
|---|---|
| Condense content to N bullets | `sidekick_summarize` |
| Translate between two known languages | `sidekick_translate` |
| Extract/transform/draft/classify/q&a with known file paths | `sidekick_task` |
| Explore workspace (unknown file paths, scan folder, grep, read multiple) | `sidekick_agent_run` |

## Multi-turn pattern — senior compacts + re-sends (stateless)

The MCP does **not** persist history between `sidekick_agent_run` calls.
Each call is independent. To let the junior "remember" prior turns, the
senior compacts context and injects it into the next `task`.

**Why stateless:** tokens stay flat per turn instead of linear, the senior
controls what to carry, and the server doesn't lose state on restart.

### Compact pattern

After each `sidekick_agent_run`:
1. Senior reads the final text + trace
2. Extract 3-5 key facts to carry forward (file paths discovered, data
   found, decisions made)
3. Next turn: prepend a `[CONTEXT FROM PRIOR TURN]` block to `task`

### Example

```python
# Turn 1
r1 = sidekick_agent_run(
  task="Scan inworking/ and list TODO items with file path + line number",
  write_allowlist=["inworking/**"],
)
# r1 text: "Found 23 TODOs across 5 files: inworking/a.md:12, …"

# Senior compacts (does NOT resend r1 verbatim)
context = """
[CONTEXT FROM PRIOR TURN]
Turn 1 scanned inworking/ and found 23 TODOs across 5 files:
- inworking/a.md (8 TODOs, deployment theme)
- inworking/b.md (5 TODOs, testing theme)
- inworking/c.md (4 TODOs, docs theme)
- inworking/d.md (3 TODOs, mixed)
- inworking/e.md (3 TODOs, mixed)
Full files are re-readable by the junior on demand.
"""

# Turn 2
r2 = sidekick_agent_run(
  task=context + "\n\nTASK: Re-read inworking/a.md and inworking/d.md, "
       "pull the top 5 deployment-related TODOs, and write them to "
       "inworking/deploy-todo.md",
  write_allowlist=["inworking/**"],
)
```

Compaction rules:
- **Keep:** file paths discovered, facts/data extracted, decisions made,
  errors or constraints encountered
- **Drop:** verbose tool traces, full file content (the junior can re-read),
  thinking blocks, preambles
- **Length:** 3-10 lines is usually enough. Longer → split into a note
  file the junior can `read_file` on demand

### When multi-turn isn't needed

- Task is standalone; no prior context to inherit → single-shot
- Task is small enough for one `agent_run` → don't split turns
- Senior already has full context and only needs mechanical execution
  → use one of the 3 narrow tools

## Constraints

- Never call with a file outside the workspace — tool will reject
- Never call with a file matching the blacklist (secrets, keys, `.git`, etc.)
- One call = one action (summarize *or* translate *or* extract). For
  multi-step work, decompose into a chain of single-step calls and let
  the senior orchestrate between them
- Always run the verify checklist before persisting output
- Multi-turn `agent_run` → senior compacts + resends; never dump prior
  conversation verbatim into `task`

## Pointers

- Prompt examples per tool → `prompts.md`
- Senior verify checklist → `verify.md`
- Real use cases with token impact → `../../../examples/use-cases.md`
- Install / setup the MCP (first time, troubleshoot connection) →
  `../../../guide/setup-guide.md`
- Delegation philosophy (when to use vs not) → `../../rules/rule-sidekick-delegation.md`
- MCP source + provider config → `../../../README.md`
