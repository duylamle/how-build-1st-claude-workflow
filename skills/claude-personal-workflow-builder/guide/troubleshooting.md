# Troubleshooting

Common problems and how to fix them. Each entry follows: **Problem → Cause → Fix.**

---

## Agent Doesn't Trigger

**Problem:** You ask for something and the wrong agent handles it, or no agent is spawned at all.

**Cause:** Claude matches intent by reading the `description` field in AGENT.md. If the description doesn't contain keywords matching your request, Claude won't route to that agent.

**Fix:**
1. Open the agent's AGENT.md
2. Check the `description` field — does it contain trigger keywords for your request?
3. Add relevant keywords. Example: if you want "write a spec" to trigger your producer agent, the description should include "spec" or "specification"
4. Check `.claude/agents/CLAUDE.md` — is the agent listed there?

---

## Skill Doesn't Match

**Problem:** The right agent is triggered, but it doesn't use the skill you expected.

**Cause:** The skill's `description` field in SKILL.md doesn't contain specific enough trigger keywords. Or the skill isn't listed in the agent's `skills:` list in AGENT.md.

**Fix:**
1. Check SKILL.md `description` — are trigger keywords present and specific?
2. Check the agent's AGENT.md `skills:` list — is this skill included?
3. If multiple skills could match, make descriptions more distinct. "Write a PRD" and "write a vision doc" should trigger different skills with clear keyword boundaries.

---

## Hook Fails Silently

**Problem:** A hook (pre-write validator, post-session task) doesn't seem to run.

**Cause:** Usually one of: invalid JSON in `settings.local.json`, wrong script path, missing script permissions, or script error that's swallowed.

**Fix:**
1. Validate `settings.local.json` syntax — paste into a JSON validator
2. Check script path — must be correct relative to your workspace root
3. Run the script manually to see error output:
   ```bash
   python .claude/scripts/validators/your-validator.py test-file.md
   ```
4. Check that Python is available in your PATH
5. On Windows: check that the bash command in the hook config uses forward slashes

---

## Context Too Long / Quality Drops

**Problem:** AI starts forgetting earlier instructions, output quality degrades, or you see compression warnings.

**Cause:** Your always-load rules + root CLAUDE.md exceed the context budget. AI has to process too many instructions before doing real work, leaving less room for reasoning about your actual task.

**Fix:**
1. Count total lines of always-load rules + root CLAUDE.md
2. If over budget (e.g., 900 lines), trim:
   - Move less-critical rules to on-demand
   - Remove verbose explanations (keep constraints, cut rationale)
   - Merge related rules into fewer files
3. Check if knowledge files are being loaded unnecessarily — they should be on-demand, not always-load

---

## Agent Produces Wrong Format

**Problem:** Agent output doesn't match the expected structure — sections missing, wrong headings, improvised format.

**Cause:** The skill either doesn't point to a template, or the prompt sent to the agent didn't include the template path. Without a template, AI improvises.

**Fix:**
1. Check SKILL.md — does it reference a TEMPLATE.md?
2. Check the prompt you (or the coordinator) sent — did it include the template path?
3. Add explicit instruction in the prompt: "Read template at [path] before writing. Follow its structure exactly."
4. If the template exists but output still diverges, add `EXAMPLE-*.md` files showing approved output

---

## Agent Asks Questions That Were Already Answered

**Problem:** You already decided something in conversation, but the spawned agent asks about it again.

**Cause:** Agents start with a blank slate. They don't see conversation history. Your prompt didn't include confirmed decisions.

**Fix:** Add a "Decisions already confirmed" section to your prompt:

```
Decisions already confirmed:
1. Scope is drag-and-drop only, no folder upload
2. Max file size: 5MB
3. User confirmed: no need for progress bar in v1
```

The agent sees this list and doesn't question or suggest alternatives for these items.

---

## Memory Not Being Read

**Problem:** You saved feedback last session, but AI doesn't seem to know about it this session.

**Cause:** Memory is on-demand, not auto-loaded. Claude only reads memory entries when the current task seems related to stored feedback. If the task doesn't trigger a memory scan, your feedback sits unread.

**Fix:**
- If you want Claude to check, say explicitly: "Check memory for relevant feedback before starting"
- For critical feedback that must be applied every session, graduate it to a rule (Level 2 on the escalation ladder)
- Make sure your memory index (`_INDEX.md`) has clear descriptions so Claude can match relevance

---

## Validator Blocks Legitimate Work

**Problem:** A validator hook rejects output that's actually correct.

**Cause:** The validator is too strict or has a bug. Common case: validator checks for fields that are optional in some contexts but required in others.

**Fix:**
1. Read the validator script — identify the specific check that's failing
2. Fix the logic to handle the legitimate case
3. If you need to unblock immediately: temporarily disable the hook in `settings.local.json` (comment it out or remove it), do your work, then re-enable after fixing
4. Add a test case for the legitimate scenario so it doesn't regress

---

## Output Language Issues

**Problem:** If using English-first workflow, the final translated output has garbled characters, missing accents, or encoding issues.

**Cause:** Known issue with AI subagents producing text in non-Latin scripts. The subagent may produce correct English but the translation step (or direct non-English production) can introduce encoding errors.

**Fix:**
1. After any agent returns non-English output, **always read the file back** and verify encoding
2. If characters are garbled, rewrite the file
3. For critical artifacts, have the coordinator (main context) do the translation instead of the subagent
4. Add a rule or checklist item: "After writing non-English file, read it back and verify diacritics display correctly"

---

## "I Already Told You This" Frustration

**Problem:** You keep correcting the same behavior across sessions. It feels like AI has amnesia.

**Cause:** You're telling AI in conversation, but not saving the correction anywhere persistent. Each new session starts fresh.

**Fix:** Use the escalation ladder (Phase 11):

1. **First time:** save as feedback (memory entry)
2. **Third time:** graduate to a rule
3. **Still happening:** add a checklist or validator
4. **Format/style issue:** add template + approved examples

The fix is always the same: move the correction from your memory to the system's memory. The harder the mechanism, the more reliably it sticks.

---

## Agent Output Is Too Generic / Shallow

**Problem:** Agent produces technically correct but shallow output that doesn't reflect your specific context.

**Cause:** The prompt lacked sufficient context. Agent doesn't know your domain, your audience, or your standards.

**Fix:**
1. Check your prompt — did you include background on why this task exists?
2. Did you point to relevant knowledge files (company context, team info, system docs)?
3. Did you include decisions already confirmed?
4. Consider using Full prompt tier instead of Lite (see Phase 9 — Framed Task Prompt)
5. Add approved examples (`EXAMPLE-*.md`) so the agent sees what "good" looks like in your context

---

## System Feels Overwhelming

**Problem:** Too many agents, skills, rules, and files. You're not sure what's being used and what's dead weight.

**Cause:** System grew organically without pruning. Common after the first few months of enthusiastic building.

**Fix:**
1. Run the monthly maintenance ritual (Phase 11)
2. For each agent: when did you last use it? If >1 month ago, consider removing
3. For each skill: same question. Unused skills are pure overhead
4. For each rule: is AI actually following it? If you can't tell, it might not matter
5. Consolidate: can two similar agents merge? Can two overlapping skills become one?
6. Goal: get back to a system where you know what every file does and why it exists
