# Session Log: Closed Book

## 2026-07-14 - Initial scaffold

Project scaffolded as **factory-output**. Purpose: Learn Anthropic's Claude Developer certification material (Foundations to Professional) the agent-native way: hands-on Claude Code exercises gated by closed-book practice checkpoints against the published exam blueprint.

### Decisions Made

- Classification: factory-output
- Owner: coderturtle
- Vault mutation: not allowed by default (see `vault_mutation_allowed` in `.hekton/project.yaml` for the authoritative, current value)
- Promotion target: none

### Next Actions

- Define brief and first phase plan
- Add first implementation
- Record initial decisions

## 2026-07-14 - Workshop Gremlin pipeline: scaffold through skeleton, all roster steps complete

Ran the Workshop Gremlin end-to-end in one session: scaffold, naming, design docs, Review Panel, module skeleton/branding, build-log/Pages site. Every step in the Gremlin's own Completion Condition is done except the deferred human gates (first push, first Pages deploy).

### What changed

- Scaffolded as `claude-cert-workshop`, renamed to **Closed Book** after the naming pass (local dir, GitHub repo, git remote, repo-local mind-palace mirror, and the live vault card all renamed; vault mutation explicitly authorized for this rename).
- **Correction:** original scope ("Claude Developer, Foundations → Professional") doesn't exist — only Architect has both exam levels today. Redirected to Architect, at coderturtle's explicit direction, with the tradeoff (less pure hands-on-coding, more design/governance) named up front.
- Researched and fetched Anthropic's own primary-source CCA-F and CCAR-P exam guide PDFs in full (not secondary "exam prep" site summaries, several of which turned out to recycle an identical, unreliable domain list across different exam pages).
- Wrote `docs/workshop-design.md` (10-module arc: 6 for CCA-F, 4 for CCAR-P, each anchored to real domains/task statements) and `docs/design-tension.md` (naming the learn-with-AI/test-without-AI tension explicitly and resolving it via a two-tier gate).
- Ran the 7-persona Workshop Review Panel against the design docs; all seven returned distinct findings. Two cross-confirmed (stale README tagline, unspecified per-module checkpoint format). Applied the cheap fixes directly; deferred the real open questions (grading-authority mechanism, prerequisite enforcement, time estimates) to `docs/next-actions.md`.
- Built 10 module skeletons (8-part template each), split learner-facing `README.md` from `docs/maintainers.md`, added `docs/brand.md`.
- Adapted Borrow Native's Astro-on-Pages site: locally validated (`npm run build` and `astro check` both clean, `/closed-book/` base prefix confirmed on every internal link). Logged 4 inherited npm vulnerabilities as RISK-0002.

### Decisions Made

See `docs/decisions.md` for the full ADR log (naming, the Developer→Architect correction, the primary-source curriculum anchor, the 10-module arc rationale, the two-tier gate design, the dogfooding commitment, the site adaptation).

### Assumptions

- Anthropic's published exam guide PDFs (fetched 2026-07-14) remain accurate; the guides themselves note they're "subject to change without notice."
- The two-tier gate design (hands-on + closed-book) actually builds durable no-AI recall better than alternatives — stated hypothesis, untested until real module content and real exam attempts exist.

### Risks

See `docs/risks.md`: RISK-0002 (inherited npm vulnerabilities, low real-world impact, deferred to before first deploy), RISK-0003 (closed-book checkpoints are honor-system, no technical enforcement, accepted limitation).

### Next Actions

See `docs/next-actions.md`: content-building (Coachgremlin, one module at a time, out of scope for this Gremlin), first push confirmation, first Pages deploy confirmation, real CCA-F/CCAR-P exam attempts once content exists.

### Validation status

Locally validated only: `npm run build` and `astro check` both clean in `site/`. GitHub Actions deploy itself unproven until a human triggers `workflow_dispatch`. Repo created on GitHub but not yet pushed (Human Gate).

### Mind-palace updated

Yes — vault card renamed to match (`claude-cert-workshop` → `closed-book`), explicitly authorized. Repo-local mirror renamed in the same commit as the repo rename.

## 2026-07-15 - PR merged; Coachgremlin's first content pass (Module 01)

PR #1 merged to `main` (all Workshop Gremlin roster work). Moved to the Learn phase: Coachgremlin authored Module 01 for real.

### What changed

- Decided Modules 01-06 build one shared project (`fixtures/resolve/`, a customer support resolution agent modeled on CCA-F's own Scenario 1) rather than independent fixtures, at coderturtle's direction.
- Authored `fixtures/resolve/SPEC.md` and the project skeleton (4 stub MCP tools, a stub coordinator agent, a placeholder test file).
- Authored Module 01's real exercise + rubric (property-phrased conceptual criteria, per Coachgremlin's rubric-spoiler-tension discipline), replacing the skeleton placeholder.
- Wrote `scripts/verify-module-01.sh`, a real deterministic checker for Claude Code configuration structure.
- Ran a real dry run (`runs/2026-07-14-module-01-dry-run/`): 3 constructed attempts (naive, correct, broken-glob). The checker discriminated correctly across all three, and the dry run caught a real bug in the checker itself (a missing `shopt -s globstar`) before it could produce a false negative against a genuinely correct attempt.
- Adapted Borrow Native's `agentic-learning-discipline` Skill for Closed Book's own sharper version of the tension (the real exam forbids the very agent the hands-on tier is built around).

### Decisions Made

See `docs/decisions.md`'s 2026-07-15 entries.

### Assumptions

The two-tier gate's conceptual tier hasn't been validated the way the deterministic tier has — no constructed attempt yet tests "passes the checker but is conceptually weak." Logged in `docs/next-actions.md`.

### Risks

No new risks this session beyond what's already in `docs/risks.md`.

### Next Actions

Module 02 (Prompts and Structured Output), continuing `resolve`. See `docs/next-actions.md`.

### Validation status

`scripts/verify-module-01.sh` run against all 3 dry-run attempts, correct results confirmed (see `runs/2026-07-14-module-01-dry-run/grading.md`). No real learner attempt yet — only self-constructed dry runs.

### Mind-palace updated

Not this session — no structural rename or vault-card change occurred.

## 2026-07-15 (cont'd) - Doubt-driven-development review and remediation of Module 01

Before treating Module 01 as done, ran a doubt-driven-development pass at the user's request: a fresh-context Claude subagent and Codex CLI (both given ARTIFACT+CONTRACT only, sandboxed read-only for Codex), plus a Fable-model subagent tasked with critiquing and replanning given both reviews' findings.

### What changed

- Both adversarial reviews found substantial, largely non-overlapping, mostly-corroborated real issues — not doubt theater. Full reconciliation in `docs/decisions.md`'s 2026-07-15 entries.
- Headline finding (Codex): the closed-book checkpoint tier — this workshop's namesake feature — had never been authored for any module. Fixed: `modules/01-configuring-claude-code/checkpoint.md`, 12 originally-written questions, full CCA-F Domain 3 coverage.
- Rewrote `scripts/verify-module-01.sh` as `scripts/verify_module_01.py`, closing several real bugs structurally (non-portable `globstar`, quoted-only YAML matching, weak scoping check, no path-escape protection). Found and fixed a further bug in the rewrite itself during re-verification (a false-positive match against `SPEC.md`'s own requirement description).
- Added `fixtures/resolve/SPEC.md`'s compatibility contract and cumulative-gate convention, addressing the coupling/regression risk both reviews flagged.
- Reconciled a real self-inconsistency: rubric criterion 2 named its own technique, violating this workshop's stated property-phrasing rule (Codex's finding, independently real).
- Reconciled a competing-safety-rule contradiction between `workshop-design.md` and Module 01's README.
- Added a 4th dry-run attempt (`weak-conceptual-attempt`) that passes the deterministic tier completely while failing the conceptual criteria — real, constructed evidence the two-tier design's conceptual half catches something the deterministic half structurally cannot.
- Fixed `CLAUDE.md`'s unconditional session-closeout instruction, which caused Codex's read-only review agent to attempt running the closeout script mid-review (failed safely under the read-only sandbox, but the instruction itself was a real bug, not just a review artifact).

### Decisions Made

See `docs/decisions.md`'s 2026-07-15 doubt-driven-development entries.

### Assumptions

None of this changes the workshop's largest remaining assumption: no real learner has attempted any of it yet.

### Risks

RISK-0003 (honor-system closed-book checkpoints) is now partially addressed by the checkpoint itself existing and stating an explicit pre-checkpoint ritual; the underlying honor-system limitation is unchanged and still accepted, not solved.

### Next Actions

Module 02, authoring both tiers together this time. See `docs/next-actions.md`.

### Validation status

`scripts/verify_module_01.py` run against all 4 dry-run attempts (naive/correct/broken-glob/weak-conceptual), results match expectations. Closed-book checkpoint content has not been attempted by anyone, including in a dry-run sense (no mechanism exists yet to "dry run" a closed-book quiz the way a deterministic checker can be dry-run).

### Mind-palace updated

Not yet this session — pending before push/PR, per this repo's own established discipline.

## 2026-07-15 (cont'd) - Module 02 authored, both tiers together

### What changed

- Implemented `extract_refund_request` interface stub (`fixtures/resolve/src/extraction.py`) and a real, provided pytest suite (`fixtures/resolve/tests/test_extraction.py`, 7 tests) as Module 02's deterministic gate.
- Wrote `scripts/verify_module_02.py`, implementing the cumulative-gate convention for real: it imports and calls `check_module_01` before running its own pytest check, and correctly fails at that step (before pytest even runs) when Module 01's configuration is absent — isolation-tested directly.
- Authored `modules/02-prompts-structured-output/checkpoint.md`: 12 originally-written questions, full CCA-F Domain 4 coverage (4.1-4.6), built alongside the hands-on tier from the start rather than as a follow-up remediation.
- Ran a real dry run (`runs/2026-07-15-module-02-dry-run/`): a correct reference implementation (7/7), a naive no-retry attempt (4/7, fails broadly), and a subtler attempt using a real Python footgun (`raw.get(x) or 0`) that fabricates a refund amount (6/7, fails narrowly on exactly the test built to catch it).
- Found and fixed a bug in the dry run's own construction of the third attempt before recording it as a finding: the first version used the wrong failure pattern (`raw.get(x, 0)`, which only fires on an absent key) and was never actually exercised by the test suite, which always supplies an explicit `None`.
- Added `fixtures/resolve/requirements.txt` (pytest) as the project's first real Python dependency.

### Decisions Made

See `docs/decisions.md`'s 2026-07-15 Module 02 entries.

### Assumptions

Module 02's conceptual-tier criteria (few-shot quality, retry-message specificity, documented nullable rationale) are untested by dry-run attempts — all 3 constructed attempts differ only in `extraction.py`'s runtime behavior, not prompt-design artifacts. Logged in `docs/next-actions.md`.

### Risks

No new risks beyond `docs/risks.md`'s existing entries.

### Next Actions

Module 03 (Designing Tools and MCP Interfaces), continuing `resolve`, both tiers together. See `docs/next-actions.md`.

### Validation status

`scripts/verify_module_02.py` run against all 3 constructed attempts plus an isolation check (cumulative gate blocks correctly with no Module 01 config present) — all match expectations. No real learner attempt yet.

### Mind-palace updated

Not yet this session — pending before push/PR.

## 2026-07-15 (cont'd) - Doubt-driven-development review of Module 02, and remediation

At the user's request, ran the same doubt-driven-development process used for Module 01 against Module 02 before treating it as done: a fresh-context Claude subagent, Codex CLI (with live web-search access), and a Fable-model subagent to critique and replan given both reviews' findings.

### What changed

- Both reviews found real, substantial, largely non-overlapping issues. The dominant one, more severe than anything in Module 01's review: rubric criteria 3 and 4 graded a prompt/few-shot artifact the exercise's original interface never actually required a learner to produce — `model_client` was fully injected, with no place in the exercise for real prompt-engineering content to exist.
- Fable's structural call, adopted: change the interface, not the rubric. Added `build_extraction_prompt(message, prior_attempts) -> str` and `FEW_SHOT_EXAMPLES` as real exercise deliverables; `extract_refund_request` now passes the constructed prompt (not the raw message) to `model_client`. Required zero changes to the original 7 tests.
- Test suite grew from 7 to 14 tests, closing an asserted-but-untested `"other"`-requires-detail rule, unvalidated `confidence`/type checks, a loose exhaustion-count assertion, an unchecked `prior_attempts` contract field, and adding direct tests that the prompt/few-shot artifacts exist and that a retry prompt literally embeds the specific prior error.
- Fixed a real technical-precision issue in the checkpoint (Q5's `tool_use` guarantee claim, found via Codex's live doc search) and a real mental-model imprecision (Q11's "same model instance" framing).
- Fixed a self-contradiction in the README (an attempt called a "valid alternate terminal" that actually fails the stop condition).
- Documented the Python 3.9+ requirement and added an explicit, evidenced ARB-trigger-check-N/A line to `grading.md`, closing a Coachgremlin-checklist gap Codex caught (the reasoning existed but was never written down).
- Added a 4th dry-run attempt (`weak-few-shot-attempt`): passes all 14 tests with only clean, textbook-only few-shot examples — real, constructed evidence rubric criterion 3 catches what the deterministic suite structurally can't.

### Decisions Made

See `docs/decisions.md`'s 2026-07-15 doubt-driven-development entries for Module 02.

### Assumptions

Rubric criterion 4 (documented nullable-field rationale) still has no dry-run attempt isolating it specifically. Logged in `docs/next-actions.md`.

### Risks

No new risks beyond `docs/risks.md`'s existing entries.

### Next Actions

Module 03, both tiers together, doubt-driven-development before done — now the standing practice for every module. See `docs/next-actions.md`.

### Validation status

`scripts/verify_module_02.py` re-run against all 4 constructed attempts plus the cumulative-gate isolation check after the interface change — all match expectations.

### Mind-palace updated

Not yet this session — pending before push/PR.

## 2026-07-15 (cont'd) - Module 03 authored, both tiers together, lessons applied proactively

### What changed

- Implemented `Backend` protocol (`fixtures/resolve/src/backend.py`) and a shared `tool_error()` helper (`fixtures/resolve/src/tool_errors.py`) so all four MCP tools (`get_customer`, `lookup_order`, `process_refund`, `escalate_to_human`) share one consistent injection pattern and error shape.
- Refactored `scripts/verify_module_02.py` to expose an importable `check_module_02()`, matching Module 01's `check_module_01()` pattern, so `scripts/verify_module_03.py` chains it via a real function call rather than shelling out to a subprocess.
- Wrote a real, provided test suite (`fixtures/resolve/tests/test_tools.py`, 16 tests), including the safety-critical property: `process_refund` must independently re-verify `customer_id` against the backend before proceeding, distinct from Module 04's later session-level hook.
- Applied both prior modules' doubt-driven-development lessons proactively rather than waiting for a review to find them: designed rubric criterion 2 (docstring keyword presence) as deterministic from the start; constructed a `weak-docstring-attempt` before shipping, confirming the deterministic/conceptual split actually catches what it's supposed to.
- Found and fixed a real bug in the exercise's own first draft, before any attempt was graded: every tool's description was written as a module-level docstring, not the function's own `__doc__` — real MCP tooling reads the latter. `get_customer.__doc__` came back empty against the first draft.
- Authored `modules/03-tool-mcp-design/checkpoint.md`: 12 originally-written questions, full CCA-F Domain 2 coverage (2.1-2.5).

### Decisions Made

See `docs/decisions.md`'s 2026-07-15 Module 03 entries.

### Assumptions

Rubric criterion 4 (process_refund's defense-in-depth reasoning documented as deliberate) has no dry-run attempt isolating it. Doubt-driven-development has not yet been run against this module this pass.

### Risks

No new risks beyond `docs/risks.md`'s existing entries.

### Next Actions

Ask about a doubt-driven-development pass for Module 03 before merging (each Codex invocation needs its own turn's authorization). Then Module 04. See `docs/next-actions.md`.

### Validation status

`scripts/verify_module_03.py` run against all 3 constructed attempts (correct/trusts-caller/weak-docstring) plus the cumulative-gate chain (Module 01 -> 02 -> 03) — all match expectations.

### Mind-palace updated

Not yet this session — pending before push/PR.

## 2026-07-15 (cont'd) - Doubt-driven-development review of Module 03, and remediation

Ran the same process as Modules 01-02: a fresh-context Claude subagent, Codex CLI (with live repo exploration this time, not just web search), and a Fable-model replan.

### What changed

- Found the cumulative-gate chain into Module 04 was already broken: `check_module_01` returns a bare `CheckResult`, `check_module_02` (added during its own remediation) returns `tuple[CheckResult, str]`, and Module 03's first draft exposed no `check_module_03` at all for Module 04 to chain against.
- Found something more serious than anything in either prior review: both `verify_module_02.py` and the first `verify_module_03.py` ran the test file *from the submission itself*, not a canonical copy — a learner could weaken or delete `tests/test_extraction.py`/`tests/test_tools.py` and pass trivially. The "don't edit this" notice at the top of each file was prose, not enforcement.
- Fixed both structurally: unified every `check_module_NN(target) -> CheckResult` on one shape, added `check_module_03`, and rewrote both checkers to copy the repo's own canonical test file to a temp location before running it. Verified empirically (not just by code inspection) that legitimate submissions are unaffected and that a tampered test file no longer helps — tested against both Module 02 and Module 03.
- Closed the remaining gaps: `process_refund`'s docstring is now checked (previously 2 of 4 tools, despite the rubric's claim); a new ordering test makes "re-verify BEFORE doing anything else" a real gate, not prose; `ERROR_CATEGORIES` gained documented semantics and became a tuple; `escalate_to_human` is now documented and tested as the project's deliberate fail-open path; the order-leak test tightened to an equality assertion; exam-meta commentary stripped from `lookup_order`'s docstring; the README's `.mcp.json` takeaway overclaim fixed; two checkpoint answers gained precision caveats; `backend.py` now explicitly defers refund execution semantics to Module 04.

### Decisions Made

See `docs/decisions.md`'s 2026-07-15 Module 03 doubt-driven-development entries.

### Assumptions

Rubric criterion 4 still has no dry-run attempt isolating it from the now-deterministic ordering test.

### Risks

No new risks beyond `docs/risks.md`'s existing entries. The test-file-tampering gap (fixed here) applied to every module built so far and would have applied to every future one if not caught now.

### Next Actions

Module 04, both tiers together, `check_module_03` ready to chain. See `docs/next-actions.md`.

### Validation status

`scripts/verify_module_03.py` re-run against all 3 attempts (20 tests each), the cumulative-gate isolation check, and a tampering check (weakening a broken attempt's own test file no longer helps it pass) — all match expectations. Same tampering check re-verified for Module 02.

### Mind-palace updated

Not yet this session — pending before push/PR.

## 2026-07-15 (cont'd) - Module 04 authored (Agentic Loops and Multi-Agent Orchestration)

Fourth Coachgremlin content pass, continuing `resolve`. Both tiers built together from the start, per this workshop's own established practice since Module 02.

### What changed

- `fixtures/resolve/src/agent.py`: real docstrings + exercise contract for `SessionState`, `verify_before_refund_hook`, and `run_support_session` (all still `raise NotImplementedError` in the shipped stub, real bodies live in `runs/2026-07-15-module-04-dry-run/*/src/agent.py`). Dependency-injection pattern matching Modules 02-03 (`model_client`, `tools`, `backend` all injected).
- `fixtures/resolve/tests/test_agent.py`: a real, provided pytest suite (12 tests) using spy tool functions rather than Module 03's real tool implementations, isolating this module's own exercise (the loop and the hook) from already-tested tool behavior.
- `scripts/verify_module_04.py`: chains `check_module_03` (which chains `check_module_02`, which chains `check_module_01`), then runs the repo's canonical `tests/test_agent.py` via the same canonical-test-execution pattern Module 03's remediation established.
- `fixtures/resolve/src/backend.py`: docstring rewritten to resolve the deferred stateful-backend question Module 03 left open — Module 04 does not extend `Backend` into a mutating protocol; see Decisions.
- `modules/04-agentic-orchestration/README.md`: full exercise, two-tier gate, rubric (4 criteria), required-to-advance, self-check, takeaway — replacing the design-phase skeleton.
- `modules/04-agentic-orchestration/checkpoint.md`: 14 originally-written questions, full CCA-F Domain 1 coverage (Task Statements 1.1-1.7).
- `fixtures/resolve/SPEC.md`: Module 04 status row and detail section added; "Running it" section extended.
- `modules/README.md`: content-status line updated (Modules 01-04 real, 05-10 skeleton).

### Decisions Made

See `docs/decisions.md`'s 2026-07-15 Module 04 entries: both tiers built together; the deferred stateful-backend question resolved (orchestration only, no refund persistence/idempotency in this module); 4 dry-run attempts constructed, including one (`thin-docstring-attempt`) built proactively to isolate the conceptual-tier rubric gap before any external review, rather than after one — the first module in this arc to apply that discipline from the start rather than learning it via remediation.

### Assumptions

Rubric criterion 3 (rejection-message quality beyond the deterministic keyword check) has no dry-run attempt isolating it specifically. No doubt-driven-development review has been run against this module yet — pending, per standing practice.

### Risks

No new risks beyond `docs/risks.md`'s existing entries.

### Next Actions

Offer and (if accepted) run doubt-driven-development review (fresh Claude subagent + Codex + Fable replan) before treating Module 04 as done. Then Module 05 (Context and Reliability at Scale), `check_module_04` ready to chain. See `docs/next-actions.md`.

### Validation status

`scripts/verify_module_04.py` run against all 5 constructed attempts (correct/no-hook/text-parsing/trusts-attempted-call/thin-docstring) plus the cumulative-gate chain (Module 01 → 02 → 03 → 04) — all match expectations. Full regression re-run across all prior modules' dry-run attempts (Module 01: 4 attempts, Module 02: 4 attempts, Module 03: 3 attempts) after this module's `backend.py` docstring edit — no change in outcomes.

### Mind-palace updated

Not yet this session — pending before push/PR.

## 2026-07-15/16 (cont'd) - Doubt-driven-development review of Module 04, and remediation

Ran the same process as Modules 01-03: a fresh-context Claude subagent (adversarial review, ARTIFACT+CONTRACT only), Codex CLI (with live repo exploration and its own constructed attacks), then a Fable-model critique of the remediation itself once fixes were applied — the last step had been skipped in the rush to fix and was added back in for consistency with standing practice.

### What changed

- **Dominant finding (both reviewers, independently reproduced live):** `verify_before_refund_hook` blocked `process_refund` based on "did *any* `get_customer` call succeed in this session," never checking *which* customer it verified — a session verifying customer A could refund customer B, undetected by all 5 originally-constructed dry-run attempts. Fixed: `SessionState` gained `verified_customer_id`, set only from a successful `get_customer` result's actual `customer_id`; the hook now requires an exact match. Test suite grew 12→16, then 17 after the Fable pass found the fix's false-allow direction was untested (see below).
- **4 further findings from Claude+Codex:** a test-double loophole (spy tools silently tolerated a missing `backend` kwarg an implementation needs to pass to the real tools — fixed with a keyword-only required parameter, verified via a constructed submission that omits it: `TypeError`); a factually-wrong checkpoint answer (Q14 claimed session forking isolates real-world tool-call side effects, not just conversation state — rewritten so the misconception is the wrong answer); a stale cross-module contradiction (Module 03's README still promised refund persistence was "Module 04's exercise," contradicting the actual scope decision — fixed in Module 03's live README); a checkpoint/README pass-threshold arithmetic mismatch (12/14 vs. 11/14 — fixed to 12/14, matching 80% rounded up correctly).
- **3 further findings from the Fable critique of the remediation:** stale pre-fix rule statements survived in two live documents (`fixtures/resolve/SPEC.md`, the shipped `process_refund.py` and its copies across all 5 Module 04 attempt directories) — fixed to name the customer-identity binding explicitly; a stale quotation of the pre-fix docstring wording survived inside the shipped `tests/test_agent.py` — fixed; `trusts-identifier-attempt` (renamed from `trusts-attempted-call-attempt`, whose original bug became unobservable once identity-binding existed) was only caught in the false-block direction, not the false-allow direction the bug actually reintroduces — added a 17th test closing this, `trusts-identifier-attempt` now fails 2/17.

### Decisions Made

See `docs/decisions.md`'s 2026-07-15 Module 04 doubt-driven-development and Fable-critique entries.

### Assumptions

Module 04 rubric criterion 3 (rejection-message quality) still has no isolating dry-run attempt. No attempt constructs a long, realistic multi-turn session exercising the hook under drift across several unrelated customers.

### Risks

No new risks beyond `docs/risks.md`'s existing entries, except one process observation: Codex's Module 04 review attempted to run `bash ~/hekton/scripts/end-session.sh` again despite making zero changes and the 2026-07-15 scoping fix to `CLAUDE.md` — failed safely (read-only sandbox, missing `--title`), but confirms prose scoping doesn't reliably bind an external CLI's own judgment. Logged in `docs/next-actions.md`, not fixed (same out-of-scope reasoning as the prior factory-wide audit item).

### Next Actions

Module 05 (Context and Reliability at Scale), continuing `resolve`, both tiers together, doubt-driven-development before done. `check_module_04` is ready to chain. See `docs/next-actions.md`.

### Validation status

`scripts/verify_module_04.py` re-run against all 5 attempts (17 tests each) after every fix — correct 17/17, no-hook 12/17 (5 fail), text-parsing 16/17 (1 fail), trusts-identifier 15/17 (2 fail, both directions of its bug), thin-docstring 17/17 (conceptually weak). A constructed submission omitting `backend=backend` fails loudly (`TypeError`, 9/17 fail). Full regression re-run across Modules 01-03's own dry-run attempts (4+4+3 attempts) after every Module 04 doc/code edit — all outcomes match their pre-existing expected results exactly, no regressions introduced at any point in this remediation.

### Mind-palace updated

Not yet this session — pending before push/PR.
