# Module 02: Prompts and Structured Output That Survive Production

## The question this module answers

How do you get Claude to produce output you can actually trust and parse, every time — not just on the demo run?

## Where it sits in the arc

Second module. Hard prerequisite: [Module 01, Configuring Claude Code](../01-configuring-claude-code/README.md) — this module's exercises are delivered through the configured harness Module 01 built. Next: [Module 03, Designing Tools and MCP Interfaces](../03-tool-mcp-design/README.md) — the hinge is that a tool's `input_schema` reuses the same JSON-schema discipline this module builds for structured output, even though the two are separate mechanisms. See [`modules/README.md`](../README.md) for the full arc.

## Learning objectives (placeholder — finalized when content is authored)

- Replace a vague instruction ("be conservative," "check that comments are accurate") with explicit, checkable criteria.
- Write few-shot examples that demonstrate ambiguous-case handling, not just format.
- Force schema-compliant structured output via `tool_use`, and design nullable/optional fields so the model doesn't fabricate values.
- Decide correctly between the synchronous API and the Message Batches API for a given latency requirement.

## Exercise material to draw from (not a spec — Coachgremlin authors the real exercise later)

Real material this module's exercise should be built from: CCA-F Exam Guide Domain 4 (Prompt Engineering & Structured Output), Task Statements 4.1–4.6 — explicit criteria, few-shot prompting, `tool_use`/JSON schema enforcement, validation-retry loops, batch processing strategy, multi-instance/multi-pass review architectures. The guide's own Exercise 3 ("Build a Structured Data Extraction Pipeline") and Sample Questions under "Scenario: Structured Data Extraction" are real, usable anchors. See [`docs/workshop-design.md`](../../docs/workshop-design.md).

## Required gate (placeholder — shape decided now, real rubric written later)

- **Deterministic tier (hands-on, with Claude Code):** a real structured-extraction tool built with `tool_use` and a JSON schema, tested against documents with missing/ambiguous fields, verified to return `null` rather than fabricate values, plus a validation-retry loop that actually recovers from a semantic error.
- **Exam-condition tier (closed-book, without Claude Code):** a timed multiple-choice checkpoint against Domain 4's task statements. Default format: 10–15 questions, 15–20 minutes, 80% to pass.

## Takeaway

A reusable few-shot/JSON-schema template library for ambiguous-extraction scenarios — built from real extraction failures hit during the exercise. Packaged by Coachgremlin once the rubric is met.

## Stop condition (placeholder)

The learner's extraction tool is real, handles the stated edge cases correctly, and Coachgremlin confirms the closed-book checkpoint was passed at 80%+ under real exam conditions.

---

> **Skeleton only.** This module has a decided question, arc position, gate shape, and takeaway shape. It has no authored exercise, fixture, or closed-book question bank yet — that's Coachgremlin's job, run later. See [`modules/README.md`](../README.md) for workshop-wide status.
