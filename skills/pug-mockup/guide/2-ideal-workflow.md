# Ideal Workflow — Getting the Best Out of Pug Mockup

> Pug-mockup is one piece of the puzzle. This guide shows the full picture:
> what comes before, what comes after, and which skills fill each gap.
> You don't need all of them — but knowing what's possible helps you
> decide what's worth investing in.

---

## The Full Picture

A great mockup isn't just code — it's the result of good decisions made
at every stage. Here's the ideal flow:

```
[1] DEFINE      →  [2] DESIGN      →  [3] BUILD       →  [4] REVIEW      →  [5] CONVERT
What to build      How it looks        Pug code          Quality check       Production
```

**Pug-mockup lives at stage 3.** The better your input from stages 1-2,
the fewer revision rounds you need. Stages 4-5 are optional but valuable.

---

## Stage 1: DEFINE — What Are You Building?

**Goal:** Clarify what the mockup should contain and who it's for.

**What you need:**
- List of pages/screens with purpose
- User types (public visitor vs logged-in user vs admin)
- Key interactions (what happens when user clicks X?)
- Content hierarchy (what's most important on each page?)

**Without this:** AI guesses what pages you need, invents features, adds
unnecessary complexity. You spend time removing things instead of building.

**Skill types that help:**
- Product requirements / PRD skill
- User story mapping
- Information architecture planning

**Minimum viable input (no skill needed):**
```
I need a mockup for [product name] with these pages:
1. [Page] — [what it shows, who uses it]
2. [Page] — [what it shows]
...
Key flows: [user does X → sees Y → clicks Z]
```

---

## Stage 2: DESIGN — How Should It Look?

**Goal:** Make visual decisions before writing code.

**What you need:**

### 2a. Design Tokens (feeds → `main.css`)
| Decision | Why it matters | Default if missing |
|---|---|---|
| Primary color + variants | Brand identity, button/link colors | Generic blue `#2563EB` |
| Semantic colors | Success/warning/danger consistency | Standard green/amber/red |
| Font family | Personality (playful vs corporate vs editorial) | `system-ui` (invisible) |
| Font size scale | Hierarchy clarity, readability | 12-36px scale |
| Spacing system | Visual rhythm, breathing room | 4px grid |
| Border radius | Sharp vs rounded personality | 4-16px range |
| Shadows | Depth, elevation system | Subtle shadows |

### 2b. Layout Direction (feeds → Pug structure)
| Decision | Why it matters | Default if missing |
|---|---|---|
| Navigation pattern | Sidebar vs top nav vs both | Sidebar for dashboard |
| Page layout per screen | Grid columns, section order | Single column |
| Responsive strategy | Desktop-only vs mobile-first | Desktop + basic mobile |
| Header behavior | Sticky vs static, what's in it | Sticky with logo + nav |

### 2c. Component Specs (feeds → CSS + Pug mixins)
| Decision | Why it matters | Default if missing |
|---|---|---|
| Button variants | How many styles, what for | Primary + secondary + ghost |
| Card structure | Header/body/footer, hover effect | Simple bordered card |
| Form style | Label position, error display | Stacked labels, inline errors |
| Table style | Dense vs spacious, sortable UI | Simple striped table |

**Without this:** AI produces a generic-looking mockup. It works, but it
looks like every other AI-generated UI — "AI slop."

**Skill types that help:**
- Design system / style guide skill
- UI/UX planning skill
- Design specs / handoff skill

**Minimum viable input (no skill needed):**
```
Style: [clean/bold/playful/corporate/editorial]
Primary color: [hex code or "your pick"]
Layout: [sidebar/top-nav/both]
Vibe: [reference website or screenshot]
```

---

## Stage 3: BUILD — Pug Mockup (this skill)

**Goal:** Generate a working, clickable prototype.

**What happens:**
1. AI reads your input (text description, design brief, or full specs)
2. Copies the `template/` folder as project starter
3. Customizes design tokens in `main.css`
4. Writes components (header, sidebar, footer as Pug mixins)
5. Writes pages (1 file per page)
6. Builds: `pug src/index.pug -o dist -P`
7. Output: self-contained HTML, open in any browser

**Prompt tips for better results:**
- Name your pages explicitly: "dashboard, tasks, settings" not "a few pages"
- Describe what each page *contains*, not just what it's called
- Mention layout: "sidebar layout for logged-in pages"
- Reference a style: "clean like Linear" or "dense like Jira"
- Specify data: "show 5 sample tasks with status badges"

**Iteration:**
- Ask for changes: "move the stats cards above the activity feed"
- Add pages: "add a user profile page with the sidebar layout"
- Refine styling: "make buttons rounded, increase card shadow"
- Each edit → rebuild → refresh browser

---

## Stage 4: REVIEW — Is It Good?

**Goal:** Check the mockup for usability, accessibility, and visual quality.

**What to check:**

### Usability
- Can a user find the primary action within 3 seconds?
- Is navigation clear? (current page highlighted, logical grouping)
- Are empty states handled? (what does the page look like with no data?)
- Do form error states make sense?

### Accessibility
- Color contrast: text readable on all backgrounds? (WCAG AA: 4.5:1)
- Touch targets: buttons/links at least 44x44px on mobile?
- Keyboard navigation: focus states visible?

### Visual Consistency
- Same spacing rhythm across pages?
- Same button styles for same-level actions?
- Same card treatment throughout?
- Icons consistent in size and stroke weight?

**Skill types that help:**
- Heuristic evaluation (Nielsen's 10 usability heuristics)
- Accessibility audit (WCAG compliance check)
- Design QA / visual review

**Without this:** You ship a mockup with contrast issues, inconsistent
spacing, or confusing navigation that stakeholders will catch in review.

---

## Stage 5: CONVERT — Moving to Production

**Goal:** Turn the approved mockup into production code.

**What transfers (~60-70%):**
| From Pug Mockup | To Production Framework | How |
|---|---|---|
| `main.css` design tokens | Tailwind config / CSS variables | Copy token values directly |
| Page structure | React/Vue/Svelte components | Same hierarchy, framework syntax |
| Pug mixins | Framework components | `+sidebar('x')` → `<Sidebar active="x" />` |
| CSS component classes | Framework CSS / styled components | Reuse class names or convert |
| SPA hash router | Framework router | Same page structure, proper routing |
| Lucide SVG inline | `lucide-react` / `lucide-vue` | Package import instead of inline |

**What you write fresh:**
- Authentication (login, sessions, tokens)
- API integration (data fetching, mutations)
- Form validation (real validation, not UI-only)
- Error handling (network errors, edge cases)
- State management (global state, caching)
- Testing (unit, integration, e2e)

**Vue bonus:** Vue natively supports Pug in Single File Components:
```vue
<template lang="pug">
.dashboard
  Sidebar(:active="currentPage")
  main.main-content
    h2 Dashboard
</template>
```

**Skill types that help:**
- Production frontend skill (Next.js, Nuxt, SvelteKit)
- Code review / architecture skill

---

## Workflow Combinations

### Solo — Text Only (fastest)
```
[Describe what you want] → pug-mockup → done
```
Best for: quick prototypes, personal projects, exploring ideas.

### With Design Input (recommended)
```
[Design brief with colors/layout] → pug-mockup → share with team
```
Best for: stakeholder demos, feature proposals, design discussions.

### Full Pipeline (best quality)
```
PRD/requirements → design specs → pug-mockup → review/audit → iterate → convert to production
```
Best for: production features, client deliverables, polished demos.

---

## Quick Reference: What Each Companion Skill Outputs

| Companion Skill Type | What It Gives Pug-Mockup | Impact |
|---|---|---|
| **Requirements / PRD** | Page list, user flows, content hierarchy | AI builds the right pages with the right content |
| **Design system** | Color tokens, typography scale, spacing rules | Mockup looks intentional, not generic |
| **UI/UX planning** | Layout direction, component specs, interaction patterns | Structure and behavior match user needs |
| **Design specs** | Full token + component + screen specs | Near pixel-perfect output, minimal iteration |
| **Accessibility audit** | Contrast issues, target sizes, keyboard nav gaps | Mockup meets WCAG standards |
| **Heuristic eval** | Usability issues ranked by severity | UX problems caught before stakeholder review |

Each of these is optional. The more you provide, the better the result.
The less you provide, the more the AI decides for you.
