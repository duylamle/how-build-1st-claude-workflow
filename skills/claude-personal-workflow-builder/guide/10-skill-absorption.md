# Phase 10 — Skill Absorption

You don't need to be an expert in every domain to build great skills. You need a method for finding what already works and making it yours.

---

## The Problem

When you need a skill for a new domain — code review, data analysis, content marketing, test planning — you face a cold start problem. You don't know what best practices exist, what edge cases to handle, or what output structure works best. Building from scratch means reinventing wheels that others have already built.

---

## The Pattern: Skill Absorption

Instead of starting from zero or blindly copying someone else's work, use this 6-step pattern to bootstrap and grow any skill.

### Step 1 — Bootstrap

Tell Claude what you need. Describe the task, who it's for, and what good output looks like.

```
"I need a skill for code review. It should check for security issues,
performance problems, and readability. Output should be a structured
report with severity levels. The reviewer is a senior engineer persona."
```

Claude proposes and creates a basic agent + skill based on your requirements. This gives you a working starting point — not perfect, but functional.

### Step 2 — Research

Search for existing skills in the same domain:

```bash
npx skills find code-review
npx skills find security-review
npx skills find pull-request
```

Browse results on [skills.sh](https://skills.sh). Install promising ones:

```bash
npx skills add <owner/repo@skill-name> -y
```

Install 2-3 that look relevant. You're not committing to any of them — you're gathering reference material.

### Step 3 — Gap Analysis

Compare your bootstrapped skill against each community skill, side by side. Look for:

- **Scripts** they have that you don't (automation, API calls, formatters)
- **Templates** with better structure or more comprehensive sections
- **Checklists** covering edge cases you didn't think of
- **Patterns** for handling tricky situations (error recovery, fallbacks)
- **Constraints** that prevent common mistakes

Read their files thoroughly — SKILL.md, guides, templates, examples, scripts. Don't skim.

### Step 4 — Absorb

Extract the good parts and integrate them into YOUR skill. This is not copy-paste — it's adaptation.

- Take their edge case handling and add it to your constraints
- Take their template sections and merge with yours (keeping your conventions)
- Take their scripts and adapt to your project structure
- Take their checklist items and add to your quality criteria

**Key decisions during absorption:**
- Does this addition serve your actual workflow? If not, skip it.
- Does it conflict with your existing conventions? If so, adapt it.
- Does it add value beyond what you already have? If not, skip it.

### Step 5 — Review

After absorbing, review your upgraded skill holistically:

- Did you miss anything from the community skills?
- Does the combined result still make sense as a coherent skill?
- Are there any contradictions between absorbed parts and your original design?
- Would your skill handle edge cases the community skill handles?

### Step 6 — Cleanup

Delete the community skills you installed. Keep only yours, now upgraded.

```bash
# Remove installed community skills
rm -rf .claude/skills/community-code-review/
```

Your skill is now the single source of truth. No external dependencies.

> **Why This Matters:** Community skills are teaching material, not production dependencies. Using someone else's skill as-is means inheriting their conventions, their assumptions, and their limitations. Absorbing the best parts into your own skill means you understand every line and it fits your system perfectly.

---

## Example Walkthrough: Building a "Code Review" Skill

**Day 1 — Bootstrap:**
You tell Claude: "I need a code review skill. Focus on Python. Check security, performance, maintainability. Output a report with findings by severity."

Claude creates:
```
.claude/skills/code-review/
  SKILL.md          (basic: input, output, constraints)
  report/TEMPLATE.md (simple severity-based report)
```

You use it for 2-3 real reviews. It works but misses some things.

**Day 3 — Research + Gap Analysis:**
```bash
npx skills find code-review
# Found: alice/dev-tools@code-review, bob/workflows@pr-review
npx skills add alice/dev-tools@code-review -y
npx skills add bob/workflows@pr-review -y
```

You read both skills thoroughly. Findings:
- Alice's skill has a security checklist covering OWASP Top 10 — yours doesn't
- Bob's skill has a "review by file type" pattern — checks different things for tests vs production code
- Alice's template includes a "positive feedback" section — good for team morale
- Bob's skill has a script that auto-extracts changed files from a PR

**Day 3 — Absorb:**
You integrate:
- OWASP checklist items into your constraints
- File-type-aware review pattern into your guide
- Positive feedback section into your template
- Adapted version of Bob's script into your skill's scripts folder

You skip:
- Alice's JavaScript-specific rules (you work in Python)
- Bob's CI/CD integration (you don't need it yet)

**Day 3 — Cleanup:**
```bash
rm -rf .claude/skills/community-code-review/
rm -rf .claude/skills/community-pr-review/
```

Your code-review skill is now significantly better than any individual community skill — because it's tailored to your needs and enriched by the best of what's out there.

---

## Applies to Any Domain

This pattern is not limited to engineering skills:

| Domain | Bootstrap prompt | Research queries |
|---|---|---|
| Content writing | "I need a skill for blog posts targeting developers" | `npx skills find blog-writing`, `npx skills find content` |
| Data analysis | "I need a skill for SQL analysis with visualization recommendations" | `npx skills find data-analysis`, `npx skills find sql` |
| Testing | "I need a skill for writing test plans from PRDs" | `npx skills find test-plan`, `npx skills find qa` |
| Documentation | "I need a skill for API documentation" | `npx skills find api-docs`, `npx skills find documentation` |
| Marketing | "I need a skill for product launch planning" | `npx skills find gtm`, `npx skills find launch` |

You don't need domain expertise upfront. The bootstrap step leverages Claude's general knowledge, and the absorption step leverages the community's specialized experience.

---

## Commands Reference

| Command | Purpose |
|---|---|
| `npx skills find [query]` | Search skills.sh for skills matching your query |
| `npx skills add <owner/repo@skill> -y` | Install a community skill into your project |
| `npx skills` | List installed skills |
| Browse [skills.sh](https://skills.sh) | Discover skills visually |

---

## Upgrading Existing Skills

The 6-step pattern above is for building new skills. But what about skills you already have that need improvement?

Upgrading is different from bootstrapping — you're not starting from zero. You have a working skill with known strengths and gaps.

### When to upgrade

- **Output quality drops** — your domain has evolved, but your skill hasn't
- **Community catches up** — new skills on skills.sh cover things yours doesn't
- **You outgrow it** — your process has changed and the skill doesn't reflect it
- **New tools appear** — npm packages, MCP servers, or kits that could enhance your skill

### The upgrade flow

1. **Re-research** — run `npx skills find [your-domain]` again. The ecosystem evolves.
2. **Gap analysis against YOUR current skill** — not against a blank slate. What's missing now that wasn't missing before?
3. **Absorb the delta** — only the new parts. Don't rebuild what already works.
4. **Update sources.md** — log what you absorbed, from where, and when.
5. **Version bump** — update your CHANGELOG with what changed.

> **Key difference from bootstrapping:** you're comparing against your existing skill, not against nothing. This means you can be surgical — absorb specific improvements without disrupting what already works well.

---

## The Consultant Model

Not everything needs to be absorbed into your system. Some external resources are more valuable kept as-is — like an outsource partner you call when needed.

### Three strategies for external resources

| Strategy | When to use | What happens |
|---|---|---|
| **Absorb** | You want to own it completely | Extract the good parts into your skill → delete the source |
| **Consultant** | It works well as-is, you don't need to own it | Keep it in a reference folder, route to it when relevant |
| **Promote** | A consultant has proven its value over time | Absorb the best parts → optionally keep or delete the source |

### What counts as an external resource?

- **Community skills** from skills.sh (`npx skills add ...`)
- **Kits** — bundled toolsets (starter kits, boilerplate repos, domain-specific toolkits)
- **npm packages** that include Claude skills or prompts
- **MCP servers** that extend your system's capabilities

### Storage convention

Keep external resources in a dedicated folder (e.g., `external/`) separate from your working system:

```
your-workspace/
├── .claude/          ← YOUR system (agents, skills, rules)
├── external/         ← External resources (read-only reference)
│   ├── .claudeignore ← Prevents Claude from scanning nested .claude/ folders
│   ├── CLAUDE.md     ← What's here and how to use it
│   ├── some-kit/
│   └── some-package/
└── ...
```

**Why separate?** External resources often have their own `.claude/` folders with hooks, settings, and skills. If they live inside your workspace, Claude Code might scan them and create conflicts. A dedicated folder with `.claudeignore` prevents this.

### The decision flow

```
Install external resource
    → Read it thoroughly
    → Try using it for real tasks
    → Ask yourself: "Do I want to own this, or just use it?"
        → Own it → Absorb (Steps 3-6 from the absorption pattern)
        → Use it → Keep as Consultant
    → After using a consultant 5+ times:
        → Still valuable as-is? → Keep
        → Parts worth owning? → Promote (absorb the best parts)
        → No longer useful? → Delete
```

> **Why This Matters:** The absorption pattern assumes you always want to own everything. But that's not always true. Some tools are better as dependencies than as internalized knowledge. The consultant model gives you a middle ground — benefit from external resources without the maintenance cost of full absorption.

---

## Key Principle

**Don't use someone else's skill as-is — use it as a benchmark to level up your own.** But not everything needs absorbing — some resources serve you better as consultants you call when needed.

Community skills are written for their author's context, conventions, and needs. Your skill should be written for yours. The absorption pattern lets you benefit from others' experience without inheriting their limitations. The consultant model lets you benefit without the maintenance cost.
