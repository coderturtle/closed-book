# Module 01 dry run: Configuring Claude Code for Real Work

**Date:** 2026-07-14
**Purpose:** validate that Module 01's deterministic tier (`scripts/verify-module-01.sh`) actually discriminates a correct attempt from a plausible naive one, per Coachgremlin's Workflow step 3 ("two-tier grading for subjects with an objective checker" — check that tier first, mechanically, before any conceptual read).

## Attempts constructed

1. **`naive-attempt/`** — an honest, plausible first instinct: a single, comprehensive root `CLAUDE.md` covering the safety rule, tool conventions, and testing conventions all in one file. Content is correct (the safety rule is stated accurately, the conventions match what Module 03's tools will need); the structural choice is what's wrong. No `.claude/rules/` path-scoping, no slash command.
2. **`correct-attempt/`** — the same content, split across a project-root `CLAUDE.md` (project context + safety rule only) and two path-scoped `.claude/rules/` files (`tools.md` scoped to `src/tools/**/*`, `tests.md` scoped to `tests/**/*`), plus a project-scoped slash command (`.claude/commands/review-tool.md`).
3. **`broken-glob-attempt/`** — a third shape, added after the first two ran clean, to stress-test the checker itself: a `.claude/rules/tools.md` file that exists, has valid frontmatter, and has a `paths:` key — but the glob is typo'd (`src/tool/**/*`, singular, the project's real directory is `src/tools/`). Tests whether the deterministic tier catches a config that's structurally present but functionally inert, not just "does a rules file exist."

## Results

| Attempt | CLAUDE.md | rules/ exists | rules/ glob matches real files | commands/ exists | Overall |
|---|---|---|---|---|---|
| naive | OK | FAIL | FAIL | FAIL | **FAIL** |
| correct | OK | OK | OK | OK | **PASS** |
| broken-glob | OK | OK | **FAIL** | FAIL | **FAIL** |

## Finding

The deterministic tier discriminates correctly across all three constructed attempts, including the case that matters most: a rules file that's syntactically present (exists, has frontmatter, has a `paths:` key) but scopes to nothing real. A naive "does `.claude/rules/` contain a file" check would have passed `broken-glob-attempt` — this checker's actual glob-resolution step (`compgen -G` against the target project's own directory, with `globstar` enabled) is what catches it.

**A real bug was found and fixed during this dry run, not just a clean pass reported after the fact:** the first version of `scripts/verify-module-01.sh` failed the `correct-attempt` too, because `compgen -G` doesn't treat `**` as recursive without `shopt -s globstar` explicitly set. Without that fix, the checker would have produced a false negative against a genuinely correct attempt, exactly the kind of "the check itself is broken, not the attempt" failure the git-contract's own verification discipline exists to catch before it ships to a learner.

## What this does and doesn't validate

**Validated:** the deterministic tier's mechanical checks (structure exists, glob actually resolves) correctly separate all three constructed attempts as designed.

**Not validated:** whether the *conceptual* tier (is the CLAUDE.md's actual project-context prose good, is the slash command genuinely useful, would a real reviewer accept this configuration) adds real signal beyond the deterministic tier — that requires a real learner attempt, or at minimum a fourth constructed attempt that passes the deterministic tier but is conceptually weak (e.g. a rules file that scopes correctly but states wrong or vague conventions). Worth a follow-up dry run before treating Module 01's two-tier design as fully proven, same honesty discipline Borrow Native applied to its own Module 01/02 findings.

## Files

- `naive-attempt/`, `correct-attempt/`, `broken-glob-attempt/` — the three constructed attempts, full project copies.
- `scripts/verify-module-01.sh` — the deterministic checker, fixed during this run (globstar bug).
