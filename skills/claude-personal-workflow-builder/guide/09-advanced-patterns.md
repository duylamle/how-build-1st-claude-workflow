# Phase 9 — Advanced Patterns

Once your system is running, these patterns will help you get significantly more out of it. Each one comes from real operational experience — not theory.

---

## English-First Workflow (for Non-English Speakers)

LLM reasoning and writing quality is measurably better in English. If you work in another language, this creates an opportunity: separate the **content layer** (English) from the **presentation layer** (your language).

**The pattern:**

- **Main artifacts** (PRD, spec, report, brief, handoff) — have AI produce in English first, then translate to your language when sharing with stakeholders
- **Internal ops** (meeting notes, todos, chat, memory entries) — write directly in your language. No translation needed for things only you see

**Why this works:** English production gives you higher-quality reasoning, better structure, and more precise language. Translation is a mechanical step that preserves the quality while making it accessible.

**Implementation:**

```
1. Agent produces artifact in English
2. Coordinator translates to your language
3. Coordinator reads the translated file back and verifies:
   - Accents/diacritics display correctly
   - Technical meaning preserved
   - No context lost in translation
4. If encoding issues → rewrite immediately
```

> **Why This Matters:** The quality difference between English-first and direct non-English production is noticeable — especially for complex documents with multi-step reasoning. You get the best of both worlds: AI thinks in its strongest language, you read in yours.

---

## Framed Task Prompt — Deep Dive

When you spawn an agent, that agent starts with a blank slate. It has no conversation history, no idea what you decided, no context about why this task matters. Your prompt must compensate for all of that.

### The 5-Section Structure

1. **Background** — why this task exists (2-3 sentences). What problem, for whom, what deadline. What the coordinator already did or ruled out.
2. **Skill + Mode** — which skill to run, which mode. Path to SKILL.md so the agent reads the flow and constraints.
3. **Input** — what to read. File paths preferred over dumping content. Only dump text when it doesn't exist in any file (e.g., a decision confirmed in chat).
4. **Decisions Already Confirmed** — short list of what the user already decided. The agent must not question these or suggest alternatives.
5. **Output** — where to write, what format. Always include template path so the agent doesn't improvise structure.

### Before and After

**BAD prompt (terse):**
```
Review this PRD and tell me what's wrong.
```

What happens: the agent doesn't know who the PRD is for, what matters most, what was already debated, or where to write findings. It produces a generic review that misses the real issues.

**GOOD prompt (full context):**
```
Background: We're building a file upload feature for internal users.
The PRD went through 2 rounds of feedback from the dev lead — main
concerns were error handling and file size limits. User confirmed
max 20 files per upload, 5MB each.

Skill: challenge (mode: standard)
Read SKILL.md at .claude/skills/challenge/SKILL.md

Input: Read the PRD at knowledge/projects/upload/2026-03-15-prd-v2.md

Decisions already confirmed:
- Scope: drag-and-drop only, no folder upload
- Max 20 files, 5MB each, 100MB total per upload
- FE validates first, BE validates again on upload

Output: Write challenge report to
knowledge/projects/upload/2026-03-15-challenge-report-v1.md
Use template at .claude/skills/challenge/report/TEMPLATE.md

Focus areas: error handling completeness, edge cases around
concurrent uploads, and whether acceptance criteria are testable.
```

> **Why This Matters:** The cost of a detailed prompt is 1 minute. The cost of a generic output is 10 minutes of rework. Every minute invested in prompt quality saves multiples in output quality.

### Prompt Tiers

Not every task needs a full 5-section prompt:

- **Lite** (low/medium effort skills): Background 1-2 sentences + skill/mode + input paths + output path. Three elements: context, input, output.
- **Full** (high effort skills): All 5 sections + reasoning instructions if the output is complex.

When in doubt, use Full. It's safer to over-brief than under-brief.

---

## Parallel vs Sequential Agent Spawning

**Default: sequential.** Agent B needs agent A's output. Think produces analysis → PRD skill uses that analysis. Challenge reviews the PRD → fix skill uses the challenge findings.

**Only parallel when outputs are completely independent.** Both agents must produce something that doesn't depend on the other's work.

Valid parallel examples:
- QA review + task management updates at session end
- Two independent research tasks for different topics

Invalid parallel (must be sequential):
- Think → PRD (PRD needs think output)
- Produce → Challenge (challenge needs the produced artifact)
- Challenge → Fix (fix needs challenge findings)

**Rule of thumb:** if agent B would read agent A's output file, they must run sequentially.

---

## Multi-Step Handoff

When passing output from agent A to agent B:

1. **Summarize** agent A's output in 200 tokens or less — key findings, decisions, flags
2. **Provide the file path** so agent B can read the full artifact if needed
3. **Don't dump raw work** between agents — agent B doesn't need agent A's reasoning process, just the conclusions

**Example handoff in a prompt:**

```
Previous step: Think skill analyzed the upload feature requirement.
Key findings: scope is bounded (1 feature, 1 sprint), main risks
are error handling edge cases and concurrent upload behavior.
2 alternatives considered — chose progressive upload over batch
because it gives better UX feedback. Full analysis available at:
knowledge/projects/upload/2026-03-15-think-output.md

Your task: Write the PRD based on this analysis...
```

> **Why This Matters:** Dumping raw work between agents wastes context tokens and forces agent B to parse through irrelevant details. A clean summary + file path gives agent B exactly what it needs to start working.

---

## Sticky Session

If the user sends a follow-up request that's in the **same scope** and **same task type**, keep the same agent — no re-planning needed.

**Stay in session:**
- "Fix section 3" (after writing a doc)
- "Add an edge case for empty files" (after writing PRD)
- "Make the tone more direct" (after producing content)

**Re-plan needed:**
- "Now challenge this PRD" (task type changed: produce → review)
- "Write a Jira story for this" (task type changed: produce → execute)
- "Start working on a different feature" (scope changed)

This avoids the overhead of re-analyzing intent and re-spawning agents for simple iterations.

---

## Checkpoint Control

Pause for user review at exactly two points:

1. **After artifact v1 is complete** — user needs to review before further work
2. **Before publishing to any external system** — Jira, Confluence, GitHub, Slack, etc.

**Don't pause for:**
- Intermediate thinking between steps
- Internal handoffs between agents
- Research or discovery outputs that feed into the next step

Over-checkpointing slows down the flow. Under-checkpointing risks publishing something the user hasn't seen.

---

## Depth Detection

Before planning any task, determine its depth — this affects how much thinking and how many agents to involve.

| Signal | Depth | What It Means |
|---|---|---|
| 1 feature, 1 team, 1-3 sprints | **Standard** | Bounded scope. Think focuses on facts + risks. Fewer agents needed. |
| Vision, strategy, C-level audience, cross-team, multi-quarter | **Strategic** | Unbounded scope. Think focuses on framing + alternatives. More agents, deeper analysis. |
| Not clear from the request | **Ask the user** | Don't guess. A quick question saves significant rework. |

**Depth doesn't change mid-task.** If you start Standard and discover the task is actually Strategic (cross-team dependencies, multi-quarter timeline), flag it to the user rather than silently switching.

Standard tasks might involve: think → produce → challenge → fix.
Strategic tasks might involve: think → discovery → strategy → produce → challenge → fix → execute.

> **Why This Matters:** Applying Strategic depth to a simple bug fix wastes time. Applying Standard depth to a company-wide initiative misses critical analysis. Getting depth right is the single biggest leverage point in planning.
