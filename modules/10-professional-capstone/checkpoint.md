# Module 10 closed-book mock exam

**Format:** matches CCAR-P's own real structure, not the workshop's smaller per-module default — like Module 06, this is deliberate (see the module README). A pool of **6 scenarios** below; **complete 4 of the 6** (have someone else pick your 4 by number, or roll a die twice discarding repeats — don't cherry-pick the ones you feel strongest on). **120 minutes. 720/1000 to pass**, scored as: (questions correct across your 4 scenarios ÷ total questions across your 4 scenarios) × 1000. Two questions (B6, F5) are marked **(Select all that apply — TWO correct answers)** — matching the real exam's own multiple-choice *and* multiple-response format; every other question has exactly one correct answer.

**Before you start:** close or minimize your Claude Code session. No notes, no AI assistance, no searching. See [`docs/design-tension.md`](../../docs/design-tension.md).

**Scope, stated honestly:** the real CCAR-P exam is 63 items in 120 minutes. This pool has 6 scenarios of 7 questions each (42 total; a completed 4-scenario draw is 28 questions) — a deliberate reduction from 63, not a claim of matching it exactly, the same honest-reduction discipline Module 06 established for CCA-F. What *is* matched faithfully: the scenario-based framing, a 720/1000-equivalent scoring threshold computed the same way the real exam computes it, and — new for this capstone — the multiple-response question format the real exam also uses.

**Scenario originality note:** none of these 6 scenarios' content is copied or lightly reworded from the real CCAR-P exam's own published scenarios or sample questions — doing that would violate this workshop's own constraint (see `docs/design-tension.md`). Scenario A is this project's own Foundry, the shared system built across Modules 07-09 of this workshop — every question about it is original, but the system itself is, by design, this workshop's own creation, not an independent invention standing in for a real exam scenario. The other five scenarios are original premises chosen to exercise each domain's real skills without echoing any specific published exam scenario.

**Domain coverage across the full pool (all 6 scenarios), stated exactly rather than rounded to the intended target:** Domain 1 (Solution Design & Architecture, 17%) — 4 questions. Domain 2 (Claude Models, Prompting & Context Engineering, 13%) — 5 questions. Domain 3 (Integration, 19%) — 8 questions. Domain 4 (Evaluation, Testing & Optimization, 16%) — 7 questions. Domain 5 (Governance, Safety & Risk, 14%) — 9 questions. Domain 6 (Stakeholder Communication & Lifecycle, 14%) — 6 questions. Domain 7 (Developer Productivity & Operational Enablement, 7%) — 3 questions. (42 total.) This isn't the proportional split originally intended — Domain 1 undershoots its real 17% weight (4/42 ≈ 9.5%) and Domain 5 overshoots its real 14% weight (9/42 ≈ 21%), because three questions (B4, D2, E4) that read naturally as architecture-risk questions are actually testing "risk/failure-mode identification," which this workshop's own established domain mapping (from Module 09's checkpoint) places in Domain 5, not Domain 1. Caught and corrected during authoring rather than left mislabeled; the resulting skew is disclosed here rather than smoothed over.

---

## Questions

### Scenario A: Foundry, this workshop's own internal AI platform system

You've built Foundry across Modules 07-09: `ticket_triage` (a cache-friendly single-turn classifier for the Helpdesk team), `doc_qa`/`evaluation` (a RAG documentation Q&A system for the Platform Docs team, with a real evaluation harness), and `governance` (a human-in-the-loop compliance gate wrapping `doc_qa`).

**A1. (Domain 1: architectural pattern selection) The Helpdesk team's first instinct was "we want something like a full agentic loop." What made single-turn classification the correct call instead?

A) Agentic loops are the wrong choice here because powerful patterns are inherently a bad fit for internal tooling work, whatever the specific task looks like.
B) Single-turn classification is the cheaper option, and being cheaper is reason enough to choose it without needing to check whether the task actually fits.
C) Most Helpdesk tickets are single-turn structured classification decisions with no real need for multi-step tool use or autonomy — the powerful pattern would add latency, cost, and failure surface for no functional benefit over a well-scoped prompt.
D) The Helpdesk team lacked the technical sophistication to operate an agentic system.

**A2. (Domain 2: prompt-reuse / caching strategy) Why does `classify_ticket`'s system prompt need to stay byte-identical across every call, including retries?

A) It doesn't need to; regenerating the prompt on every retry (Module 02's own pattern) would work identically well here.
B) Byte-identical prompts are a Claude API technical requirement with no connection to caching or cost.
C) The requirement mainly matters for the very first call in a session; retries are a secondary concern since they happen less often.
D) At real volume (~4,000 tickets/month against the same static policy text), a static, reusable system prompt is what makes prompt caching pay off — mutating it on retry, even to add error feedback, defeats the caching this design exists to enable.

**A3. (Domain 3: RAG pipeline design) Why does `doc_qa` retrieve chunks via keyword-overlap scoring rather than calling a real embedding-based semantic search API?

A) Keyword scoring generally outperforms semantic search for retrieval tasks like this one, which is why it was chosen here.
B) No real embedding model is available in this teaching environment — `score_chunk`'s keyword overlap is a disclosed, deliberate stand-in, not a claim that it outperforms real semantic retrieval in production.
C) Semantic search would require infrastructure that's technically out of reach for a Claude-based system like this one.
D) Keyword scoring was chosen because the Platform Docs corpus is too small for semantic search to matter.

**A4. (Domain 4: evaluation metric design) Why does `evaluate` require the model to cite the *specific* expected document, not just cite something?

A) Citing anything at all is sufficient evidence a RAG system is working correctly.
B) A metric accepting any citation would silently pass a system confidently grounding answers in the *wrong* document — exactly the failure a real evaluation metric exists to catch, not average away.
C) Specific-citation requirements mostly come up for compliance-sensitive systems; general Q&A doesn't lean on them as heavily.
D) The requirement mainly makes the metric harder to compute, and the benefit to what it measures is marginal at best.

**A5. (Domain 5: human-in-the-loop strategy) Why does `governance.py` check retrieved chunks for sensitive content *before* calling `model_client`, rather than checking the model's response afterward?

A) Checking before or after produces an identical compliance outcome either way.
B) Checking beforehand means sensitive content never reaches the model call at all if flagged — checking only the response afterward means the content has already left the system's boundary by the time a problem is caught.
C) The model's response is typically close enough to the retrieved context that the timing of the check shouldn't matter much.
D) Human-in-the-loop strategy is mainly a final-output concern; inputs are further from user-facing risk and matter less.

**A6. (Domain 6: architecture documentation) What distinguishes Foundry's own ADRs and shipping-readiness reviews from a status update saying "the system works"?

A) Both documents mostly serve the same status-reporting function, just written up more formally.
B) Architecture documents mostly become worth writing after a system has already failed once; before that, they're a lower priority.
C) A real architecture document states what was decided, why, what alternative was rejected and why, and what the decision honestly costs — information a bare status update never carries.
D) The two mostly differ in length and formality, not really in the kind of information each contains.

**A7. (Domain 7: team tooling configuration) Why does Foundry's `.claude/rules/src.md` document conventions like "deterministic test doubles only" as team-wide configuration rather than leaving it to informal team knowledge?

A) `.claude/rules/` files mostly just restate things a new engineer would pick up naturally within their first few weeks anyway.
B) This kind of convention is better left undocumented so each engineer independently rediscovers it.
C) Team tooling configuration is mainly meant for build/deploy scripts; design conventions are more of an edge-case use for it.
D) Team-wide tooling configuration exists specifically for conventions a new engineer can't infer from the code alone but genuinely needs to know — informal knowledge doesn't reliably transfer to someone new.

---

### Scenario B: a real-time fraud detection review system

A Payments team wants Claude to review transactions flagged by a rules-based fraud detector, calling a third-party fraud-scoring API and recommending approve/hold/decline within a strict latency budget.

**B1. (Domain 3: connection-protocol selection) What's the most important factor in choosing how Claude connects to the third-party fraud-scoring API?

A) Use whichever connection technology is newest, since newer generally means better regardless of the specific API's own shape.
B) Whether the integration is met by a direct API call, an MCP server exposing it as a structured tool, or a different mechanism — driven by the API's own real shape (auth model, rate limits, whether multi-step tool use is actually needed) rather than habit.
C) The fraud-scoring vendor's own preferred integration pattern should be the deciding factor for Foundry's internal architecture here.
D) Connection-protocol selection doesn't carry much real trade-off in practice; most mechanisms end up roughly interchangeable.

**B2. (Domain 3: auth/security-gap analysis) The team argues the integration is safe because "Claude only reads fraud scores, it never approves anything itself." Why is read-only access alone not a complete security analysis?

A) It's a complete analysis, since read-only access carries essentially no risk on its own.
B) Read access is generally the more dangerous of the two, since it's harder to notice when something goes wrong.
C) Read-only access to sensitive transaction data still carries real exposure risk (data leaving its intended boundary, appearing in logs or model context beyond where it should) even without any write capability.
D) This concern is mainly a write-access issue; read-only integrations don't need the same level of security review.

**B3. (Domain 1: architectural pattern selection) Given the strict latency budget, why might a single well-designed prompt call outperform an agentic loop here, similar to Foundry's own `ticket_triage` reasoning?

A) If the decision (approve/hold/decline) can be made from the flagged transaction and fraud score alone with no need for multi-step investigation, a single call avoids the added latency and failure surface an agentic loop would introduce for no functional benefit.
B) Agentic loops are generally slower than single calls, which is reason enough on its own to avoid them here.
C) Latency budgets are a deployment-tuning concern, not something that should factor into the initial architectural pattern choice.
D) A single call is the safer choice here regardless of whether the task turns out to need multi-step reasoning.

**B4. (Domain 5: risk/failure-mode identification) What's a real failure mode specific to a strict latency budget that wouldn't exist without it?

A) Pressure to skip a real safety check (e.g., a human review step for high-value transactions) in order to hit the latency target — a real, specific tension worth naming rather than discovering after a shortcut ships.
B) A stricter latency requirement mostly just adds cost pressure; it doesn't really introduce a new category of risk.
C) Once a latency budget is set and agreed on, the risk questions around it are largely settled.
D) This reads mainly as a Domain 6 stakeholder-communication concern rather than something with real Domain 1 architectural weight.

**B5. (Domain 5: regulatory compliance) Beyond "do we have a compliance policy," what real architectural question does financial-fraud review raise?

A) A policy document mostly covers this; the specifics of system design don't add much obligation beyond what the policy already states.
B) Compliance requirements are mainly a consumer-facing concern; an internal review tool carries comparatively little of that weight.
C) Whether transaction data genuinely needs to be sent to a model call at all for the decision to work, and what retention/audit guarantees apply once it's part of a request — real, system-level questions a policy alone doesn't answer.
D) The question is mostly a legal one, with architecture playing a fairly minor supporting role.

**B6. (Domain 5: guardrails)** **(Select all that apply — TWO correct answers.)** Which of the following are real guardrails worth enforcing programmatically for this system, not left to a prompt instruction alone?

A) A hard block preventing an automatic "decline" action above a certain transaction value without human sign-off.
B) A stylistic preference for how the recommendation is phrased in the response text.
C) A requirement that the model never fabricate a fraud score it wasn't actually given by the third-party API.
D) A preference for shorter responses over longer ones when both are equally accurate.

**B7. (Domain 4: accuracy-latency trade-offs) If a larger model tier measurably improves fraud-decision accuracy but pushes latency over budget, what does a sound trade-off analysis require?

A) A stated, real threshold for what latency increase is acceptable for this system's actual use case, weighed against the real size of the accuracy gain — not treating either metric as automatically dominant.
B) Ship the accuracy improvement now; an accuracy gain is generally worth prioritizing over a latency budget.
C) Hold off on any accuracy improvement that adds latency cost, since the existing budget was presumably set for good reason.
D) Accuracy and latency are different enough metrics that they're best evaluated on separate tracks rather than jointly.

---

### Scenario C: a content localization QA pipeline

A Content team runs a pipeline that uses Claude to translate marketing copy into 12 languages and flag translations that need human review, under a real per-language cost budget.

**C1. (Domain 2: model selection trade-offs) Why might different languages in this pipeline reasonably use different model tiers?

A) Model tier should stay identical across languages here, since consistency is generally worth more than chasing marginal per-language differences.
B) Model tier selection is more of a budget lever than something meaningfully tied to language-specific translation quality.
C) Differentiating tiers per language usually isn't justified, since the added complexity tends to outweigh the benefit.
D) Some languages may have measurably higher error rates or more nuanced idiom-handling needs than others — a real, data-driven basis for tier differentiation, not an arbitrary per-language preference.

**C2. (Domain 2: system prompt / guardrail design) What's a real guardrail worth building into the translation prompt itself, beyond "translate this text accurately"?

A) A capable enough model mostly makes explicit guardrails redundant here.
B) Guardrails are mainly a Domain 5 governance concern; prompt design isn't really where they belong.
C) An explicit instruction to flag culturally sensitive phrasing or idioms that don't translate literally, rather than silently producing a technically-accurate but contextually wrong translation.
D) The main guardrail worth building in is a maximum output length; other concerns are secondary here.

**C3. (Domain 4: evaluation metric design) The pipeline's current metric is "% of translations that completed without an API error." Why is this an incomplete evaluation metric for translation quality?

A) It's a reasonably complete metric; successful completion is close to the main thing worth measuring here.
B) It measures whether a translation was *produced*, not whether it was *correct* — a confidently wrong translation that completes without error is invisible to this metric.
C) A translation that completes without an API error has most likely also passed quality review, since API errors are the main way a bad translation would tend to show up.
D) This metric isn't worth keeping around; it should be replaced by a real quality metric rather than supplemented.

**C4. (Domain 4: A/B testing) The team wants to compare two different prompt phrasings for flagging translations needing review. What does a valid A/B comparison require?

A) Testing each phrasing against a different sample of source text, since variety improves the comparison.
B) A/B testing is unnecessary once a phrasing looks reasonable on a few manual examples.
C) The two phrasings must use different model tiers to produce a meaningful comparison.
D) Holding the source text constant across both phrasings so the only variable that changed is the phrasing itself — otherwise a difference in flag rate could reflect a harder text sample rather than a worse phrasing.

**C5. (Domain 6: stakeholder communication) How should the Content team communicate a real trade-off (a cheaper model tier for low-risk languages, in exchange for a slightly higher review-flag rate) to a non-technical marketing stakeholder?

A) Lean on technical terms in the explanation and trust the stakeholder to look up what they need if they care enough.
B) Frame the real trade-off in terms the stakeholder actually needs to decide on — the cost savings and what it means for review workload — not just report that "an optimization was made."
C) Cost optimizations like this one generally don't need much stakeholder awareness, so it's fine to leave it out of the conversation.
D) Frame it to the stakeholder as if there's basically no real trade-off, since the review-rate change is small enough not to worry about.

**C6. (Domain 6: lifecycle-phase support) Six months after launch, three new languages are added to the pipeline. What real lifecycle-phase concern applies that didn't exist at launch?

A) Once a pipeline has launched successfully, there's not much more lifecycle concern until it's time to decommission it.
B) Whether the original per-language model-tier decisions and quality thresholds still make sense for the new languages, or whether they need their own independent evaluation rather than inheriting assumptions built for the original 12.
C) Lifecycle-phase support is mainly about infrastructure scaling; model or quality decisions aren't usually part of it.
D) New languages should generally inherit the same configuration as the existing ones, since re-evaluating each one individually is a lot of overhead.

**C7. (Domain 7: debugging/operational support) A marketing lead reports "the German translations feel off lately," with no further detail. What's the most useful team-tooling investment to make this actionable?

A) Vague reports like this are hard to do much with; there's not a lot of tooling that would make this kind of feedback more actionable.
B) Require the marketing lead to learn to read raw API logs before filing reports.
C) This reads mainly as a Domain 4 evaluation concern rather than something with a real Domain 7 operational-support angle.
D) Structured logging that captures enough of the actual request (source text, model tier used, flag status) per language that a vague report can be traced to specific, reproducible examples.

---

### Scenario D: an incident-response copilot for an SRE team

An SRE team wants Claude to help triage production incidents: reading alert data, suggesting likely causes, and optionally taking low-risk remediation actions (restarting a specific service) with human approval required for anything higher-risk.

**D1. (Domain 1: multi-agent orchestration strategy) The team proposes a coordinator agent that dispatches to specialized subagents (one for log analysis, one for metrics analysis, one for remediation). What real design question does this raise that a single-agent design wouldn't?

A) Subagents are mostly an implementation detail; the overall architecture doesn't really need to account for them separately.
B) Multi-agent systems generally don't need much explicit coordination logic; the subagents mostly handle themselves.
C) How results and partial failures from each subagent are reconciled by the coordinator, and what context each subagent actually needs passed to it explicitly, since subagents don't automatically inherit the coordinator's own context.
D) The main open question here is really just which language or framework each subagent gets implemented in.

**D2. (Domain 5: risk/failure-mode identification) What's a real, specific risk introduced by allowing the copilot to take remediation actions at all, distinct from the risk of a pure read-only triage assistant?

A) Adding action-taking capability doesn't introduce much beyond the risk a read-only assistant already carries.
B) This risk mainly applies to database actions; a service restart is a comparatively low-stakes action by comparison.
C) A wrong or premature remediation action (like restarting the wrong service) can itself cause an outage, not just fail to help with one — the blast radius is fundamentally different from a read-only tool that can only be wrong in its advice.
D) Remediation actions are arguably the safer choice here, since resolving the incident quickly reduces overall exposure.

**D3. (Domain 3: connection-protocol selection) What's the most important factor in choosing how the copilot connects to the paging/monitoring system to read alert data?

A) Lean toward whatever connection method was used most recently on a different project, since it's already familiar.
B) The monitoring vendor's own preferred integration approach should be the main driver of the SRE team's tooling choices here.
C) Connection-protocol selection stops mattering much once some working connection is in place.
D) Whether the integration needs a simple read-only API call or a richer, structured tool interface — driven by the monitoring system's own real shape and the copilot's actual query patterns, not habit.

**D4. (Domain 3: tool/agent capability-bloat evaluation) The team proposes one broad `manage_incident` tool that can read logs, read metrics, AND take remediation actions. What's the concern, consistent with this workshop's own tool-design discipline?

A) A single flexible tool is generally simpler to build and maintain, so the concern here is mostly theoretical.
B) The concern mainly kicks in once a tool crosses some number of distinct actions; three is probably still fine.
C) A broad, do-everything tool is harder to reason about, test, and scope permissions for than several narrow, purpose-built tools — the same capability-bloat risk this workshop's tool-design discipline (Module 03) and system-level architecture discipline (Foundry's own three-system defense) both name explicitly.
D) Tool capability mostly affects development convenience, not security or reasoning difficulty in any meaningful way.

**D5. (Domain 5: human-in-the-loop strategy) Why does "restart a specific service" get auto-approved while other remediation actions require human sign-off?

A) A real, stated risk tier — the specific, low-blast-radius action was deliberately distinguished from higher-risk ones, rather than treating "any automated action" as one undifferentiated risk category.
B) All remediation actions are probably safer treated identically for approval purposes, regardless of their individual blast radius.
C) Auto-approval is generally too risky to build into a system like this, whatever the specific action involved.
D) The distinction looks more like a convenience call than something grounded in a real risk difference.

**D6. (Domain 7: team tooling configuration) Why does the SRE team's own `.claude/` configuration matter for onboarding a new team member onto this copilot, beyond the copilot's own code?

A) Team-wide configuration captures conventions (which actions are safe to auto-approve, how to interpret a triage suggestion) a new engineer can't safely infer without documentation, the same Domain 7 distinction Foundry's own team tooling makes.
B) It mostly doesn't matter much; new engineers tend to pick up these conventions from the code before long.
C) `.claude/` configuration is mainly meant for build scripts; operational conventions are more of a side use for it.
D) Onboarding reads mainly as a Domain 6 stakeholder-communication concern rather than a real Domain 7 tooling one.

**D7. (Domain 4: diagnosing system issues) The copilot's triage suggestions were accurate for weeks, then started missing an increasingly common root cause. What's the most likely class of explanation worth investigating first?

A) The copilot isn't really the kind of system that degrades on its own, so this is probably better explained as a measurement error.
B) The most likely explanation is that the underlying model itself has degraded, independent of anything in the system's own design.
C) Accuracy issues that show up gradually are usually lower priority to investigate than sudden ones.
D) Something changed in the underlying system (a new service, a changed alert schema, a shifted failure pattern) that the copilot's own context or tooling hasn't been updated to reflect — the same "what changed" diagnostic instinct this workshop applies to stale retrieval (Module 08) applies here too.

---

### Scenario E: a sales proposal drafting assistant

A Sales Engineering team wants Claude to draft custom RFP responses by pulling from a large corpus of past proposals, under a real per-proposal cost constraint the VP of Sales has flagged as a budget concern.

**E1. (Domain 2: model selection trade-offs) Why might RFP drafting justify a more capable (and more expensive) model tier than Foundry's own `ticket_triage`, even though both are Claude-based systems?

A) More capable models are generally the safer default to reach for, whatever the specific task looks like.
B) The Sales team asked for a capable model by name, which alone is sufficient justification.
C) RFP drafting requires synthesizing relevant language across a large, varied corpus into a coherent, accurate document where a wrong or fabricated claim has real business consequences — a harder generation task than five-way classification, justifying the added cost.
D) Model tier should be chosen based on which team is more senior in the organization.

**E2. (Domain 2: context/token optimization) The proposal corpus is too large to fit in any context window. What's the most direct optimization?

A) Retrieve only the subset of past proposals actually relevant to the new prospect's requirements, rather than paying for and diluting context with the full corpus every time.
B) Use the largest available context window and attempt to include the entire corpus in every call.
C) Context optimization matters less once a large enough model tier is chosen, since the bigger window absorbs most of the inefficiency.
D) Reduce the corpus down to one solid generic template that gets reused across most proposals.

**E3. (Domain 1: architectural pattern selection) Given the VP's cost concern, why might a retrieval-then-single-call pattern be preferable to an agentic loop that iteratively searches the corpus across multiple turns?

A) Agentic loops tend to be the more expensive option here, which is reason enough to avoid one for this task.
B) If the retrieval step reliably surfaces what's needed in one pass, a single generation call avoids the added cost of multiple tool-use turns an agentic loop would introduce for the same underlying task.
C) Cost concerns are more of a downstream optimization question than something that should drive the initial pattern choice.
D) A single call is the safer bet here regardless of whether the task turns out to need iterative search.

**E4. (Domain 5: risk/failure-mode identification) What's a real failure mode specific to RFP drafting that wouldn't apply to Foundry's own ticket classification?

A) The two systems mostly share the same failure-mode profile, given they're both Claude-based generation-and-decision systems underneath.
B) A fabricated or misremembered claim about the company's own capabilities, presented confidently in a document a prospect might rely on — a real business and reputational risk with no equivalent in a five-way classification decision.
C) RFP drafting doesn't really have failure modes worth documenting in the same way a decision task does.
D) The main practical risk here is really just the document ending up too long for a prospect to read.

**E5. (Domain 4: cost/latency optimization) The team notices most of the per-proposal cost comes from re-processing the same boilerplate company-background section on every single proposal. What's the most direct fix, consistent with Foundry's own cache-friendliness lesson?

A) Switch to a cheaper model tier across the board; that's usually the most direct lever for cost regardless of where it's coming from.
B) Cost is driven mostly by model tier and call volume; how the content itself is structured across calls doesn't move the needle much.
C) Cap the number of proposals the team can draft per month to keep the recurring cost under control.
D) Isolate the static, reused boilerplate into a cacheable prompt segment, the same static/dynamic separation `classify_ticket`'s own system prompt design established, rather than resending it fresh with every proposal.

**E6. (Domain 4: evaluation metric design) How should the team measure whether a drafted proposal is actually good, beyond "did it generate without an error"?

A) Completion without an API error is close to a sufficient quality signal on its own for a task like this.
B) Quality is a lot harder to measure for a generation task like this than it is for a classification task.
C) A real accuracy/relevance metric against a labeled set of known-good proposals — checking whether cited past-proposal content was actually relevant to the new prospect's stated requirements, not just that text was produced.
D) Proposal length ends up being the most useful practical metric to track here.

**E7. (Domain 6: stakeholder communication) How should the team respond when the VP's cost concern conflicts with the Sales Engineering team's desire for the most capable model available?

A) Bring real data (cost per proposal, quality difference between tiers) and a stated set of options with real trade-offs, rather than either dismissing the cost concern or capitulating without evidence.
B) Generally defer to whichever stakeholder outranks the other, since that's usually how these disagreements get resolved anyway.
C) Avoid the conversation and let the disagreement resolve itself.
D) Reassure both stakeholders that their full preference is achievable, since surfacing the trade-off explicitly would probably just create friction.

---

### Scenario F: a legal team evaluating Claude for contract review

A Legal/Compliance team is evaluating whether to adopt Claude to flag risky clauses in vendor contracts pulled from a document management system, before rolling it out company-wide.

**F1. (Domain 3: connection-protocol selection) What's the most important factor in choosing how Claude connects to the document management system?

A) Whether a simple read API, a structured MCP tool, or another mechanism best fits the document system's own real shape (auth model, document format, retrieval patterns) — not habit or convenience.
B) Lean toward the newest connection technology available, since newer generally means better for a use case like this.
C) The document management vendor's own preferred integration pattern should be the main driver of the Legal team's internal architecture here.
D) Connection-protocol selection doesn't carry much real trade-off for a use case like this one.

**F2. (Domain 3: auth/security-gap analysis) The team argues the integration is safe because "Claude only reads contracts, it never modifies them." Why is this not a complete security analysis?

A) Read-only access to legally sensitive contract content still carries real exposure risk (where the content ends up, what's retained in logs or context) independent of whether anything is ever written back.
B) It's a fairly complete analysis, since read-only access carries little exposure risk on its own.
C) Read access is generally the riskier of the two here, since flagged content moves through more of the pipeline.
D) This concern is mainly a write-access issue and doesn't carry much weight for a read-only integration.

**F3. (Domain 3: tool/agent capability-bloat evaluation) The team proposes one broad `handle_contract` tool that can read, summarize, flag risks, AND auto-reject vendor contracts below a certain risk score. What's the concern?

A) Broader tool capability is generally the more convenient choice, so the concern here is mostly theoretical.
B) Bundling read, summarize, flag, and auto-reject into one tool makes it harder to reason about, test, and scope permissions for than narrower, purpose-built tools — especially concerning here since auto-rejection has real legal and business consequences a summarization action doesn't.
C) The concern mainly kicks in once contract volume crosses some threshold; a modest caseload should be fine.
D) Tool capability mostly affects development convenience, not legal risk in any meaningful way.

**F4. (Domain 5: guardrails) What's a real guardrail worth enforcing programmatically before this system can auto-flag (not auto-reject) a contract clause as risky?

A) A requirement that every flagged clause include the specific contract text and section it's flagging, so a human reviewer can verify the flag rather than trusting an unsupported claim.
B) A model capable enough at legal analysis mostly makes explicit guardrails redundant here.
C) Guardrails matter most for auto-reject actions; flagging and advisory actions carry comparatively little need for them.
D) The main guardrail worth building in here is a limit on how many clauses can be flagged per contract.

**F5. (Domain 5: ethical AI considerations)** **(Select all that apply — TWO correct answers.)** Which of the following are real ethical considerations for this system, distinct from its legal-compliance obligations?

A) Whether the user interface uses a visually appealing color scheme.
B) Whether the system's risk-flagging is consistently calibrated across different vendor sizes, rather than systematically flagging small vendors' contracts more aggressively than large vendors' for reasons unrelated to actual risk.
C) Whether the tool completes its analysis in under five seconds per contract.
D) Whether over-reliance on the tool could erode reviewers' own contract-review skills over time if used without any ongoing human judgment.

**F6. (Domain 6: structured discovery) Before building this system, what does a real structured discovery pass need to establish beyond "flag risky clauses"?

A) The one-line goal mostly stands on its own as a working requirements specification.
B) Structured discovery mostly becomes unnecessary once a rough goal statement has been agreed upon.
C) The main practical thing left to establish is really just which document format the system will read.
D) What "risky" actually means to this specific Legal team (which clause types, what risk tolerance), which contracts are in scope for an initial rollout versus later phases, and what a false negative actually costs the business if missed.

**F7. (Domain 6: lifecycle-phase support) Three months after a successful pilot with one vendor category, the team wants to expand to all vendor categories. What real lifecycle-phase concern applies?

A) A successful pilot is a pretty strong signal the system will hold up at full scale without much further concern.
B) Lifecycle-phase support is mainly about infrastructure capacity; the original discovery assumptions aren't usually the concern here.
C) Expansion should generally follow once a pilot succeeds, since category differences tend to matter less than the core system working at all.
D) Whether the original discovery assumptions (which clause types matter, what risk tolerance was calibrated for) still hold for vendor categories the pilot never actually tested, rather than assuming uniform performance across categories.

---

## Answer key

**Do not scroll further until you've completed all 4 of your drawn scenarios closed-book and recorded your answers.**

### Scenario A

A1. **C.** Most tickets are single-turn classification with no real need for the more powerful pattern; the powerful pattern would add cost and failure surface for no benefit. (A and B both substitute a blanket rule for actual analysis. D is an unsupported, dismissive claim.)
A2. **D.** A static, cache-reusable prompt is what makes caching pay off at real volume; mutating it on retry defeats that. (A denies a real, documented distinction between Module 02's context and this one. B misattributes the requirement. C understates the requirement's actual scope.)
A3. **B.** Keyword scoring is a disclosed, deliberate stand-in given no real embedding model is available, not a claim of superiority. (A and D both overclaim keyword scoring's merits. C is factually false — semantic search integration is technically possible.)
A4. **B.** A too-lenient "cited anything" metric would miss a system confidently grounding answers in the wrong document. (A and C both accept or narrow away a real gap. D denies the metric's real purpose.)
A5. **B.** Checking beforehand keeps sensitive content from ever reaching the model call; checking after leaves a real exposure window. (A and C both deny a real, meaningful difference. D mischaracterizes where human-in-the-loop strategy can apply.)
A6. **C.** Real architecture documents carry decision reasoning, rejected alternatives, and honest costs a status update never does. (A and D both understate the real difference. B is an arbitrary, unsupported requirement.)
A7. **D.** Team-wide configuration exists precisely for conventions a new engineer can't infer alone. (A and B both deny the real value documented conventions provide. C draws an arbitrary, incorrect scope limit.)

### Scenario B

B1. **B.** The connection mechanism should be driven by the API's own real shape, not habit. (A and C substitute a rule of thumb or an external party's preference for actual analysis. D denies real trade-offs exist.)
B2. **C.** Read-only access still carries real exposure risk around where sensitive data ends up. (A and B both mischaracterize the actual risk profile. D draws an incorrect, arbitrary distinction.)
B3. **A.** If the decision doesn't need multi-step investigation, a single call avoids added latency and failure surface for no functional benefit. (B and D both overgeneralize. C denies latency's real relevance to pattern choice.)
B4. **A.** A latency budget can create real pressure to skip a genuine safety check — a specific, nameable risk. (B and C both deny a real risk. D draws an incorrect domain boundary.)
B5. **C.** Real architectural questions (does the data need to be sent at all, what retention applies) go beyond a policy document. (A and B both understate compliance's real architectural reach. D minimizes architecture's real role in the question almost to nothing.)
B6. **A and C.** A hard block on high-value auto-decline and a no-fabrication requirement on fraud scores are both real, consequential guardrails worth enforcing programmatically. (B and D are stylistic preferences with no real safety or correctness stake — not guardrails in the sense this question tests.)
B7. **A.** A real trade-off analysis weighs a stated latency threshold against the real size of the accuracy gain. (B and C both treat one metric as automatically dominant. D treats the two metrics as independent enough to skip joint evaluation, when the trade-off between them is exactly the point.)

### Scenario C

C1. **D.** Real, measured per-language error-rate differences are a legitimate, data-driven basis for tier differentiation. (A and C both deny any legitimate basis for differentiation exists. B denies a real, plausible connection.)
C2. **C.** Flagging culturally sensitive or non-literal phrasing is a real, useful guardrail beyond bare accuracy. (A treats capability as a substitute for explicit guardrails. B draws an incorrect domain boundary. D trivializes guardrail design.)
C3. **B.** A completion-rate metric can't distinguish a correct translation from a confidently wrong one. (A and C both overstate the existing metric's completeness or scope. D discards a metric with some value instead of supplementing it.)
C4. **D.** Holding source text constant isolates phrasing as the only variable, which is what makes the comparison valid. (A and B both deny or invert this core A/B testing principle. C introduces an unrelated, incorrect requirement.)
C5. **B.** Framing the real trade-off in decision-relevant terms respects what the stakeholder actually needs to know. (A and D both fail to actually communicate the real consequence. C incorrectly removes the stakeholder from a decision that affects them.)
C6. **B.** Real lifecycle concern is whether original per-language assumptions still hold for languages they were never built for. (A and D both treat lifecycle support as nonexistent or automatic between launch and change. C draws an incorrect, arbitrary scope limit.)
C7. **D.** Structured logging capturing real request detail per language turns a vague report into a debuggable one. (A gives up prematurely. B is an unreasonable requirement. C draws an incorrect domain boundary — this is exactly Domain 7's own operational-support objective.)

### Scenario D

D1. **C.** Real orchestration questions include result reconciliation and explicit context-passing, since subagents don't automatically inherit a coordinator's context. (A denies these are real architectural concerns. B is factually false. D trivializes the question.)
D2. **C.** A wrong remediation action can itself cause an outage — a fundamentally different blast radius than a read-only tool's advice being wrong. (A denies a real, significant risk difference. B narrows the risk arbitrarily. D inverts the actual risk relationship.)
D3. **D.** The connection mechanism should fit the monitoring system's real shape and the copilot's actual query needs. (A and B substitute habit or an external party's preference for real analysis. C denies real trade-offs exist.)
D4. **C.** A broad, do-everything tool is harder to reason about and scope than narrow, purpose-built ones — the same capability-bloat risk named throughout this workshop. (A asserts the opposite of the documented risk. B invents an arbitrary threshold. D denies a real connection between capability and reasoning difficulty.)
D5. **A.** A real, stated risk tier distinguishes low-blast-radius actions from higher-risk ones, rather than treating all automation as one category. (B and C both deny any legitimate tiering is possible. D denies the distinction has any real basis, which the scenario's own stakes argue against.)
D6. **A.** Team-wide configuration captures conventions a new engineer can't safely infer alone — the same Domain 7 distinction Foundry's own tooling makes. (B and C both deny documented conventions have real value. D draws an incorrect domain boundary.)
D7. **D.** A changed underlying system is the most likely explanation for a gradually emerging blind spot, the same "what changed" instinct Module 08's own stale-retrieval diagnosis applies. (A and B both jump to unsupported explanations. C dismisses a real, investigable pattern.)

### Scenario E

E1. **C.** A harder generation task with real business consequences for a wrong claim justifies a more capable tier than a bounded five-way classification. (A treats capability as a context-free default. B substitutes team preference for task-based reasoning. D is an arbitrary, indefensible criterion.)
E2. **A.** Retrieving only the relevant subset directly addresses cost and relevance together. (B pays maximal cost for minimal relevance. C denies optimization matters once tier is large enough. D discards the per-prospect relevance the task actually requires.)
E3. **B.** If retrieval reliably surfaces what's needed in one pass, a single call avoids the added cost of iterative search for the same task. (A and D both overgeneralize. C denies cost's real relevance to pattern choice.)
E4. **B.** A confidently fabricated claim in a document a prospect relies on is a real, distinct business/reputational risk. (A denies any real difference between the two systems' risk profiles. C denies generation tasks have real failure modes. D trivializes the actual risk.)
E5. **D.** Isolating static boilerplate into a cacheable segment directly addresses the redundant cost, mirroring `classify_ticket`'s own cache-friendly design. (A misdiagnoses the cost source. B denies a real, direct relationship. C addresses volume instead of the actual cause.)
E6. **C.** A real relevance/accuracy metric against known-good proposals is what actually measures quality, not mere successful completion. (A and B both understate or deny the need for a real quality metric. D substitutes an irrelevant proxy.)
E7. **A.** Bringing real data and a stated set of options respects both stakeholders' legitimate interests without dismissing either. (B and D both fail to engage the real trade-off honestly. C avoids the conversation stakeholders need to have.)

### Scenario F

F1. **A.** The connection mechanism should fit the document system's own real shape, not habit or convenience. (B and C substitute a rule of thumb or an external party's preference for real analysis. D denies real trade-offs exist.)
F2. **A.** Read-only access to legally sensitive content still carries real exposure risk independent of write capability. (B and C both mischaracterize the real risk profile. D draws an incorrect, arbitrary distinction.)
F3. **B.** Bundling read, summarize, flag, and auto-reject into one tool is harder to scope and reason about, especially given auto-rejection's real legal consequences. (A treats broader capability as generally preferable, the opposite of the documented risk. C invents an arbitrary threshold. D denies legal risk has any connection to tool design.)
F4. **A.** Requiring the specific flagged text and section lets a human reviewer verify the flag instead of trusting an unsupported claim. (B treats capability as a substitute for explicit verification. C draws an arbitrary scope limit the scenario doesn't support. D trivializes guardrail design into an unrelated constraint.)
F5. **B and D.** Consistent risk-calibration across vendor sizes and guarding against skill erosion from over-reliance are both real ethical considerations distinct from legal-compliance obligations. (A and C are UI/performance concerns with no real ethical stake in the sense this question tests.)
F6. **D.** Real discovery establishes what "risky" means to this team, initial scope, and the real cost of a false negative — none of which a one-line goal captures. (A and B both treat the goal statement as a complete spec. C substitutes an unrelated technical question.)
F7. **D.** Real lifecycle concern is whether original discovery assumptions hold for categories the pilot never actually tested. (A and C both treat expansion as automatically safe once any pilot succeeds. B draws an incorrect, arbitrary scope limit.)

---

*Mock exam authored 2026-07-17, alongside Module 10's hands-on capstone exercise, both built together. Scoring: (correct answers across your 4 drawn scenarios ÷ total questions across those 4 scenarios) × 1000; 720/1000 to pass. Multiple-response questions (B6, F5) count as correct only if both correct letters are selected and no incorrect letter is selected.*
