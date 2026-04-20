<div align="center">

# 🧰 Product Collection

**Claude Code skills for people who build products.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.4.0-orange)](CHANGELOG.md)
[![skills.sh](https://img.shields.io/badge/skills.sh-compatible-brightgreen)](https://skills.sh/duylamle/product-collection)
[![Made with Claude Code](https://img.shields.io/badge/Made_with-Claude_Code-blueviolet?logo=anthropic)](https://claude.ai/claude-code)
[![Last Commit](https://img.shields.io/github/last-commit/duylamle/product-collection)](https://github.com/duylamle/product-collection)

</div>

---

## Why this exists

This isn't trying to replace the powerful, feature-rich skills already out there. Those are great — if you're technical enough to understand them.

This collection fills a different gap: **the space between Tech and Product.** As a non-tech Product Owner who learned to build AI workflows from scratch, Lam found that most existing tools assume you already know what you're doing. They don't explain *why*, just *how*.

Every skill here comes from real daily product work — simple frameworks that are easy to understand, practical enough for everyday use, and built by someone who had to figure it all out without an engineering background.

If you're a product person, a manager, or anyone non-technical trying to make [Claude Code](https://claude.ai/claude-code) actually work for you — this is your starting point. Zero to one, at your own pace.

---

## 🚀 Install everything

```bash
npx skills add duylamle/product-collection -y
```

This installs all skills in the collection. See each skill below for usage instructions.

---

## 📦 Skills

### 1. Claude Personal Workflow Builder

[![View Skill — v2.0.0](https://img.shields.io/badge/View_Skill-v2.0.0-orange)](skills/claude-personal-workflow-builder/README.md)

An interactive guide to build, maintain, and grow your AI Personal System with Claude Code — specialized agents, behavioral rules, bounded skills, memory, hooks. 13 phases from zero to a working system.

**What you'll learn:**
- How to structure agents (producer vs reviewer — and why they must be separate)
- How to write skills that produce consistent output
- How to upgrade skills and manage external resources (community skills, kits, npm packages)
- 12 proven patterns from real operational use

```bash
npx skills add duylamle/product-collection@claude-personal-workflow-builder -y
```

### 2. Pug Mockup

[![View Skill — v1.1.0](https://img.shields.io/badge/View_Skill-v1.1.0-orange)](skills/pug-mockup/README.md)

Generate self-contained SPA mockups using Pug template engine + Lucide SVG icons. Single HTML output — works offline, share with anyone.

**Why Pug for AI mockups:**
- ~40-50% fewer tokens than HTML — AI writes more UI in less context
- Mixin = component reuse without frameworks
- Self-contained output — CSS/JS inlined, no server needed
- Not a dead-end — ~60-70% reusable in React/Next.js/Vue

```bash
npx skills add duylamle/product-collection@pug-mockup -y
```

### 3. Excel Pipeline

[![View Skill — v1.0.0](https://img.shields.io/badge/View_Skill-v1.0.0-orange)](skills/excel-pipeline/README.md)

Parse multi-source data (Excel, CSV, markdown) into JSONL, then export to formatted Excel with formulas, lookups, and conditional highlighting. Full pipeline: parse → merge → audit → diff → export.

**Why JSONL as intermediate format:**
- Plain text — AI reads and writes it natively (unlike binary Excel)
- One record per line — easy to merge from multiple sources
- Version-diffable — compare old vs new to see what changed
- Reproducible — re-run pipeline anytime with updated source

```bash
npx skills add duylamle/product-collection@excel-pipeline -y
```

### 4. Sidekick Setup

[![View Skill — v1.0.0](https://img.shields.io/badge/View_Skill-v1.0.0-orange)](skills/sidekick-agent-mcp-setup/README.md)

Install the [sidekick-agent MCP server](https://github.com/ltdlam/sidekick-agent-mcp) and start shifting tokens from your expensive senior Claude to a cheaper junior LLM (Claude Haiku, OpenRouter, MiniMax via LiteLLM, or self-hosted). Covers install, backend config, Claude Code registration, delegation rule, and a nested `sidekick-call` companion skill for day-to-day use.

**Controlled token shift, not outsourcing:**
- Senior frames narrow scope for the junior — junior never guesses
- Senior verifies junior output before persisting — encoding, facts, shape
- One MCP call = one action; multi-step work is a chain of calls the senior orchestrates
- Bundles the delegation rule + call skill — install one, get everything

```bash
npx skills add duylamle/product-collection@sidekick-agent-mcp-setup -y
```

> More skills coming. Each is self-contained with its own guide, templates, and examples.

---

## 👤 About

Built by **Lê Trương Duy Lam** — Technical Product Owner at [VNG Corporation](https://www.vng.com.vn/), building products since 2020. These skills are distilled from running an AI personal system for product work every day — PRDs, discovery, strategy, stakeholder management, and team coordination.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin)](https://www.linkedin.com/in/le-truong-duy-lam/)

---

---

<p align="center">
  Thanks for visiting <b>Product Collection</b>
  <br><br>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=duylamle.product-collection&style=flat" alt="visitors"/>
</p>

## 📄 License

[MIT](LICENSE) — use it, modify it, share it.
