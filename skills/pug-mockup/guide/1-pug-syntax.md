# Pug Syntax Guide

> Comprehensive Pug reference for AI-generated SPA mockups.
> Generic patterns + examples — works for landing pages, portals, dashboards, e-commerce, etc.
> Source: [pugjs.org](https://pugjs.org/api/getting-started.html)

---

## Why Pug?

| Criteria | Plain HTML | Pug |
|---|---|---|
| **Component reuse** | Copy-paste | Mixin + include — edit once, apply everywhere |
| **Data-driven** | Manual duplication | `each` loop — 1 template renders N items |
| **Maintainability** | 1 giant file | Split into components + pages, easy to find/edit |
| **Output** | The source file itself | Compiles to 1 self-contained HTML |
| **Syntax** | Verbose (`<div class="foo">`) | Concise (`.foo`) |
| **Production path** | Is the production code | ~60-70% reusable in React/Next.js (CSS, structure, logic) |

**When to use:** mockup 5-30 pages, demo flows for stakeholders, interactive prototypes (cart, form, navigation).
**When not to use:** 100+ pages, real API/auth needed → use a production framework (Next.js, etc.).

---

## 1. Prerequisites

- **pug-cli** installed globally: `npm install -g pug-cli`
- Check: `pug --version`
- Alternative: use `npx pug-cli` without global install
- Pug docs: [pugjs.org](https://pugjs.org/api/getting-started.html)

---

## 2. Project Structure

```
project/
├── src/
│   ├── index.pug         ← entry point, includes all
│   ├── components/       ← shared (mixins, includes)
│   ├── pages/            ← 1 file per page
│   ├── css/main.css      ← design tokens + styles
│   └── js/main.js        ← router + interactive logic
└── dist/
    ├── index.html        ← compiled output
    └── assets/           ← images, icons, fonts
```

---

## 3. Build

```bash
pug src/index.pug -o dist -P        # build (pretty print)
pug src/index.pug -o dist -P -w     # watch mode
```

Output is self-contained — copy `dist/` and it runs anywhere.

---

## 4. Pug Language Reference

### Tags, Classes, IDs

```pug
h1.title#main Hello                  //- <h1 class="title" id="main">Hello</h1>
.container                           //- <div class="container"></div>
a.btn.btn-primary(href="#") Click    //- <a class="btn btn-primary" href="#">Click</a>
img(src="photo.png" alt="Photo")     //- self-closing tag
a: img(src="logo.png")              //- block expansion: <a><img></a>
```

### Attributes

```pug
input(type="text" placeholder="Name" required)
a(href=url)= linkText                //- JS expression
button(class={active: isActive})     //- conditional class (object)
a(style={color: 'red'})             //- style object
div&attributes({id: 'foo'})         //- spread attributes
input(type='checkbox' checked)       //- boolean attribute
```

### Text Content

```pug
p Inline text                        //- text on the same line as tag
p
  | Piped text — multiline           //- use | for each line
  | or mix text with inline tags
p.
  Block text — dot after tag         //- for large blocks (script, style)
  Everything indented below is plain text
```

### Interpolation

```pug
p Hello #{userName}                  //- string (escaped)
p!= '<strong>Bold</strong>'          //- unescaped (raw HTML)
p This is #[strong bold] and #[a(href="#") a link]  //- tag interpolation
p Line 1#[br]Line 2                  //- inline break
```

### Conditionals

```pug
if user.isLoggedIn
  p Welcome #{user.name}
else if user.isGuest
  p Welcome guest
else
  a(href="#login") Sign in

unless user.isAnonymous
  p Signed in
```

### Iteration

```pug
//- Array
each item in ['A', 'B', 'C']
  li= item

//- Array + index
each product, i in products
  .card(data-index=i)
    h3= product.name
    p= product.price

//- Object
each val, key in {name: 'John', role: 'PM'}
  .row
    span.label= key
    span.value= val

//- Fallback when empty
each item in []
  li= item
else
  li No data available
```

**Usage:** instead of copy-pasting N cards, declare a data array + `each` loop.

### Case (switch)

```pug
case status
  when 'success': span.badge-success Done
  when 'pending': span.badge-pending In progress
  default: span Unknown
```

### Code (JS in templates)

```pug
- var title = 'Home'                  //- unbuffered: declare variable
p= title                             //- buffered: output escaped
p!= '<em>Raw</em>'                   //- unescaped: output raw

-
  var products = [
    {name: 'A', price: 9600},
    {name: 'B', price: 19200}
  ]
```

### Comments

```pug
// Visible in HTML output
//- Only in Pug source (not rendered)
```

### Include

```pug
//- Include Pug file
include components/header.pug
include pages/home.pug

//- Include plain text (CSS, JS) — self-contained output
style
  include css/main.css
script
  include js/main.js
```

### Mixin

```pug
//- Basic
mixin btn(text, href, variant='primary')
  a(href=href class='btn btn-' + variant)= text

+btn('Sign Up', '#register')
+btn('Learn More', '#about', 'outline')

//- Block content (slot)
mixin card(title)
  .card
    h3= title
    if block
      block
    else
      p No content

+card('Product A')
  p Product description here

//- &attributes (pass-through)
mixin link(href, text)
  a(href=href)&attributes(attributes)= text

+link('/about', 'About')(class="nav-link")

//- Rest arguments
mixin list(id, ...items)
  ul(id=id)
    each item in items
      li= item

+list('menu', 'Home', 'About', 'Contact')
```

### Extends / Block (Template Inheritance)

```pug
//- layout.pug
html
  head
    title= pageTitle
    block head
  body
    block content
    block footer
      footer Default footer

//- page.pug
extends layout.pug
block content
  h1= pageTitle

//- Append/prepend
extends layout.pug
append head
  script(src="extra.js")
```

Use `extends` for multi-file output. For SPA single-file → `include` is sufficient.

### Raw HTML

```pug
//- SVG inline on a single line
span.icon
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/></svg>
```

### Whitespace Control

```pug
//- Tag interpolation preserves whitespace
p Hello #[strong World], welcome!

//- Pipe + empty line creates space
| Text
|
button Click

//- Block text
script.
  console.log('Hello')
```

---

## 5. SPA Hash Router

All pages live in a single HTML. URL `#hash` → JS toggles `.active` class.

### Basic

```js
var pages = ['home', 'about', 'contact'];

function navigate() {
  var hash = location.hash.replace('#','') || 'home';
  if (pages.indexOf(hash) === -1) hash = 'home';

  document.querySelectorAll('.page').forEach(function(p) {
    p.classList.remove('active');
  });

  var target = document.getElementById('page-' + hash);
  if (target) target.classList.add('active');

  window.scrollTo(0, 0);
}

window.addEventListener('hashchange', navigate);
window.addEventListener('DOMContentLoaded', navigate);
```

### Extended — public vs authenticated

```js
var publicPages = ['home', 'login', 'register'];
var loggedPages = ['dashboard', 'settings'];

function navigate() {
  // ... show/hide pages ...
  var isPublic = publicPages.indexOf(hash) !== -1;
  document.getElementById('header-public').className = isPublic ? 'active' : '';
  document.getElementById('header-logged').className = isPublic ? '' : 'active';
}
```

---

## 6. Component Patterns

### Mixin with conditional class

```pug
mixin sidebar(activePage)
  aside.sidebar
    nav
      a(href="#home" class={active: activePage === 'home'}) Home
      a(href="#settings" class={active: activePage === 'settings'}) Settings
```

### Data-driven (each + mixin)

```pug
mixin productCard(p)
  .card(data-id=p.id data-price=p.price)
    img(src=p.img)
    h3= p.name
    span.price= p.price

- var products = [{id: 1, name: 'Widget', price: '$50', img: 'widget.png'}]
each product in products
  +productCard(product)
```

---

## 7. Layout Patterns

### Single layout (landing page)

```pug
.page#page-home
  section.hero ...
  section.features ...
  +footer()
```

### Multi-layout (portal — public + sidebar)

```pug
//- Public
.page#page-home
  section ...
  +footer()

//- Authenticated
.page#page-dashboard
  .page-layout
    +sidebar('dashboard')
    main.main-content ...
```

### Dual pages (same content, different layout)

```pug
.page#page-blog          //- public, standalone
.page#page-blog-logged   //- portal, with sidebar
```

---

## 8. Interactive Patterns (JS)

### Event delegation

```js
document.addEventListener('click', function(e) {
  if (e.target.closest('.btn-add')) {
    var card = e.target.closest('[data-id]');
    // handle click
  }
});
```

### Data attributes + dynamic render

```pug
.product(data-id="123" data-price="50000")
```

```js
function formatCurrency(n) {
  return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}
```

---

## 9. Mockup → Production Transition

Pug mockup is a **reference to build on**, not a 1:1 conversion target.

| From Pug | To Next.js/React | How |
|---|---|---|
| `main.css` | Tailwind config + CSS modules | Copy token values |
| HTML structure | JSX | Change syntax, keep structure |
| Mixin | React component | `+sidebar('x')` → `<Sidebar active="x" />` |
| JS logic | React hooks | Wrap in `useState`/`useEffect` |
| Assets | `public/` | Copy directly |
| Lucide SVG inline | `lucide-react` | `<Search size={18} />` |

**Write fresh in production:** auth, API routes, form validation, error handling, data fetching.

---

## 10. Gotchas

- **SVG inline:** raw HTML on a single line, or wrap in `span`
- **Sticky:** `position: sticky` on wrapper div, not child
- **Overlay:** `position: relative` container + `absolute` content
- **Whitespace:** use `#[tag]` interpolation instead of `|` pipes
- **Boolean attributes:** `input(checked)` → with `doctype html` renders terse `<input checked>`
- **Class conditional:** `class={active: cond}` instead of `class=(cond ? 'active' : '')`

---

## References

- [Pug official docs](https://pugjs.org/api/getting-started.html)
- [Pug language reference](https://pugjs.org/language/tags.html)
- [Lucide icons](https://lucide.dev) — copy SVG for inline use
