# Pug Mockup

> Generate self-contained SPA mockups with Pug template engine.
> Install: `npx skills add duylamle/product-collection@pug-mockup -y`

## How to use

Say **"create a mockup"** or **"build a pug mockup"** in Claude Code.

### Two phases of work:

**Phase 1 — Generate:** Describe what you want → skill creates full project (all pages, components, routing, CSS).

**Phase 2 — Iterate:** Open a specific `.pug` file → select the section → describe the change → rebuild.

> Don't edit the whole project at once. Point to the exact file + section for precise changes.

## Structure

```
pug-mockup/
├── SKILL.md                    ← Skill definition (start here)
├── CLAUDE.md                   ← This file
├── guide/
│   ├── 0-nontech-workflow.md   ← Start here if non-technical
│   ├── 1-pug-syntax.md         ← Pug language reference
│   ├── 2-ideal-workflow.md     ← Full 5-stage workflow
│   ├── 3-input-spec.md         ← Input format from companion skills
│   ├── 4-convert-to-production.md ← Convert to React/Vue/Svelte/Angular
│   └── 5-troubleshooting.md    ← Common errors + fixes
├── template/                   ← Starter project (copy to begin)
│   ├── README.md               ← Getting started guide
│   ├── package.json            ← npm run build / watch
│   ├── .gitignore
│   ├── src/
│   │   ├── index.pug           ← Entry point
│   │   ├── components/         ← Starter mixins + pattern reference
│   │   ├── pages/              ← Starter pages + layout reference
│   │   ├── css/                ← Design tokens + component reference
│   │   └── js/                 ← SPA router + interaction reference
│   └── dist/                   ← Build output (do not edit)
│       ├── index.html
│       └── assets/
└── examples/
    └── demo-project/           ← 5-page working demo (open demo.html)
```

## Key files to read

| When you need... | Read |
|---|---|
| How the skill works | `SKILL.md` |
| Pug syntax help | `guide/1-pug-syntax.md` |
| Full workflow (define → build → review → convert) | `guide/2-ideal-workflow.md` |
| What input makes better output | `guide/3-input-spec.md` |
| Convert mockup to production framework | `guide/4-convert-to-production.md` |
| Fix build errors | `guide/5-troubleshooting.md` |
| How to customize CSS tokens | `template/src/css/README.md` |
| How to write components | `template/src/components/README.md` |
| How to create pages | `template/src/pages/README.md` |
| How to add interactivity | `template/src/js/README.md` |
| What the output looks like | `examples/demo-project/demo.html` |

## CLAUDE.md for generated projects

When creating a new mockup project, **always generate a `CLAUDE.md`** in the
project root. This is the map that helps Claude (and the user) navigate the
project in future sessions.

**What to include:**

```markdown
# [Project Name] — Pug Mockup

> One-line description.

## Pages
| Page | File | Route | Layout |
| (list all pages with file path, hash route, layout type) |

## Components
| File | Mixin | Used by |
| (list all components, which pages use them) |

## Design Decisions
- Primary color: [hex] — [why]
- Layout: [sidebar/top-nav] — [why]
- (any non-obvious decisions so future edits don't break them)

## Build
npm install / npm run build / npm run watch
```

**Why:** Without this file, opening the project later requires reading every
`.pug` file to understand what exists. With it, Claude reads one file and
knows the full structure — faster edits, fewer mistakes.

See `examples/demo-project/CLAUDE.md` for a working example.

## Build commands

```bash
npm run build        # compile src/index.pug → dist/index.html
npm run watch        # auto-rebuild on file changes
```

## Prerequisites

- Node.js (any recent version)
- pug-cli: `npm install -g pug-cli` or use `npx pug-cli`
- Docs: https://pugjs.org/api/getting-started.html
