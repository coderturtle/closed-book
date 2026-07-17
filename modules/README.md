# Modules

Closed Book's spine is Anthropic's own Claude Certification Program blueprint, in two parts: **Architect Foundations** (5 domains, Modules 01–06) then **Architect Professional** (7 domains, grouped into 3 thematic clusters, Modules 07–10). Work through them in order — each module states a hard prerequisite on an earlier one.

Every module's core exercise is built hands-on through Claude Code, then checked closed-book (no AI, no notes) against a practice checkpoint modeled on the exam's own blueprint and sample-question style — never copied from the real exam or Anthropic's own official sample questions. See the top-level README, [`docs/workshop-design.md`](../docs/workshop-design.md), and [`docs/design-tension.md`](../docs/design-tension.md) for the full thesis and the named tension between the two.

Part 1's modules (01-06) all build one real shared project, `resolve`, a customer support resolution agent modeled directly on CCA-F's own Scenario 1 — see [`fixtures/resolve/SPEC.md`](../fixtures/resolve/SPEC.md) for the full spec and build-out table.

**Hands-on by design, not passive text.** No module here completes by reading it. Every module states a required gate: a real artifact plus an observed closed-book checkpoint. Every gate also has a stated **takeaway**: you keep something reusable, not just proof you did the exercise.

> **Content status: Modules 01-09 are real, Module 10 is skeleton.** [Module 01](01-configuring-claude-code/README.md), [Module 02](02-prompts-structured-output/README.md), [Module 03](03-tool-mcp-design/README.md), [Module 04](04-agentic-orchestration/README.md), [Module 05](05-context-reliability/README.md), and [Module 06](06-foundations-capstone/README.md) each have a working exercise, a real deterministic checker (`scripts/verify_module_01.py` through `verify_module_06.py`, each chaining the one before it per the cumulative-gate convention), a real closed-book checkpoint, and a completed multi-attempt dry run you can run today. Module 06 closes Part 1 (Architect Foundations) in full. [Module 07](07-solution-design-context-strategy/README.md) opens Part 2 (Architect Professional) on a new shared project, `fixtures/foundry/` (not a continuation of `resolve` — see [`fixtures/foundry/SPEC.md`](../fixtures/foundry/SPEC.md) for why), with its own real exercise, deterministic checker (`scripts/verify_module_07.py`), closed-book checkpoint, and dry run. [Module 08](08-integration-evaluation/README.md) continues Foundry with the Platform Docs team's RAG documentation Q&A problem (`scripts/verify_module_08.py`, chaining `check_module_07`), its own closed-book checkpoint, and dry run. [Module 09](09-governance-stakeholders/README.md) governs and ships Module 08's own system responsibly — a human-in-the-loop gate, a shipping-readiness review, and real team tooling configuration (`scripts/verify_module_09.py`, chaining `check_module_08`), its own closed-book checkpoint, and dry run. Module 10 (Professional Capstone) has a decided question, gate shape, and takeaway shape, but no authored exercise yet.

## Part 1 — Architect Foundations (CCA-F)

| # | Module | Hard prerequisite | The question it answers | Domain (weight) |
|---|---|---|---|---|
| 01 | [Configuring Claude Code for Real Work](01-configuring-claude-code/README.md) | none (day-one harness fluency) | How do you configure Claude Code so it works the way your team needs, not the way it ships by default? | Claude Code Configuration & Workflows (20%) |
| 02 | [Prompts and Structured Output That Survive Production](02-prompts-structured-output/README.md) | 01 | How do you get Claude to produce output you can actually trust and parse, every time? | Prompt Engineering & Structured Output (20%) |
| 03 | [Designing Tools and MCP Interfaces](03-tool-mcp-design/README.md) | 02 | How do you design a tool interface Claude will actually pick correctly, and fail safely when it can't? | Tool Design & MCP Integration (18%) |
| 04 | [Agentic Loops and Multi-Agent Orchestration](04-agentic-orchestration/README.md) | 01+02+03 | When should one agent do the whole job, and when does it need to be split across several? | Agentic Architecture & Orchestration (27%, largest) |
| 05 | [Context and Reliability at Scale](05-context-reliability/README.md) | 04 | How do you keep a long-running agent's understanding accurate instead of quietly degrading? | Context Management & Reliability (15%) |
| 06 | [Foundations Capstone: Sit-Ready for CCA-F](06-foundations-capstone/README.md) | 01–05 | Are you actually ready to sit the real exam? | All 5 domains, synthesized |

## Part 2 — Architect Professional (CCAR-P)

| # | Module | Hard prerequisite | The question it answers | Domains (combined weight) |
|---|---|---|---|---|
| 07 | [Designing the Solution: Architecture, Models & Context Strategy](07-solution-design-context-strategy/README.md) | 06 | Given a real business problem, what's the right architecture and model/prompt strategy — and can you defend it? | Solution Design & Architecture + Claude Models/Prompting/Context Engineering (30%) |
| 08 | [Building and Proving It: Integration, Evaluation & Optimization](08-integration-evaluation/README.md) | 07 | Once it's built, how do you actually prove it works, and keep proving it as things change? | Integration + Evaluation/Testing/Optimization (35%) |
| 09 | [Shipping Responsibly: Governance, Stakeholders & Team Enablement](09-governance-stakeholders/README.md) | 08 | How do you ship this responsibly, and keep a team productive building on it? | Governance/Safety/Risk + Stakeholder Communication/Lifecycle + Developer Productivity (35%) |
| 10 | [Professional Capstone: Sit-Ready for CCAR-P](10-professional-capstone/README.md) | 07–09 | Are you actually ready to sit the real exam? | All 7 domains, synthesized |

## What you keep

| # | Module | Takeaway |
|---|---|---|
| 01 | Claude Code Configuration | A personal CLAUDE.md/rules/skills starter kit |
| 02 | Prompts & Structured Output | A reusable few-shot/JSON-schema template library |
| 03 | Tool & MCP Design | A tool-description checklist + a scoped `.mcp.json` template |
| 04 | Agentic Orchestration | A coordinator-subagent reference implementation |
| 05 | Context & Reliability | A context-degradation diagnostic playbook |
| 06 | Foundations Capstone | A personal CCA-F exam-day prep sheet |
| 07 | Solution Design & Context Strategy | An architecture-decision-record template |
| 08 | Integration & Evaluation | An evaluation-dataset/A-B-test harness template |
| 09 | Governance & Stakeholders | A governance/risk checklist |
| 10 | Professional Capstone | A personal CCAR-P exam-day prep sheet |

## Why this order, and why 10 modules instead of the originally-scoped 8

CCA-F's 5 domains map one module each, ordered by real technical dependency (Claude Code fluency and tool/prompt mechanics precede the agentic loop built on top of them; context management is taught last among Part 1's modules because its hardest task statements need an agent already running). CCAR-P's 7 domains don't split evenly into module-per-domain the way CCA-F's did — they cluster into 3 real thematic groups that mirror the exam's own stated solution lifecycle (design → build & validate → govern & deliver), roughly balanced by weight (30%/35%/35%). Forcing either exam's real domain count into a false 4+4 parity would have meant either merging differently-weighted domains or inventing content that isn't in the blueprint — see `docs/decisions.md`'s 2026-07-14 entries for the full correction record. Full reasoning: [`docs/workshop-design.md`](../docs/workshop-design.md).

## Gate tiers (every module uses this vocabulary)

| Tier | What it is |
|---|---|
| Deterministic (hands-on, WITH Claude Code) | A real artifact, graded against the exam guide's own "Skills in:" bullets. |
| Exam-condition (closed-book, WITHOUT Claude Code) | A timed multiple-choice checkpoint, written originally against the domain's task statements — default 10-15 questions/15-20 minutes/80% to pass, except Modules 06 and 10, which mirror the real exam's exact format as a dress rehearsal. |

Both tiers are required to advance, in sequence, per module — neither substitutes for the other. This is a stated hypothesis about what actually builds exam-day readiness, not a proven finding: see [`docs/design-tension.md`](../docs/design-tension.md).
