# Module 05 dry run: Context and Reliability at Scale

**Date:** 2026-07-16, updated same day after a doubt-driven-development review and a Fable-model critique of the remediation.
**Purpose:** validate that Module 05's deterministic tier (`scripts/verify_module_05.py`, chaining Module 04's checker, which chains Module 03's, Module 02's, Module 01's) discriminates real attempts, and that the rubric's split between deterministic and conceptual criteria is drawn correctly.

## ARB / regression-trigger check (Coachgremlin Workflow step 0)

Checked. Within the shared `fixtures/resolve/` project, Module 05 adds two new files only (`src/context.py`, `tests/test_context.py`) and does not modify anything Module 01-04's exercises produce or grade — no prior shipped stub, tool, or test file was touched. (This module's own new checker, checkpoint, README, and dry-run directory are new additions elsewhere in the repo, not modifications to any shared graded state — the "new files only" claim is scoped to `fixtures/resolve/`, not the whole changeset.) No ARB trigger fires. Confirmed by re-running Modules 01-04's own dry-run attempts unchanged (see Results) — all match their pre-existing expected outcomes exactly.

## Scoping decision: which Domain 5 task statements get a real artifact

Domain 5 (Context Management & Reliability) has 6 task statements: 5.1 (conversation context preservation), 5.2 (escalation/ambiguity resolution), 5.3 (multi-agent error propagation), 5.4 (large-codebase context management — scratchpad files, `/compact`), 5.5 (human review/confidence calibration), 5.6 (provenance/multi-source synthesis).

`resolve` has no subagents yet (Module 04's coordinator is single-agent; multi-agent decomposition is explicitly deferred to Domain 1's own remaining task statements, tested only in Module 04's checkpoint) and isn't a "large codebase" scenario in the sense Task Statement 5.4 means. Following the same division-of-labor convention every prior module has used: **5.1, 5.2, 5.5, and 5.6 get a real `resolve`-specific artifact in the hands-on tier; 5.3 and 5.4 have no natural artifact yet and are tested only in the closed-book checkpoint.**

The artifact: `fixtures/resolve/src/context.py`'s `CaseFacts`/`update_case_facts` (persistent, sourced case facts extracted from tool results, with explicit conflict annotation rather than silent overwrite — 5.1, 5.6) and `should_escalate` (an escalation decision keyed to structured signals only — unresolved conflicts, a real error-count threshold, proximity to `max_iterations` — never a model-reported confidence score, which the function's own signature has no room for — 5.2, 5.5).

**A relationship to Module 04 that needed stating explicitly, not left implicit:** Module 04's `SessionState.verified_customer_id` is last-verified-wins by design (a session enforces one active verified customer for authorization purposes). This module's `CaseFacts.conflicts` does the opposite for a different reason — it's a reliability/audit concern, not a real-time authorization one, so silently keeping only the newest value would hide a real signal. Both are correct for what each is for; `context.py`'s own docstring says so directly, since a learner who's just internalized Module 04's "overwrite is correct" lesson could reasonably import that assumption into this module's differently-scoped problem.

## Attempts constructed (initial pass, before doubt-driven-development)

1. **`correct-attempt/`** — real `update_case_facts` (extracts facts from tool results, not tool args; increments `error_count` on failure only; records conflicts as `(field, old, new)` tuples without discarding either side) and `should_escalate` (checks conflicts, then error threshold, then iteration proximity, in that order, each with a distinct reason string).
2. **`silent-overwrite-attempt/`** — `update_case_facts` overwrites a changed fact without ever appending to `conflicts` — the disagreement itself vanishes.
3. **`request-trusting-attempt/`** — originally: for `process_refund` specifically, records the *requested* `amount_cents` from `tool_args` instead of the backend's actual `refunded_cents` from `tool_result`. Extended after doubt-driven-development (see below) to also misread `lookup_order`'s `order_id` the same way, once the review found the original attempt didn't represent the full scope of the flaw the contract actually warns against.
4. **`confidence-proxy-attempt/`** — `should_escalate` uses iteration count alone as a stand-in signal for "the session is struggling," ignoring `case_facts.conflicts` and `case_facts.error_count` entirely — the same unreliable-proxy anti-pattern Task Statement 5.5 names, just applied to an internal signal instead of the model's own self-reported confidence.
5. **`thin-docstring-attempt/`** — behaviorally identical to `correct-attempt/`, but every docstring stripped to one line, with no documented reasoning for why this module's conflict-preserving design is correct where Module 04's overwrite-on-verify is *also* correct — constructed proactively, before any external review, continuing the discipline Module 04 established.

Initial results (20 tests): correct PASS (20/20), silent-overwrite FAIL (17/20), request-trusting FAIL (19/20), confidence-proxy FAIL (16/20), thin-docstring PASS (20/20, conceptually weak). All matched expectations for their intended, narrower flaws — but see below for what this suite missed.

## 2026-07-16 update: a doubt-driven-development review, and what it changed

Before this module was treated as done, the same process used for Modules 01-04 ran: a fresh-context Claude subagent (adversarial review, ARTIFACT+CONTRACT only), then Codex CLI (with its own constructed counter-implementations run live against the real files, not just reasoned about). Both found the same dominant class of issue, and Codex deepened it substantially.

**The dominant issue: the test suite tested `customer_id` far more rigorously than `order_id` or `refund_amount_cents` — the same field, not the same rigor, across three structurally-identical mappings.** `test_update_case_facts_reads_the_actual_result_not_the_requested_args` (the request-vs-result test) existed only for `process_refund`'s `refunded_cents`; `lookup_order`'s `order_id` had no analogous test, and since `tool_args["order_id"]` and `tool_result["order_id"]` share a key name, a counter-implementation reading `order_id` from the request instead of the result passed all 20 original tests. The conflict-preservation test (`(field_name, old_fact, new_fact)`, both sides sourced) existed in full only for `customer_id`; a counter-implementation recording `('order_id', None, None)` — a hollow, unsourced conflict entry — also passed all 20. `refund_amount_cents` had no conflict test at all: two successful `process_refund` results with different `refunded_cents` values could be silently overwritten with zero test noticing. Both reviewers constructed and ran these exact counter-implementations against the real checker to confirm the gap, not just identify it by inspection.

**Fixed:** added the missing symmetric tests for `order_id` and `refund_amount_cents` — a request-vs-result test for `lookup_order`, conflict-preservation and no-conflict-on-repeat tests for `order_id`, and a conflict test for `refund_amount_cents`. `request-trusting-attempt` was extended to also misread `lookup_order`'s `order_id` from the request (previously it only demonstrated the flaw for `process_refund`), so the dry run's own flaw matrix actually represents the contract's full scope. Test suite grew from 20 to 28.

**Two further structural findings, both confirmed by constructing and running the actual counter-implementation:**
- **Shallow-copy mutation hole.** The non-mutation test only checked scalar-field reassignment (`original.customer_id is None`); an implementation using `dataclasses.replace(case_facts)` (a shallow copy sharing the *same* `conflicts` list object) passed all 20 original tests while still corrupting the caller's original the moment a later conflict was appended. Fixed: added `test_update_case_facts_conflicts_list_is_independent_of_the_original`, verified against a live shallow-copy counter-implementation (fails, as intended, on the new test specifically). Also added a companion test that a failed call neither discards existing facts nor mutates the original object — verified against a live counter-implementation that mutates `case_facts.error_count` in place on the error path.
- **`should_escalate`'s "no confidence parameter" guarantee was asserted in prose, never checked.** An implementation adding an unused `confidence: float = None` parameter passed all 20 original tests. Fixed: added `test_should_escalate_signature_has_no_confidence_or_extra_parameters`, using `inspect.signature` to check the function's actual parameter list — verified against a live counter-implementation with the added parameter (fails, as intended).

**Two smaller findings, also fixed:**
- `CaseFacts.issue_summary` was a dead field — no `FACT_SOURCES` mapping, no test, no docstring explanation, and (Codex's deepening) a structural risk: an implementation could turn it into an undetected fourth `should_escalate` trigger with nothing to catch it. Removed entirely from `CaseFacts` in the shipped stub, the reference implementation, and all five dry-run attempts, rather than kept and merely documented — an unused field with no exercise purpose doesn't earn its place by being explained instead of deleted. Also closed the adjacent gap Codex found in the same area: `should_escalate`'s iteration-proximity check had no test at the exact boundary (`max_iterations - 1` vs. `- 2`), only "near" (9 of 10) and "well before" (2 of 10) — an off-by-one implementation (`- 2` instead of `- 1`) passed all 20 original tests; added `test_should_escalate_iteration_boundary_is_exact`, verified against a live off-by-one counter-implementation.
- Checkpoint Q12's answer key overclaimed that `source_tool` alone can distinguish two independent calls to the *same* tool from a single re-report — `CaseFact` records no call ID or timestamp, only which tool produced a value, so it structurally cannot make that distinction. Rewritten so the overclaim is a wrong answer, and the question stem now states directly what `CaseFact` does and doesn't store.

Also fixed for precision, not correctness: the ARB-check's original "two new files only" phrasing could be misread as "the whole changeset touches two files" (it doesn't — the checker, checkpoint, README, and dry-run directory are all new too); reworded to scope the claim explicitly to `fixtures/resolve/`.

Full reconciliation: `docs/decisions.md`'s 2026-07-16 Module 05 doubt-driven-development entries.

## 2026-07-16 update: a Fable-model critique of the remediation, and what it changed

Per standing practice, a Fable-model subagent then critiqued the *remediation itself* — reading the actual current files rather than trusting a summary — asking specifically whether the "symmetric coverage" fix above was actually complete. It found the fix was honestly executed but still incomplete against its own dominant finding: the new tests for `order_id`/`refund_amount_cents` covered the specific counter-implementations the first review happened to construct, not the full guarantee-by-field matrix those two fields needed to match `customer_id`'s existing rigor. Four gaps, each confirmed by constructing and running a new live counter-implementation:

- **Hollow conflict entries were still possible for `order_id` and `refund_amount_cents` specifically.** The new conflict-preservation tests for those two fields asserted `old_fact.value`/`new_fact.value` but never `source_tool` — despite "sourced" being the entire point. A counter-implementation storing `CaseFact(value, source_tool=None)` in conflict tuples for those two fields (while keeping `customer_id`'s handling fully correct) passed all 28 tests. Fixed: added `source_tool` assertions to both tests.
- **The error path could still leak a fact via the exact key-collision the success-path fix had just closed.** No test exercised a *failed* `lookup_order` call with real `tool_args` carrying an `order_id` key; a counter-implementation that extracted `order_id` from `tool_args` specifically on the error path (never touching the success path at all) passed all 28 tests. Fixed: added `test_update_case_facts_error_does_not_extract_a_fact_from_the_request_args`, verified against a live counter-implementation that does exactly this.
- **Most-recent-wins was untested for `refund_amount_cents` conflicts.** The customer_id and order_id conflict tests both assert the field's *current* value reflects the newer result; the refund conflict test asserted only the conflict tuple, never `facts.refund_amount_cents.value` itself. A counter-implementation that recorded the conflict correctly but kept the *old* refund amount as current passed all 28 tests. Fixed: added the current-value assertion to the existing test.
- **No-conflict-on-repeat was untested for `refund_amount_cents`.** `customer_id` and `order_id` both had a test confirming an identical re-report isn't a conflict; `refund_amount_cents` had none — and given `should_escalate`'s conflicts-first precedence, a spurious refund conflict would wrongly escalate a perfectly fine session. A counter-implementation forgetting the equality check for that one field passed all 28 tests. Fixed: added `test_update_case_facts_no_conflict_when_second_refund_result_matches_first`.

All four fixes verified against live counter-implementations constructed specifically to defeat them (not the same ones used to justify the fix) — each fails exactly its own new test and passes everything else. Test suite grew from 28 to 30. Full record: `docs/decisions.md`'s 2026-07-16 Fable-critique entries.

## Attempts (final)

1. **`correct-attempt/`** — request-vs-result discipline and conflict preservation now verified symmetric across all three mapped fields; independent `conflicts` list on every return; `should_escalate` with exactly three parameters and an exact iteration boundary.
2. **`silent-overwrite-attempt/`** — never records a conflict for any field.
3. **`request-trusting-attempt/`** — misreads both `lookup_order`'s `order_id` and `process_refund`'s `refunded_cents` from the request instead of the result.
4. **`confidence-proxy-attempt/`** — ignores `case_facts` entirely in `should_escalate`, using iteration count alone.
5. **`thin-docstring-attempt/`** — behaviorally identical to `correct-attempt/`, all reasoning stripped from docstrings.

## Results (final, 30 tests)

| Attempt | Cumulative gate (01+02+03+04) | Fact-extraction tests | Conflict tests | Escalation tests | Overall |
|---|---|---|---|---|---|
| correct | PASS | PASS | PASS | PASS | **PASS** (30/30) |
| silent-overwrite | PASS | PASS | 6 FAIL | PASS | **FAIL** (24/30) |
| request-trusting | PASS | 2 FAIL | 2 FAIL | PASS | **FAIL** (26/30) |
| confidence-proxy | PASS | PASS | PASS | 4 FAIL | **FAIL** (26/30) |
| thin-docstring | PASS | PASS | PASS | PASS | **PASS** (30/30, conceptually weak) |

Eight additional ad hoc constructions across both review rounds (not permanent attempt directories, matching the empirical-verification discipline Module 04 established for its own `backend`-omission check): a shallow-copy non-mutation counter-implementation, a `confidence`-parameter counter-implementation, an iteration-boundary off-by-one counter-implementation, an error-path in-place-mutation counter-implementation (all four from the Claude+Codex round), plus a hollow-conflict-entry counter-implementation, an error-path args-extraction counter-implementation, a keep-old-value-on-refund-conflict counter-implementation, and a spurious-refund-conflict counter-implementation (all four from the Fable-critique round). All eight fail exactly the test built to catch them and pass everything else, confirmed by live execution against the real checker, not by inspection.

Cumulative-gate isolation, re-confirmed: running `verify_module_05.py` against `fixtures/resolve/` directly (no Module 01-04 work) fails at the cumulative-gate step before `test_context.py` even collects.

Regression check: Modules 01-04's own dry-run attempts (4 + 4 + 3 + 5 = 16 attempts total) re-run unchanged against their respective checkers after every Module 05 code/doc edit in this remediation — all outcomes match their pre-existing expected results exactly.

## Finding

The proactively-constructed `thin-docstring-attempt` closed the conceptual-tier gap this arc had needed an external review to find in earlier modules — a real, evidenced improvement in this pipeline's own discipline, carried forward from Module 04. But it didn't catch the deeper issue this round: the test suite's *own* internal asymmetry (rigorous for one field, thin for two structurally identical others) survived both the initial dry run's attempt construction *and* would have survived shipping without doubt-driven-development, because the flawed attempts constructed by hand happened to probe the same field the suite already tested well. This is the same lesson Module 04's own review taught, generalized: constructing adversarial attempts against your own mental model of the failure modes has a blind spot exactly where that mental model does — and in this case, the blind spot was in the *test suite's* coverage shape, not just in any one implementation's behavior.

More strikingly, the pattern repeated one level deeper: the Claude+Codex round's own "symmetric coverage" fix was itself asymmetric in a subtler way — it added *a* test per field, not the *same rigor* per field, so the fix for `order_id`/`refund_amount_cents` still lacked the source-attribution, error-path, and repeat-value checks `customer_id` already had. Only a critique of the remediation itself (reading the actual diffs, not the description of what was fixed) caught this. Three stages, three different blind spots closed: a dry run catches behavior against the author's own mental model; doubt-driven-development catches behavior against a fresh reviewer's mental model; a critique of the remediation catches whether the *fix* actually matches its own stated scope. None of the three would have caught what the other two did.

## What this does and doesn't validate

**Validated:** the deterministic tier discriminates all constructed behavioral flaws correctly, now with symmetric rigor across all three mapped fields; the cumulative gate chains through all four prior modules; adding two new files (within `fixtures/resolve/`) causes zero regression in any prior module's own dry-run attempts (empirically re-confirmed at every step of this remediation, not assumed); rubric criterion 2's necessity is directly evidenced by `thin-docstring-attempt`; the non-mutation, signature, and iteration-boundary guarantees are now enforced by tests verified against live counter-implementations, not merely asserted in docstrings.

**Not validated:** no real learner attempt exists yet, same open gap as every prior module.

## Files

- `correct-attempt/`, `silent-overwrite-attempt/`, `request-trusting-attempt/`, `confidence-proxy-attempt/`, `thin-docstring-attempt/` — the five constructed attempts, full project copies (seeded from Module 04's own `correct-attempt/`, which already has working `src/agent.py`, `src/tools/*.py`, `src/backend.py`, `src/extraction.py`).
- `fixtures/resolve/tests/test_context.py` — the provided test suite (30 tests), shipped with the fixture.
- `scripts/verify_module_05.py` — the deterministic checker, chaining `verify_module_04.py` (which chains `verify_module_03.py`, `verify_module_02.py`, `verify_module_01.py`).
