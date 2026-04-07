# JavaScript — SPA Router & Interactive Logic

> This folder contains `main.js` — the SPA hash router and interactive logic.
> It gets inlined into the HTML via Pug `include`.

---

## How the Router Works

All pages live in a single HTML file. The router shows/hides pages based on `#hash` in the URL.

```
URL: index.html#dashboard  →  shows #page-dashboard, hides all others
URL: index.html#login      →  shows #page-login, hides all others
URL: index.html             →  defaults to #page-home
```

### Basic Setup

```js
// 1. List all page IDs (without "page-" prefix)
var pages = ['home', 'about', 'contact'];

// 2. Navigate function — called on hash change
function navigate() {
  var hash = location.hash.replace('#','') || 'home';
  if (pages.indexOf(hash) === -1) hash = 'home';

  // Hide all, show target
  document.querySelectorAll('.page').forEach(function(p) {
    p.classList.remove('active');
  });
  document.getElementById('page-' + hash).classList.add('active');
  window.scrollTo(0, 0);
}

// 3. Listen for changes
window.addEventListener('hashchange', navigate);
window.addEventListener('DOMContentLoaded', navigate);
```

### Adding a New Page

1. Create the page file in `pages/` (see `pages/README.md`)
2. Add the page ID to the `pages` array in `main.js`:
   ```js
   var pages = ['home', 'about', 'contact', 'your-new-page'];
   ```
3. Link to it: `a(href="#your-new-page") Your Page`

---

## Public vs Authenticated Pages

For apps with login, split pages into two groups and toggle headers/sidebar:

```js
var publicPages = ['home', 'login', 'register'];
var loggedPages = ['dashboard', 'tasks', 'settings'];

function navigate() {
  var hash = location.hash.replace('#','') || 'home';
  // ... show/hide page ...

  // Toggle header variant
  var isPublic = publicPages.indexOf(hash) !== -1;
  document.getElementById('header-public').style.display = isPublic ? '' : 'none';
  document.getElementById('header-logged').style.display = isPublic ? 'none' : '';

  // Toggle sidebar (only on logged pages)
  var sidebar = document.querySelector('.sidebar');
  if (sidebar) sidebar.style.display = isPublic ? 'none' : '';
}
```

---

## I Need To... → Use This

---

### "I need tabs to switch content"

```js
document.addEventListener('click', function(e) {
  if (e.target.closest('.tab')) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    e.target.closest('.tab').classList.add('active');
  }
});
```

---

### "I need to open/close a modal"

```js
// Open — from a button with data-modal="modal-id"
document.addEventListener('click', function(e) {
  if (e.target.closest('[data-modal]')) {
    var id = e.target.closest('[data-modal]').dataset.modal;
    document.getElementById(id).classList.add('active');
  }
  // Close — click close button or overlay background
  if (e.target.closest('.modal-close') || e.target.classList.contains('modal-overlay')) {
    e.target.closest('.modal-overlay').classList.remove('active');
  }
});
```
```pug
//- Pug: button that opens modal
button.btn.btn-danger(data-modal="delete-modal") Delete
```

---

### "I need to show/hide a dropdown or section"

```js
function toggle(selector) {
  var el = document.querySelector(selector);
  el.style.display = el.style.display === 'none' ? '' : 'none';
}
```
```pug
//- Pug: toggle button
button.btn.btn-ghost(onclick="toggle('.dropdown-menu')") Menu
```

---

### "I need to handle clicks on dynamic/repeated items"

Use event delegation — one listener on `document` instead of one per element:

```js
document.addEventListener('click', function(e) {
  var btn = e.target.closest('.btn-add');
  if (btn) {
    var card = btn.closest('[data-id]');
    console.log('Added:', card.dataset.id);
  }
});
```
```pug
//- Pug: each card has data attributes for JS to read
each item in items
  .card(data-id=item.id)
    h4= item.name
    button.btn.btn-sm.btn-primary.btn-add Add
```

---

### "I need to show a temporary success/error message"

```js
function showToast(message, type) {
  var toast = document.getElementById('toast');
  toast.textContent = message;
  toast.className = 'toast active toast-' + (type || 'info');
  setTimeout(function() { toast.classList.remove('active'); }, 3000);
}
// showToast('Saved!', 'success')
// showToast('Something went wrong', 'error')
```
```pug
//- Pug: include toast container once in index.pug
#toast.toast
```

---

### "I need to format large numbers"

```js
function formatNumber(n) {
  return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}
// formatNumber(1234567) → "1,234,567"
```

---

### "I need to filter a list"

```js
function filterItems(status) {
  document.querySelectorAll('[data-status]').forEach(function(el) {
    el.style.display = (status === 'all' || el.dataset.status === status) ? '' : 'none';
  });
}
```
```pug
//- Pug: filter buttons + data-tagged rows
.flex.gap-2
  button.btn.btn-sm(onclick="filterItems('all')") All
  button.btn.btn-sm(onclick="filterItems('active')") Active
  button.btn.btn-sm(onclick="filterItems('done')") Done

each task in tasks
  .list-item(data-status=task.status)
    span= task.title
```

---

### "I need to count or update a number on click"

```js
document.addEventListener('click', function(e) {
  if (e.target.closest('.btn-like')) {
    var counter = e.target.closest('.btn-like').querySelector('.count');
    counter.textContent = parseInt(counter.textContent) + 1;
  }
});
```
```pug
button.btn.btn-ghost.btn-like ♥ #[span.count 0]
```

---

## Tips

- **Keep it simple** — this is a mockup, not production code. Fake the interactions
- **No frameworks** — vanilla JS only. No React, no jQuery
- **Data in Pug** — define mock data in `.pug` files with `- var data = [...]`, not in JS
- **Inline via include** — `main.js` gets inlined into HTML. No `<script src>` needed
