# Module 09 dry run: Shipping Responsibly — Governance, Stakeholders & Team Enablement

**Date:** 2026-07-17.
**Purpose:** validate that Module 09's deterministic tier (`scripts/verify_module_09.py`) discriminates real attempts on all three of its deliverables — a human-in-the-loop governance gate (code), a stakeholder-facing shipping-readiness review (prose), and real team tooling configuration (`.claude/`) — and that it correctly chains `check_module_08`.

## The scenario, and why it's not a new internal team this time

Every module since Module 07 has opened on a new internal team's stated problem. Module 09 deliberately doesn't — it asks what has to happen *before* Module 08's own system (the Platform Docs team's doc_qa RAG pipeline) actually ships to real users. That's the real shape of Domain 5/6/7's combined objectives: governance and stakeholder communication apply to a system that already exists and has already been evaluated, not a hypothetical. Chaining `check_module_08` isn't just the cumulative-gate convention here — it's structurally what the module is about.

**Three required deliverables, matching Domain 5 (Governance, Safety & Risk), Domain 6 (Stakeholder Communication & Lifecycle), and Domain 7 (Developer Productivity & Operational Enablement):**

1. **`fixtures/foundry/src/governance.py`** (build-from-stub) — `answer_question_with_governance` sits in front of `doc_qa.answer_question` and inspects retrieved chunks for sensitive content *before* ever calling `model_client`, withholding the answer entirely (not just redacting it after the fact) when flagged. `approve_and_release` requires a real, non-empty `approver_id` — a genuine audit trail — before releasing the real answer. The compliance angle: the Platform Docs team's corpus includes security runbooks referencing credentials and PII as a byproduct of documenting real incidents.
2. **`fixtures/foundry/docs/shipping-readiness-review.md`** (prose, regex-section-checked, reusing Module 07's `check_adr` pattern) — 4 required sections: Failure Modes, Compliance Requirement and Architectural Consequence, Human-in-the-Loop Checkpoint, Stakeholder Summary.
3. **`fixtures/foundry/.claude/`** (Domain 7, reusing Module 01's own exercise shape and checker helpers) — real rules scoping `src/**` and `tests/**`, plus a project-scoped slash command, for `fixtures/foundry/` itself.

## Attempts constructed

1. **`correct-attempt/`** — all three deliverables real: governance gate correctly checks sensitivity before any model call, a real 4-section shipping-readiness review, real `.claude/rules/` + `.claude/commands/`.
2. **`unfixed-attempt/`** — the shipped state exactly: `governance.py` stub (only `contains_sensitive_content` implemented), no review doc, no `.claude/` config at all.
3. **`no-review-doc-attempt/`** — governance gate and `.claude/` config both real and correct; `docs/shipping-readiness-review.md` doesn't exist.
4. **`weak-tooling-attempt/`** — governance gate and review doc both real and correct; `.claude/rules/` only scopes `tests/**`, no rule scopes `src/**`, and no `.claude/commands/` directory at all.
5. **`bypasses-model-client-attempt/`** — the subtlest attempt: `governance.py` returns the *correct-looking* `GovernedAnswer` (answer nulled out when flagged, `requires_human_review=True`) but calls `answer_question` (and therefore `model_client`) *before* checking retrieved content for sensitivity — the compliance violation (sensitive content reaching a model call) has already happened by the time the function decides to withhold the result from the caller.

## Results (17 tests, chains `check_module_08`, post-doubt-driven-development)

| Attempt | Tests | Review doc | Tooling | Overall |
|---|---|---|---|---|
| correct | PASS (17/17) | PASS | PASS | **PASS** |
| unfixed | FAIL (5/17, 12 fail) | FAIL | FAIL | **FAIL** |
| no-review-doc | PASS (17/17) | FAIL | PASS | **FAIL** |
| weak-tooling | PASS (17/17) | PASS | FAIL (2 checks) | **FAIL** |
| bypasses-model-client | FAIL (11/17, 6 fail) | PASS | PASS | **FAIL** |

(Originally 14 tests; doubt-driven-development grew the suite to 17 — see below. Isolation re-confirmed after every change: `no-review-doc-attempt` and `weak-tooling-attempt` each fail *only* their own targeted deliverable; `bypasses-model-client-attempt`'s 6 failures are all within the governance/call-order category, zero bleed into the review-doc or tooling checks.)

## Doubt-driven-development review, before treating this module as done

Standing practice, continued from every prior module — this review's dominant finding is the single most severe of any module in this project to date, since it defeated the exercise's entire core safety property while looking correct.

**Stage 1 (fresh Claude subagent):** most severe finding, **empirically confirmed live**: every one of the original 14 tests happened to place the sensitive marker word (e.g. "password") in *both* the query string and the retrieved chunk's text. A submission checking `contains_sensitive_content(query)` — the query, never inspecting any retrieved chunk's actual content — passed all 14 tests while completely defeating the module's purpose: any query whose own wording avoids a trigger word sails straight through to `model_client`, even when the retrieved document contains a real secret. Confirmed live: this exact mutant scored 14/14, `Deterministic tier: PASS`. Also found: the `.claude/` team-tooling checker accepts a bare-directory glob match (`paths: ["src"]`, no wildcard, matches the directory node itself) and an overly-broad single-pattern rule file with no real prose; the readiness-review's structural check accepts keyword-stuffed, content-free prose (an already-accepted, disclosed limitation matching Module 07's own ADR checker); `approve_and_release` has no binding to a specific prior-flagged query or real identity system (any non-blank string works) — disclosed rather than fixed, since no real auth system exists in this environment.

**Stage 2 (Codex cross-model):** confirmed the query-vs-chunk finding and the shared `.claude/` checker weakness (independently verifying it's the *same root cause* in `verify_module_01.py`'s own `check_module_01`, not a Module-09-only bug), then surfaced its own dominant finding, also **empirically confirmed live**: `review_reason` (the human-readable withholding explanation) was only checked for non-emptiness — a submission setting `review_reason = flagged[0].text` (the actual sensitive chunk content) passed all 14 tests, meaning the "withheld" answer leaked the sensitive content right back to the caller through the one field meant to protect it. Also found only 1 of 4 withholding-path tests asserted `result.answer is None` (the other 3 only checked `requires_human_review` and call count), and `approve_and_release`'s default `top_k=3` was never exercised.

**Fixed:** two new tests closing the two critical gaps, each verified live against its exact target mutant before being trusted — `test_governance_withholds_based_on_chunk_content_even_when_the_query_itself_is_clean` (a query with zero overlap with any sensitive marker, retrieving a chunk that does contain one) and `test_governance_review_reason_never_leaks_the_actual_sensitive_chunk_text` (asserts a specific secret string doesn't appear in `review_reason`). `answer is None` assertions added to the 3 previously-uncovered withholding tests; `test_approve_and_release_default_top_k_is_three` added. Test suite grew from 14 to 17. The shared bare-directory-match bug fixed in *both* `verify_module_01.py` and `verify_module_09.py` at once (same precedent as Module 07's project-wide checker fix) — matches are now filtered to real files only (`m.is_file()`), not directory nodes; re-verified live that the bypass is closed on both checkers, and that all 4 of Module 01's own dry-run attempts plus the full 25-attempt Part 1 regression (which chains through `check_module_01`) still reproduce their exact expected pattern.

**Stage 3 (Fable-model critique of the remediation):** unavailable this session ("Usage credits are required for this model" — an account-level limit, not transient). Proceeded without it on the user's explicit direction, given Stages 1 and 2 already found and fixed two independently-confirmed critical issues plus three further real ones, each verified live against constructed mutants — solid coverage even without a third pass. Flagged here rather than silently skipped.

## What this does and doesn't validate

**Validated:** the deterministic tier discriminates all four constructed flaws with clean, non-overlapping isolation across three structurally different deliverable types (code, prose, filesystem config) in one gate, after two full doubt-driven-development rounds; `check_module_09` correctly chains `check_module_08`; the checker's test-execution applies the neutral-temp-dir + expected-pass-count hardening from the start; Module 01's own frontmatter-parsing helpers were reused rather than reimplemented, and a real, shared precision bug in that reused logic was found and fixed in both checkers at once.

**Not validated:** no real learner attempt exists yet, same open gap as every prior module. `contains_sensitive_content`'s keyword-based detection is a coarse, disclosed proxy for a real PII/security classifier (won't catch a bare SSN digit pattern without the word "SSN" nearby), same discipline as `doc_qa.py`'s own `score_chunk`. `approve_and_release`'s lack of binding to a specific flagged query or real identity system is a genuine, disclosed simplification — a real production system would need a real auth/audit integration this environment can't provide. The Fable-model critique stage did not run this session; a future pass against the current, already-twice-reviewed files remains open.

## Files

- `correct-attempt/`, `unfixed-attempt/`, `no-review-doc-attempt/`, `weak-tooling-attempt/`, `bypasses-model-client-attempt/` — the five constructed attempts, full project copies (each carrying Modules 07-08's own completed work, since the gate chains `check_module_08`).
- `fixtures/foundry/tests/test_governance.py` — the provided test suite (17 tests after doubt-driven-development, up from 14), shipped with the fixture.
- `scripts/verify_module_09.py` — the deterministic checker: chains `check_module_08`, canonical-test execution with the same hardening as Modules 07-08, a regex-based prose review checker reused from Module 07's `check_adr`, and a `.claude/` team-tooling checker reusing Module 01's own frontmatter/safe-pattern helpers.
