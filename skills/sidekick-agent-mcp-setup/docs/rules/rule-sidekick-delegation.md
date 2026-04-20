# Rule: Sidekick Delegation

> Generic rule for any senior LLM (e.g. Claude Sonnet) that has the
> `sidekick-agent` MCP server available. Philosophy:
> **sidekick is a controlled token-shift strategy** — move repetitive,
> narrow-scope work from the expensive senior to a cheaper junior LLM,
> keep the senior focused on judgment. Quality is preserved by two
> controls: clear scope given to the junior, and the senior verifying
> the junior's output before anything is persisted or forwarded.

Drop this file into the senior's rules directory (for Claude Code,
that's the project's `.claude/rules/` folder). Adjust paths and
workspace references to match your setup.

---

## What sidekick is

The `sidekick-agent` MCP server wraps a cheaper Anthropic-compatible
LLM as a bounded toolset:

- `sidekick_summarize` — compact long content into N bullets
- `sidekick_translate` — bulk translation preserving markdown
- `sidekick_task` — generic extract / transform / draft / classify
- `sidekick_agent_run` — bounded autonomous agent with file tools

See the paired skill doc for tool signatures, prompt patterns, and the
verify checklist.

---

## Philosophy — Controlled token shift

By default the senior (Claude) handles everything. Tokens burn fast,
budgets cap out, and meaningful judgment gets crowded out by mechanical
work (summarizing, translating, formatting, scanning).

Sidekick is a channel to **move repetitive, narrow-scope work to a
cheaper junior LLM** — not to outsource and relax, but to **shift
tokens to where they fit, so the senior can focus on work that
actually needs senior reasoning**.

Control happens in two places:

1. **Scope given to the junior** — the junior must know exactly what
   it's doing and what output shape is expected. Ambiguous prompts
   produce ambiguous output regardless of model.
2. **Senior verification** — every sidekick output is a draft. The
   senior checks encoding, facts, and shape before anything reaches
   a file or the user.

Skip either control and the junior becomes a liability, not a saving.

---

## Opportunities to shift (where the ROI is obvious)

When you see these patterns, ask "what part is narrow enough to shift?"
instead of "can sidekick do this?":

- **Summarize long content** (PRDs, meeting notes, research) —
  shift 10-50k tokens per call
- **Bulk translation** — shift proportional to input length
- **Extract fields into a fixed schema** — shift when input pattern
  repeats across many files
- **Draft v0 against an existing template** — senior refines instead
  of writing from scratch
- **Scan folder + grep + synthesize** (via `sidekick_agent_run`) —
  shift the "walk the files" phase, senior decides what the findings mean

Default stance for a new task: find the narrowest slice the junior can
own, and shift just that slice. Don't try to shift the whole task.

---

## Principles for framing a sidekick task

Five non-negotiables. Violating any of them converts token savings
into cleanup cost.

- **The junior must know exactly what it's doing.** The prompt states
  the action and the minimum context needed — no guessing.
- **Output expectations are explicit.** Format, length, structure,
  and a few-shot example when the shape is non-obvious.
- **One call does one action.** Summarize *or* translate *or*
  extract — not all three. Chain them in the senior if needed.
- **Input is sufficient, not excessive.** Pass only the files that
  matter. Don't dump the whole repo.
- **The senior owns verification.** Encoding, fact spot-check, shape
  match, and the final sign-off all happen in the senior. Never
  delegate verification to the junior.

---

## Hard-to-shift tasks — how to slice them

Some tasks look unshiftable at first. The issue is almost always that
the scope is too broad, not that the junior is incapable. Re-scope
before concluding sidekick "can't do it."

- **Production code / debugging** — extract the pure-function slice
  (explicit signature, no side effects, no hidden state) or the
  boilerplate-per-pattern slice. Keep complex logic and judgment
  calls in the senior.
- **Multi-step reasoning** — decompose into single-step tasks the
  senior orchestrates. Each sidekick call handles one closed action,
  the senior chains them.
- **Judgment calls / trade-offs** — the senior decides. Sidekick can
  still prepare inputs: listing options, extracting pros/cons,
  surfacing prior decisions — narrow, list-shaped work the junior
  handles well.

Rule of thumb: if you can't write a one-sentence description of what
you want sidekick to do, the scope isn't ready — not the junior.

---

## Verify before persist

Sidekick output is a draft. Before writing to a file or forwarding to
the user, the senior checks:

- Encoding correct (Unicode, Vietnamese diacritics, fullwidth characters…)
- No preamble ("Here's…", "Sure,…", "Đây là tóm tắt:")
- No postamble ("Hope this helps…", "Let me know if…")
- Spot-check 2-3 concrete facts against the source (numbers, names, dates)
- Output shape matches the request (bullet count, JSON schema, format hints)
- If the response is `INSUFFICIENT_INPUT:`, `REJECTED_PATHS:`, or
  `SIDEKICK_ERROR:` → relay verbatim to the user, don't fabricate a fallback

---

## Safety

Sidekick has its own workspace whitelist and blacklist (secret
patterns, `.git`, `node_modules`, and whatever the operator adds via
`SIDEKICK_EXTRA_BLACKLIST`). If the tool returns `REJECTED_PATHS:` —
don't attempt to bypass. Report to the user and stop.

Write tools (`write_file`, `append_file` inside `sidekick_agent_run`)
only activate when the caller passes a non-empty `write_allowlist`.
Blacklist still wins over allowlist.

---

## Multi-turn pattern (stateless by default)

`sidekick_agent_run` does not persist history between calls. For
multi-turn work, the senior compacts context from the previous result
(3-5 key facts) and injects that into the next `task` argument. This
keeps token cost flat instead of linear in turn count. See the skill
doc for the full pattern and example.

The three narrow tools (`sidekick_summarize`, `sidekick_translate`,
`sidekick_task`) do support a `conversation_id` param for automatic
history persistence, but the store is LRU-capped and cleared when the
MCP process restarts — treat it as convenience, not durable state.
