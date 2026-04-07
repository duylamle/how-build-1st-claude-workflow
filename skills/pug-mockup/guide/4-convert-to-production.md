# Converting Pug Mockup to Production Code

> Your mockup is approved. Now what? This guide covers the **general principles**
> for converting to any production framework. The patterns are the same whether
> you're targeting React, Vue, Svelte, Angular, or anything else.

---

## What Transfers (~60-70%)

| From Mockup | → Production | How |
|---|---|---|
| Design tokens (`:root` vars) | Framework theme / config | Copy values directly |
| Page structure | Routes / pages | Same sections, same hierarchy |
| Component breakdown | Framework components | Each mixin → one component |
| Layout patterns | Layout components | Same sidebar+main, header, grid |
| Mock data shape | API response shape | Same field names guide your API design |
| CSS classes + styles | Global CSS or scoped styles | Copy or convert to utility classes |

## What You Write Fresh

| Concern | Why it can't transfer |
|---|---|
| Authentication | Mockup fakes login — production needs real auth |
| API / data fetching | Mockup uses hardcoded vars — production calls real endpoints |
| Form validation | Mockup shows error UI — production validates for real |
| Error handling | Network errors, 404s, edge cases |
| State management | Mockup is stateless — production needs store/context |
| Routing | Hash router → framework router (history, guards, params) |
| Testing | Unit, integration, e2e |

---

## 5 Conversion Steps (Any Framework)

### Step 1: Transfer design tokens

Your `main.css` `:root` block is a portable design system. Copy the values into
whatever your framework uses — Tailwind config, CSS variables, theme object, SCSS vars.

```
--c-primary: #2563EB        →  primary: '#2563EB'  (or keep as CSS var)
--radius-md: 8px            →  borderRadius.md: '8px'
--shadow-md: 0 2px 8px ...  →  boxShadow.md: '0 2px 8px ...'
```

The token **names** may change. The **values** stay identical.

### Step 2: Convert mixins → components

Every Pug mixin maps to one component. The conversion pattern is always the same:

| Pug concept | → Framework concept |
|---|---|
| Mixin name | Component name |
| Mixin parameters | Component props |
| `block` (slot content) | Children / slot |
| `each` loop | Framework loop syntax |
| `if/else` | Framework conditional syntax |
| `class={active: cond}` | Dynamic class binding |
| `&attributes` | Prop spreading |

**Example — sidebar mixin → generic component:**

```pug
//- PUG (before)
mixin sidebar(activePage)
  aside.sidebar
    nav
      each item in ['dashboard', 'tasks', 'settings']
        a(href='#' + item class={active: activePage === item})= item
```

This becomes a component that:
- Accepts `activePage` as a prop
- Loops through items
- Applies `.active` class conditionally
- Renders `<aside>` with `<nav>` inside

The HTML structure stays the same. Only the template syntax changes per framework.

### Step 3: Convert pages → routes

Each `.page#page-[name]` becomes a route/page in your framework:

```
pages/home.pug       →  /           (home route)
pages/dashboard.pug  →  /dashboard  (dashboard route)
pages/login.pug      →  /login      (login route)
```

Inside each page:
- Import the components it uses (header, sidebar, footer)
- Keep the same section structure and order
- Replace hardcoded data with props / API calls

### Step 4: Replace mock data → real data

Mockup data tells you the **shape** your API needs to return:

```pug
//- Mockup — this IS your API contract
-
  var tasks = [
    {id: 1, title: 'Design homepage', status: 'done', priority: 'high'},
    {id: 2, title: 'Write API docs', status: 'in-progress', priority: 'medium'}
  ]
```

Production: fetch from API, same field names:
```
GET /api/tasks → [{ id, title, status, priority }, ...]
```

The mockup data structure becomes your API spec.

### Step 5: Replace Lucide SVG → icon package

```
//- Mockup: raw SVG inline
<svg width="18" height="18" viewBox="0 0 24 24" ...><rect .../></svg>

//- Production: import from lucide-[framework]
import { LayoutDashboard } from 'lucide-react'   // or lucide-vue, etc.
<LayoutDashboard size={18} />
```

All major frameworks have a Lucide package: `lucide-react`, `lucide-vue-next`,
`lucide-svelte`, `lucide-angular`.

---

## Syntax Quick Reference

This table shows how the same concept looks in Pug vs common frameworks.
Use it as a cheat sheet during conversion:

### React (JSX) / Next.js

| Pug | React JSX |
|---|---|
| `.card` | `<div className="card">` |
| `h1= title` | `<h1>{title}</h1>` |
| `each item in items` | `{items.map(i => <X key={i.id} />)}` |
| `if show` | `{show && <X/>}` |
| `class={active: cond}` | `className={cond ? 'active' : ''}` |
| `+sidebar('x')` | `<Sidebar active="x" />` |
| `include file.pug` | `import X from './X'` |
| `block` | `{children}` |

### Vue / Nuxt

| Pug | Vue template |
|---|---|
| `.card` | `<div class="card">` |
| `h1= title` | `<h1>{{ title }}</h1>` |
| `each item in items` | `<div v-for="i in items" :key="i.id">` |
| `if show` | `<div v-if="show">` |
| `class={active: cond}` | `:class="{ active: cond }"` |
| `+sidebar('x')` | `<Sidebar active="x" />` |
| `include file.pug` | `import X from './X.vue'` |
| `block` | `<slot />` |

**Vue bonus:** supports Pug natively (`<template lang="pug">`) — skip template conversion entirely.

### Svelte / SvelteKit

| Pug | Svelte |
|---|---|
| `.card` | `<div class="card">` |
| `h1= title` | `<h1>{title}</h1>` |
| `each item in items` | `{#each items as i (i.id)}` |
| `if show` | `{#if show}` |
| `class={active: cond}` | `class:active={cond}` |
| `+sidebar('x')` | `<Sidebar active="x" />` |
| `include file.pug` | `import X from './X.svelte'` |
| `block` | `<slot />` |

### Angular

| Pug | Angular template |
|---|---|
| `.card` | `<div class="card">` |
| `h1= title` | `<h1>{{ title }}</h1>` |
| `each item in items` | `<div *ngFor="let i of items">` |
| `if show` | `<div *ngIf="show">` |
| `class={active: cond}` | `[class.active]="cond"` |
| `+sidebar('x')` | `<app-sidebar [active]="'x'" />` |
| `include file.pug` | `import` + declare in module |
| `block` | `<ng-content />` |

### Plain HTML / Vanilla JS

| Pug | HTML + JS |
|---|---|
| `.card` | `<div class="card"></div>` |
| `h1= title` | `<h1 id="title"></h1>` + `el.textContent = title` |
| `each item in items` | `items.forEach(i => container.innerHTML += ...)` |
| `if show` | `el.style.display = show ? '' : 'none'` |
| `class={active: cond}` | `el.classList.toggle('active', cond)` |
| `include file.pug` | Copy-paste (no component system) |
| `block` | N/A |

This is what the Pug mockup already compiles to — `dist/index.html` is plain HTML + vanilla JS.

---

## Conversion Checklist

### Structure
- [ ] Create project with framework CLI
- [ ] Transfer design tokens to framework config / global CSS
- [ ] Create layout component (header + sidebar + main)
- [ ] Create route for each page from mockup

### Components (for each mixin)
- [ ] Create component file
- [ ] Mixin parameters → props
- [ ] `block` → slot / children
- [ ] `each` → framework loop
- [ ] `if/else` → framework conditional
- [ ] Lucide SVG inline → icon package import

### Pages (for each page)
- [ ] Create page / route file
- [ ] Import and use components
- [ ] Hardcoded data → API fetch / store
- [ ] Add loading states (skeleton / spinner)
- [ ] Add error states
- [ ] Add empty states

### Write Fresh
- [ ] Authentication
- [ ] API routes / data fetching
- [ ] Form validation (real, not just UI)
- [ ] Error boundaries / global error handling
- [ ] SEO (meta tags, open graph)
- [ ] Tests

---

## Key Principle

The mockup is a **visual contract** — it defines what the user sees and how
they interact. Production code implements that contract with real data, real
auth, and real error handling. The closer your production output matches the
mockup HTML, the better your conversion went.
