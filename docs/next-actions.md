# Next Actions: Closed Book

## Immediate

- [x] Build module/deliverables skeleton (10 module READMEs + brand layer), per `docs/workshop-design.md`'s arc
- [x] Stand up build-log/Pages site skeleton (Astro-on-Pages, adapted from Borrow Native's pipeline)
- [x] Coachgremlin: author Module 01 for real (exercise, rubric, deterministic checker, dry run) — done 2026-07-15
- [x] Doubt-driven-development review of Module 01 (fresh Claude subagent + Codex + Fable replan) — done 2026-07-15, findings and full remediation recorded in `docs/decisions.md`
- [x] Author Module 01's closed-book checkpoint (`checkpoint.md`, 12 questions, full Domain 3 coverage) — done 2026-07-15, was previously missing entirely
- [x] Rewrite `verify_module_01.py` in Python, fixing portability/scoping/path-escape bugs — done 2026-07-15
- [x] A fourth dry-run attempt for Module 01 that passes the deterministic tier but is conceptually weak — done 2026-07-15 (`weak-conceptual-attempt`), confirms rubric criteria 2-4 catch what the checker structurally can't
- [x] Coachgremlin: author Module 02 (Prompts and Structured Output), continuing the `resolve` project — done 2026-07-15, both tiers built together from the start this time.
- [x] Wire the cumulative-gate convention for real (`verify_module_02.py` imports and calls `check_module_01`) — done 2026-07-15, isolation-tested (fails correctly when Module 01's config is absent, before pytest even runs).
- [x] Doubt-driven-development review of Module 02 (fresh Claude subagent + Codex with live web search + Fable replan) — done 2026-07-15. Dominant finding: the exercise interface never actually required the prompt/few-shot artifact 2 rubric criteria graded. Fixed by adding `build_extraction_prompt`/`FEW_SHOT_EXAMPLES` as real exercise deliverables, not by weakening the rubric. Full record in `docs/decisions.md`.
- [x] A 4th dry-run attempt for Module 02 that passes the full test suite but is conceptually weak — done 2026-07-15 (`weak-few-shot-attempt`, clean-only few-shot examples), confirms rubric criterion 3 catches what the 14-test deterministic suite structurally can't.
- [ ] Module 02 rubric criterion 4 (documented reason `refund_amount_cents` is nullable) still has no constructed dry-run attempt that isolates it in particular — logged in `runs/2026-07-15-module-02-dry-run/grading.md`'s "not yet validated" note.
- [x] Coachgremlin: author Module 03 (Designing Tools and MCP Interfaces), continuing `resolve` — done 2026-07-15, both tiers together, applying Modules 01-02's lessons proactively (docstring-presence check designed deterministic from the start, not found conceptual-then-fixed after a review).
- [ ] Doubt-driven-development review of Module 03 — not yet run this pass; ask before invoking Codex again (each invocation needs its own turn's authorization per the skill's own rule).
- [ ] Module 03 rubric criterion 4 (process_refund's defense-in-depth reasoning documented as deliberate) has no constructed dry-run attempt isolating it specifically — logged in `runs/2026-07-15-module-03-dry-run/grading.md`.
- [ ] Coachgremlin: author Module 04 (Agentic Loops and Multi-Agent Orchestration), continuing `resolve` — both tiers together. This is where the coordinator agent and the real hook enforcing verify-before-refund first exist; Module 03's own `process_refund` defense-in-depth becomes testable as a *second* layer alongside it, not the only layer.
- [ ] A real learner (not just constructed attempts) needed before this workshop's two-tier gate hypothesis has any evidence beyond self-constructed dry runs
- [ ] `fixtures/resolve/requirements.txt` (pytest) has no documented venv-setup step in the module READMEs yet beyond `SPEC.md`'s "Running it" section — consider whether this belongs in the top-level README's prerequisites too, before Module 03 adds more dependencies

## This Week

- [ ] Deferred from the 2026-07-14 Review Panel pass (`docs/review-panel/2026-07-14-initial-design.md`), real open questions not fixable as design-doc text:
  - [ ] Concrete grading-authority mechanism for the hands-on tier in a self-paced, facilitator-less repo (self-check checklist vs. something else — currently stated as "self-graded via checklist," needs a real decision on whether that's sufficient)
  - [ ] Prerequisite-enforcement mechanism (currently prose-only reasoning, no technical gate preventing skipping ahead)
  - [ ] Time-per-module estimate (needs real content to estimate honestly)
  - [ ] Module 01 skip-ahead path for learners already fluent in Claude Code configuration
  - [ ] README's learner-facing rewrite (lead with the hands-on payoff, not the certification framing; split internal Hekton framing into `docs/maintainers.md`) — belongs to the Deliverables & branding pass, not a standalone fix
- [ ] Re-run the Workshop Review Panel (or a scoped subset) once Deliverables & branding produces real module content — several findings can only be checked against actual exercises

## Later

- [ ] Schedule and sit the real CCA-F exam once Modules 01-06 exist (dogfooding commitment, `docs/workshop-design.md`)
- [ ] Schedule and sit the real CCAR-P exam once Modules 07-10 exist
- [ ] Get a human to enable GitHub Pages and trigger the first real deploy (human-confirmed gate, matches Terminal Velocity/Borrow Native precedent)
- [ ] Confirm the first push to the public GitHub remote (`git push -u origin main`) — currently created but not pushed, per the Human Gate
- [ ] Factory-wide: audit whether other Hekton-scaffolded repos' `CLAUDE.md` files have the same unconditional "close every session by running end-session.sh" instruction that caused a read-only Codex review agent to attempt writing during this workshop's doubt-driven-development pass (fixed locally here 2026-07-15; not fixed at the `~/hekton` scaffold-template level, out of scope for this repo's own session)
