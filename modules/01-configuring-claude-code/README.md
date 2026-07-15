# Module 01: Configuring Claude Code for Real Work

## The question this module answers

How do you configure Claude Code so it works the way your team needs, not the way it ships by default?

## Where it sits in the arc

First module. No prior module: this is day-one harness fluency, assumed by every later module rather than taught by any of them again. Next: [Module 02, Prompts and Structured Output That Survive Production](../02-prompts-structured-output/README.md) — the hinge is that Module 02's exercises are *delivered through* the Claude Code configuration this module builds. See [`modules/README.md`](../README.md) for the full arc and why this order.

## Learning objectives (placeholder — finalized when content is authored)

- Diagnose a configuration-hierarchy bug (e.g. a teammate not receiving project instructions because they landed in user-level, not project-level, config).
- Choose correctly between a `.claude/rules/` path-scoped file and a subdirectory `CLAUDE.md` for a given convention.
- Decide when a task needs plan mode versus direct execution, and defend the call.
- Wire Claude Code into a non-interactive CI context without it hanging on interactive input.

## Exercise material to draw from (not a spec — Coachgremlin authors the real exercise later)

Real material this module's exercise should be built from: CCA-F Exam Guide Domain 3 (Claude Code Configuration & Workflows), Task Statements 3.1–3.6 — CLAUDE.md hierarchy/`@import`/`.claude/rules/`, custom slash commands and skills (`context: fork`, `allowed-tools`, `argument-hint`), path-specific rules, plan mode vs. direct execution, iterative refinement techniques, and CI/CD integration (`-p`/`--print`, `--output-format json`). The guide's own Exercise 2 ("Configure Claude Code for a Team Development Workflow") is a real, usable starting shape — see [`docs/workshop-design.md`](../../docs/workshop-design.md)'s curriculum-anchor section for the full research this arc is grounded in.

## Required gate (placeholder — shape decided now, real rubric written later)

- **Deterministic tier (hands-on, with Claude Code):** a real, working configuration artifact — a multi-level CLAUDE.md hierarchy, at least one `.claude/rules/` file with correct glob scoping, and one project-scoped skill or slash command — built for a real (not toy) project, verified to actually load and apply as intended.
- **Exam-condition tier (closed-book, without Claude Code):** a timed multiple-choice checkpoint against Domain 3's task statements, written originally in the exam's own scenario-based style. Default format: 10–15 questions, 15–20 minutes, 80% to pass (see [`docs/workshop-design.md`](../../docs/workshop-design.md) for the workshop-wide default and the suggested closed-book ritual).

## Takeaway

A personal CLAUDE.md/rules/skills starter kit, structured the way the exam blueprint expects (hierarchy, path-scoping, frontmatter options) — built from real configuration decisions made during the exercise, not copied from documentation. Packaged by Coachgremlin once the rubric is met.

## Stop condition (placeholder)

The learner's configuration artifact is real, verified to load correctly, and Coachgremlin confirms the closed-book checkpoint was passed at 80%+ under real exam conditions (no Claude, no notes). Reading this page does not count: advancement requires both tiers actually observed, not just attempted.

---

> **Skeleton only.** This module has a decided question, arc position, gate shape, and takeaway shape. It has no authored exercise, fixture, or closed-book question bank yet — that's Coachgremlin's job, run later, per the Workshop Gremlin's Completion Condition (it stops before content exists). See [`modules/README.md`](../README.md) for workshop-wide status.
