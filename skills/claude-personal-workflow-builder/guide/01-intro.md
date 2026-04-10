# Phase 1 — What You're Building and Why

---

## What Is an AI Personal System?

Most people use AI like a search engine with better grammar: ask a question, get an answer, start over next time. An AI personal system is fundamentally different.

It's a structured workspace where AI knows your role, your domain, your preferences, and your accumulated feedback — without you explaining it every session. It has specialized roles that produce, review, and execute. It remembers what worked and what didn't.

The difference is like hiring a freelancer for every task vs having a team that knows your business.

---

## Before vs After

To make this concrete, here are three scenarios showing what changes:

**Scenario 1: Writing a product spec**

| Without a system | With a system |
|---|---|
| Open ChatGPT, paste requirements, paste context about your company, explain your format preferences, get a generic draft, manually fix tone and structure, forget to check edge cases | Say "write PRD for feature X." AI reads your rules (format, tone, language), reads knowledge about your company's systems and teams, follows your PRD template, flags edge cases automatically, then a separate reviewer agent challenges the draft before you see it |

**Scenario 2: Starting a new session next week**

| Without a system | With a system |
|---|---|
| Re-explain everything. "I'm a PM at company X, we use these systems, last time you made these mistakes, please don't do that again" | AI reads CLAUDE.md (your role, your rules), reads memory (lessons from past sessions), picks up where context left off. Zero re-explanation. |

**Scenario 3: Reviewing your own work**

| Without a system | With a system |
|---|---|
| Ask AI to "review this." AI says "looks great!" because the same instance that wrote it is now defending it | A separate Reviewer agent — with different instructions optimized for finding weaknesses — reads the artifact cold and produces a ranked list of genuine gaps. Producer never reviews its own output. |

The system doesn't make AI smarter. It makes AI consistently useful by removing the parts that fail silently: lost context, self-review bias, repeated mistakes, generic output.

---

## Core Philosophy

**AI enhances input quality so YOU make better decisions — AI doesn't replace your judgment.**

This is the single most important idea. Everything else follows from it.

What this means in practice:

- AI produces drafts — you review and decide scope, priority, and action
- AI simulates multiple perspectives — you choose the direction
- AI maintains context and accumulated feedback — you set the goals
- AI surfaces blind spots and asks sharp questions — you make the call

If you let AI decide and just click "approve," you're skipping the most valuable part.

---

## You Become an Engineering Manager of AI Agents

Your job shifts from "doing the work" to:

1. **Providing context** — what's the problem, who's affected, what are the constraints
2. **Defining intent** — what outcome you want, not step-by-step how to get there
3. **Setting quality gates** — when to stop, what "good enough" looks like
4. **Making decisions** — choosing between options AI presents, resolving ambiguity

AI handles the production. You handle the judgment. This is a better division of labor because AI is faster at producing but worse at knowing what matters to your specific situation.

Think about what a good engineering manager does: they don't write every line of code. They set direction ("we're building X for Y reason"), provide context ("here's the constraint from the business side"), define quality ("it needs to handle Z edge case"), and review output ("this part doesn't match what the customer actually needs"). The team does the production work.

That's your relationship with AI agents. You're not "using a tool" — you're managing a team. The better your briefs, the better their output. The clearer your quality standards, the less rework. The more context you provide upfront, the fewer corrections downstream.

This also means the skills that make you effective shift. Writing detailed step-by-step instructions matters less. Writing clear problem statements, defining good-enough criteria, and making fast review decisions matters more.

---

## The 3 Modules — Big Picture Before Details

Before diving into the 13 phases, understand the three modules that make up any AI personal system. Everything you build falls into one of these:

| Module | What it is | What you'll build | Files |
|---|---|---|---|
| **Context** | What AI knows about you and your domain | CLAUDE.md, knowledge files, memory entries | `CLAUDE.md`, `knowledge/`, `memory/` |
| **Prompts** | How AI behaves and what it produces | Rules (behavioral guardrails), skills (structured procedures), agent personas | `.claude/rules/`, `.claude/skills/`, `.claude/agents/` |
| **Tools** | What AI can do beyond thinking | Hooks (automated scripts), Python helpers, external integrations | `.claude/hooks/`, `.claude/scripts/` |

**Context** answers "who am I working with and what do I need to know?"
**Prompts** answer "how should I behave and what should I produce?"
**Tools** answer "what actions can I take in the real world?"

When you want to change something about your system, the module tells you where to look:

| You want to... | Module | You'll edit... |
|---|---|---|
| Change how AI talks to you | Prompts | `rules/rule-communication.md` |
| Add info about your company | Context | `knowledge/company/` |
| Make AI remember a correction | Context | `memory/` |
| Create a new document type | Prompts | `skills/[new-skill]/SKILL.md` + template |
| Auto-check files after writing | Tools | `hooks/` + `settings.local.json` |
| Add a new AI specialist role | Prompts | `agents/[new-agent]/AGENT.md` |
| Store lessons from past sessions | Context | `memory/[feedback-entry]/` |

The 13 phases build these modules incrementally. Phases 0-3 set up Context, Phases 4-6 build Prompts, Phases 7-8 add Tools and more Context, and Phases 9-12 teach you to optimize all three.

---

## Agent vs Skill — WHO/WHY vs HOW/WHAT

Two concepts that people often confuse. Here's the distinction:

**Agent = WHO does the work + WHY they approach it that way**
An agent is a persona with a specific role, worldview, and boundaries. A Producer agent creates documents with a "produce drafts, human decides" mindset. A Reviewer agent finds weaknesses with a "read cold, be critical" mindset. Same task (read a document), completely different approaches because the WHO is different.

**Skill = HOW to do a specific task + WHAT to produce**
A skill is a structured procedure: input → process → output. "Write a spec" is a skill. "Challenge a document" is a skill. Skills are recipes — they define ingredients (input), steps (process), and plating (output template).

**The relationship:** An agent owns multiple skills. The agent's persona shapes HOW it executes each skill. A Producer with a "write-spec" skill produces documents following the spec template. A Reviewer with a "challenge" skill reads documents and produces findings reports.

| | Agent | Skill |
|---|---|---|
| Defined in | `AGENT.md` | `SKILL.md` |
| Contains | Persona, principles, constraints, tool permissions | Input, output, constraints, template pointers |
| Changes when | You need a new specialist role | You need a new type of output |
| Example | "Producer — creates all written artifacts" | "write-spec — produces feature specifications" |

Think of it this way: you hire agents (WHO), then assign them skills (HOW). You don't create a new agent for every task — you give existing agents new skills.

---

## Architecture Overview

Here's the full picture of what you'll build:

```
                         +-------------------+
                         |       YOU         |
                         | (decisions, goals,|
                         |  review, judgment)|
                         +--------+----------+
                                  |
                                  v
                      +-----------+-----------+
                      |    MAIN CONTEXT       |
                      |    (coordinator)      |
                      |  analyzes intent,     |
                      |  plans work, routes   |
                      |  to agents, controls  |
                      |  checkpoints          |
                      +-----------+-----------+
                                  |
                 +----------------+----------------+
                 |                |                 |
                 v                v                 v
          +------+------+  +-----+-------+  +------+------+
          |   AGENTS    |  |   RULES     |  |  KNOWLEDGE  |
          | specialized |  | behavioral  |  |  static     |
          | roles with  |  | guardrails  |  |  domain     |
          | skills      |  | (tone, file |  |  context    |
          +------+------+  | naming,     |  +-------------+
                 |         | workflow)   |
                 v         +-------------+
          +------+------+
          |   SKILLS    |         +-------------+
          | bounded     |         |   MEMORY    |
          | procedures  |         | accumulated |
          | with        |         | feedback &  |
          | templates   |         | lessons     |
          +-------------+         +-------------+
                                        ^
                                        |
                                  (feeds back from
                                   your corrections)

          +-------------+
          |   HOOKS     |
          | automated   |
          | checks that |
          | run on      |
          | triggers    |
          +-------------+
```

**The directory structure:**

```
workspace/
├── CLAUDE.md              <- entry point: map of the whole system
├── .claude/               <- system brain
│   ├── agents/            <- specialized roles (producer, reviewer, etc.)
│   ├── skills/            <- structured procedures (write PRD, challenge, etc.)
│   ├── rules/             <- behavioral guardrails (tone, naming, workflow)
│   ├── hooks/             <- automated checks (validate after write, etc.)
│   └── scripts/           <- Python helpers (API calls, batch ops)
├── knowledge/             <- static domain context (company, teams, systems)
├── memory/                <- accumulated feedback and lessons
└── inworking/             <- ideas and working notes
```

**How the layers interact:**

```
You send request
    -> Main context (coordinator) analyzes intent
        -> Reads rules for behavioral constraints
        -> Reads relevant knowledge for domain context  
        -> Spawns the right agent + skill
            -> Agent reads SKILL.md for procedure
            -> Agent reads template for output format
            -> Agent produces artifact
        -> You review at checkpoint
        -> Feedback captured in memory for next time
```

> **Why this matters:** This architecture separates things that change at different speeds. Rules change rarely. Knowledge changes when reality changes. Content changes every task. Keeping them separate means updating one layer doesn't break another — and AI loads only what's relevant instead of everything.

---

## Common Objections (Honest Answers)

**"Isn't this over-engineering? I just want to chat with AI."**

If your AI usage is occasional and low-stakes, yes — this is more structure than you need. But if you use AI daily for work that matters (documents that ship, decisions that stick), the structure pays for itself within a week. The alternative is re-explaining context every session, correcting the same mistakes, and never building on previous work. That's not simplicity — it's waste.

**"Can't I just use ChatGPT/Claude chat directly?"**

You can. And for one-off questions, you should. A personal system is for recurring, structured work where consistency and context matter. If you write PRDs weekly, you want AI to know your template, your company's terminology, and the mistakes it made last time. Chat can't do that.

**"This seems like a lot of setup for uncertain payoff."**

The minimum viable system takes about 3 hours to build (see Quick Start Path below). After that, every task you run through it gives you data on what works and what doesn't. You're not committing to a year-long project — you're investing an afternoon to see if the approach fits your work. Most people know within 5 real tasks whether this is worth continuing.

**"I'm not technical. Can I actually do this?"**

Yes. You'll write markdown files (text with simple formatting), not code. The terminal commands you need fit on one screen (see Phase 0). Claude Code itself helps you build the system — you can literally ask it "create an AGENT.md file for a producer role" and it will do it.

---

## Quick Start Path

The full guide has phases 0 through 6+. If you want to get running fast, here's the minimum viable path:

| Phase | What | Time | What You'll Do | Skip? |
|---|---|---|---|---|
| **0 — Prerequisites** | Install Claude Code, learn vocabulary | 15 min | Install the tool, read the glossary so terms make sense later | Required |
| **1 — Intro** | Understand what you're building (this file) | 10 min | Internalize the philosophy and architecture so your design choices have a foundation | Required |
| 2 — Self-Assessment | Identify your pain points and MVP scope | 20 min | Answer 5 questions about your work, pick 2 AI roles to build first | Can do informally |
| **3 — Foundation** | Create workspace, folder structure, root CLAUDE.md | 30 min | Set up folders, write your first CLAUDE.md that describes your system | Required |
| **4 — Rules** | Write 3 core rules (communication, workflow, coordination) | 45 min | Define how AI should communicate, manage files, and coordinate work | Required |
| **5 — Agents** | Create 2 agents (producer + reviewer) | 30 min | Write AGENT.md files that give AI specialized roles with clear boundaries | Required |
| **6 — Skills** | Create 3 skills (think, produce, challenge) | 45 min | Create structured procedures with templates so AI produces consistent output | Required |

**Minimum viable path: 0 → 1 → 3 → pick what you need** (see below).

Phase 2 (self-assessment) is valuable but you can do it informally — just know your 2-3 biggest pain points before starting Phase 3.

> **Phases are not sequential.** The numbers are for reference, not a mandatory order. After the foundation (0 → 1 → 3), pick phases based on what you actually need — you might only need skills (6), or rules + skills (4 + 6), or the full stack. See the "Flexible Reading Order" section below.

---

## Flexible Reading Order

After completing the foundation (Phases 0, 1, 3), the remaining phases are **modules you pick based on your needs**, not a fixed sequence.

### Common paths

| Your situation | Path | Time |
|---|---|---|
| "I just want AI to follow a procedure consistently" | 0 → 1 → 3 → **6 (Skills)** | ~1.5 hours |
| "I want consistent behavior + one procedure" | 0 → 1 → 3 → **4 (Rules)** → **6 (Skills)** | ~2 hours |
| "I want a full system with specialized roles" | 0 → 1 → 3 → 4 → **6 (Skills)** → **5 (Agents)** → 7 | ~3 hours |
| "I want AI to learn from my corrections" | 0 → 1 → 3 → **7 (Memory)** | ~1.5 hours |
| "I want automated quality checks" | 0 → 1 → 3 → 4 → **8 (Hooks)** | ~2 hours |
| "I already have a system, I want to level up" | **9-12** (pick what's relevant) | varies |

### Reading order tips

- **Skills (6) before Agents (5):** Create skills first, then assign them to agents. You need to know what your agents will do before defining their roles.
- **Memory (7) pairs with Foundation (3):** Memory is part of the Context module — if you care about AI remembering your corrections, read it right after setting up your workspace.
- **Hooks (8) after Rules (4):** Hooks automate rule enforcement. Write rules first, then automate them.
- **Phases 9-12 are independent:** Advanced patterns, skill absorption, tuning, and scaling can be read in any order when you're ready.

---

## What You'll Have by the End

After completing all phases, you'll have a working system with:

- **2 agents**: a Producer (creates documents/artifacts) and a Reviewer (independently challenges them)
- **3 skills**: Think (frame problems before producing), a domain-specific Produce skill (with template), and Challenge (find weaknesses in artifacts)
- **3 core rules**: communication style, file/workflow management, and coordination behavior
- **Memory system**: a place to capture feedback so AI improves over time
- **Knowledge folder**: static context about your domain that AI reads when relevant

This is not a finished product — it's a foundation that grows through use. The system improves every time you correct AI behavior and capture the lesson.

---

## Anti-Patterns to Avoid from Day One

Before you start building, internalize these lessons from real operational experience:

1. **Don't over-design before using.** The best system is one that gets used and iterated. Spending a week designing the perfect architecture on paper is wasted effort — you'll redesign after 3 real sessions.

2. **Don't create a separate Orchestrator agent.** It sounds elegant but creates overhead: extra layer of indirection, lost context during handoff, coordinator can't produce directly. Use the coordinator pattern instead — main context orchestrates.

3. **Don't let the producer self-review.** AI reviewing its own output is defensive, not critical. Always have a separate reviewer role.

4. **Don't skip feedback capture.** Every correction you make to AI behavior is a lesson. If you don't write it down, you'll make the same correction next session.

5. **Don't build for imaginary future needs.** Build for what you need this week. The system is designed to grow incrementally — adding an agent later takes 10 minutes. Don't pre-build agents "just in case."

---

## Next Step

Move to [02-self-assessment.md](./02-self-assessment.md) to identify what YOUR system should focus on, or skip ahead to [03-foundation.md](./03-foundation.md) if you already know your pain points.
