# Pug Mockup

**Generate self-contained SPA mockups with Pug — from idea to clickable prototype in minutes.**

[![Version](https://img.shields.io/badge/version-v1.0.0-orange)](CHANGELOG.md)
[![skills.sh](https://img.shields.io/badge/skills.sh-compatible-brightgreen)](https://skills.sh)
[![Made with Claude Code](https://img.shields.io/badge/Made_with-Claude_Code-blueviolet?logo=anthropic)](https://claude.ai/claude-code)
[![Pug v3](https://img.shields.io/badge/Pug-v3-A86454?logo=pug)](https://pugjs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/duylamle/product-collection)](https://github.com/duylamle/product-collection)

---

## Why Pug for AI Mockups?

- **~40-50% fewer tokens** than HTML — indent-based, no closing tags. AI writes more UI in less context
- **Structurally enforced nesting** — indentation = hierarchy, fewer broken `</div>` errors
- **Mixin = component** — reuse without frameworks or complex build tools
- **Self-contained output** — CSS/JS inlined via `include`. Single HTML file, works offline
- **Zero runtime** — just `pug-cli` (~2MB). No heavy Node frameworks
- **Not a dead-end** — ~60-70% reusable when moving to React/Next.js/Vue

## Install

```bash
npx skills add duylamle/product-collection@pug-mockup -y
```

## Quick Start

1. Install the skill (above)
2. In Claude Code, say: **"Create a mockup for a task manager app"**
3. Claude generates a Pug project with pages, components, and routing
4. Build: `npm run build`
5. Open `dist/index.html` in any browser — done!

## Prerequisites

- **Node.js** (any recent version)
- **pug-cli**: `npm install -g pug-cli` (or the skill uses `npx`)
- Pug docs: [pugjs.org](https://pugjs.org/api/getting-started.html)

## What's Inside

```
pug-mockup/
├── SKILL.md                           ← Skill definition (Claude reads this)
├── CLAUDE.md                          ← Project map for Claude
├── guide/
│   ├── 1-pug-syntax.md                ← Pug language reference
│   ├── 2-ideal-workflow.md            ← Full 5-stage workflow
│   ├── 3-input-spec.md               ← Input format from companion skills
│   ├── 4-convert-to-production.md     ← Convert to React/Vue/Svelte/Angular
│   └── 5-troubleshooting.md           ← Common errors + fixes
├── template/                          ← Starter project (copy and build on)
│   ├── README.md                      ← Getting started + CLAUDE.md guide
│   ├── package.json                   ← build/watch scripts
│   ├── .gitignore
│   ├── src/
│   │   ├── index.pug                  ← Entry point
│   │   ├── components/                ← Starter mixins (header, sidebar, footer)
│   │   ├── pages/                     ← Starter pages (home, dashboard, login)
│   │   ├── css/main.css               ← Design system (~380 lines)
│   │   └── js/main.js                 ← SPA hash router
│   └── dist/                          ← Build output (do not edit)
│       ├── index.html
│       └── assets/
└── examples/
    └── demo-project/                  ← 5-page working demo (open demo.html)
```

## Guides (reading order)

| # | Guide | When to read |
|---|---|---|
| 1 | [Pug Syntax](guide/1-pug-syntax.md) | Learning Pug or looking up syntax |
| 2 | [Ideal Workflow](guide/2-ideal-workflow.md) | Understanding the full mockup pipeline |
| 3 | [Input Spec](guide/3-input-spec.md) | Feeding better input from companion skills |
| 4 | [Convert to Production](guide/4-convert-to-production.md) | Moving approved mockup to React/Vue/etc. |
| 5 | [Troubleshooting](guide/5-troubleshooting.md) | Build errors, blank pages, broken icons |

## Output

The skill produces a **single self-contained HTML file**:
- All CSS and JS inlined (no external dependencies)
- Hash-based SPA routing (multiple pages, one file)
- Works offline — double-click to open
- Share with anyone — no server needed

## Works Well With

| Skill type | Why |
|---|---|
| UI/UX planning | Design before coding — layout, flow, wireframe |
| Design system | Feed color/typography tokens into `main.css` |
| Accessibility audit | QC the mockup after build |

Find complementary skills on [skills.sh](https://skills.sh).

## Converting to Production

Pug mockups transfer to any framework:

| Pug | → Production |
|---|---|
| Mixin | React/Vue component |
| `include` | ES module `import` |
| CSS tokens | Tailwind config |
| Lucide SVG | `lucide-react` / `lucide-vue` |

Vue natively supports Pug in templates (`<template lang="pug">`).

See [full conversion guide](guide/4-convert-to-production.md) for step-by-step + syntax mapping.

## License

[MIT](../../LICENSE)
