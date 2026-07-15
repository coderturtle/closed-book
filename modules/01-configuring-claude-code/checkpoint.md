# Module 01 closed-book checkpoint

**Format:** 12 questions, 15 minutes, 80% (10/12) to pass. Multiple choice, one correct answer, three distractors.

**Before you start:** close or minimize your Claude Code session. No notes, no AI assistance, no searching. This checkpoint exists to rehearse the exact condition the real CCA-F exam imposes — see [`docs/design-tension.md`](../../docs/design-tension.md). If you complete this with Claude Code open in another tab, you've passed a checkpoint, not demonstrated the thing it exists to check.

**Coverage note:** this checkpoint, not the hands-on exercise, carries full coverage of CCA-F Domain 3's Task Statements 3.1–3.6. The hands-on tier can only test what produces an artifact (config structure, a working rule, a working command); process judgment calls (when to use plan mode, how to iterate) have no artifact to build, so they're tested here instead. Two questions per task statement, in order.

**Originality note:** every question below is written originally against the published task statement it tests. None are copied or reworded from Anthropic's real exam, any leaked item bank, or Anthropic's own official sample questions — see `docs/design-tension.md`'s Constraint section.

---

## Questions

**1. (Task Statement 3.1)** A `resolve` contributor wants every teammate's Claude Code session to always run `/review-tool` before shipping a new MCP tool. They add the instruction to `~/.claude/CLAUDE.md` on their own machine. A new teammate clones the repo and never sees the instruction. What's the most likely cause?

A) User-level `CLAUDE.md` isn't shared via version control — the instruction never reached the new teammate's machine at all.
B) The instruction needs `@import` syntax to take effect.
C) Claude Code only reads directory-level `CLAUDE.md` files, not user-level ones.
D) The new teammate needs to run `/memory` to load the instruction.

**2. (Task Statement 3.1)** `resolve`'s root `CLAUDE.md` has grown to include the safety rule, tool conventions, testing conventions, and unrelated notes about the team's deploy schedule, all in one file. What's the most direct fix for keeping it modular without losing anything?

A) Split topic-specific content into `.claude/rules/` files (for path-scoped conventions) or separate imported files via `@import` (for content that should always load but doesn't belong inline), keeping only truly universal context in the root file.
B) Delete the deploy-schedule notes, since `CLAUDE.md` should never contain anything outside of code conventions.
C) Move the entire file to `.claude/rules/general.md` with no `paths:` scoping, so it still always loads.
D) Split the file into multiple `CLAUDE.md` files in the project root, since Claude Code merges all root-level `CLAUDE.md` files automatically.

**3. (Task Statement 3.2)** A `resolve` contributor is writing a `/review-tool` slash command that produces a long, exploratory analysis of a tool file before giving a final verdict. They want the exploratory part to stay out of the main conversation, so the team only sees the verdict. Which configuration achieves this?

A) A project-scoped skill in `.claude/skills/` with `context: fork` in its frontmatter.
B) A project-scoped command in `.claude/commands/` with `allowed-tools: []`.
C) A user-scoped command in `~/.claude/commands/`, since personal commands don't post to shared history.
D) A skill with `argument-hint` set, so the exploratory output is treated as a hint rather than main output.

**4. (Task Statement 3.2)** Two `resolve` contributors both want a `/review-tool` command, but one wants it to also check for a company-specific licensing header the other doesn't use. What's the correct way for the second contributor to get their own version without affecting the shared one?

A) Create a personal variant under a different name in `~/.claude/commands/`, leaving the project-scoped `.claude/commands/review-tool.md` untouched for the team.
B) Edit `.claude/commands/review-tool.md` directly and ask teammates not to pull that specific commit.
C) Add an `if` conditional inside the shared command file that checks which contributor is running it.
D) Create a second project-scoped command with the same name in a different subdirectory of `.claude/commands/`.

**5. (Task Statement 3.3)** `resolve`'s test files live in `tests/`, but future modules may add test files colocated next to source files too (e.g. `src/tools/get_customer_test.py`). The team wants one set of testing conventions to apply regardless of where a test file physically lives. What's the most maintainable way to do this?

A) A `.claude/rules/` file with a `paths:` glob matching test-file naming patterns wherever they occur (e.g. `**/*_test.py`, `tests/**/*`), rather than a single directory-scoped rule.
B) A `CLAUDE.md` file placed in both `tests/` and `src/tools/`, each restating the same conventions.
C) A single project-root `CLAUDE.md` section titled "Testing," trusting Claude Code to apply it only when relevant.
D) A `.claude/skills/` skill that a contributor must remember to invoke manually before writing any test.

**6. (Task Statement 3.3)** A `resolve` contributor adds a `.claude/rules/tools.md` file with `paths: ["src/tool/**/*"]` (singular "tool"). The project's real directory is `src/tools/` (plural). What actually happens when they edit `src/tools/get_customer.py`?

A) The rule silently never loads for that file, since the glob doesn't match any real path in the project — Claude Code won't error, it will just behave as if the rule doesn't exist.
B) Claude Code raises a configuration error on startup, refusing to proceed until the typo is fixed.
C) The rule loads anyway, because Claude Code fuzzy-matches glob patterns against real directory names.
D) The rule loads for every file in the project, since an unmatched glob falls back to matching everything.

**7. (Task Statement 3.4)** A `resolve` contributor needs to rename a single internal variable inside `get_customer.py`, with no other changes. What's the appropriate way to approach this in Claude Code?

A) Direct execution — the change is simple, well-scoped, and has no architectural implications.
B) Plan mode, to explore whether the rename affects other files before making it.
C) Plan mode, because any change to a file governed by a `.claude/rules/` file requires a plan first.
D) A dedicated skill, since renames should always be handled by a reusable, invokable command rather than done inline.

**8. (Task Statement 3.4)** A `resolve` contributor is migrating all four MCP tools from raising bare exceptions to returning structured error objects (`errorCategory`, `isRetryable`), a change touching every file in `src/tools/` and the tests that check them. What's the appropriate way to approach this?

A) Plan mode first, to decide the structured-error shape and confirm it's applied consistently before touching every file, then execute the agreed plan.
B) Direct execution, since the change is mechanical (find bare exceptions, wrap them) and doesn't require exploration.
C) Direct execution, but only after writing a `.claude/rules/` file describing the new error shape, since rules substitute for planning.
D) Plan mode is unnecessary here; multi-file changes only need planning if they cross module boundaries, and this change stays within `src/tools/`.

**9. (Task Statement 3.5)** A `resolve` contributor asks Claude Code to "make the error messages more helpful" across all four tools. The first attempt produces inconsistent results: some messages gain detail, others barely change. What's the most effective next step?

A) Provide 2-3 concrete before/after examples of what "more helpful" means for a specific error case, so the instruction stops being interpreted differently per file.
B) Repeat the same instruction a second time, since Claude Code sometimes needs reinforcement to apply an instruction consistently.
C) Switch to a `.claude/rules/` file describing "helpful error messages" in the abstract, since rules are more authoritative than inline instructions.
D) Split the task into four separate sessions, one per tool file, so each gets full attention.

**10. (Task Statement 3.5)** A `resolve` contributor wants Claude Code to add retry logic to `lookup_order`, but is unsure whether transient network failures should retry differently than a "not found" result. What's the most effective way to get a better-considered implementation before code is written?

A) Ask Claude Code to first list the open design questions and confirm the intended behavior for each case, before implementing.
B) Ask Claude Code to implement its best guess immediately, then review the diff for correctness afterward.
C) Write the retry logic manually first, then ask Claude Code to add error handling around it.
D) Skip retries entirely for this module, since retry logic is out of scope until Module 05.

**11. (Task Statement 3.6)** The `resolve` team wants a CI job that runs Claude Code against every pull request to flag MCP tools with missing structured error handling, posting results as a machine-readable summary. Which invocation shape fits a non-interactive CI job?

A) `claude -p "..." --output-format json`, so the process exits without waiting for interactive input and produces output another CI step can parse.
B) `claude "..."`, the default interactive invocation, since CI runners provide a virtual terminal that satisfies interactive prompts automatically.
C) `claude -p "..." --output-format json`, but only after first running `claude` once interactively in the CI job to "warm up" the session.
D) A `.claude/commands/` slash command, since CI-invoked Claude Code can only run project-scoped commands, not raw prompts.

**12. (Task Statement 3.6)** A CI job uses Claude Code to review a pull request that Claude Code itself helped generate in an earlier, separate step of the same pipeline. What's the most important design consideration here?

A) The review step should run as an independent session (not resuming the generation session's context), since a session that retains its own generation reasoning is less likely to question its own prior decisions.
B) The review step should always resume the generation session with `--resume`, so it has full context on why each change was made.
C) No special handling is needed, since Claude Code's review quality doesn't depend on whether it generated the code being reviewed.
D) The review step should be skipped entirely for CI-generated PRs, since self-review is inherently unreliable regardless of session handling.

---

## Answer key

**Do not scroll further until you've answered all 12 questions closed-book and recorded your answers.**

1. **A.** User-level config isn't version-controlled; it never left the original contributor's machine. (B confuses `@import`, a file-referencing mechanism, with "taking effect." C is a false claim — all three hierarchy levels exist. D confuses a diagnostic command with a fix.)
2. **A.** Path-scoped rules and `@import` are the two real mechanisms for keeping `CLAUDE.md` modular without losing content. (B is destructive and assumes a rule that doesn't exist. C removes path-scoping, defeating the purpose. D is a false claim — Claude Code doesn't merge multiple root `CLAUDE.md` files.)
3. **A.** `context: fork` is exactly the frontmatter option that isolates a skill's output from the main conversation. (B's `allowed-tools: []` restricts tool access, not context isolation. C is a real distinction but doesn't solve the stated problem — a user-scoped command isn't about isolating output. D misapplies `argument-hint`, which prompts for parameters, not output routing.)
4. **A.** Personal variants in `~/.claude/commands/` under a different name are exactly the documented mechanism for this. (B is destructive and fragile. C and D both try to force one shared file to serve two purposes, against the grain of the actual feature.)
5. **A.** A glob-pattern rule matching by filename pattern, not directory, is the only option that works "regardless of where a test file physically lives." (B doesn't scale and duplicates content. C relies on inference rather than explicit matching. D requires manual invocation, defeating "automatic wherever it occurs.")
6. **A.** An unmatched glob simply means the rule never loads — silently, with no error. This is the exact failure mode Module 01's own deterministic checker specifically tests for. (B, C, D all describe error-handling or fallback behaviors that don't exist.)
7. **A.** A single-variable rename in one file is exactly the "simple, well-scoped, clear stack trace" shape direct execution is for. (B over-applies plan mode to a trivial change. C is a false claim — rule-governed files don't require planning by default. D misapplies skills to a one-off task.)
8. **A.** Multi-file, architecturally-meaningful changes (a new error shape applied consistently) are exactly what plan mode exists for. (B underestimates the change's real scope. C misunderstands what a rules file does — it states conventions, it doesn't substitute for planning a migration. D's "boundary" heuristic isn't the real criterion; scope and architectural weight are.)
9. **A.** Concrete input/output examples are the documented fix for inconsistent interpretation of a vague instruction. (B assumes repetition fixes ambiguity, which it doesn't. C misapplies a rules file to a one-off vague instruction rather than a standing convention. D avoids the actual problem rather than fixing it.)
10. **A.** Surfacing open design questions before implementation (the "interview pattern") is exactly the fix for genuine ambiguity the contributor hasn't resolved yet. (B skips the ambiguity instead of resolving it. C reverses the actual workflow this module teaches. D avoids the question rather than answering it.)
11. **A.** `-p`/`--print` for non-interactive mode plus `--output-format json` for machine-parseable output is the documented CI-integration shape. (B is false — CI runners do not automatically satisfy interactive prompts; this is the exact hang scenario Task Statement 3.6 warns about. C's "warm up" step doesn't correspond to anything Claude Code actually does. D is a false claim — `-p` accepts a raw prompt directly.)
12. **A.** Independent review sessions catch more because they don't carry the generation session's own reasoning momentum. (B does the opposite of what's needed. C is false — this is a documented, real effect. D is an overcorrection; the fix is session independence, not skipping review.)

---

*Checkpoint authored 2026-07-15, alongside a remediation pass on Module 01's hands-on tier — see `docs/decisions.md`.*
