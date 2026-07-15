# Risks: Closed Book

## Risk Register

Machine-readable risk state lives in `.hekton/risk-register.yaml`. Keep this
Markdown file as the human-readable explanation of material risks and mitigations.

| ID | Date | Risk | Impact | Likelihood | Mitigation | Status |
|---|---|---|---|---|---|---|
| RISK-0001 | 2026-07-14 | Initial governance baseline needs first human/agent review | Medium | Medium | Run governance preflight and end-session review during the first material session | Open |
| RISK-0002 | 2026-07-14 | `site/`'s Astro starter (adapted from Borrow Native) carries 4 inherited npm vulnerabilities (3 low, 1 high: XSS/SSRF classes in Astro <=7.0.0-alpha.1, an esbuild dev-server file-read issue) | Low (static-site build/dev tooling only, no server-side runtime in the deployed output) | Low | Run `npm audit fix --force` (breaking change to astro@7.0.9, needs a full re-validation of build + `astro check`) before the first real Pages deploy, not after — same discipline Borrow Native applied | Open |
| RISK-0003 | 2026-07-14 | Closed-book practice checkpoints are self-administered in a facilitator-less public repo; nothing technically prevents a learner from keeping Claude Code open during a checkpoint | Medium (undermines the workshop's central claim if widespread, but doesn't affect other learners) | Medium | README states an explicit closed-book ritual (close/minimize the session, separate device, real timing); no technical enforcement exists or is planned — this is a stated, accepted limitation, not a gap to silently close later | Open |
