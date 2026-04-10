# Changelog — pug-mockup

## v1.1.0 (2026-04-10)

### Added
- **Nontech Workflow Guide** (`guide/0-nontech-workflow.md`) — step-by-step for non-technical users: describe → build → iterate, with cheat sheet
- **Nontech-first README** — "What This Does" section at top explaining the skill in plain language
- **Concrete prompt examples** in input spec guide (3 detailed prompts)
- **awesome-design-md reference** — 58 design systems for style inspiration

## v1.0.0 (2026-04-08)

### Added
- SKILL.md — full skill definition (why Pug, flow, iterate workflow, constraints, companion skills, conversion guide)
- CLAUDE.md — project map + guide for generating CLAUDE.md in user projects
- **Guides** (numbered reading order):
  - `1-pug-syntax.md` — Pug language reference, SPA router, component/layout patterns, gotchas
  - `2-ideal-workflow.md` — 5-stage workflow (define → design → build → review → convert)
  - `3-input-spec.md` — input format from companion skills (3 tiers: text → brief → full specs)
  - `4-convert-to-production.md` — generic conversion guide + syntax mapping (React, Vue, Svelte, Angular, vanilla)
  - `5-troubleshooting.md` — 9 common errors with fixes
- **Template** (starter project):
  - `index.pug` — entry point with inline documentation
  - `css/main.css` — design system (~380 lines: tokens, typography, layout, buttons, cards, badges, forms, tables, modals, toasts, tabs, avatars, responsive)
  - `js/main.js` — SPA hash router (public vs logged pages)
  - 3 starter components: `header.pug`, `sidebar.pug`, `footer.pug`
  - 3 starter pages: `home.pug` (landing), `dashboard.pug` (sidebar), `login.pug` (centered card)
  - `package.json` with build/watch scripts
  - `.gitignore`
  - `dist/` output folder with `assets/`
  - README guides in every subfolder (`components/`, `pages/`, `css/`, `js/`, `dist/`) — "I need to..." format
- **Examples**:
  - `demo-project/` — 5-page working demo (home, dashboard, tasks, settings, login) with 3 components, pre-built `demo.html`
  - `demo-project/CLAUDE.md` — example project map
- README.md with badges, guides table, hyperlinked file index
