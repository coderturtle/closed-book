# Module 03 closed-book checkpoint

**Format:** 12 questions, 15 minutes, 80% (10/12) to pass. Multiple choice, one correct answer, three distractors.

**Before you start:** close or minimize your Claude Code session. No notes, no AI assistance, no searching. See [`docs/design-tension.md`](../../docs/design-tension.md).

**Coverage note:** this checkpoint carries full coverage of CCA-F Domain 2's Task Statements 2.1–2.5. The hands-on exercise's test suite verifies 2.1 (tool interface/description presence) and 2.2 (structured error responses) directly; 2.3 (tool distribution across agents), 2.4 (MCP server integration), and 2.5 (built-in tool selection) are architectural/configuration judgment calls with no `resolve`-specific artifact yet (Module 04 is where multiple agents and a real MCP server wiring first exist), so they're tested here instead.

**Originality note:** every question is written originally against the published task statement it tests — none are copied or reworded from Anthropic's real exam, any leaked item bank, or Anthropic's own official sample questions.

---

## Questions

**1. (Task Statement 2.1)** `resolve`'s `get_customer` and `lookup_order` tools have nearly identical signatures (both take one or two string identifiers). Production logs show the agent sometimes calls `get_customer` with what is clearly an order ID. What's the most direct fix?

A) Expand both tools' descriptions to explicitly state which identifier formats each accepts and give at least one boundary example distinguishing them, rather than relying on the tool names alone.
B) Rename `get_customer` to `get_customer_do_not_use_for_orders` so the distinction is unmissable.
C) Merge the two tools into one that accepts either kind of identifier and figures out which is which internally.
D) Add a few-shot example to the agent's system prompt showing correct tool selection, instead of touching the tool descriptions.

**2. (Task Statement 2.1)** A `resolve` contributor is designing `escalate_to_human`'s tool description. Which description would most effectively prevent an agent from calling it with an incomplete summary?

A) A description that explicitly lists the required summary fields (`root_cause`, `recommended_action`) and states that a human reviewing the case has no access to the conversation transcript, so an incomplete summary produces a worse outcome than delaying the call.
B) A description that says "escalate the case to a human agent" with no further detail, trusting the model to infer what a good summary looks like.
C) A description that lists every possible field a summary could theoretically contain, to maximize completeness.
D) No description at all — the parameter names (`customer_id`, `reason`, `summary`) are self-explanatory.

**3. (Task Statement 2.1)** `resolve`'s tools currently give an agent access to `get_customer`, `lookup_order`, `process_refund`, and `escalate_to_human` — four tools total. A contributor proposes adding twelve more granular tools (e.g., splitting `get_customer` into `get_customer_by_email`, `get_customer_by_phone`, `get_customer_by_account_id`). What's the most likely effect on tool selection reliability?

A) Reliability likely degrades — giving an agent many similar tools increases decision complexity and the chance of picking a plausible-but-wrong one, the opposite of the goal.
B) Reliability likely improves, since each tool now does exactly one thing.
C) There's no meaningful effect either way; tool count doesn't influence selection accuracy.
D) Reliability improves only if each new tool's name is longer and more descriptive than the original.

**4. (Task Statement 2.2)** `resolve`'s `process_refund` currently returns a bare `False` on any failure, with no further detail. An agent handling this response can't tell whether to retry, explain a policy limit to the customer, or escalate. What's the fix?

A) Return structured error metadata (`errorCategory`, `isRetryable`, a human-readable `message`) so the agent can choose an appropriate recovery path per failure type, instead of one undifferentiated failure signal.
B) Change the bare `False` to a bare `True` so failures don't block the conversation.
C) Log the failure server-side and continue returning `False` to the agent — the agent doesn't need failure detail, only whether to proceed.
D) Retry the call automatically inside `process_refund` itself until it succeeds, so the agent never sees a failure.

**5. (Task Statement 2.2)** `lookup_order` currently returns the exact same error message whether an `order_id` doesn't exist at all, or exists but belongs to a different customer. A contributor proposes making the message more specific in the second case, naming the actual owning customer. What's the concern?

A) Naming the actual owning customer would leak that the `order_id` is valid for someone else's account — the uniform message is a deliberate security boundary, not an oversight to fix.
B) There's no concern; more specific error messages are always better for debugging.
C) The concern only applies to `process_refund`, not read-only tools like `lookup_order`.
D) The fix is fine as long as the more specific message is only shown in server logs, not returned to the agent — but the question describes returning it to the agent, so this option doesn't resolve the actual proposal.

**6. (Task Statement 2.2)** `resolve`'s four tools currently use different error shapes: `get_customer` returns `{"found": false}`, `process_refund` returns `{"success": false, "reason": "..."}`, and `escalate_to_human` raises a bare exception. What's the most direct fix for an agent trying to build one consistent failure-handling strategy across all tool calls?

A) Standardize every tool on the same structured error shape (e.g., `errorCategory`/`isRetryable`/`message`), so the agent's recovery logic doesn't need per-tool special-casing.
B) Leave each tool's error shape as-is, since each tool's failure modes are different anyway.
C) Wrap every tool call in a try/except at the agent level so shape differences never matter.
D) Standardize only `get_customer` and `process_refund`, since `escalate_to_human` is rarely called.

**7. (Task Statement 2.3)** `resolve`'s coordinator agent (Module 04) will eventually delegate to specialized subagents. A contributor proposes giving every subagent access to all four tools "to be safe." What's the concern?

A) Agents with tools outside their actual specialization tend to misuse them — scoped tool access (only what a given agent's role actually needs) reduces this risk; "give everyone everything" trades a real reliability cost for a hypothetical convenience.
B) There's no concern; more tool access is strictly safer than less.
C) The concern only applies to `process_refund`, since it's the only tool with financial consequences.
D) Scoping tool access is a performance optimization, not a reliability one — it has no bearing on correctness.

**8. (Task Statement 2.3)** A `resolve` subagent needs to guarantee it calls `get_customer` before attempting anything else, every time, rather than leaving the choice to the model's judgment. Which `tool_choice` configuration achieves this?

A) Forced tool selection (`tool_choice: {"type": "tool", "name": "get_customer"}`) for the first call, ensuring that specific tool runs before any other step proceeds.
B) `tool_choice: "auto"`, which allows the model to decide whether to call a tool at all.
C) `tool_choice: "any"`, which guarantees a tool call but not which one.
D) No `tool_choice` configuration can guarantee call order; this must be enforced entirely through prompt instructions instead.

**9. (Task Statement 2.4)** `resolve`'s team wants every contributor's Claude Code session to have the same MCP server access to the tools in this project, shared via version control. Where should this be configured?

A) Project-scoped `.mcp.json` at the repository root, checked into version control, so every contributor who clones the repo gets the same server configuration automatically.
B) Each contributor's personal `~/.claude.json`, so individual preferences don't conflict.
C) A `.claude/rules/` file, since MCP server configuration is a "rule" in the same sense path-scoped conventions are.
D) An environment variable set manually on each contributor's machine, with no file-based configuration at all.

**10. (Task Statement 2.4)** `resolve`'s MCP server configuration needs an API credential to reach the real backend. What's the correct way to include it in the project-scoped `.mcp.json` without committing the actual secret to version control?

A) Use environment variable expansion (e.g., `${RESOLVE_BACKEND_TOKEN}`) in the checked-in `.mcp.json`, with the real value supplied via each contributor's local environment, never the file itself.
B) Commit the real credential directly in `.mcp.json`, since the repo is private during development.
C) Store the credential in a code comment above the `.mcp.json` block so contributors know where to find it.
D) Split the credential across two files, each committed, so no single file contains the complete value.

**11. (Task Statement 2.5)** A `resolve` contributor wants to find every place in the codebase that calls `process_refund`, before changing its signature. Which built-in tool is the right first choice?

A) `Grep`, searching file contents for the literal string `process_refund` across the codebase.
B) `Glob`, searching for files matching a naming pattern like `**/*refund*`.
C) `Bash`, running a shell script that recursively greps the codebase — technically works, but duplicates what the purpose-built `Grep` tool already does more directly.
D) `Read`, opening every file in the project one at a time to check for the string manually.

**12. (Task Statement 2.5)** While editing `process_refund.py`, a contributor's `Edit` tool call fails because the target text isn't unique in the file (it appears in both the function body and a nearby comment). What's the correct fallback?

A) Use `Read` to load the full file, then `Write` the corrected version back — a reliable fallback when `Edit`'s unique-anchor-text requirement can't be satisfied.
B) Retry the identical `Edit` call repeatedly until it happens to succeed.
C) Switch to `Bash` with a `sed` command, since shell text substitution doesn't have the same uniqueness requirement and is therefore always safer.
D) Delete the ambiguous comment first using a separate `Edit` call, then retry the original edit — technically works, but adds an unnecessary intermediate step when Read+Write solves it directly.

---

## Answer key

**Do not scroll further until you've answered all 12 questions closed-book and recorded your answers.**

1. **A.** Explicit format/boundary information in the tool description is the direct fix for selection confusion between similarly-shaped tools. (B is a real hack, not a description fix. C removes the actual distinction rather than clarifying it. D treats a tool-design problem as a prompting problem.)
2. **A.** Naming the required fields and explaining *why* completeness matters (a human with no transcript access) is what actually prevents an incomplete call. (B relies on inference that isn't reliable. C over-specifies past the point of being usable. D removes the one thing that actually disambiguates the tool's requirements.)
3. **A.** More tools, especially near-duplicates, increases decision complexity and misselection risk — the documented tradeoff of over-granular tool design. (B assumes narrower always means clearer, which isn't true once tools start overlapping. C is false — tool count is a documented factor in selection reliability. D misidentifies naming length as the relevant variable.)
4. **A.** Structured error metadata lets the agent choose the right recovery path per failure category — the same principle Module 03's own test suite (`_assert_valid_error_shape`) checks directly. (B doesn't fix anything, it just changes which wrong signal is returned. C withholds exactly the information the agent needs to act correctly. D hides real failures from the agent entirely, removing its ability to react appropriately.)
5. **A.** The uniform "not found" message for both cases is a deliberate boundary preventing information leakage about other customers' data — exactly what `resolve`'s own `lookup_order` test (`test_lookup_order_does_not_leak_other_customers_orders`) checks for. (B ignores a real security concern. C incorrectly narrows the concern to one tool. D describes a variant that isn't the proposal actually being evaluated.)
6. **A.** One consistent error shape across every tool is what lets an agent's failure-handling logic generalize, instead of needing a special case per tool. (B accepts the actual problem as unavoidable. C papers over the inconsistency at the call site instead of fixing the source. D partially fixes the problem while leaving a real gap.)
7. **A.** Unscoped tool access is a documented reliability risk (agents misusing tools outside their specialization), not just a hypothetical concern. (B ignores this documented risk entirely. C incorrectly narrows the concern to the one tool with the most obviously visible consequences. D miscategorizes a correctness concern as a performance one.)
8. **A.** Forced tool selection with a specific named tool is exactly the mechanism for guaranteeing a specific call happens before anything else proceeds. (B and C both leave the choice partially or fully to the model, which is the opposite of "guarantee." D is false — `tool_choice` is precisely the mechanism designed for this.)
9. **A.** Project-scoped `.mcp.json`, checked into version control, is the documented mechanism for shared, consistent MCP configuration across a team. (B is for personal, not shared, configuration — the opposite of what's being asked. C conflates two unrelated configuration mechanisms. D abandons file-based configuration entirely, losing the "shared via version control" requirement.)
10. **A.** Environment variable expansion in the checked-in file is the documented pattern for shared configuration with per-contributor secrets. (B is a direct secret leak into version control. C and D are both real secret-handling anti-patterns that don't actually keep the credential out of the repository.)
11. **A.** `Grep` is the purpose-built tool for searching file *contents* for a specific string — exactly this task. (B searches file *names*, not contents, and wouldn't find calls inside arbitrarily-named files. C works but duplicates a built-in tool's exact purpose with an unnecessary extra layer. D is correct in principle but wildly inefficient compared to the purpose-built option.)
12. **A.** Read-then-Write is the documented, reliable fallback exactly when `Edit`'s unique-match requirement can't be satisfied. (B doesn't address the actual cause of the failure. C swaps a safer, purpose-built tool for a less precise one under a false safety claim. D solves the problem indirectly with an unneeded extra step when Read+Write solves it directly.)

---

*Checkpoint authored 2026-07-15, alongside Module 03's hands-on tier, both built together from the start.*
