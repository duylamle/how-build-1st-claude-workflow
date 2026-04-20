---
type: artifact
scope: sidekick-agent-mcp-setup
created: 2026-04-20
updated: 2026-04-20
---

# Changelog — sidekick-agent-mcp-setup

## v1.0.0 (2026-04-20)

### Added
- `SKILL.md` — skill entry point for installing and registering sidekick-agent MCP
- `CLAUDE.md` — project map for Claude Code
- `README.md` — user-facing docs with badges, problem/solution framing, backend options, install
- `mcp/` — **Python MCP server source shipped inside the skill** (no `git clone` required):
  - `server.py` — launcher shim
  - `sidekick_agent/` — the package (server, config, client, safety, audit, agent_loop, prompts, agent_tools)
  - `requirements.txt`, `pyproject.toml`, `.env.example`, `LICENSE`
- `guide/setup-guide.md` — 9-step end-to-end setup: install Python deps, smoke test, live endpoint test, register with Claude Code, install rule, first real call, tune env vars, troubleshoot, uninstall
- `examples/use-cases.md` — 8 real scenarios showing when to shift work to sidekick and token impact per case (summarize PRD, translate research, extract action items, draft Jira story, scan folder for API refs, classify feedback, synthesize interviews, rewrite spec section). Includes anti-patterns that should stay with senior Claude.
- `docs/` — drop-in docs bundle for Claude Code projects:
  - `rules/rule-sidekick-delegation.md` — delegation rule with the "controlled token shift" philosophy (copy into your `.claude/rules/`)
  - `skills/sidekick-call/` — nested companion skill for day-to-day calls:
    - `SKILL.md` — when and how to call the 4 MCP tools
    - `prompts.md` — copy-paste prompts per tool
    - `verify.md` — senior verify checklist before persisting output
