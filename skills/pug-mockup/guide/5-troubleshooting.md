# Troubleshooting

Common issues when working with pug-mockup and how to fix them.

---

### "pug: command not found"

**Cause:** pug-cli not installed.

**Fix:**
```bash
npm install -g pug-cli       # install globally
# or use without installing:
npx pug-cli src/index.pug -o dist -P
```

If using `package.json` (recommended):
```bash
npm install                  # installs pug-cli as devDependency
npm run build                # uses local pug-cli
```

---

### "unexpected token / indentation error"

**Cause:** Pug is whitespace-sensitive. Mixed tabs and spaces, or wrong indent level.

**Fix:**
- Use **spaces only** (2 spaces per indent level is standard)
- Check your editor is not inserting tabs
- Every child element must be indented exactly one level deeper than its parent

```pug
//- ✗ Wrong — mixed indent
.card
  h3 Title
    p Text          //- this is 2 levels deep, should be 1

//- ✓ Correct
.card
  h3 Title
  p Text            //- same level as h3 (both children of .card)
```

---

### "build succeeds but page is blank"

**Cause:** Page not registered in `main.js`, or page ID mismatch.

**Check:**
1. Page file has `.page#page-[name]` wrapper:
   ```pug
   .page#page-dashboard    //- ID must match
   ```
2. `main.js` includes the page name in the pages array:
   ```js
   var loggedPages = ['dashboard'];   //- must match "dashboard" from #page-dashboard
   ```
3. `index.pug` includes the page file:
   ```pug
   include pages/dashboard.pug
   ```

All three must agree on the same name.

---

### "component mixin not found / undefined"

**Cause:** Component file not included in `index.pug`, or included after the page that uses it.

**Fix:** Include components **before** pages in `index.pug`:
```pug
//- ✓ Correct order
include components/header.pug      //- define mixins first
include components/sidebar.pug
include pages/dashboard.pug        //- then pages that use them

//- ✗ Wrong — page before component
include pages/dashboard.pug        //- +sidebar() not defined yet!
include components/sidebar.pug
```

---

### "CSS changes don't show up"

**Cause:** Browser cache, or forgot to rebuild.

**Fix:**
1. Rebuild: `npm run build`
2. Hard refresh browser: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
3. Or use watch mode to auto-rebuild: `npm run watch`

---

### "SVG icons not rendering"

**Cause:** SVG wrapped in Pug syntax instead of raw HTML.

**Fix:** SVG must be raw HTML on a single line inside Pug:
```pug
//- ✓ Correct — raw HTML inline
span.icon
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/></svg>

//- ✗ Wrong — trying to use Pug syntax for SVG
span.icon
  svg(width="18" height="18")     //- attributes work but children break
    circle(cx="11" cy="11" r="8") //- self-closing tags get mangled
```

Get SVG code from [lucide.dev](https://lucide.dev) → copy the SVG → paste as raw HTML.

---

### "special characters / unicode broken in output"

**Cause:** File not saved as UTF-8.

**Fix:**
- Ensure your editor saves `.pug` files as **UTF-8** (not UTF-8 BOM, not ANSI)
- Check terminal encoding if characters look wrong in the compiled HTML
- Pug passes text through unchanged — if the source file is UTF-8, the output will be too

---

### "npm run build fails with ENOENT"

**Cause:** Running build from wrong directory, or `src/index.pug` doesn't exist.

**Fix:**
```bash
# Make sure you're in the project root (where package.json is)
cd my-project
ls src/index.pug       # should exist
npm run build
```

---

### "I edited main.css but new styles aren't applied"

**Cause:** CSS class name in `.pug` doesn't match what's in `main.css`.

**Fix:** Check that the Pug class matches exactly:
```pug
//- Pug uses this class:
.card.stat-card

//- main.css must have:
.stat-card { ... }     //- ✓ matches
.statCard { ... }      //- ✗ doesn't match (camelCase vs kebab-case)
```

Use the browser DevTools (F12 → Elements) to inspect which classes are on the element and whether the CSS rules are being applied.
