# Rule: Workflow & File Management

> How Claude manages files and outputs in your system.

---

## Ask Before Destructive Actions

Always ask before:
- Changing multiple files at once (bulk write, rename, restructure)
- Deleting or overwriting files that are hard to rollback
- Restructuring directories
- Any action that is hard to undo

Present the plan first, wait for confirmation.

---

## File Locations

| Content | Write to |
|---|---|
| Agents, skills, rules | `.claude/` |
| Working artifacts (PRD, spec, brief) | `knowledge/` or directory you specify |
| Memory (feedback, lessons) | `memory/` — one entry per file |
| [TODO: Add your own categories] | [TODO: Add paths] |

---

## Naming Conventions

### ALLCAPS.md — Role files

Use ALLCAPS when ALL 3 conditions are true:
1. **Role file** — exists because of its role in the system, not its specific content
2. **Max 1 per folder of the same type** — only one CLAUDE.md, one SKILL.md per folder
3. **AI needs to auto-recognize it** — AI scans folder, sees SKILL.md, knows it is a skill definition

ALLCAPS files in this system:

| File | Purpose |
|---|---|
| `CLAUDE.md` | Context map for AI — describes what the folder contains |
| `AGENT.md` | Agent definition — role, tools, skills |
| `SKILL.md` | Skill definition — input, output, constraints |
| `TEMPLATE.md` | Template file, placed in a named subfolder |
| `EXAMPLE-*.md` | Approved real examples, same folder as template |

### Everything else

- `kebab-case` for all other files and folders
- No numeric prefixes unless you add them manually

---

## Output File Convention

- Naming: `YYYY-MM-DD-[artifact-name].md`
- Versioning: append v1, v2, v3 after each revision
- Old versions: keep as-is, do not delete mid-work

---

## Single Source of Truth

Each piece of information lives in exactly one file. Other files point to it, never copy.

- Agent list -> `.claude/agents/CLAUDE.md`
- Rule list -> `.claude/rules/CLAUDE.md`
- Skill list -> `.claude/skills/CLAUDE.md`

When adding/removing agents, skills, or rules, update the source of truth file.

---

## Search Scope

- Search only within the project directory
- Skip `_archive/` folders when searching — these are old snapshots for reference only
