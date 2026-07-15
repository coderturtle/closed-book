# Module 03: Designing Tools and MCP Interfaces

## The question this module answers

How do you design a tool interface Claude will actually pick correctly, and fail safely when it can't?

## Where it sits in the arc

Third module. Hard prerequisite: [Module 02, Prompts and Structured Output](../02-prompts-structured-output/README.md) — this module's checker chains Module 02's (which chains Module 01's), per the cumulative-gate convention. Next: [Module 04, Agentic Loops and Multi-Agent Orchestration](../04-agentic-orchestration/README.md) — the hinge is that an agentic loop is built out of the tools this module designs.

## Exercise: the four `resolve` tools

Runs against `fixtures/resolve/`, continuing the shared project. Implement all four MCP tool functions in `fixtures/resolve/src/tools/`: `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human` — each currently `raise NotImplementedError`, each already has a real docstring stating its accepted inputs and boundaries (your job is the *behavior*, not rewriting the description, though you may improve it).

Each tool takes an injected `backend: Backend` (see `fixtures/resolve/src/backend.py`) so the provided test suite can supply fake customer/order records without a real database — the same injection pattern Module 02 used for `model_client`.

A real, provided test suite (`fixtures/resolve/tests/test_tools.py`, 16 tests) checks, among other things: `get_customer`/`lookup_order` return structured "not found" results rather than exceptions, and never confirm that an order belongs to a different customer even indirectly; **`process_refund` independently re-verifies `customer_id` against the backend before doing anything else** — this is the module's safety-critical property, distinct from Module 04's later session-level hook (see `process_refund`'s own docstring for why both layers exist); `escalate_to_human` rejects a summary missing `root_cause` or `recommended_action`; and all four tools share one consistent error shape (`src/tool_errors.py`).

Get `python3 scripts/verify_module_03.py <path-to-your-attempt>` (run from the repo root) to pass, then check it against the rubric below.

## The two-tier gate

**Tier 1 — deterministic, hands-on with Claude Code.** `scripts/verify_module_03.py`: chains Module 02's check (which chains Module 01's), then runs the real pytest suite against your four tools.

**Tier 2 — exam-condition, closed-book without Claude Code.** [`checkpoint.md`](checkpoint.md): 12 originally-written questions covering the full CCA-F Domain 2 blueprint (2.1–2.5), including tool distribution across agents, MCP server configuration, and built-in tool selection — none of which have a `resolve`-specific artifact yet (Module 04 is where multiple agents and a real MCP server first exist). Close your Claude Code session before starting it. 80% (10/12) to pass.

Both tiers are required to advance.

## Rubric (deterministic tier's rubric; the closed-book checkpoint is scored separately)

1. **`python3 scripts/verify_module_03.py` exits 0 (gate, deterministic).** The chained cumulative gate passes, and all 16 provided tests pass.
2. **Each tool's docstring states its accepted input format(s) and at least one explicit boundary against a similarly-shaped tool (deterministic: the test suite checks specific required keywords are present).** This moved from conceptual to deterministic in this module's own design — a lesson carried forward from Modules 01-02's own doubt-driven-development reviews, applied proactively this time rather than found afterward.
3. **A docstring that merely contains the required keywords isn't the same claim as one that actually helps an agent choose correctly (scored, conceptual).** This exercise's own dry run constructed an attempt where every docstring passes criterion 2's keyword check while giving no real boundary reasoning ("Gets a customer. Takes an identifier which could be an email, phone, or account thing.") — only this criterion catches that gap.
4. **`process_refund`'s defense-in-depth re-verification is documented as a deliberate choice distinct from Module 04's later hook enforcement, not just something that happens to be checked (scored, conceptual).** Property, not technique: the *reasoning* (why two layers, not one) should be visible, not just the check's presence.

**Before trusting a green checker as proof you're done:** this exercise's own dry run (`runs/2026-07-15-module-03-dry-run/grading.md`) found a real bug in its own first draft, not just in a constructed naive attempt — every tool's description was originally written as a *module*-level docstring, which isn't the same object as the *function's* own `__doc__` that real MCP tooling actually reads. A file that looks like it documents its tool can still hand an agent nothing. The dry run also constructed a plausible safety mistake (`process_refund` trusting a caller-supplied `customer_id` without its own re-check, reasoning "the hook already covers this") that fails exactly one test, and a weak-docstring attempt that passes all 16 deterministic tests while giving an agent nothing real to act on — read that file before assuming your own green run means what you think it means.

## Required to advance / stop condition

Produce implementations of all four tools that pass `scripts/verify_module_03.py` and demonstrate the two scored conceptual criteria (3-4), **and** pass the closed-book checkpoint at 80%+. Reading this page does not count.

## Before the checkpoint: a non-scored self-check

Before opening `checkpoint.md`, predict which of Domain 2's five task statements you feel shaky on. Before running `scripts/verify_module_03.py`, predict which of the 16 tests will fail and why — specifically, could you explain *why* `process_refund` needs its own re-verification even though Module 04 will add a hook that's supposed to prevent it from being called wrongly in the first place? If you can't answer that without looking, that's the actual concept this module is testing. See [`.claude/skills/agentic-learning-discipline/SKILL.md`](../../.claude/skills/agentic-learning-discipline/SKILL.md).

## Takeaway

A tool-description checklist (boundary conditions, distinguishing near-duplicate tools) plus a scoped `.mcp.json` template with safe credential handling built in — built from your own four tool implementations, not copied from documentation.

---

*Module content authored 2026-07-15, both tiers built together from the start, applying the docstring-quality and rubric-criterion-split lessons from Modules 01-02's doubt-driven-development reviews proactively rather than waiting for a review to find them. Dry run: `runs/2026-07-15-module-03-dry-run/grading.md`.*
