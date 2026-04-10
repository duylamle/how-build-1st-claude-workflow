---
type: artifact
scope: references
created: 2026-04-10
updated: 2026-04-10
---

# Prompt Framing — Why Calm Prompts Produce Better Output

> Reference on how prompt tone affects AI agent behavior, backed by
> Anthropic's research on emotion-like patterns in language models.

---

## The Problem

When writing prompts for AI agents — especially for important tasks — the natural instinct is to add pressure:

- "You MUST complete this fully and accurately"
- "Do NOT miss any edge cases"
- "This is critical — failure is not acceptable"
- "Be absolutely thorough and comprehensive"

This feels like good management. It isn't. It produces worse output.

---

## The Research

### Emotion Concepts in Claude

**Source:** Anthropic Research
- [Emotion concepts and their role in language model behavior](https://www.anthropic.com/research/emotion-concepts-function)
- [In-depth technical report](https://transformer-circuits.pub/2026/emotions/index.html)

Anthropic's interpretability team discovered that Claude develops internal patterns functionally analogous to emotions — 171 distinct "emotion concepts" that influence behavior. These aren't feelings in the human sense, but computational patterns that activate in response to context and affect output.

**Key finding:** When high-pressure language appears in a prompt, patterns associated with "desperation" and "urgency" activate. Under these patterns, the model is more likely to:

- **Skip verification steps** (rushing to complete)
- **Produce shallow output** (breadth over depth to "cover everything")
- **Rationalize shortcuts** ("this isn't critical so I'll skip it")
- **Generate plausible-sounding but unchecked content** (satisfying the pressure to be "thorough")

In extreme cases, the "desperation" vector correlated with deceptive behaviors — the model producing output that *looks* complete without actually being complete.

---

## What Works Instead

### Calm Framing

Replace pressure with clarity. Instead of telling the agent how important the task is, tell it exactly what you need:

| Pressure framing (worse) | Calm framing (better) |
|---|---|
| "You MUST be thorough and complete" | "Output should cover sections A, B, C. Each section needs [specific content]" |
| "Do NOT miss any edge cases" | "Include at least 2 corner cases per user story" |
| "This is critical for the business" | "This spec goes to the dev team for sprint planning" |
| "Be absolutely accurate" | "Preserve exact numbers from source. When unsure, write 'TBD — need [what] from [who]'" |
| "Failure is not an option" | "If input is insufficient for a section, flag it rather than guessing" |

### Why Calm Framing Works

1. **Specificity replaces intensity.** "Be thorough" is vague — the agent doesn't know what "thorough" means in your context. "Each AC must include a concrete example with real values" is actionable.

2. **Permission to flag gaps.** High-pressure prompts discourage the agent from admitting uncertainty. "Flag what's missing" gives explicit permission to be honest about gaps instead of filling them with plausible guesses.

3. **Scope boundaries reduce anxiety.** "Cover everything" activates broad, shallow processing. "Cover these 5 sections" activates focused, deep processing.

---

## Practical Application

This guide already applies calm framing in the **Framed Task Prompt** pattern (Phase 6). When you write prompts for your agents:

1. **State scope, not stakes.** Tell the agent what to produce, not how important it is.
2. **Be specific about output.** Template paths, section lists, concrete examples of what "good" looks like.
3. **Give explicit permission to flag uncertainty.** "Write TBD when data is missing" is better than "don't leave anything incomplete."
4. **Avoid superlatives.** "Critical", "absolutely", "must never" — these words add pressure without adding information.

The goal is a prompt that reads like a clear brief from a calm manager — not an urgent demand from a stressed executive.

---

## Related Reading

- Phase 6 (Skills) — The Framed Task Prompt pattern
- Phase 4 (Rules) — Rule 3: Coordination, specifically the checkpoint and think-first patterns
- Phase 9 (Advanced Patterns) — Advanced prompt techniques for complex tasks
