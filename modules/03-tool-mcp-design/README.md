# Module 03: Designing Tools and MCP Interfaces

## The question this module answers

How do you design a tool interface Claude will actually pick correctly, and fail safely when it can't?

## Where it sits in the arc

Third module. Hard prerequisite: [Module 02, Prompts and Structured Output](../02-prompts-structured-output/README.md) — this module's checker chains Module 02's (which chains Module 01's), per the cumulative-gate convention. Next: [Module 04, Agentic Loops and Multi-Agent Orchestration](../04-agentic-orchestration/README.md) — the hinge is that an agentic loop is built out of the tools this module designs.

## Exercise: the four `resolve` tools

Runs against `fixtures/resolve/`, continuing the shared project. Implement all four MCP tool functions in `fixtures/resolve/src/tools/`: `get_customer`, `lookup_order`, `process_refund`, `escalate_to_human` — each currently `raise NotImplementedError`, each already has a real docstring stating its accepted inputs and boundaries (your job is the *behavior*, not rewriting the description, though you may improve it).

Each tool takes an injected `backend: Backend` (see `fixtures/resolve/src/backend.py`) so the provided test suite can supply fake customer/order records without a real database — the same injection pattern Module 02 used for `model_client`. **Scope, stated explicitly:** this backend is read-only (lookups only), and stays that way for the rest of this project. You're verifying a refund *decision* here — is the customer real, does the order belong to them, is the amount within what's refundable — not executing one. Persistence, decrementing `refundable_cents`, and idempotency against a double-submitted request are real production concerns this project deliberately does not implement — Module 04's own exercise is orchestration (the agentic loop and its session-level hook), not refund execution. See `docs/decisions.md`'s 2026-07-15 Module 04 entries for the scope call.

A real, provided test suite (`fixtures/resolve/tests/test_tools.py`, 20 tests) checks, among other things: `get_customer`/`lookup_order` return structured "not found" results rather than exceptions, and an order that exists but belongs to a different customer produces a result *indistinguishable* from a genuinely nonexistent one (checked by equality, not just a string-absence heuristic); **`process_refund` independently re-verifies `customer_id` against the backend *before doing anything else*** — checked not just by the final result but by call order: `find_order` must never be called before `find_customer` succeeds — this is the module's safety-critical property, distinct from Module 04's later session-level hook (see `process_refund`'s own docstring for why both layers exist); `escalate_to_human` rejects a summary missing `root_cause` or `recommended_action`, but deliberately does **not** require backend verification of `customer_id` — escalation is this project's fail-open safe path; and all four tools share one consistent error shape (`src/tool_errors.py`), whose category semantics (transient/validation/business/permission) are documented there, not left for you to reverse-engineer from a hidden test.

Get `python3 scripts/verify_module_03.py <path-to-your-attempt>` (run from the repo root) to pass, then check it against the rubric below.

## The two-tier gate

**Tier 1 — deterministic, hands-on with Claude Code.** `scripts/verify_module_03.py`: chains Module 02's check (which chains Module 01's) via a real importable `check_module_02`/`check_module_03` function, then runs the *repo's own canonical copy* of the test suite against your four tools — not whatever copy sits in your own submission, so editing your local `tests/test_tools.py` doesn't change what you're actually graded against.

**Tier 2 — exam-condition, closed-book without Claude Code.** [`checkpoint.md`](checkpoint.md): 12 originally-written questions covering the full CCA-F Domain 2 blueprint (2.1–2.5), including tool distribution across agents, MCP server configuration, and built-in tool selection — none of which have a `resolve`-specific artifact yet (Module 04 is where multiple agents and a real MCP server first exist). Close your Claude Code session before starting it. 80% (10/12) to pass.

Both tiers are required to advance.

## Rubric (deterministic tier's rubric; the closed-book checkpoint is scored separately)

1. **`python3 scripts/verify_module_03.py` exits 0 (gate, deterministic).** The chained cumulative gate passes, and all 20 provided tests pass.
2. **Each of the four tools' docstrings states its accepted input format(s) and at least one explicit boundary or reasoning point (deterministic: the test suite checks specific required keywords are present, for all four tools, not just the two with near-identical signatures).** This moved from conceptual to deterministic in this module's own design — a lesson carried forward from Modules 01-02's own doubt-driven-development reviews. **Caught by this module's own review, not applied fully the first time:** the first version only checked `get_customer` and `lookup_order`; `process_refund`'s docstring (which documents the module's own flagship safety property) had no test at all until a second review pass added one.
3. **A docstring that merely contains the required keywords isn't the same claim as one that actually helps an agent choose correctly (scored, conceptual).** This exercise's own dry run constructed an attempt where every docstring passes criterion 2's keyword check while giving no real boundary reasoning ("Gets a customer. Takes an identifier which could be an email, phone, or account thing.") — only this criterion catches that gap.
4. **`process_refund`'s defense-in-depth re-verification is documented as a deliberate choice distinct from Module 04's later hook enforcement, not just something that happens to be checked (scored, conceptual, though the ordering claim itself is now deterministically tested — see below).** Property, not technique: the *reasoning* (why two layers, not one) should be visible, not just the check's presence.

**Before trusting a green checker as proof you're done:** this module went through two rounds of scrutiny before shipping, both real. First, its own dry run (`runs/2026-07-15-module-03-dry-run/grading.md`) found a bug in its own first draft — every tool's description was originally a *module*-level docstring, not the *function's* own `__doc__` that real MCP tooling actually reads; `get_customer.__doc__` came back empty against the first version. Second, a doubt-driven-development review (a fresh Claude subagent + Codex, synthesized by a Fable-model replan) found the cumulative-gate chain was already broken going into this module (two different, incompatible return shapes) and, more seriously, that the checker trusted a learner-editable test file — a submission could weaken its own gate by editing `tests/test_tools.py` directly. Both fixed; see `docs/decisions.md`'s 2026-07-15 entries for the full record. Read the dry-run file before assuming your own green run means what you think it means — it also covers a plausible safety mistake (`process_refund` trusting a caller-supplied `customer_id` without its own re-check) and a weak-docstring attempt that passes every deterministic test while giving an agent nothing real to act on.

## Required to advance / stop condition

Produce implementations of all four tools that pass `scripts/verify_module_03.py` and demonstrate the two scored conceptual criteria (3-4), **and** pass the closed-book checkpoint at 80%+. Reading this page does not count.

## Before the checkpoint: a non-scored self-check

Before opening `checkpoint.md`, predict which of Domain 2's five task statements you feel shaky on. Before running `scripts/verify_module_03.py`, predict which tests will fail and why — specifically, could you explain *why* `process_refund` needs its own re-verification even though Module 04 will add a hook that's supposed to prevent it from being called wrongly in the first place, and why `escalate_to_human` deliberately does *not* need the same check? If you can't answer both without looking, that's the actual concept this module is testing. See [`.claude/skills/agentic-learning-discipline/SKILL.md`](../../.claude/skills/agentic-learning-discipline/SKILL.md).

## Takeaway

A tool-description checklist (boundary conditions, distinguishing near-duplicate tools), built from your own four tool implementations, not copied from documentation. **Not produced by the graded exercise itself, and not claimed as one:** a scoped `.mcp.json` template with safe credential handling is worth writing for `resolve` once the checkpoint's Task Statement 2.4 questions land, using the environment-variable-expansion pattern those questions cover — a real, useful artifact, just not one this module's deterministic tier checks.

---

*Module content authored 2026-07-15, both tiers built together from the start. A doubt-driven-development review the same day found the cumulative-gate chain was broken and the checker trusted learner-editable test files, among other real issues — remediated same day, see `docs/decisions.md`. Dry run: `runs/2026-07-15-module-03-dry-run/grading.md`.*
