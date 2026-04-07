# 08 — Hooks and Automation: Making Rules Impossible to Violate

Rules tell AI what to do. Hooks make sure it actually does it.

Hooks are shell commands that execute automatically when Claude Code performs specific actions. They run at the OS level — outside AI's control. AI cannot skip them, forget them, or rationalize around them.

The principle: **"impossible to violate" beats "remember to follow"** every time.

---

## What Hooks Are

Claude Code fires events when tools are used:
- **PreToolUse** — before a tool executes (chance to block or modify)
- **PostToolUse** — after a tool executes (chance to validate output)
- **Stop** — when the conversation turn ends (chance to run cleanup/logging)

Hooks are configured in `settings.local.json` and run as shell commands. They receive context about which tool was called and on which file.

---

## 3 Essential Hooks to Start With

### 1. Backup Before Edit

**Event:** PreToolUse, tool: Edit
**Purpose:** Before any modification to system files (`.claude/` folder), create a backup. Safety net for when AI edits go wrong.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/scripts/shared/backup-before-edit.py \"$TOOL_INPUT_FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

The backup script checks if the file is in `.claude/` and creates a timestamped copy before the edit proceeds. If the edit breaks something, you can restore from backup.

Example backup script (`backup-before-edit.py`):
```python
import sys
import shutil
from pathlib import Path
from datetime import datetime

file_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
if not file_path or ".claude" not in file_path.parts:
    sys.exit(0)  # Not a system file, skip

backup_dir = Path(".claude/_backups") / datetime.now().strftime("%Y-%m-%d")
backup_dir.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%H%M%S")
backup_name = f"{timestamp}--{file_path.name}"
shutil.copy2(file_path, backup_dir / backup_name)
print(f"Backed up: {file_path.name}")
```

### 2. Validate After Write

**Event:** PostToolUse, tool: Write
**Purpose:** After writing any `.claude/` file, run validators to check conventions are followed.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/scripts/shared/validate-dispatcher.py \"$TOOL_INPUT_FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

The dispatcher examines the file path and routes to the right validator:
- `AGENT.md` or `SKILL.md` → check YAML frontmatter (required fields, valid values)
- Any `.md` in `.claude/` → check naming convention (ALLCAPS for system files, kebab-case for others)
- Rules files → check total line count stays under budget

If validation fails, the hook outputs a warning that AI sees in its next turn — prompting it to fix the issue immediately.

### 3. Session Audit Log

**Event:** Stop
**Purpose:** Auto-write a session summary to `_logs/`. Creates an accountability trail of what was done, what was changed, what is pending.

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/scripts/shared/session-log.py"
          }
        ]
      }
    ]
  }
}
```

The log captures: timestamp, files modified, agents spawned, tasks completed, open items. Useful for picking up where you left off in the next session, and for auditing what AI did.

> **Why This Matters:** Without audit logs, you have no record of what AI changed in your system. After a week of sessions, you cannot tell which edits were intentional and which were AI drift. Logs cost nothing and save hours of forensic investigation.

---

## The Validator Pattern

Individual validators each check one thing. A dispatcher routes to the right validator based on file path. This pattern scales — add a new validator without touching existing ones.

### Architecture

```
scripts/
  shared/
    validate-dispatcher.py      <-- routes to correct validator
    validators/
      validate-frontmatter.py   <-- checks YAML frontmatter
      validate-naming.py        <-- checks file naming conventions
      validate-budget.py        <-- checks line count budgets
      validate-agent-skills.py  <-- checks agent-skill consistency
```

### Dispatcher logic

```python
import sys
from pathlib import Path

file_path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
if not file_path:
    sys.exit(0)

validators = []

# Route based on file characteristics
if file_path.name in ("AGENT.md", "SKILL.md"):
    validators.append("validators/validate-frontmatter.py")

if ".claude" in file_path.parts:
    validators.append("validators/validate-naming.py")

if file_path.parent.name == "rules" and not file_path.name.startswith("on-demand"):
    validators.append("validators/validate-budget.py")

# Run all applicable validators
for v in validators:
    # Execute validator, collect results
    ...
```

### When to create a validator

Every new rule should ask: **can this be validated by a script?** If yes, write a validator. Common candidates:

- Frontmatter has required fields and valid values
- File naming follows conventions
- Always-load rules stay under line budget
- Agent `skills` list matches actual skill folders
- Template files exist where SKILL.md points to them

> **Why This Matters:** Rules that are only enforced by AI memory will be forgotten. Rules enforced by validators are checked every time, automatically. The validator catches the violation immediately — before it compounds into bigger problems. Start with frontmatter validation (highest impact), add more as patterns emerge.

---

## Python Scripts: Precision Work

AI handles judgment (what to write, how to structure). Scripts handle precision (API calls, format conversion, batch operations).

### Organization

```
.claude/
  scripts/
    CLAUDE.md                   <-- index of all scripts
    shared/                     <-- reusable across skills
      backup-before-edit.py
      validate-dispatcher.py
      validators/
        validate-frontmatter.py
  skills/
    publish-jira/
      scripts/
        create-issues.py        <-- skill-specific script
```

Two locations:
- `scripts/shared/` — reusable scripts used by multiple skills or hooks
- `skills/[name]/scripts/` — scripts that belong to one specific skill

### Calling scripts

Always through the Bash tool:

```
python .claude/scripts/shared/validate-dispatcher.py "path/to/file.md"
python .claude/skills/publish-jira/scripts/create-issues.py --input issues.json
```

### When to use scripts vs. AI directly

| Use scripts for | Use AI directly for |
|---|---|
| API calls (Jira, Confluence, GitHub) | Deciding what content to write |
| Format conversion (markdown to HTML) | Analyzing requirements |
| Batch operations (create 20 issues) | Reviewing artifacts |
| Data validation and checking | Summarizing and synthesizing |
| File manipulation at scale | Structuring and organizing |

AI generates the content or decisions. Scripts execute the mechanical parts. Do not ask AI to format API payloads or handle auth tokens — scripts do that reliably every time.

---

## Complete settings.local.json Example

```json
{
  "env": {
    "WORKSPACE_ROOT": "/path/to/your/workspace"
  },
  "permissions": {
    "allow": [
      "Read",
      "Write",
      "Edit",
      "Bash",
      "Glob",
      "Grep"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/scripts/shared/backup-before-edit.py \"$TOOL_INPUT_FILE_PATH\""
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/scripts/shared/validate-dispatcher.py \"$TOOL_INPUT_FILE_PATH\""
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/scripts/shared/session-log.py"
          }
        ]
      }
    ]
  }
}
```

> **Why This Matters:** This configuration gives you three layers of protection from day one: backups before destructive edits, validation after writes, and audit trails after every session. You can run your system for months without worrying about silent drift or unrecoverable mistakes.

---

## The Tuning Escalation Ladder

When AI output is not right, escalate enforcement gradually — from soft to hard:

| Level | Mechanism | When to use |
|---|---|---|
| 1 | **Memory entry** | First-time error, may not recur |
| 2 | **Rule** | Pattern repeats across sessions |
| 3 | **Checklist** | Specific skill keeps missing steps |
| 4 | **Validator hook** | Important rule that AI keeps forgetting |
| 5 | **Template + Example** | Output format/style keeps drifting |

Start at level 1. Escalate only when the lower level fails to prevent recurrence. Most corrections stay at level 1-2. Level 4-5 are for chronic issues.

---

## Key Principles

- **Hooks run outside AI**: AI cannot skip, forget, or rationalize around them
- **Start with 3 hooks**: backup, validate, audit log. Add more when needed
- **Validators beat instructions**: a rule checked by script is a rule that works
- **Scripts handle precision, AI handles judgment**: do not mix their strengths
- **Escalate enforcement gradually**: memory first, hooks for chronic issues
- **Audit everything**: if you do not log what AI does, you cannot tell when it drifts
