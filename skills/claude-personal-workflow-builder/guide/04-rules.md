# Phase 4 — Rules

Rules are the behavioral guardrails of your system. They shape HOW AI behaves across every output — not WHAT to do for a specific task (that's what skills are for).

---

## Rules vs Skills vs Agent Instructions

| Layer | Purpose | Example |
|---|---|---|
| **Rule** | Behavioral constraint across ALL outputs | "Use probabilistic language — say 'likely' not 'certainly'" |
| **Skill** | Structured procedure for ONE type of work | "When writing a PRD, follow this template with these sections" |
| **Agent instruction** | Role-specific behavior for ONE agent | "You are a reviewer. Find weaknesses, don't praise." |

Rules apply to everything. Skills apply to specific tasks. Agent instructions apply to specific roles. Don't mix them — a rule about PRD format belongs in a skill, not a rule file.

---

## Always-Load vs On-Demand

**Always-load rules** are read automatically every session. They must be universally relevant — if a rule applies to less than 80% of sessions, it doesn't belong here.

**On-demand rules** live in a subfolder (`.claude/rules/on-demand/`) and are read only when the task requires them. Example: "rule-writing.md" is only relevant when producing a document, not when AI is searching files or updating memory.

### The Overhead Budget

Here's the critical constraint: **cap your always-load content at ~900 lines total** (all always-load rule files + root CLAUDE.md combined).

Why? Every line of always-load content is read at the start of every session. If your rules grow to 2000 lines, AI spends significant context reading meta-instructions instead of doing actual work. The system grows in capability, but context cost should not grow proportionally.

When you hit the cap: either make an existing rule more concise, or move it to on-demand.

> **Why this matters:** This budget constraint is the difference between a system that stays fast and one that gradually slows down as you add features. Without it, the natural tendency is to add more rules, more detail, more edge cases — until AI spends 30% of its context just reading instructions. One production system hit 1500 lines of always-load rules before discovering this problem. After trimming to 900, response quality improved noticeably because AI had more context for the actual task.

---

## Rule 1: Communication

Create `.claude/rules/rule-communication.md`:

```markdown
# Rule: Communication

## Tone
- Direct and concise — get to the point, no filler
- Use probabilistic language when uncertain: "likely", "probably",
  "needs confirmation" — NEVER "certainly", "definitely", "must be"
- Professional but not robotic

## When to Ask
- If a request can be interpreted multiple ways → ask BEFORE producing
- Maximum 3 questions per turn — prioritize the question that unlocks the most
- Number your questions for easy reference

## MECE Thinking
When analyzing problems or listing options:
- Mutually Exclusive: no overlap between categories
- Collectively Exhaustive: nothing important missing
- If not MECE → state where the overlap or gap is

## Objectivity
- Comparisons → always state criteria explicitly, not "X is better" generically
- Recommendations → state reasoning + trade-offs, don't advocate one side
- When data is insufficient → say so directly, don't guess
```

### What This Gives You

- AI won't produce overconfident statements ("this will definitely work")
- AI asks clarifying questions BEFORE wasting effort on wrong interpretation
- AI structures analysis cleanly (MECE) so you can evaluate options properly
- AI stays objective rather than telling you what you want to hear

---

## Rule 2: Workflow

Create `.claude/rules/rule-workflow.md`:

```markdown
# Rule: Workflow & File Management

## File Locations
| Content | Save to |
|---|---|
| Agents, skills, rules | `.claude/` |
| Working artifacts (docs, specs) | `knowledge/` or directory you specify |
| Feedback and lessons | `memory/` — one entry per file |
| Ideas, drafts | `inworking/` |

## Naming Conventions
- ALLCAPS.md = system role files (CLAUDE.md, AGENT.md, SKILL.md)
- kebab-case = everything else
- Output: YYYY-MM-DD-name.md, versioned v1/v2/v3
- Old files: keep them, don't delete mid-session

## Single Source of Truth
Each piece of information lives in exactly one file.
Other files point to it, never copy it.
- Agent list → `.claude/agents/CLAUDE.md`
- Rule list → `.claude/rules/CLAUDE.md`

## Ask Before Destructive Actions
- Bulk file changes (rename, restructure, delete)
- Publishing to external systems
- Any action that's hard to undo
→ Present plan first, wait for confirmation.

## Output Convention
- Save to the directory specified for the task
- Version: v1, v2, v3 after each revision
- Keep previous versions, don't overwrite
```

### What This Gives You

- Files always end up in the right place
- Consistent naming you can grep and glob
- No accidental deletions or overwrites
- Single source of truth prevents information drift

---

## Rule 3: Coordination

Create `.claude/rules/rule-coordination.md`:

```markdown
# Rule: Coordination

## Think-First
Before producing any artifact, analyze the request first:
- What's the scope? What's included and excluded?
- What assumptions am I making? Are they valid?
- What information is missing?
- What approach makes sense?

Skip think-first when: you call a specific skill directly, it's a
continuation of current work ("fix section 3"), or the task is a
simple system operation (file search, memory update).

## Depth Detection
| Signal | Depth |
|---|---|
| Single feature, one team, one sprint | Simple — produce directly |
| Multi-team, strategy, multi-quarter | Complex — full think + plan |
| Unclear | Ask before proceeding |

## Framed Tasks for Subagents
When spawning a subagent, write a complete brief:
1. Background — why this task exists (2-3 sentences)
2. Skill + mode — which skill to run
3. Input — file paths to read (don't dump content, point to files)
4. Confirmed decisions — what's already decided, don't re-ask
5. Output — where to save, what format

Subagent starts with a blank slate. No conversation history.
Brief it like onboarding a new colleague who just walked into the room.

## Checkpoints
Stop for review:
- After artifact v1 is complete
- Before publishing to external systems (Jira, Confluence, etc.)

Don't stop for:
- Intermediate thinking
- Internal handoffs between steps

## Main Context Can Produce Directly
Spawn subagent when: task has clear scope + needs deep expertise.
Produce directly when: task needs fast iteration or scope is obvious.
Subagents are helpers, not mandatory gates.
```

### What This Gives You

- AI thinks before acting — no wasted effort on wrong framing
- Subagents get full context instead of cryptic one-liners
- You review at the right moments, not too early or too late
- Simple tasks stay simple, complex tasks get proper treatment

---

## The "Read Before Execute" Pattern

This deserves special emphasis because it solves a persistent problem: AI "remembering" conventions incorrectly and producing output that violates its own rules.

Add this to your coordination rule or as a separate small rule:

```markdown
## Read Before Execute
Don't trust "I remember." Before producing any output:
1. Re-read the relevant skill (SKILL.md + template)
2. Re-read relevant rules if producing an artifact
3. Check memory for past feedback on this type of task

Reading conventions takes seconds. Fixing violations takes minutes
and erodes trust.
```

> **Why this matters:** This single pattern eliminated about 40% of output errors in production use. AI is confident it "knows" the convention — and it's often wrong about details like file naming, template structure, or constraint nuances. Forcing a re-read before every production step costs almost nothing and catches errors before they happen.

---

## Always-Load vs On-Demand Decision

Use this filter for every rule you write:

**Always-load if:**
- Applies to >80% of sessions
- Violation would cause immediate problems
- Examples: communication tone, file management, coordination behavior

**On-demand if:**
- Applies only to specific task types
- Can be loaded when that task starts
- Examples: writing style guide (only when producing documents), publishing checklist (only when pushing to external systems), Python script conventions (only when running scripts)

Store on-demand rules in `.claude/rules/on-demand/` and reference them in your rules CLAUDE.md:

```markdown
## On-demand (read when relevant)
| Rule | Read when |
|---|---|
| rule-writing.md | Producing artifacts (PRD, spec, brief) |
| rule-publishing.md | Publishing to Jira, Confluence |
```

---

## Verify Your Rules

Run Claude Code and test:

1. Ask an ambiguous question — does AI ask for clarification instead of guessing?
2. Ask it to create a file — does it use the right naming convention and location?
3. Ask it to write a short analysis — does it use probabilistic language and structure analysis with MECE?

If yes to all three, your rules are working.

---

## Line Count Check

Count your always-load content:

```bash
wc -l CLAUDE.md .claude/rules/rule-communication.md .claude/rules/rule-workflow.md .claude/rules/rule-coordination.md
```

If the total exceeds 900 lines, trim. You're early in the build — staying well under budget leaves room for growth.

---

## Next Step

Move to Phase 5 (agents) and Phase 6 (skills) to create your producer, reviewer, and core procedures. Those guides are coming next in this skill.
