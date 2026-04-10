---
name: claude-personal-workflow-builder
description: >
  Interactive guide to build, maintain, and grow your AI Personal System
  with Claude Code. Agents, skills, rules, hooks, memory — from zero
  to a working system, plus upgrade paths and external resource management.
  Trigger: "build my AI workflow", "setup AI system",
  "how to build claude workflow", "AI personal system".
---

# Claude Personal Workflow Builder

> Hướng dẫn từng bước xây dựng hệ thống AI cá nhân với Claude Code.
> Từ con số 0 đến hệ thống hoạt động với agents, skills, rules, memory.

## What This Skill Does

This skill guides you through building a complete AI Personal System —
a structured thinking space where specialized AI agents work together
under your direction. You become the engineering manager of your AI team.

Skill này dẫn bạn qua từng bước xây dựng hệ thống AI cá nhân hoàn chỉnh —
nơi các AI agents chuyên biệt làm việc cùng nhau dưới sự điều phối của bạn.

## How to Use

**Three modes:**

- **Guided** (default) — Say "build my AI workflow" or "guide me through
  setting up my AI system". I'll walk you through each phase, asking for
  your input and generating files at each step.

- **Menu** — Say "show me the phases" or "I want to jump to phase 5".
  I'll show all 13 phases and you pick which one to work on.

- **Consult** — Say "I have a question about my AI system" or "consult
  about agents". I answer questions, troubleshoot issues, and advise on
  design decisions — no step-by-step walkthrough, just direct Q&A.
  Best for people who already have a system or want to understand
  concepts before building.

## The 13 Phases

| # | Phase | What you'll build |
|---|---|---|
| 0 | Prerequisites | Claude Code installed, workspace ready |
| 1 | Intro | Understand philosophy + architecture |
| 2 | Self-Assessment | Your role, pain points, MVP scope |
| 3 | Foundation | Workspace, root CLAUDE.md, folder structure |
| 4 | Rules | 3 core behavioral guardrails |
| 5 | Agents | Producer + Reviewer agents |
| 6 | Skills | 2-3 bounded capabilities with templates |
| 7 | Memory & Knowledge | Feedback system + domain context |
| 8 | Hooks & Automation | Validators, backup, session logging |
| 9 | Advanced Patterns | English-first, framed task, handoff |
| 10 | Skill Absorption | Learn from community skills |
| 11 | Tuning | Escalation ladder for improving output |
| 12 | Iterate & Grow | Monthly review, publishing, scaling |

**Quick start:** Phases 0 → 1 → 3 are required foundation. Then pick what
you need — just skills (6)? Rules + skills (4 + 6)? Full system with agents
(4 + 6 + 5 + 7)? See Phase 1 for flexible reading paths.

## Instructions for Claude

When the user triggers this skill:

1. Ask: "Which mode? Guided (step by step), Menu (pick a phase), or
   Consult (ask me anything about AI systems)?"
2. **Guided mode**: Start at Phase 0. For each phase:
   - Read the corresponding guide file from `guide/0X-*.md`
   - Explain the concepts and why they matter
   - Ask the user for their specific input (role, preferences, domain)
   - Generate files in their workspace using `templates/` as base
   - Show what was created, ask if ready for next phase
3. **Menu mode**: Show the phase table above. User picks a phase.
   Read and execute that phase's guide file.
4. **Consult mode**: Answer questions directly using guide files,
   references, and examples as knowledge base. No walkthrough — just
   focused answers with relevant context. Read the specific guide/reference
   files that relate to the user's question. If the user describes their
   current setup, give tailored advice (what to add, what to change,
   what to skip).
5. Reference `examples/` when the user asks "show me what this looks
   like for a [role]" — we have PO, marketer, developer, and manager examples.
6. After each phase, briefly note what was accomplished and what comes next.

### Key principles to follow while guiding:
- Ask before generating — understand the user's role and needs first
- Generate files into their workspace, not abstractly
- Use templates/ as starting points, customize based on user input
- When user seems overwhelmed, remind them of the quick start path
- Each phase should feel like a conversation, not a lecture
- Reference `references/` when users ask about external research,
  RAG architectures, prompt techniques, or enterprise AI platforms
