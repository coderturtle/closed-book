# Module 08: Building and Proving It — Integration, Evaluation & Optimization

## The question this module answers

Once it's built, how do you actually prove it works, and keep proving it as things change?

## Where it sits in the arc

Eighth module. Hard prerequisite: [Module 07, Designing the Solution](../07-solution-design-context-strategy/README.md) — this module evaluates and integrates the architecture Module 07 designed; there's nothing real to test or connect to production systems until a design exists. Next: [Module 09, Shipping Responsibly](../09-governance-stakeholders/README.md) — the hinge is that governance and delivery apply to a system that's been built and evaluated, not a proposal. See [`modules/README.md`](../README.md).

## Learning objectives (placeholder — finalized when content is authored)

- Design a RAG pipeline with a chunking/indexing strategy matched to the data shape and query pattern at hand.
- Select the correct integration mechanism (MCP, API/CLI, agent-to-agent) for a stated system, with the trade-offs named.
- Define evaluation metrics (accuracy, latency, cost, safety, security) and build a mixed-methodology evaluation dataset.
- Diagnose a real system failure (prompt failure vs. hallucination vs. model mismatch vs. stale retrieval) from symptoms alone.

## Exercise material to draw from (not a spec — Coachgremlin authors the real exercise later)

Real material this module's exercise should be built from: CCAR-P Exam Guide Domain 3 (Integration, 19%) and Domain 4 (Evaluation, Testing & Optimization, 16%) — their full listed objectives (tool/agent capability-bloat evaluation, auth/security-gap analysis, accuracy-latency trade-offs, observability at scale, RAG pipeline design, connection-protocol selection, evaluation metric design, A/B testing, diagnosing system issues, cost/latency optimization). The guide's own Sample 1 (least-privilege tool scoping) and Sample 3 (RAG returning confident-but-wrong answers after a document refresh) are real, usable anchors. See [`docs/workshop-design.md`](../../docs/workshop-design.md).

## Required gate (placeholder — shape decided now, real rubric written later)

- **Deterministic tier (hands-on, with Claude Code):** a real evaluation harness (dataset + metrics + at least one A/B comparison) run against Module 07's design, plus a diagnosed-and-fixed real failure scenario (e.g. a deliberately staled RAG index).
- **Exam-condition tier (closed-book, without Claude Code):** a timed multiple-choice checkpoint against Domains 3 and 4's combined task statements. Default format: 10–15 questions, 15–20 minutes, 80% to pass.

## Takeaway

An evaluation-dataset/A-B-test harness template — reusable on the learner's next real system, built from a real diagnosed failure rather than a synthetic example. Packaged by Coachgremlin once the rubric is met.

## Stop condition (placeholder)

The learner's evaluation harness produces a real result, the diagnosed failure is correctly root-caused and fixed, and Coachgremlin confirms the closed-book checkpoint was passed at 80%+ under real exam conditions.

---

> **Skeleton only.** This module has a decided question, arc position, gate shape, and takeaway shape. It has no authored exercise, fixture, or closed-book question bank yet — that's Coachgremlin's job, run later. See [`modules/README.md`](../README.md) for workshop-wide status.
