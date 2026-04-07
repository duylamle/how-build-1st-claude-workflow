# 07 — Memory and Knowledge: Teaching AI to Remember

AI has no memory between sessions by default. Every conversation starts from zero. If you corrected AI behavior yesterday, it will make the same mistake today — unless you build systems to preserve lessons and context.

This guide covers two separate systems that serve different purposes and must not be mixed.

---

## Memory System: Accumulated Lessons

Memory stores what AI has learned about working WITH you. Corrections, preferences, patterns that failed, patterns that worked.

### Structure

```
memory/
  _INDEX.md                    <-- index of active entries
  fix-generic-summaries/
    FEEDBACK.md                <-- one lesson per folder
  use-prose-not-bullets/
    FEEDBACK.md
  _archive/                    <-- processed entries, no longer loaded
    old-feedback-1/
      FEEDBACK.md
```

Each entry is one folder containing one `FEEDBACK.md` file with simple frontmatter:

```yaml
---
name: fix-generic-summaries
description: AI summarizes with vague language instead of preserving specific data
type: feedback
---

## What happened
When summarizing meeting notes, AI replaced specific numbers ("revenue dropped 23%
in Q3") with generic language ("revenue decreased significantly").

## What to do instead
Preserve exact numbers, names, and dates from source material. Never round,
generalize, or paraphrase specific data points. If you must shorten, cut
context sentences — never cut data.
```

### Lifecycle

1. **Discover**: You correct AI behavior during a session ("do not summarize numbers, keep them exact")
2. **Save**: Create a memory entry capturing the lesson — what went wrong and what to do instead
3. **Apply**: In future sessions, AI reads relevant entries and applies the lesson without being reminded
4. **Archive**: When the lesson has been incorporated into a rule or skill (making the memory entry redundant), move it to `_archive/`

### Read on-demand, not auto-loaded

Memory entries are loaded when relevant, not dumped into every session. If you have 30 memory entries and today's task only relates to 2 of them, loading all 30 wastes context on irrelevant lessons.

The index file (`_INDEX.md`) lets AI scan what exists and load specific entries when the task matches.

> **Why This Matters:** Auto-loading all memory every session is a common mistake. It fills your context window with stale lessons while leaving less room for actual work. On-demand loading keeps context focused.

### Memory Decay

This is the maintenance problem nobody warns you about.

Feedback accumulates over time. After a few months, you have dozens of entries. Many are outdated — the behavior they corrected has been fixed in a rule. Some contradict each other because your preferences evolved. Others are so specific to one project they will never apply again.

If you do not prune, AI spends tokens reading irrelevant lessons and may apply outdated corrections to new work.

**Monthly review (15 minutes):**
1. Scan the index
2. Entries already baked into rules or skills? Move to `_archive/`
3. Entries about projects that are done? Archive
4. Entries that contradict current preferences? Delete or update
5. Keep only what is still actively relevant

> **Why This Matters:** A lean memory with 5-10 sharp entries beats a bloated memory with 50 stale ones. AI focuses on what actually matters when there is less noise to filter through. Schedule a monthly cleanup — treat it like clearing your desk.

---

## Knowledge Base: Static Domain Context

Knowledge stores facts about your domain — your company, teams, systems, projects. It is reference material AI reads when doing work, not instructions about how to behave.

### Structure

```
knowledge/
  company/
    teams/
      engineering.md            <-- who they are, what they own
      design.md
    systems/
      payment-gateway.md        <-- what it does, key constraints
      user-service.md
    stakeholders/
      sales-division.md
  projects/
    project-alpha/
      requirements.md
      design-v2.md
      2025-01-15-spec-v1.md     <-- output artifacts live here too
```

### Loaded on-demand

Knowledge is NOT loaded into every session. Agents and skills declare which knowledge paths they need, and the coordinator loads only those paths when spawning work.

For example, a skill writing a payment spec will load `knowledge/company/systems/payment-gateway.md` and `knowledge/company/teams/engineering.md`. A skill writing a marketing brief will load different paths entirely.

### Facts, not instructions

Knowledge files contain domain facts. They do NOT contain AI behavioral instructions — those belong in rules.

**Good knowledge file:**
```markdown
# Payment Gateway

- Provider: Stripe (primary), PayPal (secondary)
- Daily transaction volume: ~50,000
- Settlement: T+2 for Stripe, T+3 for PayPal
- PCI DSS Level 1 compliance required
- Rate limits: 100 requests/second per API key
```

**Bad knowledge file (mixing facts with instructions):**
```markdown
# Payment Gateway

When writing specs about payments, always mention PCI DSS compliance
and check with the security team before finalizing.
Provider: Stripe. Remember to use formal language when discussing payment flows.
```

The bad example mixes domain facts with behavioral instructions. Put behavioral instructions in rules or agent constraints.

> **Why This Matters:** AI works better with focused, relevant context than with everything dumped in. Loading your entire company wiki into context produces worse output than loading just the 2-3 files relevant to today's task.

---

## Feedback Capture Habit

This is the behavior that makes the entire memory system work. Without it, you have empty files and no accumulated intelligence.

**After every session where you corrected AI:**
1. What did AI do wrong?
2. What should it do instead?
3. Save as a memory entry

If you do not save it, you will correct the same thing next session. And the session after that. The correction takes 30 seconds. Repeating it costs minutes every time — compounding forever.

You do not need to capture everything. Prioritize:
- Errors that will definitely recur (formatting preferences, domain-specific rules)
- Corrections that took significant effort to explain
- Patterns, not one-off mistakes

Skip:
- Task-specific corrections that will not apply again
- Obvious errors AI self-corrected after one reminder
- Preferences you are still figuring out

---

## The Separation (Do Not Mix These)

| System | Contains | Example | Lives in |
|---|---|---|---|
| **Memory** | What AI learned about working with you | "Preserve exact numbers, never round" | `memory/` |
| **Knowledge** | Facts about your domain | "Payment gateway: Stripe, 50K txn/day" | `knowledge/` |
| **Rules** | How AI should behave | "Always use natural prose, not flowcharts" | `.claude/rules/` |

When you mix them, everything degrades:
- Domain facts in rules = rules bloat with content that changes often
- Behavioral instructions in knowledge = AI reads facts expecting instructions, gets confused
- Lessons in knowledge = lessons are not reviewed/archived, they rot

Keep each system clean. When in doubt: "Is this about AI behavior (rule), about my domain (knowledge), or about a specific correction (memory)?"

---

## Key Principles

- **Memory is on-demand, not auto-loaded**: load relevant entries, not all entries
- **Knowledge is facts, not instructions**: domain context separate from behavioral rules
- **Capture feedback immediately**: 30 seconds now saves minutes every future session
- **Prune monthly**: memory that is not maintained becomes noise. Archive what is stale
- **Separation is structural**: memory, knowledge, and rules serve different purposes at different timescales. Mixing them degrades all three
