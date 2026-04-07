---
# YAML frontmatter — Claude reads this to understand what this skill does.
#
# FIELD GUIDE:
#
# name:
#   kebab-case identifier. Must match the folder name this SKILL.md lives in.
#   Example: folder `.claude/skills/write-prd/` -> name: write-prd
#
# description:
#   What this skill does + trigger keywords for auto-matching. This is how
#   Claude decides to activate this skill. Be specific and include the exact
#   phrases a user would say.
#   Good: "Writes feature PRDs with user stories and acceptance criteria.
#          Trigger: 'write PRD', 'create spec', 'feature detail'."
#   Bad:  "Helps with product documentation." (too vague to match reliably)
#
# metadata.agent:
#   Which agent owns this skill. Must match an agent name in `.claude/agents/`.
#   One skill belongs to exactly one agent.
#
# metadata.input:
#   What types of input this skill needs to run. Use standard vocabulary:
#   - requirement — user or stakeholder request
#   - design — wireframes, mockups, Figma links
#   - data — metrics, analytics, numbers
#   - meeting-notes — notes from a meeting
#   - prd — an existing PRD document
#   - artifact — any other existing document
#   You can list multiple: [requirement, design]
#
# metadata.output:
#   What type of artifact this skill produces. Use standard vocabulary:
#   - prd — product requirements document
#   - report — analysis or review report
#   - spec — technical specification
#   - handoff — developer handoff document
#   - diagram — visual diagram (PlantUML, Mermaid, etc.)
#
# metadata.tags:
#   For cross-project search. Convention: [project-tag, topic-tag, detail-tags...]
#   Example: [acme-app, onboarding, user-flow, signup]
#   Reuse existing tags when possible — don't create synonyms.
#
# metadata.effort:
#   How much reasoning this skill requires. Affects prompt detail level:
#   - low: simple transformation, formatting, extraction. Short prompt is fine.
#   - medium (default): analysis, synthesis, moderate reasoning. Standard prompt.
#   - high: complex reasoning, multi-step production, expert judgment needed.
#     Full prompt with all 5 sections (context, skill, input, decisions, output).
#   Only specify if different from medium.

name: [TODO: skill-name]
description: >
  [TODO: Describe what this skill does in 2-3 sentences. Include trigger
  keywords so Claude knows when to activate it.
  Example: "Writes feature PRDs with user stories, acceptance criteria,
  and corner cases. Trigger: 'write PRD', 'create spec', 'feature detail'."]
metadata:
  agent: [TODO: agent-name]
  input: [TODO: e.g., requirement, design]
  output: [TODO: e.g., prd, report]
  tags: [TODO: e.g., product, feature-detail]
  effort: medium
---

# [TODO: Skill Name]

> [TODO: One-line description of what this skill produces.]

---

## Goal

- [TODO: What is this skill trying to achieve?]
- [TODO: What problem does the output solve for the reader?]

---

## Input

[TODO: Describe what this skill needs to run. Be specific about minimum
viable input vs nice-to-have input.

Example:
- Required: Requirement description (from user or upstream document)
- Optional: wireframes, research data, baseline metrics

Minimum viable: a clear description of what needs to be built and for whom.
If input is less than 2 sentences or too vague, ask for clarification before
running the skill.]

---

## Output

[TODO: Describe the artifact this skill produces. If you have a template,
point to it here.

Example:
- Feature PRD following `./prd/TEMPLATE.md`
- Includes: overview, user stories, acceptance criteria, error handling

If the skill can produce different formats depending on context, describe
each variant and when to use it.]

---

## Constraints

- [TODO: What should this skill NOT do?]
- [TODO: Boundaries, limits, things to avoid]
- Missing info -> note as "TBD — needs [what] from [who]", do not fill with assumptions
- [TODO: Add domain-specific constraints]

---

## Pointers

[TODO: Point to supporting files in this skill's folder. Only create these
files when you actually need them — do not pre-create empty files.

Examples:
- `./guide.md` — detailed step-by-step procedure (create when flow > 30 lines)
- `./prd/TEMPLATE.md` — output template (create when output needs fixed structure)
- `./EXAMPLE-01.md` — approved real example for AI to learn style from]

---

## Filled Example — write-analysis Skill

Below is what a completed SKILL.md looks like. Use it as a reference, then
delete this section from your own file.

```yaml
---
name: write-analysis
description: >
  Writes structured analysis reports from raw data or research input.
  Covers competitive analysis, market sizing, and feature comparison.
  Trigger: "analyze", "comparison report", "market analysis", "competitive review".
metadata:
  agent: product-owner
  input: [data, requirement]
  output: [report]
  tags: [product, analysis, competitive]
  effort: high
---
```

```markdown
# Write Analysis

> Produces structured analysis reports from raw data, research, or feature comparisons.

---

## Goal

- Transform raw data and research into actionable, structured analysis
- Make recommendations explicit with supporting evidence and trade-offs
- Output should be shareable with stakeholders without further editing

---

## Input

- Required: Research data or topic description with clear analysis question
- Optional: competitor data, internal metrics, previous analysis for comparison
- Minimum viable: a clear question ("How does our pricing compare to X and Y?")

---

## Output

- Analysis report following `./analysis/TEMPLATE.md`
- Includes: executive summary, methodology, findings, recommendations, appendix
- Charts described in markdown (or PlantUML if visual is critical)

---

## Constraints

- Cite sources for every factual claim — no unsourced assertions
- Separate findings (what the data shows) from recommendations (what to do)
- Do not recommend a single option without showing alternatives and trade-offs
- Numbers from sources stay exact — no rounding

---

## Pointers

- `./analysis/TEMPLATE.md` — output template with section structure
- `./guide.md` — step-by-step procedure for running the analysis
- `./EXAMPLE-01.md` — approved competitive analysis for reference
```

---

## Tips for Companion Files

### When to create `guide.md`

Create a guide file when the skill's procedure exceeds 30 lines. The guide
contains the step-by-step flow, decision points, and edge case handling.
Keep SKILL.md lean (constraints + pointers) and put procedures in the guide.

### When to create a `template/` folder

Create a template folder when the output needs a fixed structure that should
be consistent across uses. Templates define sections, headings, and
placeholder content. If the output format varies every time, you don't need
a template — describe the format in the Output section instead.

### When to add `EXAMPLE-*.md` files

Add example files when:
- The output has a specific style or tone that's hard to describe in words
- You've approved a real output and want future outputs to match its quality
- Claude keeps missing the mark despite clear constraints — an example
  teaches by showing, not telling

Examples should be real, approved artifacts — not fabricated demos. Name them
`EXAMPLE-01.md`, `EXAMPLE-02.md`, etc.

---

## Common Mistakes

1. **SKILL.md too long:** If your SKILL.md exceeds 60 lines (excluding the
   filled example), push detail into companion files. SKILL.md should be
   constraints + pointers, not a full manual.

2. **Missing template pointer:** If the skill produces structured output but
   doesn't point to a template, every run will produce a different format.
   Either create a template or describe the expected format precisely in Output.

3. **Vague constraints:** "Be thorough" and "write clearly" are not constraints.
   "Every recommendation must include at least one trade-off" and "Flag data
   points from assumption vs source" are constraints.

4. **No input minimum:** Without a minimum viable input definition, the skill
   will try to run on vague one-liners and produce garbage. Define what
   "enough input" looks like.

5. **Effort mismatch:** Marking a complex reasoning skill as `effort: low`
   means it gets a short prompt with minimal context. Be honest about
   complexity — it affects output quality.
