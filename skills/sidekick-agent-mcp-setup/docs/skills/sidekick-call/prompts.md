# Sidekick Prompts — How to call each tool

Generic examples. Replace paths with ones from your workspace.

## sidekick_summarize

### Basic

```
sidekick_summarize(
  file_paths=["path/to/some-doc.md"],
  max_bullets=5,
)
```

### With focus

```
sidekick_summarize(
  file_paths=["path/to/meeting-notes.md"],
  max_bullets=4,
  focus="decisions and action items only",
)
```

### Multiple files

```
sidekick_summarize(
  file_paths=[
    "path/to/interview-a.md",
    "path/to/interview-b.md",
  ],
  max_bullets=7,
  focus="shared pain points across interviews",
)
```

## sidekick_translate

### Basic

```
sidekick_translate(
  file_paths=["drafts/draft.md"],
  target_language="en",
  tone="neutral",
)
```

### Formal tone

```
sidekick_translate(
  file_paths=["drafts/executive-summary.md"],
  target_language="English",
  tone="formal, concise, leadership-facing",
)
```

## sidekick_task (generic)

### Extract → JSON

There is no native JSON strict mode on MiniMax. Spell the constraint in the
prompt and validate the result on the senior side.

```
sidekick_task(
  file_paths=["meeting-notes.md"],
  task="Extract all action items with owner and deadline. If owner or "
       "deadline is missing, use null. Return VALID JSON ONLY — a JSON "
       "array of objects with keys: action, owner, deadline. No markdown "
       "fences, no commentary, no trailing text.",
  output_format="auto",
  reader="claude",
  constraints=["Output must parse as valid JSON", "No markdown code fences"],
)
```

### Classify feedback

```
sidekick_task(
  file_paths=["user-feedback.md"],
  task="Classify each feedback item into one of: bug, feature-request, "
       "praise, question, spam. Return a markdown table with columns: id, "
       "text (truncated 60 chars), category.",
  output_format="markdown",
  reader="human",
)
```

### Draft commit message

```
sidekick_task(
  file_paths=["diff-output.txt"],
  task="Draft a conventional commit message for this diff. Subject line "
       "<= 72 chars, body explains the why in 2-3 sentences.",
  output_format="plain",
  reader="human",
  constraints=["English", "No emoji"],
)
```

### Q&A on a specific doc

```
sidekick_task(
  file_paths=["prd-v3.md"],
  task="Answer: What is the deadline for Phase 2? Who owns the auth "
       "module? What is the target user segment?",
  output_format="markdown",
  reader="human",
)
```

### Transform format

```
sidekick_task(
  file_paths=["data/raw-table.md"],
  task="Convert this markdown table to a JSON array. Keep column names as "
       "keys, lowercase, with underscores. Return VALID JSON ONLY, no "
       "markdown fences.",
  output_format="auto",
  reader="claude",
  constraints=["Output must parse as valid JSON"],
)
```

### Safeguards example

With `safeguards=True` (default), the junior marks uncertain / missing
pieces inline:

```
- Deadline: 2026-Q3
- Owner: [TBD: not specified in source]
- Budget: $50k [ASSUMPTION: based on similar feature X, not stated]
```

Senior sees `[TBD:]` / `[ASSUMPTION:]` and either relays to the user or
fills manually with real data.

## sidekick_agent_run

### Read-only scan

```
sidekick_agent_run(
  task="List every .md file in inworking/ and return a 2-sentence "
       "one-liner summary for each.",
  write_allowlist=[],  # read-only
  max_iterations=10,
)
```

### Scan + synthesize + write

```
sidekick_agent_run(
  task="Scan notes/ for the term 'auth refactor'. For every match, read "
       "the containing file and extract the decision (if any). Write a "
       "consolidated summary to notes/auth-refactor-digest.md with one "
       "section per source file.",
  write_allowlist=["notes/**"],
  max_iterations=15,
)
```

### Narrow write target

```
sidekick_agent_run(
  task="Read the three PRD files I'll reference and produce an executive "
       "summary at drafts/exec-summary.md. Files: drafts/prd-a.md, "
       "drafts/prd-b.md, drafts/prd-c.md.",
  write_allowlist=["drafts/exec-summary.md"],  # single-file allowlist
  max_iterations=8,
)
```

## Failure modes

- `INSUFFICIENT_INPUT: <reason>` — junior declared the input inadequate.
  Relay verbatim; don't fabricate.
- `REJECTED_PATHS:\n  - <path>: <reason>` — path failed safety checks.
  Don't try to bypass.
- `SIDEKICK_ERROR: <detail>` — upstream failure (timeout, 5xx, API error).
  Retry once or fall back to the senior doing it directly.
- `SIDEKICK_WARNING: hit iteration cap` — agent loop reached its turn
  limit. Output may be partial; review the trace to decide next step.
- `SIDEKICK_WARNING: stopped early because the same tool error repeated` —
  circuit breaker fired. Fix the underlying issue (wrong path, missing
  allowlist, bad pattern) and retry with a clearer task.

## Anti-patterns

- Calling "summarize" without `max_bullets` — junior drifts in length
- Calling sidekick for analysis, recommendations, judgment — out of scope
- Passing files > `SIDEKICK_FILE_SIZE_KB` (default 500KB) — reject `oversized`
- Passing > `SIDEKICK_MAX_FILES` (default 10) files per call — reject
  `too_many_files`
- Using `sidekick_agent_run` for a task where the senior already knows
  every file path — use `sidekick_task` instead (cheaper, no loop overhead)
