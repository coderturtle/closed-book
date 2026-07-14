# The learn-with-AI / test-without-AI tension

**Status:** named design decision (2026-07-14, coderturtle), stated at skeleton stage per this
workshop's own module-README template requirement. Not yet stress-tested against real module
content — that's the Workshop Review Panel's job next, and Coachgremlin's job once content exists.

## The problem, in one line

Closed Book teaches agent-native — every module's core exercise is built *with* Claude Code — but
the real exam it prepares candidates for is proctored, closed-book, and explicitly **prohibits AI
assistance**. The method and the target condition are opposites. A workshop that only ever
practiced with Claude's help would leave a candidate more fluent at the skill and *less* prepared
for the one moment that actually matters: 120 minutes, alone, no agent.

## Where this shows up

Straight from Anthropic's own exam guides (fetched and read in full, not summarized):

> "During the exam you must: ... Keep your workspace clear of notes, books, phones, secondary
> monitors, and other materials ... Refrain from communicating with any other person during the
> exam ... Not capture, copy, photograph, or reproduce any exam content in any form."
> — CCAR-P Exam Guide §12, "Exam-Day Experience and Rules of Conduct"

Every prior workshop this Gremlin has built assumed the learning method and the target skill were
the same thing, or at least compatible (Borrow Native: learn Rust with an agent, the compiler
checks you either way — the compiler doesn't care whether a human or an agent wrote the code).
Closed Book is the first workshop where the *evaluation condition itself* forbids the tool the
whole method is built around.

## Why a quick fix doesn't resolve it

**"Just don't use Claude for the practice quizzes"** is necessary but not sufficient on its own —
it produces closed-book *questions*, but doesn't teach the learner how to *recall* the material
without reflexively reaching for the agent, which is a different, unpracticed skill. A learner who
has only ever had Claude reason through agentic-loop tradeoffs *for* them has no rehearsed memory
of reasoning through it *themselves* — the closed-book checkpoint would be the first time they've
ever tried.

## The two-tier gate is the resolution, not a workaround

Every module's required gate (`docs/workshop-design.md`) has both tiers **by design**, not as a
late patch:

1. **Build it with Claude Code.** This is where real understanding gets constructed — the same
   "harness is the classroom" bet every workshop in this pipeline makes. Skipping this tier and
   going straight to memorization would produce a candidate who can pass a quiz but can't actually
   build the agentic loop, tool interface, or context-management pattern the exam's own scenarios
   describe.
2. **Then defend it closed-book.** Immediately after building, before moving to the next module,
   a short timed multiple-choice checkpoint against that module's own domain — no Claude, no
   notes, same condition as exam day. This is deliberately placed *right after* the hands-on
   exercise, while the reasoning is fresh, rather than batched into a single end-of-arc review —
   the closer the closed-book rehearsal sits to the hands-on construction, the more it's actually
   practicing recall-without-agent rather than testing whether the quiz was memorized separately.

The bet: repeated small closed-book checkpoints, immediately following real hands-on construction,
build the specific muscle the real exam demands — recalling *why* a design choice is correct
without a tool doing the reasoning — better than either an all-agent workshop (never rehearses
the constraint) or an all-quiz workshop (never builds the real understanding the quiz is checking
for). **This is a stated hypothesis, not a proven finding** — same honesty discipline every prior
workshop in this pipeline has applied to its own untested bets.

## Constraint: where the closed-book questions come from

A real risk surfaced during this workshop's own curriculum-anchor research, worth recording here
rather than only in `docs/workshop-design.md`: an early search pass for the exam blueprints
returned several third-party "exam prep" sites presenting **identical domain/weight lists** under
different exam names (a "Developer Foundations" page and an "Architect Foundations" page from two
different SEO sites returned the exact same 5 domains at the exact same percentages) — either
copied content, scraper error, or genuinely coincidental overlap; it wasn't possible to tell from
the secondary sources alone. Fetching Anthropic's own primary-source exam guide PDFs directly
resolved the ambiguity and is what this workshop's module arc is actually anchored to.

The same discipline applies to every closed-book practice question this workshop's modules will
ever contain:

1. **Written originally**, against the exam guide's own published task statements and sample-
   question *style* (scenario framing, one correct answer, three distractors each representing a
   specific plausible wrong reasoning path — not randomly wrong).
2. **Never copied or lightly reworded** from Anthropic's own sample questions, any leaked or
   scraped item bank, or any third-party "practice exam" product — both because Anthropic's exam
   content is explicitly confidential/proprietary under its own Non-Disclosure terms (CCAR-P Exam
   Guide §13) and independent of that, because a workshop that taught the real answer key would be
   teaching memorization, not the skill.
3. **Graded against the guide's own "Knowledge of:" and "Skills in:" bullets**, not against an
   invented rubric — Anthropic already did the job task analysis; this workshop's job is teaching
   toward it, not re-deriving it.

## What this doesn't solve

Named honestly, matching Borrow Native's own rubric-spoiler-tension precedent: this design
doesn't eliminate the possibility that a learner games the closed-book checkpoint by having
already seen (outside this workshop) real exam questions or a leaked item bank — no workshop can
control for that. It also doesn't yet have real evidence that the "immediately-after, small,
repeated" checkpoint cadence actually builds durable no-AI recall better than a single end-of-arc
review would — that's exactly the kind of claim coderturtle's real CCA-F/CCAR-P exam attempts
(`docs/workshop-design.md`'s dogfooding commitment) are meant to test, not something this design
doc can claim as proven before either exam has been sat.
