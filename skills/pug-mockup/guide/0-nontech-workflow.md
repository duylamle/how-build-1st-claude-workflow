---
type: artifact
scope: guide
created: 2026-04-10
updated: 2026-04-10
---

# Getting Started — For Non-Technical Users

> You don't need to know code to use this skill. This guide walks you through
> the actual workflow: what you do, what you say, and what happens.

---

## What This Skill Does (Plain English)

You describe what you want ("a dashboard with 5 pages for a task manager").
AI builds a clickable prototype — a real web page you can open in your browser,
click through, and share with anyone. No server needed, no coding required.

The output is a single HTML file. Double-click it → it opens in your browser.
Send it to a colleague → they double-click → they see exactly what you see.

---

## Your Workflow (3 Steps)

### Step 1: Describe What You Want

Tell Claude Code what to build. Be specific about pages and content:

```
Create a mockup for a project management tool with these pages:
- Dashboard: show 4 stat cards (total projects, active, completed, overdue)
  and a recent activity feed
- Projects list: table with name, status, owner, deadline. Filterable
- Project detail: title, description, timeline, team members, files
- Settings: profile info, notification preferences
- Login: email/password form, forgot password link

Use blue as primary color. Sidebar layout for logged-in pages.
Style: clean and minimal, like Linear or Notion.
```

**The more specific you are, the better the result.** Compare:

| Vague (more revision rounds) | Specific (fewer revision rounds) |
|---|---|
| "Make a dashboard" | "Dashboard with 4 stat cards showing total, active, completed, overdue counts + a recent activity feed below" |
| "Add some pages" | "5 pages: dashboard, projects list, project detail, settings, login" |
| "Make it look nice" | "Clean and minimal like Linear. Blue primary color. Sidebar navigation" |

### Step 2: Build and View

After AI generates the project, build it:

```bash
npm run build
```

Then open the result in your browser:
- Find `dist/index.html` in your project folder
- Double-click it (or drag into browser)
- Click through pages, check layout, review content

### Step 3: Ask for Changes (One at a Time)

Don't say "make it better." Point to the specific thing you want to change:

| What you want to change | What to say |
|---|---|
| Colors | "Change primary color to green (#059669)" |
| A specific page's layout | "On the dashboard page, move the activity feed above the stat cards" |
| Add content to a page | "On the projects list, add a search bar above the table" |
| Navigation | "Add a 'Reports' section to the sidebar with 2 links: Weekly and Monthly" |
| Overall style | "Make buttons more rounded and increase card shadows" |
| Add a new page | "Add a user profile page with avatar, name, email, and activity history" |

After each change → `npm run build` → refresh browser → check result.

---

## Cheat Sheet: "I Want To..." → "I Say..."

| I want to... | I say to Claude... | What changes |
|---|---|---|
| Change the colors | "Change primary color to [hex] in main.css" | `src/css/main.css` |
| Rearrange a page | "In pages/dashboard.pug, move [section] above [section]" | `src/pages/[page].pug` |
| Change sidebar items | "In components/sidebar.pug, add/remove [item]" | `src/components/sidebar.pug` |
| Change header | "In components/header.pug, change [what]" | `src/components/header.pug` |
| Add a new page | "Create a new page called [name] with [content]" | New file in `src/pages/` |
| Fix spacing/fonts | "In main.css, change font size to [X] / increase card padding" | `src/css/main.css` |
| Start over with different style | "Rebuild the project with [new style description]" | Most files |

---

## What's In the Project Folder

```
your-project/
├── src/                 ← SOURCE (what gets edited)
│   ├── components/      ← Shared pieces (header, sidebar, footer)
│   ├── pages/           ← One file per page (dashboard.pug, settings.pug)
│   ├── css/main.css     ← Colors, fonts, spacing
│   └── js/main.js       ← Page switching logic
└── dist/
    └── index.html       ← OUTPUT (what you open in browser)
```

**You only care about 2 things:**
1. **`src/` folder** — where changes happen (AI edits these files for you)
2. **`dist/index.html`** — what you open in the browser after building

You never need to edit files directly. Just tell Claude what to change.

---

## Common Questions

**"Do I need to know Pug/HTML/CSS?"**
No. You describe changes in plain language. AI writes the code. You review the visual result.

**"What if I don't like the result?"**
Ask for changes. Be specific: "the stat cards are too wide, make them narrower" works better than "I don't like it."

**"Can I share the result?"**
Yes. The `dist/index.html` file is self-contained. Send it via email, Slack, or any file sharing. The recipient just opens it in a browser.

**"Can this become a real product?"**
Yes, with additional work. The mockup's structure (pages, components, styling) transfers ~60-70% to production frameworks like React or Vue. But auth, API integration, and real data are built fresh. See [guide/4-convert-to-production.md](4-convert-to-production.md).

**"What's the design reference library?"**
Check out [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) — a collection of 58 design systems (Apple, Google, Stripe, Linear, etc.) as markdown files. You can reference any of these when describing your desired style: "style like the Stripe design system."

---

## Next Steps

- Want to understand the full workflow? → [guide/2-ideal-workflow.md](2-ideal-workflow.md)
- Want to give better input for better output? → [guide/3-input-spec.md](3-input-spec.md)
- Build errors? → [guide/5-troubleshooting.md](5-troubleshooting.md)
