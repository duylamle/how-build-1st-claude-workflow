# Template — Starter Project

> Copy this folder to start a new mockup project.
> Everything is ready — just add pages and build.

## Getting Started

```bash
# 1. Copy this folder
cp -r template/ my-project/

# 2. Install pug-cli
cd my-project
npm install

# 3. Add your pages in src/pages/, include them in src/index.pug

# 4. Create CLAUDE.md (project map — helps Claude navigate your project)
#    See "CLAUDE.md for your project" section below

# 5. Build
npm run build        # → dist/index.html (open in browser)
npm run watch        # auto-rebuild on file changes
```

## What's in package.json

```
"scripts": {
  "build": "pug src/index.pug -o dist -P"     ← compile once (pretty-print)
  "watch": "pug src/index.pug -o dist -P -w"   ← auto-rebuild on save
}

"devDependencies": {
  "pug-cli": "^1.0.0-alpha6"    ← the Pug compiler (only dependency)
}
```

- `npm run build` reads `src/index.pug` → compiles all includes → outputs `dist/index.html`
- `npm run watch` does the same but watches for file changes and rebuilds automatically
- `pug-cli` is the only dependency (~2MB). No frameworks, no bundlers

## Folder Structure

```
template/
├── package.json          ← build scripts + pug-cli dependency
├── .gitignore            ← ignores node_modules/ and dist/
├── src/                  ← EDIT HERE
│   ├── index.pug         ← entry point — includes everything
│   ├── components/       ← shared mixins (header, sidebar, footer)
│   ├── pages/            ← 1 file per page
│   ├── css/main.css      ← design tokens + component styles
│   └── js/main.js        ← SPA hash router
└── dist/                 ← BUILD OUTPUT (do not edit)
    ├── index.html        ← compiled HTML — open this to view
    └── assets/           ← static files (images, icons, fonts)
```

## Every folder has a README

Each subfolder has its own README with "I need to..." examples:
- `src/components/README.md` — mixin patterns
- `src/pages/README.md` — page layout patterns
- `src/css/README.md` — design tokens + CSS component reference
- `src/js/README.md` — router + interaction patterns
- `dist/README.md` — what the output is and how to share it

## CLAUDE.md for Your Project

After creating your pages and components, **add a `CLAUDE.md`** in the project
root. This is the map that helps Claude (and you) navigate the project later.

```markdown
# [Project Name] — Pug Mockup

> One-line description of what this mockup is for.

## Pages

| Page | File | Route | Layout |
|---|---|---|---|
| Home | `src/pages/home.pug` | `#home` | Landing — hero, features |
| Dashboard | `src/pages/dashboard.pug` | `#dashboard` | Sidebar — stats, activity |
| Login | `src/pages/login.pug` | `#login` | Standalone — centered card |

## Components

| File | Mixin | Used by |
|---|---|---|
| `src/components/header.pug` | `+header('page')` | All pages |
| `src/components/sidebar.pug` | `+sidebar('page')` | Dashboard |
| `src/components/footer.pug` | `+footer()` | Home |

## Design Decisions

- Primary color: #2563EB — [reason]
- Layout: sidebar for logged-in pages — [reason]
- (any non-obvious choices so future edits don't break them)

## Build

npm install && npm run build
```

**Why?** Without this, reopening the project later means reading every `.pug`
file to understand what exists. With it, Claude reads one file and knows the
full structure — faster edits, fewer mistakes.

See `../examples/demo-project/CLAUDE.md` for a working example.
