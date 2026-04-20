# Product Collection

> A curated collection of Claude Code skills for product work.
> Install individual skills with `npx skills add duylamle/product-collection@[skill-name] -y`.

## Available Skills

| Skill | What it does |
|---|---|
| `claude-personal-workflow-builder` | Interactive guide to build, maintain, and grow your AI Personal System with Claude Code. 13 phases from zero to a working system with agents, skills, rules, hooks, and memory. |
| `pug-mockup` | Generate self-contained SPA mockups with Pug template engine + Lucide SVG icons. Single HTML output, works offline. |
| `excel-pipeline` | Parse multi-source data (Excel, CSV, markdown) → JSONL → formatted Excel. Full pipeline with formulas, lookups, audit, diff. |
| `sidekick-agent-mcp-setup` | Install sidekick-agent MCP to shift tokens from senior Claude to a cheaper junior LLM. Bundles delegation rule + nested `sidekick-call` companion skill for day-to-day calls. |

## How to use

Each skill lives in `skills/[skill-name]/`. After installing a skill, say its trigger phrase in Claude Code:

- **claude-personal-workflow-builder**: Say "Build my AI workflow" or "Guide me through setting up my AI system"
- **pug-mockup**: Say "Create a mockup" or "Build a pug mockup"
- **excel-pipeline**: Say "Parse data", "Export excel", or "Data pipeline"
- **sidekick-agent-mcp-setup**: Say "install sidekick" or "setup sidekick" the first time. Afterwards "sidekick tóm tắt", "sidekick dịch", or "nhờ sidekick extract" triggers the nested `sidekick-call` skill

## Structure

```
skills/
├── claude-personal-workflow-builder/
│   ├── SKILL.md      ← Skill definition (Claude reads this automatically)
│   ├── guide/        ← Phase-by-phase guides
│   ├── templates/    ← Starter templates you'll customize
│   └── examples/     ← Complete setups for 3 roles
├── pug-mockup/
│   ├── SKILL.md      ← Skill definition
│   ├── guide/        ← Pug syntax reference
│   ├── template/     ← Starter project (copy and build on)
│   └── examples/     ← Walkthrough examples
├── excel-pipeline/
│   ├── SKILL.md      ← Skill definition
│   ├── guide/        ← Workflow guide with examples
│   └── scripts/      ← 7 Python scripts (parse, merge, audit, diff, export)
└── sidekick-agent-mcp-setup/
    ├── SKILL.md            ← Skill definition
    ├── mcp/                ← Python MCP server source (ship-in-skill)
    ├── guide/              ← Setup walk-through (9 steps)
    ├── examples/           ← Real use cases with token impact
    └── docs/               ← Drop-in docs for Claude Code projects
        ├── rules/              ← Delegation rule for your .claude/rules/
        └── skills/
            └── sidekick-call/  ← Companion skill for day-to-day calls
```

## Versioning

- Repo: `0.Y.Z` — Y = number of skills, Z = patch (docs/badges)
- Skills: independent semver — X (multi-folder change), Y (single folder), Z (single file)

## About

Built by Lê Trương Duy Lam — Technical Product Owner at VNG Corporation.
These skills are distilled from real operational experience running an AI personal system for product work.
