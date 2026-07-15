# Module 02: Prompts and Structured Output That Survive Production

## The question this module answers

How do you get Claude to produce output you can actually trust and parse, every time — not just on the demo run?

## Where it sits in the arc

Second module. Hard prerequisite: [Module 01, Configuring Claude Code](../01-configuring-claude-code/README.md) — this module's checker chains Module 01's, per the cumulative-gate convention in `fixtures/resolve/SPEC.md`'s compatibility contract. Next: [Module 03, Designing Tools and MCP Interfaces](../03-tool-mcp-design/README.md) — the hinge is that a tool's `input_schema` reuses the JSON-schema discipline this module builds. See [`modules/README.md`](../README.md).

**Requires Python 3.9+** (the generic type aliases in `extraction.py` use PEP 585 subscripting outside annotation position, which `from __future__ import annotations` doesn't cover). Requires `pytest` — `pip install -r fixtures/resolve/requirements.txt`.

## Exercise: `extract_refund_request`, `build_extraction_prompt`, and `FEW_SHOT_EXAMPLES`

Runs against `fixtures/resolve/`, continuing the shared project. `resolve`'s coordinator agent (Module 04) needs a customer's freeform message turned into a structured request before any tool call can happen — this module builds that, before there's an agentic loop to feed it or real MCP tools (Module 03) to act on it.

Implement three things in `fixtures/resolve/src/extraction.py`:

1. **`build_extraction_prompt(message, prior_attempts) -> str`** — the actual prompt-engineering artifact this module is about. Must state the schema explicitly (Task Statement 4.1: explicit criteria over vague instructions), embed your few-shot examples (Task Statement 4.2), and, on a retry, embed the *specific* prior validation error so the model can actually correct its mistake (Task Statement 4.4) — not just carry that error in `prior_attempts` unused.
2. **`FEW_SHOT_EXAMPLES`** — at least 2 examples, each with a `message` and an `expected` structured output. At least one must demonstrate a genuinely ambiguous case (a message that doesn't name its category explicitly, or bundles multiple issues), not only clean textbook messages — this is the exercise's real content, not decoration.
3. **`extract_refund_request(message, model_client, max_retries=2)`** — the retry/validation wrapper around an *injected* `model_client` callable (so the provided test suite can supply canned responses without a live API call), calling `build_extraction_prompt` internally and validating the response against the schema before returning it.

A real, provided test suite (`fixtures/resolve/tests/test_extraction.py`, 14 tests) checks, among other things: clean extraction, honest `None` on a missing amount (never a fabricated guess), `"other"` requiring a real detail, invalid `reason_category`/`confidence`/type values all rejected and retried, retries carrying the specific error forward *and into the actual prompt text*, exhausting `max_retries` raising rather than guessing, `max_retries=0` making exactly one attempt, and the prompt/few-shot artifacts existing in the right shape. Read the test file itself for the full, current list — this README doesn't restate every case.

Get `python3 scripts/verify_module_02.py <path-to-your-attempt>` (run from the repo root) to pass, then check it against the rubric below.

## The two-tier gate

**Tier 1 — deterministic, hands-on with Claude Code.** `scripts/verify_module_02.py`: chains Module 01's checker first (a Module 02 submission that broke Module 01's already-passed configuration fails here, not silently), then runs the real pytest suite against your `extraction.py`.

**Tier 2 — exam-condition, closed-book without Claude Code.** [`checkpoint.md`](checkpoint.md): 12 originally-written questions covering the full CCA-F Domain 4 blueprint (4.1–4.6), including the architectural judgment calls (batch processing, multi-instance review) that have no artifact for the test suite to check. Close your Claude Code session before starting it. 80% (10/12) to pass.

Both tiers are required to advance.

## Rubric (deterministic tier's rubric; the closed-book checkpoint is scored separately)

1. **`python3 scripts/verify_module_02.py` exits 0 (gate, deterministic).** Module 01's chained gate passes, and all 14 provided tests pass — including that `build_extraction_prompt` names the schema fields and categories, and `FEW_SHOT_EXAMPLES` has at least 2 well-formed entries.
2. **The retry request sent back to the model on a validation failure names the specific field(s) that failed, not a generic "try again" (deterministic: `test_retry_prompt_embeds_the_specific_prior_error` checks the error text literally appears in the retry prompt).** This one moved from conceptual to deterministic in this module's own remediation — the test suite can check it directly.
3. **At least one few-shot example genuinely demonstrates an ambiguous case (a message that doesn't name its category explicitly, or bundles multiple issues), not only clean textbook messages (scored, conceptual).** The test suite can only check that examples exist and are well-formed — not whether any of them are actually hard. This exercise's own dry run constructed an attempt that passes every deterministic test with two clean-only examples; only this criterion catches it.
4. **The reason `refund_amount_cents` is nullable is visible somewhere (a comment, or the prompt's own explicit instruction) as "prevents fabrication," not just present because `Optional[int]` happened to type-check (scored, conceptual).** Property, not technique: the *reason* should be visible, not just the fact that the type allows it.

**Before trusting a green checker as proof you're done:** this exercise's own dry run (`runs/2026-07-15-module-02-dry-run/grading.md`) constructed four attempts, not just a correct one. A no-retry attempt (happy path only) fails broadly and obviously. A subtler attempt retries correctly but silently converts an honest "no amount stated" into a fabricated `0` via a `raw.get(...) or 0` pattern — a real Python footgun, not a contrived one — and passes 13 of 14 tests; only the one test built specifically to catch it does. A fourth attempt passes **all 14** tests while having only clean, textbook few-shot examples — no test can see that gap, only rubric criterion 3 does. Read that grading file before assuming your own green run means what you think it means.

## Required to advance / stop condition

Produce an `extraction.py` that passes `scripts/verify_module_02.py` and demonstrates the two scored conceptual criteria (3-4), **and** pass the closed-book checkpoint at 80%+. Reading this page does not count.

**Expected intermediate state, not a stopping point:** if your first attempt handles the happy path and nothing else (the no-retry attempt this module's dry run constructed), that's a normal step on the way to done, not a failure and not somewhere to stop. It fails the checker (8 of 14 tests) and the stop condition above requires a passing checker — go back and ask: what does the model client return when it can't produce a valid extraction, and what should happen then?

## Before the checkpoint: a non-scored self-check

Before opening `checkpoint.md`, predict which of Domain 4's six task statements you feel shaky on. Before running `scripts/verify_module_02.py` for the first time, predict which tests will fail and why. Write both down, then compare. See [`.claude/skills/agentic-learning-discipline/SKILL.md`](../../.claude/skills/agentic-learning-discipline/SKILL.md).

## Takeaway

A reusable few-shot/JSON-schema template library for ambiguous-extraction scenarios — the schema shape, the retry-with-error-feedback pattern, and at least one real ambiguous-case few-shot example, all built from your own `extraction.py`, not copied from documentation. Unlike Module 01's takeaway, this one is now directly backed by the exercise's own interface (`build_extraction_prompt`, `FEW_SHOT_EXAMPLES`) rather than a promise the exercise didn't actually require producing — a gap this module's own doubt-driven-development review found and closed before shipping (see `docs/decisions.md`'s 2026-07-15 Module 02 entries).

---

*Module content authored 2026-07-15, both tiers built together from the start (the explicit lesson from Module 01's doubt-driven-development remediation). A second doubt-driven-development pass (Claude subagent + Codex + Fable replan) then found the exercise's interface didn't actually require the prompt/few-shot artifact two rubric criteria graded — remediated the same day: see `docs/decisions.md`. Dry run: `runs/2026-07-15-module-02-dry-run/grading.md`.*
