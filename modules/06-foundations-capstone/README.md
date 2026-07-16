# Module 06: Foundations Capstone — Sit-Ready for CCA-F

## The question this module answers

Are you actually ready to sit the real Claude Certified Architect – Foundations exam?

## Where it sits in the arc

Sixth module, closing Part 1 (Architect Foundations). Hard prerequisite: all of [Module 01](../01-configuring-claude-code/README.md)–[Module 05](../05-context-reliability/README.md) — this module's checker chains Module 05's (which chains Module 04's, Module 03's, Module 02's, Module 01's), and its hands-on exercise is a real integration of Modules 02, 04, and 05's own code, not a new isolated capability. A learner could stop here, sit the real CCA-F exam, and treat Part 2 as a separate, later commitment. Next, if continuing: [Module 07, Designing the Solution](../07-solution-design-context-strategy/README.md), which opens Part 2 (Architect Professional). See [`modules/README.md`](../README.md).

## Exercise: diagnose and fix a real, seeded cross-module defect

This module's shape is different from every prior one, deliberately. Modules 01-05 each shipped a stub (`raise NotImplementedError`) and asked you to implement it. `fixtures/resolve/src/session.py` ships **fully written and already running** — `run_full_support_session`, a real integration of Module 02's extraction, Module 04's agentic loop and hook, and Module 05's case facts and escalation decision into one function. It also ships with **two real, seeded defects**, each spanning a different pair of those modules. `scripts/verify_module_06.py`'s provided test suite already fails against this file exactly as shipped. Your job is to diagnose each failure's actual root cause and fix it — not to rewrite the function from scratch, and not to make the failing tests pass by weakening what they check.

This file's own docstring intentionally does not say which lines are the bugs. Figuring out *why* a specific test fails, using the prior modules' own docstrings and this file's structure as your evidence, is the real diagnostic skill CCA-F's own scenario-based format tests — not a fact you're handed upfront.

Two model clients are injected with genuinely different shapes: `extraction_model_client` is Module 02's `(prompt, prior_attempts) -> dict`; `agent_model_client` is Module 04's `(conversation_history) -> dict`. They are not interchangeable — a correct fix does not collapse them into one, and if your fix does that, you've changed the contract, not fixed the defect.

Get `python3 scripts/verify_module_06.py <path-to-your-attempt>` (run from the repo root) to pass — starting from 2 of 6 tests already failing — then check it against the rubric below.

## The two-tier gate

**Tier 1 — deterministic, hands-on with Claude Code.** `scripts/verify_module_06.py`: chains Module 05's check (which chains Module 04's, Module 03's, Module 02's, Module 01's) via a real importable `check_module_05`/`check_module_06` function, then runs the *repo's own canonical copy* of the test suite against your `session.py` — not whatever copy sits in your own submission.

**Tier 2 — exam-condition, closed-book without Claude Code.** [`checkpoint.md`](checkpoint.md): a full mock exam matching CCA-F's own real structure rather than the workshop's smaller per-module default — a pool of 6 original scenarios (none of them the real exam's own published scenarios), complete 4 of the 6 (drawn, not self-selected), 120 minutes, 720/1000 to pass. See the checkpoint's own scope note for the honest reduction from the real exam's ~60-question total to this pool's 42.

Both tiers are required to advance.

## Rubric (deterministic tier's rubric; the closed-book mock exam is scored separately)

1. **`python3 scripts/verify_module_06.py` exits 0 (gate, deterministic).** The chained cumulative gate passes, and all 6 provided tests pass.
2. **Both defects are fixed at their actual root cause, not worked around (scored, conceptual, though partially deterministic — the test suite is specifically constructed so that fixing only one defect, or "fixing" one by deleting the feature it belongs to, still leaves at least one test failing).** This module's own dry run constructed exactly these two failure modes (`fix-bug1-only-attempt`/`fix-bug2-only-attempt`, and `over-correction-attempt`, which deletes the extraction step entirely rather than fixing its misuse) — read `runs/2026-07-16-module-06-dry-run/grading.md` before assuming a single passing test tells you which defect, if either, you've actually fixed.
3. **Your own written explanation of each defect's actual root cause and why the fix addresses it, not just that the tests now pass (scored, conceptual).** A green checker proves behavior; it doesn't by itself demonstrate diagnosis, which is the skill this module exists to test.

**Before trusting a green checker as proof you're done:** unlike every prior module, this one's checker was never expected to start green — 2 of 6 tests fail against the exact file you're given. If you find yourself editing `tests/test_session.py` to make a failure go away, you've mistaken the gate for the obstacle; the gate is doing its job. Read `runs/2026-07-16-module-06-dry-run/grading.md` for the real dry run behind this exercise, including exactly which lines seed each defect and why an over-corrected "fix" (deleting a whole feature instead of its misuse) is caught as cleanly as an incomplete one. A doubt-driven-development review (fresh Claude subagent + Codex) found a *third*, more severe gap in what this module originally shipped as its own "correct" reference: a hook rejection never reached `should_escalate` at all, so a model stuck repeatedly attempting a blocked `process_refund` made no progress yet never escalated — silently running to `max_iterations` instead, contradicting this project's own stated fail-closed default. That's not one of the two things you're asked to diagnose; it's fixed uniformly in the code you're given, and a 6th test (`test_repeated_hook_rejections_eventually_escalate`) now checks it directly.

## Required to advance / stop condition

Fix both seeded defects so that `scripts/verify_module_06.py` passes, write your own root-cause explanation for each (rubric criterion 3), **and** complete 4 of the mock exam's 6 scenarios at 720/1000+. Reading this page does not count.

## Before the mock exam: a non-scored self-check

Before opening `checkpoint.md`, predict, for each of the 6 scenarios in the pool, which CCA-F domain(s) it's actually testing — the scenario names don't announce this the way this workshop's own module titles do. Before running `scripts/verify_module_06.py` for the first time, read `src/session.py` in full and predict which two things about it feel structurally suspicious, *before* running any test and seeing which ones actually fail. If you can't form a suspicion without the test output telling you first, that's the actual skill this module is testing — CCA-F's own scenario-based questions expect you to reason about a system's structure, not just pattern-match against a known failure. See [`.claude/skills/agentic-learning-discipline/SKILL.md`](../../.claude/skills/agentic-learning-discipline/SKILL.md).

## Takeaway

A personal CCA-F exam-day prep sheet, built from your own mock-exam attempt's actual weak spots — which scenarios and domains you missed, not a generic study guide. **Not produced by the graded exercise itself, and not claimed as one:** a general diagnostic checklist for "how to find a cross-module defect in an unfamiliar agentic codebase" would be a natural artifact to write once you've done this exercise, but this module's own rubric doesn't require or check for one — the two seeded defects here are specific, not a template for defects in general.

---

*Module content authored 2026-07-16, both tiers built together from the start. A doubt-driven-development review the same day found a third, real gap in the "correct" reference implementation (hook rejections never reached `should_escalate`) — remediated same day, see `docs/decisions.md`. Dry run: `runs/2026-07-16-module-06-dry-run/grading.md`.*
