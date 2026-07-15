# Maintainers

This is the internal/agent-facing doc. Learners should read the top-level `README.md` instead; this file is for anyone working on the workshop itself.

**Classification:** factory-output
**Lifecycle:** active
**Owner:** coderturtle
**Promotion target:** `none`

This repo has two goals:

1. **Ship a workshop** teaching Anthropic's Claude Certified Architect material (Foundations then Professional) to agent-literate practitioners, taught by building every exercise hands-on through Claude Code, then checking recall closed-book against a practice checkpoint modeled on the exam's own published blueprint.
2. **Test a new curriculum-anchor shape for the Workshop Gremlin pipeline**: this is the pipeline's first run anchored against a certifying body's own primary-source exam guide (not community teaching material, per Terminal Velocity/Borrow Native's precedent) and its first run where the teaching *method* (agent-native) is in deliberate, named tension with the target *evaluation condition* (closed-book, no AI). See `docs/design-tension.md` for the tension and `~/hekton/gremlins/workshop/workshop-gremlin.md` for whether this becomes a documented variant.

## Implementation Status

- 2026-07-14 — Scaffolded as factory-output (as `claude-cert-workshop`). Naming pass complete: **Closed Book**.
- **Correction, same day:** original scope ("Claude Developer, Foundations → Professional") redirected to **Claude Architect** — no Developer-Professional exam exists. See `docs/decisions.md`.
- Design docs complete: [Workshop Design](workshop-design.md) (audience, two-tier gate method, 10-module arc anchored to Anthropic's own CCA-F/CCAR-P exam guide PDFs) and [Design Tension](design-tension.md) (the learn-with-AI/test-without-AI tension, named and resolved via the two-tier gate).
- First [Workshop Review Panel](review-panel/2026-07-14-initial-design.md) run complete against the design docs — all seven personas returned distinct findings; the cheap, design-doc-text fixes were applied in the same pass (see that report's prioritized action list for what was fixed vs. deferred).
- Module skeleton (`modules/`, 10 modules + index), brand layer (`docs/brand.md`), and this maintainers split are done. Build-log/Pages site is the remaining Completion Condition item — see [Next Actions](next-actions.md).

## Documentation Contract

Agents working here must inspect `.hekton/project.yaml` before structural changes, keep `docs/session-log.md` current, record meaningful design decisions in `docs/decisions.md`, and update `docs/next-actions.md` when the work queue changes.

Vault mutation policy: see `vault_mutation_allowed` in `.hekton/project.yaml` (authoritative). The repo-local `mind-palace/` folder is only a mirror draft; do not write to the live vault unless explicitly authorised in-session.

## Voice and style for published content

Anything a learner reads (README, module content, build-log entries, the site once built) follows `docs/brand.md` — voice, hard rules (no em dashes, no efficacy guarantees, no implied Anthropic affiliation), banned phrases. Internal docs under `docs/` are working documents and are exempt.

## A standing constraint every future session must respect

Practice/quiz questions for every module are written originally against Anthropic's published exam guides, never copied or lightly reworded from the real exam, any leaked/scraped item bank, or Anthropic's own official sample questions. See `docs/design-tension.md`'s Constraint section before authoring any closed-book checkpoint content.

## Key Docs

- [Workshop Design](workshop-design.md) — audience, format, two-tier gate teaching method, certification-anchored module arc
- [Design Tension](design-tension.md) — the learn-with-AI/test-without-AI tension and its resolution
- [Brand / Style Layer](brand.md) — voice, hard rules, visual identity
- [Workshop Review Panel Report](review-panel/2026-07-14-initial-design.md) — 7-persona critique of the naming + design docs, first run
- [Modules index](../modules/README.md) — the full arc, gate tiers, and per-module skeleton status
- [Session Log](session-log.md)
- [Decisions](decisions.md)
- [Risks](risks.md)
- [Project Walkthrough](project-walkthrough.md)
- [Next Actions](next-actions.md)
- [Operating Model](operating-model.md)
- [Human Understanding Check](human-understanding-check.md)
- [Depth Decision](depth-decision.md)
- [Retire / Promote Review](retire-promote-review.md)
