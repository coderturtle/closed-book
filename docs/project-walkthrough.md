# Closed Book — Plain-English Project Walkthrough

## What this project is in one paragraph

Learn Anthropic's Claude Certified Architect material (Foundations to Professional) the agent-native way: hands-on Claude Code exercises gated by closed-book practice checkpoints against the published exam blueprint.

## The simple analogy

## What problem we are solving

## What we have built so far

- Scaffolded 2026-07-14 — repo and vault control plane created; naming pass (Closed Book), scope correction (Claude Architect, not Developer), design docs, and a 7-persona Workshop Review Panel pass all complete the same day.
- All 10 modules authored 2026-07-15 through 2026-07-17: each has a real hands-on exercise, a deterministic checker (chained cumulative-gate convention), a closed-book checkpoint, and a completed multi-attempt dry run. Every module went through a doubt-driven-development review (fresh Claude subagent + Codex cross-model, most with a third Fable-model critique of the remediation) before being treated as done — see `docs/decisions.md` for the full record, module by module.
- Part 1 (Modules 01-06, Architect Foundations) builds one shared project, `resolve`; Part 2 (Modules 07-10, Architect Professional) builds a second, `foundry` — both real, working systems, not disconnected snippets.
- A systemic checker-execution bypass (submissions could shadow pytest or exit early to fake a clean pass) was found and closed across all six checkers, 2026-07-17.
- Custom domain live: `closed-book.coderturtle.io`, via `agentic-infra-lab`'s `github-pages-dns` Terraform pattern. First deploy and the push-triggered auto-deploy both tested end to end and confirmed working, 2026-07-18.
- Not yet done: the maintainer's own dogfooding commitment (sitting the real CCA-F/CCAR-P exams) — stated intent, not yet evidenced. See `docs/next-actions.md`.

## How the pieces fit together

## What is deliberately not automated yet

## How this could connect to the wider Hekton factory



## Current confidence level

Medium-High for the shipped content and deployment pipeline (all 10 modules real, DDD-reviewed,
deployed and confirmed live via direct verification, not just green CI). Low-to-unproven for the
workshop's own central hypothesis — that hands-on-with-Claude-then-closed-book-quiz produces
better exam readiness than alternatives — since that's evidenced only by the real CCA-F/CCAR-P
exam attempts, which haven't happened yet.

## Open questions

-

## Next recommended session

Review the brief, define the first hypothesis or phase plan, and implement the first working step.
