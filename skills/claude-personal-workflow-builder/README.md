<div align="center">

# 🏗️ Claude Personal Workflow Builder

**Build, maintain, and grow your AI Personal System with Claude Code.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](../../LICENSE)
[![skills.sh](https://img.shields.io/badge/skills.sh-compatible-brightgreen)](https://skills.sh/duylamle/product-collection/claude-personal-workflow-builder)
[![Version](https://img.shields.io/badge/version-v2.0.0-orange)](CHANGELOG.md)
[![Made with Claude Code](https://img.shields.io/badge/Made_with-Claude_Code-blueviolet?logo=anthropic)](https://claude.ai/claude-code)
[![Last Commit](https://img.shields.io/github/last-commit/duylamle/product-collection)](https://github.com/duylamle/product-collection)

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
| 0 | [**Prerequisites**](guide/00-prerequisites.md) | Claude Code installed, workspace ready |
| 1 | [**Intro**](guide/01-intro.md) | Understand philosophy + architecture |
| 2 | [**Self-Assessment**](guide/02-self-assessment.md) | Your role, pain points, MVP scope |
| 3 | [**Foundation**](guide/03-foundation.md) | Workspace, root CLAUDE.md, folder structure |
| 4 | [**Rules**](guide/04-rules.md) | 3 core behavioral guardrails + overhead budget |
| 5 | [**Agents**](guide/05-agents.md) | Producer + Reviewer (why they must be separate) |
| 6 | [**Skills**](guide/06-skills.md) | Bounded capabilities with templates + framed prompts |
| 7 | [**Memory & Knowledge**](guide/07-memory-knowledge.md) | Feedback system + domain context |
| 8 | [**Hooks & Automation**](guide/08-hooks-automation.md) | Validators, backup, session logging |
| 9 | [**Advanced Patterns**](guide/09-advanced-patterns.md) | English-first, handoff, parallel agents |
| 10 | [**Skill Absorption**](guide/10-skill-absorption.md) | Learn from community skills on skills.sh |
| 11 | [**Tuning**](guide/11-tuning.md) | Escalation ladder: feedback → rule → validator |
| 12 | [**Iterate & Grow**](guide/12-iterate-grow.md) | Monthly review, publishing, scaling |

> 💨 **Minimum viable path:** Phases 0 → 1 → 3 are foundation. Then pick what you need — just skills (6)? Rules + skills (4 + 6)? Full system (4 + 6 + 5 + 7)? See Phase 1 for flexible paths.

---

## 📁 What's Inside

```
claude-personal-workflow-builder/
├── [SKILL.md](SKILL.md)        ← Skill definition (Claude reads this)
├── README.md                    ← You are here
├── [guide/](guide/)             ← 13 detailed guide files (English)
├── [templates/](templates/)     ← 8 starter templates you'll customize
└── [examples/](examples/)       ← 3 complete setups (marketer, developer, manager)
```

---

## 🔑 Key Patterns You'll Learn

Battle-tested patterns from months of real operational use:

| Pattern | Why It Matters |
|---|---|
| [**Coordinator, not Orchestrator**](guide/09-advanced-patterns.md) | Main context manages everything. No extra agent layer needed |
| [**Producer/Reviewer split**](guide/05-agents.md) | AI that reviews its own work is defensive. Separate them |
| [**Framed task prompt**](guide/09-advanced-patterns.md) | Brief agents like onboarding a colleague. Prompt quality = output quality |
| [**Overhead budget**](guide/04-rules.md) | Cap auto-load lines. System grows, context cost doesn't |
| [**Read before execute**](guide/04-rules.md) | Don't trust "I remember." Re-read conventions before producing |
| [**Validators > willpower**](guide/08-hooks-automation.md) | "Impossible to violate" beats "remember to follow" |
| [**Memory decay**](guide/07-memory-knowledge.md) | Feedback bloats over time. Archive monthly. Keep context lean |
| [**Skill Absorption**](guide/10-skill-absorption.md) | Bootstrap your skill → benchmark vs community → absorb best parts → delete theirs |
| [**Consultant Model**](guide/10-skill-absorption.md) | Not everything needs absorbing. Keep external kits as consultants, promote when proven |
| [**Upgrade Path**](guide/12-iterate-grow.md) | Re-research → gap analysis → absorb delta. Don't rebuild from scratch |
| [**Tuning ladder**](guide/11-tuning.md) | Feedback → Rule → Checklist → Validator → Template. Each level harder to bypass |

---

## 🎯 Examples

The `examples/` folder has complete setups for three roles — ready to adapt:

| Role | Agents Included |
|---|---|
| 📋 [**Product Owner**](examples/po-setup.md) | PO + Challenger + Secretary |
| 📝 [**Content Marketer**](examples/marketer-setup.md) | Writer + Analyst + Reviewer |
| 💻 [**Software Developer**](examples/developer-setup.md) | Doc Writer + Code Reviewer + Debug Assistant |
| 📊 [**Product Manager**](examples/manager-setup.md) | Meeting Secretary + Planner + Decision Reviewer |

Each example includes full `CLAUDE.md`, `AGENT.md`, `SKILL.md`, rules, and memory entries.

---

## 🔄 Three Modes

| Mode | Best For |
|---|---|
| **🟢 Guided** (default) | First-time setup — walk through each phase step by step |
| **📋 Menu** | Returning users — jump to any specific phase |
| **💬 Consult** | Q&A — ask about concepts, troubleshoot issues, get design advice |

---

## 👤 About the Author / Về tác giả

Built by **Lê Trương Duy Lam** — Technical Product Owner at [VNG Corporation](https://www.vng.com.vn/), building epic products since 2020. This skill distills months of real experience building and operating an AI personal system for product work: PRDs, discovery, strategy, stakeholder management, and team coordination.

Được xây dựng bởi **Lê Trương Duy Lam** — Technical Product Owner tại VNG Corporation. Skill này đúc kết kinh nghiệm thực tế nhiều tháng xây dựng và vận hành hệ thống AI cá nhân cho công việc sản phẩm.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin)](https://www.linkedin.com/in/le-truong-duy-lam/)

---

## 📌 Version

**Current: v2.0.0** (2026-04-10) — See [CHANGELOG.md](CHANGELOG.md) for full history.

---

<p align="center">
  Thanks for visiting <b>Claude Personal Workflow Builder</b>
  <br><br>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=duylamle.product-collection.workflow-builder&style=flat" alt="visitors"/>
</p>

## 📄 License

[MIT](../../LICENSE) — use it, modify it, share it.