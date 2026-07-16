# Session Log: Closed Book

## 2026-07-14 - Initial scaffold

Project scaffolded as **factory-output**. Learn Anthropic's Claude Certified Architect material (Foundations to Professional) the agent-native way: hands-on Claude Code exercises gated by closed-book practice checkpoints against the published exam blueprint.

## 2026-07-14 - Workshop Gremlin pipeline complete

Naming pass (**Closed Book**), design docs, Review Panel, module skeleton, build-log/Pages site — all roster steps done. PR #1 merged 2026-07-15.

## 2026-07-15 - Coachgremlin: Module 01 authored for real

First content pass. Decided a shared project (`resolve`, a customer support resolution agent) across Modules 01-06. Module 01 has a real exercise, rubric, deterministic checker, and a completed dry run. See repo `docs/session-log.md` for full detail.

## 2026-07-16 - Coachgremlin: Modules 02-05 authored for real, each with doubt-driven-development

Modules 02 (structured extraction), 03 (four MCP tools), 04 (agentic loop + hook), and 05 (case facts + escalation decision) each authored with both tiers built together, a real deterministic checker chaining every prior module's (`verify_module_02.py` through `verify_module_05.py`), a real closed-book checkpoint, and a completed multi-attempt dry run. Modules 02-04 each went through a full doubt-driven-development review (fresh Claude subagent + Codex, Module 04 also a Fable-model critique of the remediation) that found and fixed real issues — most notably Module 04's hook originally didn't bind to *which* customer was verified. Module 05 built and dry-run validated but not yet doubt-driven-development reviewed. Full detail: repo `docs/session-log.md` and `docs/decisions.md`.
