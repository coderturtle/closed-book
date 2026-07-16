# Module 06 dry run: Foundations Capstone

**Date:** 2026-07-16, updated same day after a doubt-driven-development review and a Fable-model critique of the remediation.
**Purpose:** validate that Module 06's deterministic tier (`scripts/verify_module_06.py`, chaining Module 05's checker, which chains Module 04's, Module 03's, Module 02's, Module 01's) discriminates real diagnose-and-fix attempts, and that the two seeded defects are each independently catchable and independently fixable.

## ARB / regression-trigger check (Coachgremlin Workflow step 0)

Checked. Module 06 adds two new files only (`fixtures/resolve/src/session.py`, `fixtures/resolve/tests/test_session.py`) and does not modify anything Module 01-05's exercises produce or grade — no prior shipped stub, tool, or test file was touched. Confirmed by re-running Modules 01-05's own dry-run attempts unchanged (see Results) — all match their pre-existing expected outcomes exactly.

## A structural difference from every prior module, stated explicitly

Modules 01-05 each shipped `raise NotImplementedError` stubs; a fresh learner's starting point always failed the deterministic gate trivially (nothing implemented yet). Module 06 is a genuine capstone: `src/session.py` ships **fully written and running**, integrating Module 02's `extract_refund_request`, Module 04's `verify_before_refund_hook`/agentic-loop pattern, and Module 05's `update_case_facts`/`should_escalate` into one `run_full_support_session` function — with two real, seeded defects already in place. A fresh learner's starting point (`unfixed-attempt` below) fails 2 of the final 6 tests, not all of them, and not zero — this is deliberate: the exercise is diagnosis and repair of a mostly-working system, not construction from nothing, matching CCA-F's own scenario-based exam format testing whether a candidate can locate a defect in an unfamiliar, largely-correct codebase. (The suite was 5 tests at initial authoring, before doubt-driven-development added a 6th — see below.)

## The two seeded defects

1. **Extraction-confidence escalation bypass (spans Modules 02 & 05, Domains 4 & 5).** `extract_refund_request`'s `ExtractionResult.confidence` field describes how confident the *extraction step itself* was in parsing the customer's message — a legitimate Module 02 concept, describing extraction quality. The shipped `session.py` fed this field into a parallel, ad hoc escalation check (`if extraction.confidence == "low": return {"escalated": True, ...}`) that runs *before* the agentic loop even starts — reintroducing, via a side door, exactly the "unreliable self-reported signal as an escalation trigger" anti-pattern Module 05's `should_escalate` was built specifically to keep out, by giving that function's own signature no confidence parameter at all. The bug isn't that `should_escalate` was weakened; it's that a second, unofficial escalation path was added that bypasses it entirely.
2. **Escalation-timing gap (spans Modules 04 & 05, Domains 1 & 5).** The shipped loop called `should_escalate(facts, ...)` *before* folding the current turn's tool result into `facts` via `update_case_facts`. This means a conflict or the 3rd-error threshold introduced by the *current* tool call isn't visible to the escalation check until the *next* iteration at the earliest — a one-turn-stale escalation decision, structurally identical in shape to the request-vs-result and staleness bugs Modules 04 and 05's own doubt-driven-development reviews each had to find and fix in their own code.

## Attempts constructed

1. **`correct-attempt/`** — both defects fixed at their root cause: the ad hoc confidence-based escalation branch removed entirely (extraction's result still runs and is surfaced in the return value for audit purposes, just never drives escalation control flow), and `update_case_facts` moved before `should_escalate` in the loop body.
2. **`unfixed-attempt/`** — exactly the shipped file, both defects present. Validates the gate isn't trivially green and isn't trivially all-red either.
3. **`fix-bug1-only-attempt/`** — removes the confidence-escalation bypass, leaves the escalation-timing gap in place.
4. **`fix-bug2-only-attempt/`** — reorders `update_case_facts`/`should_escalate` correctly, leaves the confidence-escalation bypass in place.
5. **`over-correction-attempt/`** — "fixes" defect 1 by deleting the extraction step entirely (`extract_refund_request` is never called) rather than removing only its misuse as an escalation signal; defect 2 is fixed correctly. Represents a realistic overreaction: recognizing something is wrong with how extraction is used and removing the whole feature instead of the specific defect.

## Results (initial pass, 5 tests)

| Attempt | Cumulative gate (01+02+03+04+05) | Baseline sanity tests (3) | Defect 1 test | Defect 2 test | Overall |
|---|---|---|---|---|---|
| correct | PASS | PASS | PASS | PASS | **PASS** (5/5) |
| unfixed | PASS | PASS | FAIL | FAIL | **FAIL** (3/5) |
| fix-bug1-only | PASS | PASS | PASS | FAIL | **FAIL** (4/5) |
| fix-bug2-only | PASS | PASS | FAIL | PASS | **FAIL** (4/5) |
| over-correction | PASS | 1 FAIL (`test_extraction_actually_runs_before_the_loop`) | PASS (vacuously — extraction never runs, so nothing can misuse its confidence) | PASS | **FAIL** (4/5) |

Cumulative-gate isolation, re-confirmed: running `verify_module_06.py` against `fixtures/resolve/` directly (no Module 01-05 work) fails at the cumulative-gate step before `test_session.py` even collects.

Regression check: Modules 01-05's own dry-run attempts (4 + 4 + 3 + 5 + 5 = 21 attempts total) re-run unchanged against their respective checkers after this module's two new files were added — all outcomes match their pre-existing expected results exactly.

Each of the four flawed attempts fails exactly the test(s) that exist to catch its specific gap, with no cross-contamination: `fix-bug1-only-attempt` and `fix-bug2-only-attempt` each pass the test for the defect they actually fixed and fail only the test for the one they didn't touch — direct evidence the two seeded defects are genuinely independent, not two symptoms of one root cause. `over-correction-attempt` is the most pedagogically important case: it "resolves" defect 1's symptom (the session no longer escalates on low confidence, trivially, since extraction never runs at all) while failing a *different* test that specifically checks the extraction step still executes — proof that a fix must be checked against the full contract, not just against the symptom that first drew attention.

## 2026-07-16 update: a doubt-driven-development review, and what it changed

Before this module was treated as done, the same process used for Modules 01-05 ran: a fresh-context Claude subagent (adversarial review, ARTIFACT+CONTRACT only, actually executing the checker against every attempt directory rather than reasoning from code alone), then Codex CLI (with its own execution and its own hand-recount of the checkpoint's domain tally). Both confirmed everything above held up under real execution. Then each found real, distinct issues beyond it.

**Claude subagent's dominant finding, on the checkpoint, not the code: every one of the 42 answer-key entries named option A as correct — no exceptions.** A test-taker could score 1000/1000 by circling "A" 28 times without reading a single stem, completely defeating the closed-book design. Fixed: every question's 4 options were mechanically rotated (a fixed per-question rotation `k ∈ {0,1,2,3}`, assigned via a seeded shuffle targeting an even ~10-11-per-letter distribution) so the correct answer's position and the answer key's own letter references were both relabeled consistently. The fix was verified two ways: (1) a script re-parsed the transformed file and confirmed, for all 42 questions, that the option text *originally* at "A" now sits at exactly the letter the answer key claims; (2) a second script confirmed every answer-key line's 3 mentioned distractor letters are exactly the 3 non-correct letters, no duplicates or omissions. Final distribution: A:10, B:11, C:11, D:10.

**Claude subagent's second finding: 3 of the 5 "original" scenarios (C, D, F) were too structurally similar to 3 of the real exam's own published scenarios** (a code-review-in-CI bot ~ "Claude Code for CI"; a research aggregator querying parallel subagents ~ "Multi-Agent Research System"; an onboarding assistant for new engineers on an unfamiliar codebase ~ "Developer Productivity with Claude"). Renamed: Scenario C is now a release-notes drafting agent in a deploy pipeline; Scenario D is a multi-channel customer feedback synthesizer; Scenario F is a legacy-codebase documentation generator. Every scenario-specific noun reference throughout each scenario's 7 questions was updated to match, not just the section header.

**Claude subagent's third and fourth findings, disclosed rather than silently fixed:** Task Statement 5.4 (large-codebase context management) has zero questions anywhere in this 42-question pool — the only one of CCA-F's 30 task statements with zero coverage here (it *is* covered in Module 05's own checkpoint, so not an uncovered gap in the workshop overall). Domain 3 (10 questions) and Domain 4 (7 questions) have equal real blueprint weight (20% each) but unequal representation, an artifact of each scenario being fixed at 7 questions rather than a deliberate weighting choice. Both now stated explicitly in the checkpoint's own intro rather than left implicit.

**Codex's finding, more severe than any of the above: the "correct" reference implementation itself never escalates when the hook repeatedly rejects a call.** `verify_before_refund_hook` rejections hit a bare `continue`, before `update_case_facts`/`should_escalate` ran — meaning a model stuck repeatedly attempting a blocked `process_refund` made no real progress, yet the session just ran silently to `max_iterations` rather than escalating. Codex reproduced this live against `correct-attempt` itself (3 repeated blocked refunds → `max_iterations`, `error_count=0`, no escalation) and pointed out this contradicts this project's own stated fail-closed design principle (a blocked/ambiguous action should escalate, not run out the clock in silence — see the Review Panel's own safe-design-default finding in `docs/workshop-design.md`). This is **not** one of the two seeded pedagogical defects — it was a genuine gap in the *base design* shared identically by all six copies of `session.py` (shipped stub and all five dry-run attempts), since none of the two defects' fixes touch the rejection path at all. Fixed uniformly across all six files: a rejection now also calls `should_escalate` before continuing, escalating once the iteration-proximity signal (or any other structured signal already present) fires. A 6th test, `test_repeated_hook_rejections_eventually_escalate`, checks this directly — 2 identical scripted "always blocked `process_refund`" responses with `max_iterations=2`, asserting escalation on the 2nd. Verified against the actual fixed code (passes) and reasoned through against the pre-fix structure (would have failed, matching Codex's own live repro).

**One wording issue, also fixed:** the checkpoint's original "none of these 6 scenarios are the real CCA-F exam's own published scenarios" claim was in tension with Scenario A being `resolve` itself, which — as `fixtures/resolve/SPEC.md` already states elsewhere — was deliberately modeled on the real exam's own "Customer Support Resolution Agent" scenario from the start of this workshop. Reworded so the note states this parallel explicitly as a disclosed exception, rather than an unqualified "none," which Codex correctly flagged as an internal contradiction.

Full reconciliation: `docs/decisions.md`'s 2026-07-16 Module 06 doubt-driven-development entries.

## 2026-07-16 update: a Fable-model critique of the remediation, and what it changed

Per standing practice, a Fable-model subagent then critiqued the remediation itself — reading the actual current files, building and running its own mutants, not trusting the write-up above. Verdict: substantively sound (the rejection-path fix is correct and uniform across all six `session.py` files, the answer-key shuffle is genuinely verified, no scope creep) but the new 6th test had a real precision gap, plus two scenario-renaming sweeps were incomplete.

- **The 6th test didn't distinguish the intended fix from an over-eager one.** A constructed mutant that escalates unconditionally on the *first* rejection (never actually calling `should_escalate`, ignoring iteration budget entirely) passed all 6 tests — the test only checked that escalation eventually happens, never that it *doesn't* happen prematurely. Fixed: `test_repeated_hook_rejections_eventually_escalate` now also asserts the model was consulted twice (`len(agent_client.calls) == 2`) before escalating, and `test_hook_still_blocks_unverified_refund_through_the_full_integration` now asserts the session reaches a normal `end_turn` (not an escalation) when a single rejection occurs with plenty of iteration budget left. Verified against Fable's own constructed mutant: now fails exactly the two tightened tests.
- **Scenario renaming left stale vocabulary from the old framing in distractor options** (not the correct answers, so no answer-key damage, but undercutting the rename's own point): Scenario C's C3/C4 still said "reviewed"/"review" in three distractors (the release-notes agent drafts, it doesn't review); Scenario F's F1 still had a "new engineers... first week" distractor (residue of the old onboarding-assistant framing). Fixed: reworded to "drafted"/"draft"/"summarized" for C, and to the documentation-generator's own framing for F. Also fixed in the same pass: B7's stem described a generic "PR review comment" scenario disjoint from Scenario B's actual premise (a documentation search assistant) — reworded to be about the assistant's own citation-extraction code being checked in CI, matching its scenario.
- Independently re-verified by Fable, not just by the original scripts: read all 42 questions directly, manually cross-checked ~15 across all six scenarios for answer-key/option consistency, and independently recounted the domain tally from each question's task-statement tag — all matched exactly what was claimed.

All fixes re-verified: full 6-test suite still passes 6/6 against `correct-attempt`; all four flawed attempts still fail exactly their intended tests; Fable's own escalate-immediately mutant now fails the tightened tests as intended; full regression across Modules 01-05's 21 attempts unchanged.

## Results (final, 6 tests)

| Attempt | Cumulative gate (01+02+03+04+05) | Baseline sanity tests (3) | Defect 1 test | Defect 2 test | Rejection-escalation test | Overall |
|---|---|---|---|---|---|---|
| correct | PASS | PASS | PASS | PASS | PASS | **PASS** (6/6) |
| unfixed | PASS | PASS | FAIL | FAIL | PASS | **FAIL** (4/6) |
| fix-bug1-only | PASS | PASS | PASS | FAIL | PASS | **FAIL** (5/6) |
| fix-bug2-only | PASS | PASS | FAIL | PASS | PASS | **FAIL** (5/6) |
| over-correction | PASS | 1 FAIL | PASS (vacuously) | PASS | PASS | **FAIL** (5/6) |

The new rejection-escalation test passes uniformly across all five attempts — expected, since that fix was applied identically everywhere as a base-design correction, not gated behind either of the two seeded defects.

Regression re-confirmed after this remediation: Modules 01-05's own dry-run attempts (21 attempts total) re-run unchanged — all outcomes match their pre-existing expected results exactly.

## What this does and doesn't validate

**Validated:** the deterministic tier discriminates the unfixed baseline, both single-defect partial fixes, and the over-correction case, all correctly and with clean isolation; the cumulative gate chains through all five prior modules; adding two new files causes zero regression in any prior module's own dry-run attempts (empirically re-confirmed, not assumed); the two seeded defects are independently diagnosable and independently fixable; the checkpoint's answer-key shuffle is mechanically verified consistent for all 42 questions; the rejection-path escalation gap Codex found is real, reproduced live, and now fixed and tested uniformly.

**Not validated:** no real learner attempt exists yet, same open gap as every prior module. Rubric criterion 3 (a learner's own written root-cause explanation) has no mechanical check and can't have one by its own nature — this dry run validates only that the code-level defects are real and independently catchable, not that a diagnosis-in-writing rubric is gradable at scale.

## Files

- `correct-attempt/`, `unfixed-attempt/`, `fix-bug1-only-attempt/`, `fix-bug2-only-attempt/`, `over-correction-attempt/` — the five constructed attempts, full project copies (seeded from Module 05's own `correct-attempt/`, which already has working `src/agent.py`, `src/context.py`, `src/tools/*.py`, `src/backend.py`, `src/extraction.py`).
- `fixtures/resolve/tests/test_session.py` — the provided test suite (6 tests), shipped with the fixture, written to fail 2/6 against `src/session.py` exactly as shipped.
- `scripts/verify_module_06.py` — the deterministic checker, chaining `verify_module_05.py` (which chains `verify_module_04.py`, `verify_module_03.py`, `verify_module_02.py`, `verify_module_01.py`).
