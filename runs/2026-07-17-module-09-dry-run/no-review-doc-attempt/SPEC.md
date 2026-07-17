# Spec: `foundry`

This is the authoritative spec for `foundry`, the one project every module in Part 2 of Closed Book's arc (Modules 07-10, Architect Professional) builds a real capability onto. Keep this file as the single source of truth; don't restate the product pitch differently inside a module README.

**Why a new shared project, not a continuation of `resolve`:** `resolve` (Part 1's shared project, `fixtures/resolve/`) is a real but single-purpose system: one customer-facing agent, one internal team building it. CCAR-P's own 7 Professional domains — solution design, models/context strategy, integration, evaluation, governance, stakeholder communication, and **developer productivity & operational enablement** — are architect-level judgment and organizational skills a single customer-facing product has no natural room for, Domain 7 above all: it's specifically about a platform team enabling *other* teams, which `resolve`'s own team-of-one framing structurally can't provide a home for without distorting the story. Two alternatives were considered and rejected: keep extending `resolve` with more code (would force artificial code onto domains that are really about judgment and communication, per Domain 6/7's own actual content), and scale `resolve` up in place to "enterprise" size (keeps a single-customer-type framing that still can't naturally host Domain 7's multi-team enablement material). See `docs/decisions.md`'s 2026-07-17 entry for the full reasoning.

## The product

`foundry` is an internal AI platform team's own product: the team and tooling that lets *other* engineering teams at the company adopt Claude Code and the Agent SDK safely and effectively. Foundry doesn't build one product for one team — it designs, integrates, evaluates, governs, and supports Claude-based solutions **for** many internal teams, each bringing a different real business problem to Foundry's door.

Every module in Part 2 builds a real capability into Foundry's own toolkit by solving one internal team's real, stated problem — the same "one shared project, one real capability per module, incrementally" discipline Part 1 used for `resolve`, adapted for what Professional-level work actually looks like: Part 1's modules mostly added *code*; Part 2's modules mostly add *defensible decisions with the working artifacts that demonstrate them* — an architecture proposal that's actually built and runs, not just described, per each module's own stated gate (see each module's README for its own "built and demonstrated" requirement).

**The canonical throughline, stated once:** an internal team shows up with a real problem, and Foundry has to make a real, defensible choice — not the maximal-complexity choice, not the choice that reuses the last team's exact solution regardless of fit — every time, and be able to explain *why* to the requesting team's own stakeholders, who will ask. Every module's specific artifact is an *instance* of this discipline, not a competing rule of its own — the same convention `resolve`'s own `SPEC.md` established for Part 1's canonical safety rule.

## Compatibility contract

Same conventions Part 1 established for `resolve`, carried forward rather than re-litigated: each module's checker is the *only* thing a later module may assume from an arbitrary passing submission (see `fixtures/resolve/SPEC.md`'s own compatibility-contract section for the full statement of this principle — it applies here unchanged). Cumulative-gate chaining, the shared `CheckResult` shape, and canonical-test execution (a checker runs the repo's own copy of a test file, never the submission's) all apply to `foundry`'s own checkers exactly as they did to `resolve`'s, starting from `verify_module_07.py`.

**One deliberate difference from `resolve`'s own convention, stated explicitly:** `resolve`'s modules chained *every* prior module's checker (`verify_module_04` called `check_module_03`, and so on back to `check_module_01`). `foundry`'s modules chain every prior *Part 2* module's checker (`verify_module_08` will call `check_module_07`), but do **not** chain back through Part 1's `check_module_06`/`resolve` gate — a learner arriving at Module 07 has already cleared all of Part 1 to get here (Module 06's own hard-prerequisite framing establishes this), and `foundry` is a structurally separate project from `resolve`, not a continuation of the same codebase. Re-validating six already-passed Part 1 gates against an unrelated Part 2 fixture would test nothing real.

## Feature build-out (one module, one internal team's problem, in order)

| # | Module | Internal team & problem | Capability added to Foundry | Status |
|---|---|---|---|---|
| 07 | Designing the Solution: Architecture, Models & Context Strategy | The IT Helpdesk team: thousands of repetitive internal tickets (password resets, VPN access, software requests) need automated triage, and the team doesn't know if they need "an agent" or something much simpler | A real, working ticket-triage classifier (`src/ticket_triage.py`) with a deliberately cache-friendly prompt structure, plus a real architecture decision record defending the pattern and model choice against a stated, more-complex alternative | Authored, dry-run validated (5 attempts, see `runs/2026-07-17-module-07-dry-run/`) |
| 08 | Building and Proving It: Integration, Evaluation & Optimization | The Platform Docs team: employees ask ad hoc questions about internal engineering docs (runbooks, onboarding guides), and a prototype gave a confidently wrong answer using an outdated procedure after a revision | A real documentation Q&A system (`src/doc_qa.py`) with a diagnosed-and-fixed stale-retrieval defect, plus a real evaluation harness with an A/B comparison (`src/evaluation.py`) | Authored, dry-run validated (5 attempts, see `runs/2026-07-17-module-08-dry-run/`) |
| 09 | Shipping Responsibly: Governance, Stakeholders & Team Enablement | Not yet decided | Not yet decided | Not started |
| 10 | Professional Capstone | all of 07-09 | A real end-to-end architecture review, defended in writing against a stakeholder objection | Not started |

## Module 07: the IT Helpdesk team's ticket-triage problem

### The problem, as the Helpdesk team actually stated it

The Helpdesk team handles roughly 4,000 internal IT tickets a month. Most are one of a small number of recurring categories (password reset, VPN/network access, software install/license request, hardware request, "other"). They've heard about `resolve` (Part 1's multi-tool agentic coordinator) and their first instinct is "we want that, but for IT tickets" — a full agentic loop with tools that look up account status, reset credentials, and escalate. Foundry's job is to determine whether that's actually the right architecture for *this* problem, not to build whatever the requesting team happened to ask for by name.

**The real design tension this module's exercise is built around:** most of these tickets are single-turn, structured classification-and-routing decisions with no real need for multi-step tool use, memory across turns, or agentic autonomy — the kind of problem a well-designed prompt (or a short workflow) solves correctly, cheaply, and predictably, where a full agentic architecture would add latency, cost, and failure surface for no real benefit. Recognizing *when not to reach for the most powerful pattern* is itself the CCAR-P skill Domain 1 tests (architectural pattern selection among workflow / augmented-LLM / agentic, not just "how to build an agent").

### What's already here

`src/ticket_triage.py` (Module 07, stub — both functions raise `NotImplementedError`), `src/doc_qa.py` (Module 08, ships mostly working with one seeded defect) and `src/evaluation.py` (Module 08, stub), `tests/test_ticket_triage.py` (20 canonical tests) and `tests/test_doc_qa.py` (34 canonical tests), `docs/adr-0001-ticket-triage-architecture.md` (learner-authored deliverable, not shipped). Checked by `scripts/verify_module_07.py` and `scripts/verify_module_08.py`.

### The exercise (see `modules/07-solution-design-context-strategy/README.md` for the full rubric)

Two real, gradeable deliverables, not one:
1. **A working ticket-triage classifier** (`src/ticket_triage.py`): given a raw ticket message, classify it into the Helpdesk team's real categories with a structured, schema-validated result — built with a deliberately cache-friendly prompt structure (the large, static "IT policy and category definitions" content isolated from the small, per-ticket dynamic content), since the exam guide's own Sample Question 2 (a large, repeatedly-sent static system prompt) is exactly this shape.
2. **A real architecture decision record** defending the chosen pattern (workflow/augmented-LLM, not a full agentic loop) and model tier against the Helpdesk team's own stated alternative ("we want something like `resolve`"), with real trade-offs named (cost, latency, failure surface) rather than asserted.

### The actual point of this exercise

See `runs/` for the real dry run and its findings once authored, and `modules/07-solution-design-context-strategy/README.md` for the full rubric.

## Module 08: the Platform Docs team's documentation Q&A problem

### The problem, as the Platform Docs team actually stated it

Employees keep asking the same "how do I..." questions about internal engineering docs (deploy runbooks, onboarding guides) in Slack, and the docs themselves change over time as procedures get revised. An early prototype the Platform Docs team built on their own gave a confidently wrong answer to "how do we roll back a deploy" — it cited an outdated runbook procedure, because the prototype's index was never refreshed after the runbook was revised. This is a genuine RAG use case, unlike Module 07's ticket triage: the corpus is large, it changes, and a correct answer depends on retrieving whichever version of a document is *current*.

**The real design tension this module's exercise is built around:** Module 07 taught recognizing when *not* to reach for a retrieval-heavy pattern; this module teaches the complementary skill — recognizing when RAG genuinely is the right call, and then building and *proving* it works, including proving it keeps working as the underlying documents change. The exam guide's own Sample Question 3 (a RAG system returning confident-but-wrong answers after a document refresh) is this module's real anchor.

### What's already here

`src/doc_qa.py` (ships mostly working — chunking, indexing, retrieval, and grounded answer generation are all correct as shipped; `refresh_index` has one seeded defect to diagnose and fix), `src/evaluation.py` (stub — `evaluate`/`compare_top_k` both raise `NotImplementedError`), `tests/test_doc_qa.py` (34 canonical tests, grew from 21 via doubt-driven-development). Checked by `scripts/verify_module_08.py`, which chains `check_module_07`.

### The exercise (see `modules/08-integration-evaluation/README.md` for the full rubric)

Two real, gradeable, deliberately independent deliverables:
1. **Diagnose and fix `refresh_index`'s staleness bug** (`src/doc_qa.py`): it checks whether a document's `doc_id` is already present in the index, never whether the document's *content* has actually changed — a revised doc with the same `doc_id` keeps its stale chunks forever.
2. **Build a real evaluation harness** (`src/evaluation.py`): `evaluate` scores a labeled Q&A dataset against `doc_qa.py` (correct only if the model cites the *specific* expected document, not just any document), and `compare_top_k` runs the same harness under two or more `top_k` values as a real A/B comparison.

### The actual point of this exercise

See `runs/2026-07-17-module-08-dry-run/grading.md` for the real dry run and its findings, and `modules/08-integration-evaluation/README.md` for the full rubric.

## Running it

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # first time only
python3 scripts/verify_module_07.py fixtures/foundry   # from repo root
python3 scripts/verify_module_08.py fixtures/foundry   # chains Module 07's gate
```
