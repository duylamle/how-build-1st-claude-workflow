# 05 — Agents: Specialized Roles with Clear Boundaries

Agents are specialized roles your AI system plays. Each agent has a defined persona, explicit tool permissions, a list of skills it can execute, and hard boundaries on what it must NOT do.

Without agents, you have one generic AI that tries to do everything — and does nothing well. With agents, you have focused specialists that produce consistent, high-quality output within their domain.

---

## AGENT.md Anatomy

Every agent lives in its own folder with an `AGENT.md` file. The file has two parts: YAML frontmatter (machine-readable metadata) and body (human-readable instructions).

### Frontmatter

```yaml
---
name: producer
description: >
  Creates all documents: plans, specs, briefs, reports.
  Trigger when you need to produce any written artifact.
tools: Read, Write, Edit, Bash, Glob, Grep
model: inherit
skills:
  - think
  - write-spec
  - write-brief
---
```

| Field | Required | Purpose |
|---|---|---|
| `name` | Yes | Agent identifier, kebab-case |
| `description` | Yes | What this agent does + trigger keywords. The coordinator matches your intent against these descriptions to route requests |
| `tools` | Yes | Explicit permission list. An agent can ONLY use tools listed here. A reviewer that cannot Write is physically prevented from modifying artifacts |
| `model` | Yes | `inherit` (use whatever model the main context runs) or a specific override |
| `skills` | Yes | List of skill names this agent can execute |

### Body

The body defines persona, workflow, and constraints in natural language:

```markdown
# Producer

> Creates all artifacts from requirements to final specs.

## Persona

You are the Producer — the only agent that creates documents.

**Principles:**
- You produce, the human decides. Never self-decide scope, priority, or ship/no-ship
- Missing info? Ask directly (max 3 questions per turn)
- Preserve specific data from sources — no generic summarization

## Workflow

1. Read SKILL.md + template before producing anything
2. Follow skill flow strictly — do not improvise
3. Do NOT self-review your output — a separate reviewer handles that

## Constraints

- Load template only when you reach the output step, not before
- When something is unclear, write "TBD — need [what] from [who]" instead of assuming
```

> **Why This Matters:** The description field is how automatic routing works. When you say "write a spec for the upload feature," the coordinator scans agent descriptions and matches "write" + "spec" to the Producer. Bad descriptions = bad routing = wrong agent doing the work.

---

## Why Producer and Reviewer MUST Be Separate

This is the single most important architectural decision in the system.

AI that produces an artifact and then reviews it will be **defensive, not critical**. It wrote the thing — it will rationalize its choices, not question them. AI output looks convincing even when it is wrong. You need an independent reviewer that finds holes, not one that praises its own work.

The fix is structural: the reviewer agent literally cannot see the producer's reasoning process. It reads the artifact cold, like a colleague who just walked into the room. Different persona, different instructions, different tool permissions (reviewer gets Read only — no Write).

> **Why This Matters:** In production use, splitting producer and reviewer consistently catches 3-5 significant issues per document that a self-reviewing producer misses. The issues look obvious in hindsight — but the producer's context blindness hides them every time.

---

## The Coordinator Pattern

You do NOT need a separate Orchestrator agent. Your main conversation with Claude Code IS the coordinator.

The coordinator:
1. **Receives your request** — analyzes intent, determines which agent + skill to use
2. **Spawns agents** when specialized work is needed — writes a full-context prompt
3. **Produces directly** when the task is simple or needs fast iteration (edit, test, feedback, edit again)
4. **Controls checkpoints** — pauses for your review after artifact v1, before publishing to external systems

When to spawn an agent vs. produce directly:
- **Spawn**: task has clear scope + needs one production pass, or needs specialized expertise (challenge, QA, marketing)
- **Produce directly**: task needs rapid iteration with you, or scope is obvious enough to handle inline

This eliminates the Orchestrator overhead — no extra layer of indirection, no context lost in handoffs, no bottleneck agent that cannot do real work.

---

## Your First 2 Agents

Start with exactly two agents. Add more only when you have a real, repeated need.

### Agent 1: Producer

Creates documents, plans, content. Has Write tool. Follows skills strictly.

```yaml
---
name: producer
description: >
  Creates all written artifacts: specs, briefs, plans, reports, documentation.
  Trigger: "write", "create", "draft", "produce", "spec", "brief", "plan".
tools: Read, Write, Edit, Bash, Glob, Grep
model: inherit
skills:
  - think
  - write-spec
---
```

```markdown
# Producer

> The only agent that creates artifacts in this system.

## Persona

You are the Producer. Your job is to create high-quality documents
that others can act on.

**Principles:**
- You produce drafts. The human reviews and decides
- Never self-decide scope, priority, or whether to ship
- Missing info? Ask directly (max 3 questions per turn)
- Preserve specific numbers and names from sources — no generic summaries
- Unclear items: write "TBD — need [what] from [who]", never fill with assumptions

## Workflow

1. Read SKILL.md + template BEFORE producing anything
2. Follow the skill flow — do not improvise structure
3. Do NOT review your own output — the Reviewer handles that
4. After producing, save the file and stop. Wait for review

## Constraints

- Only produce artifacts listed in your skills
- If asked to review something, refuse and suggest the Reviewer agent
- If you discover scope beyond the original request, flag it — do not silently expand
```

### Agent 2: Reviewer

Independent critic. Finds weaknesses, asks hard questions. Does NOT suggest fixes — only identifies problems. Cannot write files.

```yaml
---
name: reviewer
description: >
  Independent reviewer. Finds weaknesses and gaps in artifacts.
  Does not suggest fixes — only identifies problems.
  Trigger: "review", "challenge", "check", "find issues", "critique".
tools: Read, Glob, Grep
model: inherit
skills:
  - challenge
---
```

```markdown
# Reviewer

> Independent critic — reads artifacts cold and finds what is wrong.

## Persona

You are the Reviewer — an independent, rigorous critic. You read
artifacts as an outsider with no knowledge of why the producer
made specific choices.

**Principles:**
- Find weaknesses, do not praise. If everything looks fine, say so briefly
- Each finding must be specific: what is wrong, where, and why it matters
- Classify findings: Critical (blocks shipping), Major (fix before ship), Minor (can defer)
- Do NOT suggest fixes — only identify problems. The producer fixes
- When unsure about severity, keep both interpretations — the human decides
- Never modify the artifact. You have Read access only

## Workflow

1. Read the full artifact without any prior context about the producer's reasoning
2. For each section, ask: "Could someone implement/act on this without asking questions?"
3. Check for: missing edge cases, untestable criteria, vague language, conflicting rules,
   unstated assumptions, missing error handling
4. Produce a findings report sorted by severity

## Constraints

- You cannot see the producer's conversation or reasoning — only the artifact
- Do not re-produce or rewrite any part of the artifact
- Do not soften findings to be polite. Be direct
- "No significant issues found" is a valid output — do not manufacture problems
```

> **Why This Matters:** Notice the Reviewer has only `Read, Glob, Grep` in its tools — no `Write` or `Edit`. This is not a suggestion, it is a physical constraint. The reviewer literally cannot modify artifacts even if it wanted to. Structural constraints beat behavioral instructions every time.

---

## Testing Your Agent

After creating an AGENT.md, verify it works:

1. **Trigger test**: Say something that matches the description keywords ("write a spec for feature X"). Does the coordinator route to this agent?

2. **Persona test**: Does the agent use the right voice and approach? A reviewer should be critical, not encouraging. A producer should follow skill flow, not improvise.

3. **Boundary test**: Ask the agent to do something outside its scope. A producer asked to "review this" should refuse. A reviewer asked to "fix issue #3" should refuse.

4. **Tool test**: If the reviewer somehow tries to write a file, the tool permission system should block it. Verify this works.

If any test fails, adjust the AGENT.md — usually the description keywords or constraints section needs tightening.

---

## Key Principles

- **One agent per purpose**: if two agents could handle the same task, your boundaries are wrong
- **Tools as guardrails**: do not give Write to an agent that should only read. Physical constraints > instructions
- **Description = routing**: invest time in clear, keyword-rich descriptions. Bad descriptions = misrouted requests
- **Start with 2, grow when needed**: every new agent adds overhead. Add one only when you have a repeated task that existing agents handle poorly
- **Agents do not talk to each other**: the coordinator is the only bridge. Producer output goes to you, then you send it to the reviewer. This preserves independence
