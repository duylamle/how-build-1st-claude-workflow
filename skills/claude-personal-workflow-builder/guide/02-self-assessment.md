# Phase 2 — Self-Assessment

Before configuring anything, figure out what YOUR system should do. A generic AI system helps nobody — yours should target your specific pain points.

---

## Step 1: Identify Your Role and Daily Work

Answer these questions honestly. Write your answers down — you'll reference them throughout the build process.

1. **What is your job title and core responsibility?**
   (e.g., "Product Manager — I define what we build and why")

2. **What do you spend most of your time on?**
   List your top 5 activities by time spent. Be specific — "meetings" is too vague, "aligning stakeholders on feature scope" is better.

3. **What decisions do you make that matter most?**
   These are where AI judgment-enhancement is most valuable.

4. **What do you produce regularly?**
   Documents, reports, analyses, code, plans, content — what artifacts leave your desk?

5. **Who reads your output?**
   Different audiences need different AI roles. Output for executives needs different treatment than output for engineers.

### Self-Assessment Worksheet

Copy this template and fill it in. Spend 10 minutes max — rough answers are better than perfect ones.

```markdown
## My AI System Assessment

**Role:** [your title + one-sentence description of what you do]

**Top 5 time-consuming activities:**
1. [activity] — approx [X] hrs/week
2. [activity] — approx [X] hrs/week
3. [activity] — approx [X] hrs/week
4. [activity] — approx [X] hrs/week
5. [activity] — approx [X] hrs/week

**Highest-stakes decisions I make:**
1. [decision type] — affects [who/what]
2. [decision type] — affects [who/what]

**Artifacts I produce regularly:**
- [artifact type] — [frequency] — read by [audience]
- [artifact type] — [frequency] — read by [audience]
- [artifact type] — [frequency] — read by [audience]

**My top 2-3 pain points (from Step 2):**
1. [pain point]
2. [pain point]
3. [pain point — optional]

**My MVP scope (from Step 4):**
- Producer agent will: [what it produces]
- Reviewer agent will: [what it checks]
- Think skill will: [what it frames/analyzes before production]
```

---

## Step 2: Find Your 2-3 Biggest Pain Points

Look at your answers above. Where do you feel the most friction? Common patterns:

| Pain point | Signal |
|---|---|
| "I spend hours writing documents that could be drafted faster" | Production bottleneck |
| "I keep making the same mistakes in my specs" | Missing quality gates |
| "Every meeting generates action items nobody tracks" | Missing operational support |
| "I review my own work and miss obvious gaps" | Missing independent review |
| "I explain the same context to AI every single time" | Missing persistent context |
| "I don't know if my strategy is solid until it fails" | Missing upfront analysis |
| "I synthesize information from many sources into reports" | Missing structured synthesis |
| "I need to produce content that matches a brand/tone consistently" | Missing style enforcement |

Pick your top 2-3. These become your MVP scope.

---

## Step 3: Map Pain Points to AI Roles

Different pain points need different AI roles. Here's a mapping table with examples across professions:

| Your role | Common pain points | AI roles to build |
|---|---|---|
| **Product Manager** | Writing PRDs takes too long; specs have gaps QC finds later; no one challenges assumptions before dev starts | Producer (drafts PRDs), Reviewer (challenges before handoff), Analyst (frames problems) |
| **Software Developer** | Documentation is always outdated; PR reviews miss architectural issues; debugging is slow | Doc Writer (generates/updates docs), Code Reviewer (architectural review), Debug Assistant |
| **Marketer** | Content takes forever; messaging is inconsistent; campaign analysis is manual | Content Writer (drafts), Brand Reviewer (consistency check), Analyst (campaign data) |
| **Researcher** | Literature synthesis is tedious; interview analysis takes days; report writing is painful | Synthesizer (combines sources), Interview Analyst (extracts themes), Report Writer |
| **Designer** | Writing design rationale is slow; user research synthesis; spec handoff gaps | Rationale Writer, Research Synthesizer, Spec Reviewer |
| **Consultant** | Client deliverables take too long; frameworks need adapting per engagement; proposal writing is repetitive | Deliverable Producer (adapts frameworks), Proposal Writer (structured drafts), Quality Reviewer (checks rigor) |
| **Startup Founder** | Wearing too many hats; investor materials need constant updating; strategy keeps shifting without documentation | Strategy Writer (vision/pitch docs), Ops Assistant (tracks decisions), Challenger (stress-tests plans) |
| **Manager/Lead** | Meeting notes are lost; decisions aren't tracked; planning documents are inconsistent | Secretary (meeting notes + follow-up), Planner (structured plans), Reviewer (consistency) |

> **Why this matters:** Starting with pain points (not capabilities) ensures you build something you'll actually use. Most abandoned AI setups fail because they were designed around "cool things AI can do" instead of "problems I need solved." The mapping above comes from patterns across dozens of real implementations.

---

## Red Flags: When NOT to Use AI

Not every task benefits from an AI system. Watch for these signs that a task is a poor fit:

**Tasks requiring real-time human judgment:**
- Live negotiations, sensitive personnel conversations, crisis communication
- AI can help you prepare (talking points, scenario planning), but the execution must be human

**Taste-based creative decisions:**
- "Does this logo feel right?" or "Is this marketing copy on-brand?"
- AI can generate options, but the selection is pure human taste. Don't outsource your aesthetic judgment.

**Politically sensitive decisions:**
- Anything where the decision process matters as much as the decision itself
- "Who gets promoted," "which team loses headcount," "how to communicate layoffs"
- AI can help structure your thinking, but the decision and communication must be visibly yours

**Tasks with rapidly changing ground truth:**
- If the facts change faster than you can update knowledge files, AI will work from stale context
- Breaking news analysis, live market trading, real-time incident response

**Tasks where being wrong has irreversible consequences:**
- Legal filings, medical diagnoses, financial compliance certifications
- AI can draft, but a qualified human must verify before submission

The pattern: AI is great at production, synthesis, and structured analysis. AI is poor at judgment calls that require human accountability, real-time adaptation, or taste.

---

## Step 4: Choose Your MVP Scope

**Start with exactly 2 roles:**

1. **One Producer** — the role that creates your most common output
2. **One Reviewer** — the role that independently challenges that output

Why only 2? Because:
- You need to learn the system by using it, not designing it
- Producer + Reviewer is the minimum pattern that actually works (self-review doesn't)
- Adding more roles is easy once the foundation works

**Then add 1 "think" skill** — a procedure that frames problems before the producer starts working. This prevents the most common failure: producing the wrong thing efficiently.

Your MVP: **Think -> Produce -> Review**

### MVP Planning Template

Fill this in before starting Phase 3:

```markdown
## My MVP System

**My first 2 agents will be:**
1. Producer: ___ (what it produces — e.g., "drafts product specs")
2. Reviewer: ___ (what it checks — e.g., "finds gaps and weak assumptions in specs")

**My first 3 skills will be:**
1. Think: frames the problem before production (standard for everyone)
2. [Produce skill]: ___ (e.g., "write-prd", "draft-report", "create-proposal")
3. Challenge: reviews output from a critical perspective (standard for everyone)

**My first domain-specific template will be:**
- [template name]: ___ (e.g., "PRD template with sections for problem, solution, AC, edge cases")

**Success looks like:**
- After 5 real tasks, I spend [less/more] time on ___ and the output quality is [better/same/worse] than doing it myself.
```

---

## Step 5: Define "Good Enough"

For each role, write one sentence describing what "good output" looks like:

**Producer:** "A first draft that covers 80% of what I need, so I spend time refining rather than writing from scratch."

**Reviewer:** "A list of 3-5 genuine weaknesses or gaps, ranked by severity, that I hadn't noticed."

These become your quality criteria later. Don't over-specify now — you'll refine through actual use.

---

## Warning: Don't Over-Design

If you're spending more than 30 minutes on this assessment, stop. You have enough to start building.

The most common mistake is designing an elaborate 10-agent system on paper before ever using it. Real insight comes from running 5 real tasks through a minimal system and seeing where it breaks.

**Build minimal. Use it. Fix what breaks. Repeat.**

Your self-assessment will change after a week of actual use — and that's exactly right.

---

## Checklist Before Moving On

- [ ] I know my top 2-3 pain points
- [ ] I've picked 2 AI roles (producer + reviewer) that address them
- [ ] I can describe "good output" for each role in one sentence
- [ ] I resisted the urge to design 10 roles
- [ ] I filled in the MVP Planning Template (at least roughly)

---

## Start Here: Prompts for Phase 3

Once you've completed this assessment, you can start Phase 3 by saying any of these to Claude Code:

- **"Create the folder structure for my AI personal system in this directory."** — Claude will set up the workspace folders.
- **"I want to build a personal AI system. My role is [your role] and my biggest pain point is [pain point]. Help me create a CLAUDE.md."** — Claude will help you write the root context file.
- **"Read 03-foundation.md and walk me through setting up my workspace step by step."** — If you want guided setup.

You don't need to memorize the architecture. Claude Code can build the scaffolding for you — you just need to know what you want the system to do (which you now do from this assessment).

---

## Next Step

Move to [03-foundation.md](./03-foundation.md) to create your workspace and folder structure.
