# Module 09 closed-book checkpoint

**Format:** 14 questions, 20 minutes, 80% (12/14, rounded up) to pass. Multiple choice, one correct answer, three distractors.

**Before you start:** close or minimize your Claude Code session. No notes, no AI assistance, no searching. See [`docs/design-tension.md`](../../docs/design-tension.md).

**Citation note:** as with Modules 07 and 08's checkpoints, CCAR-P's exam guide doesn't enumerate Domain 5/6/7 into a granular decimal task-statement scheme in the primary-source material this workshop's design phase actually read — confirmed by search, not assumed. Questions are cited by each domain's own named objective instead, grouped from the objectives listed in `docs/workshop-design.md`.

**Coverage note:** the hands-on exercise's artifacts (`governance.py`'s human-in-the-loop gate, `shipping-readiness-review.md`, `.claude/` team tooling) directly verify human-in-the-loop strategy, stakeholder communication, and team tooling configuration against exactly one scenario (the Platform Docs team's own shipping decision). This checkpoint carries the remaining objectives — guardrails, risk/failure-mode identification, regulatory compliance, ethical AI considerations, structured discovery, SLA management, architecture documentation, lifecycle-phase support, debugging/operational support — plus re-tests judgment on the hands-on objectives against two new scenarios.

**Originality note:** every question is written originally against the objective it tests — none are copied or reworded from Anthropic's real exam, any leaked item bank, or Anthropic's own official sample questions.

---

## Scenarios

**Scenario 1 (reused from your hands-on work): the Platform Docs team's `doc_qa` system**, shipping decision covered in `fixtures/foundry/`.

**Scenario 2: the Data Science team** wants to build a Claude-based tool that summarizes customer support tickets, some of which contain EU customers' personal data — a real GDPR-relevant scenario.

**Scenario 3: the Growth team** is launching a customer-facing Claude-based agent under a hard SLA (sub-2-second response commitment to the business), and needs to onboard 12 engineers across 3 sub-teams onto it after launch.

---

## Questions

**1. (Domain 5: guardrails)** For Scenario 2, a contributor proposes handling GDPR concerns entirely through a written data-handling policy, with no code changes to the summarization tool itself. What's the gap in that approach?

A) There is no gap; a written policy is always sufficient for regulatory compliance regardless of what the code actually does.
B) A policy that isn't enforced by the system itself relies entirely on every future engineer reading and following it correctly — the same "a rule this consequential belongs in an enforced mechanism, not just documentation" principle Module 09's own governance gate applies to sensitive content, and Part 1's `resolve` hook applied to refund authorization.
C) GDPR only applies to databases, never to model calls, so no guardrail is needed here at all.
D) Guardrails are exclusively a Domain 7 concern and have no bearing on regulatory compliance.

**2. (Domain 5: risk/failure-mode identification)** For Scenario 1's `doc_qa` system, which of the following is a real, already-identified failure mode distinct from the sensitive-content risk Module 09's own exercise addresses?

A) The system might become too popular with employees, which is not a real risk worth documenting.
B) Stale retrieval — a document revision that isn't correctly re-indexed leaves the system confidently answering from a superseded procedure, the exact failure mode Module 08's `refresh_index` exercise was built around.
C) There is no other failure mode; sensitive-content exposure is the system's only real risk.
D) The system could fail by being too fast, which is never a real operational risk.

**3. (Domain 5: human-in-the-loop strategy)** Why does Module 09's own `governance.py` check retrieved content for sensitivity *before* calling `model_client`, rather than checking the model's *response* afterward?

A) Checking before or after makes no real difference to the compliance outcome.
B) Checking beforehand means sensitive content never reaches the model call at all if flagged — checking only the response afterward would mean the sensitive content has already left the system's boundary by the time a problem is detected, even if the final output is correctly withheld.
C) The model's response is always identical to its input, so checking either point produces the same result.
D) Human-in-the-loop strategy only applies to the final output stage, never to inputs.

**4. (Domain 5: regulatory compliance)** For Scenario 2, what real architectural question does GDPR raise beyond "do we have a privacy policy"?

A) None; a privacy policy fully satisfies every GDPR obligation regardless of system design.
B) Whether customer PII genuinely needs to be included in what's sent to a model call at all for the summarization task to work, and if so, what retention/deletion guarantees apply to that data once it's part of a request — real, system-level questions a policy document alone doesn't answer.
C) GDPR only applies to companies headquartered in the EU, so a Data Science team elsewhere has no real obligation to consider it.
D) The question is purely legal and has no architectural consequence of any kind.

**5. (Domain 5: ethical AI considerations)** For Scenario 2's ticket-summarization tool, what's a real ethical consideration distinct from the GDPR compliance question already raised?

A) There is no separate ethical question once GDPR compliance is satisfied; legal compliance and ethical design are identical.
B) Whether a summary could omit or distort details in a way that changes how a support agent treats the customer (e.g., summarizing away a customer's stated urgency or frustration) — a real quality/fairness concern independent of whether the data-handling itself is legally compliant.
C) Ethical AI considerations only apply to consumer-facing products, never to internal tooling.
D) The only ethical consideration is whether the tool is popular with the team using it.

**6. (Domain 5: risk/failure-mode identification)** For Scenario 3's SLA-bound agent, what's a real risk specifically introduced by the sub-2-second response commitment?

A) None; a stricter latency requirement never introduces new risk, only new cost.
B) Pressure to skip or shortcut real safety/governance checks (like a human-in-the-loop gate) in order to hit the SLA, trading a documented risk for a speed guarantee — a real tension worth naming explicitly rather than discovering after a latency-driven shortcut ships.
C) The SLA guarantees the system will never fail, so no risk analysis is needed once it's in place.
D) Response-time commitments are a Domain 6 concern exclusively and have no Domain 5 risk implications.

**7. (Domain 6: structured discovery)** Before building Scenario 3's agent, what does a real structured discovery pass need to establish beyond "the SLA is 2 seconds"?

A) Nothing further; the SLA number alone is a complete requirements specification.
B) What "acceptable" actually means to the business if the SLA is occasionally missed under real load, which failure modes are tolerable versus which require a hard stop, and which of the 3 sub-teams' own workflows the agent needs to support on day one versus later — real requirements a single number doesn't capture.
C) Structured discovery is unnecessary once a numeric SLA has been agreed upon by any party.
D) The only thing left to establish is which programming language to use.

**8. (Domain 6: stakeholder communication)** Module 09's own shipping-readiness review names a real trade-off in its Stakeholder Summary: the sensitivity gate adds latency to a minority of queries. Why does stating this trade-off explicitly matter more than just shipping the gate silently?

A) It doesn't matter; stakeholders never need to know about trade-offs that don't affect the majority of queries.
B) An undisclosed trade-off discovered later (a stakeholder noticing some queries are slower without knowing why) damages trust in a way that the same trade-off, disclosed up front with its reasoning, does not — the same "state the honest cost, not just the benefit" discipline every prior module's own ADR/review documents have applied.
C) Stakeholder communication is only required for trade-offs that affect 100% of usage.
D) The trade-off should be hidden specifically because disclosing it might cause the stakeholder to object.

**9. (Domain 6: stakeholder communication / SLA management)** For Scenario 3, the agent occasionally exceeds the 2-second SLA during peak load. What's the right first step in managing this with the business stakeholder who owns the SLA commitment?

A) Say nothing and hope the business doesn't notice, since raising it might create a difficult conversation.
B) Bring real data (how often, by how much, under what conditions) and a stated set of options with real trade-offs (more infrastructure cost, a narrower feature set at peak, a renegotiated SLA) — rather than either hiding the miss or promising a fix without knowing if one is actually feasible.
C) Immediately promise the SLA will never be missed again, regardless of whether that's actually achievable.
D) SLA management is purely a Domain 5 governance concern and doesn't involve stakeholder communication at all.

**10. (Domain 6: architecture documentation)** What distinguishes a real architecture document (like Module 09's own shipping-readiness review, or Module 07's ADR) from a status update that just says "the system is done and working"?

A) Nothing; both serve exactly the same purpose for exactly the same audience.
B) A real architecture document states what was decided, why, what alternative was rejected and why, and what the decision honestly costs — a status update states only that something exists, with none of the reasoning a future reader (or a stakeholder deciding whether to approve a change) would actually need.
C) Architecture documents are only required for systems that have already failed at least once.
D) A status update and an architecture document differ only in length, not in content.

**11. (Domain 6: lifecycle-phase support)** For Scenario 3, once the agent has been live for 3 months, what real lifecycle-phase concern applies that didn't exist at launch?

A) None; once a system launches successfully, no further lifecycle concern exists until it's fully decommissioned.
B) Whether the original discovery assumptions (which sub-teams' workflows mattered most, what "acceptable" latency meant) still hold as real usage patterns emerge, and whether the governance gates configured at launch still match the system's actual current risk profile as it's extended.
C) Lifecycle-phase support is exclusively about performance tuning and has no connection to the original discovery or governance decisions.
D) The only lifecycle concern after launch is choosing when to decommission the system entirely.

**12. (Domain 6: stakeholder communication)** For Scenario 2, how should the Data Science team communicate the architectural consequence of GDPR (limiting what customer data enters a model call) to a non-technical product stakeholder who just wants the summarization feature to work well?

A) Use only technical terms (tokens, context windows, model calls) and assume the stakeholder will look them up if they care enough.
B) Frame the real trade-off in terms the stakeholder actually needs to decide on — what the feature can and can't do as a result, and why — not just report that "a compliance requirement was addressed" without explaining what changed for the product.
C) Don't communicate it at all, since compliance decisions don't need product stakeholder input.
D) Tell the stakeholder the feature is unaffected, even if it genuinely is, to avoid a difficult conversation.

**13. (Domain 7: team tooling configuration)** Module 09's own `.claude/rules/src.md` documents a convention (deterministic test doubles only, never a real model API call from source code). Why does this belong in team-wide `.claude/` configuration rather than just being something the original author remembers?

A) It doesn't need to be documented anywhere; every future engineer will naturally follow the same convention without being told.
B) Team-wide tooling configuration is specifically for conventions a new engineer, unfamiliar with the codebase's history, needs to know but can't infer from the code alone — the same "team-wide, not personal" distinction Domain 7's own objective names explicitly.
C) `.claude/rules/` files are purely cosmetic and have no bearing on what a new engineer actually needs to know.
D) This kind of convention is better left undocumented so each engineer can independently rediscover it.

**14. (Domain 7: debugging/operational support)** For Scenario 3, a sub-team reports the agent "sometimes gives a weird answer" three weeks after launch, with no further detail. What's the most useful team-tooling investment to make this kind of report actionable going forward?

A) Nothing; vague reports like this can never be made more actionable regardless of tooling.
B) Structured logging/observability that captures enough of the actual request (query, retrieved context, which governance path was taken) that a "weird answer" report can be traced to a specific, reproducible case — turning a vague report into a debuggable one.
C) Require every sub-team to become expert Python debuggers before they're allowed to report issues.
D) Operational support tooling is a Domain 5 governance concern exclusively and has no real connection to debugging.

---

## Answer key

**Do not scroll further until you've answered all 14 questions closed-book and recorded your answers.**

1. **B.** An unenforced policy depends on every future engineer following it correctly — the same enforced-mechanism principle this project has applied consistently since Part 1's own refund-authorization hook. (A and C both dismiss the real gap. D draws an arbitrary domain boundary the scenario doesn't support.)
2. **B.** Stale retrieval is a real, already-identified failure mode from Module 08's own exercise, distinct from sensitive-content exposure. (A and D both treat non-issues as risks or non-risks arbitrarily. C wrongly claims sensitivity is the only risk.)
3. **B.** Checking beforehand keeps sensitive content from ever reaching the model call; checking only the response leaves a real exposure window even if the final output is correct. (A denies a real, meaningful difference. C is factually false. D mischaracterizes where human-in-the-loop strategy can apply.)
4. **B.** Real architectural questions about whether PII needs to be sent at all, and what retention/deletion guarantees apply, go beyond a policy document. (A and D both understate GDPR's real architectural reach. C is a common but incorrect scoping assumption about GDPR's applicability.)
5. **B.** A summary that distorts urgency or tone is a real quality/fairness concern distinct from legal data-handling compliance. (A collapses two genuinely separate concerns into one. C and D both draw arbitrary, unsupported scope limits.)
6. **B.** SLA pressure creating an incentive to shortcut safety/governance checks is a real, specific risk introduced by the commitment itself. (A denies any new risk from a stricter requirement. C treats an SLA as a guarantee against failure, which it isn't. D draws an incorrect domain boundary.)
7. **B.** Real discovery has to establish tolerance for partial failure and which workflows matter first — a single SLA number doesn't capture either. (A and C both treat the number as a complete spec. D substitutes an irrelevant question.)
8. **B.** Disclosing a real trade-off up front, with reasoning, preserves trust in a way an undisclosed one discovered later does not — consistent with this project's own documentation discipline throughout. (A and C both understate when disclosure matters. D inverts the actual reasoning for disclosure.)
9. **B.** Real data plus a stated set of genuine options respects the stakeholder's actual decision-making role. (A avoids the conversation entirely. C promises something that may not be achievable. D misassigns SLA management away from stakeholder communication entirely, which is incorrect.)
10. **B.** A real architecture document carries the reasoning and honest cost a status update never does. (A and D both understate the real difference. C is an arbitrary, unsupported requirement.)
11. **B.** Real lifecycle-phase concern is whether original discovery assumptions and governance configuration still match actual usage as the system matures. (A and D both treat lifecycle support as binary/nonexistent between launch and decommission. C draws an arbitrary, incorrect scope limit.)
12. **B.** Framing the real trade-off in decision-relevant terms respects what the stakeholder actually needs, rather than technical jargon or a vague non-answer. (A and D both fail to actually communicate the real consequence. C incorrectly removes the stakeholder from a decision that affects their own product.)
13. **B.** Team-wide tooling configuration exists precisely for conventions a new engineer can't infer alone — the real Domain 7 distinction between personal and team-wide use. (A and D both assume conventions propagate without documentation, which is the exact gap Domain 7's objective addresses. C dismisses a real, useful mechanism.)
14. **B.** Structured logging that captures enough real context to reproduce a report turns a vague complaint into an actionable one. (A gives up prematurely. C is an unreasonable, irrelevant requirement. D draws an incorrect domain boundary — operational debugging support is Domain 7's own named objective.)

---

*Checkpoint authored 2026-07-17, alongside Module 09's hands-on tier, both built together from the start.*
