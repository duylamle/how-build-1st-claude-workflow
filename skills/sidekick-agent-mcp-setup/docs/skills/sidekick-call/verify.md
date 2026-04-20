# Sidekick Verify Checklist

Run before persisting sidekick output to a file or forwarding it to the user.

## 1. Shape matches request

- [ ] `summarize`: exactly `max_bullets` bullets, no sub-bullets
- [ ] `translate`: markdown structure preserved (headings, lists, tables, code fences)
- [ ] No preamble ("Here's…", "Sure,…", "Đây là tóm tắt:")
- [ ] No postamble ("Hope this helps…", "Let me know if…")
- [ ] For JSON-by-prompt tasks: parses as valid JSON (the senior should run
      `json.loads` before persisting)

## 2. Encoding

- [ ] Non-ASCII characters render correctly (no "?" or mojibake)
- [ ] Special characters intact (quotes, em-dash, fullwidth, diacritics)
- [ ] No BOM or control chars at the start of output

## 3. Faithfulness (hallucination guard)

- [ ] Spot-check 2-3 specific facts against the source (numbers, names, dates)
- [ ] No fact in the output that isn't in the source
- [ ] No opinion / recommendation if the task didn't ask for one

## 4. Safety envelope

- [ ] `INSUFFICIENT_INPUT:` → surface verbatim, don't fill gaps yourself
- [ ] `REJECTED_PATHS:` → surface verbatim, don't retry a different path
      without asking the user
- [ ] `SIDEKICK_ERROR:` → transient; retry once or escalate
- [ ] `SIDEKICK_WARNING: iteration cap` / `repeated_tool_failure` → review
      trace before continuing

## 5. Agent-run specific

- [ ] Trace reviewed — every tool call looks reasonable for the task
- [ ] No unexpected writes (writes only to paths in `write_allowlist`)
- [ ] Final text addresses the task, not just reports exploration
- [ ] Repeated-error warnings investigated (bad path? missing allowlist?)

## 6. Action on failure

- **Minor** (strip preamble, fix formatting slip): senior fixes inline
- **Structural** (wrong bullet count, translation drift, malformed JSON):
  re-call with a tighter prompt OR do it yourself
- **Factual** (hallucinated fact, wrong number): discard output and do it
  yourself — don't try to patch
