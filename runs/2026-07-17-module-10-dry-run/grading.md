# Module 10 dry run: Professional Capstone — Sit-Ready for CCAR-P

**Date:** 2026-07-17.
**Purpose:** validate that Module 10's deterministic tier (`scripts/verify_module_10.py`) discriminates real attempts on its one hands-on deliverable — a real, written architecture defense of Foundry's own Part 2 system against a seeded stakeholder objection — and that it correctly closes Part 2's cumulative gate by chaining `check_module_09`.

## The capstone's shape, and why it's purely written this time

Every prior Part 2 module paired a code deliverable with a prose one. Module 10 is the one exception: per its own skeleton, the hands-on tier is "a real end-to-end architecture review... defended in writing against a real seeded stakeholder objection" — no new source file. This matches Module 06's own capstone precedent of closing an arc with synthesis rather than new build, adapted for what Part 2's own arc actually needs synthesized: not a diagnose-and-fix on unfamiliar code, but a defense of a real design choice across all three systems Modules 07-09 built (`ticket_triage`, `doc_qa`/`evaluation`, `governance`).

**The seeded objection:** a VP of Engineering challenges Foundry's own three-systems-instead-of-one design on cost grounds — "why not consolidate into one general-purpose assistant?" This is deliberately the mirror image of Module 07's own design tension (the Helpdesk team's instinct toward *more* architecture than needed): here the pressure runs the other way, toward consolidating *away* real, justified architectural boundaries for a plausible-sounding efficiency argument. Defending against it requires synthesizing the actual, distinct risk profile each of the three systems carries — exactly the material Modules 07-09 built.

**One required deliverable:** `fixtures/foundry/docs/capstone-architecture-defense.md`, four required sections (The Objection, Why It's a Reasonable Challenge, The Defense, What Would Change Our Mind), checked structurally via the same regex-section-extraction discipline as Module 07's `check_adr` and Module 09's `check_readiness_review`, plus two content checks: The Defense must name all three of Foundry's real systems (not read as a generic architecture essay), and What Would Change Our Mind must state a real conditional criterion (not just restate confidence in the current design).

## Attempts constructed

1. **`correct-attempt/`** — a real defense: steelmans the cost objection honestly, distinguishes duplicated infrastructure from duplicated architecture, names a real falsifiability condition (convergent problem shape, not budget pressure alone) for when consolidation would actually become correct.
2. **`no-defense-attempt/`** — the file doesn't exist at all.
3. **`generic-essay-attempt/`** — all four sections present with real prose length, but never names Foundry's actual systems (`ticket_triage`, `doc_qa`, `governance`) — a generic, could-apply-to-any-company essay about architecture in general.
4. **`no-real-criterion-attempt/`** — everything else correct, but "What Would Change Our Mind" just restates confidence in the current design rather than stating any real conditional criterion.

## Results (chains `check_module_09`, which chains `check_module_08`/`check_module_07`)

| Attempt | Defense doc | Overall |
|---|---|---|
| correct | PASS (all sections + both content checks) | **PASS** |
| no-defense | FAIL (file missing) | **FAIL** |
| generic-essay | FAIL (doesn't name real systems) | **FAIL** |
| no-real-criterion | FAIL (no real conditional criterion) | **FAIL** |

Isolation confirmed clean: `generic-essay-attempt` and `no-real-criterion-attempt` each fail exactly the one content check they were built to violate, with every structural section-presence check still passing (both attempts have real, non-trivial prose in all four sections — they're not caught by length alone).

## What this does and doesn't validate

**Validated:** the deterministic tier discriminates a missing document, a structurally-complete-but-generic document, and a structurally-complete-but-unfalsifiable document, with clean isolation; `check_module_10` correctly closes Part 2's full cumulative chain (07→08→09→10); the "names real systems" and "real conditional criterion" checks are coarse keyword/pattern proxies (disclosed as such, same discipline as every prior module's prose checker) that catch the two most likely ways a technically-present document could still fail to be a real defense.

**Not validated at time of first writing (now closed, see below):** no real learner attempt existed yet, and the mock exam had no dry-run validation beyond the authoring-time domain-tally cross-check, which caught and fixed 3 mislabeled questions (B4, D2, E4 — "risk/failure-mode identification" is a Domain 5 objective per this workshop's own established mapping from Module 09's checkpoint, not Domain 1) before publishing.

## Doubt-driven-development: three full review cycles

Per standing practice, offered before treating this module as done. Full detail in `docs/decisions.md`'s 2026-07-17 entries; summarized here.

**Self-caught, before any external review:** 39 of 40 single-answer questions had "B" as the correct letter (the same "always-one-letter" anti-pattern Module 06's own DDD had found previously) — caught via `grep`, fixed with a mechanical answer-shuffle script. That first shuffle script then corrupted 4 answer-key explanation lines via an over-broad regex (matching the English article "A" and the literal term "A/B testing"), caught via a second, targeted `grep`. No git history existed to revert to; reconstructed the pre-shuffle content from conversation context and rebuilt the shuffle with a narrower, prefix-anchored regex that never touches an explanation's leading clause.

**Stage 1 (fresh Claude subagent, ARTIFACT+CONTRACT only):** 9 findings. One (a claimed D4/F3 domain mislabel) was checked against Module 08's own established checkpoint mapping and found to be **not a bug** — classified as noise. Real and actionable: the checker's architecture-defense check could be satisfied by a throwaway one-sentence "Defense," and by a falsifiability section containing a trigger word alongside an explicit refusal to ever reconsider; the reference defense argued a false binary and never rebutted the objection's onboarding-cost sub-argument; two negative dry-run attempts didn't isolate their intended failure; one weak distractor (C3-B).

**Stage 2 (Codex, cross-model, `codex exec --sandbox read-only`):** found the reshuffled answer-key letters formed a literal repeating A,B,C,D cycle (excluding the two multiple-response questions) — predictable by position, worse than the "always B" bug caught at authoring time — and that both multiple-response questions shared the identical correct pair ("A and C"). Also found a checker-fix side effect breaking one negative fixture's isolation, the other negative fixture not actually exercising its intended bypass, a factual overstatement in the reference's steelman ("three sets of dependencies to track" against a repo with one shared `requirements.txt`), and an underspecified falsifiability condition.

**Stage 3 (Fable, critique of the Stage 1+2 remediation itself):** found the remediation's own new checks had gaps — a hollow-buzzword-listing bypass, and, more seriously, a **false-positive risk**: the fix's whole-sentence negation exclusion would incorrectly fail genuinely honest writing that states real system guarantees in negation-shaped language ("sensitive content never reaches a model call"). Also found a synonym-dodgeable falsifiability check, a self-contradiction introduced by Stage 2's own "coordinator" paragraph rewrite, a stale negative fixture, and — separate from anything introduced this round — a project-wide construct-validity issue present since original authoring: every one of the 42 questions' distractors used absolute-quantifier language ("always/never/none/exclusively") while the correct answer was consistently the hedged, trade-off-shaped option, letting a test-taker score well by surface pattern-matching alone.

**All findings from all three stages fixed and re-verified**, including — per explicit user direction, given the scale was judged worth it rather than disclosing a known-gameable exam — a full rewrite of all 42 questions' distractors across all 6 scenarios to remove the absolute-quantifier tell while preserving each option's original category of wrongness. One residual, disclosed limitation: a purely affirmative, non-negated buzzword mention (e.g., quoting a stakeholder's memo) can still pass the risk-vocabulary check — no lexical check distinguishes real engagement from name-dropping in every case; the conceptual rubric is the backstop, matching this project's established precedent for coarse prose-checker proxies.

**Final validation:** all 4 dry-run attempts isolate cleanly, including against Fable's own constructed bypass documents; zero regression across all 44 attempts project-wide; the 42-question/168-option/42-answer-key exam's structural integrity (global and per-scenario letter distribution, keyword-overlap cross-check, "A/B testing" term preservation) reconfirmed after every content change. Three-cycle stop condition met.

## Files

- `correct-attempt/`, `no-defense-attempt/`, `generic-essay-attempt/`, `no-real-criterion-attempt/` — the four constructed attempts, full project copies (each carrying Modules 07-09's own completed work, since the gate chains through all three).
- `scripts/verify_module_10.py` — the deterministic checker: chains `check_module_09`, regex-based structural + content checks on the architecture defense document.
- `modules/10-professional-capstone/checkpoint.md` — the 42-question, 6-scenario mock exam.
