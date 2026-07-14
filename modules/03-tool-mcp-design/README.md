# Module 03: Designing Tools and MCP Interfaces

## The question this module answers

How do you design a tool interface Claude will actually pick correctly, and fail safely when it can't?

## Where it sits in the arc

Third module. Hard prerequisite: [Module 02, Prompts and Structured Output](../02-prompts-structured-output/README.md) — tool `input_schema` design reuses the JSON-schema discipline Module 02 builds, even though they're separate API mechanisms (a distinction this module states explicitly, corrected during the 2026-07-14 Review Panel pass — see `docs/decisions.md`). Next: [Module 04, Agentic Loops and Multi-Agent Orchestration](../04-agentic-orchestration/README.md) — the hinge is that an agentic loop is built out of the tools this module designs. See [`modules/README.md`](../README.md).

## Learning objectives (placeholder — finalized when content is authored)

- Write a tool description that clearly disambiguates it from a near-duplicate tool, and diagnose real misrouting caused by minimal descriptions.
- Return structured error responses (`errorCategory`, `isRetryable`) that let an agent make an appropriate recovery decision, not just fail.
- Scope tool access per agent/role to avoid cross-specialization misuse.
- Configure an MCP server correctly at project vs. user scope, with environment-variable credential expansion.

## Exercise material to draw from (not a spec — Coachgremlin authors the real exercise later)

Real material this module's exercise should be built from: CCA-F Exam Guide Domain 2 (Tool Design & MCP Integration), Task Statements 2.1–2.5 — tool interface design, structured error responses, tool distribution/`tool_choice`, MCP server integration (`.mcp.json`, resources), built-in tool selection (Read/Write/Edit/Bash/Grep/Glob). The guide's own Exercise 1 (multi-tool agent with escalation logic) and the "Customer Support Resolution Agent"/"Developer Productivity with Claude" scenarios are real, usable anchors. See [`docs/workshop-design.md`](../../docs/workshop-design.md).

## Required gate (placeholder — shape decided now, real rubric written later)

- **Deterministic tier (hands-on, with Claude Code):** a real MCP tool set (3-4 tools minimum, including two with deliberately similar functionality) with descriptions precise enough to avoid selection confusion, structured error responses, and a scoped `.mcp.json` using environment-variable expansion — no secrets committed. Must satisfy this workshop's stated safe-design default (fail-closed on ambiguous/blocked calls; see `docs/workshop-design.md`).
- **Exam-condition tier (closed-book, without Claude Code):** a timed multiple-choice checkpoint against Domain 2's task statements. Default format: 10–15 questions, 15–20 minutes, 80% to pass.

## Takeaway

A tool-description checklist (boundary conditions, distinguishing near-duplicate tools) plus a scoped `.mcp.json` template with safe credential handling built in. Packaged by Coachgremlin once the rubric is met.

## Stop condition (placeholder)

The learner's tool set is real, demonstrably avoids selection confusion under test, meets the safe-design default, and Coachgremlin confirms the closed-book checkpoint was passed at 80%+ under real exam conditions.

---

> **Skeleton only.** This module has a decided question, arc position, gate shape, and takeaway shape. It has no authored exercise, fixture, or closed-book question bank yet — that's Coachgremlin's job, run later. See [`modules/README.md`](../README.md) for workshop-wide status.
