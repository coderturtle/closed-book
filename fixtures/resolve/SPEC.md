# Spec: `resolve`

This is the authoritative spec for `resolve`, the one project every module in Part 1 of Closed Book's arc (Modules 01-06, Architect Foundations) builds a real capability onto. Keep this file as the single source of truth; don't restate the product pitch differently inside a module README.

**Why one shared project, not independent per-module fixtures:** CCA-F's own exam guide describes almost exactly this system as "Scenario 1: Customer Support Resolution Agent" in its own primary source — a customer-support agent with `get_customer`, `lookup_order`, `process_refund`, and `escalate_to_human` as its MCP tools, targeting 80%+ first-contact resolution while knowing when to escalate. Building the real thing the exam's own scenario describes, incrementally, module by module, teaches directly toward how CCA-F actually tests this material — closer to the exam's own framing than an invented, unrelated toy would be.

## The product

`resolve` is a customer support resolution agent: it handles high-ambiguity requests (returns, billing disputes, account issues) through Claude, backed by real tools against backend systems, with a target of high first-contact resolution and a hard rule about when to escalate to a human instead of guessing.

## Feature build-out (one module, one capability, in order)

| # | Module | Capability | Status |
|---|---|---|---|
| 01 | Configuring Claude Code for Real Work | Full Claude Code configuration for this project: CLAUDE.md hierarchy, path-scoped rules, a project slash command, CI-mode readiness | **Exercise authored + dry-run complete** (`runs/2026-07-14-module-01-dry-run/`). |
| 02 | Prompts and Structured Output That Survive Production | Structured extraction for refund amounts/escalation reasons from freeform customer messages | Not started |
| 03 | Designing Tools and MCP Interfaces | Real implementations of `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human` as MCP tools with structured error responses | Not started |
| 04 | Agentic Loops and Multi-Agent Orchestration | The coordinator agent (`src/agent.py`): the real agentic loop calling the Module 03 tools, with a programmatic hook enforcing verify-before-refund | Not started |
| 05 | Context and Reliability at Scale | Context handling across a long, multi-issue support session (case-facts extraction, escalation handoff summaries) | Not started |
| 06 | Foundations Capstone | A real, seeded bug spanning 3+ of the above capabilities, diagnosed and fixed | Not started |

## Module 01: Claude Code configuration

### What's already here

`fixtures/resolve/` ships with a minimal but real project skeleton the learner configures Claude Code around — not empty, since "configure Claude Code for an existing, growing codebase" is the actual exam-tested skill (Task Statement 3.1's own example: a new team member not receiving instructions because they're in the wrong config scope presumes a codebase that already exists):

- `src/tools/` — four stub MCP tool files (`get_customer.py`, `lookup_order.py`, `process_refund.py`, `escalate_to_human.py`), each `raise NotImplementedError` (real bodies land in Module 03).
- `src/agent.py` — the coordinator agent stub (real body lands in Module 04).
- `tests/test_tools.py` — placeholder test collection target for `src/tools/`.

### The exercise (see `modules/01-configuring-claude-code/README.md` for the full rubric)

Configure Claude Code for this project for real production team use, not a toy demo:

1. A project-root `CLAUDE.md` with real project context (what this project is, its safety-critical rule: never call `process_refund` before a verified `get_customer` result).
2. At least one `.claude/rules/` file, YAML-frontmatter path-scoped, applying conventions to `src/tools/**` specifically (tool-description/error-shape discipline) — distinct from whatever applies to `tests/**`.
3. At least one project-scoped slash command in `.claude/commands/`.
4. Evidence the configuration is CI-ready: a documented `claude -p` invocation pattern for this project (non-interactive mode).

### The actual point of this exercise

See `runs/2026-07-14-module-01-dry-run/` for the real dry run and its finding, and `modules/01-configuring-claude-code/README.md` for the full rubric.

## Running it

```bash
cd fixtures/resolve
scripts/verify-module-01.sh   # from repo root; see that script for what it checks
```
