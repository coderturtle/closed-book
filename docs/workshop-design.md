# Workshop Design

> **Closed Book.** Naming pass complete (see `docs/decisions.md`) — this doc was drafted after the name was chosen, so it uses the final name throughout.

## The one-line problem

Agent-literate practitioners already learn new tools by doing, harness in hand — but "the certification" for doing that with Claude specifically didn't exist as a target until Anthropic launched the Claude Certification Program in March 2026. This workshop's bet is that nothing *yet* teaches toward that real, proctored credential the way this audience already learns everything else: agent in hand, real exam blueprint as the syllabus, practice under the same closed-book conditions the actual exam imposes — a claim about a gap in what exists today, not a claim this workshop has verified is permanently true or that no other resource is attempting the same thing.

**Correction, 2026-07-14:** this workshop was originally scoped as "Claude Developer, Foundations → Professional" — a single-track, two-level spine. That target doesn't exist as stated. As of today there are exactly four live Claude Certification exams: **Claude Certified Associate – Foundations**, **Claude Certified Developer – Foundations**, **Claude Certified Architect – Foundations**, and **Claude Certified Architect – Professional**. Developer has a Foundations level only; Architect is the *only* track with both levels today. Redirected, at coderturtle's direction, to the **Architect** track — a real deviation from "pure hands-on coding" toward design/governance framing, chosen explicitly with that tradeoff named up front. See `docs/decisions.md` for the full correction record.

## External Validation: The Claude Certification Program

Real, current, and verified against Anthropic's own exam guide PDFs (not third-party prep-site summaries, several of which turned out to recycle identical domain lists across different exam pages — see `docs/design-tension.md`'s research-sourcing note):

- **Claude Certified Architect – Foundations (CCA-F).** 60 scenario-based multiple-choice questions, 120 minutes, scaled score 100–1,000, 720 to pass. Proctored (online or test center), closed-book, no AI assistance, no notes, workspace must stay clear of secondary monitors and phones. $125. No mandatory prerequisites (6+ months' hands-on Claude experience recommended). The exam draws 4 scenarios at random from a published pool of 6 (Customer Support Resolution Agent, Code Generation with Claude Code, Multi-Agent Research System, Developer Productivity with Claude, Claude Code for CI, Structured Data Extraction), each framing roughly 15 questions — this 6-scenario/4-drawn structure is what Module 06's capstone mock exam mirrors. Source: Anthropic's own *Claude Certified Architect – Foundations Certification Exam Guide* (fetched in full 2026-07-14).
- **Claude Certified Architect – Professional (CCAR-P).** 63 items (multiple-choice and multiple-response), 120 minutes, same 100–1,000 scale, 720 to pass, criterion-referenced. $175. 12-month validity with a free on-time renewal assessment. No mandatory prerequisites. Source: Anthropic's own *Claude Certified Architect – Professional Exam Guide*, v1.0, effective July 2026 (fetched in full 2026-07-14).

coderturtle has committed to personally sitting the real CCA-F exam once Modules 01-06 exist, and the real CCAR-P exam once Modules 07-10 exist, as this workshop's own dogfooding evidence — same discipline Borrow Native applied to the Ardan Labs exam. **This is a stated intent, not yet evidenced** — no exam has been attempted at time of writing.

## Audience

Agent-literate practitioners: comfortable driving Claude Code daily, reading a diff, working through a harness — but **new to the certification body of material specifically**, not new to Claude itself. Not an intro-to-agents workshop (harness fluency assumed); the thing assumed unfamiliar is the *exam's own blueprint* — its exact domain weights, task statements, and scenario framing — and the discipline of demonstrating that knowledge without the agent's help.

## Format

Self-paced, public repo. Matches Terminal Velocity's and Borrow Native's precedent.

## Subject vs. method

- **Subject:** the Claude Certification Program's Architect track — Foundations (5 domains) then Professional (7 domains), per Anthropic's own published blueprints.
- **Method:** agent-native *and* exam-native at once, deliberately in tension (see `docs/design-tension.md`): every module's core exercise is built hands-on through Claude Code, then checked against a closed-book, no-AI practice quiz that simulates the real exam's own conditions.

## The shared project: `resolve`

Added 2026-07-15, at coderturtle's direction, before Module 01's content was authored. Part 1 (Modules 01-06) builds one real project across the arc rather than independent per-module fixtures: `resolve`, a customer support resolution agent modeled directly on CCA-F's own Scenario 1 (`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`, targeting 80%+ first-contact resolution with a hard escalate-when-unsure rule). By Module 06's capstone, a learner has a real, working agent, not six disconnected snippets — same shape Borrow Native adopted for its own arc, and for a similar reason: CCA-F's five domains are additive toward one real system, not five different lenses on one problem the way Terminal Velocity's subject was. Full spec and module-by-module build-out table: `fixtures/resolve/SPEC.md`.

Part 2 (Modules 07-10) does not extend `resolve` directly — Professional-level work (solution design, evaluation, governance) operates one level up from a single system's implementation, closer to reviewing/extending a Claude-based solution generally than adding one more feature to one fixture. Whether Part 2 needs its own shared artifact (e.g. a written architecture proposal carried across Modules 07-09) is an open question for whoever authors that content, not decided here.

## The teaching method: two-tier gate

Every module's gate has two required parts, per coderturtle's explicit design decision:

1. **Deterministic tier — hands-on, WITH Claude Code.** A real artifact: a working agentic loop, a designed MCP tool, a CLAUDE.md hierarchy, a RAG pipeline sketch — whatever the domain's task statements actually ask a practitioner to *build*. Graded against the exam guide's own "Skills in:" bullets, not a rubric invented from scratch. Self-graded via a per-module checklist derived directly from those bullets (this is a self-paced, facilitator-less repo — see `docs/design-tension.md`'s open-question note on grading authority for the honest limits of that).
2. **Exam-condition tier — closed-book, WITHOUT Claude Code.** A short, timed, multiple-choice checkpoint written *originally* against the domain's published task statements and weight — modeled on the exam guide's own sample-question *style and difficulty* (scenario framing, one correct answer, plausible distractors that represent a specific wrong reasoning path, not random noise) but never its actual items. **Never copied or lightly reworded from the real exam, any leaked/scraped item bank, or Anthropic's own official sample questions published in the exam guides** — see `docs/design-tension.md`'s Constraint section. **Default format** (stated here so the gate is buildable, not just promised as a category; a module may state a different count in its own README if its domain genuinely warrants it, but the default applies unless overridden): 10-15 questions, 15-20 minutes, 80% to pass — deliberately similar in spirit to the real exam's own 720/1000 (~72%) bar, set a little higher because a practice checkpoint should be a harder bar than the credential itself. **Suggested ritual, stated explicitly rather than left to the honor system:** close or minimize the Claude Code session before starting the checkpoint, use a separate device or printed copy if possible, and time it for real — the checkpoint's value is entirely in genuinely rehearsing recall without the agent, not in getting a passing score.

Both are required to advance. Neither substitutes for the other: passing the closed-book quiz by guessing doesn't demonstrate the hands-on skill, and building the artifact with Claude's help doesn't prove it survives exam conditions.

## Canonical-curriculum anchor (research pass, 2026-07-14)

Anthropic's own exam guides are the curriculum anchor — fetched and read in full, not summarized from secondary sources (an early research pass found third-party "exam prep" sites recycling an *identical* 5-domain/weight list across pages nominally about different exams in the Claude Certification Program — which turned out to be either wrong or conflated; the primary-source PDFs resolved this). This workshop is the first in this pipeline to differentiate against **the certifying body's own published blueprint** rather than community teaching material (the Book/Rustlings/Exercism precedent from Borrow Native) — a new curriculum-anchor shape worth naming for future workshops that target a real exam.

**Differentiator against the exam guide itself:** the guide tells you what's tested and gives 12 sample questions; it doesn't grade a real attempt, doesn't run you through the actual Claude Agent SDK/MCP/Claude Code mechanics hands-on, and doesn't simulate exam-condition recall under time pressure repeatedly across every domain. Closed Book's bet — a hypothesis this workshop is testing via the dogfooding commitment above, not a finding it's reporting — is that doing both, building the real thing and then defending it closed-book, might prepare a candidate better than the guide's own "read this, then take our sample questions" approach on its own.

## The module arc

### Part 1 — Architect Foundations (CCA-F), Modules 01–06

Anchored directly to CCA-F's 5 domains and 30 task statements. Ordered by real dependency, not just blueprint weight order — Claude Code fluency and tool/prompt mechanics have to exist before an agentic loop can be built on top of them, and several of Domain 5's task statements (error propagation across multi-agent systems, large-codebase context management under an active agent) are specifically about *agentic* context management, which needs Module 04's agent to exist first even though context management as a general concern (prompt caching, conversation-history handling) doesn't strictly require it.

| # | Module | Domain (CCA-F weight) | Hard prerequisite | Task statements covered |
|---|---|---|---|---|
| 01 | Configuring Claude Code for Real Work | Domain 3: Claude Code Configuration & Workflows (20%) | none (day-one harness fluency) | 3.1–3.6: CLAUDE.md hierarchy, slash commands/skills, path-specific rules, plan mode vs. direct execution, iterative refinement, CI/CD integration |
| 02 | Prompts and Structured Output That Survive Production | Domain 4: Prompt Engineering & Structured Output (20%) | 01 (delivered through configured Claude Code) | 4.1–4.6: explicit criteria, few-shot, tool_use/JSON schemas, validation-retry loops, batch processing, multi-instance review |
| 03 | Designing Tools and MCP Interfaces | Domain 2: Tool Design & MCP Integration (18%) | 02 (tool `input_schema` design reuses the JSON-schema discipline Module 02 builds for structured output — a related skill, not, as an earlier draft of this table overstated, the identical mechanism) | 2.1–2.5: tool interface design, structured error responses, tool distribution/tool_choice, MCP server integration, built-in tools |
| 04 | Agentic Loops and Multi-Agent Orchestration | Domain 1: Agentic Architecture & Orchestration (27%, largest domain) | 01+02+03 (an agentic loop calls tools (03), built on configured Claude Code (01), reasoning over structured prompts (02)) | 1.1–1.7: agentic loop lifecycle, coordinator-subagent patterns, subagent invocation/context passing, multi-step workflows/handoff, Agent SDK hooks, task decomposition, session state/resumption/forking |
| 05 | Context and Reliability at Scale | Domain 5: Context Management & Reliability (15%) | 04 (this module's hardest task statements — multi-agent error propagation, large-codebase context management under an active agent — need Module 04's agentic system to exist as the thing being managed; the domain's more general concerns, like conversation-context preservation, don't strictly require it but are taught here as one coherent module rather than split across the arc) | 5.1–5.6: conversation context preservation, escalation/ambiguity resolution, error propagation across multi-agent systems, large-codebase context management, human review/confidence calibration, provenance/multi-source synthesis |
| 06 | Foundations Capstone: Sit-Ready for CCA-F | all of 01–05 | all of 01–05 | full closed-book mock exam (4 scenarios drawn from a pool matching the real exam's own 6-scenario/4-drawn format) + a real seeded scenario spanning 3+ domains, diagnosed and fixed hands-on |

### Part 2 — Architect Professional (CCAR-P), Modules 07–10

CCAR-P's 7 domains don't map 1:1 to modules the way CCA-F's 5 did without misrepresenting either their real weights or their dependency order — compressing 7 real domains into a false parity with Part 1's 5 would be the same mistake as inventing a "Developer Professional" arc in the first place. Instead, they're grouped into 3 real thematic clusters that mirror Domain 1's own stated solution lifecycle (discovery → design → build/validate → govern → deliver), roughly balanced by combined weight (30% / 35% / 35%):

| # | Module | Domains (CCAR-P weight) | Hard prerequisite | Cluster theme |
|---|---|---|---|---|
| 07 | Designing the Solution: Architecture, Models & Context Strategy | Domain 1: Solution Design & Architecture (17%) + Domain 2: Claude Models, Prompting & Context Engineering (13%) = 30% | 06 (CCA-F fluency in agentic patterns/prompting is what Professional-level design judgment builds on) | Design |
| 08 | Building and Proving It: Integration, Evaluation & Optimization | Domain 3: Integration (19%) + Domain 4: Evaluation, Testing & Optimization (16%) = 35% | 07 (you evaluate the thing 07 designed) | Build & validate |
| 09 | Shipping Responsibly: Governance, Stakeholders & Team Enablement | Domain 5: Governance, Safety & Risk Management (14%) + Domain 6: Stakeholder Communication & Lifecycle Management (14%) + Domain 7: Developer Productivity & Operational Enablement (7%) = 35% | 08 (governance and delivery apply to a system that's been built and evaluated) | Govern & deliver |
| 10 | Professional Capstone: Sit-Ready for CCAR-P | all of 07–09 | all of 07–09 | full closed-book mock exam (63-item format) + a real end-to-end architecture review defended in writing against a stakeholder objection |

**Deviation from the originally-scoped "8 modules, 4+4" arc, stated honestly (mirrors Borrow Native's own module-count corrections):** the real blueprints have 5 and 7 domains, not 4 and 4. Forcing them into 4-module halves would mean either merging two real, differently-weighted domains into one module (misrepresenting the exam's own emphasis) or inventing a domain that doesn't exist. Ten modules (six + capstone, three + capstone) is what fidelity to Anthropic's own published blueprint actually requires.

## What you keep

Per the Gremlin's takeaway requirement: every module's gate produces something reusable. Concrete takeaways are Coachgremlin's job at content-building time; intended shape per module:

| # | Module | Intended takeaway shape |
|---|---|---|
| 01 | Claude Code Configuration | A personal CLAUDE.md/rules/skills starter kit, structured the way the exam blueprint expects (hierarchy, path-scoping, frontmatter options) |
| 02 | Prompts & Structured Output | A reusable few-shot/JSON-schema template library for ambiguous-extraction scenarios |
| 03 | Tool & MCP Design | A tool-description checklist (boundary conditions, distinguishing near-duplicate tools) plus a scoped `.mcp.json` template |
| 04 | Agentic Orchestration | A coordinator-subagent reference implementation (hooks, `Task` tool patterns, session resumption) |
| 05 | Context & Reliability | A context-degradation diagnostic playbook (scratchpad discipline, structured error propagation) |
| 06 | Foundations Capstone | A personal CCA-F exam-day prep sheet, built from the mock exam's own weak spots |
| 07 | Solution Design & Context Strategy | An architecture-decision-record template scoped to Claude solution design |
| 08 | Integration & Evaluation | An evaluation-dataset/A-B-test harness template |
| 09 | Governance & Stakeholders | A governance/risk checklist (compliance, human-in-the-loop, stakeholder sign-off) |
| 10 | Professional Capstone | A personal CCAR-P exam-day prep sheet, same discipline as Module 06's |

**Safe-design default for Modules 03-04's reusable artifacts (Security-Conscious Reviewer finding, Review Panel 2026-07-14):** the tool/MCP interface checklist and the coordinator-subagent reference implementation are published, copyable artifacts. Both must default to fail-closed hooks (a blocked/ambiguous tool call escalates rather than proceeds), no secrets embedded in tool code or example `.mcp.json` files (environment-variable expansion only, per the exam guide's own Task Statement 2.4), and human approval required before any destructive action pattern (deletes, refunds, account changes) — named here at skeleton stage so Coachgremlin builds to this default rather than deciding it ad hoc per module.

## Build-in-public build log

Same Astro-on-Pages pipeline as Terminal Velocity and Borrow Native.

## What's explicitly out of scope for this design pass

- The Associate track and any non-Architect Developer content — this workshop targets Architect only; a future workshop could cover Associate/Developer as its own differently-shaped run.
- Real module content (Coachgremlin's job, later, one module at a time).
- The real CCA-F/CCAR-P exam attempts themselves — stated intents, not yet scheduled or sat.
- The actual Astro site content and first Pages deploy.
