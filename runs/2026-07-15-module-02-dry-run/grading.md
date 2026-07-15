# Module 02 dry run: Prompts and Structured Output That Survive Production

**Date:** 2026-07-15, updated same day after a doubt-driven-development review.
**Purpose:** validate that Module 02's deterministic tier (`scripts/verify_module_02.py`, chaining `verify_module_01.py` per the cumulative-gate convention) actually discriminates a correct attempt from plausible naive ones — built alongside the closed-book checkpoint from the start, per the explicit lesson from Module 01's doubt-driven-development remediation.

## ARB / regression-trigger check (Coachgremlin Workflow step 0)

Checked and **not applicable**: Module 02 only adds new files (`src/extraction.py`'s real body, `tests/test_extraction.py`) to the shared `fixtures/resolve/` project. It does not modify any file Module 01's exercise produces or grades (the learner's own `.claude/` configuration). No ARB trigger fires. Recorded here explicitly because Coachgremlin's own Completion Checklist requires this be *evidenced*, not merely true — a gap Codex's review of this module caught (the reasoning existed but had never been written down).

## 2026-07-15 update: a second doubt-driven-development review, and what it changed

Before this module was treated as done, the same doubt-driven-development process used for Module 01 ran again: a fresh-context Claude subagent, Codex CLI (with live web-search access to Anthropic's current docs), and a Fable-model subagent to critique and replan given both reviews' findings. The dominant finding this time was structural, not a bug: **rubric criteria 3 and 4 graded a prompt/few-shot artifact the exercise's original interface never actually required a learner to produce.** `extract_refund_request`'s `model_client` was fully injected — a learner implementing exactly what was asked would write a validate/retry wrapper with no prompt, no few-shot examples, and no schema-construction logic anywhere in their submission. The "correct" reference implementation itself had none.

Fable's call: change the interface, not the rubric — weakening the criteria would leave a module titled "Prompts and Structured Output" containing no actual prompt engineering, and the stated takeaway (a few-shot/JSON-schema template library) would be structurally unbuildable. Fixed by adding `build_extraction_prompt(message, prior_attempts) -> str` and `FEW_SHOT_EXAMPLES` as required parts of the exercise, with `extract_refund_request` now passing the *constructed prompt* (not the raw message) to `model_client`. This required no changes to any of the original 7 tests (none asserted on the first element of a recorded call), and made criteria 3/4 gradeable against a real artifact.

Other real findings closed in the same pass: the `"other"` category's "requires non-empty detail" rule was asserted as part of the reference implementation but never actually tested; `confidence`'s two-value domain and `refund_amount_cents`'s type were never validated by any test; the exhaustion test's `<= 3` bound let a never-retrying implementation pass; `prior_attempts` entries were never checked for the documented `"response"` key, only `"error"`; a `ModelClient` type alias used PEP 585 subscripting that isn't protected by `from __future__ import annotations` and requires Python 3.9+, undocumented anywhere; a checkpoint answer (Q5) stated `tool_use`+JSON-schema "guarantees" schema compliance more strongly than is precisely true without `strict: true` (a real finding from Codex's live web search, reconciled by keeping the exam guide's own correct-answer ranking but adding the `strict: true` nuance to the explanation); Q11 conflated "same model instance" with "same conversation/context," a real mental-model imprecision; and the README's "valid alternate terminal" language directly contradicted the stop condition two sections later (the no-retry attempt fails the checker, so calling it a valid terminal state was self-contradictory — reworded to "expected intermediate state").

Test suite grew from 7 to 14 tests to close these gaps. Full reconciliation: `docs/decisions.md`'s 2026-07-15 Module 02 doubt-driven-development entries.

## Attempts constructed (final: 4, after the interface change)

1. **`correct-attempt/`** — a real reference implementation, including real prompt construction (`build_extraction_prompt`) and 3 few-shot examples (one deliberately ambiguous: no explicit category word, no dollar amount stated).
2. **`no-retry-attempt/`** — an honest, plausible first instinct: call the model once with a constructed prompt, trust the response, no validation or retry logic at all. Has a working `build_extraction_prompt`/`FEW_SHOT_EXAMPLES` (2 clean examples) — the *only* deliberate flaw is the missing retry/validation logic, keeping this a single-variable attempt.
3. **`fabricates-attempt/`** — real retry/validation logic (now including the "other"-detail, confidence-enum, and type checks added during remediation), but constructs the final result with `raw.get("refund_amount_cents") or 0` instead of `raw.get("refund_amount_cents")` — a real Python footgun that collapses an honest, explicit `None` into a fabricated `0`.
4. **`weak-few-shot-attempt/`** (added during remediation, closing the exact gap the original 3-attempt run had flagged as untested) — identical to `correct-attempt` in every mechanical respect, but `FEW_SHOT_EXAMPLES` has only 2 clean, textbook-clear examples (explicit category cue, explicit dollar amount in both) — no ambiguous case anywhere.

All four ship with a valid Module 01 configuration, so the cumulative gate doesn't block any of them — that's tested separately (see below).

## A real bug found in the dry run's own construction, before any attempt was graded

The first version of `fabricates-attempt` used `raw.get("refund_amount_cents", 0)` (default-on-missing-key) rather than `raw.get("refund_amount_cents") or 0` (collapses-explicit-None). Run against the test suite, it **passed every test** — a false negative in the dry run's own adversarial construction, not the checker: the test always supplies `refund_amount_cents: None` explicitly (realistic — a real `tool_use` response includes all declared fields, nullable ones included), so a bug that only fires on an *absent* key was never exercised. Fixed by rewriting the attempt to use the actual common failure mode. Recorded here rather than silently fixed, matching Module 01's own dry-run discipline: a check that looks like it's testing something and isn't is exactly the failure mode this whole process exists to catch, including when the "check" is a hand-constructed adversarial attempt rather than a script.

## Results (final, 14 tests)

| Attempt | Cumulative gate | Core extraction tests | Retry-prompt-embeds-error | Prompt/few-shot presence tests | Overall |
|---|---|---|---|---|---|
| correct | PASS | PASS | PASS | PASS | **PASS** (14/14) |
| no-retry | PASS | mostly FAIL | FAIL | PASS | **FAIL** (6/14) |
| fabricates | PASS | 1 FAIL (fabrication) | PASS | PASS | **FAIL** (13/14) |
| weak-few-shot | PASS | PASS | PASS | PASS (presence only) | **PASS** (14/14, conceptually weak) |

Cumulative-gate isolation check: running `verify_module_02.py` against `fixtures/resolve/` directly (no `.claude/` configuration present) correctly fails at the cumulative-gate step, before pytest ever runs.

## Finding

The deterministic tier now discriminates correctly across three differently-shaped naive attempts, and — the case that matters most, closing the exact validation gap this dry run's first version left open — the conceptual tier catches a fourth attempt (`weak-few-shot-attempt`) that passes all 14 deterministic tests while failing rubric criterion 3. This is the same pattern Module 01's remediation established: a two-tier gate is only evidenced as necessary once a real attempt is constructed that the deterministic half cannot distinguish from a genuinely good one.

## What this does and doesn't validate

**Validated:** the deterministic tier (14-test suite + cumulative gate) correctly separates a correct implementation from three differently-shaped naive ones, including one that's deterministically perfect but conceptually weak on exactly the criterion the test suite structurally cannot check.

**Not validated:** rubric criterion 4 (the *documented reason* `refund_amount_cents` is nullable) still has no constructed attempt that isolates it — all four attempts either have the reasoning stated (correct-attempt, weak-few-shot-attempt inherit it) or fail earlier for unrelated reasons. A future attempt with a syntactically-nullable field but no stated reason would close this. Also unchanged: no real learner has attempted any of this yet.

## Files

- `correct-attempt/`, `no-retry-attempt/`, `fabricates-attempt/`, `weak-few-shot-attempt/` — the four constructed attempts, full project copies.
- `fixtures/resolve/tests/test_extraction.py` — the provided test suite (14 tests), shipped with the fixture.
- `scripts/verify_module_02.py` — the deterministic checker, chaining `verify_module_01.py` per the cumulative-gate convention.
