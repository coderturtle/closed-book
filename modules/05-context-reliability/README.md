# Module 05: Context and Reliability at Scale

## The question this module answers

How do you keep a long-running agent's understanding accurate instead of quietly degrading, and know when to escalate instead of guessing?

## Where it sits in the arc

Fifth module, and the final module of Part 1 before the Foundations capstone. Hard prerequisite: [Module 04, Agentic Loops and Multi-Agent Orchestration](../04-agentic-orchestration/README.md) — this module's hardest task statements (multi-agent error propagation, large-codebase context management under an active agent) need Module 04's agentic system to exist as the thing being managed; the domain's more general concerns (conversation-context preservation) are taught here as one coherent module rather than split across the arc. Next: [Module 06, Foundations Capstone](../06-foundations-capstone/README.md). See [`modules/README.md`](../README.md).

## Learning objectives (placeholder — finalized when content is authored)

- Extract transactional facts into a persistent "case facts" block, rather than letting them decay through progressive summarization.
- Design escalation criteria that don't rely on unreliable proxies (self-reported confidence, sentiment).
- Propagate structured error context between subagents so the coordinator can make an intelligent recovery decision, not just see a generic failure status.
- Preserve claim-source provenance through a multi-agent synthesis pipeline, including conflicting-source annotation.

## Exercise material to draw from (not a spec — Coachgremlin authors the real exercise later)

Real material this module's exercise should be built from: CCA-F Exam Guide Domain 5 (Context Management & Reliability), Task Statements 5.1–5.6 — conversation context preservation, escalation/ambiguity resolution, multi-agent error propagation, large-codebase context management (scratchpad files, `/compact`), human review/confidence calibration, provenance/multi-source synthesis. The guide's own Exercise 4 and the "Customer Support Resolution Agent"/"Multi-Agent Research System" scenarios are real, usable anchors. See [`docs/workshop-design.md`](../../docs/workshop-design.md).

## Required gate (placeholder — shape decided now, real rubric written later)

- **Deterministic tier (hands-on, with Claude Code):** a real diagnosis-and-fix against a deliberately context-degraded multi-agent session — extract the lost facts, restructure the context-passing, and demonstrate the fix holds under a longer follow-up run.
- **Exam-condition tier (closed-book, without Claude Code):** a timed multiple-choice checkpoint against Domain 5's task statements. Default format: 10–15 questions, 15–20 minutes, 80% to pass.

## Takeaway

A context-degradation diagnostic playbook (scratchpad discipline, structured error propagation) — built from a real degraded session diagnosed during the exercise. Packaged by Coachgremlin once the rubric is met.

## Stop condition (placeholder)

The learner's diagnosis correctly identifies the degradation's root cause, the fix is verified to hold, and Coachgremlin confirms the closed-book checkpoint was passed at 80%+ under real exam conditions.

---

> **Skeleton only.** This module has a decided question, arc position, gate shape, and takeaway shape. It has no authored exercise, fixture, or closed-book question bank yet — that's Coachgremlin's job, run later. See [`modules/README.md`](../README.md) for workshop-wide status.
