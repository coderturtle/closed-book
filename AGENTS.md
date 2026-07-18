# AGENTS.md — Closed Book

## Project Classification

- **Type:** factory-output
- **Local repo:** /Users/hekton/Development/hekton/factory-output/closed-book
- **Vault:** /Users/hekton/vaults/hekton-mind-palace/20-projects/factory-output/closed-book
- **Vault mutation allowed:** see `vault_mutation_allowed` in `.hekton/project.yaml` (authoritative)
- **Owner:** coderturtle

## Shared Agent Rules

Follow all rules in `~/hekton/AGENTS.md` — including the **Hekton Documentation Contract**, **Ongoing Hekton Project Operating Rules**, and traceability requirements.

This project is classified as **factory-output**. All agents must:
1. Work on a short-lived `agent/<agent-name>/<task-slug>` branch and never commit directly to `main`/`master` — see `~/hekton/.rules/git-contract.md`
2. Read `.hekton/project.yaml` before making structural changes
3. Read `docs/project-walkthrough.md` before structural changes
4. Stay within `/Users/hekton/Development/hekton/factory-output/closed-book` for code changes
5. Update `docs/decisions.md` for any significant design decisions
6. Append to `docs/session-log.md` at end of every session
7. Update `docs/next-actions.md` when the work queue changes
8. Not promote this project to a new lifecycle stage without user confirmation

## Traceability Artefacts

All of the following must be kept current:

| Artefact | Location |
|---|---|
| `.hekton/project.yaml` | repo root |
| `docs/session-log.md` | repo docs/ |
| `docs/decisions.md` | repo docs/ |
| `docs/risks.md` | repo docs/ |
| `docs/operating-model.md` | repo docs/ |
| `docs/project-walkthrough.md` | repo docs/ |
| `docs/next-actions.md` | repo docs/ |
| `index.md` (project card) | vault control plane |
| `session-log.md` (brain learning layer) | vault control plane |

## Session Closeout & Radar

**If this session made changes to the repo**, close it by running `bash ~/hekton/scripts/end-session.sh` from anywhere inside this repo. **Do not run this for a read-only session** (e.g. a review or audit that made no edits) — it writes to `docs/session-log.md` and central ledgers, which a read-only reviewer should never do. (An unconditional version of this instruction caused a read-only adversarial-review agent to attempt running it during a doubt-driven-development pass on 2026-07-15; it failed safely under a read-only sandbox, but the instruction itself was the bug — see `CLAUDE.md`.)

It writes the session log and captures Blog Radar (`--blog-worthy`) and Gremlin Radar (`--gremlin-radar`) signals into the central ledgers under `~/hekton/state/`. A project-local `scripts/end-session.sh`, if one is ever added, must keep capturing Blog Radar signals via `~/hekton/scripts/capture-blog-signal.sh`.
