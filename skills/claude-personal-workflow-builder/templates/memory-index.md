# Memory Index

> Accumulated lessons, feedback, and context that persist across sessions.
> Each entry is a separate file in `memory/`. This index points to active entries.

---

## Lifecycle

Memory follows a 4-step lifecycle:

### 1. SAVE — Capture during a session

When something goes wrong (or right) during a session, save it as a new file
in `memory/`. Each entry is one `.md` file with a clear title and one-line
description.

**When to save:**
- Claude made an error you had to correct (e.g., wrong format, missed constraint)
- You discovered a preference that should persist (e.g., "always use bullet points in PRDs")
- A project-specific context that future sessions will need (e.g., "API v2 is deprecated, use v3")
- A workflow pattern that worked well and should be repeated

**When NOT to save:**
- One-off corrections that won't recur
- Temporary context that expires after the current task
- Information already captured in rules or skills

### 2. READ — Scan before relevant tasks

At the start of tasks that touch a domain where you have recorded feedback,
scan this index for applicable lessons. Do NOT auto-load all memories every
session — only read what is relevant to the current task.

Example: Before writing a PRD, check if there are memories about PRD formatting
preferences or past mistakes in PRD writing.

### 3. APPLY — Use the lesson to improve output

When a memory is relevant, apply it directly. The goal is to avoid repeating
mistakes and to carry forward what works.

Example: Memory says "User prefers acceptance criteria with concrete numeric
examples" — so when writing AC, include specific numbers instead of vague
thresholds.

### 4. ARCHIVE — Graduate or retire

Once a lesson is fully integrated into a rule or skill file, move the memory
entry to `memory/_archive/`. This keeps the active index clean and focused.

---

## Entry Format

Each entry in the Active Entries section below follows this format:

```
- [Short title](filename.md) — One-line description of the lesson
```

**Guidelines for writing entries:**
- Title should be scannable — someone reading the index should know if the
  entry is relevant without opening the file
- Description is one sentence max — the detail lives in the linked file
- Group related entries if the list grows long (by domain, by agent, etc.)

---

## Graduating to Rules

If you notice the same feedback appearing 3 or more times across different
sessions, it is a pattern — not a one-off. Patterns should graduate from
memory entries into permanent rules (in `.claude/rules/`).

**Process:**
1. Identify the repeated pattern across memory entries
2. Write a rule that captures the pattern as a permanent constraint
3. Add the rule to `.claude/rules/` and register it in `.claude/rules/CLAUDE.md`
4. Archive the original memory entries to `memory/_archive/`

This keeps memory lean (for recent, evolving lessons) and rules stable (for
proven patterns).

---

## Active Entries

<!-- Add entries as they accumulate. Examples of what entries look like: -->

<!-- - [Use structured output for API calls](api-structured-output.md) — Claude should return JSON with schema, not free text, when calling external APIs -->
<!-- - [Prefer bullet AC over paragraph AC](bullet-ac-preference.md) — Acceptance criteria are easier to test when written as bullets, not paragraphs -->
<!-- - [Project X uses v3 API only](project-x-api-version.md) — All Project X integrations must use API v3; v2 is deprecated since Jan 2025 -->
<!-- - [Skip executive summary for internal docs](skip-exec-summary.md) — Internal team docs do not need executive summaries; they add overhead without value -->
