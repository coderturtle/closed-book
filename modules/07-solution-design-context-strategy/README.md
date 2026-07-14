# Module 07: Designing the Solution — Architecture, Models & Context Strategy

## The question this module answers

Given a real business problem, what's the right Claude-based architecture — and the right model/prompt/context strategy — to solve it, and how do you defend that choice to someone who'll ask why?

## Where it sits in the arc

Seventh module, opening Part 2 (Architect Professional). Hard prerequisite: [Module 06, Foundations Capstone](../06-foundations-capstone/README.md) — CCA-F fluency in agentic patterns and prompting is what Professional-level design judgment builds on; this module asks *which* architecture and model strategy to choose, which presumes Part 1's fluency in *how* to build any of them. Next: [Module 08, Building and Proving It](../08-integration-evaluation/README.md) — the hinge is that Module 08 evaluates the thing this module designs. See [`modules/README.md`](../README.md).

## Learning objectives (placeholder — finalized when content is authored)

- Translate a stated business problem into a Claude-based solution shape, choosing correctly between workflow, agentic, and augmented-LLM architectural patterns.
- Select an appropriate Claude model given real trade-offs (capability, latency, cost).
- Design system prompts, templates, and guardrails, applying zero-shot/few-shot/chain-of-thought technique correctly to the problem at hand.
- Apply prompt-reuse strategy (caching, modular prompts, Skills) to a design with real cost/latency constraints.

## Exercise material to draw from (not a spec — Coachgremlin authors the real exercise later)

Real material this module's exercise should be built from: CCAR-P Exam Guide Domain 1 (Solution Design & Architecture, 17%) and Domain 2 (Claude Models, Prompting & Context Engineering, 13%) — their full listed objectives (translating business problems into solutions, end-to-end architecture design, architectural pattern selection, multi-agent orchestration strategy, model selection trade-offs, system prompt/guardrail design, context/token optimization, prompt-reuse strategy). The guide's own Sample 2 ("An application sends the same 8,000-token system prompt...") is a real, usable anchor. See [`docs/workshop-design.md`](../../docs/workshop-design.md).

## Required gate (placeholder — shape decided now, real rubric written later)

- **Deterministic tier (hands-on, with Claude Code):** a real architecture proposal for a stated business problem — pattern choice, model selection with stated trade-offs, and a working prompt/context strategy (including a real prompt-caching decision), built and demonstrated, not just described.
- **Exam-condition tier (closed-book, without Claude Code):** a timed multiple-choice checkpoint against Domains 1 and 2's combined task statements. Default format: 10–15 questions, 15–20 minutes, 80% to pass.

## Takeaway

An architecture-decision-record template scoped to Claude solution design — capturing the pattern/model/prompt-strategy choices made and why, reusable on the learner's next real project. Packaged by Coachgremlin once the rubric is met.

## Stop condition (placeholder)

The learner's architecture proposal is real, defensible against a stated alternative, and Coachgremlin confirms the closed-book checkpoint was passed at 80%+ under real exam conditions.

---

> **Skeleton only.** This module has a decided question, arc position, gate shape, and takeaway shape. It has no authored exercise, fixture, or closed-book question bank yet — that's Coachgremlin's job, run later. See [`modules/README.md`](../README.md) for workshop-wide status.
