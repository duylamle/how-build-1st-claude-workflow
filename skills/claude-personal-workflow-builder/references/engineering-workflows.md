---
type: artifact
scope: references
created: 2026-04-10
updated: 2026-04-10
---

# Engineering Workflows for AI Agents

> Reference for users building engineering-focused AI personal systems.
> If your system is code-heavy (not product/content), these patterns are directly applicable.

---

## Agent Skills — 20 Engineering Workflows

**Source:** [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) by Addy Osmani (Engineering Leader at Shopify)

A collection of 20 skill files that teach AI agents to code like a senior engineer. Each skill covers one engineering practice with structured prompts, anti-rationalization tables, and verification gates.

### What's Inside

| Category | Skills |
|---|---|
| **Planning** | Spec-first development, architecture review |
| **Code Quality** | Code review (5-axis), refactoring, documentation |
| **Testing** | TDD workflow, test coverage analysis |
| **Security** | OWASP-aware security review, dependency audit |
| **CI/CD** | Pipeline design, deployment verification |
| **Debugging** | Root cause analysis, performance profiling |

### Key Patterns Worth Noting

**Anti-rationalization tables:** Each skill includes a table of "reasons the agent might skip this step" paired with counter-arguments. This preempts the common failure mode where AI rationalizes skipping verification to save time.

Example from the code review skill:
| Agent's rationalization | Counter-argument |
|---|---|
| "The code is simple enough to skip review" | Simple code still has edge cases. Review catches assumption gaps |
| "Tests pass, so the code is correct" | Tests verify what was written, not what was meant. Review checks intent |

**Verification gates:** Hard checkpoints where the agent must stop and verify before proceeding. Similar to the checkpoint pattern in this guide (Phase 4, Rule 3).

### How to Use This

If your AI personal system focuses on software development:

1. **Start with 3-4 skills** most relevant to your daily work (code review, testing, and debugging are common starting points)
2. **Adapt the agent persona** — these skills assume a coding agent, but the patterns (anti-rationalization, verification gates) work for any domain
3. **Combine with the Producer/Reviewer split** from this guide — use engineering skills for the Producer agent, and adapt the review skill for the Reviewer agent

### Why This Is Not Absorbed Into This Guide

This guide focuses on product/management workflows. Engineering workflows have different concerns (code correctness, performance, security) that deserve dedicated treatment. If you're a developer, the Agent Skills repo is a better starting point for your Producer agent's skills than the product-focused templates in this guide.

---

## Related Reading

- Phase 5 (Agents) — Producer/Reviewer split pattern
- Phase 6 (Skills) — How to structure skills with templates
- Phase 10 (Skill Absorption) — How to absorb external skills into your system
