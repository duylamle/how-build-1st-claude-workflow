---
type: artifact
scope: sidekick-agent-mcp-setup
created: 2026-04-20
updated: 2026-04-20
---

# Sidekick Agent MCP Setup

**Install the sidekick-agent MCP server and start shifting tokens from your senior Claude to a cheaper junior LLM — narrow scope you frame, output you verify.**

[![Version](https://img.shields.io/badge/version-v1.0.0-orange)](CHANGELOG.md)
[![skills.sh](https://img.shields.io/badge/skills.sh-compatible-brightgreen)](https://skills.sh/duylamle/product-collection/sidekick-agent-mcp-setup)
[![Made with Claude Code](https://img.shields.io/badge/Made_with-Claude_Code-blueviolet?logo=anthropic)](https://claude.ai/claude-code)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/duylamle/product-collection)](https://github.com/duylamle/product-collection)

---

## The Problem

Your Claude usage keeps hitting ceilings. Summarizing long PRDs, translating content, scanning folders for references, drafting v0 from templates — all of that burns senior Claude tokens on work that doesn't need senior reasoning.

You can't tell Claude "please be cheaper." You can only delegate work that doesn't need senior thinking to a cheaper model — but doing that naively (switching models, hacking prompts) loses Claude's context and orchestration.

## The Solution

This skill sets up [sidekick-agent-mcp](https://github.com/duylamle/product-collection/tree/main/skills/sidekick-agent-mcp-setup) — a small Python MCP server that wraps any Anthropic-compatible cheaper LLM as four tools your senior Claude can call:

```
      Senior Claude (expensive, good at judgment)
                         │
                 frames narrow task
                         ↓
          sidekick-agent MCP (4 tools)
                         │
                 calls junior LLM
                         ↓
         Junior LLM (cheap, MiniMax/Haiku/OSS)
                         │
                 returns draft output
                         ↓
          Senior verifies → persists
```

**Why controlled shift, not outsource:** the senior frames scope and verifies output. The junior handles the mechanical part at a fraction of the cost. Token savings show up per call (10-50k per summary), accumulating across a session.

## Install

```bash
npx skills add duylamle/product-collection@sidekick-agent-mcp-setup -y
```

## Quick Start

1. Install the skill (above)
2. In Claude Code, say **"install sidekick"** or **"setup sidekick"**
3. Claude walks through `guide/setup-guide.md` (9 steps): install MCP server → configure LLM backend → register with Claude Code → install delegation rule + companion call skill → first real call
4. After setup, say **"sidekick tóm tắt PRD này"**, **"sidekick dịch file này sang EN"**, or **"nhờ sidekick extract action items"** — the nested `sidekick-call` skill fires automatically

## Prerequisites

- **Python 3.10+** (for the MCP server)
- **An Anthropic-compatible LLM endpoint** with API key. Options:
  - **Claude Haiku** — Anthropic API direct, simplest setup
  - **OpenRouter** — gateway to many cheap models, one key
  - **LiteLLM gateway** (routing to MiniMax, Gemini, Llama) — best cost/quality if you already run LiteLLM
  - **MiniMax direct** — native Anthropic format
  - **vLLM / sglang / Ollama** — self-hosted on your own GPU
- **Claude Code** (or any MCP-compatible host)
- **Git**

## What's Inside

```
sidekick-agent-mcp-setup/
├── SKILL.md                            ← Claude reads this automatically
├── README.md                           ← This file
├── CHANGELOG.md
├── CLAUDE.md                           ← Project map
├── mcp/                                ← Python MCP server source (ship-in-skill)
│   ├── server.py
│   ├── sidekick_agent/                 ← The package
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── .env.example
│   └── LICENSE
├── guide/
│   └── setup-guide.md                  ← 9-step end-to-end walk-through
├── examples/
│   └── use-cases.md                    ← 8 real scenarios with token impact
└── docs/                               ← Drop-in docs for Claude Code projects
    ├── rules/
    │   └── rule-sidekick-delegation.md ← Drop into your .claude/rules/
    └── skills/
        └── sidekick-call/              ← Companion skill for day-to-day calls
            ├── SKILL.md                ← When and how to call the 4 tools
            ├── prompts.md              ← Copy-paste prompts per tool
            └── verify.md               ← Senior verify checklist
```

Install this one skill → you get everything: the MCP Python source (no `git clone` required), the setup guide, 8 real use cases, the delegation rule Claude applies to know when to shift, and the day-to-day call skill.

## Key Principles

Five non-negotiables for any sidekick call (drawn from `docs/rules/rule-sidekick-delegation.md`):

- **The junior must know exactly what it's doing** — no guessing
- **Output expectations are explicit** — format, length, structure
- **One call does one action** — summarize or translate, not both
- **Input is sufficient, not excessive** — only the files that matter
- **The senior owns verification** — encoding, facts, shape

## Example Savings

One typical session:

- Summarize 5 PRDs (8k tokens each) → **~40k tokens shifted** to junior
- Translate 10k-word research doc → **~20k tokens shifted**
- Extract action items from meeting notes → **~5k tokens shifted**
- Senior Claude spends its tokens on writing the follow-up PRD, challenging assumptions, and pushing back — the work that actually needs senior reasoning

See [`examples/use-cases.md`](examples/use-cases.md) for 8 detailed scenarios with the exact tool calls, verification steps, and per-case token impact.

## About

Built by **Lê Trương Duy Lam** — Technical Product Owner at [VNG Corporation](https://www.vng.com.vn/). This skill is the user-facing companion to the [sidekick-agent-mcp](https://github.com/duylamle/product-collection/tree/main/skills/sidekick-agent-mcp-setup) server — the MCP is the infrastructure, this skill is how a non-technical Claude Code user gets it running and starts shifting tokens the same day.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin)](https://www.linkedin.com/in/le-truong-duy-lam/)

---

<p align="center">
  Thanks for visiting <b>Sidekick Agent MCP Setup</b>
  <br><br>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=duylamle.product-collection.sidekick-agent-mcp-setup&style=flat" alt="visitors"/>
</p>

## License

[MIT](../../LICENSE)
