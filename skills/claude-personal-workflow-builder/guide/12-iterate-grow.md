# Phase 12 — Iterate and Grow

Your system is running, tuned, and producing good output. Now the question becomes: when should you add more, and when should you leave it alone?

---

## Growth Principles

### Add only when you have a REAL need

The temptation is to build agents and skills for everything you *might* do someday. Resist it. Every addition costs context budget — AI has to read more instructions before doing real work.

**The rule:** if you haven't done a task at least 3 times manually, you don't need a skill for it yet.

"Three similar lines of code is better than a premature abstraction" — this applies to AI systems too. A manual prompt you copy-paste 3 times is fine until you see the pattern clearly enough to formalize it.

### Each addition has a cost

| What you add | Context cost | Maintenance cost |
|---|---|---|
| New agent | AGENT.md + routing complexity | Must keep description accurate for intent matching |
| New skill | SKILL.md + template + guide files | Must update when process changes |
| New rule (always-load) | Lines counted against budget | Must verify it's still relevant monthly |
| New rule (on-demand) | Loaded per session when relevant | Lower cost, but still needs maintenance |
| New template | Structure AI must follow | Must update when output needs change |

### Be deliberate

Before adding anything, ask:
1. Can the existing system handle this with a good prompt? (Often yes)
2. Will I use this more than 3 times in the next month?
3. Does this justify the ongoing maintenance?

If you answer "no" to any of these, don't add it.

---

## When to Add a New Agent

**Add an agent when:** you have 3+ skills that share a domain and need a consistent persona, tool set, and knowledge context.

**Until then:** main context can handle it. You don't need a "research agent" if you have one research skill — the coordinator can run that skill directly.

**Signs you need a new agent:**
- You keep writing the same persona context in prompts for different skills
- Multiple skills need the same set of tools and knowledge paths
- The domain has specific constraints that apply to all tasks in it

**Signs you don't need a new agent:**
- You have only 1-2 skills in that domain
- The coordinator handles the tasks well with direct prompts
- The "agent" would just be a pass-through to one skill

---

## When to Add a New Skill

**Add a skill when:** you do a task 3+ times AND the output needs consistent structure AND you find yourself repeating the same instructions.

**Signs you need a new skill:**
- You paste the same template/instructions every time you do this task
- Output quality varies because you forget constraints
- The task has a clear input → output pattern with known edge cases

**Signs you don't need a new skill:**
- It's a one-off task you might never do again
- The task is too varied to standardize (each instance is unique)
- A good prompt from the coordinator is sufficient

> **Why This Matters:** Over-building is the most common failure mode for AI personal systems. People create elaborate structures they never use, then feel overwhelmed by maintenance. Start minimal, grow from real needs, and your system stays lean and useful.

---

## Upgrading Existing Skills

Adding new skills is covered above. But what about improving skills you already have?

### Triggers for upgrading

- **Feedback accumulates** — you keep correcting the same output patterns
- **Domain shifts** — new regulations, tools, or processes change what "good output" means
- **Community evolves** — new skills on skills.sh do things yours can't
- **External resources prove value** — a consultant kit (see Phase 10) has patterns worth absorbing

### The upgrade flow

1. **Diagnose** — is the issue in the skill (constraints, template) or in how you use it (prompt quality)?
2. **Re-research** — `npx skills find [domain]` to see what's new in the community
3. **Gap analysis** — compare your current skill against new community skills. What's missing?
4. **Absorb the delta** — integrate only the new parts. Don't rebuild what works.
5. **Update CHANGELOG** — version bump with what changed and why
6. **Update sources.md** — log new sources absorbed

### Upgrade vs. rebuild

Upgrade when: the core design is sound but needs additions or refinements.
Rebuild when: the fundamental approach is wrong (wrong output structure, wrong persona, wrong constraints). Rebuilding is rare — most skills just need incremental improvement.

> **Why This Matters:** Skills are living tools, not static documents. A skill that worked 3 months ago may not work today. Regular upgrades — triggered by real feedback, not scheduled maintenance — keep your system effective.

---

## Publishing Your Skills

Once a skill is battle-tested — used 10+ times, tuned through feedback, producing consistently good output — consider sharing it with the community.

### Preparing for publication

1. **Remove all personal/company references.** Your skill should be generic — usable by anyone in the same domain. Replace company-specific knowledge paths with placeholders or instructions.

2. **Write a clear SKILL.md.** Someone installing your skill should understand what it does, what input it needs, and what output it produces — without reading your entire system.

3. **Include examples.** Add 1-2 `EXAMPLE-*.md` files showing real (anonymized) output. Examples teach more than instructions.

4. **Test in isolation.** Can someone use this skill without your agents, rules, or knowledge base? If not, document the dependencies.

### Publishing

Push your skill to a public GitHub repository:

```
your-repo/
  skills/
    your-skill-name/
      SKILL.md
      template/TEMPLATE.md
      EXAMPLE-01.md
      guide.md (optional)
```

Others install via:
```bash
npx skills add <your-github>/<repo>@<skill-name>
```

Your skill becomes discoverable on [skills.sh](https://skills.sh).

### Maintaining published skills

- Respond to issues and feedback from users
- Update when you improve your own version
- Version breaking changes clearly

---

## Versioning Your System

Use git or file versioning to track changes. This matters because:

- You can roll back if a change makes things worse
- You can see what changed when behavior shifts unexpectedly
- You have a history of your system's evolution

**File versioning convention:**
```
2026-03-15-prd-upload-v1.md    ← first version
2026-03-17-prd-upload-v2.md    ← after challenge feedback
2026-03-20-prd-upload-v3.md    ← after stakeholder review
```

Keep old versions. Don't delete while iterating. You might need to reference what changed between versions or roll back a section.

**System versioning:** if you use git, commit after meaningful changes to your `.claude/` folder. A commit message like "add code-review skill, update challenge template" tells future-you what happened.

---

## Scaling Patterns

As your system grows, different coordination patterns become appropriate.

### 2-5 Agents: Coordinator Pattern

This is where most personal systems live. The main context (coordinator) manages everything directly:

- Routes requests to the right agent
- Writes prompts with full context
- Handles handoffs between agents
- Can self-produce for simple tasks

This works well because the coordinator has full conversation context and can make informed routing decisions.

### 5-10 Agents: Functional Grouping

When you have more agents, group them by function to keep routing manageable:

```
Produce:  PO, Designer, Marketing
Review:   Challenge, QA
Support:  Data Analytics, Secretary
Execute:  Ops, DevOps
```

The coordinator routes to a functional group first, then picks the specific agent. This reduces the number of options to evaluate at each routing decision.

### 10+ Agents: Hierarchy

Most personal systems don't need this many agents. But if you do:

- Consider sub-coordinators for each functional group
- Each sub-coordinator manages 3-5 agents in its domain
- Main coordinator routes to sub-coordinators, not individual agents

**Warning:** hierarchy adds overhead. Every level of indirection means potential context loss and slower execution. Only add hierarchy when the flat coordinator pattern genuinely can't keep up — not as a premature optimization.

> **Why This Matters:** The right coordination pattern depends on your system's actual size. Using hierarchy for 3 agents is over-engineering. Using flat coordination for 15 agents is chaos. Match the pattern to your scale.

---

## The Growth Timeline

A realistic trajectory for building an AI personal system:

| Timeframe | What you should have | What you're doing |
|---|---|---|
| Week 1 | Identity file, 2-3 agents, 2-3 skills, 1-2 rules | Learning the basics, making lots of corrections |
| Month 1 | 3-5 agents, 5-8 skills, 3-5 rules, active memory | Tuning through feedback, discovering what works |
| Month 3 | 5-8 agents, 10-15 skills, 5-8 rules, pruned memory | Absorbing community skills, publishing your own |
| Month 6+ | Stable core, occasional additions | Maintaining more than building, high output quality |

Don't try to reach Month 6 in Week 1. The system needs real usage to tell you what it actually needs.
