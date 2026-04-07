# 06 — Skills: Bounded Capabilities with Clear Input/Output

Skills are structured procedures for specific task types. Each skill defines: what input it needs, what output it produces, and what constraints it follows. Without skills, your agents improvise every time — producing inconsistent results. With skills, you get repeatable quality.

Think of skills as recipes. The agent is the chef (persona, judgment), the skill is the recipe (ingredients, steps, plating). Same chef, different recipe = different dish with consistent quality.

---

## SKILL.md Anatomy

Every skill lives in its own folder with a `SKILL.md` file as the entry point. Like agents, it has YAML frontmatter and a body.

### Frontmatter

```yaml
---
name: write-spec
description: >
  Write a feature specification with user stories, acceptance criteria,
  and business rules. Includes error handling and edge cases.
  Trigger: "write spec", "create spec", "feature spec", "acceptance criteria".
metadata:
  agent: producer
  input: [requirement, design]
  output: [spec]
  tags: [spec, feature-detail]
  effort: high
---
```

| Field | Required | Purpose |
|---|---|---|
| `name` | Yes | Skill identifier, kebab-case |
| `description` | Yes | What + trigger keywords. Coordinator matches intent here |
| `metadata.agent` | Yes | Which agent owns this skill |
| `metadata.input` | Yes | Input types needed (requirement, design, data, etc.) |
| `metadata.output` | Yes | Output type produced (spec, report, etc.) |
| `metadata.tags` | Yes | For cross-project search |
| `metadata.effort` | No | `low`, `medium` (default), or `high`. Controls prompt tier |
| `metadata.model` | No | Override default model. Only set when different from default |

### Body

The body stays concise — goal, input, output, constraints, pointers:

```markdown
# Write Spec

## Goal
Translate requirements into a specification detailed enough for developers
and QA to execute without asking follow-up questions.

## Input
- Requirement from stakeholder or high-level plan
- Context: user, business goal, constraints
- Design mockups (if available — not required)

## Output
- Spec v1 following ./spec-template/TEMPLATE.md

## Constraints
- Write natural prose, not flowchart-style bullet lists
- If design is incomplete, document logic first and tag design gaps with [GAP-DESIGN-nn]
- Producer does not self-review — reviewer handles that
- Each "TBD" must specify what is needed from whom

## Pointers
- Template: ./spec-template/TEMPLATE.md
- Writing guide: ./writing-guide.md
- Example: ./spec-template/EXAMPLE-01.md
```

> **Why This Matters:** SKILL.md is the entry point, not the entire skill. Keep it under 60 lines. Push procedures to companion files, templates to subfolders, examples alongside templates. A bloated SKILL.md wastes context on every invocation.

---

## Keep SKILL.md Concise

The main definition file contains only what the agent needs to understand scope and constraints. Everything else lives in companion files:

```
skills/
  write-spec/
    SKILL.md                    <-- entry point (concise)
    writing-guide.md            <-- detailed procedures
    spec-template/
      TEMPLATE.md               <-- output structure
      EXAMPLE-01.md             <-- real approved artifact
      EXAMPLE-02.md             <-- another example
```

Rules of thumb:
- SKILL.md: 60 lines max (constraints + pointers)
- Guide file: create only when flow exceeds 30 lines
- Template: create only when output needs fixed structure
- If a skill wraps a single tool call, consider using a rule instead of a dedicated skill

---

## Template + Example Pattern

### Templates define output structure

Templates live in subfolders: `skill-name/template-name/TEMPLATE.md`. They define sections, headings, and placeholders — the skeleton of your output.

```markdown
# [Feature Name] — Specification

## 1. Overview
[Brief description of the feature and its purpose]

## 2. User Stories

### US-01: [Story Title]
**As a** [user type], **I want to** [action], **so that** [benefit].

**Acceptance Criteria:**
- AC-01: [Specific, testable criterion with concrete example]
- AC-02: [Another criterion]

**Corner Cases:**
- CC-01: [Edge case + expected behavior]

## 3. Business Rules
- BR-01: [Rule — declarative, testable, one line]

## 4. Error Handling
| Code | Condition | User Message |
|---|---|---|
| E-01 | [When this happens] | [What user sees] |

## 5. Open Questions
- [ ] [Question] — need [what] from [who] by [when]
```

### Examples are real approved artifacts

Examples sit alongside templates: `EXAMPLE-01.md`, `EXAMPLE-02.md`. These are actual artifacts that passed review — not synthetic demonstrations.

The AI learns style and depth from examples. It does not copy them verbatim. Good examples teach judgment: how detailed should acceptance criteria be? How specific should error messages get? What counts as a corner case worth documenting?

Adding a new example requires no changes to SKILL.md or any other file — just drop it in the folder.

> **Why This Matters:** Templates without examples produce structurally correct but shallow output. Examples without templates produce stylistically good but inconsistently structured output. You need both. Template = skeleton. Example = muscle.

---

## Effort Metadata and Prompt Tiers

The `effort` field in SKILL.md metadata controls how much context the coordinator puts into the prompt when spawning an agent.

### Lite prompt (effort: low or medium)

For straightforward tasks where the agent has enough context from the skill definition and input files.

```
Context: We need a meeting summary from yesterday's product sync.
Skill: meeting-notes
Input: Read g:/workspace/meetings/2025-01-15-product-sync.md
Output: Write summary to g:/workspace/meetings/2025-01-15-product-sync-summary.md
```

Three elements: context (1-2 sentences), input (file paths), output (where to write).

### Full prompt (effort: high)

For complex tasks where the agent needs comprehensive briefing. Five sections:

```
## Context
We are building a file upload feature for the document management module.
Design is 80% complete — drag-and-drop flow is finalized but error states
are still being designed. This spec will go to the dev team for sprint
planning next week.

## Skill + Mode
Skill: write-spec
Read SKILL.md at: .claude/skills/write-spec/SKILL.md
Read template at: .claude/skills/write-spec/spec-template/TEMPLATE.md

## Input
- Requirements doc: knowledge/projects/doc-mgmt/requirements.md
- Design mockup: knowledge/projects/doc-mgmt/upload-flow-v2.md
- Note: error state designs are NOT finalized — document logic, tag gaps

## Confirmed Decisions (do not re-ask these)
1. Max file size: 10MB per file, 100MB total per upload
2. Supported formats: PDF, DOCX, XLSX, PNG, JPG only
3. No folder upload — files only
4. Drag-and-drop + click-to-browse, both required

## Output
Write to: knowledge/projects/doc-mgmt/2025-01-15-upload-spec-v1.md
Follow template at: .claude/skills/write-spec/spec-template/TEMPLATE.md
Read TEMPLATE.md before writing.
```

> **Why This Matters:** This is the single biggest lever for output quality. A terse command ("write a spec for file upload") produces shallow, generic output. A full prompt with context, confirmed decisions, and explicit file paths produces output that reflects your actual situation. Invest 2 minutes writing a good prompt — save 20 minutes fixing bad output.

---

## The Framed Task Prompt (Most Important Pattern)

When the coordinator spawns an agent, that agent starts with a **blank slate**. It sees nothing from your conversation. No history, no decisions you discussed, no context about why this task matters.

You must brief the agent like onboarding a new colleague who just walked into the room:

### The 5 sections

**1. Context — why this task exists (2-3 sentences)**
- What problem are you solving, for whom, by when
- What has been decided so far, what has been ruled out

**2. Skill + mode — what to run**
- Skill name and mode (if the skill has multiple modes)
- Path to SKILL.md so the agent reads flow + constraints
- Path to template so the agent reads output format

**3. Input — what to read**
- File paths (agent reads them itself). Prefer file paths over dumping content
- Only paste text when the content does not exist in any file (verbal decisions, screenshot descriptions)
- If input is output from a previous agent, summarize in 200 tokens max + provide the file path

**4. Confirmed decisions — do not re-ask**
- Short list: "Decided: (1) X, (2) Y, (3) Z"
- Agent needs this to avoid proposing alternatives you already rejected

**5. Output — where and what format**
- Output file path
- Template path (agent MUST read template before writing)

### Why this matters

Without a framed task prompt, the agent guesses. It guesses your context, your constraints, your decisions. Its guesses look plausible — which is worse than obviously wrong, because you might not catch the drift.

With a framed task prompt, the agent operates with the same information you have. Its output reflects your actual situation instead of a generic scenario.

---

## Testing Your Skill

After creating a SKILL.md + template:

1. **Trigger test**: Say something matching the description keywords. Does the coordinator route to the right agent + skill?

2. **Template test**: Does the agent actually read the template before writing? Check: does the output follow the template structure, or did it freestyle?

3. **Constraint test**: Deliberately provide incomplete input. Does the agent flag what is missing (per constraints), or silently assume?

4. **Output test**: Is the output in the right location with the right filename? Does it have frontmatter if your convention requires it?

If the agent ignores the template, add an explicit instruction in SKILL.md: "You MUST read TEMPLATE.md before producing output." Sometimes the pointer alone is not enough — make it a constraint.

---

## Example: Complete Skill for Writing a Spec

```
skills/
  write-spec/
    SKILL.md
    writing-guide.md
    spec-template/
      TEMPLATE.md
      EXAMPLE-01.md
```

**SKILL.md** (the concise entry point shown earlier in this guide)

**writing-guide.md** (procedures, loaded on-demand):
```markdown
# Writing Guide for Specs

## Principles
- Write complete sentences as if explaining to a colleague, not step-by-step
  robot instructions
- Every sentence should pass the "could someone act on this without asking
  a follow-up question?" test
- Business rules stay as bullets (devs need quick reference) but each
  bullet explains enough to be unambiguous
- Brevity is good, but do not cut context that the reader needs to guess

## Process
1. Read all input materials completely. Note specific numbers and names
2. Load template. Fill section by section (do not skip ahead)
3. For each acceptance criterion: include a concrete example with real values
4. For each user story: include at least one corner case
5. Self-check before saving: read each criterion and ask "could QA write
   a test case from this alone?"
```

---

## Key Principles

- **One skill = one task type**: if a skill does two different things, split it
- **SKILL.md is the entry point, not the manual**: keep it concise, point to companion files
- **Templates + examples together**: template gives structure, example gives calibration
- **Effort metadata drives prompt investment**: high-effort skills get full prompts, low-effort get lite
- **Framed task prompts are non-negotiable for quality**: blank-slate agents need full context every time
- **Test after creating**: a skill that is not tested is a skill that does not work
