# Module 08: Building and Proving It — Integration, Evaluation & Optimization

## The question this module answers

Once it's built, how do you actually prove it works, and keep proving it as things change?

## Where it sits in the arc

Eighth module. Hard prerequisite: [Module 07, Designing the Solution](../07-solution-design-context-strategy/README.md) — this module evaluates and integrates the architecture Module 07 designed; there's nothing real to test or connect to production systems until a design exists. Next: [Module 09, Shipping Responsibly](../09-governance-stakeholders/README.md) — the hinge is that governance and delivery apply to a system that's been built and evaluated, not a proposal. See [`modules/README.md`](../README.md).

`scripts/verify_module_08.py` chains `check_module_07` — Foundry's own cumulative-gate convention within Part 2 (see [`fixtures/foundry/SPEC.md`](../../fixtures/foundry/SPEC.md)'s compatibility contract).

## The exercise

Module 07 taught recognizing when *not* to reach for a retrieval-heavy pattern. This module teaches the complementary skill: recognizing when retrieval-augmented generation genuinely *is* the right call, then building and evaluating it competently. The requesting team this time is the **Platform Docs team** — employees ask ad hoc questions about internal engineering docs (runbooks, onboarding guides), the corpus is large and genuinely changes over time, and answers must be grounded in whichever version of a document is *current*, not memorized. That's a real RAG shape, unlike Module 07's single-turn classification.

Two real deliverables, both required:

1. **`fixtures/foundry/src/doc_qa.py`** — ships mostly working (chunking, indexing, retrieval, and grounded answer generation are all correct as shipped, matching Module 06's diagnose-and-fix format). Find and fix the one real, seeded defect in `refresh_index`: it checks whether a document's `doc_id` is already *present* in the index before re-chunking it, never whether the document's *content* has actually changed. A revised runbook keeps its stale chunks forever, and the system goes on confidently answering from a superseded procedure — directly anchored to the CCAR-P exam guide's own Sample Question 3 ("a RAG system returns confident-but-wrong answers after a document refresh"). The defect isn't named anywhere in the shipped file's own docstrings; diagnosing it from the test suite's own failures is part of the exercise.
2. **`fixtures/foundry/src/evaluation.py`** — ships as a stub (`evaluate`/`compare_top_k` both raise `NotImplementedError`, matching Module 07's build-from-stub format). Implement `evaluate(index, model_client, dataset, top_k)`, which scores a labeled Q&A dataset against `doc_qa.py` (a case is correct only if the model's answer cites the *specific* document the case expects — citing something is not the same as citing the right thing), and `compare_top_k(...)`, which runs the same harness under two or more `top_k` values as a real A/B comparison.

Both are validated by the provided test suite, `fixtures/foundry/tests/test_doc_qa.py` (34 tests).

**Why these two deliverables are deliberately independent:** fixing the staleness bug and building the evaluation harness don't depend on each other — a learner could fix one without touching the other. The dry run (`runs/2026-07-17-module-08-dry-run/`) constructs both single-fix attempts to prove this isolation holds, the same discipline Module 06's `fix-bug1-only`/`fix-bug2-only` attempts established for its own two seeded defects.

**Why a too-lenient evaluation metric is its own real failure mode, not a hypothetical:** a `broken-eval-metric-attempt` in the dry run implements `evaluate` in a way that runs cleanly and "looks done" — it just counts any citation as correct, not specifically the expected one. This is exactly the class of mistake Domain 4's "evaluation metric design" objective exists to catch: an evaluation harness that always reports high accuracy isn't necessarily testing the right thing.

## Required gate

- **Deterministic tier (hands-on, with Claude Code):** `python scripts/verify_module_08.py fixtures/foundry` must pass all 34 tests and Module 07's own chained gate. Necessary, not sufficient — the tests confirm `refresh_index` is fixed and `evaluate`/`compare_top_k` behave correctly against the provided dataset shape; they don't grade the quality of a learner's own eval dataset design if one is built beyond the provided cases, which is what the conceptual rubric below is for.
- **Exam-condition tier (closed-book, without Claude Code):** [`checkpoint.md`](checkpoint.md) — 14 originally-written multiple-choice questions covering CCAR-P Domain 3 (Integration, 19%) and Domain 4 (Evaluation, Testing & Optimization, 16%), 80% (12/14) to pass, closed-book and timed.

## Conceptual rubric (deterministic tier's non-mechanical half)

1. **The staleness fix is explained, not just applied.** A learner can state *why* checking `doc_id` presence alone was wrong (it conflates "never seen this document" with "seen this document, but not its current content") — not just that changing one condition made tests pass.
2. **The evaluation metric's precision is understood.** A learner can explain why "cited something" and "cited the right thing" are different claims, and why the looser one would have shipped a system that looks evaluated but isn't.
3. **The A/B result is interpreted, not just produced.** `compare_top_k`'s output is a real result (which `top_k` value performed better, and by how much) — a learner should be able to say what that result would mean for a real production configuration choice, not just that the numbers differ.

## Takeaway

A real evaluation harness (dataset + accuracy metric + A/B comparison) built against a real RAG system, plus a diagnosed-and-fixed staleness bug — both reusable on the learner's next real system. Packaged by Coachgremlin once the rubric is met.

## Self-check before advancing

- Can you state, in one sentence, why `refresh_index`'s original `if doc_id not in new_chunks` check was wrong?
- Does `evaluate` correctly mark a case incorrect when the model cites a *different* document than expected, not just when it cites nothing at all?
- Does `compare_top_k` actually vary `top_k` per run, or would a hardcoded value pass your own tests too?

## Stop condition

`python scripts/verify_module_08.py` passes all 34 tests and Module 07's chained gate, the conceptual rubric's three criteria are met, and the closed-book checkpoint is passed at 80%+ (12/14) under real exam conditions.

---

> Authored 2026-07-17, both tiers together, following the dry run at [`runs/2026-07-17-module-08-dry-run/`](../../runs/2026-07-17-module-08-dry-run/grading.md). See [`modules/README.md`](../README.md) for workshop-wide status.
