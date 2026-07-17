# foundry

Foundry is an internal AI platform team's own product: the team and tooling that lets other engineering teams adopt Claude Code and the Agent SDK safely and effectively. Foundry designs, integrates, evaluates, governs, and supports Claude-based solutions for many internal teams, each bringing a real business problem.

## The canonical discipline

An internal team shows up with a real problem, and Foundry has to make a real, defensible choice — not the maximal-complexity choice, not whatever the requesting team happened to ask for by name — every time, and be able to explain why to that team's own stakeholders. See `SPEC.md` for the full statement of this principle and the module-by-module build-out.

## Working here

Each module in Part 2 of the Closed Book workshop solves one internal team's stated problem, adding one real capability to this codebase. Read `SPEC.md` before assuming what a prior module's checker guarantees — only what a checker actually verifies is safe to assume, per the compatibility contract.

## CI usage

Run in non-interactive mode for automated checks: `claude -p "Review src/ against SPEC.md's stated conventions" --output-format json`. The `-p`/`--print` flag exits after producing output instead of waiting for interactive input.
