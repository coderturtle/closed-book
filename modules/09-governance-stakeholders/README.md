# Module 09: Shipping Responsibly — Governance, Stakeholders & Team Enablement

## The question this module answers

How do you ship this responsibly, and keep a team productive building on it, once "does it work" has already been answered?

## Where it sits in the arc

Ninth module. Hard prerequisite: [Module 08, Building and Proving It](../08-integration-evaluation/README.md) — governance and delivery apply to a system that's been built and evaluated; there's nothing real to govern or hand off until Module 08's evaluation exists. Next: [Module 10, Professional Capstone](../10-professional-capstone/README.md). See [`modules/README.md`](../README.md).

`scripts/verify_module_09.py` chains `check_module_08` (which chains `check_module_07`) — Foundry's own cumulative-gate convention within Part 2.

## The exercise

Every module since Module 07 opened on a new internal team's problem. This one doesn't — it asks what has to happen *before* Module 08's own system (the Platform Docs team's `doc_qa` RAG pipeline) actually ships to real users. That's the real shape of Domain 5 (Governance, Safety & Risk), Domain 6 (Stakeholder Communication & Lifecycle), and Domain 7 (Developer Productivity & Operational Enablement) combined: governance and stakeholder communication apply to a system that already exists and has already been evaluated, not a hypothetical one.

Three real deliverables, all required:

1. **`fixtures/foundry/src/governance.py`** (build-from-stub) — a human-in-the-loop gate in front of `doc_qa.answer_question`. The Platform Docs team's own corpus includes security runbooks and credential-rotation procedures that reference genuinely sensitive content (API keys, passwords, SSNs in old incident writeups) as a byproduct of documenting real incidents. Shipping `answer_question` as-is means any retrieved sensitive content goes straight into a model call. Implement `answer_question_with_governance`, which inspects retrieved chunks for sensitive content *before* ever calling `model_client`, withholding the answer entirely when flagged — the same "don't call the tool until verified" discipline as `resolve`'s own `verify_before_refund_hook` from Part 1's Module 04, applied to content sensitivity instead of customer identity. And `approve_and_release`, which requires a real, non-empty `approver_id` (a genuine audit trail — who approved this, not just that someone did) before releasing the real answer.
2. **`fixtures/foundry/docs/shipping-readiness-review.md`** — a real, structurally-checked stakeholder-facing document: Failure Modes, Compliance Requirement and Architectural Consequence, Human-in-the-Loop Checkpoint, Stakeholder Summary. Same regex-section-checking discipline as Module 07's ADR — necessary, not sufficient; the conceptual rubric below is what judges whether the reasoning is actually good.
3. **`fixtures/foundry/.claude/`** — real team tooling configuration for `fixtures/foundry/` itself (Domain 7's own objective), reusing Module 01's exercise shape in a new project: rules scoping real `src/**` and `tests/**` content, plus a project-scoped slash command.

**Why the order of operations matters, not just the final result:** a `governance.py` that calls `model_client` first and only checks sensitivity afterward can produce an identical-looking `GovernedAnswer` (answer nulled out, `requires_human_review=True`) to a correct implementation — but the actual compliance violation (sensitive content reaching a model call) has already happened by the time the function decides to withhold the result. This is a real, constructed dry-run attempt (`bypasses-model-client-attempt`), not a hypothetical — see `runs/2026-07-17-module-09-dry-run/grading.md`.

## Required gate

- **Deterministic tier (hands-on, with Claude Code):** `python scripts/verify_module_09.py fixtures/foundry` must pass all 17 tests, the shipping-readiness review's structural check, the `.claude/` team-tooling check, and Module 08's own chained gate.
- **Exam-condition tier (closed-book, without Claude Code):** [`checkpoint.md`](checkpoint.md) — 14 originally-written multiple-choice questions covering CCAR-P Domain 5 (Governance, Safety & Risk, 14%), Domain 6 (Stakeholder Communication & Lifecycle, 14%), and Domain 7 (Developer Productivity & Operational Enablement, 7%), 80% (12/14) to pass, closed-book and timed.

## Conceptual rubric (deterministic tier's non-mechanical half)

1. **The call-order property is explained, not just implemented.** A learner can state *why* checking sensitivity before calling `model_client` matters, distinct from an implementation that merely returns the correct-looking withheld result — the `bypasses-model-client-attempt` gap, in their own words.
2. **The compliance consequence is architectural, not just written down.** The shipping-readiness review's "Compliance Requirement and Architectural Consequence" section should describe a real code-level change the requirement forced (the governance gate itself), not a policy statement that sits alongside unchanged code.
3. **The team-tooling rules are genuinely useful, not decorative.** A learner should be able to explain what a new Foundry engineer, unfamiliar with this codebase, would actually learn from the `.claude/rules/` they wrote — not just that the glob patterns technically match files.

## Takeaway

A real human-in-the-loop governance gate wired into a real system, a real stakeholder-facing shipping-readiness review, and real team tooling configuration — all three reusable on the learner's next real system, built from something that was actually shipped rather than a generic template. Packaged by Coachgremlin once the rubric is met.

## Self-check before advancing

- Does your `governance.py` call `retrieve` and check sensitivity *before* any call to `model_client`, or does it call `answer_question` first and check afterward?
- Would a new Foundry engineer reading only your `.claude/rules/` files understand something true and useful about this codebase they didn't already know?
- Does your shipping-readiness review's "Compliance Requirement and Architectural Consequence" section name a specific code change, or could it be deleted without anything in `governance.py` needing to change?

## Stop condition

`python scripts/verify_module_09.py` passes all three deliverables and Module 08's chained gate, the conceptual rubric's three criteria are met, and the closed-book checkpoint is passed at 80%+ (12/14) under real exam conditions.

---

> Authored 2026-07-17, both tiers together, following the dry run at [`runs/2026-07-17-module-09-dry-run/`](../../runs/2026-07-17-module-09-dry-run/grading.md). See [`modules/README.md`](../README.md) for workshop-wide status.
