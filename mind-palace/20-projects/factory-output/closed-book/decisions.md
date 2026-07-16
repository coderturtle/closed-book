# Decisions: Closed Book

| Date | Decision | Rationale |
|---|---|---|
| 2026-07-14 | Project scaffolded as factory-output | Initial setup |
| 2026-07-14 | Naming pass complete: renamed to **Closed Book** | Chosen by coderturtle from naming-agent candidates, GitHub-slug-checked first. |
| 2026-07-14 | **Correction:** target redirected from "Claude Developer" to **Claude Architect**, Foundations → Professional | No "Developer Professional" exam exists; Architect is the only track with both levels today. |
| 2026-07-14 | Module arc anchored to Anthropic's own primary-source exam guide PDFs | Secondary "exam prep" sites recycled unreliable, possibly-conflated domain lists; fetched and read the real CCA-F/CCAR-P guides in full instead. |
| 2026-07-14 | 10-module arc (6 Foundations + 4 Professional, two capstones), not the originally-scoped 8 | CCA-F has 5 real domains, CCAR-P has 7 — forcing 4+4 would misrepresent the exams' real weights/dependency order. |
| 2026-07-14 | Two-tier module gate: hands-on Claude Code artifact, then closed-book no-AI checkpoint | Resolves the named learn-with-AI/test-without-AI tension. Stated hypothesis, not yet evidenced. |
| 2026-07-14 | Dogfooding commitment: sit the real CCA-F exam after Modules 01-06, CCAR-P after 07-10 | Same discipline as Borrow Native's Ardan Labs commitment. |
| 2026-07-14 | Build-log/Pages site adapted from Borrow Native's Astro starter | Pipeline validated twice already; locally validated build + astro check clean. |
| 2026-07-15 | Modules 01-06 build one shared project, `resolve` | Modeled on CCA-F's own Scenario 1 (customer support resolution agent). |
| 2026-07-15 | Module 01 authored for real, with a completed dry run | Deterministic checker validated against 3 constructed attempts; caught a real bug in itself. |
| 2026-07-15 | Doubt-driven-development review of Module 01 (Claude + Codex + Fable) | Found the closed-book tier didn't exist, checker had real bugs, rubric violated its own rules. |
| 2026-07-15 | Full remediation: checkpoint authored, checker rewritten in Python, compatibility contract added | 4th dry-run attempt confirms the conceptual tier catches what the deterministic tier structurally can't. |
| 2026-07-15 | Module 02 authored, both tiers together from the start | Deterministic tier: real pytest suite against a learner-implemented extraction.py, chaining Module 01's checker (cumulative gate). |
| 2026-07-15 | Dry run constructed 2 differently-shaped naive attempts | A broadly-failing no-retry attempt and a narrowly-failing fabrication bug (`or 0` collapsing an honest None). |
| 2026-07-15 | Doubt-driven-development review of Module 02 (Claude + Codex + Fable) | Dominant finding: the exercise interface never required the prompt/few-shot artifact 2 rubric criteria graded. |
| 2026-07-15 | Structural fix: changed the exercise interface, not the rubric | Added build_extraction_prompt/FEW_SHOT_EXAMPLES as real deliverables; zero changes needed to the original 7 tests. |
| 2026-07-15 | Remaining remediation: test suite grew 7->14, checkpoint precision fixes, 4th dry-run attempt | 4th attempt (weak-few-shot) passes all 14 tests while failing rubric criterion 3 — closes the conceptual-tier validation gap. |
| 2026-07-15 | Module 03 authored (4 MCP tools), both tiers together, lessons applied proactively | Real bug found and fixed before grading: tool descriptions were module-level docstrings, not the function's own `__doc__`. |
| 2026-07-15 | Dry run constructed 2 attempts closing the conceptual-tier gap proactively | `trusts-caller-attempt` (skips re-verification) and `weak-docstring-attempt` (passes tests, no real boundary reasoning). |
| 2026-07-15 | Doubt-driven-development review of Module 03 (Claude + Codex + Fable) found the checker chain was broken and trusted learner-editable test files | Two structural issues worse than either prior module's review, both fixed same day. |
| 2026-07-15 | Fixed: unified check_module_NN interface + canonical-test execution (checkers now run the repo's own test file, not the submission's copy) | Verified empirically a tampered test file no longer helps a broken submission pass. Applied retroactively to Module 02's checker too. |
| 2026-07-15 | Fixed: canonical-test execution applied retroactively to Module 02's checker too | Same trust-boundary hole existed there; verified a tampered test file no longer helps either module's broken submissions pass. |
| 2026-07-15 | Remaining Module 03 remediation: test suite grew 16->20, ordering test, error-category semantics documented | Closes the gap between claimed and actual docstring coverage; makes the safety property a real gate, not prose. |
| 2026-07-15 | Module 04 authored (coordinator agent + hook), both tiers together, lessons applied proactively | 12-test suite against `run_support_session`/`verify_before_refund_hook`, using spy tools rather than Module 03's real ones to isolate this module's own exercise. |
| 2026-07-15 | Resolved Module 03's deferred stateful-backend question: Module 04 stays orchestration-only, no refund persistence | Refund execution/idempotency is Domain 2 (tool design) territory Module 03 already resolved, not Domain 1 (orchestration), which is what this module teaches. |
| 2026-07-15 | Dry run constructed 4 attempts, one built proactively to close the conceptual-tier gap before an external review found it | `thin-docstring-attempt` passes all 12 tests with zero documented reasoning — first module to apply this discipline from the start, not via remediation. |
| 2026-07-15 | Doubt-driven-development review of Module 04 (Claude + Codex) found the hook didn't bind to *which* customer was verified | A session verifying customer A could refund customer B, undetected by all 5 dry-run attempts, both reviewers reproduced it live against the checker. |
| 2026-07-15 | Fixed: identity-bound hook enforcement | `SessionState.verified_customer_id`, set only from a successful `get_customer` result's actual customer_id; test suite grew 12->16. |
| 2026-07-15 | Fixed 4 further issues from the same review | Test-double `backend`-omission loophole, a factually-wrong checkpoint answer on session forking, a stale Module 03 README contradiction, a checkpoint/README pass-threshold mismatch. |
| 2026-07-15/16 | Fable-model critique of the remediation itself (not just the original findings) before treating Module 04 as done | Verdict: sound at its core, no scope creep, but incomplete at the documentation edges. |
| 2026-07-16 | Fixed 3 gaps Fable's critique found | Stale pre-fix rule statements in live docs, a stale quotation in the shipped test file, and an untested false-allow direction of the identity-binding bug — test suite grew 16->17. |

Full ADR log with rationale detail: repo `docs/decisions.md`.
