# Pages

Each page is a separate `.pug` file included in `index.pug`.
Pages use hash-based routing — URL `#about` shows the About page.

## How to Create a Page

1. Create a `.pug` file here (e.g., `home.pug`, `about.pug`)
2. Wrap content in a `.page` div with `id="page-[name]"`:

```pug
//- pages/home.pug
.page#page-home
  section.hero
    h1 Welcome to My App
    p A brief description of what this app does.
```

3. Include it in `index.pug`:

```pug
//- In index.pug, under "Pages"
include pages/home.pug
include pages/about.pug
```

4. Register the page ID in `js/main.js`:

```js
var pages = ['home', 'about'];  // add your page name here
```

5. Link to it from anywhere:

```pug
a(href="#about") About Us
```

## I Need a Page That... → Use This Layout

---

### "Landing page — hero, features, CTA, footer"

```pug
.page#page-home
  +headerPublic('home')
  section.hero
    h1 Headline
    p Subheadline
    .hero-actions
      a.btn.btn-primary.btn-lg(href="#signup") Get Started
  section.container.mt-8
    h2.text-center Features
    .grid.grid-3.gap-6
      .card
        .card-body
          h4 Feature
          p.text-muted Description
  +footer()
```

---

### "Dashboard — sidebar + stats + content"

```pug
.page#page-dashboard
  +headerLogged()
  .page-layout
    +sidebar('dashboard')
    main.main-content
      .flex.items-center.justify-between.mb-6
        h2 Dashboard
        a.btn.btn-primary(href="#") + New
      .grid.grid-4.gap-4.mb-6
        .card.stat-card
          .stat-label Total
          .stat-value 142
          .stat-change.up ↑ 12%
      .card
        .card-header
          h3 Recent Activity
        .card-body
          //- list items here
```

---

### "Data table page — filters + tabs + table"

```pug
.page#page-tasks
  +headerLogged()
  .page-layout
    +sidebar('tasks')
    main.main-content
      h2 Tasks
      //- Filters
      .flex.gap-3.mb-4
        select.form-select(style="width: 160px")
          option All Statuses
          option Active
          option Done
        input.form-input(type="text" placeholder="Search..." style="width: 240px")
      //- Tabs
      .tabs.mb-4
        a.tab.active All (42)
        a.tab Active (18)
      //- Table
      .card
        .table-wrapper
          table.table
            thead
              tr
                th Name
                th Status
            tbody
              each item in items
                tr
                  td= item.name
                  td
                    span.badge(class='badge-' + item.status)= item.status
```

---

### "Settings / profile — form with sections"

```pug
.page#page-settings
  +headerLogged()
  .page-layout
    +sidebar('settings')
    main.main-content
      h2 Settings
      .tabs.mb-6
        a.tab.active Profile
        a.tab Notifications
      .card
        .card-header
          h3 Profile Information
        .card-body
          .grid.grid-2.gap-4
            .form-group
              label.form-label First Name
              input.form-input(value="John")
            .form-group
              label.form-label Last Name
              input.form-input(value="Doe")
          .form-group
            label.form-label Email
            input.form-input(type="email" value="john@example.com")
        .card-footer
          .flex.justify-between
            span.text-sm.text-muted Last saved 3 days ago
            button.btn.btn-primary Save
```

---

### "Login / signup — centered card, no nav"

```pug
.page#page-login
  .flex.justify-center.items-center(style="min-height: 100vh; background: var(--c-gray-50)")
    .card(style="width: 380px")
      .card-body
        h3.text-center Welcome Back
        p.text-center.text-muted.mb-6 Sign in to your account
        .form-group
          label.form-label Email
          input.form-input(type="email" placeholder="you@example.com")
        .form-group
          label.form-label Password
          input.form-input(type="password" placeholder="••••••••")
        button.btn.btn-primary(style="width: 100%") Sign In
        .divider
        p.text-center.text-sm Don't have an account? #[a(href="#register" style="color: var(--c-primary)") Sign up]
```

---

### "Detail page — info panel + related content"

```pug
.page#page-detail
  +headerLogged()
  .page-layout
    +sidebar('tasks')
    main.main-content
      //- Back link
      a.text-sm.text-muted(href="#tasks") ← Back to Tasks
      h2.mt-4 Task Title Here
      .grid.grid-2.gap-6.mt-4
        //- Main content
        .flex-col.gap-4
          .card
            .card-body
              h4 Description
              p Task description goes here...
          .card
            .card-header
              h3 Comments
            .card-body
              .list-item
                .avatar JD
                .flex-col
                  p.text-sm Comment text here
                  p.text-xs.text-muted 2 hours ago
        //- Side panel
        .card(style="height: fit-content")
          .card-body
            .form-group
              label.form-label.text-xs Status
              span.badge.badge-info In Progress
            .form-group
              label.form-label.text-xs Priority
              span.badge.badge-danger High
            .form-group
              label.form-label.text-xs Assignee
              .flex.items-center.gap-2
                .avatar.avatar-sm JD
                span.text-sm John Doe
```

---

### "Empty / error page"

```pug
.page#page-empty
  +headerLogged()
  .page-layout
    +sidebar('reports')
    main.main-content
      .empty-state
        h3 No reports yet
        p Generate your first report to see data here.
        a.btn.btn-primary(href="#") Generate Report
```

---

Don't forget to register each new page in `main.js` — see `js/README.md`.
