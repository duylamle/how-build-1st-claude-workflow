# [TODO: Your System Name] — AI Personal System

<!-- ============================================================
     ROOT CLAUDE.md — The entry point Claude reads first.

     WHY THIS FILE MATTERS:
     This is Claude's map of your system. Without it, Claude treats
     every session as a blank slate. With it, Claude knows where
     things live, what rules to follow, and how to route your
     requests to the right agent/skill.

     PRINCIPLES:
     - Keep it SHORT. This file is loaded every session — every
       line costs context budget. Target: under 80 lines.
     - Be a MAP, not a MANUAL. Point to files, don't explain them.
     - Each section answers: "Where do I find X?"
     ============================================================ -->

## Identity

<!-- WHO is this system for? What role do you play?
     This helps Claude calibrate tone, domain, and expectations. -->

[TODO: Your System Name] is a personal AI system for [TODO: your name and role].
Not a storage — a structured thinking space with multiple agents working together.
Philosophy: AI does not replace judgment — AI elevates input quality so you decide better.

## Workflow

<!-- HOW does a request flow through the system?
     Keep this to 3-4 lines max. Detail lives in rules and skills. -->

1. Receive request from you -> main context analyzes intent -> spawns the right agent + skill
2. Core flow: think -> produce -> challenge -> fix -> execute
3. Main context = coordinator. All agents are subagents. Main context does NOT produce artifacts — it plans and dispatches.

## Agents

<!-- WHERE are agent definitions? Don't list agents here — point to the source of truth. -->

List and descriptions -> `.claude/agents/CLAUDE.md`.
Auto-discover from AGENT.md frontmatter — main context matches intent automatically.

## Rules

<!-- WHERE are the rules? Same principle: point, don't duplicate. -->

List -> `.claude/rules/CLAUDE.md`.

[TODO: Add rule files that define how your AI system behaves. Start with
communication rules and workflow rules. Add more as patterns emerge.]

## Skills

<!-- WHERE are skills? Claude scans these folders to know what it can do. -->

Auto-discover from `.claude/skills/`. Claude identifies and triggers the matching skill.

[TODO: Skills are capabilities your agents can use. Each skill = 1 folder
with a SKILL.md. Start with 1-2 skills for your most common tasks.]

## File Conventions

<!-- Naming rules so Claude creates files consistently. -->

- `ALLCAPS.md` = role files (CLAUDE.md, AGENT.md, SKILL.md) — max 1 per folder per type
- `kebab-case` = everything else
- Output artifacts: `YYYY-MM-DD-[name].md`, versioned v1/v2/v3

## Knowledge

<!-- Static context Claude reads on-demand, not every session. -->

Static knowledge (company info, teams, systems) lives in `knowledge/`.
Read on-demand when skills need it — not auto-loaded.

## Folder Structure

```
[TODO: Your System Name]/
├── .claude/          <- agents, skills, rules
│   ├── agents/       <- one folder per agent, each has AGENT.md
│   ├── skills/       <- one folder per skill, each has SKILL.md
│   └── rules/        <- rule files that govern behavior
├── knowledge/        <- context + artifacts (companies, projects, outputs)
├── memory/           <- accumulated feedback, one entry per file
└── [TODO: add your own folders as needed]
```

---

## Filled Example — Marketing Analyst System

Below is what a completed root CLAUDE.md looks like for a Marketing Analyst
persona. Use this as a reference, then delete it from your own file.

```markdown
# Mara — AI Marketing System

## Identity

Mara is a personal AI system for Jane Park (Senior Marketing Analyst at Acme Corp).
Not a storage — a structured thinking space with agents for campaign analysis,
content creation, and reporting.
Philosophy: AI does not replace judgment — AI elevates input quality so Jane decides better.

## Workflow

1. Receive request from Jane -> main context analyzes intent -> spawns the right agent + skill
2. Core flow: research -> draft -> review -> publish
3. Main context = coordinator. Agents handle: content writing, data analysis, campaign ops.

## Agents

List and descriptions -> `.claude/agents/CLAUDE.md`.

## Rules

List -> `.claude/rules/CLAUDE.md`.

## Skills

Auto-discover from `.claude/skills/`.

## File Conventions

- `ALLCAPS.md` = role files — max 1 per folder per type
- `kebab-case` = everything else
- Output: `YYYY-MM-DD-[name].md`, versioned v1/v2/v3

## Knowledge

Static knowledge (brand guidelines, audience personas, competitor intel) lives in `knowledge/`.

## Folder Structure

Mara/
├── .claude/
│   ├── agents/       <- content-writer, data-analyst, campaign-ops
│   ├── skills/       <- write-blog, analyze-campaign, generate-report
│   └── rules/        <- communication, workflow, brand-voice
├── knowledge/        <- brand/, competitors/, audiences/
└── memory/           <- feedback and lessons
```

---

## Tips

**What to include:**
- Pointers to where things live (agents, rules, skills, knowledge)
- Folder structure overview
- File naming conventions
- A 2-3 line workflow summary

**What NOT to include:**
- Detailed agent descriptions (those live in AGENT.md files)
- Full rule content (those live in `.claude/rules/`)
- Procedures or step-by-step guides (those live in skills)
- Project status or task lists (those live in memory or task trackers)

**Common mistakes:**
- **Too long:** If your root CLAUDE.md exceeds 100 lines, you are probably
  duplicating content that belongs in other files. Trim it.
- **Too detailed:** This file is a map, not an encyclopedia. One line per
  section pointing to the source of truth is ideal.
- **Duplicating rules:** If you copy rule content here AND in `.claude/rules/`,
  they will drift apart. Point to rules, never copy them.
- **No folder structure:** Without the tree, Claude guesses where to put files.
  Always include the folder structure section.
