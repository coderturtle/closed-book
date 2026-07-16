# Module 06 closed-book mock exam

**Format:** matches CCA-F's own real structure, not the workshop's smaller per-module default — this is the one module where that's deliberate (see the module README). A pool of **6 scenarios** below; **complete 4 of the 6** (before you start, have someone else pick your 4 by number, or roll a die twice discarding repeats — don't cherry-pick the ones you feel strongest on, the same discipline the real exam's own random draw enforces). **120 minutes. 720/1000 to pass**, scored as: (questions correct across your 4 scenarios ÷ total questions across your 4 scenarios) × 1000.

**Before you start:** close or minimize your Claude Code session. No notes, no AI assistance, no searching. See [`docs/design-tension.md`](../../docs/design-tension.md).

**Scope, stated honestly:** the real CCA-F exam's 4-drawn-from-6 format totals roughly 60 questions. This pool has 6 scenarios of 7 questions each (42 total; a completed 4-scenario draw is 28 questions) — a deliberate reduction from "roughly 60," not a claim of matching it exactly. Building the real exam's full per-scenario item count would need visibility into the actual exam's own question bank this project doesn't have. What *is* matched faithfully: the 6-pool/4-draw structure, the scenario-based framing (not a flat unscoped question list), and a 720/1000-equivalent scoring threshold computed the same way the real exam computes it.

**Scenario originality note, stated precisely rather than overclaimed:** none of these 6 scenarios' *content* is copied or lightly reworded from the real CCA-F exam's own published scenarios (Customer Support Resolution Agent, Code Generation with Claude Code, Multi-Agent Research System, Developer Productivity with Claude, Claude Code for CI, Structured Data Extraction) — doing that would violate this workshop's own constraint (see `docs/design-tension.md`). One exception to *premise*, disclosed rather than hidden: Scenario A is this project's own `resolve` system, and `resolve` was itself deliberately modeled on the real exam's own "Customer Support Resolution Agent" scenario from the start of this workshop (see `fixtures/resolve/SPEC.md`'s own stated rationale) — every Scenario A question is original, but the system it's about is intentionally, admittedly parallel to that one real scenario, not an independent invention. The other five scenarios' premises were chosen to deliberately steer clear of the real exam's other five named premises (e.g., a release-notes drafting agent rather than a code-review-in-CI agent; a customer-feedback synthesizer rather than a research system; a legacy-codebase documentation generator rather than a general developer-productivity assistant) even where the underlying CCA-F skill being tested is necessarily similar, since these five domains are what they are regardless of which scenario illustrates them.

**Domain coverage across the full pool (all 6 scenarios), stated with two honest gaps:** Domain 1 (Agentic Architecture & Orchestration, 27%) — 11 questions across Scenarios A, C, D. Domain 2 (Tool Design & MCP Integration, 18%) — 8 questions across Scenarios A, E, F. Domain 3 (Claude Code Configuration & Workflows, 20%) — 10 questions across Scenarios B, C, F. Domain 4 (Prompt Engineering & Structured Output, 20%) — 7 questions across Scenarios B, E. Domain 5 (Context Management & Reliability, 15%) — 6 questions across Scenarios A, D. (42 total.) Two gaps worth naming directly rather than leaving implicit: (1) Domains 3 and 4 carry equal real weight (20% each) but this pool gives them 10 and 7 questions respectively — an artifact of each scenario being fixed at 7 questions rather than a deliberate weighting choice. (2) Task Statement 5.4 (large-codebase context management) has no question anywhere in this 42-question pool, the only one of CCA-F's 30 task statements with zero coverage here — it *is* covered directly in [Module 05's own checkpoint](../05-context-reliability/checkpoint.md), so it isn't an uncovered gap in this workshop overall, but a learner treating this mock exam alone as comprehensive should know 5.4 isn't in it.

---

## Questions

### Scenario A: `resolve`, this project's own customer support agent

You've built `resolve` across Modules 01-05 of this workshop: a coordinator agent (`run_support_session`) calling four MCP tools, with a session-level hook, sourced case facts, and a structured escalation decision.

**A1. (Task Statement 1.5)** A contributor proposes replacing `verify_before_refund_hook` with a system-prompt instruction telling the model "always verify the customer before refunding." What's the concern?

A) A prompt instruction is advisory, not enforced — the model can still violate it under a long context, an ambiguous case, or adversarial input; a programmatic hook is what actually guarantees the ordering regardless of what the model decides.
B) There's no concern; a sufficiently clear prompt instruction is functionally equivalent to a hook.
C) The concern only applies to financial actions, so a similar rule for `escalate_to_human` would need no enforcement at all.
D) Hooks and prompt instructions are redundant, so adding a hook means removing the prompt instruction is optional either way.

**A2. (Task Statement 2.1)** `resolve`'s `get_customer` and `lookup_order` have similarly-shaped signatures. What's the most direct fix for an agent occasionally calling the wrong one?

A) Expand both tools' descriptions to state which identifier formats each accepts and give a boundary example distinguishing them.
B) Rename both tools to include the word "important" so the model treats them more carefully.
C) Merge them into one tool that accepts either kind of identifier and infers which is which.
D) Add a few-shot example to the system prompt instead of touching the tool descriptions.

**A3. (Task Statement 1.4)** `resolve`'s canonical safety rule spans multiple steps: `get_customer` must succeed before `process_refund` runs. Why is this correctly described as a *multi-step workflow enforcement* problem, not a single-tool validation problem?

A) The distinction is purely about which module owns the code, not about the underlying difficulty.
B) The rule constrains the *order* and *relationship* between two separate tool calls across turns, not the validity of any one call's arguments in isolation — exactly what Task Statement 1.4 names as a distinct concern from single-tool input validation.
C) It isn't actually different from single-tool validation; `process_refund` could enforce the entire rule alone with no session-level component.
D) Multi-step workflow enforcement only applies when three or more tools are involved.

**A4. (Task Statement 5.6)** Two `get_customer` calls in one `resolve` session return different `customer_id` values. What must the session's case-facts record do?

A) Merge the two customer_id values into one combined value.
B) Record the disagreement with both sourced values preserved, updating the current value to the more recent result — silently keeping only one side would hide a real signal from whoever reviews the case.
C) Keep only the first value permanently and ignore the second result.
D) Halt the session immediately; any factual disagreement is unrecoverable.

**A5. (Task Statement 2.2)** `resolve`'s four tools originally returned different ad hoc failure shapes. What's the benefit of standardizing on one shared error shape (`errorCategory`/`isRetryable`/`message`) across all of them?

A) It replaces the need for any tool to validate its own inputs.
B) It lets the calling agent's recovery logic generalize across tools instead of needing a special case per tool's own failure format.
C) It has no functional benefit; it's purely a stylistic preference.
D) It only matters for tools with financial consequences, not read-only lookups.

**A6. (Task Statement 1.2)** A contributor proposes extending `resolve`'s single coordinator into a coordinator-subagent system, giving every subagent access to all four tools "to be safe." What's the concern?

A) Tool scoping is a performance optimization with no bearing on correctness.
B) Unscoped tool access increases the risk of a subagent misusing a tool outside its actual specialization — scoped access (only what a role needs) reduces this, trading a real reliability cost for a hypothetical convenience.
C) There's no concern; more tool access for every subagent is strictly safer.
D) The concern applies only to `process_refund`, since it's the one tool with financial consequences.

**A7. (Task Statement 5.5)** Why does `resolve`'s `should_escalate` take no confidence or sentiment parameter in its signature?

A) A model's self-reported confidence is an unreliable proxy for whether a session actually needs human review — the function is designed to only see structured, externally-checkable signals, so it can't lean on an unverifiable one.
B) It's an oversight that should be corrected by adding a confidence parameter.
C) Confidence scores are perfectly reliable, so the omission is a pure implementation-simplicity choice.
D) The omission is arbitrary and unconnected to any stated design principle.

---

### Scenario B: an internal documentation search assistant

A platform team is building an assistant that answers engineer questions from a large, frequently-updated internal wiki, always citing which document supported each claim.

**B1. (Task Statement 3.1)** A new team member's Claude Code sessions aren't picking up the wiki-search project's conventions, even though a `CLAUDE.md` exists somewhere in the repo. What's the most likely cause?

A) The new team member needs a personal API key before any project config takes effect.
B) `CLAUDE.md` conventions only apply after the first commit the new member makes.
C) The `CLAUDE.md` is scoped to a subdirectory the new member's working directory isn't under — CLAUDE.md hierarchy resolution is scope-sensitive, not repo-wide by default from every location.
D) `CLAUDE.md` files only apply to the person who originally wrote them.

**B2. (Task Statement 4.3)** The assistant extracts a `publish_date` field from wiki pages, but some pages have no publish date at all. What's the correct handling, consistent with this workshop's own extraction discipline (Module 02)?

A) Represent the missing date explicitly as `null`/`None` in the structured output, distinct from a wrong or fabricated date — collapsing "unknown" into a default value hides that the field was never actually established.
B) Substitute today's date as a reasonable placeholder whenever no date is found.
C) Omit the field from the output entirely so the schema never has to represent "unknown."
D) Fail the whole extraction if any single field is missing, regardless of whether it's actually required.

**B3. (Task Statement 3.3)** The team wants different conventions for `docs/*.md` (writing style rules) versus `src/**/*.py` (code style rules) within the same repo. What's the correct mechanism?

A) One repo-root `CLAUDE.md` containing both sets of rules, trusting the model to apply the right one contextually.
B) Two separate git repositories, since Claude Code cannot scope rules within one repo.
C) A single rules file with no path scoping, relying on the rule text itself to say which files it applies to.
D) Multiple path-scoped `.claude/rules/` files, each with frontmatter limiting it to the relevant glob, so each convention only applies where it's actually relevant.

**B4. (Task Statement 4.4)** The assistant's citation-extraction step occasionally returns a citation that doesn't match the required schema. What's the correct recovery strategy?

A) Silently accept the malformed citation, since some citation is better than none.
B) Retry with the exact same prompt, unchanged, until it happens to succeed.
C) Abandon citations entirely and just have the assistant summarize without sourcing.
D) Retry with the specific validation error fed back into the next prompt, rather than either fabricating a plausible-looking citation or silently dropping the requirement.

**B5. (Task Statement 3.5)** A contributor's first attempt at a Claude Code task fails a validation step. What does *iterative refinement*, as a named Claude Code skill, actually mean here?

A) Manually fixing the output by hand without giving Claude the chance to revise it.
B) Running the exact same prompt again without any change, hoping for a different result.
C) Feeding the specific failure back to Claude and letting it revise its approach based on that concrete feedback, rather than starting over from scratch or repeating the identical attempt.
D) Immediately switching to a different tool or model, since the first attempt already failed once.

**B6. (Task Statement 4.1)** The team wants the assistant's answers to consistently include a confidence label and a list of source document IDs. What's the most direct way to get this reliably, rather than hoping the model remembers to include them?

A) State the required output fields explicitly as part of the prompt's stated criteria, rather than leaving the format to the model's own judgment call each time.
B) Ask the model nicely in natural language without specifying any concrete field names or format.
C) Add the requirement to a comment in the codebase that the model never actually sees.
D) Rely on the model's general training to know what a "good" answer includes.

**B7. (Task Statement 3.6)** The team wants every update to the wiki-search assistant's own citation-extraction code to automatically run its validation checks in CI, not just interactively. What enables running Claude Code in a CI pipeline rather than only interactively?

A) There is no way to run Claude Code outside an interactive terminal session.
B) A separate, entirely different tool is required for any CI integration; Claude Code itself has no CI-facing mode.
C) Non-interactive mode (`claude -p`/`--print`), which produces output and exits instead of waiting for interactive input — the mechanism CI runners actually need.
D) Interactive mode, since CI runners can supply keyboard input the same way a human would.

---

### Scenario C: a release-notes drafting agent in a deploy pipeline

A team wants an agent that runs after every merge to main: it reads the merged commits, drafts a changelog entry categorized by area, and posts it to a release channel — sometimes needing to inspect files well outside the merged diff itself to understand context.

**C1. (Task Statement 1.1)** The release-notes agent's loop needs to know when it has finished drafting the entry and is ready to post it. What's the correct signal, and what's the documented anti-pattern to avoid?

A) Use the API response's `stop_reason` field (`end_turn` vs. `tool_use`) — never infer completion by parsing the assistant's own text for phrases that sound like "done."
B) Parse the assistant's text for words like "finished" or "done," since that's the most human-readable signal.
C) Use a fixed number of tool calls as the only signal, regardless of what `stop_reason` says.
D) Assume the draft is complete as soon as any file-reading tool has been called once.

**C2. (Task Statement 1.5)** The team wants to guarantee the bot can never run `git push --force`, regardless of what the model decides mid-draft. What's the correct mechanism?

A) Trusting the model's own judgment, since a well-written system prompt should be sufficient.
B) Removing git tools from the bot entirely, even though it needs them for other operations.
C) A programmatic hook that intercepts the tool call before it executes and blocks it outright — not a prompt instruction asking the model not to, which the model could still violate.
D) A code comment near the git tooling asking contributors not to force-push.

**C3. (Task Statement 1.6)** A contributor proposes decomposing "draft release notes for this large merge" into one subagent per changed file, regardless of how small or related the files are. What's the concern?

A) There's no concern; more subagents always means more parallelism and strictly better results.
B) The concern only applies if the files would otherwise be drafted in a fixed order anyway.
C) One-subagent-per-file is the documented best practice for any multi-file drafting task, regardless of the files' actual relationships.
D) Fragmenting a task with real cross-file dependencies into overly fine-grained subagents adds coordination overhead at every boundary without adding genuine specialization — the same over-fragmentation risk this workshop has named for tool design, here applied to task decomposition.

**C4. (Task Statement 1.7)** A CI runner hosting the release-notes agent is restarted mid-draft, after several files' changes have already been summarized successfully. What's the correct way to continue?

A) Discard the specific files already summarized and skip them entirely rather than resuming or repeating them.
B) Session interruption has no defined handling; the draft should simply fail and require a human to write it manually instead.
C) Resume the existing session — the work already completed (and the context it required) is still valid, so redoing it from scratch wastes real, already-verified progress.
D) Always restart the entire draft from the first file, regardless of how much progress existed before the restart.

**C5. (Task Statement 3.2)** The team wants a repeatable "run the full release-notes draft" command available to every contributor who clones the repo, not just whoever wrote it. What's the correct mechanism?

A) A personal slash command defined only in the original author's own local configuration.
B) A shell alias defined in the original author's own shell profile, unrelated to the repository.
C) A comment at the top of the drafting script explaining the steps in prose, with no actual command defined.
D) A project-scoped slash command under `.claude/commands/`, checked into version control, so every contributor gets the same command automatically.

**C6. (Task Statement 3.4)** A contributor is about to have Claude Code make a change to the CI pipeline configuration itself — a change with a high blast radius if wrong, since it could break every future build. What's the appropriate mode to use first?

A) Plan Mode is only appropriate for changes to application code, never to CI configuration.
B) There's no meaningful difference between reviewing a plan first and executing directly; both carry identical risk.
C) Plan Mode — review the intended change and its reasoning before anything is actually executed, given how costly a wrong CI config change would be.
D) Direct execution immediately, since CI config files are typically small and low-risk.

**C7. (Task Statement 1.3)** The release-notes agent's coordinator delegates "summarize the changes in this area" to a subagent, without passing along which files actually changed in this merge. What's wrong with this delegation?

A) Nothing is wrong; subagents automatically share the coordinator's full context, including which files changed.
B) The subagent would need to independently re-discover which files changed regardless of what's passed to it, since subagents can't receive any information from a coordinator.
C) This is only a problem if the subagent is defined with `AgentDefinition`; ad hoc subagent invocations don't have this limitation.
D) A subagent does not automatically inherit the coordinator's own context — it starts fresh and only knows what's explicitly passed to it; the coordinator must include the changed-file list directly in the task it hands off.

---

### Scenario D: a multi-channel customer feedback synthesizer

A tool characterizes a recurring product complaint by querying several independent feedback channels (support chat logs, app-store reviews, a sentiment-tagging system) in parallel, then reconciling what each one reports.

**D1. (Task Statement 5.6)** Two of the synthesizer's channels report conflicting figures for the same statistic. What must the synthesis step do?

A) Report only the figure from whichever source was queried first, discarding the other silently.
B) Average the two figures together and present the average as if it were a real, sourced value.
C) Omit the statistic entirely rather than ever surfacing a disagreement between sources.
D) Surface the disagreement explicitly, attributing each figure to its source, rather than silently picking one figure or averaging them into a number neither source actually reported.

**D2. (Task Statement 1.2)** The synthesizer's coordinator queries three specialized subagents (one per feedback channel) and then must reconcile their answers. What's the coordinator's actual job here, distinct from any one subagent's?

A) Picking exactly one subagent's answer at random and discarding the other two entirely.
B) There is no meaningful difference; the coordinator is just another subagent with the same role as the other three.
C) Synthesis and conflict resolution across results the subagents already produced — a coordination role distinct from, and not reducible to, any individual subagent's own narrower retrieval task.
D) Re-doing each subagent's retrieval work itself, in addition to whatever the subagents already did.

**D3. (Task Statement 1.3)** A channel-querying subagent finishes and needs to report its finding back to the coordinator. What's the correct mechanism?

A) The subagent can only communicate by writing to a file the coordinator polls on some fixed schedule.
B) There is no defined mechanism; results are inferred by the coordinator guessing from context.
C) The subagent's result is returned as the invoking tool call's result to the coordinator, arriving as a tool result in the coordinator's own conversation — the same as any other tool call's output.
D) The subagent directly appends its own messages into the coordinator's conversation history in real time as it works.

**D4. (Task Statement 5.3)** One of the three channel-querying subagents fails partway through (its underlying channel's API is unreachable), while the other two succeed. What should the coordinator do?

A) Silently present an answer as if all three sources had succeeded, omitting any mention of the failure.
B) Treat the failure independently — surface the specific failure for the failed source while still synthesizing an answer from the two that succeeded, rather than discarding all three results.
C) Discard all three subagents' results, since one of them failed.
D) Retry the two successful subagents as well, on the theory that any single failure invalidates the whole batch.

**D5. (Task Statement 5.1)** The synthesizer's conversation grows very long across a multi-turn characterization session. A contributor proposes periodically summarizing older turns to save context. What's the risk to guard against?

A) The risk applies only to numeric facts, never to categorical ones like a source's name.
B) The only correct fix is to never summarize at all, regardless of how long the conversation grows.
C) A summary can quietly drop or alter a specific fact established earlier — a structured, persistent record of key facts (not a hope that summarization preserves everything) is the more reliable approach for facts that must survive.
D) There is no risk; summarization is guaranteed to losslessly preserve every fact from the summarized turns.

**D6. (Task Statement 1.4)** The synthesizer has a rule: a final characterization may not be presented until at least two independent channels have been successfully queried. Why is this best enforced as a programmatic check rather than a prompt instruction?

A) A prompt instruction is provably equivalent in reliability to a programmatic check for this kind of rule.
B) This kind of ordering rule cannot be enforced programmatically at all; only prompting can express it.
C) The choice between the two mechanisms has no bearing on reliability, only on code readability.
D) A programmatic check guarantees the ordering regardless of what the model decides to do, including under a long context or an ambiguous case — a prompt instruction is advisory and can be violated.

**D7. (Task Statement 5.2)** A contributor proposes escalating to a human analyst whenever the model's own generated text "sounds uncertain." What's the concern, consistent with this workshop's own design?

A) Textual uncertainty cues aren't a structured, externally-checkable signal — an unreliable proxy for whether escalation is actually warranted, unlike a real signal such as an unresolved source conflict.
B) There's no concern; text-based uncertainty cues are always a fully reliable escalation signal.
C) The concern only applies when there are fewer than two sources queried.
D) Text-based escalation triggers should replace structured signals entirely, since they're simpler to implement.

---

### Scenario E: a batch content-moderation pipeline

A pipeline runs Claude over a large daily batch of user-submitted listings, flagging policy violations with a structured category and a recommended action, then a small number are spot-checked by a second reviewing pass.

**E1. (Task Statement 4.5)** The team needs to moderate 50,000 listings a day without keeping a live interactive session open for each one. What's the appropriate mechanism?

A) Splitting the 50,000 listings across 50,000 separate human-supervised interactive sessions.
B) The Message Batches API (or an equivalent asynchronous batch-processing mechanism), designed specifically for large-volume, non-interactive processing rather than one live turn per item.
C) A single long-running interactive Claude Code session that processes all 50,000 listings sequentially in one conversation.
D) Batch processing isn't a real distinction; every listing must go through an individual live API turn regardless of volume.

**E2. (Task Statement 2.2)** The moderation tool that applies an action (remove listing, warn seller, no action) currently returns a bare `True`/`False`. What's the fix, consistent with this workshop's own tool-design discipline?

A) Log the actual outcome only server-side and continue returning an undifferentiated signal to the caller.
B) Return structured error/result metadata (a category, whether the action is retryable, a human-readable message) so a calling process can choose an appropriate response per outcome, not one undifferentiated signal.
C) Change the bare boolean to a bare integer instead, which carries the same amount of information either way.
D) Leave the tool as-is; a boolean is sufficient information for any downstream consumer.

**E3. (Task Statement 4.6)** A second pass spot-checks 5,000 of the day's flagged listings for reviewer accuracy, and review quality visibly degrades toward the end of each session. What's the most effective fix?

A) Continue the single long pass, since splitting it would only add overhead with no benefit.
B) Reduce the spot-check sample size to whatever a single pass can sustain at full attention, regardless of whether that sample is statistically meaningful.
C) Have the same reviewer redo the same single long pass a second time and average the two sets of findings.
D) Split the spot-check into multiple smaller, focused passes rather than one long continuous pass — the same attention-dilution problem large review workloads have, with the same fix.

**E4. (Task Statement 4.2)** The moderation prompt needs to reliably distinguish "spam" from "prohibited item" for genuinely ambiguous listings. What's the most direct way to improve reliability here?

A) Remove examples entirely and rely purely on an abstract category definition.
B) Increase the number of categories to cover every possible edge case individually.
C) Add a small number of concrete few-shot examples that specifically illustrate the ambiguous boundary cases, not just the clear-cut ones.
D) Add more clear-cut, unambiguous examples only, since ambiguous cases are inherently unteachable.

**E5. (Task Statement 2.3)** The moderation pipeline gives its single moderation agent access to a "ban seller account" tool alongside its listing-review tools, even though banning is a separate, rarer, higher-consequence action. What's the concern?

A) High-consequence tools should only ever be excluded entirely, never accessed by any agent regardless of scoping.
B) Broad, unscoped access to a high-consequence tool increases the chance of it being invoked outside its actual intended, narrower use — scoping tool access to what a role actually needs reduces this real risk.
C) There's no concern; giving one agent every available tool is always the safer default.
D) The concern is purely about performance overhead, not about correctness or safety.

**E6. (Task Statement 4.4)** A moderation category-extraction call occasionally returns a category string that isn't one of the pipeline's defined valid categories. What's the correct handling?

A) Silently map any unrecognized category to "no action" so the pipeline never has to handle the error.
B) Accept the invalid category string as-is and pass it downstream unchanged.
C) Fail the entire day's batch run if a single listing's category doesn't validate.
D) Validate the response against the defined category list and retry with the specific validation error fed back, rather than accepting an invalid category or silently coercing it to a default.

**E7. (Task Statement 2.4)** Multiple contributors work on the moderation pipeline's repository and need the same MCP tool configuration for the moderation tools. Where should this be configured?

A) Each contributor's personal, machine-local configuration, so individual differences don't conflict.
B) A `.claude/rules/` file, since MCP server configuration is the same kind of thing as a path-scoped convention.
C) A shared spreadsheet documenting the configuration in prose, with no machine-readable file at all.
D) A project-scoped `.mcp.json` at the repository root, checked into version control, so every contributor who clones the repo gets the same configuration automatically.

---

### Scenario F: a legacy-codebase documentation generator

A team builds a Claude Code setup meant to generate and keep up to date architecture docs and API references for a decade-old, sparsely-documented codebase — running project-specific checks and following the project's own conventions throughout.

**F1. (Task Statement 3.1)** A contributor's Claude Code session generating a new doc page isn't following the team's stated conventions, even though `CLAUDE.md` files exist in the repo. What's the most likely explanation, given this is the exact scenario Task Statement 3.1 itself uses?

A) `CLAUDE.md` conventions only take effect after the contributor's first pull request is merged.
B) The conventions were written in the wrong programming language for Claude Code to parse them.
C) The relevant `CLAUDE.md` is scoped to a directory the contributor isn't currently working in — config scope, not the mere existence of a `CLAUDE.md` somewhere in the repo, determines what's actually picked up.
D) Documentation-generation sessions are exempt from project conventions until the docs are fully published.

**F2. (Task Statement 3.2)** The team wants a reusable, documented way to teach Claude a specific multi-step procedure (e.g., "how to generate a new API reference page from a module's docstrings") that any contributor's session can invoke by name. What's the right mechanism?

A) A Claude Code skill — a structured, reusable capability definition, distinct from a one-off slash command meant for a single quick action.
B) A single giant `CLAUDE.md` entry describing the procedure in unstructured prose, with no way to invoke it by name.
C) A personal note the original author keeps in a private file no one else can access.
D) There is no mechanism for teaching a reusable multi-step procedure; each engineer must rediscover it independently every time.

**F3. (Task Statement 2.5)** A contributor wants to find every place in the large, unfamiliar codebase that calls a specific internal function, before documenting its signature as part of the API reference. Which built-in tool is the right first choice?

A) `Read`, opening every file in the codebase individually to check for the function name by hand.
B) `Grep`, searching file contents for the literal function name across the codebase — the purpose-built tool for exactly this task.
C) `Glob`, searching for files matching a naming pattern, which finds files by name, not by their contents.
D) `Bash` with a hand-rolled recursive shell search, which works but duplicates what the purpose-built tool already does more directly.

**F4. (Task Statement 3.3)** The team wants conventions for `tests/**` to differ from conventions for `src/**` within the same documentation-generator repo. What's the correct mechanism, and why not just one big `CLAUDE.md`?

A) A single rules file with no path scoping, since scoping only matters for repos larger than the documentation generator's own.
B) Separate path-scoped `.claude/rules/` files with frontmatter limiting each to its own glob — a single unscoped file can't express "this convention applies here, but not there" without relying on prose alone.
C) One repo-root `CLAUDE.md` covering both, since path scoping isn't something Claude Code configuration actually supports.
D) Two entirely separate Claude Code installations, one per directory.

**F5. (Task Statement 2.1)** The documentation generator has a `run_project_checks` tool and a `run_tests` tool with overlapping-sounding descriptions. Contributors' sessions sometimes call the wrong one. What's the most direct fix?

A) Make each tool's description state what specifically it checks and give a concrete example distinguishing when to use one over the other.
B) Rename both tools to start with the word "important" so the model is more careful selecting between them.
C) Remove one of the two tools entirely, even though they serve genuinely different purposes.
D) Leave the descriptions as-is and add a few-shot example to the system prompt instead.

**F6. (Task Statement 3.6)** The team wants the documentation generator's checks to also run automatically as part of every CI run, not just interactively. What enables this?

A) Non-interactive mode (`claude -p`/`--print`), which allows Claude Code to run in a CI pipeline and exit with output rather than waiting on a human.
B) There is no way to run Claude Code checks in CI; they can only ever be run by a human interactively.
C) Interactive mode works identically in CI, since CI runners can supply keyboard input the same way a terminal does.
D) A completely separate product would be required for any CI-facing use, distinct from Claude Code itself.

**F7. (Task Statement 2.5)** While updating a widely-referenced generated doc file, a contributor's `Edit` tool call fails because the target text isn't unique in the file. What's the correct fallback?

A) Give up on the edit entirely and ask a human to make the change manually.
B) Use `Read` to load the full file, then `Write` the corrected version back — the documented, reliable fallback exactly when `Edit`'s unique-anchor-text requirement can't be satisfied.
C) Retry the identical `Edit` call repeatedly until it happens to succeed by chance.
D) Switch to a `Bash` `sed` command instead, on the theory that shell text substitution has no uniqueness requirement and is therefore always safer.

---

## Answer key

**Do not scroll further until you've completed all 4 of your drawn scenarios closed-book and recorded your answers.**

### Scenario A

A1. **A.** A prompt instruction is advisory; only a programmatic hook actually guarantees the ordering. (B treats an unenforced instruction as equivalent to an enforced one. C draws a distinction the scenario doesn't support. D misunderstands defense in depth as redundancy.)
A2. **A.** Explicit format/boundary information in the description is the direct fix for tool-selection confusion. (B is not a real fix. C removes the distinction rather than clarifying it. D treats a tool-design problem as a prompting problem.)
A3. **B.** The rule constrains order and relationship across turns, which single-tool validation structurally can't express. (C denies the real distinction Task Statement 1.4 draws. D invents an arbitrary tool-count threshold. A misidentifies the distinction as organizational rather than technical.)
A4. **B.** Recording the disagreement with both sourced values is the conflicting-source-annotation requirement in practice. (C discards a potentially more current result for no reason. D treats a documentable disagreement as fatal. A fabricates a value neither source actually reported.)
A5. **B.** One shared error shape lets recovery logic generalize instead of special-casing per tool. (C denies a real, stated benefit. D narrows the benefit to one tool arbitrarily. A confuses error-shape standardization with input validation, which is a separate concern.)
A6. **B.** Unscoped access is a documented reliability risk, not a hypothetical one. (C asserts the opposite of the documented risk. D narrows the concern to one tool without basis. A miscategorizes a correctness concern as a performance one.)
A7. **A.** The signature's own shape rules out the unreliable-proxy anti-pattern structurally. (B treats a deliberate design choice as an oversight. C asserts confidence scores are reliable, contradicting the stated design rationale. D denies a design rationale the module states directly.)

### Scenario B

B1. **C.** CLAUDE.md hierarchy resolution is scope-sensitive; existence somewhere in the repo isn't the same as being picked up from every location. (D, A, B all invent rules Claude Code configuration doesn't actually have.)
B2. **A.** Explicit `null`/`None` distinguishes "genuinely unknown" from a real, established value — the same nullable-field discipline this workshop's own Module 02 review found and fixed. (B fabricates a value that was never actually established. C hides that the field exists in the schema at all. D over-corrects into failing on a legitimately optional field.)
B3. **D.** Path-scoped rules files are exactly the mechanism for differing conventions by directory within one repo. (A relies on the model's judgment where a technical mechanism exists instead. B invents an unnecessary, costly workaround. C discards the actual mechanism that solves this.)
B4. **D.** Feeding back the specific validation error is the retry-loop discipline this workshop's own extraction module establishes; the alternatives fabricate or discard a real requirement. (A accepts what the schema says is invalid. B repeats a failed attempt with no new information. C discards a real, stated requirement rather than fixing the failure.)
B5. **C.** Iterative refinement means using concrete failure feedback to revise, not restarting blindly or repeating unchanged. (D abandons the current approach without using the failure's information. A bypasses Claude's own ability to revise. B repeats an already-failed attempt with no change.)
B6. **A.** Explicit output-field criteria in the prompt is the direct way to reliably get a specific structured format. (B leaves the format to chance. C hides the requirement from the model entirely. D relies on an unstated, unreliable assumption about general training.)
B7. **C.** Non-interactive mode is exactly the mechanism CI runners need — produce output and exit rather than waiting on input. (D reverses which mode actually enables CI use. A denies a real, existing capability. B invents an unnecessary second tool.)

### Scenario C

C1. **A.** `stop_reason` is the documented, authoritative completion signal; text-parsing is the named anti-pattern. (B is the anti-pattern itself. C substitutes an arbitrary count for the real signal. D conflates one tool call with actual completion.)
C2. **C.** A hook intercepting before execution is what actually guarantees a destructive action never runs, regardless of model behavior. (D and A both rely on unenforced trust. B is a disproportionate response that removes needed capability instead of gating it.)
C3. **D.** Over-fragmenting a task with real cross-file dependencies adds coordination overhead without adding real specialization. (A ignores the coordination cost. B narrows the concern arbitrarily. C asserts a "best practice" the scenario's own dependencies argue against.)
C4. **C.** Resuming preserves already-completed, valid work instead of discarding it for no reason tied to actual risk. (D and A both discard valid progress unnecessarily. B describes an avoidable failure mode, not a correct design.)
C5. **D.** A project-scoped, version-controlled slash command is exactly the shared, repeatable mechanism the team needs. (A, B, and C all fail to provide something every contributor automatically gets.)
C6. **C.** Plan Mode's review-before-execution property is precisely suited to a high-blast-radius change. (D ignores the stated risk. A draws an arbitrary category exclusion. B denies a real difference in risk exposure between reviewing first and executing directly.)
C7. **D.** Subagents start with a fresh context window and need context explicitly passed to them — the same discipline this workshop's own tool docstrings (e.g., `escalate_to_human`'s required summary) already establish. (A claims an automatic sharing mechanism that doesn't exist. B overcorrects into "subagents can never receive context," which isn't true either. C invents a distinction based on definition style that isn't the actual mechanism.)

### Scenario D

D1. **D.** Surfacing the disagreement with attribution is the conflicting-source-annotation requirement; the alternatives all hide a real signal. (A and B both silently resolve a disagreement a reader needs to see. C discards real information rather than surfacing the conflict.)
D2. **C.** Synthesis and reconciliation across already-produced results is a distinct coordination role a single subagent's narrower retrieval task doesn't perform. (D duplicates work unnecessarily. A discards two-thirds of legitimately gathered information. B denies a real distinction in role.)
D3. **C.** A subagent's result returns to the coordinator as a tool result, the same shape as any other tool call's output. (D, A, and B all invent mechanisms that aren't how subagent results are actually returned.)
D4. **B.** Treating one subagent's failure independently preserves the two subagents' real, valid results instead of discarding them. (C and D both discard good work unnecessarily. A fabricates success that didn't happen, hiding a real failure.)
D5. **C.** A structured, persistent fact record — not hoping summarization preserves everything — is the reliable approach for facts that must survive. (D overstates summarization's reliability. A narrows the risk to numeric facts without basis. B over-corrects into an impractical absolute the scenario doesn't require.)
D6. **D.** A programmatic check guarantees the ordering regardless of model behavior; a prompt instruction is advisory and can be violated. (A claims an equivalence the whole point of enforcement design argues against. B denies that ordering rules can be enforced programmatically, which they demonstrably can. C denies a real reliability difference between the two mechanisms.)
D7. **A.** Textual uncertainty cues are an unreliable, unverifiable proxy, unlike a real structured signal such as an unresolved conflict. (B asserts the opposite of the documented concern. C draws an arbitrary, unsupported distinction. D proposes replacing a reliable signal with the very proxy the question identifies as unreliable.)

### Scenario E

E1. **B.** Asynchronous batch processing is the mechanism designed specifically for large, non-interactive volume. (C is impractical and doesn't match the actual need. D denies a real, meaningful distinction in processing mode. A is a wildly inefficient, impractical substitute.)
E2. **B.** Structured result metadata lets a caller choose an appropriate response per outcome, the same principle this workshop's own tool-error discipline establishes. (C changes the shape without adding real information. D accepts an undifferentiated signal as sufficient when it isn't. A withholds exactly the detail a caller needs to act correctly.)
E3. **D.** Splitting into smaller, focused passes is the documented fix for attention dilution across a large review workload. (A ignores the documented degradation. B discards meaningful coverage rather than fixing the underlying cause. C repeats the same flawed process instead of addressing it.)
E4. **C.** Concrete examples illustrating the actual ambiguous boundary are what improve reliability exactly where the model struggles. (D avoids the cases that actually need addressing. A removes a proven fix entirely. B solves a different problem than the one described.)
E5. **B.** Broad tool access is a documented reliability risk when a tool's consequences are high and its use should be narrow. (C asserts the opposite of the documented risk. D misidentifies a safety concern as a performance one. A is a disproportionate response given that scoped access is the actual, more measured fix.)
E6. **D.** Validating against the defined category list and retrying with the specific error is the same discipline this workshop's own extraction module establishes. (A silently miscategorizes rather than fixing the actual problem. B passes invalid data downstream unchanged. C is a disproportionate response to one listing's failure.)
E7. **D.** A project-scoped, version-controlled `.mcp.json` is the documented mechanism for shared, consistent configuration across contributors. (A is for personal, not shared, configuration — the opposite of what's needed. B conflates two unrelated configuration mechanisms. C abandons machine-readable configuration entirely.)

### Scenario F

F1. **C.** Config scope, not mere existence somewhere in the repo, determines what's actually picked up — the exact framing Task Statement 3.1 itself uses. (D, A, and B all invent rules that don't reflect how Claude Code configuration scope actually works.)
F2. **A.** A skill is the structured, reusable, invoke-by-name mechanism for a multi-step procedure, distinct from a one-off slash command. (B provides no reusable, invokable structure. C isn't shared with anyone else. D denies a real, existing mechanism.)
F3. **B.** `Grep` searches file contents for a literal string — exactly this task. (C searches file names, not contents. D duplicates a purpose-built tool's exact function with an unnecessary extra layer. A is correct in principle but wildly inefficient.)
F4. **B.** Path-scoped rules files are exactly the mechanism for differing conventions by directory in one repo. (C denies a real, existing capability. D is an unnecessary, costly workaround. A draws an arbitrary size threshold that doesn't reflect why scoping matters.)
F5. **A.** Explicit, distinguishing descriptions are the direct fix for tool-selection confusion between similarly-described tools. (B is not a real fix. C removes a tool that serves a genuinely different purpose. D treats a tool-design problem as a prompting problem instead.)
F6. **A.** Non-interactive mode is what allows Claude Code to run in CI and exit with output rather than waiting on a human. (B denies a real, existing capability. C reverses which mode actually enables CI use. D invents an unnecessary separate product.)
F7. **B.** Read-then-Write is the documented, reliable fallback exactly when `Edit`'s unique-anchor-text requirement can't be satisfied. (C doesn't address the actual cause of the failure. D swaps a safer, purpose-built tool for a less precise one under a false safety claim. A abandons a solvable problem unnecessarily.)

---

*Mock exam authored 2026-07-16, alongside Module 06's hands-on capstone exercise, both built together. Scoring: (correct answers across your 4 drawn scenarios ÷ total questions across those 4 scenarios) × 1000; 720/1000 to pass.*
