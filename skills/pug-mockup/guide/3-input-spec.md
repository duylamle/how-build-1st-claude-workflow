# Input Spec — What Companion Skills Should Provide

> This file describes the **ideal input format** for pug-mockup.
> If you're building a skill that feeds into mockup generation (UI/UX planning,
> design system, etc.), this is what your output should look like.
>
> Pug-mockup works without any of this — a text description is enough.
> But structured input → dramatically better output.

---

## Why This Matters

Without structured input, AI guesses:
- Colors? Defaults to generic blue
- Layout? Defaults to sidebar + cards
- Typography? Defaults to system font
- Spacing? Defaults to uniform gaps

With structured input, AI builds exactly what you designed. The mockup
reflects intentional decisions, not AI defaults.

---

## Input Tiers

### Tier 1: Text Description (minimum)

Just describe what you want. This always works.

```
Create a task manager with 5 pages: dashboard, task list, task detail,
settings, login. Use blue primary color. Sidebar layout for logged-in pages.
```

**Result:** Functional mockup with AI-chosen design decisions.

**More example prompts to try:**

```
Create a landing page for a SaaS product called "FlowSync" — hero section
with headline + CTA, 3 feature cards with icons, pricing table (3 tiers),
testimonials section, footer with links. Style: clean like Linear, dark mode.
```

```
Build an admin dashboard for an e-commerce store. Pages: overview (revenue
chart placeholder, order stats, top products table), orders list (filterable
by status), customer list, settings. Sidebar nav. Light theme, green primary.
```

```
Create a portfolio website with 4 sections: hero with name + tagline,
projects grid (6 cards with thumbnails), about me, contact form. Single page,
top nav that scrolls to sections. Minimal, lots of whitespace, dark accent color.
```

### Tier 2: Design Brief (recommended)

Add structure to your description. Covers the major design decisions.

```markdown
## Project
Task manager for small teams.

## Pages
1. Dashboard — stats cards (total, in-progress, done, overdue) + recent activity feed
2. Tasks — filterable list (status, priority, assignee) + bulk actions
3. Task Detail — title, description, comments, attachments, status sidebar
4. Settings — profile, notifications, team members
5. Login — email/password, "forgot password" link, sign-up CTA

## Layout
- Login: standalone, centered card
- All others: sticky header + sidebar (240px) + main content

## Brand
- Primary: #2563EB (blue)
- Font: Inter or system-ui
- Style: clean, minimal, lots of whitespace

## Key Interactions
- Sidebar highlights current page
- Task list rows are clickable → navigate to detail
- Dashboard stats show change indicators (↑12%, ↓3%)
```

**Result:** Mockup matches your vision. Fewer revision rounds.

### Tier 3: Design Specs (best)

Full design specification from a UI/UX planning skill or design system skill.
This is what professional design handoffs look like.

```markdown
## Design Tokens

### Colors
--c-primary: #2563EB
--c-primary-hover: #1D4ED8
--c-primary-light: #DBEAFE
--c-secondary: #7C3AED
--c-success: #16A34A
--c-warning: #D97706
--c-danger: #DC2626

### Typography
Font: Inter, system-ui
Scale: 12/14/16/18/22/28/36px
Weights: 400 (body), 500 (labels), 600 (headings), 700 (hero)

### Spacing
Base: 4px grid
Scale: 4/8/12/16/20/24/32/40/48/64px

### Radius
sm: 4px, md: 8px, lg: 12px, xl: 16px, pill: 9999px

## Component Specs

### Button
- Primary: bg primary, white text, radius-md, padding 8px 16px
- Hover: bg primary-hover
- Sizes: sm (6px 12px, 12px font), default, lg (12px 24px, 14px font)

### Card
- Border: 1px gray-200, radius-lg, shadow-sm
- Header: border-bottom, flex space-between
- Body: padding 20px

### (... more components ...)

## Screen Specs

### Dashboard
- Header: sticky, 56px height, logo left, nav center, avatar right
- Below header: sidebar (240px) + main
- Main: 4-column stat cards grid, then 2-column (activity feed + chart placeholder)
- Stat card: label (sm, muted), value (2xl, bold), change badge

### (... more screens ...)
```

**Result:** Pixel-accurate mockup. Minimal iteration needed.

---

## Field Reference

If your skill outputs structured data, here's what pug-mockup can consume:

### Design Tokens (feeds → `main.css` `:root`)
| Field | Maps to | Example |
|---|---|---|
| Primary color + variants | `--c-primary`, `--c-primary-hover`, `--c-primary-light` | `#2563EB` |
| Semantic colors | `--c-success`, `--c-warning`, `--c-danger`, `--c-info` | `#16A34A` |
| Gray scale | `--c-gray-50` through `--c-gray-900` | Standard neutral scale |
| Font family | `--font-family` | `'Inter', system-ui` |
| Font size scale | `--fs-xs` through `--fs-3xl` | `12px` to `36px` |
| Font weights | `--fw-normal` through `--fw-bold` | `400/500/600/700` |
| Spacing scale | `--sp-1` through `--sp-16` | 4px grid multiples |
| Border radius | `--radius-sm` through `--radius-full` | `4px` to `9999px` |
| Shadows | `--shadow-sm` through `--shadow-xl` | Box-shadow values |
| Layout dimensions | `--sidebar-width`, `--header-height`, `--container-max` | `240px`, `56px`, `1200px` |

### Component Specs (feeds → CSS component sections + Pug mixins)
| Field | What it defines |
|---|---|
| Button variants | Which `.btn-*` classes to generate, colors, sizes |
| Card structure | Header/body/footer presence, padding, border style |
| Form elements | Input styles, label position, error states |
| Navigation | Header vs sidebar, items, active state behavior |
| Badge/tag styles | Colors, shapes, sizes for status indicators |
| Table style | Striped, hoverable, header style |
| Modal | Width, overlay color, animation |

### Screen Specs (feeds → Pug page files)
| Field | What it defines |
|---|---|
| Page name + ID | File name and `#page-[id]` for routing |
| Layout type | Standalone, sidebar+main, centered card |
| Sections (ordered) | What blocks appear and in what order |
| Grid layout | Column count, gap, responsive behavior |
| Content hints | What data/text appears in each section |
| Public vs authenticated | Which header/sidebar variant to use |

---

## For Skill Builders

If you're building a companion skill that feeds into pug-mockup:

1. **Output markdown** — pug-mockup reads `.md` files
2. **Use the token names above** — AI maps them directly to CSS variables
3. **Be specific about values** — `#2563EB` not "a nice blue"
4. **Include screen specs** — which pages, what layout, what sections
5. **Don't worry about Pug syntax** — your output is design intent, not code

The more structured your output, the less the AI guesses.
The less the AI guesses, the fewer revision rounds.
