# Phase 11 — Tuning Your System

Your system will NOT be perfect from day one. The best systems are continuously refined through real usage. This phase teaches you how to systematically improve your system when things go wrong.

---

## The Tuning Mindset

Every time AI produces output that isn't right, you have a choice: fix it once and move on, or fix it permanently so it never happens again. The tuning mindset means asking: **"How do I make this correction stick?"**

The answer depends on how severe the issue is and how often it repeats. That's where the escalation ladder comes in.

---

## The Escalation Ladder

When output isn't right, escalate through increasing levels of "hardness." Start soft. Go harder only when the softer level isn't enough.

### Level 1: Feedback (Softest)

**What:** Save a memory entry describing what went wrong and what you wanted instead.

**When to use:** First-time issue. Not sure if it will repeat. You want AI to know about it next session without creating a permanent rule.

**How:**
```markdown
# memory/tone-too-formal/FEEDBACK.md
---
name: tone-too-formal
description: AI used overly formal language in internal meeting notes
type: feedback
---

Meeting notes should be conversational, not formal.
Use "we decided" not "it was determined that".
```

**Hardness:** Low. AI reads memory on-demand — it might miss it if the task doesn't seem related.

### Level 2: Rule (Medium)

**What:** Write a rule file that AI loads every session (always-load) or when relevant (on-demand).

**When to use:** The same issue happened 3+ times across different sessions. Feedback alone isn't preventing it.

**How:**
```markdown
# .claude/rules/rule-tone.md
## Meeting notes tone
- Use conversational language: "we decided", "the team agreed"
- Never use passive voice in meeting notes
- Names as-is from the meeting, no "the stakeholder" generalization
```

Register it in `.claude/rules/CLAUDE.md` under always-load or on-demand.

**Hardness:** Medium. AI reads rules consistently, but might still miss edge cases.

### Level 3: Checklist (Medium-High)

**What:** Create a `checklist.md` file for a specific skill. AI runs through it before delivering output.

**When to use:** A specific skill keeps missing specific steps — not a general problem, but a targeted one.

**How:**
```markdown
# .claude/skills/meeting-notes/checklist.md
Before delivering meeting notes, verify:
- [ ] All attendee names spelled correctly
- [ ] Action items have owner + deadline
- [ ] Decisions listed separately from discussion
- [ ] No passive voice
- [ ] Tone is conversational
```

Reference it in the skill's SKILL.md so the agent knows to check it.

**Hardness:** Medium-high. Targeted to one skill, hard to miss if the skill references it.

### Level 4: Validator (Hard)

**What:** Write a Python script that runs as a hook — automatically checking output before or after AI writes a file.

**When to use:** A rule is critical AND AI keeps forgetting it. You need enforcement, not guidelines.

**How:**
```python
# .claude/scripts/validators/check-frontmatter.py
"""Validates that every artifact has required YAML frontmatter."""
import sys, yaml

def validate(filepath):
    with open(filepath) as f:
        content = f.read()
    if not content.startswith('---'):
        print(f"ERROR: {filepath} missing YAML frontmatter")
        sys.exit(1)
    # ... parse and validate required fields

validate(sys.argv[1])
```

Register in `settings.local.json` as a post-write hook.

**Hardness:** High. Code runs automatically — impossible to forget. But requires writing and maintaining a script.

### Level 5: Template + Example (Hardest)

**What:** Update the output template and add approved `EXAMPLE-*.md` files that show exactly what good output looks like.

**When to use:** Output format or style is consistently wrong despite rules and checklists. AI needs to see what "right" looks like, not just read about it.

**How:**
```
.claude/skills/meeting-notes/
  notes/
    TEMPLATE.md       ← updated with better structure
    EXAMPLE-01.md     ← real meeting notes you approved
    EXAMPLE-02.md     ← another approved example, different meeting type
```

AI reads examples to learn style and structure. Examples are more powerful than instructions for format/style issues.

**Hardness:** Highest. Templates constrain structure, examples constrain style. Together they leave very little room for AI to deviate.

> **Why This Matters:** Each level is "harder" than the previous — feedback is soft (AI might not read it), validators are hard (code blocks the action). Starting soft is cheaper and faster. Escalating when needed ensures persistent issues get permanently fixed. Don't over-engineer tuning for issues that happen once.

---

## The Feedback-to-Rule Pipeline

Many rules start as feedback entries. Here's how to recognize when it's time to graduate:

| Signal | Action |
|---|---|
| Same feedback appears 1-2 times | Keep as feedback. Monitor. |
| Same feedback appears 3+ times | Graduate to a rule. Archive the feedback. |
| Rule exists but AI still violates | Add a checklist or validator. |
| Checklist exists but output format is still wrong | Add template + examples. |

When you graduate feedback to a rule:
1. Write the rule file
2. Register it in `.claude/rules/CLAUDE.md`
3. Move the original feedback to `memory/_archive/`
4. The feedback served its purpose — it identified a pattern worth codifying

---

## Monthly Maintenance Ritual

Set aside 15-30 minutes monthly to keep your system lean and effective.

### Review Memory

- Open `memory/_INDEX.md`
- For each active entry: is this still relevant?
  - Already baked into a rule or skill? → Move to `_archive/`
  - Still happening? → Keep, or escalate to rule
  - Outdated (project ended, process changed)? → Archive
- Goal: keep active memory entries under 10-15

### Review Rules

- Read through each always-load rule
- Any rule that never triggers in practice? → Remove it or move to on-demand
- Any rule frequently violated? → Needs a validator or checklist
- Any rule that contradicts another? → Merge or clarify
- Check total line count: still under your budget (e.g., 900 lines)?

### Review Skills

- For each skill used in the past month:
  - Output consistently good? → No action needed
  - Output consistently bad in a specific way? → Add checklist, update template, or add examples
  - Skill never used? → Consider removing it
- For templates: do they still match what good output looks like?

### Check Overhead Budget

Count total lines of always-load rules + root CLAUDE.md. If over budget:
- Move less-critical rules to on-demand
- Trim verbose sections
- Merge related rules

The budget exists because AI quality degrades when it has to process too many instructions before doing real work. Lean instructions = better output.

> **Why This Matters:** Systems that aren't maintained decay. Memory fills with outdated entries, rules accumulate without pruning, skills drift from actual needs. Monthly maintenance takes 15-30 minutes and prevents the slow degradation that makes people abandon their systems.
