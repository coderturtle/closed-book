# Module 10: Professional Capstone — Sit-Ready for CCAR-P

## The question this module answers

Are you actually ready to sit the real Claude Certified Architect – Professional exam?

## Where it sits in the arc

Tenth and final module, closing Part 2 (Architect Professional) — and this workshop's whole arc — in full. Hard prerequisite: all of [Module 07](../07-solution-design-context-strategy/README.md)–[Module 09](../09-governance-stakeholders/README.md) — this module synthesizes all seven CCAR-P domains rather than testing any one in isolation. See [`modules/README.md`](../README.md).

`scripts/verify_module_10.py` chains `check_module_09` (which chains `check_module_08`, which chains `check_module_07`) — the final link in Part 2's cumulative gate.

## The exercise

Every prior Part 2 module paired a code deliverable with a prose one. This one is purely written — there's no new source file, because the capstone's job is synthesis, not new build. You've built three real systems across Modules 07-09: `ticket_triage` (a cache-friendly single-turn classifier for the Helpdesk team), `doc_qa`/`evaluation` (a RAG documentation Q&A system for the Platform Docs team, with a real evaluation harness), and `governance` (a human-in-the-loop compliance gate wrapping `doc_qa`).

A VP of Engineering raises a real challenge: **why not consolidate these three systems into one general-purpose internal assistant?** Fewer codebases, fewer onboarding surfaces, less duplicated infrastructure. This is the deliberate mirror image of Module 07's own design tension — there, the pressure was toward *more* architecture than the Helpdesk team's problem actually needed; here, the pressure runs the other way, toward consolidating *away* real, justified architectural boundaries for a plausible-sounding efficiency argument.

**One required deliverable:** `fixtures/foundry/docs/capstone-architecture-defense.md`, with four required sections:

1. **The Objection** — state the VP's real challenge, in their own terms.
2. **Why It's a Reasonable Challenge** — steelman it honestly. The cost argument is real; don't dismiss it.
3. **The Defense** — the real architectural reasoning for why `ticket_triage`, `doc_qa`, and `governance` remain genuinely separate systems, grounded in what Modules 07-09 actually established about each one's distinct risk profile. Must name all three systems specifically — a generic essay about "architecture in general" isn't a defense of *this* architecture.
4. **What Would Change Our Mind** — a real, falsifiable condition under which consolidation would become the *right* call, not just a cheaper one. Budget pressure alone isn't a sufficient trigger; a genuine convergence in problem shape is.

Checked by `scripts/verify_module_10.py` via the same regex-section-extraction discipline as Module 07's ADR checker and Module 09's shipping-readiness-review checker — necessary, not sufficient. A technically-structured document that never actually engages with Foundry's own three systems, or that states no real falsifiability condition, is exactly the failure mode a constructed dry-run attempt (`generic-essay-attempt`, `no-real-criterion-attempt`) proves the checker catches — but the conceptual rubric below is what judges whether the *reasoning* is actually good, not just present.

## Required gate

- **Deterministic tier (hands-on, with Claude Code):** `python scripts/verify_module_10.py fixtures/foundry` must pass the architecture defense's structural and content checks, and Module 09's own chained gate (which chains 08, which chains 07).
- **Exam-condition tier (closed-book, without Claude Code):** [`checkpoint.md`](checkpoint.md) — like Module 06, this is the one module where the checkpoint format matches the real exam's own scale rather than the workshop's smaller per-module default: a 6-scenario pool (42 originally-written questions, including 2 multiple-response items), complete 4 of 6, 120 minutes, 720/1000 to pass.

## Conceptual rubric (deterministic tier's non-mechanical half)

1. **The objection is actually engaged, not strawmanned.** A learner's own defense should make the VP's cost argument as strong as it honestly is before countering it — the same "engage the real alternative, not a weak version of it" discipline Module 07's own ADR rubric applies to the Helpdesk team's agentic-loop proposal.
2. **The defense is specific to these three systems' real risk profiles, not architecture platitudes.** "Different systems solve different problems" is true of almost anything; a real defense names *which* risk each system's separation actually protects against (classification error vs. stale-retrieval error vs. undetected compliance violation).
3. **The falsifiability condition is genuinely falsifiable.** A learner should be able to say, concretely, what observed evidence would flip their own conclusion — not just restate confidence in the current design with different words.

## Takeaway

A personal CCAR-P exam-day prep sheet, same discipline as Module 06's — built from this specific attempt's actual weak spots (which domains and scenarios the mock exam actually missed), not a generic study guide. Packaged by Coachgremlin once the rubric is met.

## Self-check before advancing

- Could you explain, out loud, to someone who's never seen this codebase, *why* `ticket_triage` and `doc_qa` are separate systems rather than one system with two modes?
- Does your "What Would Change Our Mind" section name a condition you could actually observe happening, or does it just restate that you're confident in the current design?
- If a real stakeholder pushed back on your defense in a live conversation, do you have a real answer, or only a written one you haven't pressure-tested?

## Stop condition

The learner's stakeholder-objection defense is real and specific (`python scripts/verify_module_10.py` passes, and the conceptual rubric's three criteria are met), the mock exam is completed at real pacing and scored, and Coachgremlin confirms both before this module — and the workshop — counts as done. Passing the mock exam is not the same claim as passing the real one — see [`docs/workshop-design.md`](../../docs/workshop-design.md)'s dogfooding commitment for how this workshop tests that claim for real.

---

> Authored 2026-07-17, both tiers together, following the dry run at [`runs/2026-07-17-module-10-dry-run/`](../../runs/2026-07-17-module-10-dry-run/grading.md). See [`modules/README.md`](../README.md) for workshop-wide status.
