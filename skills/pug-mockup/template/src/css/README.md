# CSS Guide — How to Customize main.css

> This guide explains the design system in `template/src/css/main.css`.
> Customize tokens to match your brand, then use the ready-made components.

---

## 1. Design Tokens — Where to Start

Open `main.css` and edit the `:root` block. Everything else references these tokens.

### Colors

```css
/* Primary — your brand color. Used by buttons, links, active states, badges */
--c-primary: #2563EB;          /* ← change this to your brand color */
--c-primary-hover: #1D4ED8;    /* ← slightly darker for hover */
--c-primary-light: #DBEAFE;    /* ← very light tint for backgrounds */
```

**How to pick colors:**
- Start with 1 primary color (your brand)
- Generate hover (10% darker) and light (90% lighter) variants
- Tools: [Tailwind color palette](https://tailwindcss.com/docs/customizing-colors), [Coolors](https://coolors.co)

**Semantic colors** — don't change unless you have a reason:
```css
--c-success: #16A34A;     /* green — confirmations, positive changes */
--c-warning: #D97706;     /* amber — caution states */
--c-danger: #DC2626;      /* red — errors, destructive actions */
--c-info: #0891B2;        /* cyan — informational notices */
```

Each semantic color has a `-light` variant for badge/tag backgrounds.

### Typography

```css
--font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
```

To use a custom font (e.g., Google Fonts Inter):
```css
/* Add to <head> in index.pug: */
/* link(href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet") */
--font-family: 'Inter', system-ui, sans-serif;
```

**Font size scale** (based on 14px root):
| Token | Size | Use for |
|---|---|---|
| `--fs-xs` | 12px | Captions, timestamps, fine print |
| `--fs-sm` | ~12px | Labels, nav items, secondary text |
| `--fs-base` | 14px | Body text (default) |
| `--fs-md` | 16px | Card titles, emphasized text |
| `--fs-lg` | 18px | Section headings, large labels |
| `--fs-xl` | 22px | Page subtitles, h3 |
| `--fs-2xl` | 28px | Page titles, h2 |
| `--fs-3xl` | 36px | Hero headlines, h1 |

### Spacing

Based on a **4px grid**. Use these for padding, margin, gap:

| Token | Value | Common use |
|---|---|---|
| `--sp-1` | 4px | Tight gaps (badge padding, icon spacing) |
| `--sp-2` | 8px | Button padding, small gaps |
| `--sp-3` | 12px | Form input padding, list item spacing |
| `--sp-4` | 16px | Card padding, section gaps |
| `--sp-6` | 24px | Page padding, large gaps |
| `--sp-8` | 32px | Section spacing |
| `--sp-12` | 48px | Major section breaks |
| `--sp-16` | 64px | Hero padding, page-level spacing |

### Shadows

| Token | Effect | Use for |
|---|---|---|
| `--shadow-sm` | Subtle | Cards at rest, list items |
| `--shadow-md` | Standard | Cards on hover, dropdowns |
| `--shadow-lg` | Prominent | Modals, floating elements |
| `--shadow-xl` | Heavy | Dialogs, overlays |

### Layout

```css
--sidebar-width: 240px;       /* sidebar nav width */
--header-height: 56px;        /* top header bar */
--container-max: 1200px;      /* max content width */
--container-narrow: 720px;    /* for text-heavy pages (blog, settings) */
```

---

## 2. I Need To... → Use This

Find what you're building → grab the Pug code.

---

### "I need a top navigation bar"

```pug
header.header
  a.logo(href="#home") MyApp
  nav
    a(href="#home" class={active: page === 'home'}) Home
    a(href="#about") About
  a.btn.btn-primary.btn-sm(href="#signup") Sign Up
```

---

### "I need a sidebar for dashboard pages"

```pug
.page-layout
  aside.sidebar
    .sidebar-section
      .sidebar-section-title Menu
      nav
        a.active(href="#dashboard") Dashboard
        a(href="#tasks") Tasks
        a(href="#settings") Settings
  main.main-content
    h2 Dashboard
    //- page content here
```

---

### "I need action buttons"

```pug
//- Pick the right variant for the action:
a.btn.btn-primary(href="#") Save Changes       //- main action
a.btn.btn-secondary(href="#") Cancel            //- secondary/alternative
a.btn.btn-outline(href="#") Learn More          //- soft emphasis
a.btn.btn-ghost(href="#") Skip                  //- minimal, text-like
a.btn.btn-danger(href="#") Delete Account       //- destructive action

//- Sizes:
a.btn.btn-sm.btn-primary(href="#") Small        //- compact (table rows, cards)
a.btn.btn-lg.btn-primary(href="#") Large        //- prominent (hero CTA)
```

---

### "I need to show content in a card"

```pug
//- Simple card
.card
  .card-body
    h4 Title
    p Content here.

//- Full card (header + body + footer)
.card
  .card-header
    h3 Card Title
    a.btn.btn-sm.btn-ghost(href="#") View All
  .card-body
    p Card content goes here.
  .card-footer
    span.text-sm.text-muted Updated 2 hours ago

//- Stat card (dashboard numbers)
.card.stat-card
  .stat-label Total Tasks
  .stat-value 142
  .stat-change.up ↑ 12% this week
```

---

### "I need status indicators / tags"

```pug
//- Match color to meaning:
span.badge.badge-success Completed      //- positive outcome
span.badge.badge-warning Pending        //- needs attention
span.badge.badge-danger Failed          //- error / critical
span.badge.badge-info New              //- informational
span.badge.badge-primary Active        //- current / selected
span.badge.badge-gray Draft            //- neutral / inactive
```

---

### "I need a form"

```pug
//- Text input with label + hint
.form-group
  label.form-label(for="email") Email
  input.form-input(type="email" id="email" placeholder="you@example.com")
  .form-hint We'll never share your email.

//- Dropdown select
.form-group
  label.form-label(for="role") Role
  select.form-select(id="role")
    option(value="") Select a role
    option(value="admin") Admin
    option(value="editor") Editor

//- Textarea
.form-group
  label.form-label(for="bio") Bio
  textarea.form-textarea(id="bio" rows="3") Your bio here.

//- Checkbox
.form-group
  label.form-check
    input(type="checkbox" checked)
    | I agree to the terms

//- Error state (validation failed)
.form-group
  label.form-label(for="name") Name
  input.form-input.error(type="text" id="name")
  .form-error Name is required.
```

---

### "I need a data table"

```pug
.table-wrapper
  table.table
    thead
      tr
        th Name
        th Status
        th Date
    tbody
      each item in items
        tr
          td= item.name
          td
            span.badge(class='badge-' + item.status)= item.status
          td.text-muted= item.date
```

---

### "I need a confirmation dialog"

```pug
.modal-overlay#modal-confirm
  .modal
    .modal-header
      h3 Confirm Delete
      button.btn.btn-ghost(onclick="closeModal()") ✕
    .modal-body
      p Are you sure? This action cannot be undone.
    .modal-footer
      button.btn.btn-secondary(onclick="closeModal()") Cancel
      button.btn.btn-danger Delete

//- Open: document.getElementById('modal-confirm').classList.add('active')
```

---

### "I need a landing page hero"

```pug
section.hero
  h1 Build Something Amazing
  p A brief description of your product and its value.
  .hero-actions
    a.btn.btn-primary.btn-lg(href="#signup") Get Started
    a.btn.btn-outline.btn-lg(href="#about") Learn More
```

---

### "I need tab navigation"

```pug
.tabs
  a.tab.active Overview
  a.tab Details
  a.tab Settings
```

---

### "I need a placeholder when there's no data"

```pug
.empty-state
  //- Lucide icon SVG here
  h3 No tasks yet
  p Create your first task to get started.
  a.btn.btn-primary(href="#") Create Task
```

---

### "I need user avatars"

```pug
.avatar JD                    //- default 32px
.avatar.avatar-sm JD          //- 24px (compact lists, tables)
.avatar.avatar-lg JD          //- 48px (profile, header)
```

---

### "I need to arrange elements side by side or in a grid"

```pug
//- Side by side (flex) — title left, button right
.flex.items-center.justify-between.gap-4
  h3 Title
  a.btn.btn-sm.btn-primary(href="#") Action

//- Grid — equal columns
.grid.grid-2.gap-4    //- 2 columns
.grid.grid-3.gap-4    //- 3 columns
.grid.grid-4.gap-4    //- 4 columns (stat cards)

//- Spacing utilities
.mt-4.mb-6.p-4        //- margin-top 16px, margin-bottom 24px, padding 16px

//- Text helpers
p.text-sm.text-muted Last updated 2 hours ago
p.text-center Centered text
```

---

## 3. Responsive Behavior

At **768px and below**, the CSS automatically:
- Stacks grid columns to single column
- Converts sidebar from vertical to horizontal scrollable nav
- Reduces hero padding
- Stacks hero action buttons vertically

No extra classes needed — it's built in.

---

## 4. Adding Custom Styles

Add project-specific styles **below** the existing sections in `main.css`.
Keep using tokens for consistency:

```css
/* ============================================================
   PROJECT-SPECIFIC: Product Cards
   ============================================================ */
.product-card {
  padding: var(--sp-4);
  border: 1px solid var(--c-gray-200);
  border-radius: var(--radius-lg);
  transition: box-shadow var(--transition-normal);
}
.product-card:hover {
  box-shadow: var(--shadow-lg);
}
.product-card .price {
  font-size: var(--fs-xl);
  font-weight: var(--fw-bold);
  color: var(--c-primary);
}
```

**Rule of thumb:** if you're typing a raw color value (`#3B82F6`) or pixel value (`16px`),
check if there's a token for it first. Tokens keep the design consistent.
