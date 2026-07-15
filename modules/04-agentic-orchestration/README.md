# Module 04: Agentic Loops and Multi-Agent Orchestration

## The question this module answers

When should one agent do the whole job, and when does the job need to be split across several — and how do you actually wire that split together?

## Where it sits in the arc

Fourth module, and the largest single domain in CCA-F by weight (27%). Hard prerequisite: [Module 01](../01-configuring-claude-code/README.md) + [Module 02](../02-prompts-structured-output/README.md) + [Module 03](../03-tool-mcp-design/README.md) — an agentic loop is built on configured Claude Code (01), reasons over structured prompts (02), and calls the tools Module 03 designs (03). This is the module every prior one was building toward. Next: [Module 05, Context and Reliability at Scale](../05-context-reliability/README.md) — the hinge is that context management has nothing real to manage until this module's agent exists to manage it for. See [`modules/README.md`](../README.md).

## Learning objectives (placeholder — finalized when content is authored)

- Implement an agentic loop's control flow correctly against `stop_reason`, without falling into an anti-pattern (arbitrary iteration caps, parsing assistant text as a completion signal).
- Design a coordinator-subagent system with correct context passing — subagents don't automatically inherit parent context.
- Choose between programmatic enforcement (hooks) and prompt-based guidance for a workflow ordering requirement, and defend the choice.
- Use session resumption/`fork_session` correctly, and know when starting fresh with an injected summary beats resuming stale context.

## Exercise material to draw from (not a spec — Coachgremlin authors the real exercise later)

Real material this module's exercise should be built from: CCA-F Exam Guide Domain 1 (Agentic Architecture & Orchestration), Task Statements 1.1–1.7 — agentic loop lifecycle, coordinator-subagent patterns, subagent invocation/context passing (the `Task` tool, `AgentDefinition`), multi-step workflows with enforcement/handoff, Agent SDK hooks (`PostToolUse`, tool-call interception), task decomposition strategies, session state/resumption/forking. The guide's own Exercise 1 and Exercise 4, and the "Customer Support Resolution Agent"/"Multi-Agent Research System" scenarios, are real, usable anchors. See [`docs/workshop-design.md`](../../docs/workshop-design.md).

## Required gate (placeholder — shape decided now, real rubric written later)

- **Deterministic tier (hands-on, with Claude Code):** a real coordinator-subagent system (2+ subagents minimum) with correct `stop_reason` handling, at least one Agent SDK hook enforcing a real business rule, and structured error propagation from a subagent back to the coordinator. Must meet this workshop's safe-design default (destructive actions require human approval).
- **Exam-condition tier (closed-book, without Claude Code):** a timed multiple-choice checkpoint against Domain 1's task statements — the largest domain, so this checkpoint may reasonably run toward the upper end of the workshop's default range. Default format: 10–15 questions, 15–20 minutes, 80% to pass (see `docs/workshop-design.md` for the workshop-wide default; a module may state a higher count here if Domain 1's real breadth warrants it once content is authored).

## Takeaway

A coordinator-subagent reference implementation (hooks, `Task` tool patterns, session resumption) — a real, reusable scaffold built from the exercise, not a toy. Packaged by Coachgremlin once the rubric is met.

## Stop condition (placeholder)

The learner's coordinator-subagent system is real, demonstrably handles the stated failure/handoff scenarios, and Coachgremlin confirms the closed-book checkpoint was passed at 80%+ under real exam conditions.

---

> **Skeleton only.** This module has a decided question, arc position, gate shape, and takeaway shape. It has no authored exercise, fixture, or closed-book question bank yet — that's Coachgremlin's job, run later. See [`modules/README.md`](../README.md) for workshop-wide status.
