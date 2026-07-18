# Closed Book

Build it with Claude. Prove you don't need Claude to pass.

## What this is

A self-paced workshop that teaches Anthropic's real Claude Certified Architect material (Foundations, then Professional) to people who already drive Claude Code daily. Every module has two parts. First, you **build a real artifact hands-on with Claude Code**: an agentic loop, an MCP tool, a CLAUDE.md hierarchy, a RAG pipeline, whatever that module's exam domain actually asks a practitioner to build. Then you **close the session and take a timed, closed-book practice checkpoint**, no AI, no notes, modeled on the real exam's own blueprint and question style, because that's the one condition under which the real exam actually happens.

The tension is the point. You learn the agent-native way, because that's how this audience already learns everything. You get tested the way the real exam tests: alone, in your head, with nothing but what you actually understand. Building it with Claude doesn't count until you can also defend it without Claude, and that's a bet this workshop is testing, not a proven method: see [`docs/design-tension.md`](docs/design-tension.md) for the honest version of that claim.

**This arc is checked against two real, external exams.** [Claude Certified Architect – Foundations (CCA-F)](https://www.pearsonvue.com/us/en/anthropic.html) and Claude Certified Architect – Professional (CCAR-P) are Anthropic's own proctored, closed-book exams (60 and 63 questions, 720/1000 to pass), real and individually achievable through Pearson VUE. The maintainer intends to sit both personally once this workshop's content exists, as its own dogfooding evidence. **That's a stated intent, not a result:** no exam has been attempted yet, and any claim that this workshop prepares you for it should be read as this workshop's own bet until that attempt happens and gets recorded in the build log.

**This workshop is not affiliated with or endorsed by Anthropic, does not guarantee you'll pass, and completing it does not itself credential anything** — only Anthropic's own proctored exam does that. Its closed-book practice questions are written originally against Anthropic's published exam guides; none are copied from the real exam, any leaked item bank, or Anthropic's own official sample questions.

**Who it's for:** agent-literate practitioners, people comfortable with git, the CLI, and driving Claude Code daily for real work, but new to the *certification's own blueprint* specifically. Not an intro-to-agents workshop (harness fluency is assumed).

## Prerequisites

- Comfortable with git, the CLI, and reading a diff.
- Already using Claude Code regularly, with it installed on your machine.
- Willingness to actually go closed-book for the practice checkpoints. Skipping that tier defeats the entire premise; see below.

## How to start

```bash
git clone git@github.com:coderturtle/closed-book.git
cd closed-book
cat modules/README.md
```

Then work through `modules/` in order. Each module states a hard prerequisite on an earlier one.

> **Current status: all 10 modules are real.** The workshop's full content arc is complete: every module has a working hands-on exercise, a real deterministic checker, a closed-book checkpoint, and a completed multi-attempt dry run (see [`modules/README.md`](modules/README.md) for the module-by-module status). Read `docs/build-log/` for the story of how it got built, or [open an issue](https://github.com/coderturtle/closed-book/issues) to ask.

## How the modules connect

Ten modules in two parts. **Part 1 (Modules 01-06)** builds toward CCA-F: Claude Code configuration, then structured prompting, then tool/MCP design, then the agentic loops and multi-agent orchestration that everything before it was building toward, then context management and reliability, then a capstone that's a real dress rehearsal for the actual exam. **Part 2 (Modules 07-10)** builds toward CCAR-P: solution design and model strategy, then integration and evaluation, then governance and stakeholder delivery, then a second capstone. A learner can stop after Module 06, sit the real CCA-F exam, and treat Part 2 as a separate, later commitment. Full arc, gate tiers, and the exam-guide research behind it: [`modules/README.md`](modules/README.md).

## Every module's checkpoint, going in closed-book

Before you take any module's practice checkpoint: close or minimize your Claude Code session, and use a separate device or a printed copy if you can. Time yourself for real. The value of the checkpoint is entirely in genuinely rehearsing recall without the agent; passing it by keeping Claude open in another tab defeats the workshop's actual thesis, not just the rules. Default format: 10-15 questions, 15-20 minutes, 80% to pass, except the two capstones, which mirror the real exam's exact format.

## What you keep

Every module leaves you with something, not just a passed check: a CLAUDE.md starter kit, a few-shot/JSON-schema template library, a tool-description checklist, a coordinator-subagent reference implementation, a context-degradation diagnostic playbook, a CCA-F exam-day prep sheet, an architecture-decision-record template, an evaluation harness template, a governance checklist, and a CCAR-P exam-day prep sheet. See [`modules/README.md`](modules/README.md#what-you-keep) for the full list.

## Build in public

This workshop's own build is published as a dated journal at [closed-book.coderturtle.io](https://closed-book.coderturtle.io): the maintainer's record of building the workshop, written deliberately rather than auto-generated from session logs.

## Something wrong?

This is early and imperfect by design. If a module reduces to "read this, then move on" instead of a real two-tier gate, or a link here is broken, [open an issue](https://github.com/coderturtle/closed-book/issues).

## Key docs

- [Workshop Design](docs/workshop-design.md): audience, format, two-tier gate teaching method, full module arc
- [Design Tension](docs/design-tension.md): the learn-with-AI/test-without-AI tension, named honestly
- [Maintainers](docs/maintainers.md): internal/agent-facing docs, classification, documentation contract
