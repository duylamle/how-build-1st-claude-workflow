# Claude Personal Workflow Builder

> Interactive guide to build your AI Personal System with Claude Code.
> Install: `npx skills add duylamle/product-collection@claude-personal-workflow-builder -y`

## How to use

Say **"build my AI workflow"** or **"guide me through setting up my AI system"**.

**Three modes:**
- **Guided** (default) — walk through phases sequentially, I ask for your input at each step
- **Menu** — say "show me the phases" to jump to any specific phase
- **Consult** — say "I have a question" for direct Q&A, no walkthrough

## Structure

```
claude-personal-workflow-builder/
├── SKILL.md                  ← Skill definition (Claude reads this)
├── CLAUDE.md                 ← This file
├── README.md                 ← GitHub readme
├── CHANGELOG.md
├── guide/                    ← 13 phases + troubleshooting
│   ├── 00-prerequisites.md
│   ├── 01-intro.md
│   ├── 02-self-assessment.md
│   ├── 03-foundation.md
│   ├── 04-rules.md
│   ├── 05-agents.md
│   ├── 06-skills.md
│   ├── 07-memory-knowledge.md
│   ├── 08-hooks-automation.md
│   ├── 09-advanced-patterns.md
│   ├── 10-skill-absorption.md
│   ├── 11-tuning.md
│   ├── 12-iterate-grow.md
│   └── 13-troubleshooting.md
├── templates/                ← Starter files generated for user
│   ├── root-claude-md.md     ← Root CLAUDE.md template
│   ├── agent-md.md           ← Agent definition template
│   ├── skill-md.md           ← Skill definition template
│   ├── rule-communication.md
│   ├── rule-workflow.md
│   ├── rule-coordination.md
│   ├── memory-index.md
│   └── hook-validate-example.py
├── references/               ← External research + context
│   ├── engineering-workflows.md
│   ├── knowledge-management-and-rag.md
│   ├── prompt-framing.md
│   └── agent-platform-mapping.md
└── examples/                 ← Complete setups for 4 roles
    ├── po-setup.md
    ├── marketer-setup.md
    ├── developer-setup.md
    └── manager-setup.md
```

## Key files to read

| When you need... | Read |
|---|---|
| How the skill works | `SKILL.md` |
| Specific phase content | `guide/[NN]-[phase].md` |
| Starter templates to customize | `templates/` |
| Real-world setup examples | `examples/` |
| External research + context | `references/` |
| Common issues | `guide/13-troubleshooting.md` |

## Phases (reading order)

| # | Phase | What gets built |
|---|---|---|
| 0 | [Prerequisites](guide/00-prerequisites.md) | Claude Code installed, workspace ready |
| 1 | [Intro](guide/01-intro.md) | Philosophy + architecture understanding |
| 2 | [Self-Assessment](guide/02-self-assessment.md) | Role, pain points, MVP scope |
| 3 | [Foundation](guide/03-foundation.md) | Workspace, root CLAUDE.md, folder structure |
| 4 | [Rules](guide/04-rules.md) | 3 core behavioral guardrails |
| 5 | [Agents](guide/05-agents.md) | Producer + Reviewer agents |
| 6 | [Skills](guide/06-skills.md) | 2-3 bounded capabilities with templates |
| 7 | [Memory & Knowledge](guide/07-memory-knowledge.md) | Feedback system + domain context |
| 8 | [Hooks & Automation](guide/08-hooks-automation.md) | Validators, backup, session logging |
| 9 | [Advanced Patterns](guide/09-advanced-patterns.md) | English-first, framed task, handoff |
| 10 | [Skill Absorption](guide/10-skill-absorption.md) | Learn from community skills |
| 11 | [Tuning](guide/11-tuning.md) | Escalation ladder for improving output |
| 12 | [Iterate & Grow](guide/12-iterate-grow.md) | Monthly review, publishing, scaling |

**Quick start:** Phases 0 → 1 → 3 are foundation. Then pick what you need.
See Phase 1 intro for flexible reading paths.

## How to guide users

1. Read the corresponding `guide/[NN]-*.md` for each phase
2. Explain concepts and why they matter
3. Ask the user for their specific input (role, preferences, domain)
4. Generate files in their workspace using `templates/` as base
5. Show what was created, ask if ready for next phase
6. Reference `examples/` when user asks "show me what this looks like for a [role]"
