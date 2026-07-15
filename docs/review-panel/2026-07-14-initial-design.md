# Workshop Review Panel — Initial Design Pass

**Date:** 2026-07-14
**Scope:** post-naming, pre-build design docs — `README.md`, `docs/workshop-design.md`, `docs/design-tension.md`, `docs/decisions.md`
**Personas run:** all 7 (AI/ML Practitioner, Developer Evangelist, End-User/Learner, Professional Technical Writer, Skeptical Critic, Instructional Designer, Security-Conscious Reviewer), independent parallel subagents, no persona saw another's output before writing.
**Raw per-persona critiques:** captured in this conversation's tool output; not filed as separate persona files this run (all 7 returned non-empty, distinct findings — see synthesis below for full attribution).

Closed Book's first design-checkpoint run of this panel — a new "certification-prep" workshop shape (differentiator against a real proctoring body's own published blueprint, not community teaching material). All seven personas returned real, distinct, non-generic findings; none came back empty.

## Cross-persona agreements (highest confidence)

**1. README.md's tagline is a verified, uncorrected leftover from the pre-correction "Claude Developer" scoping — flagged independently by Developer Evangelist and Technical Writer.**
`README.md:8` still reads *"Learn Anthropic's Claude Developer certification material (Foundations to Professional)..."* — the exact claim `docs/decisions.md` and `docs/workshop-design.md` explicitly retract (no Developer-Professional exam exists; the track redirected to Architect). Verified directly against the file. The repo's front door contradicts its own decision log in the first ten seconds.

**2. The two-tier gate is described workshop-wide but never re-specified per module — flagged independently by Instructional Designer and End-User/Learner.**
No module row states its own checkpoint's question count, time limit, or pass threshold. Only the two capstones get partial numbers, and even those are inconsistent (Module 06 cites a "6-scenario/4-drawn format" that appears nowhere else in the docs — verified, this phrase is unique to that one table cell). As written, "closed-book checkpoint" is a promised category, not a buildable gate.

## Notable single-persona findings, verified or judged real

- **AI/ML Practitioner:** two prerequisite-justification sentences overstate technical relationships to support the module ordering — "tool schemas *are* structured output" conflates two distinct API mechanisms (tool `input_schema` vs. `output_config.format`), and "context management has nothing to manage until an agent exists" overreaches what Domain 5's own task statements support (conversation-context preservation and prompt caching are pre-agentic concerns).
- **Developer Evangelist:** the actual hook ("build it with the agent, then prove you don't need the agent to pass") is stated crisply in `design-tension.md` but never surfaces in the README; certification framing is fronted over the hands-on payoff; nothing to click through to yet (no module folders).
- **End-User/Learner:** the closed-book checkpoint is 100% honor-system with no suggested ritual (timer, separate device, offline file) despite the whole premise resting on genuine no-AI recall; no time-per-module estimate anywhere; Module 01 (Claude Code config) re-onboards a skill the audience section says is already assumed, with no skip-ahead path.
- **Technical Writer:** confirmed a real leftover bug — `workshop-design.md:44` contains an undefined, unexpanded "CCDV-F" (the old Developer-Foundations code) inside a sentence otherwise about the Architect track, missed by the correction pass. Also flagged the CCA-F / CCAR-P abbreviation-stem asymmetry (consistent throughout, but stems from an asymmetry in the sourced PDFs themselves, not a drift bug).
- **Skeptical Critic:** the "two-tier gate is the resolution" section header in `design-tension.md` reads as a settled-fact claim; its own hedge ("stated hypothesis, not a proven finding") doesn't appear until 20 lines later, and `decisions.md`'s ADR row drops the hedge entirely when restating the same decision. Also: an unhedged "nothing yet teaches toward that real, proctored credential" claim with no citation, inconsistent with the doc's otherwise disciplined sourcing.
- **Instructional Designer:** no stated grading authority for the hands-on tier in a self-paced, facilitator-less repo (self-check checklist vs. something else, unspecified); prerequisite chain is well-reasoned prose but has no stated enforcement mechanism — flagged as an open question, not necessarily a defect at this stage.
- **Security-Conscious Reviewer:** the "never copy real/leaked exam content" safeguard doesn't explicitly cover Anthropic's own 12 official sample questions quoted in the exam guides — "modeled on the exam guide's sample-question style" is exactly the phrasing that could be read to license paraphrasing those specific items, a real ambiguity given they're likely covered by the same NDA terms cited elsewhere. Also: no stated safe-design default (fail-closed hooks, no secrets, human approval for destructive actions) for Module 03/04's reusable hook/tool takeaway artifacts.

## Prioritized action list

1. **Fix `README.md`'s tagline** (Developer → Architect) — highest severity, cross-confirmed, front-door-visible. *(Applied this pass.)*
2. **Remove the stray "CCDV-F" reference** in `workshop-design.md:44` — verified leftover bug. *(Applied this pass.)*
3. **State a workshop-wide default checkpoint format** (question count, time, pass threshold) with per-module override language, so the two-tier gate is a buildable spec, not a category. *(Applied this pass — see `workshop-design.md` update.)*
4. **Move/restate hedges so they sit next to the claims they qualify**, not paragraphs away — `design-tension.md`'s section header and `decisions.md`'s ADR row. *(Applied this pass.)*
5. **Extend the exam-content safeguard to explicitly cover the guide's own official sample questions**, not just "the real exam" and "leaked banks." *(Applied this pass.)*
6. **Add a stated closed-book ritual suggestion** (close the Claude Code session / separate device / timer) — cheap, directly addresses the honor-system gap. *(Applied this pass.)*
7. **Add a safe-design default line for reusable hook/tool takeaways** (Module 03/04). *(Applied this pass.)*
8. **Rewrite the two overstated prerequisite-justification sentences** (Module 03, Module 05 rows) for technical precision. *(Applied this pass.)*
9. **Deferred, not fixed this pass** (real open questions, not text-level fixes): a concrete grading-authority mechanism for the hands-on tier in a self-paced repo; a prerequisite-enforcement mechanism; a time-per-module estimate (needs real content to estimate honestly); a Module-01 skip-ahead path for already-fluent learners; the README's "hook buried"/"cert-framing-dominates" framing (a fuller rewrite, appropriate for the Deliverables & branding pass, not a one-line fix). Logged in `docs/next-actions.md`.

## What this run doesn't cover

Same caveat every prior first-pass run in this pipeline has carried: this is a design-doc-stage review. Several findings (grading-authority mechanism, exercise-level safety defaults, real per-module checkpoint content) can only be fully checked once real module content exists — re-run the panel (or a scoped subset) once Deliverables & branding produces that content, per this Gremlin's own Handoff Contracts.
