---
type: artifact
scope: sidekick-agent-mcp-setup
created: 2026-04-20
updated: 2026-04-20
---

# Sidekick Agent MCP Setup

> Install sidekick-agent MCP. Shift tokens from senior Claude to a cheaper junior LLM.
> Install: `npx skills add duylamle/product-collection@sidekick-agent-mcp-setup -y`

## How to use

Say **"install sidekick"**, **"setup sidekick"**, or **"cài sidekick"** the first time — Claude walks through `guide/setup-guide.md` (9 steps: install Python deps → configure backend → register MCP → install rule → first call + troubleshoot).

After setup, day-to-day calls are handled by the nested **`docs/skills/sidekick-call/`** skill — triggers on **"sidekick tóm tắt"**, **"sidekick dịch"**, **"nhờ sidekick extract"**, etc.

## Structure

```
sidekick-agent-mcp-setup/
├── SKILL.md                            ← Skill definition (start here)
├── README.md                           ← User-facing docs + badges
├── CHANGELOG.md
├── CLAUDE.md                           ← This file
├── mcp/                                ← Python MCP server source (ship-in-skill)
│   ├── server.py
│   ├── sidekick_agent/                 ← The package
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── .env.example
│   └── LICENSE
├── guide/
│   └── setup-guide.md                  ← 9-step end-to-end setup
├── examples/
│   └── use-cases.md                    ← 8 real scenarios with token impact
└── docs/                               ← Drop-in docs for Claude Code projects
    ├── rules/
    │   └── rule-sidekick-delegation.md ← Copy into your .claude/rules/
    └── skills/
        └── sidekick-call/              ← Companion for day-to-day calls
            ├── SKILL.md
            ├── prompts.md              ← Copy-paste prompts per tool
            └── verify.md               ← Senior verify checklist
```

## Key files to read

| When you need... | Read |
|---|---|
| Skill entry point | `SKILL.md` |
| First-time setup walk-through | `guide/setup-guide.md` |
| Real use cases + token impact | `examples/use-cases.md` |
| When + how to call the 4 tools | `docs/skills/sidekick-call/SKILL.md` |
| Copy-paste prompts | `docs/skills/sidekick-call/prompts.md` |
| Verify sidekick output | `docs/skills/sidekick-call/verify.md` |
| Why this exists (philosophy) | `docs/rules/rule-sidekick-delegation.md` |

## Prerequisites

- Python 3.10+
- An Anthropic-compatible LLM endpoint (Claude Haiku, OpenRouter, MiniMax via LiteLLM, or self-hosted)
- Claude Code (or another MCP host)
- Git

## Philosophy (short version)

**Controlled token shift, not outsourcing.** Senior Claude frames narrow scope for the junior; senior verifies output before anything is persisted. Full rule: `docs/rules/rule-sidekick-delegation.md` — copy into your own `.claude/rules/` folder.
