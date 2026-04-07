# Product Collection

> A curated collection of Claude Code skills for product work.
> Install individual skills with `npx skills add duylamle/product-collection@[skill-name] -y`.

## Available Skills

| Skill | What it does |
|---|---|
| `claude-personal-workflow-builder` | Interactive guide to build, maintain, and grow your AI Personal System with Claude Code. 13 phases from zero to a working system with agents, skills, rules, hooks, and memory. |
| `pug-mockup` | Generate self-contained SPA mockups with Pug template engine + Lucide SVG icons. Single HTML output, works offline. |

## How to use

Each skill lives in `skills/[skill-name]/`. After installing a skill, say its trigger phrase in Claude Code:

- **claude-personal-workflow-builder**: Say "Build my AI workflow" or "Guide me through setting up my AI system"
- **pug-mockup**: Say "Create a mockup" or "Build a pug mockup"

## Structure

```
skills/
├── claude-personal-workflow-builder/
│   ├── SKILL.md      ← Skill definition (Claude reads this automatically)
│   ├── guide/        ← Phase-by-phase guides
│   ├── templates/    ← Starter templates you'll customize
│   └── examples/     ← Complete setups for 3 roles
└── pug-mockup/
    ├── SKILL.md      ← Skill definition
    ├── guide/        ← Pug syntax reference
    ├── template/     ← Starter project (copy and build on)
    └── examples/     ← Walkthrough examples
```

## About

Built by Lê Trương Duy Lam — Technical Product Owner at VNG Corporation.
These skills are distilled from real operational experience running an AI personal system for product work.
