# Phase 0 — Prerequisites

Before building your AI personal system, you need the right tool and a shared vocabulary.

---

## What Is Claude Code?

Claude Code is a CLI (command-line interface) tool by Anthropic that lets you run Claude directly in your terminal. Unlike the web chat interface, Claude Code can:

- **Read and write files** on your computer
- **Run shell commands** (git, npm, python, etc.)
- **Spawn subagents** — separate AI instances with their own instructions
- **Use hooks** — automated scripts that trigger on specific events
- **Work with a project folder** — reading CLAUDE.md files for context automatically

Think of it as upgrading from "chatting with AI" to "AI that lives in your workspace and operates on your actual files."

---

## Installation Options

There are several ways to run Claude Code. Pick whichever fits your setup.

**Option A — npm (recommended for developers):**

```bash
npm install -g @anthropic-ai/claude-code
```

Then run `claude` in any terminal to start. This gives you the raw CLI experience — fast, scriptable, and works in any terminal emulator.

**Option B — Desktop app:**

Download from [claude.ai/download](https://claude.ai/download). The desktop app includes the same CLI capabilities with a graphical interface. Good if you prefer a dedicated window rather than mixing AI with your other terminal tabs.

**Option C — VS Code extension:**

Install the "Claude Code" extension from the VS Code marketplace. This embeds Claude Code directly in your editor's terminal panel. Convenient if VS Code is already your primary workspace — you can see your files, run Claude, and review output all in one window.

**Option D — Web app (claude.ai):**

The web interface at claude.ai works for basic conversations but lacks the file system access, hooks, subagents, and project context that make a personal system possible. You can use it for quick one-off questions, but you cannot build a system on it. Think of it as the "demo mode."

### Which option should you choose?

- If you're comfortable with terminals: **Option A** (npm)
- If you want a visual interface: **Option B** (desktop app)
- If you live in VS Code: **Option C** (extension)
- You can switch between them freely — they all read the same CLAUDE.md files and `.claude/` folder

---

## Pricing: What You Actually Need

Claude Code requires a paid Anthropic subscription. Here's what matters for building a personal system:

| Tier | Monthly Cost | What You Get | Good For |
|---|---|---|---|
| **Pro** | $20 | Standard usage, basic agent features | Getting started, light usage, testing the waters |
| **Max** | $100-200 | Extended context, heavy agent usage, more subagent spawns | Daily production use, complex multi-agent workflows |
| **Team** | Per-seat pricing | Shared settings, team-level controls | Teams building shared AI systems |

**Recommendation:** Start with Pro. It's enough to build your entire system and run it for moderate daily use. Upgrade to Max only if you find yourself hitting usage limits regularly — which typically happens when you're running multi-step agent flows (think + produce + review) several times per day.

The free tier is too limited for a real system — you'll hit rate limits within minutes of serious use.

---

## What You DON'T Need

Building an AI personal system sounds technical. It's not. Here's what you can safely ignore:

- **No coding skills required.** You'll write markdown files (plain text with some formatting), not code. If you can write a bullet list, you can build this system.
- **No AI/ML expertise needed.** You don't need to understand how language models work internally. You need to understand what you want AI to do for you — which is a product/management skill, not a technical one.
- **No special hardware.** Claude Code runs on Mac, Windows, and Linux. It's a lightweight CLI tool — if your computer can run a web browser, it can run Claude Code.
- **No DevOps knowledge.** You won't be deploying anything. Everything runs locally on your machine, reading and writing files in a folder.
- **No previous AI tool experience.** If you've used ChatGPT, Copilot, or any other AI tool, great — but prior experience is not required. This guide starts from zero.

---

## Terminal Basics for Non-Developers

If you've never used a terminal before, here's the minimum you need:

| Command | What it does |
|---|---|
| `cd path/to/folder` | Navigate to a folder |
| `ls` (Mac/Linux) or `dir` (Windows) | List files in current folder |
| `mkdir folder-name` | Create a new folder |
| `cat file.md` | Display file contents |
| `code .` | Open current folder in VS Code |

Claude Code handles most file operations for you — you just need to navigate to your workspace folder and run `claude`.

---

## Settings Files

Claude Code uses two settings files in your project's `.claude/` folder:

**`settings.json`** — Shared settings (committed to version control). Defines allowed tools, model preferences, and permission rules that apply to everyone using this project.

**`settings.local.json`** — Personal settings (not committed). Your local overrides: hooks, environment-specific paths, API keys references. This is where you configure automation hooks that run on your machine.

You don't need to create these immediately. Claude Code generates defaults when needed.

---

## Verify Your Setup

After installing, confirm everything works before moving on:

**1. Open a terminal and run Claude Code:**

```bash
claude
```

You should see a welcome message and an input prompt. If you get "command not found," the installation didn't add Claude Code to your PATH — reinstall or check the Anthropic docs for your OS.

**2. Check which model you're using:**

Once inside Claude Code, type:

```
What model are you running on?
```

Claude will tell you its model name (e.g., Claude Sonnet 4). This confirms your subscription is active and the tool can reach Anthropic's API.

**3. Test file access:**

Navigate to any folder and ask Claude to create a test file:

```
Create a file called test.md with the text "Hello from Claude Code"
```

Check that the file appears in your folder. Then ask Claude to read it back:

```
Read test.md and tell me what it says
```

If both work, your setup is complete. Delete the test file.

**4. Test project context (optional):**

Create a `CLAUDE.md` file in your folder with one line: `This is a test project.` Then start a new Claude Code session in that folder. Ask:

```
What do you know about this project?
```

Claude should reference your CLAUDE.md content. This confirms project context loading works — the foundation of everything you'll build.

---

## Glossary

These terms appear throughout the guide. Bookmark this section — come back when a term is unfamiliar.

### Core Architecture

| Term | Definition |
|---|---|
| **Main context** | The primary conversation between you and Claude Code. Acts as the coordinator — receives your requests, plans the work, routes to the right agent, and controls checkpoints. Can also produce output directly for simple tasks. Think of it as the "team lead" of your AI system. |
| **Coordinator** | The pattern where main context handles orchestration instead of having a separate Orchestrator agent. Reduces overhead, keeps full conversation context. |
| **Subagent** | A separate Claude instance spawned by the main context to handle a specific task. Starts with a blank slate — no conversation history, only the prompt it receives. Like assigning a task to a team member with a written brief. |
| **Framed task** | A well-structured prompt given to a subagent. Includes: background context, which skill to run, input file paths, confirmed decisions, and output location. Quality of this prompt directly determines quality of output. |
| **Checkpoint** | A deliberate pause where AI stops for your review. Happens after artifact v1 is complete and before publishing to external systems. The AI presents its work, you review and decide, then it continues. Prevents AI from running too far in the wrong direction. |
| **Depth detection** | The process of classifying a request as "Standard" (bounded feature, 1-3 sprints) or "Strategic" (product direction, multi-quarter). Different depths trigger different agent configurations and output types. Get this wrong and you'll over-engineer simple tasks or under-analyze complex ones. |

### Building Blocks

| Term | Definition |
|---|---|
| **Agent** | A specialized AI role with a defined purpose, allowed tools, and assigned skills. Defined in an `AGENT.md` file with YAML frontmatter. Examples: a Producer agent that creates documents, a Reviewer agent that finds weaknesses. |
| **Skill** | A structured procedure for a specific type of work. Defined in a `SKILL.md` file. Contains: what input is needed, what output to produce, constraints, and pointers to templates/guides. An agent can have multiple skills. |
| **Rule** | A behavioral guardrail that applies across all outputs. NOT a procedure — shapes HOW AI behaves (tone, language, file naming, when to ask vs proceed). |
| **Hook** | A shell command that runs automatically when Claude Code performs a specific action (e.g., after writing a file, before ending a session). Solves the "AI forgets to check" problem through automation. |

### Operational Concepts

| Term | Definition |
|---|---|
| **Producer** | An agent role that creates artifacts (documents, specs, plans). Should never self-review its own output. |
| **Reviewer** | An agent role that independently evaluates artifacts. Has different instructions from the producer — focused on finding weaknesses, not improving. Must be separate from the producer. |
| **Overhead budget** | A cap on total lines of always-load content (rules + root CLAUDE.md). Prevents the system from growing so large that AI spends more context reading instructions than doing actual work. Recommended: 900 lines max. |
| **Think-first** | The pattern of analyzing a request before producing output. Identifies scope, gaps, assumptions, and approach before committing to a direction. Prevents wasted effort on wrong framing. |
| **MECE** | Mutually Exclusive, Collectively Exhaustive — a thinking principle. When listing options or analyzing a problem, ensure items don't overlap (mutually exclusive) and nothing is missing (collectively exhaustive). If your analysis isn't MECE, flag where the overlap or gap is. |
| **Single source of truth** | Each piece of information lives in exactly one file. Other files point to it, never copy it. When the truth changes, you update one place. Prevents the "which version is correct?" problem that plagues every documentation system. |
| **Progressive disclosure** | Design principle: CLAUDE.md files are maps, not manuals. They list what exists with one-line descriptions — details live in the source files. AI reads the map first, then dives into details only when needed. Keeps context loading fast and focused. |
| **Separation of concerns** | Each component has one job. Rules govern behavior. Skills govern procedure. Knowledge stores facts. Memory stores lessons. Mixing them (e.g., putting procedure inside a rule) creates confusion when you need to update one without affecting the other. |

> **Why this matters:** Without shared vocabulary, you'll spend half your time confused by terms that mean different things in different contexts. This glossary comes from real operational experience — every term here maps to a concrete concept you'll implement in later phases. When you see "framed task" in Phase 4, you'll know exactly what it means and why it matters.

---

## Next Step

You have Claude Code installed and understand the vocabulary. Move to [01-intro.md](./01-intro.md) to understand what you're building and why.
