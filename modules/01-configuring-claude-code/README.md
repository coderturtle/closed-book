# Module 01: Configuring Claude Code for Real Work

## The question this module answers

How do you configure Claude Code so it works the way your team needs, not the way it ships by default?

## Where it sits in the arc

First module. No prior module: this is day-one harness fluency, assumed by every later module rather than taught by any of them again. Next: [Module 02, Prompts and Structured Output That Survive Production](../02-prompts-structured-output/README.md) — the hinge is that Module 02's exercises are *delivered through* the Claude Code configuration this module builds. See [`modules/README.md`](../README.md) for the full arc.

## Exercise: configure `resolve`

Runs against `fixtures/resolve/`, the one shared project every module in Part 1 of this workshop builds a real capability onto (see that directory's `SPEC.md` for the full spec, the module-by-module build-out table, and the compatibility contract governing what later modules may assume from a passing submission here). `resolve` is a customer support resolution agent, modeled directly on CCA-F's own Scenario 1: it handles returns, billing disputes, and account issues, backed by MCP tools (`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`).

`fixtures/resolve/` ships with a real but incomplete codebase (four stub MCP tools, a stub agent, a placeholder test file) — your job in this module isn't to implement any of that code. It's to configure Claude Code for it, for real production team use:

1. A project-root `CLAUDE.md` with real project context and `resolve`'s canonical safety rule (`SPEC.md`) stated plainly.
2. At least one path-scoped `.claude/rules/` file scoped to real files under `src/tools/**`, and at least one scoped to real files under `tests/**` — not just present, *scoped to something real*.
3. At least one project-scoped slash command in `.claude/commands/`.
4. A documented, non-interactive `claude -p`/`--print` invocation somewhere in the project (CI-readiness) — not `SPEC.md`, which only describes the requirement; this has to be something you actually wrote.

Get `python3 scripts/verify_module_01.py <path-to-your-attempt>` (run from the repo root) to pass, from your own harness, without narrating the fix as you go, then check it against the rubric below.

## The two-tier gate

**Tier 1 — deterministic, hands-on with Claude Code.** `scripts/verify_module_01.py` against your configuration. Mechanical: structure exists, each rule's glob pattern actually resolves against real files in the right place, a CI invocation is documented somewhere real. No judgment call.

**Tier 2 — exam-condition, closed-book without Claude Code.** [`checkpoint.md`](checkpoint.md): 12 originally-written questions covering the full CCA-F Domain 3 blueprint (3.1–3.6), including process judgment calls (plan mode vs. direct execution, iterative refinement) the hands-on tier has no artifact to test. Close your Claude Code session before starting it. 80% (10/12) to pass.

Both tiers are required to advance. Neither substitutes for the other — see [`docs/design-tension.md`](../../docs/design-tension.md).

## Rubric (deterministic tier's rubric; the closed-book checkpoint is scored separately, see `checkpoint.md`)

1. **`python3 scripts/verify_module_01.py` exits 0 against your configuration (gate, deterministic).** Checks structure exists, that each required rule's glob actually resolves against real files in the correct location, and that a CI invocation is documented somewhere real — a rules file that exists but matches nothing, or matches the wrong directory, is treated as equivalent to having none.
2. **A convention true of only part of the project is discoverable only when that part is actually being edited; a convention true of the whole project is discoverable without editing anything (scored, conceptual).** Property, not technique: however you achieve this split, it should hold — a monolithic file that happens to mention everything doesn't satisfy this even if it's technically "in CLAUDE.md."
3. **A teammate cloning this repo cold can find `resolve`'s canonical safety rule without reading every file in the project (scored, conceptual).** Where that rule lives, and how prominently, is a real design choice this module tests directly.
4. **The project-scoped slash command does something a real contributor to this specific project would actually reach for**, not a generic placeholder (scored, conceptual).

**Before trusting a green checker as proof you're done:** it is not the same claim as "this configuration is genuinely well-structured." This isn't hypothetical — it's the actual, evidenced finding of this exercise's own dry run (`runs/2026-07-14-module-01-dry-run/grading.md`), which constructed four attempts, not just a naive and a correct one: a plausible content-correct-but-structurally-wrong attempt (failed tier 1 entirely), a typo'd glob that looked complete but scoped to nothing (failed tier 1), and — the case that matters most — a submission that passed every mechanical check while stating almost nothing (`"Write good, clean code"` as its entire tool convention) and omitting the safety rule outright. That fourth attempt only fails because of criteria 2-4, not criterion 1. The checker itself has needed two real bug fixes so far (a shell-portability bug, then a false-positive in its own Python rewrite that matched `SPEC.md`'s own description of a requirement rather than evidence anyone met it) — worth remembering before treating any "PASS" output, including your own, as self-evidently correct.

## Required to advance / stop condition

Produce a Claude Code configuration for `fixtures/resolve/` that passes `scripts/verify_module_01.py` and demonstrates all three scored conceptual criteria (2-4) above, **and** pass the closed-book checkpoint at 80%+. Reading this page does not count: advancement requires a working, checker-verified attempt Coachgremlin has actually reviewed against the rubric, plus a real closed-book attempt — not on having read either.

**Valid alternate terminal:** if your first attempt puts everything in one root `CLAUDE.md` (the naive attempt this module's dry run constructed), that's not a failure, it's the actual exercise. Go back and ask: which of these conventions is true of the *whole* project, and which is only true when someone's editing a specific area? Split accordingly.

## Before the checkpoint: a non-scored self-check

Before opening `checkpoint.md`, predict its likely coverage without looking: which of Domain 3's six task statements do you feel confident on, which do you feel shaky on? Then, separately, before running `scripts/verify_module_01.py` for the first time, predict its output without looking at the script's source. Write both predictions down, then compare. This isn't graded — it's a habit for noticing whether *you* understood the configuration hierarchy, or whether your agent produced something that happens to look right. See [`.claude/skills/agentic-learning-discipline/SKILL.md`](../../.claude/skills/agentic-learning-discipline/SKILL.md) for why this matters more here than it might seem: Claude Code can produce a plausible-looking `.claude/rules/` file in one paste, whether or not the person asking for it understands why the split matters — and the closed-book checkpoint is where that gap stops being hideable.

## Takeaway

A personal CLAUDE.md/rules starter kit, structured the way the exam blueprint expects (hierarchy, path-scoping, frontmatter options) — built from your own configuration decisions on `resolve`, not copied from documentation. (This module's exercise doesn't require producing a `.claude/skills/` skill of your own — that pattern is taught directly in Module 02's takeaway instead; don't expect one from this module specifically.)

---

*Module content authored 2026-07-14, remediated 2026-07-15 after a doubt-driven-development review (fresh-context Claude subagent + Codex CLI, synthesized by a Fable-model replan) found the closed-book tier hadn't been authored, the checker had real portability/scoping bugs, and the conceptual tier's necessity was unvalidated. Dry run: `runs/2026-07-14-module-01-dry-run/grading.md`, now 4 attempts. See `docs/decisions.md`'s 2026-07-15 entries for the full remediation record.*
