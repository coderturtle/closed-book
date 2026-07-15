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
| 2026-07-15 | Module 02 authored, both tiers together; doubt-driven-development review found the exercise interface didn't require a prompt artifact | Fixed by adding build_extraction_prompt/FEW_SHOT_EXAMPLES as real deliverables, not by weakening the rubric. Test suite grew 7->14; 4th dry-run attempt closes the same conceptual-tier validation gap Module 01's did. |

Full ADR log with rationale detail: repo `docs/decisions.md`.
