---
name: agentic-learning-discipline
description: Check whether you actually learned this module's concept or your coding agent just demonstrated it for you. Use at the end of any Closed Book module, before the closed-book checkpoint, especially if your agent produced a working configuration/artifact quickly or with no real back-and-forth.
---

# Agentic learning discipline

Not a certification-content skill — a cross-cutting one, referenced from every module rather than owned by any single one. Adapted from Borrow Native's own version of this skill (per Coachgremlin's own Workflow, which calls it a reference implementation, generalizable beyond that one workshop).

Closed Book's version of this tension is sharper than most workshops that use this skill: the real exam this workshop prepares you for explicitly forbids the agent you're using to build the hands-on tier. If you've been delegating understanding to Claude Code during a module's build phase, the closed-book checkpoint immediately after is where that gap becomes visible, not hideable. This skill exists to catch it before the checkpoint does, when there's still time to go back and actually work through the concept.

## The check

Before opening this module's closed-book checkpoint, answer these three questions **without looking at the artifact you just built**:

1. **Name the domain task statement this exercise was actually testing, in your own words, without looking at the code or config.** Not "the checker passed" — the one sentence a reviewer would use to describe what your artifact demonstrates (e.g. "conventions that only apply to `src/tools/` live in a path-scoped rule, not the root CLAUDE.md, because they're not true of the whole project").
2. **Predict whether your artifact would still pass the deterministic checker before rerunning it.** If you can't predict this confidently, you haven't yet internalized what makes the artifact's *shape* correct, only that it happened to work once.
3. **Name the specific way a plausible, honest-but-naive attempt would have gotten this wrong, and why it would look reasonable anyway.** Every module in this workshop has a real, documented one (`runs/*/grading.md`, if you want to check your answer). If you can't name one, you likely haven't engaged with why this module's exercise is hard, only with why your specific attempt passed.

**Three "no"s (or "I'd have to look") is a real signal, not a moral failing.** It means this module's artifact was delegated, not learned — worth a second, slower pass before the closed-book checkpoint, ideally without your agent doing the work this time. This check is intentionally not scored and not something Coachgremlin grades — grading a self-reported "did I really understand this" invites the same problem this skill exists to catch, one level up. It's a tool for your own honesty, not a gate.

## Why this exists, and why it isn't a rubric fix

Named directly in this workshop's own design (`docs/design-tension.md`): the two-tier gate (hands-on artifact, then closed-book checkpoint) is the workshop's structural answer to the learn-with-AI/test-without-AI tension, but it's a *design*, not a guarantee that any given learner actually engaged rather than delegated during the hands-on tier. A closed-book checkpoint you fail because you never really understood the hands-on artifact is doing its job. A closed-book checkpoint you pass by having quietly re-derived the answer from a half-remembered agent conversation is not the same claim as genuine recall — and this skill is the only thing standing between those two outcomes, since nothing mechanical can tell them apart from the outside.

## When to reach for this

At the end of every module's hands-on tier, right before opening the closed-book checkpoint — especially if your agent produced a working artifact quickly, on the first try, or without you needing to explain the concept back to it at any point. Not needed mid-attempt, and not a substitute for actually trying the exercise yourself first; it's a check on what happened after the fact, not a rule about how to work.
