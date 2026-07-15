# Module 01: Configuring Claude Code for Real Work

## The question this module answers

How do you configure Claude Code so it works the way your team needs, not the way it ships by default?

## Where it sits in the arc

First module. No prior module: this is day-one harness fluency, assumed by every later module rather than taught by any of them again. Next: [Module 02, Prompts and Structured Output That Survive Production](../02-prompts-structured-output/README.md) — the hinge is that Module 02's exercises are *delivered through* the Claude Code configuration this module builds. See [`modules/README.md`](../README.md) for the full arc.

## Exercise: configure `resolve`

Runs against `fixtures/resolve/`, the one shared project every module in Part 1 of this workshop builds a real capability onto (see that directory's `SPEC.md` for the full spec and the module-by-module build-out table). `resolve` is a customer support resolution agent, modeled directly on CCA-F's own Scenario 1: it handles returns, billing disputes, and account issues, backed by MCP tools (`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`), with one non-negotiable safety rule: `process_refund` must never fire before `get_customer` has returned a verified customer ID.

`fixtures/resolve/` ships with a real but incomplete codebase (four stub MCP tools, a stub agent, a placeholder test file) — your job in this module isn't to implement any of that code. It's to configure Claude Code for it, for real production team use:

1. A project-root `CLAUDE.md` with real project context and the safety rule stated plainly.
2. At least one path-scoped `.claude/rules/` file whose glob pattern actually matches real files under the project — not just present, *scoped to something real*.
3. At least one project-scoped slash command in `.claude/commands/`.

Get `scripts/verify-module-01.sh` (run from the repo root, pointed at your attempt) to pass, from your own harness, without narrating the fix as you go, then check it against the rubric below.

## Rubric

1. **`scripts/verify-module-01.sh` exits 0 against your configuration (gate, deterministic).** Checks structure exists and that any path-scoped rule's glob actually resolves against real files in the project — a rules file that exists but matches nothing is treated as equivalent to having none.
2. **Every convention that applies to only part of the project lives in a path-scoped `.claude/rules/` file, not the project-root `CLAUDE.md` (scored, conceptual).** The root file states what's true everywhere; anything true only of `src/tools/**` or `tests/**` belongs in its own scoped file.
3. **A teammate cloning this repo cold can find the safety-critical rule (verify-before-refund) without reading every file in the project (scored, conceptual).** Where that rule lives, and how prominently, is a real design choice this module tests directly.
4. **The project-scoped slash command does something a real contributor to this specific project would actually reach for**, not a generic placeholder (scored, conceptual).

**Before trusting a green `scripts/verify-module-01.sh` as proof you're done:** it is not the same claim as "this configuration is genuinely well-structured." A configuration that technically satisfies every mechanical check (a rules file exists, its glob matches something) can still bury the safety rule, misuse the slash command, or split conventions along the wrong boundary. This isn't hypothetical: this exercise's own dry run (`runs/2026-07-14-module-01-dry-run/grading.md`) found a genuinely plausible, content-correct attempt that failed the deterministic tier entirely (a single monolithic `CLAUDE.md`, structurally wrong despite accurate content) — and, separately, that the checker script itself had a real bug (a glob pattern that silently never matched anything without `globstar` enabled) until the dry run caught it. Criteria 2-4 exist because criterion 1 provably can't catch a configuration that's mechanically present but conceptually thin.

## Required to advance / stop condition

Produce a Claude Code configuration for `fixtures/resolve/` that passes `scripts/verify-module-01.sh` and demonstrates all three scored criteria above. Reading this page does not count: advancement requires a working, checker-verified attempt Coachgremlin has actually reviewed against the rubric, not on having read it.

**Valid alternate terminal:** if your first attempt puts everything in one root `CLAUDE.md` (the naive attempt this module's dry run constructed), that's not a failure, it's the actual exercise. Go back and ask: which of these conventions is true of the *whole* project, and which is only true when someone's editing a specific area? Split accordingly.

## Before you start: a non-scored self-check

Before running `scripts/verify-module-01.sh` for the first time, predict its output without looking at the script's source: which of your files do you expect to pass, which do you expect to fail, and why? Write the prediction down, then run the check and compare. This isn't graded — it's a habit for noticing whether *you* understood the configuration hierarchy, or whether your agent produced something that happens to look right. See `.claude/skills/agentic-learning-discipline/SKILL.md` (packaged once a learner completes this module) for why this matters more here than it might seem: Claude Code can produce a plausible-looking `.claude/rules/` file in one paste, whether or not the person asking for it understands why the split matters.

## Takeaway

A personal CLAUDE.md/rules/skills starter kit, structured the way the exam blueprint expects (hierarchy, path-scoping, frontmatter options) — built from your own configuration decisions on `resolve`, not copied from documentation.

---

*Module content authored 2026-07-14. Dry run complete: `runs/2026-07-14-module-01-dry-run/grading.md`.*
