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

## 2026-07-17 (cont'd) - Module 08 authored, continuing Foundry with a genuine RAG exercise; two-cycle doubt-driven-development

Module 08 (documentation Q&A RAG system + evaluation harness) authored for the Platform Docs team, a scenario that genuinely needs RAG unlike Module 07's classifier — `doc_qa.py` ships mostly working with one seeded staleness defect, `evaluation.py` ships as a build-from-stub eval harness. Two full doubt-driven-development cycles: cycle 1 (Claude + Codex) found and fixed 8 real gaps (test suite 21→32), most severe a `refresh_index` that could fully rebuild or in-place-mutate and still pass, and an `evaluate` that could bypass real retrieval — all empirically confirmed live. A Codex claim of a checker bypass was tested live and refuted. Cycle 2 (Fable critique of that remediation) found the fix substantially real but not complete — `evaluate` ignoring its own `top_k` parameter while `compare_top_k` reimplemented it independently passed all 32 tests, confirmed live; fixed (32→34 tests), stop condition met. Full detail: repo `docs/session-log.md`, `docs/decisions.md`, and `runs/2026-07-17-module-08-dry-run/grading.md`.

## 2026-07-17 (cont'd) - Module 09 authored, breaking the new-team-per-module pattern; doubt-driven-development's most severe finding to date

Module 09 (Shipping Responsibly: Governance, Stakeholders & Team Enablement) doesn't open on a new internal team's problem — it asks what has to happen before Module 08's own `doc_qa` system ships, given the Platform Docs corpus references genuinely sensitive content. Three deliverables in one gate: a human-in-the-loop governance gate (code), a shipping-readiness review (prose), and real `.claude/` team tooling config (filesystem). Doubt-driven-development found the single most severe issue of any module in this project: every original test placed the sensitive marker in both the query and the retrieved chunk, so a submission checking the query instead of chunk content passed all 14 tests while completely defeating the module's core safety property — confirmed live. Codex then found `review_reason` could leak the actual sensitive content back to the caller, also confirmed live, plus a shared bare-directory-match bug in Module 01's own already-merged checker (found via Module 09 reusing its helpers), fixed in both at once. Both critical gaps fixed (suite 14→17). Stage 3 (Fable-model critique) was unavailable this session (account-level usage-credits error) — skipped on explicit user direction, logged as an open risk (RISK-0005) rather than silently treated as complete. Full detail: repo `docs/session-log.md`, `docs/decisions.md`, and `runs/2026-07-17-module-09-dry-run/grading.md`.

## 2026-07-17 (cont'd) - Module 10 authored, closing Part 2 and the workshop's full content arc; three-cycle doubt-driven-development finds the widest variety of issues of any module to date

Module 10 (Professional Capstone: Sit-Ready for CCAR-P) is the tenth and final module, closing Part 2 and this workshop's whole 10-module arc. Purely written — no new source file — since the exercise is synthesis: a real defense of Foundry's own three-system design against a seeded VP-of-Engineering objection to consolidate into one general-purpose assistant, plus a 42-question, 6-scenario mock exam matching Module 06's real-exam-scale precedent, extended with the multiple-response question format. Self-caught before any review: an all-one-letter answer bug, a domain mislabel, and a self-inflicted answer-shuffle corruption bug (no git history existed to revert to, reconstructed from conversation context). Doubt-driven-development then ran a full three cycles — Claude subagent, Codex, and a Fable critique of the remediation itself — finding checker exploits, a reshuffle that traded one gameable letter-pattern for another (caught by Codex), a fix that would have unfairly failed genuinely honest learner writing (caught by Fable), and a project-wide, pre-existing construct-validity issue where every one of the 42 questions' distractors used absolute-quantifier tells. All findings fixed, including a full rewrite of all 42 questions' distractors chosen over disclosure-only per explicit user direction. Full detail: repo `docs/session-log.md`, `docs/decisions.md`, and `runs/2026-07-17-module-10-dry-run/grading.md`.
---

## Session: Custom domain live, first deploy confirmed end to end; documentation cleanup pass

**Date:** 2026-07-18 20:57

### What Changed

Cut over to custom domain closed-book.coderturtle.io (DNS confirmed via dig, first workflow_dispatch and push-triggered deploys both live and verified via curl), plus a manual documentation cleanup pass (4 stale claims fixed, 3 judgment-shaped findings flagged, no sprawl found)

### Decisions

See docs/decisions.md's 2026-07-17/2026-07-18 entries: custom-domain cutover, documentation cleanup methodology (applied the unbuilt doc-gremlin-team spec by hand)

### Assumptions

None new

### Risks

None new

### Next Actions

- [ ] Spot-check HTTPS cert issuance; review flagged doc gaps (stale maturity_level
- [ ] blank scaffold stubs
- [ ] missing docs/walkthroughs entries)
