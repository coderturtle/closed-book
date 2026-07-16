# Module 04: Agentic Loops and Multi-Agent Orchestration

## The question this module answers

How does an agentic loop actually decide when it's done, and how do you enforce a real safety rule about tool-call ordering without trusting the model's own word for what it already did?

## Where it sits in the arc

Fourth module, and the largest single domain in CCA-F by weight (27%). Hard prerequisite: [Module 03, Designing Tools and MCP Interfaces](../03-tool-mcp-design/README.md) — this module's checker chains Module 03's (which chains Module 02's, which chains Module 01's). This is the module every prior one was building toward: `src/agent.py`'s coordinator agent is the real caller of the four tools Module 03 implemented. Next: [Module 05, Context and Reliability at Scale](../05-context-reliability/README.md) — the hinge is that context management has nothing real to manage until this module's agent exists to manage it for. See [`modules/README.md`](../README.md).

## Exercise: the coordinator agent

Runs against `fixtures/resolve/`, continuing the shared project. Implement two functions in `fixtures/resolve/src/agent.py`, both currently `raise NotImplementedError`, both already carrying a real docstring stating their contract:

- **`run_support_session`** — the agentic loop. Send the growing conversation to an injected `model_client`; while the response's `stop_reason` is `"tool_use"`, run `verify_before_refund_hook` first — if it returns a rejection, feed that rejection back to the model as the tool's result *without executing the tool*; otherwise dispatch the real tool and feed back its actual result. Append every tool call and result to the conversation history so the next turn has full context. Stop when `stop_reason` is `"end_turn"`. `max_iterations` (default 10) is a safety backstop, not the primary stopping mechanism — hitting it is a distinguishable failure, not a silent truncation.
- **`verify_before_refund_hook`** — a programmatic hook (Task Statement 1.5), not a prompt instruction. The rule it enforces: `process_refund`'s `customer_id` must match the customer a `get_customer` call already *succeeded* for, earlier in the same session — not merely "some `get_customer` call succeeded at some point." A session that verifies customer A is not license to refund customer B. `escalate_to_human` is never blocked — it's this project's fail-open path.

`model_client: AgentModelClient` and `tools: ToolRegistry` are both injected (mirroring Module 02's `model_client` injection and Module 03's `backend` injection), so the provided test suite can supply a scripted model client and spy tool functions without a live API call or Module 03's real tool bodies. Two possible response shapes from `model_client`, distinguished by `stop_reason` alone — **never by inspecting response text**, which is the module's own documented anti-pattern (a response can carry `stop_reason: "tool_use"` and misleading wrap-up-sounding text at the same time; the loop must still treat it as a tool call):

```python
{"stop_reason": "tool_use", "tool_name": str, "tool_args": dict}
{"stop_reason": "end_turn", "text": str}
```

**Scope, stated explicitly (resolves a deferral `backend.py` stated during Module 03):** this module does not extend `Backend` into a stateful, mutating protocol. Refund persistence and idempotency are real production concerns, but they're Domain 2 (tool design) territory this project already resolved in Module 03, not Domain 1 (agentic orchestration), which is what this module teaches. `process_refund`'s "success" response continues to mean "this refund decision was verified valid," not "money has moved," for the rest of this project — see `docs/decisions.md` for the record of this call.

A real, provided test suite (`fixtures/resolve/tests/test_agent.py`, 17 tests) checks, among other things: the loop terminates on `stop_reason == "end_turn"` and nowhere else, including when response text is deliberately misleading; a tool call's actual result reaches the *next* call to `model_client` inside the conversation history, not just that a second call happened; `max_iterations` returns the specific sentinel `stop_reason: "max_iterations"`, exercised against a scripted client that never stops; the hook blocks `process_refund` before `get_customer` has run, and the rejection is fed back without the tool's real implementation ever executing; a `get_customer` call that *fails* (structured "not found" error) does not count as verification; a *different* tool succeeding (e.g. `lookup_order`) does not substitute for `get_customer` specifically; a refund attempted for a `customer_id` different from the one `get_customer` actually verified is blocked, even within the same session; `escalate_to_human` is never blocked, with or without prior verification, checked both against the hook function directly and end-to-end through the loop. Every spy tool double requires `backend` to be passed explicitly by keyword — an implementation that forgets it fails loudly (`TypeError`), the same way it would against the real Module 03 tools.

Get `python3 scripts/verify_module_04.py <path-to-your-attempt>` (run from the repo root) to pass, then check it against the rubric below.

## The two-tier gate

**Tier 1 — deterministic, hands-on with Claude Code.** `scripts/verify_module_04.py`: chains Module 03's check (which chains Module 02's, which chains Module 01's) via a real importable `check_module_03`/`check_module_04` function, then runs the *repo's own canonical copy* of the test suite against your `agent.py` — not whatever copy sits in your own submission.

**Tier 2 — exam-condition, closed-book without Claude Code.** [`checkpoint.md`](checkpoint.md): 14 originally-written questions covering the full CCA-F Domain 1 blueprint (1.1-1.7) — the largest domain, so this checkpoint runs toward the upper end of the workshop's default range. Close your Claude Code session before starting it. 80% (12/14, rounded up) to pass.

Both tiers are required to advance.

## Rubric (deterministic tier's rubric; the closed-book checkpoint is scored separately)

1. **`python3 scripts/verify_module_04.py` exits 0 (gate, deterministic).** The chained cumulative gate passes, and all 17 provided tests pass.
2. **`agent.py`'s docstrings document *why* `verify_before_refund_hook` is a session-level check, distinct from and layered on top of Module 03's own tool-level re-verification in `process_refund` — not merely that the two exist (scored, conceptual).** Property, not technique: the *reasoning* for two layers instead of one should be visible in your own words, not copied from the stub's docstring. This module's own dry run constructed an attempt (`thin-docstring-attempt`) where every test passes with the reasoning fully stripped — only this criterion catches that gap.
3. **A rejected tool call's message actually names what's missing, not a bare "blocked" (partially deterministic — the test suite checks the message names `get_customer`/verification; conceptually scored beyond that for whether the message would let a real agent self-correct on its next turn).**
4. **`max_iterations` exhaustion returns the specific sentinel `stop_reason: "max_iterations"` — deterministic, tested directly against a scripted client that never stops (an implementation returning any other non-`end_turn` value does not satisfy this).**

**Before trusting a green checker as proof you're done:** this module went through two rounds of scrutiny before shipping, both real. First, its own dry run (`runs/2026-07-15-module-04-dry-run/grading.md`) constructed five attempts before any real learner touched it, proactively rather than after an external review found the gap — a discipline earned from Modules 01-03, each of which needed an external doubt-driven-development pass to find at least one issue this module tried to close by construction instead. Second, a doubt-driven-development review (a fresh Claude subagent + Codex, given ARTIFACT+CONTRACT only) found something the proactive dry run had missed anyway: the hook's original design blocked on "did *any* `get_customer` call succeed in this session," never checking *which* customer it verified — a session that verified customer A could refund customer B, and the original 12-test suite didn't catch it. Fixed by binding `verify_before_refund_hook` to the specific `customer_id` `get_customer` actually verified (`SessionState.verified_customer_id`), with four new tests closing the gap (a mismatched-customer-id integration test, a different-tool-succeeded test, a hook-unit-level mismatch test, and an `escalate_to_human` loop-level integration test). Read the dry-run file before assuming your own green run means what you think it means — one attempt (`no-hook-attempt`) implements the hook correctly in isolation but never calls it from the loop, so testing the hook function alone isn't sufficient validation either.

## Required to advance / stop condition

Produce an implementation of `run_support_session` and `verify_before_refund_hook` that passes `scripts/verify_module_04.py` and demonstrates the scored conceptual criteria (2-3), **and** pass the closed-book checkpoint at 80%+. Reading this page does not count.

## Before the checkpoint: a non-scored self-check

Before opening `checkpoint.md`, predict which of Domain 1's seven task statements you feel shakiest on — this domain has more task statements than any other, and this exercise's own artifact only gives you a real, gradeable anchor for three of them (1.1, 1.4, 1.5); the checkpoint is where 1.2, 1.3, 1.6, and 1.7 (coordinator-subagent patterns, subagent invocation/context passing, task decomposition, session resumption/forking) get tested instead, since no `resolve`-specific artifact for a *multi*-agent system exists yet in this project. Before running `scripts/verify_module_04.py`, predict which tests will fail and why — specifically, could you explain why a `get_customer` call that returns a structured "not found" error must *not* count as verification, even though the tool was genuinely called? If you can't answer without looking, that's the actual concept this module is testing. See [`.claude/skills/agentic-learning-discipline/SKILL.md`](../../.claude/skills/agentic-learning-discipline/SKILL.md).

## Takeaway

A working agentic loop and a real programmatic hook, built from your own implementation, not copied from documentation — the reference scaffold this whole project's arc has been pointing toward since Module 01. **Not produced by the graded exercise itself, and not claimed as one:** a real coordinator-subagent system (2+ subagents, `Task`-tool invocation, context passing, session resumption) is a natural next artifact once Domain 1's remaining task statements (1.2, 1.3, 1.6, 1.7) have a `resolve`-specific home — this module's checkpoint tests the concepts, but doesn't yet have code to point at.

---

*Module content authored 2026-07-15, both tiers built together from the start. A doubt-driven-development review the same day found the hook's original design didn't bind to the specific customer `get_customer` verified — remediated same day, see `docs/decisions.md`. Dry run: `runs/2026-07-15-module-04-dry-run/grading.md`.*
