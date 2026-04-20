---
type: artifact
scope: sidekick-call
created: 2026-04-20
updated: 2026-04-20
---

# Sidekick Use Cases

Real scenarios where shifting work to the junior pays off. Each case shows
**the problem**, **what you say to Claude**, **what Claude does**, and
**token impact** (rough estimate — actual varies by backend).

Pattern across all cases: senior Claude frames the narrow scope → junior
executes → senior verifies → senior decides what to persist or act on.

---

## 1. Summarize a long PRD before review

**Problem:** PM drops a 12k-word PRD in your workspace. You want the gist
before reading fully, or want Claude to write a response without loading
the whole PRD into its context.

**You say:**
> "Nhờ sidekick tóm PRD `inworking/prd-upload-files-v3.md` thành 7 bullet
> tập trung vào AC và business rules."

**What Claude does:**
```
sidekick_summarize(
  file_paths=["inworking/prd-upload-files-v3.md"],
  max_bullets=7,
  focus="acceptance criteria and business rules",
)
```
Claude verifies the bullets match the source (spot-check 2-3 facts),
then asks what to do next — write a challenge? Draft a Jira story? Reply
in chat? All downstream work uses the 7 bullets as context instead of
the full 12k words.

**Token impact:** ~15-25k tokens shifted (full PRD stays out of senior
context). Senior spends tokens only on what comes next.

---

## 2. Translate a research doc VN → EN for leadership

**Problem:** You wrote a 4k-word research note in Vietnamese. Leadership
reads English. You need a faithful translation that preserves markdown
structure (headings, tables, bullet lists, code blocks).

**You say:**
> "Sidekick dịch `research/nghien-cuu-zingcard.md` sang EN tone formal
> cho C-level."

**What Claude does:**
```
sidekick_translate(
  file_paths=["research/nghien-cuu-zingcard.md"],
  target_language="en",
  tone="formal, C-level audience",
)
```
Claude verifies encoding (no mojibake, no lost diacritics in proper
nouns), checks 2-3 technical terms were translated consistently, then
saves to `research/nghien-cuu-zingcard-en.md`.

**Token impact:** ~8-15k tokens shifted (input × 2 for translation
output, but all on the junior). Senior-side cost: just the verification
pass.

---

## 3. Extract action items from meeting notes

**Problem:** 3 meetings this week, raw notes totaling 6k words. You want
a clean action-item list — owner, deadline, status — in a table.

**You say:**
> "Nhờ sidekick extract action items từ 3 files trong `meetings/2026-04/`,
> format table `| owner | action | deadline | status |`."

**What Claude does:**
```
sidekick_task(
  file_paths=[
    "meetings/2026-04/2026-04-15-sync.md",
    "meetings/2026-04/2026-04-17-review.md",
    "meetings/2026-04/2026-04-19-plan.md",
  ],
  task="Extract every action item with owner + deadline + status. "
       "Preserve the exact wording of the action. If a field is missing, "
       "write [TBD]. Return a markdown table only — no prose.",
  output_format="markdown",
  constraints=["No preamble", "Only the table"],
)
```
Claude verifies row count matches expected (quick scan of source),
checks 2-3 action items verbatim, then persists to `meetings/2026-04/action-items.md`.

**Token impact:** ~10k tokens shifted. Senior uses the clean table as
input for "who's blocked", "what slipped", or a Jira bulk-create.

---

## 4. Draft v0 of a Jira story from a feature note

**Problem:** You have a 1-page feature description in `inworking/`. You
need a Jira story: title + description + 3-5 AC in Gherkin. Writing v0
yourself costs 10 minutes of senior thinking on structure — the creative
part (what's really being built) already lives in the feature note.

**You say:**
> "Sidekick draft 1 Jira story từ `inworking/feature-save-card.md` —
> title, description 2 đoạn, 4 AC dạng Given/When/Then. Dùng safeguards."

**What Claude does:**
```
sidekick_task(
  file_paths=["inworking/feature-save-card.md"],
  task="Draft a Jira story from this feature note. Structure:\n"
       "# Title\n\n"
       "## Description (2 paragraphs: context + scope)\n\n"
       "## Acceptance Criteria (exactly 4, Given/When/Then format)\n\n"
       "Mark [ASSUMPTION: ...] for anything you infer that isn't in the source.",
  output_format="markdown",
  safeguards=True,
)
```
Claude reviews — the structure is mechanical, but the content needs
judgment. Claude tightens the title, rewrites one AC that was too vague,
removes an assumption that conflicts with the rule file, then persists.

**Token impact:** ~5k tokens shifted (draft v0 on junior). Senior spends
tokens on the judgment edits, not the boilerplate.

---

## 5. Scan a folder for references to a deprecated API

**Problem:** You're deprecating endpoint `POST /v1/transfer`. You need
to find every doc, spec, and README that mentions it so you can update
them before release.

**You say:**
> "Nhờ sidekick scan toàn bộ `knowledge/` tìm ref đến `/v1/transfer`,
> liệt kê file path + line number + context 1 dòng. Chỉ đọc, không ghi."

**What Claude does:**
```
sidekick_agent_run(
  task="Scan the knowledge/ folder for any mention of '/v1/transfer' "
       "(as a string, case-insensitive). For each hit, report: "
       "file path, line number, and the one line containing the mention. "
       "Return a markdown list grouped by file. Do not write anything.",
  write_allowlist=[],  # explicit read-only
  max_iterations=10,
)
```
Claude sees the final list + tool-call trace, spot-checks 2-3 hits in
source (confirms file/line match), then decides the next step: batch
update those files, or file a ticket to the dev team.

**Token impact:** ~20-40k tokens shifted (the folder walk + file reads
happen on the junior). Senior reads only the final compact list.

---

## 6. Classify feedback entries for prioritization

**Problem:** 47 entries in `feedback/raw.md` — customer messages, bug
reports, feature requests mixed together. You want them tagged:
`bug | feature | question | complaint | praise` so you can prioritize.

**You say:**
> "Sidekick classify 47 entries trong `feedback/raw.md` — thêm tag vào
> đầu mỗi entry. Format: `[tag] original text`. Nếu không chắc, tag
> `[question]` + mark `[TBD: reason]`."

**What Claude does:**
```
sidekick_task(
  file_paths=["feedback/raw.md"],
  task="For every feedback entry (separated by blank lines or ---), "
       "prepend one of these tags: [bug], [feature], [question], "
       "[complaint], [praise]. Keep the original text verbatim after "
       "the tag. If uncertain, tag [question] and add [TBD: reason] "
       "on the next line.",
  output_format="plain",
  constraints=["Preserve entry separators", "Preserve original wording"],
  safeguards=True,
)
```
Claude samples 5 tagged entries against the original — does the tag
match the sentiment? Fixes any obvious mis-tags, then persists to
`feedback/tagged.md`.

**Token impact:** ~12-18k tokens shifted. Senior reads a fraction to
sanity-check, then runs analytics on the tagged file.

---

## 7. Synthesize across multiple interview transcripts

**Problem:** 5 customer interview transcripts, 2k words each. You want
the cross-cutting pain points — not a per-interview summary, but what
shows up in 3+ interviews.

**You say:**
> "Sidekick synthesize 5 transcript trong `research/interviews/` —
> pain point nào xuất hiện ≥ 3 interview. Format: `pain | #interviews
> mentioned | sample quote`."

**What Claude does:**
```
sidekick_task(
  file_paths=[
    "research/interviews/alice.md",
    "research/interviews/bob.md",
    "research/interviews/chi.md",
    "research/interviews/dung.md",
    "research/interviews/ethan.md",
  ],
  task="Find pain points mentioned in 3 or more of these transcripts. "
       "For each recurring pain: name it (short phrase), count how many "
       "interviews mentioned it, and include one representative quote. "
       "Return a markdown table: | pain | #mentions | quote |. "
       "Drop pains mentioned in only 1-2 transcripts.",
  output_format="markdown",
)
```
Claude spot-checks: does the "#mentions" count match if Claude re-greps
one of the pain phrases? Are the quotes verbatim? Then persists to
`research/pain-synthesis.md` and frames the next step — prioritization
session, OST, or PRD.

**Token impact:** ~25-40k tokens shifted (5 files × 2k words + synthesis
work). Senior uses the synthesis as input for strategy, not as raw data.

---

## 8. Rewrite a spec section for clarity (draft on junior, judgment on senior)

**Problem:** One section of a 40-page spec is confusing to dev team.
You want a v0 rewrite that's clearer, but you don't want to draft it
from scratch yourself.

**You say:**
> "Sidekick rewrite section `## Webhook retry` trong `specs/integration.md`
> cho dễ hiểu hơn — dev complain là không rõ trigger. Giữ đúng nghĩa,
> chỉ rewrite cách trình bày."

**What Claude does:**
```
sidekick_task(
  file_paths=["specs/integration.md"],
  task="Rewrite ONLY the section titled '## Webhook retry' in this spec. "
       "Keep the meaning identical — no new requirements, no removed "
       "behavior. Improve clarity: explicit trigger conditions, retry "
       "schedule as a table, failure modes as a bulleted list. Return "
       "the rewritten section as markdown, same heading level.",
  output_format="markdown",
  safeguards=True,
)
```
Claude compares the rewrite against the original paragraph-by-paragraph
— no requirement drift, no lost edge case. Fixes anything that changed
meaning, then proposes the replacement diff to you before editing the
spec file.

**Token impact:** ~8k tokens shifted. Senior keeps the spec file
itself and the judgment about what "clearer" means; junior handles the
mechanical rewrite attempt.

---

## Anti-patterns — not for sidekick

These look tempting but fail the five principles. Senior handles them
directly:

| What you might try | Why it fails | Senior handles because |
|---|---|---|
| "Decide which PRD version to ship" | Judgment call | Trade-off needs senior reasoning |
| "Debug this failing test" | Multi-step, ambiguous input | Chain of reasoning + tool calls |
| "Rewrite our entire API spec" | Scope too broad | Junior drifts without narrow scope |
| "Reply to the customer email for me" | User acts on it directly without review | Verification bypass risk |

If you really need sidekick for one of these, **re-scope** into a
narrow slice first — e.g., "list the tradeoffs between v3a and v3b for
me to decide" is shiftable; "decide" is not.
