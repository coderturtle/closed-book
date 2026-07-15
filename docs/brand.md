# Brand / Style Layer: Closed Book

> The only place this workshop's personality lives. `README.md` and, once built, `site/`'s layout and `astro.config.mjs` all read from this file — they don't redefine voice, banned language, or visual identity independently. Adapted from `borrow-native/docs/brand.md`, itself adapted from `terminal-velocity/docs/brand.md` and blog-factory-lab's `templates/brand-style-layer-template.md`.

## Site identity

**Name:** Closed Book
**Tagline:** Build it with Claude. Prove you don't need Claude to pass.
**Parent brand:** Hekton
**Slug:** `closed-book`

The tagline leads with the workshop's actual hook (the learn-with-AI/test-without-AI tension) rather than the mechanism sentence ("gated by closed-book practice checkpoints") — per this workshop's own Workshop Review Panel Developer Evangelist finding (`docs/review-panel/2026-07-14-initial-design.md`), the mechanism sentence reads as a workflow detail, not a provocation, and buries the thing worth sharing.

## Tone and voice

**Core voice:** A competent peer, not an instructor, and not a test-prep hustler. Specific, dryly aware of the irony baked into the workshop's own premise (learn with an agent, prove you don't need it), anti-hype by default. Treats the reader as someone who already ships with Claude Code daily — the only thing assumed unfamiliar is the certification's own blueprint.

**Tone rules:**
- Prefer plain verbs and concrete nouns; show the mechanism (a specific domain, a specific task statement), don't just assert the result.
- Any claim about what the two-tier gate achieves ("prepares you better," "builds real recall") must carry its hedge in the same sentence or the same heading, not paragraphs later — a direct fix for this workshop's own Skeptical Critic findings against the design docs (hedge-placement was flagged and fixed twice in the first Review Panel pass).
- First person for build-log entries. System/instructional language for module content and workshop structure.
- Admit uncertainty directly rather than smoothing over it — especially about whether this workshop's method actually works, which isn't evidenced until the real CCA-F/CCAR-P attempts happen.
- Never imply completing this workshop is the same as earning the credential. Only Anthropic's own proctored exam does that.

## Hard rules

- **No em dash characters.** Use period, colon, semicolon, comma, parenthesis, or a plain hyphen instead. (Applies to all published workshop content: README, module READMEs, build-log entries, the site. Design/planning docs under `docs/` are working documents and are exempt.)
- No AI-slop openers ("In today's fast-paced world...", "It's important to note...").
- No unqualified efficacy superlatives ("game-changing," "guaranteed to pass," "unlock your potential").
- No engagement bait, fake scarcity, or "one weird trick" framing.
- **Certification-specific:** never imply or state that this workshop guarantees passing the real exam, that it is affiliated with or endorsed by Anthropic, or that its closed-book practice questions are drawn from or equivalent to the real exam's actual item bank. Every mention of exam facts (fees, format, domain weights) must be traceable to Anthropic's own published exam guide.

## Banned phrases

Reused from the wider Hekton house style, plus workshop-specific additions:

- delve, tapestry, unlock, seamless, game-changing, revolutionize, transform your workflow, supercharge, effortlessly, cutting-edge, thought leader
- "in today's fast-paced world," "it's important to note," "at scale" (unless the content proves the scale)
- Workshop-specific: "master the art of," "in this comprehensive guide," "guaranteed pass," "official prep course," "get certified fast," "ace the exam" (implies a shortcut this workshop's own design explicitly rejects: the hands-on tier exists because shortcuts don't build real understanding)

## Visual identity

Inherit `borrow-native`'s Astro starter tokens rather than invent a new palette, once the site is built: `--accent`, `ink`/`paper` Tailwind tokens, the `.post-body` typography rhythm, "no section dividers, whitespace only."

| Element | Direction |
|---|---|
| Overall mood | Clean technical workshop notebook, not an exam-prep marketing page. |
| Colour approach | Dark-on-light default; restrained palette; dark mode optional later |
| Typography | Crisp, generous whitespace, readable code blocks |
| Imagery | Artifact-led: real terminal sessions, real closed-book quiz screenshots (blurred/redacted appropriately), diffs — not stock photos, not exam-hall stock imagery |
| Decoration | No neon AI aesthetic, no hero banners, no "pass guaranteed" badges |

## Gremlin and factory language rules

- Coachgremlin and the Workshop Gremlin are real, documented agents with concrete responsibilities (`~/hekton/gremlins/`) — reference them plainly when explaining how the workshop works, don't decorate every heading with gremlin language, and don't assume a learner already knows what a "Gremlin" is without a one-line explanation the first time the term appears in learner-facing copy.
- A module README is a production artifact: plain. A build-log entry can be funny where the actual events were funny.

## Anti-goals

- Not an AI-hype funnel or a marketing page for Hekton.
- **Not a certification itself, and not affiliated with or endorsed by Anthropic.** Completing this workshop credentials nothing on its own; only Anthropic's proctored exam does. Say this plainly wherever the workshop's relationship to the real credential is discussed.
- Not a place to publish unverified efficacy claims about the two-tier gate — every such claim gets the hypothesis treatment above until the real exam attempts happen and get recorded.
- Not overrun with gremlin language to the point of reading childish.
- Not a leaked-question-bank site, ever, under any framing. See `docs/design-tension.md`'s Constraint section for the non-negotiable line on where practice questions come from.

## Application map

| Artifact | Reads |
|---|---|
| `README.md` | Title + tagline |
| `site/` (once built) | Tone, hard rules, banned phrases, visual identity |
| Module READMEs | Tone, hard rules, banned phrases, certification-specific escape-hatch rule |
| Build-log entries | Tone and voice rules (first person, tension, no hype) |

## [TBD]: items for later

- [ ] Exact accent colour token (once site is built)
- [ ] Favicon / wordmark treatment
- [ ] Dark mode colour tokens
