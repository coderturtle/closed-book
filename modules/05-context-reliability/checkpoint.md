# Module 05 closed-book checkpoint

**Format:** 12 questions, 15 minutes, 80% (10/12) to pass. Multiple choice, one correct answer, three distractors.

**Before you start:** close or minimize your Claude Code session. No notes, no AI assistance, no searching. See [`docs/design-tension.md`](../../docs/design-tension.md).

**Coverage note:** this checkpoint carries full coverage of CCA-F Domain 5's Task Statements 5.1-5.6. The hands-on exercise's test suite verifies 5.1 (conversation context preservation, via `CaseFacts`), 5.2 (escalation/ambiguity resolution) and 5.5 (human review/confidence calibration, via `should_escalate`), and 5.6 (provenance/multi-source synthesis, via conflict-annotated `CaseFact` records) directly; 5.3 (multi-agent error propagation) and 5.4 (large-codebase context management — scratchpad files, `/compact`) are architectural/workflow judgment calls with no `resolve`-specific artifact yet (this project has no subagents and isn't itself a large codebase under active exploration), so they're tested here instead.

**Originality note:** every question is written originally against the published task statement it tests — none are copied or reworded from Anthropic's real exam, any leaked item bank, or Anthropic's own official sample questions.

---

## Questions

**1. (Task Statement 5.1)** `resolve`'s coordinator session runs 20 turns long. A contributor proposes periodically summarizing the earlier conversation to save context, trusting the summary to preserve the `customer_id` and `order_id` established at turn 3. What's the risk, and what does `resolve` actually do instead?

A) A summary is lossy by nature — a paraphrase could quietly drop or alter a specific fact; the safer approach is `CaseFacts`, a structured record extracted directly from tool results, not reconstructed from summarized prose.
B) There's no risk; summarization is guaranteed to preserve all factual content losslessly.
C) The risk only applies to numeric facts like order amounts, not identifiers like `customer_id`.
D) The fix is to never summarize at all, keeping the full unsummarized transcript forever regardless of length.

**2. (Task Statement 5.1)** `resolve`'s `CaseFacts` stores each fact as a `CaseFact(value, source_tool)` rather than a bare value. What does `source_tool` provide that a bare value wouldn't?

A) Provenance — a record of which tool call established the fact, so a human reviewing the case (or a conflict-detection routine) can judge which of two disagreeing results to trust, not just that a value exists.
B) Nothing extra; `source_tool` exists only for logging/debugging purposes with no bearing on the fact's use in escalation decisions.
C) `source_tool` determines the order tools were called in for the whole session, functioning as a session-wide event log.
D) `source_tool` is required by every dataclass field in Python and has no domain-specific meaning here.

**3. (Task Statement 5.2)** `resolve`'s `should_escalate` is asked to decide whether a session with 2 recorded tool errors and no conflicts, at iteration 4 of 10, should escalate. What should happen?

A) No escalation — `error_count` (2) is below the 3-error threshold and `iterations_used` (4) isn't near the 10-iteration limit; escalating here would be premature, treating a normal retry as if it were already a crisis.
B) Escalate immediately — any tool error at all should trigger escalation regardless of count.
C) Escalate only if the customer explicitly asks for a human, never based on internal signals.
D) No escalation is ever appropriate before `max_iterations` is fully exhausted.

**4. (Task Statement 5.2)** A contributor proposes that `resolve`'s coordinator should escalate whenever the customer's message "sounds frustrated," using the model's own sentiment read of the conversation. What's the concern, consistent with this module's design?

A) Sentiment read from the model's own interpretation is an unreliable proxy — it isn't grounded in a structured, checkable signal the way conflict detection or an error-count threshold is, and can vary in ways nothing external verifies.
B) There's no concern; sentiment analysis is always more reliable than structured signals.
C) The concern only applies to positive sentiment, not negative sentiment.
D) Sentiment should be the *only* signal used, replacing structured signals like conflicts and error counts entirely.

**5. (Task Statement 5.3)** A coordinator delegates a task to a subagent via the `Task` tool. The subagent's underlying operation fails. Which return value gives the coordinator the most useful basis for a recovery decision?

A) A structured result naming the failure category and specifics (e.g., which lookup failed and why), mirroring the same `errorCategory`/`isRetryable` discipline Module 03's tools already use — so the coordinator can choose a different recovery path per failure type, not just see one generic "the subagent failed."
B) A bare boolean `False`, since the coordinator only needs to know whether to retry.
C) Silence — the subagent should simply not return anything on failure, and the coordinator should infer failure from a timeout.
D) A raised exception that crashes the coordinator's own process, forcing a full session restart.

**6. (Task Statement 5.3)** In a multi-agent `resolve` extension, a billing-dispute subagent fails partway through and a shipping-issue subagent (working a separate part of the same case) succeeds. What's the correct way for the coordinator to handle this?

A) Treat the two results independently — the shipping subagent's success should not be discarded or blocked by the billing subagent's failure; the coordinator should surface the specific billing failure for escalation while still using the shipping result.
B) Discard both results entirely, since one subagent in the case failed.
C) Retry the shipping subagent as well, on the theory that any failure anywhere in the case invalidates every other subagent's work.
D) Silently proceed as if the billing subagent had also succeeded, to avoid interrupting the customer's overall resolution.

**7. (Task Statement 5.4)** A contributor is using Claude Code on `resolve` as it grows past its current four tools, adding many new modules across a larger codebase. Context is filling up with file contents from earlier exploration that's no longer relevant to the current task. What's the appropriate move?

A) Use `/compact` at a natural task boundary to condense the conversation, or write durable notes to a scratchpad file for facts that must survive regardless of what gets compacted — rather than letting irrelevant early exploration silently crowd out room for the current task.
B) Never compact; always keep the full history, since any compaction risks losing something.
C) Restart a brand new session for every single file read, regardless of task continuity.
D) Increase the model's context window setting to avoid ever needing to manage context at all.

**8. (Task Statement 5.4)** A contributor wants a fact discovered mid-session (e.g., "`resolve`'s refund tool caps amounts at `refundable_cents`, found by reading `process_refund.py`") to survive even if the conversation is later compacted. What's the right mechanism?

A) Write it to a scratchpad file on disk — a durable artifact `/compact` doesn't erase, unlike a fact that exists only inside the conversation's own token history.
B) Repeat the fact in every subsequent message so it's never more than one turn old.
C) Rely on the model's memory of earlier turns, since compaction only summarizes, never truly discards information.
D) There's no way to preserve a fact across compaction; it must be rediscovered from scratch afterward.

**9. (Task Statement 5.5)** `resolve`'s `should_escalate` takes `case_facts`, `iterations_used`, and `max_iterations` — no confidence parameter. Why is this a deliberate design choice, not an oversight?

A) A model's self-reported confidence is exactly the unreliable proxy Task Statement 5.5 warns against — the function is designed to only have access to structured, externally-checkable signals (conflicts, error count, iteration proximity), so it can't be tempted to lean on an unverifiable one.
B) It's an oversight; a future version should add a confidence parameter as soon as possible.
C) Confidence scores are perfectly reliable, so omitting one is purely an implementation-simplicity choice with no reliability rationale.
D) The omission is arbitrary and unrelated to any stated design principle.

**10. (Task Statement 5.5)** A contributor argues that `resolve`'s `confidence-proxy-attempt` (checking only `iterations_used`, ignoring `case_facts.conflicts` and `error_count`) is "close enough," since it still escalates once iterations get high. What's the flaw in that reasoning?

A) By the time iterations run high, real, earlier signals (an unresolved conflict, repeated tool failures) may already have made escalation the right call much sooner — "escalates eventually" isn't the same claim as "escalates when it should," and the session may burn many turns on a case that was already known to be unreliable.
B) There's no flaw; checking iterations alone is provably equivalent to checking all three signals.
C) The flaw only matters if `max_iterations` is set unusually low.
D) The correct fix is to remove the iteration check entirely, relying only on conflicts and error count.

**11. (Task Statement 5.6)** `resolve`'s `get_customer` is called twice in one session and returns two different `customer_id` values. What must `update_case_facts` do, and why?

A) Record the disagreement in `conflicts` (both the old and new sourced values), and update the current value to the latest result — silently keeping only one side would hide a real signal a human reviewing the case needs to see.
B) Keep only the first value permanently, ignoring the second result entirely.
C) Raise an exception and halt the session immediately, since any factual disagreement is unrecoverable.
D) Average or otherwise combine the two `customer_id` values into a single merged value.

**12. (Task Statement 5.6)** Why does each `CaseFact` record `source_tool` instead of the system just storing a bare `resolved: true/false` per fact? Note what `resolve`'s `CaseFact` actually stores: `value` and `source_tool` only — no call ID, timestamp, or arguments, so it cannot distinguish two separate calls to the *same* tool from each other, only which *tool* (or mechanism) produced a value.

A) A true/false flag says a fact exists but not where it came from — `source_tool` is what lets a human trace a claim back to which tool established it, and lets a conflict be judged in terms of *what kind* of source disagreed (e.g., a `lookup_order` result vs. a `process_refund` result), which is real provenance information a bare flag carries none of.
B) `source_tool` exists purely by dataclass convention and carries no information relevant to synthesis or provenance.
C) A true/false flag would be strictly more informative than tracking which tool produced a fact.
D) `source_tool` is enough on its own to tell whether two conflicting values came from two independent calls to the same tool or a single re-report — it captures call-level identity, not just which tool was involved.

---

## Answer key

**Do not scroll further until you've answered all 12 questions closed-book and recorded your answers.**

1. **A.** Structured extraction from tool results avoids the lossiness inherent to summarizing prose. (B overstates summarization's reliability. C arbitrarily narrows the risk to one fact type. D over-corrects into an impractical "never summarize" absolute that this module's actual design doesn't require.)
2. **A.** Provenance is what makes a conflict judgeable and a claim traceable — exactly what a bare value can't provide. (B dismisses a field with real functional use in conflict detection. C invents a session-log role `source_tool` doesn't play. D misattributes a Python language requirement that doesn't exist — dataclass fields carry no such obligation.)
3. **A.** Both thresholds (`error_count >= 3`, `iterations_used >= max_iterations - 1`) are unmet — escalating here is premature by this module's own stated design. (B treats any single error as a crisis, contradicting the stated threshold. C introduces a rule this module never states. D ignores that conflicts and error thresholds can independently trigger escalation before `max_iterations` is exhausted.)
4. **A.** Sentiment inferred from the model's own read is unverifiable and exactly the class of proxy Task Statement 5.5 warns against, unlike a conflict list or error count a test can actually check. (B asserts the opposite of the documented concern. C draws an arbitrary distinction not supported by the concern itself. D replaces reliable signals with the very proxy the question identifies as unreliable.)
5. **A.** Structured failure detail lets the coordinator choose an appropriate recovery path per failure type — the same principle Module 03's own tool error shape encodes. (B withholds the detail needed to choose a recovery path. C makes failure indistinguishable from a slow success. D crashes the entire system over one subagent's failure, the least graceful option available.)
6. **A.** Independent subagents' results should be handled independently — one's failure shouldn't discard another's real, valid success. (B discards good work for no reason tied to the actual failure. C treats an unrelated subagent's success as suspect without cause. D fabricates a success that didn't happen, hiding a real failure from anyone who needs to know about it.)
7. **A.** `/compact` at a natural boundary, or a scratchpad file for facts that must survive regardless, directly addresses irrelevant context crowding out room for the current task. (B ignores the actual context-management problem the question describes. C is wasteful and discards task continuity for no benefit. D describes a setting that doesn't eliminate the underlying need to manage what's actually relevant in context.)
8. **A.** A scratchpad file is durable across compaction in a way conversation-only facts are not. (B is a workable but wasteful manual substitute for the actual mechanism. C incorrectly assumes compaction never actually discards detail. D gives up on a real, available mechanism.)
9. **A.** The signature's own shape (no confidence parameter) is a deliberate structural choice ruling out the unreliable-proxy anti-pattern, not an accidental omission. (B contradicts the stated design intent. C asserts confidence scores are reliable, which is exactly the claim this module's design rejects. D denies a design rationale that the module states directly.)
10. **A.** "Eventually escalates" is a weaker property than "escalates when the earliest real signal appears" — real signals available earlier are being ignored in favor of waiting for a proxy to catch up. (B claims a false equivalence between one signal and three independent ones. C narrows the flaw to a parameter-tuning issue it isn't. D proposes removing the one signal that's actually valid, rather than restoring the two that are missing.)
11. **A.** Recording the conflict (not just silently picking one side) is Task Statement 5.6's own "conflicting-source annotation" requirement in practice. (B discards a real, potentially more current result with no justification. C treats a recoverable, documentable situation as fatal. D fabricates a value that was never actually reported by anything.)
12. **A.** Source attribution (which tool/mechanism produced a value) is real provenance information a bare flag carries none of — worth being precise about its actual limit: `source_tool` alone does *not* let you tell two independent calls to the *same* tool apart from a single re-report, since `CaseFact` records no call ID or timestamp; it only distinguishes *which tool*, not *which call*. (B dismisses a field with a clear, stated functional role. C gets the comparison backwards — true/false is strictly *less* informative. D overclaims what a bare `source_tool` string can actually prove — this is the resolvable-looking but wrong answer, since `resolve`'s `CaseFact` has no field that could make this distinction.)

---

*Checkpoint authored 2026-07-16, alongside Module 05's hands-on tier, both built together from the start.*
