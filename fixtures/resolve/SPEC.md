# Spec: `resolve`

This is the authoritative spec for `resolve`, the one project every module in Part 1 of Closed Book's arc (Modules 01-06, Architect Foundations) builds a real capability onto. Keep this file as the single source of truth; don't restate the product pitch differently inside a module README.

**Why one shared project, not independent per-module fixtures:** CCA-F's own exam guide describes almost exactly this system as "Scenario 1: Customer Support Resolution Agent" in its own primary source — a customer-support agent with `get_customer`, `lookup_order`, `process_refund`, and `escalate_to_human` as its MCP tools, targeting 80%+ first-contact resolution while knowing when to escalate. Building the real thing the exam's own scenario describes, incrementally, module by module, is this workshop's bet on how to teach toward how CCA-F actually tests this material — a stated hypothesis, not yet an evidenced outcome (see `docs/design-tension.md`'s honesty discipline on unproven claims).

## The product

`resolve` is a customer support resolution agent: it handles high-ambiguity requests (returns, billing disputes, account issues) through Claude, backed by real tools against backend systems, with a target of high first-contact resolution.

**The one canonical safety rule, stated once:** escalate to a human rather than guess, whenever policy is ambiguous, the customer explicitly asks for a human, or the agent can't make meaningful progress — this is the real exam scenario's own stated framing. Every module's specific enforcement of this is an *instance* of this one rule, not a competing rule of its own: Module 04's "never call `process_refund` before a verified `get_customer` result" is the concrete, mechanical form this rule takes once the coordinator agent exists to enforce it. Earlier modules (01-03) refer back to this canonical statement rather than each stating their own version of "the one safety rule."

## Compatibility contract (added 2026-07-15, after a doubt-driven-development review found the shared-project decision was unenforced prose)

Each module's checker is the *only* thing a later module may assume from an arbitrary passing submission — not the intent behind the exercise, not what a "typical" solution looks like. Concretely: Module 03 may assume a passing Module 01 submission has a `.claude/rules/` file scoped to `src/tools/**` and one scoped to `tests/**` (both are checker-verified), but may **not** assume anything about what those files actually say — content quality is the conceptual tier's job, not the checker's.

**Cumulative gate convention:** starting with Module 02, each module's checker chains every prior module's checker before running its own checks (e.g. `verify_module_02.py` imports and calls `check_module_01` first). This is how a later module modifying the shared project gets caught if it silently breaks an earlier, already-passed gate — the regression risk Coachgremlin's own Workflow step 0 (ARB trigger check) exists for in a shared-throughline-project workshop, made concrete here as an automated check rather than a manual review trigger alone.

**Interface convention (stated explicitly 2026-07-15, after a doubt-driven-development review of Module 03 found the first two links in the chain already disagreed on shape):** every `check_module_NN(target: Path) -> CheckResult` returns the *same* dataclass — `passed: bool`, `findings: list[str]` (short summary lines), `output: str` (raw subprocess/pytest text, if any). A module's own `main()` must call its `check_module_NN` rather than re-deriving the same logic independently — two code paths computing the same thing can silently diverge. **Canonical-test execution:** any checker that runs a provided pytest suite must run the repo's own canonical copy of that test file (copied to a temp location, executed with `cwd` set to the submission), never the copy sitting inside the submission itself — a submission's own copy of a test file is not trustworthy input, since nothing stops a learner from editing or deleting it. Found the same day as a real gap in both `verify_module_02.py` and the first version of `verify_module_03.py`.

## Feature build-out (one module, one capability, in order)

| # | Module | Capability | Status |
|---|---|---|---|
| 01 | Configuring Claude Code for Real Work | Full Claude Code configuration for this project: CLAUDE.md hierarchy, path-scoped rules, a project slash command, CI-mode readiness | **Deterministic tier authored and dry-run validated** (`runs/2026-07-14-module-01-dry-run/`, 4 constructed attempts); **closed-book checkpoint authored** (`modules/01-configuring-claude-code/checkpoint.md`). Conceptual-tier grading against a real learner attempt is not yet evidenced. |
| 02 | Prompts and Structured Output That Survive Production | Structured extraction for refund amounts/escalation reasons from freeform customer messages | **Deterministic tier authored, doubt-driven-development reviewed, and dry-run validated** (`runs/2026-07-15-module-02-dry-run/`, 4 constructed attempts); **closed-book checkpoint authored** (`modules/02-prompts-structured-output/checkpoint.md`). Conceptual-tier grading against a real learner attempt is not yet evidenced. |
| 03 | Designing Tools and MCP Interfaces | Real implementations of `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human` as MCP tools with structured error responses | **Deterministic tier authored, doubt-driven-development reviewed, and dry-run validated** (`runs/2026-07-15-module-03-dry-run/`, 3 constructed attempts, 20 tests); **closed-book checkpoint authored** (`modules/03-tool-mcp-design/checkpoint.md`). Conceptual-tier grading against a real learner attempt is not yet evidenced. |
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

1. A project-root `CLAUDE.md` with real project context (what this project is, and the canonical safety rule stated above: escalate rather than guess — concretely, in this project's current state, never call `process_refund` before a verified `get_customer` result).
2. At least one `.claude/rules/` file, YAML-frontmatter path-scoped, applying conventions to `src/tools/**` specifically (tool-description/error-shape discipline) — distinct from whatever applies to `tests/**`.
3. At least one project-scoped slash command in `.claude/commands/`.
4. Evidence the configuration is CI-ready: a documented `claude -p` invocation pattern for this project (non-interactive mode).

### The actual point of this exercise

See `runs/2026-07-14-module-01-dry-run/` for the real dry run and its finding, and `modules/01-configuring-claude-code/README.md` for the full rubric.

## Module 02: structured extraction

### What's already here

- `src/extraction.py` — `extract_refund_request`, `build_extraction_prompt`, both stubbed `raise NotImplementedError`; `FEW_SHOT_EXAMPLES` stubbed empty. The schema types (`ExtractionResult`, `REASON_CATEGORIES`, `ExtractionFailed`) and the `ModelClient` injection point are already declared. **Requires Python 3.9+.**
- `tests/test_extraction.py` — a real, provided pytest suite (14 tests), not a placeholder. This is the deterministic gate for this module, the same role `tests/test_tools.py`'s real content plays once Module 03 lands.

### The exercise (see `modules/02-prompts-structured-output/README.md` for the full rubric)

Implement `build_extraction_prompt` (states the schema explicitly, embeds `FEW_SHOT_EXAMPLES`, embeds the specific prior validation error on retry), `FEW_SHOT_EXAMPLES` (at least 2 examples, at least one genuinely ambiguous), and `extract_refund_request` (validates the model's raw response against the schema, retries with the specific validation error fed back, raises `ExtractionFailed` rather than fabricate a result after exhausting retries). `max_retries` defaults to 2.

### The actual point of this exercise

See `runs/2026-07-15-module-02-dry-run/` for the real dry run and its findings (a subtle `or 0` bug that fabricates a refund amount, caught by exactly one test; a structural gap where the original exercise interface never required a prompt/few-shot artifact at all, found and fixed by a doubt-driven-development review the same day), and `modules/02-prompts-structured-output/README.md` for the full rubric.

## Module 03: the four MCP tools

### What's already here

- `src/backend.py` — the `Backend` protocol (`find_customer`, `find_order`) every tool is injected with, mirroring Module 02's `model_client` injection.
- `src/tool_errors.py` — `tool_error()`, the one shared structured-error shape all four tools use.
- `src/tools/*.py` — all four tools, each `raise NotImplementedError`, each with a real function-level docstring (not a module-level one — a real bug found and fixed during this module's own dry run, see `runs/2026-07-15-module-03-dry-run/grading.md`) stating its accepted inputs and boundaries.
- `tests/test_tools.py` — a real, provided pytest suite (16 tests), not a placeholder.

### The exercise (see `modules/03-tool-mcp-design/README.md` for the full rubric)

Implement all four tools' bodies. `process_refund` is the safety-critical one: it must independently re-verify `customer_id` against the backend before doing anything else (defense in depth, distinct from Module 04's later session-level hook enforcement).

### The actual point of this exercise

See `runs/2026-07-15-module-03-dry-run/` for the real dry run and its findings, and `modules/03-tool-mcp-design/README.md` for the full rubric.

## Running it

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # first time only
python3 scripts/verify_module_01.py fixtures/resolve   # from repo root
python3 scripts/verify_module_02.py fixtures/resolve   # chains Module 01's check, then runs tests/test_extraction.py
python3 scripts/verify_module_03.py fixtures/resolve   # chains Module 02's check, then runs tests/test_tools.py
```
