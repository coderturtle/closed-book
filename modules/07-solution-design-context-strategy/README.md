# Module 07: Designing the Solution — Architecture, Models & Context Strategy

## The question this module answers

Given a real business problem, what's the right Claude-based architecture — and the right model/prompt/context strategy — to solve it, and how do you defend that choice to someone who'll ask why?

## Where it sits in the arc

Seventh module, opening Part 2 (Architect Professional). Hard prerequisite: [Module 06, Foundations Capstone](../06-foundations-capstone/README.md) — CCA-F fluency in agentic patterns and prompting is what Professional-level design judgment builds on; this module asks *which* architecture and model strategy to choose, which presumes Part 1's fluency in *how* to build any of them. Next: [Module 08, Building and Proving It](../08-integration-evaluation/README.md) — the hinge is that Module 08 evaluates the thing this module designs. See [`modules/README.md`](../README.md).

**A structural note, stated once here:** this module opens on a new shared project, `fixtures/foundry/` — not a continuation of `fixtures/resolve/`, Part 1's project. `resolve` doesn't naturally stretch to cover all seven CCAR-P Professional domains (Domain 7, Developer Productivity & Operational Enablement, above all), so Part 2 builds on Foundry, an internal AI platform team's own product, instead. See [`fixtures/foundry/SPEC.md`](../../fixtures/foundry/SPEC.md) for the full rationale. Module 07's own gate (`check_module_07`) does **not** chain back through Module 06's `resolve` gate — Module 06's own hard-prerequisite framing already establishes a learner reached here having cleared Part 1, and re-checking six already-passed `resolve` gates against an unrelated `foundry` fixture would test nothing real. Every Part 2 module chains onto `check_module_07` instead, the same role `check_module_01` played for Part 1.

## The exercise

The Helpdesk team's first instinct, on hearing about `resolve`, was "we want something like that." That instinct is the exercise. Most of the Helpdesk team's real ticket volume (~4,000/month) is single-turn structured classification — password resets, VPN access, software/hardware requests — with no genuine need for multi-step tool use or agentic autonomy. The skill this module tests is recognizing *when not to reach for the more powerful pattern*, not proving an agentic loop can be built (Part 1 already proved that).

Two real deliverables, both required:

1. **`fixtures/foundry/src/ticket_triage.py`** — implement `build_triage_prompt()` (a static, cache-friendly system prompt — IT policy text and the five category definitions, taking no arguments and returning a byte-identical string on every call) and `classify_ticket()` (a single-turn classifier that calls `model_client(system_prompt, turn_content)` with the *same* `system_prompt` on every call, including retries — retry-specific error feedback travels through `turn_content`, the dynamic per-call argument, never by mutating the system prompt). Validated by the provided test suite, `fixtures/foundry/tests/test_ticket_triage.py` (12 tests).
2. **`fixtures/foundry/docs/adr-0001-ticket-triage-architecture.md`** — a real architecture decision record: Context, Decision, Alternatives Considered (naming and rejecting the Helpdesk team's own proposed agentic alternative, with real trade-offs — not just naming it in passing), Consequences (including what the choice honestly gives up). Checked structurally by `scripts/verify_module_07.py`.

**Why cache-friendliness is a real, testable property, not a style preference:** the exam guide's own Sample Question 2 describes an application sending the same large system prompt repeatedly — this module's `classify_ticket` is built around exactly that shape. This is a deliberate contrast with Module 02's `extract_refund_request`, which regenerates its whole prompt (including the validation error) on every retry attempt — correct there, since that prompt isn't sent at the volume or reuse frequency that makes caching pay off, but wrong here, where the same static prompt is sent ~4,000 times a month and mutating it on retry would defeat the caching this exercise exists to teach. Recognizing which pattern applies where — not applying either pattern uniformly everywhere — is itself part of the module's Domain 2 skill (prompt-reuse strategy).

## Required gate

- **Deterministic tier (hands-on, with Claude Code):** `python scripts/verify_module_07.py fixtures/foundry` (or the equivalent invocation against your own working copy) must pass both halves — all 12 canonical tests, and the ADR's four required sections each present with real content. This is necessary, not sufficient: the ADR check is a coarse structural proxy (section presence, minimum length, a keyword check that "Alternatives Considered" actually names the agentic alternative) — a technically-passing ADR that mentions "agentic" in an unrelated sentence would still clear it. The module's conceptual rubric (below) is what actually judges the quality of the trade-off reasoning.
- **Exam-condition tier (closed-book, without Claude Code):** [`checkpoint.md`](checkpoint.md) — 14 originally-written multiple-choice questions covering CCAR-P Domain 1 (Solution Design & Architecture, 17%) and Domain 2 (Claude Models, Prompting & Context Engineering, 13%), 80% (12/14) to pass, closed-book and timed. Coverage is split deliberately: the hands-on artifact directly tests architectural pattern selection and context/token optimization against *one* scenario (Helpdesk triage); the checkpoint tests the remaining named objectives (translating business problems into solutions, end-to-end architecture design, multi-agent orchestration strategy, model selection trade-offs, system prompt/guardrail design, prompt-reuse strategy) using two additional scenarios the hands-on work doesn't cover, so a learner can't pass by pattern-matching one example.

## Conceptual rubric (deterministic tier's non-mechanical half)

Judged by a human reviewer or Coachgremlin against the submitted ADR and code, alongside the deterministic checks above:

1. **The alternative is actually engaged, not just named.** "Alternatives Considered" states the real trade-offs of the agentic pattern the Helpdesk team proposed (cost, latency, complexity, and what it would have bought them) — not a one-line dismissal.
2. **The cache-friendliness reasoning is present and correct**, in the ADR or code comments: why a static system prompt matters at this call volume, and why retry feedback belongs in turn content, not the system prompt.
3. **Consequences is honest about what the choice gives up** — not just what it gains. A single-turn classifier can't handle a ticket that genuinely needs multi-step investigation; the ADR should say so, even briefly, rather than presenting the decision as costless.

## Takeaway

A real, working single-turn classification service for an internal team, plus a real ADR defending an architectural choice against a stated, plausible alternative — the first artifact in Foundry, the shared project the rest of Part 2 builds on. Packaged by Coachgremlin once the rubric is met.

## Self-check before advancing

- Does `build_triage_prompt()` take any arguments? It shouldn't — check the signature, not just the behavior.
- If you print the `system_prompt` argument `classify_ticket` passes to `model_client` on a first call and on a retry after a validation failure, are they character-for-character identical? They must be.
- Does your ADR's "Alternatives Considered" section explain what the agentic alternative would have cost, not just that it was rejected?

## Stop condition

`python scripts/verify_module_07.py` passes both halves, the conceptual rubric's three criteria are met, and the closed-book checkpoint is passed at 80%+ (12/14) under real exam conditions.

---

> Authored 2026-07-17, both tiers together, following the dry run at [`runs/2026-07-17-module-07-dry-run/`](../../runs/2026-07-17-module-07-dry-run/grading.md). See [`modules/README.md`](../README.md) for workshop-wide status.
