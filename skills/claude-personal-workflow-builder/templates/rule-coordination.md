# Rule: Coordination

> How the main context coordinates agents and manages workflow.
> Main context = coordinator. It plans, dispatches, and verifies.

---

## Think-First Planning

Every new request: analyze before producing.

1. Main context receives request, analyzes intent
2. If unclear: ask 1-3 clarifying questions before planning
3. Plan: which agent + which skill + what input + what output
4. Spawn agent with a fully framed task (see below)

**Skip think when:**
- User calls a specific agent/skill directly
- System operations (read files, search, update config)
- Continuation of current flow ("fix section 3", "continue")
- Task matches exactly 1 skill and user provides all required input

---

## Depth Detection

Determine complexity before spawning agents:

| Signal | Depth |
|---|---|
| Single feature, one team, one sprint | Simple |
| Cross-team, multi-quarter, strategic | Complex |
| Unclear | Ask the user |

---

## Framed Task — Briefing Subagents

A subagent starts with a blank slate. It cannot see conversation history.
Brief it like a colleague who just walked into the room.

### Prompt Structure

1. **Context** (2-3 sentences) — what problem, for whom, what deadline
2. **Skill + mode** — which skill to run, which mode if applicable
3. **Input** — file paths to read (prefer paths over dumping content)
4. **Decisions already confirmed** — what the user decided, so the agent does not re-ask
5. **Output** — where to write, what format, which template to follow

### Principles

- Load skill definition + template BEFORE writing the prompt
- Point to files, do not dump 200-line documents into the prompt
- Invest 1 minute writing a good prompt to save 10 minutes fixing output
- If the skill has multiple modes, the main context chooses — do not leave it to the agent

---

## Checkpoint Control

Pause for user review:
- After artifact v1 is complete
- Before publishing to any external system

Do NOT pause for:
- Intermediate thinking between steps
- Internal handoffs between agents

---

## Multi-Step Handoff

When a flow has multiple steps (agent A -> agent B):
1. Summarize agent A's output (max 200 tokens) + file path
2. Pass summary to agent B as context
3. Agent B reads the artifact file if it needs details

Default: sequential. Only run parallel when outputs are fully independent.

---

## Sticky Session

If the user sends a follow-up within the same scope and task type
(e.g., "fix section 3" after writing a PRD): keep the current agent,
no re-planning needed.

If the task type changes (e.g., "now challenge this PRD"): re-plan and
spawn a new agent.
