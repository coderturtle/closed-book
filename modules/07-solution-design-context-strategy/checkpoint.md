# Module 07 closed-book checkpoint

**Format:** 14 questions, 20 minutes, 80% (12/14, rounded up) to pass. Multiple choice, one correct answer, three distractors.

**Before you start:** close or minimize your Claude Code session. No notes, no AI assistance, no searching. See [`docs/design-tension.md`](../../docs/design-tension.md).

**Citation note, stated honestly:** CCAR-P's own exam guide doesn't enumerate Domain 1/Domain 2 into the same granular decimal task-statement numbering CCA-F's domains used (Task Statement 1.1, 1.2, and so on) — at least not in the primary-source material this workshop's design phase actually read. Questions below are cited by each domain's own named objective instead (e.g., "Domain 1: architectural pattern selection"), drawn directly from `docs/workshop-design.md`'s own listed objectives for these two domains, rather than inventing a numbering scheme this project can't actually verify against the real guide. This is a deliberate, disclosed difference from every Part 1 checkpoint's citation style, not an oversight.

**Coverage note:** this checkpoint carries full coverage of both domains' named objectives (4 under Domain 1, 4 under Domain 2). The hands-on exercise's artifact (the Helpdesk ticket-triage classifier and its ADR) verifies architectural pattern selection and context/token optimization (prompt-reuse/cache-friendliness) directly, against exactly one scenario. The remaining objectives — and pattern selection/context strategy against *different* scenarios, since a single hands-on artifact can't demonstrate judgment across every kind of request Foundry might receive — are tested here instead, using two new scenarios your hands-on work hasn't already walked you through.

**Originality note:** every question is written originally against the objective it tests — none are copied or reworded from Anthropic's real exam, any leaked item bank, or Anthropic's own official sample questions (the exam guide's own Sample Question 2, about a repeatedly-sent 8,000-token system prompt, is used only as a style/difficulty anchor for this module's design, per `docs/workshop-design.md` — never copied into a question here).

---

## Scenarios

**Scenario 1 (reused from your hands-on work): the Helpdesk team's ticket triage,** covered in `fixtures/foundry/`.

**Scenario 2: the Sales Engineering team** wants a tool that drafts custom RFP (request-for-proposal) responses by pulling relevant language from a large corpus of ~600 past proposals, tailored to each new prospect's specific requirements list.

**Scenario 3: the Security team** wants a system that triages incoming security alerts and, for a confirmed subset, takes multi-step remediation action across several internal systems (revoking a credential, isolating a host, opening an incident ticket) — a genuinely different kind of request from Scenario 1's.

---

## Questions

**1. (Domain 1: translating business problems into solutions)** The Sales Engineering team's actual request is "give us an AI that writes RFP responses." Before proposing any architecture, what's the most important next step?

A) Start building immediately with the most capable available model, since more capability can only help a drafting task.
B) Clarify what "good" actually means to this team — is a draft that still needs heavy human editing acceptable, or do they need something closer to submission-ready, and what's the real cost of a wrong or fabricated claim in a submitted RFP — before any architecture or model choice is made.
C) Reuse the Helpdesk team's exact `classify_ticket` architecture, since it already works for one internal team.
D) Ask the Sales Engineering team to write their own technical specification before Foundry does any design work.

**2. (Domain 1: translating business problems into solutions)** The Security team says they want the alert-triage system to "act autonomously to remediate threats." Why is this stated request not yet enough information to start designing?

A) It is enough information; "act autonomously" is a complete architectural specification on its own.
B) "Autonomously" conflates several different real decisions (which actions require human approval versus which can execute unattended, what the acceptable false-positive rate is for an unattended action, what the blast radius of a wrong remediation looks like) that a Foundry architect must actually pin down with the team, not infer from one adjective.
C) The request should be rejected outright, since no security-relevant action should ever be automated.
D) The word "autonomously" should simply be removed from the request and the system built as a fully manual tool instead, without checking whether that still meets the team's actual need.

**3. (Domain 1: end-to-end architecture design)** For the Sales Engineering RFP tool, what does "end-to-end" architecture design require beyond picking a model and writing a prompt?

A) Nothing more; model choice and prompt design are the entire architecture for any Claude-based tool.
B) Only the prompt matters; model selection is a minor implementation detail.
C) Deciding how the ~600-proposal corpus is actually retrieved and supplied to the model (e.g., a retrieval step feeding relevant excerpts into context, versus some other mechanism), how a draft response is reviewed and delivered back to the requesting salesperson, and where each of those steps can fail — the full path from request to delivered artifact, not just the model call in the middle.
D) End-to-end design is only relevant for agentic systems, not for single-call drafting tools.

**4. (Domain 1: end-to-end architecture design)** The Security team's remediation actions (revoking credentials, isolating hosts) touch systems outside Foundry's own control. What does end-to-end design require Foundry to account for that a self-contained tool like the Helpdesk classifier didn't need to?

A) Nothing different — every Claude-based system has the same integration surface regardless of what its actions actually touch.
B) Real integration points with each external system (their own APIs, their own failure modes, their own authorization requirements) and what happens when one of those systems is unreachable or rejects the action mid-remediation — failure modes with no analogue in a system that only classifies and routes.
C) End-to-end design is unnecessary here since the actions are automated and therefore self-verifying.
D) The external systems' own reliability is entirely someone else's problem and out of scope for Foundry's architecture.

**5. (Domain 1: architectural pattern selection)** Which of the three scenarios most clearly warrants an agentic architecture (multi-step, tool-using, autonomous-within-bounds), and why?

A) Scenario 1 (Helpdesk triage) — because it's the most familiar example, regardless of its actual task shape.
B) Scenario 2 (RFP drafting) — because it involves a large corpus, and large corpora always require agentic retrieval loops.
C) Scenario 3 (Security remediation) — because it genuinely requires multi-step, causally dependent actions across several external systems, with real decisions about ordering and conditional escalation partway through, unlike Scenario 1's single-turn classification or Scenario 2's single-pass drafting.
D) None of the three — every one of these problems is better solved without Claude, using traditional rule-based automation instead.

**6. (Domain 1: architectural pattern selection)** A contributor argues Scenario 2 (RFP drafting) should also use a full agentic loop, "to be consistent with Scenario 3." What's the flaw in that reasoning?

A) There's no flaw; architectural consistency across unrelated internal teams' tools should always be the top priority.
B) Pattern selection should be driven by each problem's own actual shape (does it need multi-step, causally-dependent tool use with real intermediate decisions, or not) — not by matching whatever pattern a different, unrelated request happened to need. Scenario 2 is fundamentally a retrieval-and-drafting task, not a multi-step action-taking one.
C) The flaw is only that Scenario 2 needs an even more complex architecture than Scenario 3, not a simpler one.
D) Consistency doesn't matter at all, so any pattern would be equally defensible for any scenario for any reason.

**7. (Domain 1: multi-agent orchestration strategy)** If Scenario 3's remediation system is built with multiple specialized subagents (one per external system it touches), what real design question does that raise which a single-coordinator system wouldn't?

A) None — subagents are a pure implementation detail invisible to the overall architecture.
B) How results and partial failures from each subagent are reconciled by a coordinator, and what context each subagent actually needs passed to it explicitly (subagents don't inherit a coordinator's context automatically) — real orchestration decisions with no analogue in Scenario 1's single-call classifier.
C) Multi-agent systems never need a coordinator at all; each subagent should act fully independently with no reconciliation.
D) The only design question multi-agent orchestration raises is which programming language each subagent should be written in.

**8. (Domain 1: multi-agent orchestration strategy)** For Scenario 3, a contributor proposes a single subagent that handles credential revocation, host isolation, AND incident-ticket creation, reasoning "it's simpler to have one subagent do everything remediation-related." What's the concern?

A) There's no concern; broader subagent scope is always simpler and therefore always better.
B) Bundling three actions with different systems, different failure modes, and different authorization requirements into one subagent trades away the same scoping benefit Module 03's tool-design discipline already established for individual tools — a narrower, more specialized subagent is easier to reason about, test, and scope permissions for than one that does everything.
C) The concern only applies if the three actions are performed in a specific order.
D) Subagent scope has no bearing on permissioning or failure isolation, only on code organization.

**9. (Domain 2: model selection trade-offs)** The Helpdesk classifier uses a smaller, cheaper model tier by design (see its own ADR). Under what condition would that choice need revisiting, consistent with sound model-selection reasoning?

A) Never — once a model tier is chosen for a task, it should never be reconsidered regardless of what changes.
B) Only if a competitor happens to announce a new model, regardless of whether Foundry's own accuracy or cost data shows a real problem.
C) If real measured accuracy on the actual ticket distribution (not a hypothetical) showed the smaller model materially underperforming on a category that matters, or if per-ticket cost/latency requirements changed — a data-driven trigger tied to the system's actual measured behavior, not habit or trend-following.
D) The choice should be revisited on a fixed calendar schedule regardless of any evidence about actual performance.

**10. (Domain 2: model selection trade-offs)** For Scenario 2 (RFP drafting), what's a defensible reason to choose a more capable model tier than the Helpdesk classifier's, even though both are Claude-based tools?

A) More capable models are always the correct default choice for every task, with no task-specific reasoning required.
B) RFP drafting requires synthesizing relevant language across a large, varied corpus into a coherent, accurate, submission-adjacent document — a harder generation task than five-way classification, where a wrong or fabricated claim has real business consequences (a proposal representing something untrue to a prospect), justifying the added cost and latency of a more capable tier.
C) The Sales Engineering team asked for it by name, which is sufficient justification on its own regardless of the actual task's needs.
D) Model tier should be chosen based only on which team is more senior within the company, not on the task's actual demands.

**11. (Domain 2: system prompt/guardrail design)** For Scenario 3's remediation system, what guardrail belongs in the system prompt (or an equivalent programmatic control) given the stakes of the actions involved?

A) No guardrails are needed if the model is capable enough — capability alone is a sufficient substitute for explicit constraints.
B) An explicit, structural rule about which actions require human approval before executing versus which may proceed unattended — mirroring the same "a rule this consequential belongs in an enforced mechanism, not just careful prompting" discipline `resolve`'s own hook-versus-prompt-instruction lesson (Module 04) already established, now applied to a security-remediation context instead of a refund.
C) Guardrails are a Domain 5 (governance) concern exclusively and have no place in Domain 2's system prompt design at all.
D) The only necessary guardrail is a length limit on the system prompt itself.

**12. (Domain 2: system prompt/guardrail design)** The Helpdesk classifier's system prompt explicitly instructs: prefer "other" with low confidence over guessing between two plausible categories. What real design principle does this instruction encode?

A) It has no real design purpose; it's arbitrary boilerplate that could be removed without consequence.
B) A calibrated "I'm not sure" signal (routed to a human) is more useful downstream than a confident-sounding guess that's actually wrong — the same anti-fabrication discipline Module 02's own extraction design (nullable fields, honest "unknown" rather than a fabricated default) already established, here expressed as a system-prompt instruction rather than a schema constraint.
C) The instruction exists purely to make the system prompt longer, which improves classification accuracy regardless of content.
D) This instruction should be removed since "other" is a lower-value category than the four specific ones.

**13. (Domain 2: context/token optimization)** Scenario 2's RFP tool needs to draw on a ~600-proposal corpus, far too large to fit in any single context window. What's the most direct approach to context/token optimization here?

A) Use the largest available context window and attempt to include the entire 600-proposal corpus in every call regardless of relevance.
B) Retrieve only the subset of past proposals actually relevant to the new prospect's specific requirements (a retrieval step ahead of the generation call) rather than paying for and diluting context with the full corpus on every request — the same "only pay for what's actually needed in context" discipline that motivates the Helpdesk classifier's own static, minimal system prompt.
C) Context/token optimization is irrelevant once a large enough model tier is chosen.
D) Reduce the corpus to a single "average" proposal template and use that for every RFP regardless of the prospect's actual requirements.

**14. (Domain 2: prompt-reuse strategy)** The Helpdesk classifier's system prompt is designed to be byte-identical across every call, including retries — a deliberate prompt-reuse/caching strategy. Why does this same property matter *less* for Scenario 2's RFP drafting tool, even though both are real Claude-based systems Foundry built?

A) It doesn't matter less; every Claude-based system must have a byte-identical system prompt across every call, with no exceptions.
B) Prompt-reuse/caching pays off specifically when a large, static prefix is genuinely reused unchanged across a high volume of similar calls (the Helpdesk classifier's ~4,000 tickets/month against one fixed policy prompt); Scenario 2's per-prospect retrieved context is, by the nature of the task, different on every call, so there's no equivalent static prefix to cache in the first place — the strategy's value depends on the task's actual call pattern, not on applying it uniformly everywhere.
C) Caching strategy is a Domain 1 concern, not a Domain 2 one, so it doesn't apply to either scenario.
D) The RFP tool should be redesigned specifically to force a cacheable prompt, even at the cost of losing per-prospect relevance, since caching is always the higher priority.

---

## Answer key

**Do not scroll further until you've answered all 14 questions closed-book and recorded your answers.**

1. **B.** Clarifying the real acceptance bar and the cost of a wrong output is the necessary first step before any architecture commitment. (A treats capability as a substitute for actually understanding the requirement. C reuses an unrelated architecture without checking fit. D shifts Foundry's own design responsibility onto the requesting team.)
2. **B.** "Autonomously" bundles several real decisions that must be made explicit before design starts. (A treats an ambiguous adjective as a complete spec. C over-corrects into a blanket rejection the scenario doesn't warrant. D discards the team's actual need instead of clarifying it.)
3. **C.** End-to-end design covers the full path from request to delivered artifact, including retrieval and delivery, not just the model call. (A and B both collapse "architecture" into "prompt," missing the rest of the system. D draws an arbitrary distinction between agentic and non-agentic systems that isn't real.)
4. **B.** Real external integration points and their own failure modes are exactly what end-to-end design must account for once a system's actions leave its own boundary. (A denies a real difference in integration surface. C wrongly assumes automation implies self-verification. D abdicates a real design responsibility.)
5. **C.** Scenario 3's genuinely multi-step, causally-dependent, cross-system actions are the actual shape that warrants an agentic pattern — the same reasoning `resolve`'s own architecture in Part 1 was built on. (A and B both justify pattern choice by superficial factors — familiarity and corpus size — rather than the task's real structure. D dismisses all three problems without engaging their actual shape.)
6. **B.** Pattern selection is driven by each problem's own real shape, not artificial consistency with an unrelated request. (A elevates consistency over fit. C misjudges the direction of the comparison. D denies that pattern choice has any real justification at all, which the module's own hands-on exercise directly contradicts.)
7. **B.** Result reconciliation and explicit context-passing are real orchestration decisions unique to multi-agent design. (A denies these are real architectural concerns. C proposes discarding coordination entirely, which the scenario's own dependencies argue against. D trivializes the question into an unrelated implementation detail.)
8. **B.** Narrower subagent scope carries the same benefit Module 03 already established for tool scoping — easier reasoning, testing, and permissioning. (A asserts broader scope is strictly better, the opposite of the documented risk. C narrows the concern to an irrelevant detail. D denies a real connection between scope and permissioning that the scenario's own stakes make concrete.)
9. **C.** A data-driven trigger tied to real measured performance or changed requirements is the sound basis for revisiting a model choice. (A and D both substitute an arbitrary rule for actual evidence. B chases trends instead of evidence.)
10. **B.** The harder generation task and the real cost of a wrong or fabricated claim justify a more capable tier here, in a way the simpler five-way classification task doesn't. (A treats capability as a context-free default. C substitutes organizational status for task-based reasoning. D is an arbitrary, indefensible criterion.)
11. **B.** An explicit, enforced human-approval boundary for consequential actions is the same programmatic-enforcement lesson Module 04 already established, applied to a new domain. (A treats capability as a substitute for explicit constraints, the same mistake Module 04's own doubt-driven-development review found and fixed. C artificially separates two closely related concerns. D trivializes guardrail design into an unrelated constraint.)
12. **B.** A calibrated "unsure, escalate" signal beats a confident wrong guess — the same anti-fabrication principle Module 02 established, here in prompt form. (A dismisses a real, purposeful design choice as arbitrary. C misattributes the instruction's function to prompt length. D undervalues the deliberate fail-open path this instruction protects.)
13. **B.** Retrieving only the relevant subset directly addresses both cost and relevance, the same "don't pay for context you don't need" principle behind the Helpdesk classifier's own static, minimal prompt. (A pays maximal cost for minimal relevance. C denies optimization matters once model tier is large enough, which isn't true. D discards the per-prospect relevance the task actually requires.)
14. **B.** Caching pays off specifically for a static prefix reused across high call volume; a task whose context is different on every call has no equivalent static prefix to cache, so the same strategy doesn't transfer uniformly. (A wrongly universalizes a context-dependent strategy. C misassigns the concern to the wrong domain. D sacrifices the task's actual value (per-prospect relevance) to satisfy a strategy that doesn't fit it.)

---

*Checkpoint authored 2026-07-17, alongside Module 07's hands-on tier, both built together from the start.*
