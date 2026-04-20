---
name: sidekick-agent-mcp-setup
description: >
  Install and register the sidekick-agent MCP server in Claude Code. Covers
  installing Python deps, configuring an Anthropic-compatible LLM backend
  (MiniMax via LiteLLM, Claude Haiku, OpenRouter, vLLM), wiring the MCP
  into Claude Code, and installing the delegation rule + sidekick-call
  companion skill. Trigger: "install sidekick", "setup sidekick", "cài
  sidekick", "cấu hình sidekick", "register sidekick MCP", "sidekick not
  connected", "add sidekick to Claude Code".
created: 2026-04-20
updated: 2026-04-20
---

# Sidekick Agent MCP Setup

> Install sidekick-agent MCP. Shift tokens from senior Claude to a cheaper
> junior LLM — controlled scope + senior verification.

---

## What This Skill Does

Gets [sidekick-agent-mcp](https://github.com/duylamle/product-collection/tree/main/skills/sidekick-agent-mcp-setup) running in your Claude Code setup. Install Python server → configure LLM backend → register with Claude Code → drop in the rule + companion skill → first-call smoke test.

Fires when user is wiring up sidekick for the first time, moving it between machines, upgrading, or debugging a connection / auth error. For day-to-day use of the four MCP tools (summarize, translate, task, agent_run), the nested `sidekick-call` skill takes over.

## Input

Your answers about backend + workspace:

- An Anthropic-compatible LLM endpoint URL + API key
- Absolute path to the folder you want as the sidekick's "workspace"
- Extra paths to blacklist beyond defaults (`.env`, `*secret*`, `.git/`, etc.)

## Output

`claude mcp list` shows `sidekick-agent ✓ Connected`. First `sidekick_summarize` call returns bullets from a test file.

---

## Full step-by-step

See **[guide/setup-guide.md](guide/setup-guide.md)** — the 9-step end-to-end walk-through covering install, smoke test, live endpoint test, Claude Code registration, rule installation, first real call, tuning knobs, troubleshooting, and uninstall.

## Real use cases

See **[examples/use-cases.md](examples/use-cases.md)** — 8 concrete scenarios (summarize PRD, translate research, extract action items, draft Jira story, scan folder, classify feedback, synthesize interviews, rewrite spec section) with exact tool calls and token-impact estimates. Plus anti-patterns you should keep on senior Claude.

---

## Install

```bash
npx skills add duylamle/product-collection@sidekick-agent-mcp-setup -y
```

Then say **"install sidekick"** or **"setup sidekick"** in Claude Code — Claude walks through [guide/setup-guide.md](guide/setup-guide.md).

## Prerequisites

- **Python 3.10+** on PATH
- **Anthropic-compatible LLM endpoint** with API key. Options:
  - Claude Haiku (Anthropic API direct)
  - OpenRouter (gateway to many models)
  - LiteLLM gateway (routing to MiniMax, Gemini, Llama)
  - MiniMax direct (native Anthropic format)
  - vLLM / sglang / Ollama (self-hosted)
- **Claude Code** or another MCP-compatible host
- **Git**

---

## What's Bundled

```
sidekick-agent-mcp-setup/
├── SKILL.md                            ← This file
├── README.md                           ← User-facing docs + badges
├── CHANGELOG.md
├── CLAUDE.md
├── mcp/                                ← Python MCP server source (ship-in-skill)
│   ├── server.py
│   ├── sidekick_agent/                 ← The package
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── .env.example
│   └── LICENSE
├── guide/
│   └── setup-guide.md                  ← 9-step install walk-through
├── examples/
│   └── use-cases.md                    ← 8 real scenarios with token impact
└── docs/                               ← Drop-in docs for Claude Code projects
    ├── rules/
    │   └── rule-sidekick-delegation.md ← Copy into your .claude/rules/
    └── skills/
        └── sidekick-call/              ← Companion skill for day-to-day calls
            ├── SKILL.md
            ├── prompts.md              ← Copy-paste prompts per tool
            └── verify.md               ← Senior verify checklist
```

Install this one skill → you get everything needed: the MCP Python source (no git clone required), the setup guide, 8 real use cases, the rule Claude applies to know when to shift, and the call skill that fires during normal use.

---

## Constraints

- **Generic backend** — any Anthropic-compatible `/messages` endpoint works
- **Workspace-scoped** — MCP rejects paths outside `SIDEKICK_WORKSPACE_ROOT` and blacklisted paths
- **One-time skill** — after setup finishes, `sidekick-call` handles every call. This skill re-fires only on upgrade or connection errors

---

## Works Well With

| Skill | Why |
|---|---|
| **Any skill producing long-form artifacts (PRD, research, meeting notes)** | Sidekick summarizes drafts before senior review |
| **Any skill doing bulk transformation** | Sidekick handles repeated transforms on many files |
| **Data pipeline / analysis skills** | Sidekick scans folders, extracts fields, synthesizes findings |

Find complementary skills on [skills.sh](https://skills.sh).
