# CODEX.md — Closed Book

## Project Classification

- **Type:** factory-output
- **Name:** closed-book
- **Local repo:** /Users/hekton/Development/hekton/factory-output/closed-book
- **Vault control plane:** /Users/hekton/vaults/hekton-mind-palace/20-projects/factory-output/closed-book
- **Lifecycle stage:** active
- **Promotion target:** none
- **Privacy boundary:** public
- **Owner:** coderturtle

## Codex Rules

Follow all rules in `~/hekton/CODEX.md` — including the **Hekton Repository Taxonomy**, **Hekton Documentation Contract**, and **Ongoing Hekton Project Operating Rules** sections.

Before coding:
1. Work on a short-lived `agent/<agent-name>/<task-slug>` branch and never commit directly to `main`/`master` — see `~/hekton/.rules/git-contract.md`
2. Read `.hekton/project.yaml` to confirm classification and paths
3. Read `docs/project-walkthrough.md` for plain-English project context
4. Read `docs/session-log.md` for recent session history
5. Read `docs/decisions.md` for prior decisions that constrain this work
6. Read `docs/next-actions.md` for the current work queue
7. Do not add a `hekton-` prefix to files unless this is a platform repo
8. Do not commit vault paths or local filesystem paths to git

At end of session, output: changed files, decisions, assumptions, risks, next actions, validation status, vault updated (yes/no). **If this session made changes to the repo**, also run `bash ~/hekton/scripts/end-session.sh` (works from anywhere inside this repo) to log the session and capture Blog Radar / Gremlin Radar signals. **Do not run it for a read-only session** (e.g. a review that made no edits) — it writes to `docs/session-log.md` and central ledgers, which a read-only reviewer should never do. (An unconditional version of this instruction caused a read-only adversarial-review agent to attempt running it during a doubt-driven-development pass on 2026-07-15; it failed safely under a read-only sandbox, but the instruction itself was the bug — see `CLAUDE.md`.)
