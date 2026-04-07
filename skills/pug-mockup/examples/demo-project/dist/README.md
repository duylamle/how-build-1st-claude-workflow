# dist/ — Build Output

This folder contains the compiled output from `npm run build`.

## Files

- **`index.html`** — The compiled, self-contained HTML file. All CSS and JS
  from `src/` are inlined — no external dependencies. Open this file in any
  browser to view your mockup.
- **`assets/`** — Static files (images, icons, fonts). Not processed by Pug —
  copy them here manually.

## Important

- **Do not edit files here.** They get overwritten on every build.
  Edit `.pug` files in `src/` instead, then rebuild.
- **This is what you share.** Send `index.html` (or the whole `dist/` folder
  if you have assets) — recipients open it in any browser, no install needed.
