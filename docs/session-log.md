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

## 2026-07-16 - Module 05 authored (Context and Reliability at Scale)

Fifth Coachgremlin content pass, continuing `resolve`. Both tiers built together from the start.

### What changed

- `fixtures/resolve/src/context.py`: `CaseFact`/`CaseFacts` (data structures, provided) and two exercise functions, `update_case_facts` (sourced, conflict-annotated fact extraction from tool results — reads results, never requests) and `should_escalate` (a structured escalation decision checking conflicts, then a real error-count threshold, then iteration proximity, in that order; deliberately no `confidence` parameter in its signature).
- `fixtures/resolve/tests/test_context.py`: a real, provided pytest suite (20 tests).
- `scripts/verify_module_05.py`: chains `check_module_04` (which chains `check_module_03`, `check_module_02`, `check_module_01`).
- Two new files only — no prior module's shipped stub or test file touched. Full regression across all 16 prior dry-run attempts (Modules 01-04) confirms zero interference, empirically, not just by inspection.
- `modules/05-context-reliability/README.md`: full exercise, two-tier gate, rubric (3 criteria), required-to-advance, self-check, takeaway — replacing the design-phase skeleton.
- `modules/05-context-reliability/checkpoint.md`: 12 originally-written questions, full CCA-F Domain 5 coverage (Task Statements 5.1-5.6).
- `fixtures/resolve/SPEC.md`: Module 05 status row and detail section added; "Running it" extended.
- `modules/README.md`: content-status line updated (Modules 01-05 real, 06-10 skeleton).

### Decisions Made

See `docs/decisions.md`'s 2026-07-16 entries: scoping decision (5.3/5.4 have no `resolve`-specific artifact yet, checkpoint-only); the explicit statement that this module's conflict-preserving design and Module 04's overwrite-on-verify design are both correct for different reasons, not a contradiction; 4 flawed attempts plus a proactively-built conceptually-weak one; a test-suite gap (independent conflicts across two different fields) found and closed before shipping, growing the suite from 19 to 20 tests.

### Assumptions

No doubt-driven-development review has been run against this module yet — pending, per standing practice.

### Risks

No new risks beyond `docs/risks.md`'s existing entries.

### Next Actions

Offer and (if accepted) run doubt-driven-development review (fresh Claude subagent + Codex + Fable critique of the remediation) before treating Module 05 as done. Then Module 06 (Foundations Capstone), `check_module_05` ready to chain. See `docs/next-actions.md`.

### Validation status

`scripts/verify_module_05.py` run against all 5 constructed attempts (correct/silent-overwrite/request-trusting/confidence-proxy/thin-docstring) plus the cumulative-gate chain (Module 01 → 02 → 03 → 04 → 05) — all match expectations. Full regression re-run across Modules 01-04's own dry-run attempts (4+4+3+5 = 16 attempts) after adding Module 05's two new files — all outcomes match their pre-existing expected results exactly.

### Mind-palace updated

Not yet this session — pending before push/PR.

## 2026-07-16 (cont'd) - Doubt-driven-development review of Module 05, and remediation (two rounds)

Ran the same process as Modules 01-04: a fresh-context Claude subagent (adversarial review, ARTIFACT+CONTRACT only), Codex CLI (with its own constructed counter-implementations run live), then a Fable-model critique of the remediation itself.

### What changed

- **Round 1 (Claude + Codex), dominant finding:** the test suite tested `customer_id` far more rigorously than the structurally-identical `order_id`/`refund_amount_cents` mappings — a request-vs-result mixup, a hollow (unsourced) conflict entry, or a silently-overwritten conflict on either of those two fields all passed the original 20 tests. Both reviewers constructed and ran the exact counter-implementations to confirm this, not just identified the gap by inspection. Fixed with symmetric test coverage (request-vs-result test for `lookup_order`, conflict tests for `order_id` and `refund_amount_cents`); `request-trusting-attempt` extended to also misread `lookup_order`. Test suite grew 20→28.
- **Round 1, 2 further structural findings, each verified against a live counter-implementation:** a shallow-copy non-mutation hole (`dataclasses.replace()` sharing the same `conflicts` list object passed all 20 tests while corrupting the caller's original) and an unenforced `should_escalate` signature guarantee (an unused `confidence` parameter passed all 20 tests) — both fixed with dedicated tests using `inspect.signature` and independent-list checks.
- **Round 1, 2 smaller findings:** a dead `issue_summary` field (structural risk as an undetected fourth escalation trigger) removed entirely rather than merely documented; an untested iteration boundary (off-by-one passed all 20 tests) closed with a boundary test; checkpoint Q12's overclaim about `source_tool` distinguishing same-tool re-reports (it can't — no call ID or timestamp) rewritten so the overclaim is the wrong answer.
- **Round 2 (Fable critique of the round-1 remediation):** found the "symmetric coverage" fix was itself still asymmetric — conflict tests for `order_id`/`refund_amount_cents` checked values but not `source_tool`; a failed `lookup_order` could still leak a fact from request args via the same key-collision the success-path fix had just closed; refund conflicts had no most-recent-wins or no-conflict-on-repeat test at all. All four found by constructing and running new counter-implementations against the actual current files, not by re-reading the round-1 diff for plausibility. Fixed; test suite grew 28→30.

### Decisions Made

See `docs/decisions.md`'s 2026-07-16 Module 05 doubt-driven-development and Fable-critique entries.

### Assumptions

No further review rounds planned; the module has now been through dry-run construction, doubt-driven-development, and a critique of the remediation itself — the same three-stage depth Module 04 established.

### Risks

No new risks beyond `docs/risks.md`'s existing entries.

### Next Actions

Module 06 (Foundations Capstone), continuing `resolve`, `check_module_05` ready to chain. See `docs/next-actions.md`.

### Validation status

`scripts/verify_module_05.py` re-run against all 5 attempts (30 tests each) after every fix — correct 30/30, silent-overwrite 24/30 (6 fail), request-trusting 26/30 (4 fail), confidence-proxy 26/30 (4 fail), thin-docstring 30/30 (conceptually weak). Eight ad hoc counter-implementations across both review rounds each fail exactly their own targeted test and pass everything else, confirmed by live execution. Full regression re-run across Modules 01-04's own dry-run attempts (16 attempts) after every Module 05 doc/code edit in this remediation — all outcomes match their pre-existing expected results exactly.

### Mind-palace updated

Not yet this session — pending before push/PR.

## 2026-07-16 (cont'd) - Module 06 authored (Foundations Capstone), closing Part 1

Sixth and final Coachgremlin content pass for Part 1 (Architect Foundations). This module has a genuinely different exercise shape from every prior one — diagnose-and-fix, not stub-implementation — matching CCA-F's own scenario-based exam format testing whether a candidate can find a defect in a mostly-working, unfamiliar system rather than build one from nothing.

### What changed

- `fixtures/resolve/src/session.py`: `run_full_support_session`, fully written and running (not `raise NotImplementedError`), integrating Module 02's `extract_refund_request`, Module 04's `verify_before_refund_hook`/loop pattern, and Module 05's `update_case_facts`/`should_escalate` into one function. Ships with 2 real, seeded defects: (1) `ExtractionResult.confidence` fed into a parallel, unofficial escalation check bypassing `should_escalate` entirely; (2) `should_escalate` checked against a stale, pre-update `CaseFacts`, one turn behind the current tool call's result.
- `fixtures/resolve/tests/test_session.py`: a real, provided pytest suite (5 tests), written to fail 2/5 against the exact shipped file — the deterministic gate does not start green for this module, deliberately.
- `scripts/verify_module_06.py`: chains `check_module_05` (which chains `check_module_04`, `check_module_03`, `check_module_02`, `check_module_01`).
- Two new files only — no prior module's shipped stub or test file touched. Full regression across all 21 prior dry-run attempts (Modules 01-05) confirms zero interference.
- `modules/06-foundations-capstone/README.md`: full exercise (explicitly naming the diagnose-and-fix shape as different from Modules 01-05), two-tier gate, rubric (3 criteria), required-to-advance, self-check, takeaway — replacing the design-phase skeleton.
- `modules/06-foundations-capstone/checkpoint.md`: a full mock exam matching CCA-F's own real structure — 6 original scenarios (none of them the real exam's own published scenarios), complete 4 of 6 (drawn, not self-selected), 42 originally-written questions total, 720/1000 to pass. A documented, honest reduction from the real exam's ~60-question total for a 4-scenario draw.
- `fixtures/resolve/SPEC.md`: Module 06 status row and detail section added; "Running it" extended.
- `modules/README.md`: content-status line updated (Modules 01-06 real, closing Part 1 in full; 07-10 skeleton, Part 2).

### Decisions Made

See `docs/decisions.md`'s 2026-07-16 Module 06 entries: the diagnose-and-fix exercise shape decision; the two seeded defects and why each spans a different pair of prior modules; the dry-run's 4 flawed attempts (2 isolating each defect independently, 1 over-correction case); the mock exam's original-scenario-pool scope decision.

### Assumptions

No doubt-driven-development review has been run against this module yet — pending, per standing practice. The mock exam's answer key has no dry-run validation pass of its own (no constructed "attempt" checking the 42-question answer key for errors) — flagged as a real gap in `docs/next-actions.md`.

### Risks

No new risks beyond `docs/risks.md`'s existing entries.

### Next Actions

Offer and (if accepted) run doubt-driven-development review before treating Module 06 as done. Then Part 2 (Architect Professional) begins with Module 07 — no shared-project decision exists yet for Part 2, an explicitly open question left in `fixtures/resolve/SPEC.md`. See `docs/next-actions.md`.

### Validation status

`scripts/verify_module_06.py` run against all 5 constructed attempts (correct/unfixed/fix-bug1-only/fix-bug2-only/over-correction) plus the cumulative-gate chain (Module 01 → 02 → 03 → 04 → 05 → 06) — all match expectations, including the over-correction case passing its intended defect's test vacuously while failing a separate contract test. Full regression re-run across Modules 01-05's own dry-run attempts (4+4+3+5+5 = 21 attempts) after adding Module 06's two new files — all outcomes match their pre-existing expected results exactly.

### Mind-palace updated

Not yet this session — pending before push/PR.

## 2026-07-16 (cont'd) - Doubt-driven-development review of Module 06, and remediation (two rounds)

Ran the same process as Modules 01-05: a fresh-context Claude subagent (adversarial review, actually executing the checker against every attempt directory), Codex CLI (its own execution plus a hand-recount of the checkpoint's domain tally), then a Fable-model critique of the remediation itself, building its own mutants.

### What changed

- **Round 1 (Claude + Codex), dominant findings:** every one of the checkpoint's 42 answer-key entries named option A as correct, no exceptions — fixed via a mechanically-verified per-question option rotation (final distribution A:10, B:11, C:11, D:10), verified two ways (option text re-parsed to confirm it landed at the claimed letter; distractor letters re-parsed to confirm they're exactly the 3 non-correct letters) for all 42 questions. Codex's more severe finding: the "correct" reference implementation itself never escalated when the hook repeatedly rejected a call — reproduced live against `correct-attempt` (3 blocked refunds → silent `max_iterations`, `error_count=0`) — contradicting this project's own fail-closed design default. This was a gap in the shared *base design*, identical across the shipped stub and all five dry-run attempts, not one of the two seeded pedagogical defects; fixed uniformly (a rejection now also calls `should_escalate` before continuing), with a 6th test added (test suite 5→6).
- **Round 1, further findings:** 3 scenarios (C, D, F) renamed to reduce resemblance to the real exam's own published scenarios (a release-notes drafting agent, a customer-feedback synthesizer, a legacy-codebase documentation generator, replacing framings that tracked "Claude Code for CI," "Multi-Agent Research System," and "Developer Productivity with Claude" too closely). Two coverage gaps disclosed explicitly in the checkpoint's own intro rather than left implicit: Task Statement 5.4 has zero questions in this pool (covered in Module 05's own checkpoint); Domain 3/Domain 4 have equal real weight but unequal pool representation. The checkpoint's originality note reworded so Scenario A's deliberate, admitted parallel to the real exam's own "Customer Support Resolution Agent" scenario is disclosed rather than contradicted by an unqualified "none of these are the real exam's scenarios" claim.
- **Round 2 (Fable critique of round 1):** found the new 6th test never checked that escalation *doesn't* happen prematurely — a constructed mutant escalating unconditionally on the first rejection (ignoring iteration budget, never actually calling `should_escalate`) passed all 6 tests. Fixed by tightening two tests to assert the model was actually consulted twice before escalating, and that a single rejection with iteration budget remaining reaches a normal `end_turn`. Also found the Scenario C/F renaming left stale "review"/"new engineers' first week" vocabulary in 5 distractor options (not correct answers), and that Scenario B's B7 stem described a scenario disjoint from its own premise — all fixed and re-verified against Fable's own constructed mutants.

### Decisions Made

See `docs/decisions.md`'s 2026-07-16 Module 06 doubt-driven-development and Fable-critique entries.

### Assumptions

No further review rounds planned; the module has now been through dry-run construction, doubt-driven-development, and a critique of the remediation itself — the same three-stage depth Modules 04-05 established, closing Part 1 of the workshop's arc.

### Risks

No new risks beyond `docs/risks.md`'s existing entries.

### Next Actions

Part 2 (Architect Professional) begins with Module 07 — no shared-project decision exists yet for Part 2, an explicitly open question left in `fixtures/resolve/SPEC.md`. See `docs/next-actions.md`.

### Validation status

`scripts/verify_module_06.py` re-run against all 5 attempts (6 tests each) after every fix — correct 6/6, unfixed 4/6, fix-bug1-only 5/6, fix-bug2-only 5/6, over-correction 5/6. Fable's own constructed escalate-immediately mutant now fails exactly the two tightened tests, confirmed by live execution. Full regression re-run across Modules 01-05's own dry-run attempts (21 attempts) after every Module 06 doc/code edit in this remediation — all outcomes match their pre-existing expected results exactly.

### Mind-palace updated

Not yet this session — pending before push/PR.

## 2026-07-17 - Module 07 authored, opening Part 2; doubt-driven-development finds and fixes a project-wide checker bypass

Part 1 (Modules 01-06) closed with Module 06. This session opened Part 2 (Architect Professional, CCAR-P). Since `fixtures/resolve/SPEC.md` left the Part 2 shared-project question explicitly open, two `AskUserQuestion` rounds resolved it before any content was authored: a new shared system, not a `resolve` continuation (coderturtle's choice, over the recommended "anchor on resolve, artifacts not code"), and an internal AI platform team scenario (coderturtle's choice, matching the recommendation) — named **Foundry**. Module 07 (Designing the Solution: Architecture, Models & Context Strategy) was then authored on Foundry, both tiers together, followed by a doubt-driven-development review whose dominant finding turned out to be project-wide, not Module-07-scoped — the most consequential review this project has run to date.

### What changed

- `fixtures/foundry/`: new shared project. `SPEC.md` (rationale for the new system, compatibility contract explicitly stating Part 2 checkers don't chain back into Part 1's `check_module_06`, module build-out table), `CLAUDE.md`, `requirements.txt`, `src/ticket_triage.py` (stub), `tests/test_ticket_triage.py` (canonical suite, grew from 12 to 20 tests during doubt-driven-development), `docs/adr-0001-ticket-triage-architecture.md` (learner deliverable, not shipped).
- `scripts/verify_module_07.py`: new checker, first Part 2 gate. Validates two structurally different deliverables in one pass — a real pytest suite, and a regex-based structural check of the ADR (4 required sections, minimum content per section, a keyword check that "Alternatives Considered" names the agentic/`resolve` alternative).
- `modules/07-solution-design-context-strategy/README.md` and `checkpoint.md`: full exercise, two-tier gate, conceptual rubric (3 criteria), self-check, takeaway; a 14-question closed-book checkpoint covering CCAR-P Domain 1+2, cited by named objective (not invented task-statement numbers, since no granular numbered breakdown exists in this repo's design docs for these two domains — confirmed by search, not assumed).
- `runs/2026-07-17-module-07-dry-run/`: 5 constructed attempts (1 correct, 4 flawed), all re-verified against the final 20-test suite with clean isolation after every remediation round.
- **`scripts/verify_module_02.py` through `scripts/verify_module_06.py`** (all five already-merged Part 1 checkers): fixed with the same two-layer hardening found via Module 07's doubt-driven-development — test execution now runs in a neutral temp directory (never `cwd=target`), and requires the pytest summary itself report the full expected test count passed (not just a zero exit code).
- `fixtures/foundry/SPEC.md`, `modules/README.md`: status rows updated (Module 07 authored; Modules 01-07 now real, 08-10 skeleton).

### Decisions Made

See `docs/decisions.md`'s 2026-07-17 entries in full — the Part 2 new-system decision, the Foundry scenario choice, Module 07's authoring and design decisions (cache-friendliness as a property distinct from Module 02's retry pattern; the two-artifact-type gate; the no-chain-back-to-Part-1 cumulative-gate deviation), and the three-stage doubt-driven-development review:

- **Stage 1 (Claude subagent):** 10 findings on Module 07's own test suite — a gameable retry-content test, an unexercised default `max_retries`, a memoization loophole, a whitespace-only-`detail` bug, among others.
- **Stage 2 (Codex cross-model):** found the dominant issue — all six checkers ran pytest with `cwd=target`, letting a submission's own `pytest.py` shadow the real installed pytest package and skip the entire test suite while still reporting a clean pass. Empirically confirmed live against Module 04's checker with a real known-broken implementation (the missing-safety-hook bug from Module 04's own earlier doubt-driven-development) plus a shadow file — clean `Deterministic tier: PASS`.
- **Fix 1:** neutral-temp-dir test execution, all six checkers.
- **Stage 3 (Fable-model critique of that remediation):** found the fix closed one vector, not the underlying class — a submission's own code still executes during pytest's collection, so `os._exit(0)` at import time kills the subprocess with return code 0 before any test runs, still reading as a clean pass. Empirically confirmed live the same way, on both Module 04's and Module 07's checkers.
- **Fix 2:** expected-pass-count verification (the pytest summary must report the full expected count passed), all six checkers. Re-verified live: both bypass classes now correctly fail; `correct-attempt` still passes; all 25 Part 1 dry-run attempts and all 5 Module 07 attempts reproduce their exact prior pass/fail pattern (zero regression, checked twice — once after adding `fixtures/foundry/`, once after this fix).
- Also fixed from Stages 1-3: 8 test-suite precision gaps in Module 07's own suite (12→20 tests, detailed in `runs/2026-07-17-module-07-dry-run/grading.md`), and an ADR fence-strip mitigation with its own false-positive guard (only strips balanced ``` fences).

### Assumptions

The expected-pass-count check (`f"{expected} passed" in output`) is a coarse proxy — a substring match on pytest's summary line, not machine-parsed structured output. Sufficient at this project's scale; flagged in `docs/next-actions.md` if a future need for structured results arises. No real learner attempt exists yet for Module 07, same open gap as every prior module.

### Risks

The pytest-shadow and `os._exit` bypasses were live in all 6 checkers' `main` branch code (Modules 02-06 already merged) from each module's original authoring date until this session's fix — no evidence either was exploited (this is a solo/small-audience workshop, not yet publicly load-bearing), but it's a real historical exposure window, not merely a theoretical one caught in review. Recorded here rather than only in `docs/decisions.md` since it's a project-wide risk, not scoped to Module 07.

### Next Actions

Commit and open a PR for Module 07 plus the six-checker security fix together (same root-cause fix, direct precedent from Module 03's doubt-driven-development fixing a shared hole in Module 02's checker in one PR). Then Module 08 (Building and Proving It: Integration, Evaluation & Optimization), continuing Foundry, chaining `check_module_07` for real. See `docs/next-actions.md`.

### Validation status

`scripts/verify_module_07.py` re-run against all 5 attempts after every fix round — correct 20/20, no-retry 10/20, system-prompt-mixes-ticket 17/20, regenerates-prompt-on-retry 19/20, weak-adr 20/20 code (ADR-only fail). Both bypass classes (shadow `pytest.py`, `os._exit(0)`) empirically confirmed closed on both Module 04's and Module 07's checkers, post-fix. Full regression across all 25 Part 1 dry-run attempts re-run twice — zero regression both times, exact prior pass/fail patterns reproduced.

### Mind-palace updated

Not yet this session — pending before push/PR.

## 2026-07-17 (cont'd) - Module 08 authored, continuing Foundry with a genuine RAG exercise; two-cycle doubt-driven-development

Continuing the same session after Module 07's PR merged. User said "lets move onto 8" — proceeded autonomously on scenario design (matching the established pattern for every prior module's exercise design), same as Module 07's own autonomous scenario choice. Mid-session, the user also asked for a review of `claudecertificationguide.com` (an independent, explicitly-unaffiliated third-party study site) for anything worth reusing — found its domain weights, mock-exam structure, and scenario-pool format closely matched what this project had already independently derived from Anthropic's own primary-source PDF, useful as confirmation but nothing new to incorporate, consistent with this project's standing discipline against relying on third-party prep-site content.

### What changed

- `fixtures/foundry/src/doc_qa.py`: ships mostly working (chunking, indexing, retrieval, grounded answer generation all correct as shipped) with one seeded staleness defect in `refresh_index` — checks `doc_id` presence, not content, anchored to the CCAR-P exam guide's own Sample Question 3. Requesting team: the **Platform Docs team**, whose documentation Q&A problem genuinely needs RAG, unlike Module 07's classifier.
- `fixtures/foundry/src/evaluation.py`: ships as a stub (`evaluate`/`compare_top_k`), matching Module 07's build-from-stub shape — the module's second, deliberately independent deliverable.
- `fixtures/foundry/tests/test_doc_qa.py`: canonical suite, grew from 21 (as originally authored) to 34 across two doubt-driven-development review cycles.
- `scripts/verify_module_08.py`: new checker, chains `check_module_07` for real. Applied the neutral-temp-dir + expected-pass-count checker hardening from Module 07's own doubt-driven-development *from the start*, not discovered via a later review this time.
- `runs/2026-07-17-module-08-dry-run/`: 5 constructed attempts (1 correct, 4 flawed — `unfixed`, `stale-fix-only`, `eval-only`, `broken-eval-metric`), each carrying Module 07's own completed work since the gate chains it.
- `modules/08-integration-evaluation/README.md` and `checkpoint.md`: full exercise, two-tier gate, conceptual rubric (3 criteria), self-check, takeaway; a 14-question closed-book checkpoint covering CCAR-P Domain 3+4, cited by named objective (same disclosed citation-style deviation as Module 07's checkpoint, since no granular numbered breakdown exists for these domains either — confirmed by search).
- `fixtures/foundry/SPEC.md`, `modules/README.md`: status rows updated (Module 08 authored; Modules 01-08 now real, 09-10 skeleton).

### Decisions Made

See `docs/decisions.md`'s 2026-07-17 Module 08 entries in full. Summary of the two-cycle doubt-driven-development review (Claude subagent → Codex cross-model → Fable-model critique of the remediation, repeated a second time after Fable's own critique surfaced a further gap):

- **Cycle 1, Stage 1 (Claude subagent):** 8 findings, 3 empirically confirmed live by constructing submissions that passed the original 21-test suite while violating the contract — a `refresh_index` doing a full rebuild every call passed because the "leaves unchanged docs untouched" test only checked value equality on a frozen dataclass; a `refresh_index` mutating its input `index` in place and returning that same object also passed, since the relevant tests compared the returned index against the original *after* the call (tautological when they're the same object); `evaluate`'s default `top_k=3` was never exercised.
- **Cycle 1, Stage 2 (Codex):** found 4 further issues (`evaluate` not forced through real retrieval; `compare_top_k` not forced to evaluate the full dataset per k; `refresh_index`'s shallow copy sharing mutable chunk-list references across old/new index; `answer_question` validating field presence but not type) — and one claim tested live and **refuted**: a fake-summary-line checker bypass that doesn't actually work, because pytest's own output capturing during collection swallows a `print()` before `os._exit(0)` can flush it, confirmed even with an explicit flush call.
- **Cycle 1 fix:** all 8 confirmed findings closed, test suite 21→32, each new test verified live against its own constructed counter-implementation.
- **Cycle 2 (Fable-model critique of that remediation):** found the fix substantially real (independently re-verified the 32-test count and every attempt's isolation numbers) but not fully complete — most severe, **empirically confirmed live**: an `evaluate` hardcoding `top_k=3` internally while `compare_top_k` reimplemented top_k handling as an independent loop (never actually calling `evaluate`) passed all 32 tests, since no test called `evaluate` directly with a non-default `top_k`. Also found a false-failure risk in a spy test (positional-arg coupling) and an untested `failures`-deduplication path.
- **Cycle 2 fix:** all 3 gaps closed, test suite 32→34, each verified against its own constructed mutant. Stop condition met — the third review pass's remaining findings were the already-disclosed out-of-scope assumptions, re-confirmed as genuinely low-risk, requiring no further code changes.

### Assumptions

Two Codex findings (`chunk_size` changing between an index's `build_index` and later `refresh_index` calls; `refresh_index` trusting an externally-corrupted `DocIndex`) were deliberately left unfixed and disclosed as stated assumptions in `refresh_index`'s own docstring, re-confirmed as genuinely low-risk by the Fable critique's own adversarial testing rather than just asserted. No real learner attempt exists yet for Module 08, same open gap as every prior module.

### Risks

No new risks beyond `docs/risks.md`'s existing RISK-0004 (closed, from Module 07's own checker-bypass finding) — Module 08's checker was built with that fix applied from the start, so it never carried the same exposure window.

### Next Actions

Commit and open a PR for Module 08. Then Module 09 (Shipping Responsibly: Governance, Stakeholders & Team Enablement), continuing Foundry, chaining `check_module_08` for real — scenario not yet decided, covering CCAR-P Domain 5+6+7. See `docs/next-actions.md`.

### Validation status

`scripts/verify_module_08.py` re-run against all 5 attempts after every fix round — correct 34/34, unfixed 15/34 (19 fail), stale-fix-only 20/34 (14 fail), eval-only 29/34 (5 fail, all staleness-related), broken-eval-metric 28/34 (6 fail, all metric-related, disjoint from eval-only's). Every subtle new test (no-recompute spy, no-mutation snapshot, list-independence, real-retrieval-routing, full-dataset-per-k, non-default-top_k, duplicate-query-dedup) verified live against its own hand-constructed counter-implementation before being trusted, not just written and assumed correct. Full regression across all 25 Part 1 dry-run attempts and all 5 Module 07 attempts re-run multiple times through both review cycles — zero regression throughout.

### Mind-palace updated

Not yet this session — pending before push/PR.

## 2026-07-17 (cont'd) - Module 09 authored, continuing Foundry with a shipping-decision exercise; doubt-driven-development's most severe finding to date

Module 09 (Shipping Responsibly: Governance, Stakeholders & Team Enablement) breaks the pattern every prior Part 2 module followed — it doesn't open on a new internal team's problem. It asks what has to happen before Module 08's own `doc_qa` system actually ships, given the Platform Docs corpus references genuinely sensitive content. Its doubt-driven-development review found the single most severe issue of any module in this project: a submission checking the query string instead of retrieved chunk content for sensitivity passed all 14 original tests while completely defeating the module's core safety property.

### What changed

- `fixtures/foundry/src/governance.py`: ships as a stub (`answer_question_with_governance`/`approve_and_release` raise `NotImplementedError`; `contains_sensitive_content` ships implemented) — a human-in-the-loop gate wrapping `doc_qa.answer_question`, inspecting retrieved chunks for sensitive content (keyword-based: SSN, password, credential, etc.) before ever calling `model_client`.
- `fixtures/foundry/tests/test_governance.py`: canonical suite, grew from 14 (as originally authored) to 17 via doubt-driven-development.
- `scripts/verify_module_09.py`: new checker, chains `check_module_08` for real. Validates three structurally different deliverables in one gate — code (governance tests), prose (a regex-section-checked shipping-readiness review, reusing Module 07's `check_adr` pattern), and filesystem config (`.claude/` team tooling, reusing Module 01's frontmatter-parsing helpers).
- `runs/2026-07-17-module-09-dry-run/`: 5 constructed attempts (1 correct, 4 flawed — `unfixed`, `no-review-doc`, `weak-tooling`, `bypasses-model-client`), each carrying Modules 07-08's own completed work since the gate chains through both.
- `modules/09-governance-stakeholders/README.md` and `checkpoint.md`: full exercise, two-tier gate, conceptual rubric (3 criteria), self-check, takeaway; a 14-question closed-book checkpoint covering CCAR-P Domain 5+6+7.
- **`scripts/verify_module_01.py`**: a real, shared precision bug fixed alongside Module 09's own — Codex confirmed the same bare-directory-glob-match weakness (`paths: ["src"]` with no wildcard satisfying "scopes real files" without matching any real file) existed in Module 01's own already-merged checker, since Module 09 reused its frontmatter-parsing helpers. Fixed in both at once.
- `fixtures/foundry/SPEC.md`, `modules/README.md`: status rows updated (Module 09 authored; Modules 01-09 now real, Module 10 skeleton).

### Decisions Made

See `docs/decisions.md`'s 2026-07-17 Module 09 entries in full. Summary of the doubt-driven-development review:

- **Stage 1 (Claude subagent):** most severe finding of any module to date, **empirically confirmed live**: every one of the 14 original tests placed the sensitive marker word in both the query string and the retrieved chunk's text, so a submission checking `contains_sensitive_content(query)` instead of each chunk's own content passed all 14 tests while completely defeating the module's purpose. Also found the shared `.claude/` checker weakness and disclosed (not fixed) `approve_and_release`'s lack of binding to a real identity system.
- **Stage 2 (Codex):** confirmed the query-vs-chunk finding and the shared checker bug's root cause, then found its own dominant, **empirically confirmed live** issue: `review_reason` could leak the actual sensitive chunk content back to the caller (`review_reason = flagged[0].text` passed all 14 tests) — the field meant to protect the content instead exposed it.
- **Fixed:** two new tests closing both critical gaps, `answer is None` assertions added to 3 previously-uncovered withholding tests, a default-`top_k` test for `approve_and_release` (suite 14→17); the shared bare-directory-match bug fixed in both `verify_module_01.py` and `verify_module_09.py` at once, re-verified live that the bypass is closed on both and that all of Module 01's own dry-run attempts plus the full 25-attempt Part 1 regression (which chains through `check_module_01`) still reproduce their exact expected pattern.
- **Stage 3 (Fable-model critique):** unavailable this session — returned "Usage credits are required for this model," an account-level limit. Proceeded without it on explicit user direction rather than retrying indefinitely; logged as `RISK-0005` (open) rather than silently treated as complete.

### Assumptions

`contains_sensitive_content`'s keyword-based detection remains a coarse, disclosed proxy (won't catch a bare SSN digit pattern without the word "SSN" nearby), matching `doc_qa.py`'s own `score_chunk` precedent. `approve_and_release`'s lack of binding to a specific flagged query or real identity system is a genuine, disclosed simplification given no real auth system exists in this environment. No real learner attempt exists yet for Module 09, same open gap as every prior module.

### Risks

New: `RISK-0005` (open) — Module 09's doubt-driven-development only completed 2 of 3 standard stages; the Fable-model critique should be re-run against the current, already-twice-fixed files once access is restored. See `docs/risks.md`.

### Next Actions

Commit and open a PR for Module 09 plus the shared Module 01 checker fix together (same precedent as Module 07's project-wide security fix). Then Module 10 (Professional Capstone), continuing Foundry, chaining `check_module_09` for real — closes Part 2 in full. See `docs/next-actions.md`.

### Validation status

`scripts/verify_module_09.py` re-run against all 5 attempts after every fix round — correct 17/17, unfixed 5/17 (12 fail) plus missing review/tooling, no-review-doc 17/17 code (review-only fail), weak-tooling 17/17 code (tooling-only fail, 2 checks), bypasses-model-client 11/17 (6 fail, all governance/call-order-related). Both critical new tests verified live against their exact target mutants (query-vs-chunk confusion, review_reason content leak) before being trusted. The shared Module 01/09 checker fix verified live on both checkers plus a full 25-attempt Part 1 regression re-run — zero regression.

### Mind-palace updated

Not yet this session — pending before push/PR.

## 2026-07-17 (cont'd) - Module 10 authored, closing Part 2 and the workshop's full content arc; three-cycle doubt-driven-development finds and fixes the most varied set of issues of any module to date

Module 10 (Professional Capstone: Sit-Ready for CCAR-P) is the tenth and final module, closing Part 2 (Architect Professional) and this workshop's whole 10-module arc. Unlike every prior Part 2 module, it's purely written — no new source file — because the exercise is synthesis, not new build: defending Foundry's own three-system design (`ticket_triage`, `doc_qa`/`evaluation`, `governance`) in writing against a real, seeded VP-of-Engineering objection to consolidate into one general-purpose assistant. Its doubt-driven-development review ran a full three cycles (fresh Claude subagent, Codex cross-model, Fable critique of the remediation) and found a wider variety of issue classes than any prior module — checker exploits, a self-inflicted answer-shuffle corruption bug, a reshuffle that traded one gameable pattern for another, a fix that would have unfairly failed honest learner writing, and a project-wide construct-validity issue predating this module's own authoring.

### What changed

- `scripts/verify_module_10.py`: new checker, chains `check_module_09` (the final link: 07→08→09→10). Validates one prose deliverable (`docs/capstone-architecture-defense.md`) via regex-section-extraction (reusing Module 07/09's `check_adr`/`check_readiness_review` pattern) plus content checks strengthened substantially through this session's three DDD cycles — see Decisions below.
- `runs/2026-07-17-module-10-dry-run/`: 4 constructed attempts (`correct-attempt`, `no-defense-attempt`, `generic-essay-attempt`, `no-real-criterion-attempt`), each carrying Modules 07-09's own completed work since the gate chains through all three. `grading.md` rewritten to reflect the full three-stage DDD story.
- `modules/10-professional-capstone/README.md`: full exercise — the seeded VP objection, four required sections, conceptual rubric (3 criteria), self-check, takeaway (a personal CCAR-P exam-day prep sheet, same discipline as Module 06's).
- `modules/10-professional-capstone/checkpoint.md`: a 42-question, 6-scenario mock exam scaled to CCAR-P's 7 domains and real 63-item/120-minute/720-1000-scoring format (like Module 06 did for CCA-F), including 2 multiple-response questions — new for this capstone, matching the real exam's own format. Went through extensive revision this session: an all-one-letter answer bug and a domain mislabel self-caught before any review; a mechanical answer-shuffle script that corrupted 4 explanation lines, reverted and rebuilt narrower; a second reshuffle after Codex found the first one formed a literal repeating letter cycle; a third reshuffle after Fable found per-scenario letter clustering the second one missed; and a full rewrite of all 42 questions' distractors (Fable's construct-validity finding, fixed per explicit user direction rather than only disclosed).
- `fixtures/foundry/SPEC.md`, `modules/README.md`: status rows updated — all 10 modules now real, the workshop's full content arc complete.
- `docs/decisions.md`, `docs/next-actions.md`, `docs/risks.md`, `.hekton/risk-register.yaml`: this module's full authoring + DDD record; RISK-0005 updated to note Fable access is confirmed restored (successfully ran all 3 stages this session), though Module 09's own retro Stage-3 pass remains separately un-run.

### Decisions Made

Full detail in `docs/decisions.md`'s 2026-07-17 Module 10 entries. Summary:

- **Self-caught, before any external review:** an all-one-letter answer bug (39 of 40 "B") and a domain mislabel (3 questions wrongly tagged Domain 1 instead of the established Domain 5), both caught via `grep` against this project's own precedent. A first answer-shuffle script then corrupted 4 explanation lines via an over-broad regex (matching the English article "A" and the term "A/B testing" mid-sentence) — no git history to revert to, so the pre-shuffle content was reconstructed from conversation context and the shuffle rebuilt with a narrower, leading-clause-preserving regex.
- **Stage 1 (Claude subagent):** 9 findings. One (a claimed D4/F3 domain mislabel) checked against Module 08's own established mapping and found to be **not a bug** — classified as noise. Real: two checker exploits (a throwaway-sentence "Defense" bypass; a falsifiability section combining a trigger word with an explicit refusal to reconsider), two reference-defense gaps (a false binary on the "coordinator" alternative; an unrebutted onboarding-cost argument), two negative dry-run attempts not isolating cleanly, one weak distractor.
- **Stage 2 (Codex):** found the reshuffled answer key formed a literal repeating A,B,C,D cycle (worse than the "always B" bug caught during authoring — predictable by position) and both multiple-response questions shared the identical correct pair. Also found a checker-fix side effect breaking one negative fixture's isolation, the other negative fixture not exercising its intended bypass, a factual overstatement in the reference defense's steelman, and an underspecified falsifiability condition.
- **Stage 3 (Fable, critiquing the Stage 1+2 remediation itself):** found the remediation's own new checks had gaps, most seriously a **false-positive risk** — the fix's whole-sentence negation exclusion would have incorrectly failed genuinely honest writing describing real system guarantees in negation-shaped language ("sensitive content never reaches a model call"). Also found the falsifiability check's fixed-phrase list was dodgeable by direct synonym substitution, a self-contradiction introduced by Stage 2's own "coordinator" paragraph fix, a stale negative fixture, and — separate from anything introduced this session — a project-wide, pre-existing construct-validity gap: every one of the 42 questions' distractors used absolute-quantifier language while the correct answer was consistently the hedged option, letting a test-taker score well by surface pattern-matching.
- **Fixed, all three stages:** checker strengthened with a `DEFENSE_MIN_CHARS` floor specific to "The Defense," a risk-vocabulary + minimum-distinct-terms check (redesigned from whole-sentence negation exclusion to a narrow, proximity-based self-denial-phrase check after Fable's false-positive finding), and a falsifiability check redesigned from fixed phrases to same-sentence co-occurrence of a broadened refusal-word class and reconsider-verb class. The answer key reshuffled a third time with an added per-scenario balance constraint. The reference defense's coordinator paragraph rewritten to resolve its self-contradiction; the onboarding-cost rebuttal and a corrected steelman synced across all fixtures. **All 42 questions' distractors rewritten** across all 6 scenarios to remove absolute-quantifier tells while preserving each option's original category of wrongness — offered as a scope choice via `AskUserQuestion`, user chose the full rewrite over disclosure-only or a partial sample.

### Assumptions

The risk-vocabulary check's residual gap (a purely affirmative, non-negated buzzword mention can still pass) is a disclosed, accepted limitation — no lexical check distinguishes real engagement from name-dropping in every case; the conceptual rubric is the backstop, same precedent as every other prose checker in this project. No real learner attempt exists yet for Module 10, same open gap as every prior module.

### Risks

`RISK-0005` updated, not closed — Fable access confirmed restored (ran successfully for all of Module 10's DDD), but Module 09's own retro Stage-3 critique against its current files still hasn't been run. See `docs/risks.md`.

### Next Actions

Commit and open a PR for Module 10. This closes the workshop's full 10-module content arc — next real milestone per the dogfooding commitment is scheduling the real CCAR-P exam sit. See `docs/next-actions.md`.

### Validation status

`scripts/verify_module_10.py` re-run against all 4 attempts after every fix round, plus against Fable's own constructed bypass documents (a hollow-denial defense, a synonym-dodged falsifiability section, an honest-writing negation-shaped defense) — correct-attempt passes clean, all 3 flawed attempts fail exactly their own intended check, both of Fable's adversarial bypasses now correctly fail, and the honest-writing counterexample now correctly passes (confirming the false-positive fix). Checkpoint's structural integrity (42 questions, 168 options, 42 answer-key entries, global and per-scenario 10/10/10/10-ish letter distribution, "A/B testing" term preservation, keyword-overlap cross-check against every single-answer question) reconfirmed after every content revision. Full regression across all 44 attempts project-wide (Modules 01-10) re-run multiple times through all three review cycles — zero regression throughout.

### Mind-palace updated

Not yet this session — pending before push/PR.

---

## 2026-07-17 (cont'd) - Custom domain cutover (closed-book.coderturtle.io), following agentic-infra-lab's github-pages-dns onboarding template

**Agent:** Claude

### What changed

- In `agentic-infra-lab` (separate repo, not this one): onboarded closed-book as the fourth
  `github-pages-dns` Terraform consumer (`module "pages_dns_closed_book"`), real TXT
  name/value supplied by the user, read-only Route53 preflight confirmed no existing record,
  `terraform plan` (read-only) → 2 to add, 0 to change, 0 to destroy, classified GREEN. Full
  record in that repo's own `docs/session-log.md`/`docs/next-actions.md`.
- Followed `docs/github-pages-dns-implementation-plan.md`'s Phase 3 template (step 11a) rather
  than leaving it as a manual bullet: ran `gh api --method POST` then `PUT
  repos/coderturtle/closed-book/pages` directly, under the user's own already-authenticated
  `gh` session (not a CI workflow — `GITHUB_TOKEN` cannot make this call, per ADR-008).
  Confirmed: `cname: closed-book.coderturtle.io`, `protected_domain_state: "unverified"`
  (expected at this stage, not a failure — verification is a separate, later, browser-only step
  with no API, per ADR-010).
- On branch `agent/claude/custom-domain-cutover`: `site/astro.config.mjs` (`site`/`base`
  cutover, same shape as terminal-velocity's), new `site/public/CNAME`, `.hekton/project.yaml`
  gained a `deployment` block (`human_confirmed: false` — the DNS apply hasn't happened yet),
  and `.github/workflows/deploy-pages.yml`'s stale "no custom domain for this workshop" comment
  corrected. `npm run build` reconfirmed clean; routes generate at the domain root, `dist/CNAME`
  present.

### Decisions Made

See `docs/decisions.md`'s 2026-07-17 "Cut over from project-page hosting" entry.

### Assumptions

None new — TXT/cname values taken verbatim from the user and from GitHub's own API response, not
derived.

### Risks

No new RISK entry. Same open items as every prior workshop's cutover: HTTPS cert issuance is
async and unconfirmed until DNS resolves; domain verification is a required, easy-to-silently-skip
manual step (RISK-0008 precedent in agentic-infra-lab).

### Next Actions

See `docs/next-actions.md`'s updated "Later" section: human `terraform apply` in
agentic-infra-lab (the only step this template leaves to the human), then GitHub's browser-only
domain verification once DNS resolves, then review/merge this branch's PR before the first real
`workflow_dispatch` deploy.

### Validation

- `npm run build` (site) — clean, 11 pages, `dist/CNAME` = `closed-book.coderturtle.io`.
- `gh api repos/coderturtle/closed-book/pages` — real, live API call confirming `cname` and
  `build_type` set correctly.
- `grep` for hardcoded `/closed-book/` links in `site/src/` before the cutover — none found, so
  the base-path change carried no link-breakage risk.

### Mind-palace updated

No — not yet authorised this session.

---

## 2026-07-18 - DNS live; PR #15 merged; domain verification is the one step left

**Agent:** Claude

### What changed

- Human ran `terraform apply` in `agentic-infra-lab` for closed-book's DNS. Verified live via
  `dig` against public resolvers (CNAME → `coderturtle.github.io.`, TXT value matches), not just
  trusted from Terraform's output. `.hekton/project.yaml`'s `deployment` block updated:
  `record_fqdn`, `verification_record_fqdn`, `applied_date: 2026-07-18`,
  `human_confirmed: true`.
- Merged PR #15 (`agent/claude/custom-domain-cutover`) into `main` — fast-forward. Local branch
  and remote feature branch both cleaned up.

### Decisions Made

None new.

### Risks

No new RISK entry.

### Next Actions

See `docs/next-actions.md`: human completes GitHub Pages domain verification
(`github.com/settings/pages`, browser-only, no API) now that DNS resolves publicly, then triggers
the first real `workflow_dispatch` deploy.

### Validation

- `dig +short CNAME closed-book.coderturtle.io` / `dig +short TXT
  _github-pages-challenge-coderturtle.closed-book.coderturtle.io` — real, live queries.
- `gh pr view 15` confirmed `MERGED`.

### Mind-palace updated

No — not yet authorised this session.

---

## 2026-07-18 (cont'd) - First deploy tested end to end; push trigger enabled

**Agent:** Claude

### What changed

- GitHub Pages domain verification already showed `protected_domain_state: "verified"` when
  checked this session (completed by the human since the last check).
- Triggered the first real deploy via `gh workflow run deploy-pages.yml` (run `29638332750`),
  matching `deploy-pages.yml`'s own stated Human Gate ("first deploy is workflow_dispatch-only,
  run on explicit human confirmation"). Watched it live: build (24s) and deploy (8s) both green.
- Confirmed the site is actually live, not just that the workflow reported success:
  `curl http://closed-book.coderturtle.io/` returned real rendered HTML (nav, recent build-log
  entries, footer). HTTPS isn't up yet (`https_certificate: null`) — expected, GitHub issues it
  asynchronously post-verification, same precedent as every prior workshop's first hour.
- Human Gate condition met, so uncommented `deploy-pages.yml`'s `push` trigger (branch
  `agent/claude/enable-push-deploy`) — subsequent `site/**`/`docs/build-log/**` changes on `main`
  now auto-deploy, same as terminal-velocity/borrow-native/half-life.

### Decisions Made

None new — this executes the Human Gate the workflow file already specified, doesn't change it.

### Risks

No new RISK entry.

### Next Actions

Review/merge the `agent/claude/enable-push-deploy` PR. Spot-check HTTPS once GitHub's cert
issues (non-blocking, async).

### Validation

- `gh run watch 29638332750` — both jobs green, live.
- `curl http://closed-book.coderturtle.io/` — real content returned, not a placeholder/404.
- `gh api repos/coderturtle/closed-book/pages` — `protected_domain_state: "verified"`,
  `https_certificate: null` (expected, not a failure).

### Mind-palace updated

No — not yet authorised this session.
