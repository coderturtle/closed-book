# Module 01 dry run: Configuring Claude Code for Real Work

**Date:** 2026-07-14, updated 2026-07-15 after a doubt-driven-development review.
**Purpose:** validate that Module 01's two-tier gate — the deterministic checker (`scripts/verify_module_01.py`) and the conceptual rubric it doesn't cover — actually discriminates real attempts, per Coachgremlin's Workflow step 3.

## 2026-07-15 update: doubt-driven-development review and remediation

Before this module was treated as done, a doubt-driven-development pass ran two independent adversarial reviews (a fresh-context Claude subagent, and Codex CLI) against the full artifact — the exercise, rubric, checker script, SPEC.md, and this grading record — plus a Fable-model subagent tasked with critiquing and replanning given both reviews' findings. Both reviews found substantial, largely non-overlapping, mostly real issues; full reconciliation and the resulting remediation plan are recorded in `docs/decisions.md`'s 2026-07-15 entries. Headline findings that changed this module materially:

- **The closed-book checkpoint tier didn't exist at all** (Codex's most severe finding) — Module 01 had only ever shipped the hands-on tier. Now authored: `checkpoint.md`, 12 originally-written questions covering the full CCA-F Domain 3 blueprint (3.1-3.6), including the process-only task statements (plan mode, iterative refinement) the hands-on tier structurally can't test.
- **The bash checker had several real bugs**, independently verified: a non-portable `globstar` dependency (macOS's `/bin/bash` 3.2 doesn't support it), quoted-only YAML pattern matching (false negative on idiomatic unquoted lists), a scoping check weak enough that a rule scoped to the wrong directory could still pass, and a glob-match with no protection against patterns escaping the project directory via `../` or an absolute path. Rewritten in Python (`scripts/verify_module_01.py`); the rewrite closes all of these structurally rather than patching each independently.
- **Rubric criterion 2 named the technique it was testing for** ("lives in a path-scoped `.claude/rules/` file"), violating this module's own stated property-phrased-criteria rule. Rewritten as an observable property.
- **A real bug was found in the *rewrite itself* during re-verification**, not just inherited from the bash version: the new CI-readiness check initially matched `SPEC.md`'s own prose describing the requirement (which contains the literal string "claude -p"), making the check a permanent, silent no-op for every attempt, including ones that documented nothing. Fixed by excluding `SPEC.md` from the search. This is the same category of finding as the original `globstar` bug: a check that looks correct and reports a clean pass while not actually checking anything.

## Attempts constructed

1. **`naive-attempt/`** — an honest, plausible first instinct: a single, comprehensive root `CLAUDE.md` covering everything. Correct content, wrong structure.
2. **`correct-attempt/`** — the same content split across a scoped `CLAUDE.md`, two path-scoped `.claude/rules/` files (`src/tools/**/*`, `tests/**/*`), a project-scoped slash command, and (added 2026-07-15) a documented `claude -p` CI invocation.
3. **`broken-glob-attempt/`** — a rules file that exists, has valid frontmatter, and has a `paths:` key, but the glob is typo'd (`src/tool/**/*`, singular) and matches nothing real.
4. **`weak-conceptual-attempt/`** (added 2026-07-15, the previously-flagged missing case) — a rules setup and slash command that are all structurally present and correctly scoped, satisfying every mechanical check, but the *content* is nearly empty ("Write good, clean code," "Write tests for things," a slash command that says hello) and the safety-critical verify-before-refund rule is omitted from `CLAUDE.md` entirely.

## Results

| Attempt | CLAUDE.md | rules exist | scoped to `src/tools/**` | scoped to `tests/**` | commands exist | CI documented | Overall (deterministic) |
|---|---|---|---|---|---|---|---|
| naive | OK | FAIL | FAIL | FAIL | FAIL | FAIL | **FAIL** |
| correct | OK | OK | OK | OK | OK | OK | **PASS** |
| broken-glob | OK | OK | FAIL | FAIL | FAIL | FAIL | **FAIL** |
| weak-conceptual | OK | OK | OK | OK | OK | OK | **PASS** |

## Finding

The deterministic tier correctly discriminates structural presence and correctness (attempts 1-3), including the case that matters most for that tier: a rules file that's syntactically present but scopes to nothing real. It does **not**, and by its own stated design cannot, catch attempt 4 — a submission that is mechanically complete but conceptually empty. Rubric criteria 3 ("a teammate cloning this repo cold can find the safety-critical rule... without reading every file") and 4 ("the slash command does something a real contributor would actually reach for") are exactly what catches this attempt, and both fail it: the safety rule is absent entirely, and the command is a placeholder.

**This is the validating evidence the 2026-07-14 version of this dry run explicitly flagged as missing**: prior to this update, "whether the deterministic tier's pass is a reliable proxy for conceptual quality" was untested. It is now tested, and the answer is no — the two tiers catch genuinely different failure modes, which is the design's actual justification, not just its stated rationale.

## What this does and doesn't validate

**Validated:** the deterministic tier's mechanical checks discriminate structural attempts correctly (1-3), and the conceptual tier catches at least one real, concrete way a submission can pass the deterministic tier while failing the actual point of the exercise (attempt 4).

**Not validated:** whether a real learner's rubric-criteria 2-4 assessment (done by an actual Coachgremlin session reading a real attempt, not a constructed one graded by inspection) produces consistent, defensible scores — that requires a real learner, still the workshop's largest open gap (`docs/next-actions.md`).

## Files

- `naive-attempt/`, `correct-attempt/`, `broken-glob-attempt/`, `weak-conceptual-attempt/` — the four constructed attempts, full project copies.
- `scripts/verify_module_01.py` — the deterministic checker, rewritten in Python 2026-07-15 after the doubt-driven-development review; one further bug (the `SPEC.md` false-positive) found and fixed during this same re-verification pass.
