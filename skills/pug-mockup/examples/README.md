# Examples

## demo-project/

A complete 5-page mockup built from the starter template. Shows how components,
pages, and routing work together. Open `demo.html` in any browser — no install needed.

**Pages:**
| Page | Route | Layout | Demonstrates |
|---|---|---|---|
| Home | `#home` | Public header + hero | Landing page, feature grid, footer |
| Dashboard | `#dashboard` | Logged header + sidebar | Stat cards, activity feed (data-driven) |
| Tasks | `#tasks` | Logged header + sidebar | Filter bar, tabs, data table with badges |
| Settings | `#settings` | Logged header + sidebar | Forms, tabs, danger zone |
| Login | `#login` | Standalone centered | Login form, links, divider |

**Components used:**
| File | Mixin | Pattern shown |
|---|---|---|
| `header.pug` | `+headerPublic()`, `+headerLogged()` | Dual variant — JS toggles visibility |
| `sidebar.pug` | `+sidebar('page')` | Active state, sections, Lucide icons |
| `footer.pug` | `+footer()` | Simple mixin |

**Structure:**
```
demo-project/
├── demo.html             ← open this! (compiled, self-contained)
├── CLAUDE.md             ← project map
├── package.json
├── .gitignore
├── dist/                 ← build output
│   ├── index.html
│   └── assets/
└── src/
    ├── index.pug         ← includes components + 5 pages
    ├── components/
    │   ├── header.pug    ← public + logged headers
    │   ├── sidebar.pug   ← nav with icons + sections
    │   └── footer.pug
    ├── pages/
    │   ├── home.pug      ← landing (hero + cards)
    │   ├── dashboard.pug ← stats + activity feed
    │   ├── tasks.pug     ← filters + table
    │   ├── settings.pug  ← form + danger zone
    │   └── login.pug     ← centered card form
    ├── css/main.css
    └── js/main.js        ← router (public vs logged)
```

**To rebuild after editing:**
```bash
cd demo-project
npm install
npm run build        # → outputs dist/index.html
```
