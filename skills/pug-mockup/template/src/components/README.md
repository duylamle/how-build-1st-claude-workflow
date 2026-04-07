# Components

Shared UI elements used across multiple pages. Write them as **Pug mixins**
so you edit once and every page updates automatically.

## How to Create a Component

1. Create a `.pug` file here (e.g., `header.pug`, `sidebar.pug`)
2. Define a mixin inside
3. Include it in `index.pug` (before pages that use it)
4. Use it in any page with `+mixinName(args)`

```pug
//- Step 2: components/header.pug
mixin header(activePage)
  header.header
    a.logo(href="#home") My App
    nav
      a(href="#home" class={active: activePage === 'home'}) Home
      a(href="#about" class={active: activePage === 'about'}) About

//- Step 3: index.pug
include components/header.pug    //- ← before page includes
include pages/home.pug

//- Step 4: pages/home.pug
.page#page-home
  +header('home')
  main
    h1 Welcome
```

---

## Starter Components

This folder includes 3 ready-to-use components. Edit or replace them:

| File | Mixin | Usage |
|---|---|---|
| `header.pug` | `+header('pageName')` | Top nav bar with logo, links, CTA |
| `sidebar.pug` | `+sidebar('pageName')` | Vertical sidebar nav with sections |
| `footer.pug` | `+footer()` | Simple footer |

---

## Mixin Pattern Reference

Find the situation that matches what you're building → use that pattern.

---

### "I need the same element on every page" → Basic mixin

**When:** Footer, copyright, branding — identical everywhere.

```pug
mixin footer()
  footer.footer
    | © 2026 My App. All rights reserved.

+footer()
```

---

### "Same element, but with style/size variants" → Parameters with defaults

**When:** Buttons (primary/outline/danger), badges, alerts — same structure, different look.

```pug
mixin btn(text, href, variant='primary')
  a(href=href class='btn btn-' + variant)= text

+btn('Sign Up', '#register')              //- primary (default)
+btn('Learn More', '#about', 'outline')   //- outline
+btn('Delete', '#', 'danger')             //- danger
```

---

### "Navigation needs to highlight the current page" → Active state parameter

**When:** Header nav, sidebar, tab bar — one item is active, rest are normal.

```pug
mixin sidebar(activePage)
  aside.sidebar
    nav
      each item in ['dashboard', 'tasks', 'settings']
        a(href='#' + item class={active: activePage === item})= item

+sidebar('dashboard')    //- "dashboard" highlighted
+sidebar('tasks')        //- "tasks" highlighted
```

---

### "Wrapper that accepts any content inside" → Block (slot)

**When:** Cards, sections, panels — consistent outer frame, different inner content per use.

```pug
mixin card(title)
  .card
    .card-header
      h3= title
    .card-body
      if block
        block              //- ← your content goes here
      else
        p No content        //- ← fallback

+card('Monthly Revenue')
  .stat-value $42,000
  .stat-change.up ↑ 12%

+card('Coming Soon')       //- shows fallback
```

---

### "Render a list of items from data" → Data-driven with `each`

**When:** Product grids, user lists, activity feeds — same card repeated N times with different data.

```pug
mixin productGrid(products)
  .grid.grid-3.gap-4
    each p in products
      .card
        .card-body
          h4= p.name
          p.text-muted= p.description
          .flex.items-center.justify-between.mt-4
            span.stat-value= p.price
            a.btn.btn-sm.btn-primary(href='#product-' + p.id) View

-
  var products = [
    {id: 1, name: 'Starter', price: '$9/mo', description: 'For individuals'},
    {id: 2, name: 'Pro', price: '$29/mo', description: 'For small teams'},
    {id: 3, name: 'Enterprise', price: 'Custom', description: 'For organizations'}
  ]
+productGrid(products)
```

---

### "Show/hide sections based on context" → Conditional parameters

**When:** Page headers with optional subtitle/action, cards with optional footer.

```pug
mixin pageHeader(title, subtitle, showAction)
  .flex.items-center.justify-between.mb-6
    .flex-col
      h2= title
      if subtitle
        p.text-muted= subtitle
    if showAction
      a.btn.btn-primary(href="#") + New

+pageHeader('Dashboard', 'Overview of your tasks', true)
+pageHeader('Login', null, false)
```

---

### "Public and logged-in users see different UI" → Dual variant

**When:** App has public pages (landing, login) and authenticated pages (dashboard) with different headers.

```pug
mixin headerPublic(activePage)
  header.header#header-public
    a.logo(href="#home") My App
    nav
      a(href="#home" class={active: activePage === 'home'}) Home
      a(href="#pricing" class={active: activePage === 'pricing'}) Pricing
    a.btn.btn-primary.btn-sm(href="#login") Sign In

mixin headerLogged()
  header.header#header-logged
    a.logo(href="#dashboard") My App
    nav
      a(href="#dashboard") Dashboard
      a(href="#tasks") Tasks
    .avatar JD

//- JS router toggles which one is visible
+headerPublic('home')       //- public pages
+headerLogged()             //- logged-in pages
```

---

### "Sidebar items need icons" → Lucide SVG inline

**When:** Sidebar or nav items with icons from [lucide.dev](https://lucide.dev).

```pug
mixin sidebarItem(href, label, activePage, svgPath)
  a(href=href class={active: activePage === label.toLowerCase()})
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">!{svgPath}</svg>
    span= label

+sidebarItem('#dashboard', 'Dashboard', activePage, '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/>')
```

---

### "Confirm before destructive action" → Modal

**When:** Delete confirmation, unsaved changes warning, any action that needs explicit user consent.

```pug
mixin modal(id, title)
  .modal-overlay(id=id)
    .modal
      .modal-header
        h3= title
        button.btn.btn-ghost.modal-close ✕
      .modal-body
        if block
          block
      .modal-footer
        button.btn.btn-secondary.modal-close Cancel
        button.btn.btn-primary Confirm

+modal('delete-modal', 'Confirm Delete')
  p Are you sure? This action cannot be undone.

//- Open from JS: document.getElementById('delete-modal').classList.add('active')
```

---

### "Show feedback after an action" → Toast

**When:** "Saved!", "Error!", "Item deleted" — temporary notification.

```pug
mixin toast()
  #toast.toast

//- Include once in index.pug. Trigger from JS:
//- showToast('Saved!', 'success')
//- showToast('Failed to save', 'error')
```

---

### "Pass extra HTML attributes I didn't plan for" → &attributes

**When:** Reusable link/button that sometimes needs `target="_blank"`, `id`, or extra classes.

```pug
mixin link(href, text)
  a(href=href)&attributes(attributes)= text

+link('/about', 'About')(class="nav-link" target="_blank")
+link('/help', 'Help')(class="footer-link" id="help-link")
```

---

### "Variable number of items" → Rest arguments

**When:** Menu items, tag lists, breadcrumbs — different count each time.

```pug
mixin list(id, ...items)
  ul(id=id)
    each item in items
      li= item

+list('main-menu', 'Home', 'About', 'Contact', 'Blog')
+list('footer-links', 'Terms', 'Privacy')
```

---

## Quick Decision Guide

| I need to... | Pattern | Key feature |
|---|---|---|
| Reuse identical element | Basic | No parameters |
| Same structure, different style | Parameters | Default values |
| Highlight current page | Active state | `class={active: cond}` |
| Consistent frame, custom content | Block (slot) | `if block` / `block` |
| Render list from data | Data-driven | `each` + mixin |
| Show/hide parts conditionally | Conditional | `if param` |
| Different UI for different users | Dual variant | Two mixins + JS toggle |
| Icons in nav items | Lucide SVG | Raw SVG inline |
| Confirm before action | Modal | Overlay + dialog |
| Temporary feedback | Toast | Fixed position + JS |
| Pass-through attributes | &attributes | `&attributes(attributes)` |
| Variable-length input | Rest args | `...items` |

**Rule of thumb:** if you copy-paste something between pages, it should be a mixin.
