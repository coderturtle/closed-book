# Module 04 dry run: Agentic Loops and Multi-Agent Orchestration

**Date:** 2026-07-15, updated same day after a doubt-driven-development review.
**Purpose:** validate that Module 04's deterministic tier (`scripts/verify_module_04.py`, chaining Module 03's checker, which chains Module 02's, which chains Module 01's) discriminates real attempts, and that the rubric's split between deterministic and conceptual criteria is drawn correctly.

## ARB / regression-trigger check (Coachgremlin Workflow step 0)

Checked. Module 04 adds `src/agent.py`'s real body (previously `raise NotImplementedError`) and `tests/test_agent.py` (previously a stub). It also edits `src/backend.py`'s module docstring — not its `Backend` Protocol itself (no method added, removed, or retyped) — to resolve the deferred stateful-backend question flagged in Module 03's own dry run (see Decision, below). Because the Protocol's shape is unchanged, no prior module's checker or shipped test file is affected. Confirmed by re-running Modules 01-03's own dry-run attempts unchanged (see Results) — all match their pre-existing expected outcomes.

## Decision made before writing the exercise: the deferred stateful-backend question

`backend.py`'s docstring, written during Module 03, stated that refund *execution* (persistence, decrementing `refundable_cents`, idempotency) was "explicitly Module 04's exercise." Building Module 04's actual hands-on artifact required resolving this for real, not carrying the deferral forward again.

**Decision: Module 04 does not extend `Backend` into a stateful, mutating protocol.** Its exercise is orchestration — the agentic loop (`run_support_session`) and the session-level hook (`verify_before_refund_hook`) that decides *whether* `process_refund` may be called at all, not refund persistence or idempotency. Those are real production concerns, but they map to Domain 2 (tool design) territory this project already resolved in Module 03, not to Domain 1 (agentic orchestration), which is what Module 04's own CCA-F blueprint section teaches. `backend.py`'s docstring was rewritten to state this directly rather than continue pointing at a module that was never going to pick it up. Module 03's own README carried a stale forward-promise contradicting this and was fixed in the same pass (see the doubt-driven-development section, below). See `docs/decisions.md`.

This also settled `test_agent.py`'s design: it uses spy tool functions (recording calls, returning canned results), not Module 03's real tool implementations — Module 04's own tests exercise the loop and the hook in isolation, not re-proving Module 03's already-tested tool behavior.

## Attempts constructed (initial pass, before doubt-driven-development)

1. **`correct-attempt/`** — a real `run_support_session` (loop keyed strictly on `stop_reason`, never on response text) and `verify_before_refund_hook` (blocks `process_refund` unless `get_customer` had already succeeded in the same session; never blocks `escalate_to_human`).
2. **`no-hook-attempt/`** — the loop never calls `verify_before_refund_hook` at all before dispatching a tool.
3. **`text-parsing-attempt/`** — the loop terminates early if the model's `text` field contains words like "done"/"finished", even when `stop_reason` is `"tool_use"`.
4. **`trusts-attempted-call-attempt/`** (later renamed `trusts-identifier-attempt/`, see below) — originally: the loop records a tool call into `session.tool_calls_made` whenever the tool was *called*, regardless of whether it *succeeded*.
5. **`thin-docstring-attempt/`** — behaviorally identical to `correct-attempt/`, but every docstring stripped to one line, no documented reasoning for the two-layer defense-in-depth architecture.

Initial results (12 tests): correct PASS (12/12), no-hook FAIL (10/12), text-parsing FAIL (11/12), trusts-attempted-call FAIL (11/12), thin-docstring PASS (12/12, conceptually weak). All matched expectations for their intended, narrower flaws — but see below for what this pass missed.

## 2026-07-15 update: a doubt-driven-development review, and what it changed

Before this module was treated as done, the same process used for Modules 01-03 ran: a fresh-context Claude subagent (adversarial review, ARTIFACT+CONTRACT only), then Codex CLI (with live repository exploration and its own constructed attacks), then reconciliation. Both independently found — and Codex confirmed, deepened, and extended — one dominant structural issue plus several smaller real ones.

**The dominant issue: the hook's original design didn't bind to *which* customer was verified.** `verify_before_refund_hook` blocked `process_refund` based on "has `get_customer` succeeded at all in this session" — never checking that the `customer_id` being refunded was the *same* customer `get_customer` actually verified. A session that verified customer A via `get_customer`, then called `process_refund` for a completely unrelated customer B, passed every one of the original 12 tests. Both reviewers reproduced this live against the actual checker (not just by inspection). Codex additionally confirmed that a hook blocking on "*any* tool succeeded" (not `get_customer` specifically) also passed all 12 tests, since no test put a different successful tool call before `process_refund` in a session that should still be blocked.

**Fixed:** `SessionState` gained `verified_customer_id: Optional[str]`, set only when `get_customer` succeeds, to the `customer_id` its *result* actually returned (not the raw identifier the caller asked to look up — see the `trusts-identifier-attempt` rename below, which is exactly this distinction). `verify_before_refund_hook` now checks `tool_args["customer_id"] == session.verified_customer_id`, not membership in a bare list of tool names. Four new tests close the gap: a hook-unit-level customer-mismatch test, an integration-level customer-mismatch test (verify A, attempt to refund B), a test that a different tool succeeding (`lookup_order`) does not substitute for `get_customer`, and an `escalate_to_human` loop-level integration test (previously only tested at the hook-unit level, a smaller gap the same reviews flagged). Test suite grew from 12 to 16 tests.

**Other real findings closed in the same pass:**
- **Test-double loophole:** the spy tool functions accepted `backend` via `**kwargs` and silently discarded it if absent, so an implementation that forgot `tools[tool_name](**tool_args, backend=backend)` (omitting `backend=backend`) could still pass — even though the real Module 03 tools require `backend` in their own signatures. Fixed by making the spy tools' `backend` parameter keyword-only and required (`def tool(*, backend, **kwargs)`), so a missing `backend=backend` now fails loudly with `TypeError`, verified against a constructed submission that omits it (see Results).
- **Checkpoint overclaim:** Q14's answer key claimed session forking isolates a branch's *tool-call side effects*, not just its conversation state — factually wrong for the real Claude Agent SDK/Claude Code model (forking branches conversation state; it does not undo or sandbox a tool call's real-world effects already executed). Rewritten so the misconception is a wrong answer instead of the correct one — a real correction, not a caveat.
- **Cross-module contradiction:** Module 03's own README still promised "persistence, decrementing `refundable_cents`, and idempotency... are explicitly Module 04's exercise" — directly contradicting the scope decision this module actually made. Fixed in Module 03's README (a live, current-state document, unlike this module's own frozen dry-run history, which is left as a point-in-time record per this project's append-only-ADR discipline).
- **Checkpoint/README pass-threshold mismatch:** `checkpoint.md` correctly stated 80% as `12/14`; the README stated `11/14` — a real arithmetic error (11.2 rounds up to 12, not 11). Fixed to match.
- **`max_iterations` looseness:** the original test only asserted `stop_reason != "end_turn"`, satisfied by any arbitrary non-`end_turn` value, weaker than the README's claim that exhaustion is "distinguishable, reportable." Tightened: the docstring contract now states the exact required sentinel (`stop_reason: "max_iterations"`), and the test asserts that value specifically.
- The flawed attempt originally named `trusts-attempted-call-attempt` was renamed `trusts-identifier-attempt` and its bug redesigned: after the identity-binding fix, "records a call regardless of success" stopped being an observable bug in this system (error responses never carry a `customer_id` key, so the distinction was invisible to the test suite). The more realistic and more interesting bug it now demonstrates: trusting the raw `identifier` the caller *asked* `get_customer` to look up, instead of the `customer_id` the backend's result actually verified — these are not guaranteed to be the same value, and conflating them silently reintroduces the identity-binding gap through a different door.

Full reconciliation: `docs/decisions.md`'s 2026-07-15 Module 04 doubt-driven-development entries.

## Fable-model critique of the remediation itself, and what it changed

Per this project's own standing practice, a Fable-model subagent then critiqued the *remediation*, not the original findings — reading the actual current files rather than trusting a summary. Verdict: sound at its core (every claim reproduced exactly on independent re-run, no scope creep), but incomplete at the documentation edges, plus one real test-coverage gap:

- **Stale pre-fix rule statements survived in two live documents:** `fixtures/resolve/SPEC.md` and the shipped `fixtures/resolve/src/tools/process_refund.py` (plus its copies inside all five Module 04 attempt directories, which are active supporting infrastructure for this module's own dry run, not frozen history) still stated the weaker "get_customer has already succeeded" rule, with no mention of *which* customer. Fixed: all rewritten to name the customer-identity binding explicitly.
- **A stale quotation inside the shipped `tests/test_agent.py` itself** referenced the pre-fix docstring wording verbatim. Fixed.
- **Real test-coverage gap:** `trusts-identifier-attempt` was only caught in the false-*block* direction (over-blocking a legitimate refund) — no test exercised the false-*allow* direction the bug actually reintroduces (binding verification to the request instead of the result, so a refund could be allowed for a customer_id that was never actually the one verified). Added `test_loop_blocks_refund_when_requested_customer_id_matches_the_looked_up_identifier_but_not_the_verified_result`: `get_customer(identifier="cust_1")` resolves to a *different* real `customer_id` ("cust_42"), then `process_refund(customer_id="cust_1")` is attempted — the correct implementation blocks (verified customer was "cust_42", not "cust_1"); `trusts-identifier-attempt` incorrectly allows it. Test suite grew from 16 to 17 tests; `trusts-identifier-attempt` now fails 2/17 (both directions of its bug caught).
- **One undocumented-but-correct design choice, left as documentation only:** a second successful `get_customer` call for a *different* customer overwrites `verified_customer_id` (last-verified-wins) — fails closed on every malformed path traced, but was nowhere stated. A docstring sentence was added to both the shipped stub and the reference implementation; no mechanism change (would have been over-correction for an already fail-closed behavior).

## Attempts (final)

1. **`correct-attempt/`** — identity-bound hook, `max_iterations` sentinel, `backend=backend` always passed explicitly.
2. **`no-hook-attempt/`** — the loop never calls `verify_before_refund_hook` before dispatch.
3. **`text-parsing-attempt/`** — terminates early on wrap-up-sounding text despite `stop_reason: "tool_use"`.
4. **`trusts-identifier-attempt/`** — binds `verified_customer_id` to the raw `identifier` requested, not the `customer_id` the backend's result actually verified.
5. **`thin-docstring-attempt/`** — behaviorally identical to `correct-attempt/`, all reasoning stripped from docstrings, minimal (but deterministically-sufficient) rejection messages.

## Results (final, 17 tests)

| Attempt | Cumulative gate (01+02+03) | Loop lifecycle tests | Hook tests | Integration tests | Overall |
|---|---|---|---|---|---|
| correct | PASS | PASS | PASS | PASS | **PASS** (17/17) |
| no-hook | PASS | PASS | PASS (isolated hook-unit tests) | 5 FAIL | **FAIL** (12/17) |
| text-parsing | PASS | 1 FAIL | PASS | PASS | **FAIL** (16/17) |
| trusts-identifier | PASS | PASS | PASS | 2 FAIL | **FAIL** (15/17) |
| thin-docstring | PASS | PASS | PASS | PASS | **PASS** (17/17, conceptually weak) |

A sixth, ad hoc construction (not a permanent attempt directory): a copy of `correct-attempt/` with `tools[tool_name](**tool_args, backend=backend)` changed to omit `backend=backend`. Result: `TypeError: make_spy_tool.<locals>.tool() missing 1 required keyword-only argument: 'backend'`, surfaced as 9 failing tests — confirms the test-double fix actually closes the loophole, not just in principle.

Cumulative-gate isolation, re-confirmed: running `verify_module_04.py` against `fixtures/resolve/` directly (no Module 01-03 work) fails at the cumulative-gate step before `test_agent.py` even collects.

Regression check: Modules 01, 02, and 03's own dry-run attempts re-run unchanged against their respective checkers after this module's `backend.py` docstring edit and Module 03 README fix — all outcomes match their pre-existing expected results exactly.

## Finding

The proactively-constructed `thin-docstring-attempt` closed the conceptual-tier gap this arc had needed an external review to find in every prior module — a real, evidenced improvement in this pipeline's own discipline. But it didn't catch everything: the identity-binding gap survived both the initial dry run *and* would have survived shipping without doubt-driven-development, because none of the five originally-constructed attempts happened to probe "verify one customer, refund a different one" — a gap in adversarial-attempt construction, not in the checker once the right test existed. And even after that fix, the Fable-model critique found the fix itself was only half-tested (the false-block direction, not the false-allow direction) and had left stale pre-fix rule statements in two live documents. This is itself evidence for why every stage of this process — dry run, doubt-driven-development, and a critique of the remediation — stays mandatory even as proactive discipline improves at each prior stage: each one catches a category of gap the one before it structurally can't, because each is checking a different thing (behavior against a mental model of failure modes; behavior against a fresh reviewer's mental model; the fix itself against what it actually claims to fix).

## What this does and doesn't validate

**Validated:** the deterministic tier discriminates all constructed behavioral flaws correctly, including the identity-binding gap once real tests existed for it; the cumulative gate chains through all three prior modules; the `backend.py` scope decision doesn't regress any prior module and no longer contradicts Module 03's own README; the test-double `backend`-omission loophole is closed and empirically verified; rubric criterion 2's necessity is directly evidenced by `thin-docstring-attempt`.

**Not validated:** no real learner attempt exists yet, same open gap as every prior module. No attempt constructs a genuinely long, realistic multi-turn conversation exercising the hook under drift (e.g., many tool calls across several unrelated customers in one session) — the current tests are short, deliberately minimal scripted scenarios.

## Files

- `correct-attempt/`, `no-hook-attempt/`, `text-parsing-attempt/`, `trusts-identifier-attempt/`, `thin-docstring-attempt/` — the five constructed attempts, full project copies (seeded from Module 03's own `correct-attempt/`, which already has working `src/tools/*.py`, `src/backend.py`, `src/extraction.py`).
- `fixtures/resolve/tests/test_agent.py` — the provided test suite (17 tests), shipped with the fixture.
- `scripts/verify_module_04.py` — the deterministic checker, chaining `verify_module_03.py` (which chains `verify_module_02.py`, which chains `verify_module_01.py`).
