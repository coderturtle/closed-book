# Session Log: Closed Book

## 2026-07-14 - Initial scaffold

Project scaffolded as **factory-output**. Learn Anthropic's Claude Certified Architect material (Foundations to Professional) the agent-native way: hands-on Claude Code exercises gated by closed-book practice checkpoints against the published exam blueprint.

## 2026-07-14 - Workshop Gremlin pipeline complete

Naming pass (**Closed Book**), design docs, Review Panel, module skeleton, build-log/Pages site — all roster steps done. PR #1 merged 2026-07-15.

## 2026-07-15 - Coachgremlin: Module 01 authored for real

First content pass. Decided a shared project (`resolve`, a customer support resolution agent) across Modules 01-06. Module 01 has a real exercise, rubric, deterministic checker, and a completed dry run. See repo `docs/session-log.md` for full detail.

## 2026-07-16 - Coachgremlin: Modules 02-05 authored for real, each with doubt-driven-development

Modules 02 (structured extraction), 03 (four MCP tools), 04 (agentic loop + hook), and 05 (case facts + escalation decision) each authored with both tiers built together, a real deterministic checker chaining every prior module's (`verify_module_02.py` through `verify_module_05.py`), a real closed-book checkpoint, and a completed multi-attempt dry run. Modules 02-04 each went through a full doubt-driven-development review (fresh Claude subagent + Codex, Module 04 also a Fable-model critique of the remediation) that found and fixed real issues — most notably Module 04's hook originally didn't bind to *which* customer was verified. Module 05 built and dry-run validated but not yet doubt-driven-development reviewed. Full detail: repo `docs/session-log.md` and `docs/decisions.md`.

## 2026-07-16 (cont'd) - Modules 05-06 doubt-driven-development, Module 06 authored, closing Part 1

Module 05's review (Claude + Codex + Fable) found the test suite tested one mapped field far more rigorously than two structurally identical ones — fixed with symmetric coverage across two remediation rounds (20→28→30 tests). Module 06 (Foundations Capstone) authored with a different exercise shape — diagnose-and-fix on a fully-written `session.py` with 2 seeded defects — closing Part 1 (Architect Foundations) in full. Its own doubt-driven-development found every one of 42 checkpoint answers was "A" and that the reference implementation itself never escalated on repeated hook rejections; both fixed, plus a Fable-critique round closing 3 further gaps. Full detail: repo `docs/session-log.md` and `docs/decisions.md`.

## 2026-07-17 - Module 07 authored, opening Part 2; doubt-driven-development finds and fixes a project-wide checker bypass

Part 2 (Architect Professional) opened on a new shared project, **Foundry** (an internal AI platform team's own product, chosen via `AskUserQuestion` over continuing `resolve`), since a single customer-support agent has no natural home for CCAR-P Domain 7. Module 07 (ticket-triage classifier + ADR) authored, both tiers together. Its doubt-driven-development review (Claude subagent + Codex + Fable critique of the remediation) found a project-wide issue, not a Module-07-scoped one: all six deterministic checkers (Modules 02-07) trusted pytest's exit code alone, letting a submission bypass the entire test suite via a shadow `pytest.py` module or `os._exit(0)` at import time while still reporting a clean pass — both confirmed live against Module 04's checker with a real known-broken implementation, both closed the same day across all six checkers. Also closed 8 narrower precision gaps in Module 07's own test suite (12→20 tests). Full detail: repo `docs/session-log.md`, `docs/decisions.md`, and `runs/2026-07-17-module-07-dry-run/grading.md`.
