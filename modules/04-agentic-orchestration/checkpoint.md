# Module 04 closed-book checkpoint

**Format:** 14 questions, 20 minutes, 80% (12/14) to pass. Multiple choice, one correct answer, three distractors.

**Before you start:** close or minimize your Claude Code session. No notes, no AI assistance, no searching. See [`docs/design-tension.md`](../../docs/design-tension.md).

**Coverage note:** this checkpoint carries full coverage of CCA-F Domain 1's Task Statements 1.1-1.7 — the largest domain in the blueprint (27%). The hands-on exercise's test suite verifies 1.1 (agentic loop lifecycle), 1.4 (multi-step workflow enforcement), and 1.5 (Agent SDK hooks) directly; 1.2 (coordinator-subagent patterns), 1.3 (subagent invocation/context passing), 1.6 (task decomposition strategies), and 1.7 (session state/resumption/forking) are architectural judgment calls with no `resolve`-specific artifact yet (this project's coordinator agent has no subagents of its own yet), so they're tested here instead.

**Originality note:** every question is written originally against the published task statement it tests — none are copied or reworded from Anthropic's real exam, any leaked item bank, or Anthropic's own official sample questions.

---

## Questions

**1. (Task Statement 1.1)** `resolve`'s coordinator agent must decide when a customer support session is complete. A contributor proposes checking whether the model's response text contains phrases like "I've resolved this" or "let me know if you need anything else." What's the correct approach instead?

A) Check the API response's `stop_reason` field — `"end_turn"` means the model has finished its turn with no further tool call pending; text content should never be parsed to infer completion.
B) The text-matching approach is fine as a fallback if `stop_reason` is ever missing from the response.
C) Combine both: check `stop_reason` AND scan for wrap-up phrases, so either signal can end the loop.
D) There's no reliable signal for loop termination; use a fixed number of turns instead.

**2. (Task Statement 1.1)** In `resolve`'s loop, a response comes back with `stop_reason: "tool_use"` and a `text` field that reads "I'm all done here, no more actions needed." What should the loop do?

A) Treat it as a tool-use turn and execute the requested tool call — the `text` field is not authoritative over `stop_reason`, and a model can (rarely, but validly) emit misleading text alongside a real tool request.
B) Treat it as `end_turn` since the text clearly signals completion, overriding the `stop_reason` field.
C) Raise an error, since a tool-use response should never contain wrap-up-sounding text.
D) Ask the model to clarify by sending an empty follow-up message before deciding.

**3. (Task Statement 1.2)** `resolve`'s coordinator is being extended into a system with a specialized billing-dispute subagent and a shipping-issue subagent. A contributor proposes having the coordinator make every tool call itself and only use the subagents to "double check" the coordinator's own conclusions afterward. What's the concern with this design?

A) It doesn't actually delegate any work — the coordinator remains a bottleneck for every decision, and the subagents add coordination overhead without reducing the coordinator's own context or workload, defeating the reason to introduce them at all.
B) There's no concern; having subagents double-check the coordinator only adds reliability, with no downside.
C) The concern only applies if the subagents are given different tools than the coordinator has.
D) Subagents should never be used for verification tasks, only for producing original work.

**4. (Task Statement 1.2)** A coordinator-subagent design for `resolve` needs a rule for when a customer's issue is handled by the coordinator directly versus delegated to a subagent. Which is the better decision criterion?

A) Delegate when the subtask needs focused, isolated context and specialized instructions that the coordinator's own broader context would dilute or distract from — not "delegate everything" or "delegate nothing" as a blanket rule.
B) Always delegate, since a subagent is strictly more capable than a coordinator handling a task directly.
C) Never delegate for customer-facing work; delegation is only appropriate for internal/backend tasks.
D) Delegate based on which subagent would respond fastest, regardless of whether the task actually fits its specialization.

**5. (Task Statement 1.3)** `resolve`'s coordinator invokes a billing-dispute subagent via the `Task` tool, expecting the subagent to already know the customer's order history from the coordinator's own conversation so far. What's wrong with this expectation?

A) A subagent does not automatically inherit the coordinator's conversation context — it starts with a fresh context window and only receives what the coordinator explicitly passes in the task description/prompt; the coordinator must include the order history directly.
B) Nothing is wrong; the `Task` tool automatically shares the full parent conversation with every subagent it invokes.
C) The subagent would need to call `get_customer` and `lookup_order` itself regardless of what's passed, since subagents cannot receive any information from a coordinator under any circumstance.
D) Context sharing depends on whether the subagent was defined with `AgentDefinition` or invoked ad hoc — only `AgentDefinition`-based subagents inherit parent context automatically.

**6. (Task Statement 1.3)** A `resolve` subagent finishes its work and needs to report its findings back to the coordinator. What's the correct mechanism?

A) The subagent's final result is returned as the `Task` tool call's result to the coordinator — the coordinator receives it as a tool result in its own conversation, the same as any other tool call's output, not as a live shared conversation.
B) The subagent directly appends messages to the coordinator's own conversation history in real time as it works.
C) The subagent must call `escalate_to_human` to report anything back, since subagents cannot communicate results to a coordinator directly.
D) The coordinator polls a shared session file that the subagent writes progress updates to.

**7. (Task Statement 1.4)** `resolve`'s canonical safety rule (never refund before a verified customer) spans multiple steps of a session: `get_customer` must run, then `process_refund` may run. A contributor proposes enforcing this purely via a system-prompt instruction telling the model "always verify before refunding." What's the concern, given this module's own design?

A) A prompt instruction is advisory, not enforced — the model can still call `process_refund` first (a misunderstanding, a long context diluting the instruction, or an adversarial input); a programmatic hook is what actually guarantees the ordering regardless of what the model decides to do.
B) There's no concern; a clear enough prompt instruction is functionally equivalent to a programmatic check.
C) The concern only matters for financial actions, so `escalate_to_human`'s ordering doesn't need any enforcement mechanism at all.
D) Prompt instructions and hooks are redundant with each other, so adding a hook means the prompt instruction should be removed entirely.

**8. (Task Statement 1.4)** When `resolve`'s coordinator hands off an unresolved case to `escalate_to_human`, what makes the handoff itself reliable, as opposed to merely happening?

A) The handoff packages structured, complete context (the required `root_cause`/`recommended_action` summary fields) the receiving party actually needs — a handoff without sufficient context is not meaningfully different from no handoff at all.
B) The handoff is reliable as long as it occurs before the conversation times out, regardless of what it contains.
C) The handoff only needs to include the customer's original message; the receiving human can look up everything else themselves.
D) Reliability here is purely about latency — how quickly the handoff occurs, not what it contains.

**9. (Task Statement 1.5)** `resolve`'s `verify_before_refund_hook` needs to block `process_refund` from executing at all when the session hasn't verified the customer — not just flag the problem after the fact. Which hook type does this correspond to?

A) A `PreToolUse`-style hook — it runs before the tool executes and can prevent execution outright, which is what blocking a call requires; a hook that only sees the tool's result after it already ran couldn't have prevented the refund from happening.
B) A `PostToolUse`-style hook, since it needs to inspect what `process_refund` actually did.
C) Either hook type works identically here, since both run within the same tool-call lifecycle.
D) A `Notification` hook, since its job is just to alert someone that a refund was attempted.

**10. (Task Statement 1.5)** A contributor argues `resolve`'s `verify_before_refund_hook` is unnecessary, since `process_refund` (Module 03) already independently re-verifies the customer against the backend before doing anything else. What's the strongest counter-argument, consistent with this project's own stated design?

A) Defense in depth: the hook and the tool's own re-verification are two independent layers deliberately kept separate — removing either one turns a bug or bypass in the other into a single point of failure, instead of being caught by the remaining layer.
B) The hook is genuinely unnecessary once the tool re-verifies; keeping both is pure redundancy with no real benefit.
C) The hook matters only because it runs faster than the tool's own check, not because it adds independent protection.
D) The tool's own re-verification should be removed instead, since the hook alone is sufficient on its own.

**11. (Task Statement 1.6)** A contributor is decomposing a complex `resolve` case (a disputed charge, an order delivered to the wrong address, and a request to change notification preferences) into subagent-sized subtasks. They propose one subagent per individual tool call — a `get_customer`-subagent, a `lookup_order`-subagent, a `process_refund`-subagent, and so on. What's the concern?

A) Decomposing down to individual tool calls fragments a task that has real cross-step dependencies (the refund decision depends on the order lookup, which depends on the customer lookup) across coordination boundaries that add overhead without adding real specialization — the same over-fragmentation risk named for tool granularity in Module 03, here applied to subagent granularity.
B) There's no concern; more subagents always means more parallelism and strictly better performance.
C) The concern only applies if the subtasks would otherwise have run sequentially anyway.
D) One-subagent-per-tool-call is the documented best practice for any multi-tool workflow.

**12. (Task Statement 1.6)** The same case in Q11 does have one natural decomposition boundary: the billing dispute is a genuinely different specialization (policy, refund rules) from updating notification preferences (a simple account-settings change). What decomposition principle does this illustrate?

A) Decompose along real boundaries — differing expertise/specialization, or genuinely independent subtasks — not along an arbitrary unit like "one subagent per tool," and not by leaving one agent to hold unrelated concerns in a single undifferentiated context.
B) Always decompose into exactly two subagents, regardless of a case's actual structure.
C) Decomposition should be based on which subtask the customer happened to mention first in their message.
D) Decomposition doesn't matter, as long as every subagent eventually has access to every tool.

**13. (Task Statement 1.7)** A `resolve` support session is interrupted (the customer's connection drops) partway through a multi-step billing dispute, after `get_customer` succeeded but before `process_refund` was attempted. The customer reconnects five minutes later. What's the correct way to continue, rather than starting over?

A) Resume the existing session — the prior conversation history (including the successful `get_customer` result) is still valid and should be preserved, so the customer doesn't have to re-verify their identity or re-explain their issue from scratch.
B) Always start a completely fresh session on reconnect, regardless of how far the prior session had progressed, to avoid any risk of stale state.
C) Resume the session, but discard the `get_customer` result specifically, since it's now more than a few seconds old and should be treated as if it never happened.
D) Session interruption has no defined handling; the loop should simply crash and require an entirely new call to `run_support_session` to restart.

**14. (Task Statement 1.7)** A `resolve` contributor wants to try two different resolution strategies for the same difficult case from the same starting point, keeping each branch's subsequent conversation independent. They plan to fork the session before attempting a risky step (a real `process_refund` call) in one branch, reasoning that forking will let them safely "undo" that refund if the strategy turns out wrong, since the other branch won't see it happen. What's the flaw in this reasoning?

A) Forking branches the *conversation/session state* going forward into independent continuations — it does not undo or sandbox the real-world side effects of a tool call that already executed; a `process_refund` call made in one branch is not reversed or contained by forking away from it, even though the other branch's own conversation won't show it happened.
B) The reasoning is correct as stated — forking isolates both conversation state and any tool call's real-world side effects, so a refund issued in one branch has no effect outside that branch.
C) Forking makes `process_refund` unavailable entirely, since no tool with real side effects can be called inside a forked session.
D) The flaw is timing, not scope — forking would fully isolate the refund's side effects if it happened *before* the fork instead of after.

**Distinct from resumption:** ordinary session resumption continues a single session's conversation in place; forking branches it into two independent continuations from a shared checkpoint. Both share the same limitation this question tests — neither one un-does a tool call's real-world side effects once executed.

---

## Answer key

**Do not scroll further until you've answered all 14 questions closed-book and recorded your answers.**

1. **A.** `stop_reason` is the authoritative, documented signal for loop termination — text content is never a reliable substitute. (B treats an anti-pattern as an acceptable fallback. C still lets the anti-pattern trigger early termination in some cases. D discards a real, available signal for an arbitrary one.)
2. **A.** `stop_reason` governs regardless of what the accompanying text says — a `tool_use` turn must still be executed as one. (B is exactly the documented anti-pattern. C invents a constraint the API doesn't guarantee. D adds an unnecessary round-trip instead of just trusting `stop_reason`.)
3. **A.** Using subagents only to "double check" the coordinator's own work while the coordinator still makes every call itself delegates nothing real — the coordination overhead is added without the actual benefit (reduced coordinator context/workload) delegation exists to provide. (B ignores the real overhead cost. C misidentifies tool access as the relevant variable. D is an overgeneralization the scenario doesn't support.)
4. **A.** Focused, isolated context need is the real criterion — not an absolute "always/never" rule. (B overstates subagent capability as a blanket truth. C draws an arbitrary line between customer-facing and internal work. D optimizes for the wrong variable — speed instead of fit.)
5. **A.** Subagents start with a fresh context window; the coordinator must explicitly pass what a subagent needs to know. This is the same discipline as `escalate_to_human`'s summary requirement in Module 03 — a receiving party (human or subagent) gets only what it's explicitly given. (B claims automatic full-context sharing, which isn't how subagent invocation works. C overcorrects into "subagents can never receive anything," which isn't true either — they can receive an explicitly passed task description. D invents a distinction based on definition style that isn't the actual mechanism.)
6. **A.** A `Task` tool invocation's result is returned to the coordinator as a tool result, the same shape as any other tool call's output. (B describes a live-sharing mechanism that doesn't match how subagent invocation actually works. C misapplies `escalate_to_human`, a specific tool for a specific purpose, as the only communication channel. D invents an out-of-band mechanism that isn't how results are returned.)
7. **A.** A prompt instruction has no enforcement mechanism behind it; a model can still violate it under normal, non-adversarial conditions (a long context, an ambiguous case) as well as adversarial ones. A hook is what actually guarantees the ordering. (B treats an unenforced instruction as equivalent to an enforced check, which this module's whole design argues against. C draws an arbitrary distinction resolve's own design doesn't support. D misunderstands defense in depth — the two mechanisms aren't redundant, they're complementary.)
8. **A.** Complete, structured context is what makes a handoff actually usable by whoever receives it — exactly the reasoning `escalate_to_human`'s own required summary fields encode (see Module 03). (B focuses on timing, not content, missing what actually makes a handoff reliable. C discards information a human reviewer has no other way to reconstruct. D is the same timing-only mistake as B.)
9. **A.** Blocking a call before it executes requires a hook that runs before the tool, with the power to prevent execution — a `PreToolUse`-style hook. (B describes a hook that runs too late to prevent anything. C incorrectly treats the two hook types as interchangeable for this purpose. D misidentifies the hook's job as merely alerting, not preventing.)
10. **A.** Defense in depth is exactly the reasoning `process_refund`'s own docstring gives for keeping both layers: a bug or bypass in one layer is still caught by the other. (B contradicts this project's own stated design rationale. C misidentifies speed as the reason for the hook's existence, rather than independent protection. D proposes removing the layer that's actually harder to bypass from outside the loop.)
11. **A.** Fragmenting a task with real cross-step dependencies into one-subagent-per-tool-call adds coordination overhead at every dependency boundary without adding genuine specialization — the same over-granularity risk Module 03 named for tool design, here at the subagent level. (B assumes more subagents is strictly better, ignoring the coordination cost. C narrows the concern to a case that doesn't change the underlying issue. D states a "best practice" that isn't supported — the opposite is closer to true here.)
12. **A.** Real specialization or genuine independence are the boundaries that make decomposition worthwhile; an arbitrary unit like "one subagent per tool" or one undifferentiated agent holding unrelated concerns both miss this. (B invents an arbitrary fixed count unrelated to the case's actual structure. C bases decomposition on message order rather than task structure. D ignores that tool access alone doesn't substitute for actual task-appropriate decomposition.)
13. **A.** The prior session's valid state (including a successful verification) should be preserved on resumption — that's the entire value of session state existing in the first place. (B discards valid, already-verified state for no reason tied to any actual risk. C invents an arbitrary staleness rule the scenario gives no basis for. D describes an undesirable, avoidable failure mode, not a correct design.)
14. **A.** Forking isolates conversation/session state, not the real-world effects of a tool call that has already run — a `process_refund` call is not reversible by branching away from it, since the refund happened against the real backend regardless of which conversation branch continues afterward. This is a genuinely easy misconception: forking *feels* like a safe sandbox because the *conversation* is isolated, but a tool with real side effects doesn't share that isolation. (B is the misconception itself, stated as fact — the exact trap this question is testing. C overcorrects into "forking disables real tools entirely," which isn't true; forking just doesn't protect against what they do. D relocates the same wrong claim to a timing condition — side effects aren't undone by forking regardless of when the fork happens relative to the tool call.)

---

*Checkpoint authored 2026-07-15, alongside Module 04's hands-on tier, both built together from the start.*
