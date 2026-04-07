# Phase 3 — Foundation

Time to create the actual workspace. By the end of this phase, you'll have a folder structure and a root CLAUDE.md that Claude Code reads automatically.

---

## Step 1: Create the Workspace Folder

Pick a location and create your workspace:

```bash
mkdir my-ai-workspace
cd my-ai-workspace
```

Name it whatever makes sense to you. This single folder will contain your entire AI system.

---

## Step 2: Create the Folder Structure

```bash
mkdir -p .claude/agents
mkdir -p .claude/skills
mkdir -p .claude/rules
mkdir -p .claude/hooks
mkdir -p .claude/scripts
mkdir -p knowledge
mkdir -p memory
mkdir -p inworking
```

Here's what each folder does:

```
workspace/
├── CLAUDE.md              ← entry point — AI reads this first every session
├── .claude/               ← system brain (AI config)
│   ├── agents/            ← specialized roles (one folder per agent)
│   ├── skills/            ← structured procedures (one folder per skill)
│   ├── rules/             ← behavioral guardrails (one file per rule)
│   ├── hooks/             ← automated shell scripts triggered by events
│   └── scripts/           ← Python helpers for API calls, batch ops
├── knowledge/             ← static domain context
├── memory/                ← accumulated feedback and lessons learned
└── inworking/             ← ideas, drafts, working notes
```

### Why This Structure?

**`.claude/`** — Everything AI needs to know about HOW to work. This is the system's brain: roles, procedures, guardrails, automation. Separating it from content means you can update how AI works without touching your actual documents.

**`knowledge/`** — Everything AI needs to know about your DOMAIN. Company info, team structures, system architectures, stakeholder maps. This changes when reality changes (new team member, new system), not every task.

**`memory/`** — Accumulated lessons from past sessions. Each feedback entry is one file. AI reads relevant memories when a task relates to past feedback. This is how the system improves over time without you repeating corrections.

**`inworking/`** — Your scratch pad. Ideas, design explorations, working notes. Not structured, not polished — just a place for things in progress.

> **Why this matters:** This structure implements Separation of Concerns — the single most important architectural decision. Config (`.claude/`) changes per development cycle. Knowledge changes per reality. Content changes per task. They change at different speeds, so keeping them separate means each layer stays clean and AI loads only what's relevant.

---

## Step 3: Write the Root CLAUDE.md

This is the most important file in your system. Claude Code reads it automatically at the start of every session. It must be SHORT — a map, not a manual.

Create `CLAUDE.md` in your workspace root:

```markdown
# My AI Workspace

## Identity
[Your name] — [Your role]. AI supports [your domain] work.
Philosophy: AI enhances input quality so I make better decisions.

## Workflow
1. Receive request → main context analyzes intent → route to right agent + skill
2. Core flow: think → produce → review → fix → execute
3. Main context coordinates and can produce directly when appropriate

## Agents
Agent list → `.claude/agents/CLAUDE.md`

## Rules
Rule list → `.claude/rules/CLAUDE.md`

## File Conventions
- ALLCAPS.md = system/role files (CLAUDE.md, AGENT.md, SKILL.md)
- kebab-case = everything else
- Output files: YYYY-MM-DD-name.md with version suffix (v1, v2, v3)

## Folder Structure
- `.claude/`    ← agents, skills, rules, scripts, hooks
- `knowledge/`  ← static domain context
- `memory/`     ← accumulated feedback
- `inworking/`  ← ideas, working notes
```

### Key Principles for CLAUDE.md

**Map, not manual.** List what exists with one-line descriptions. Details live in the source files. If AI needs to know how an agent works, it reads the AGENT.md — not a summary in root CLAUDE.md.

**Progressive disclosure.** AI reads the root map, understands the landscape, then dives into specific files only when the task requires it. This saves context for actual work.

**If you can remove a line and AI still works fine — remove it.** Every line costs context tokens. Root CLAUDE.md under 30 lines is ideal.

---

## Step 4: Create Index Files

Create `.claude/agents/CLAUDE.md`:

```markdown
# Agents

> Source of truth for agent list. Root CLAUDE.md points here.

| Agent | Role | Skills |
|---|---|---|
| producer | Creates artifacts (docs, specs, plans) | think, produce |
| reviewer | Independently challenges artifacts | challenge |
```

Create `.claude/rules/CLAUDE.md`:

```markdown
# Rules

> Source of truth for rule list. Root CLAUDE.md points here.

## Always-load (auto-read every session)
- **rule-communication.md** — Language, tone, thinking style
- **rule-workflow.md** — File management, naming, output conventions
- **rule-coordination.md** — Main context as coordinator, think-first, checkpoints

## On-demand (read when relevant task)
- (none yet — add as needed)
```

---

## Step 5: Understand Single Source of Truth

This principle prevents the most common maintenance headache: information duplicated in multiple files that goes out of sync.

**Each piece of information lives in exactly one file. Other files point to it, never copy it.**

Examples:
- Agent list lives in `.claude/agents/CLAUDE.md` — root CLAUDE.md points to it
- Rule details live in individual rule files — rules CLAUDE.md lists them with one-line descriptions
- Skill procedures live in SKILL.md — agent AGENT.md just references skill names

When you add a new agent: update `.claude/agents/CLAUDE.md`. That's it. Root CLAUDE.md just says "Agent list → `.claude/agents/CLAUDE.md`" — no update needed.

When you add a new rule: update `.claude/rules/CLAUDE.md`. Root CLAUDE.md remains unchanged.

> **Why this matters:** In a system with 10+ files, duplication creates a maintenance nightmare. You update a skill description in one place, forget another, and AI gets conflicting instructions. Single source of truth means one update, zero inconsistencies. This seems obvious now but becomes critical as your system grows past 20 files.

---

## Step 6: Understand Naming Conventions

### ALLCAPS.md Files

Use ALLCAPS when ALL THREE conditions are true:

1. **Role file** — exists because of its role in the system, not its specific content. `SKILL.md` means "this is a skill definition" regardless of which skill.
2. **Maximum one per folder of the same type** — each folder has at most one `CLAUDE.md`, one `AGENT.md`, one `SKILL.md`.
3. **AI needs to auto-discover it** — AI scans a folder, sees `SKILL.md`, instantly knows this is a skill definition. The filename IS the signal.

### Everything Else

- `kebab-case` for all other files: `rule-communication.md`, `prd-writing-guide.md`
- Output artifacts: `YYYY-MM-DD-name.md` (e.g., `2026-04-05-feature-prd.md`)
- Versions: append v1, v2, v3 after each revision

---

## Verify Your Foundation

Run Claude Code in your workspace:

```bash
cd my-ai-workspace
claude
```

Ask: "Read the root CLAUDE.md and tell me what you understand about this workspace."

Claude should describe your identity, workflow, and point to agents/rules. If it can — your foundation works.

---

## Next Step

Move to [04-rules.md](./04-rules.md) to write the 3 core rules that shape how AI behaves in every session.
