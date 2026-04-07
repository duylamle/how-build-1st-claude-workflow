<div align="center">

# 🏗️ Claude Personal Workflow Builder

**Build, maintain, and grow your AI Personal System with Claude Code.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)
[![skills.sh](https://img.shields.io/badge/skills.sh-compatible-brightgreen)](https://skills.sh)
[![Version](https://img.shields.io/badge/version-v1.1.0-orange)]()

*Agents, skills, rules, hooks, memory — from zero to a working system,
plus upgrade paths and external resource management.*

</div>

---

> 🇻🇳 **Xây dựng, duy trì và phát triển hệ thống AI cá nhân với Claude Code.**
> Từng bước, tương tác, thân thiện với người mới.

---

## 🤔 What is this?

An interactive skill for [Claude Code](https://claude.ai/claude-code) that guides you through building your own **AI Personal System** — a structured workspace where specialized AI agents work together under your direction.

Instead of chatting with AI one-off, you'll build a system that:

- 🎭 Has **specialized agents** (producer, reviewer, analyst) with clear roles
- 📏 Follows **behavioral rules** you define (tone, format, workflow)
- ⚡ Runs **bounded skills** (input → output) for repeatable quality
- 🧠 Accumulates **memory** so AI learns from your corrections over time
- 🔒 Uses **hooks and validators** that auto-enforce your conventions

---

## 💡 Philosophy

> **AI doesn't replace your judgment — it enhances the quality of input so YOU make better decisions.**

You become the engineering manager of your AI team: providing context, setting intent, reviewing output. AI produces drafts and analysis. You decide.

---

## 🚀 Quick Start

```bash
# Install the skill
npx skills add duylamle/product-collection@claude-personal-workflow-builder -y

# In Claude Code, say:
"Build my AI workflow"
# or
"Guide me through setting up my AI system"
```

---

## 📋 The 13 Phases

| # | Phase | What You'll Build |
|---|---|---|
| 0 | **Prerequisites** | Claude Code installed, workspace ready |
| 1 | **Intro** | Understand philosophy + architecture |
| 2 | **Self-Assessment** | Your role, pain points, MVP scope |
| 3 | **Foundation** | Workspace, root CLAUDE.md, folder structure |
| 4 | **Rules** | 3 core behavioral guardrails + overhead budget |
| 5 | **Agents** | Producer + Reviewer (why they must be separate) |
| 6 | **Skills** | Bounded capabilities with templates + framed prompts |
| 7 | **Memory & Knowledge** | Feedback system + domain context |
| 8 | **Hooks & Automation** | Validators, backup, session logging |
| 9 | **Advanced Patterns** | English-first, handoff, parallel agents |
| 10 | **Skill Absorption** | Learn from community skills on skills.sh |
| 11 | **Tuning** | Escalation ladder: feedback → rule → validator |
| 12 | **Iterate & Grow** | Monthly review, publishing, scaling |

> 💨 **Minimum viable path:** Phases 0 → 1 → 3 → 4 → 5 → 6 gets you a working system.

---

## 📁 What's Inside

```
claude-personal-workflow-builder/
├── SKILL.md              ← Skill definition (Claude reads this)
├── README.md             ← You are here
├── guide/                ← 14 detailed guide files (English)
├── templates/            ← 8 starter templates you'll customize
└── examples/             ← 3 complete setups (marketer, developer, manager)
```

---

## 🔑 Key Patterns You'll Learn

Battle-tested patterns from months of real operational use:

| Pattern | Why It Matters |
|---|---|
| **Coordinator, not Orchestrator** | Main context manages everything. No extra agent layer needed |
| **Producer/Reviewer split** | AI that reviews its own work is defensive. Separate them |
| **Framed task prompt** | Brief agents like onboarding a colleague. Prompt quality = output quality |
| **Overhead budget** | Cap auto-load lines. System grows, context cost doesn't |
| **Read before execute** | Don't trust "I remember." Re-read conventions before producing |
| **Validators > willpower** | "Impossible to violate" beats "remember to follow" |
| **Memory decay** | Feedback bloats over time. Archive monthly. Keep context lean |
| **Skill Absorption** | Bootstrap your skill → benchmark vs community → absorb best parts → delete theirs |
| **Consultant Model** | Not everything needs absorbing. Keep external kits as consultants, promote when proven |
| **Upgrade Path** | Re-research → gap analysis → absorb delta. Don't rebuild from scratch |
| **Tuning ladder** | Feedback → Rule → Checklist → Validator → Template. Each level harder to bypass |

---

## 🎯 Examples

The `examples/` folder has complete setups for three roles — ready to adapt:

| Role | Agents Included |
|---|---|
| 📝 **Content Marketer** | Writer + Analyst + Reviewer |
| 💻 **Software Developer** | Doc Writer + Code Reviewer + Debug Assistant |
| 📊 **Product Manager** | Meeting Secretary + Planner + Decision Reviewer |

Each example includes full `CLAUDE.md`, `AGENT.md`, `SKILL.md`, rules, and memory entries.

---

## 🔄 Two Modes

| Mode | Best For |
|---|---|
| **🟢 Guided** (default) | First-time setup — walk through each phase step by step |
| **📋 Menu** | Returning users — jump to any specific phase |

---

## 👤 About the Author / Về tác giả

Built by **Lê Trương Duy Lam** — Technical Product Owner at [VNG Corporation](https://www.vng.com.vn/), building epic products since 2020. This skill distills months of real experience building and operating an AI personal system for product work: PRDs, discovery, strategy, stakeholder management, and team coordination.

Được xây dựng bởi **Lê Trương Duy Lam** — Technical Product Owner tại VNG Corporation. Skill này đúc kết kinh nghiệm thực tế nhiều tháng xây dựng và vận hành hệ thống AI cá nhân cho công việc sản phẩm.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin)](https://www.linkedin.com/in/le-truong-duy-lam/)

---

## 📌 Version

**Current: v1.1.0** (2026-04-07) — See [CHANGELOG.md](CHANGELOG.md) for full history.

---

## 📄 License

[MIT](../../LICENSE) — use it, modify it, share it.