# Changelog — Product Collection

> Versioning: Y = number of skills, Z = patch (docs/badges). See CLAUDE.md.

## v0.4.0 (2026-04-20)

- Added skill #4: `sidekick-agent-mcp-setup` v1.0.0 — Install sidekick-agent MCP for shifting tokens from senior Claude to a cheaper junior LLM. Ships the Python MCP server source inside the skill (no `git clone` required) plus delegation rule (`rules/rule-sidekick-delegation.md`) and nested companion skill `skills/sidekick-call/` (SKILL.md + prompts.md + verify.md) for day-to-day calls.

## v0.3.0 (2026-04-16)

- Added skill #3: `excel-pipeline` v1.0.0 — Parse multi-source data → JSONL → formatted Excel (7 Python scripts: parse, merge, audit, diff, export)

## v0.2.2 (2026-04-10)

- Updated `claude-personal-workflow-builder` to v2.0.0 (flexible phases, references, PO example)
- Updated `pug-mockup` to v1.1.0 (nontech workflow guide, concrete prompts)

## v0.2.1 (2026-04-08)

- Added closing footer with visitor badge to all READMEs
- Linked skills.sh badges to skill pages
- Synced version badges with changelogs
- Added versioning convention to CLAUDE.md

## v0.2.0 (2026-04-08)

- Added skill #2: `pug-mockup` v1.0.0 — Pug-based SPA mockup generator
- Added CLAUDE.md to `claude-personal-workflow-builder` (v1.1.1)

## v0.1.1 (2026-04-07)

- Restructured as monorepo (`skills/` folder)
- Renamed repo → `product-collection`
- Renamed + updated skill → `claude-personal-workflow-builder` v1.1.0

## v0.1.0 (2026-04-05)

- Initial release with 1 skill: `how-build-1st-claude-workflow` v1.0.0
