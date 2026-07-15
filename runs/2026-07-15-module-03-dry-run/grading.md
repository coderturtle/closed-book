# Module 03 dry run: Designing Tools and MCP Interfaces

**Date:** 2026-07-15
**Purpose:** validate that Module 03's deterministic tier (`scripts/verify_module_03.py`, chaining Module 02's checker, which chains Module 01's) discriminates real attempts, and that the rubric's split between deterministic and conceptual criteria is drawn correctly from the start — applying the lesson from both prior modules' doubt-driven-development reviews before, not after, a review finds the gap.

## A real bug found before any attempt was graded

The first version of every tool file put its description in the **module** docstring (the `"""..."""` at the top of the file), not the **function's own** `__doc__`. `get_customer.__doc__` and `lookup_order.__doc__` came back empty strings, not the intended text — a real bug, not a test artifact: real MCP tooling derives a tool's description from the function's own docstring, and a description that exists in the file but not on the function object wouldn't reach an agent either. Fixed by moving every tool's description into the function body, in both the shipped stubs and this dry run's reference implementation, before any attempt was constructed against the old (broken) shape.

## Attempts constructed

1. **`correct-attempt/`** — real implementations of all four tools: `get_customer`/`lookup_order` return structured "not found" results (never leaking whether a mismatched order belongs to someone else); `process_refund` independently re-verifies `customer_id` against the backend (defense in depth, distinct from Module 04's later session-level hook), rejects orders that don't belong to the customer, and rejects amounts outside the refundable range; `escalate_to_human` requires a real, non-empty `root_cause` and `recommended_action`. All four share one error shape (`src/tool_errors.py`).
2. **`trusts-caller-attempt/`** — a real, plausible mistake: `process_refund` skips its own `backend.find_customer` re-verification, reasoning "Module 04's hook already checks this before the tool is even called." True for the intended call path; this tool has no way to know it was actually reached through that path.
3. **`weak-docstring-attempt/`** (constructed proactively, applying the lesson from Modules 01-02's own doubt-driven-development reviews rather than waiting for one to find the gap) — all four tools behave correctly; docstrings are minimal ("Gets a customer. Takes an identifier which could be an email, phone, or account thing.") — technically containing the required disambiguating keywords, so the deterministic presence check still passes, but giving an agent no real boundary reasoning to act on.

## Results

| Attempt | Cumulative gate (Modules 01+02) | Tool behavior tests | Docstring presence tests | Overall |
|---|---|---|---|---|
| correct | PASS | PASS (16/16) | PASS | **PASS** |
| trusts-caller | PASS | 1 FAIL (`test_process_refund_fails_closed_on_unverified_customer`) | PASS | **FAIL** (15/16) |
| weak-docstring | PASS | PASS | PASS (keywords present) | **PASS** (16/16, conceptually weak) |

## Finding

`trusts-caller-attempt` fails narrowly and precisely on the one test that exists specifically to catch it — real evidence the safety-critical defense-in-depth property is actually gate-checked, not just described in a docstring. `weak-docstring-attempt` passes every deterministic test while giving an agent nothing usable to disambiguate `get_customer` from `lookup_order` beyond keyword-matching — the exact case rubric criterion 3 (conceptual) exists to catch, constructed *before* shipping this module rather than found afterward by an adversarial review, applying what both prior modules' reviews independently established: a deterministic presence check and a genuine quality check are different claims, and only constructing an attempt that separates them proves the rubric's conceptual tier is doing real work.

## What this does and doesn't validate

**Validated:** the cumulative gate chains correctly through both prior modules; the tool-behavior test suite catches the safety-critical defense-in-depth omission; the docstring-presence tests pass on both a genuinely good and a genuinely weak docstring, confirming rubric criterion 3 (not the test suite) is what has to catch the weak case.

**Not validated:** rubric criterion 4 (process_refund's defense-in-depth reasoning documented as deliberate, not incidental) has no attempt isolating it specifically — `correct-attempt`'s docstring already states this reasoning, and no constructed attempt has the correct behavior with that reasoning absent. No real learner attempt exists yet, same open gap as Modules 01 and 02.

## Files

- `correct-attempt/`, `trusts-caller-attempt/`, `weak-docstring-attempt/` — the three constructed attempts, full project copies.
- `fixtures/resolve/tests/test_tools.py` — the provided test suite (16 tests), shipped with the fixture.
- `scripts/verify_module_03.py` — the deterministic checker, chaining `verify_module_02.py` (which chains `verify_module_01.py`).
