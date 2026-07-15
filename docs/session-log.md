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
