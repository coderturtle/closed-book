# Module 08 closed-book checkpoint

**Format:** 14 questions, 20 minutes, 80% (12/14, rounded up) to pass. Multiple choice, one correct answer, three distractors.

**Before you start:** close or minimize your Claude Code session. No notes, no AI assistance, no searching. See [`docs/design-tension.md`](../../docs/design-tension.md).

**Citation note:** as with Module 07's checkpoint, CCAR-P's exam guide doesn't enumerate Domain 3/Domain 4 into a granular decimal task-statement scheme in the primary-source material this workshop's design phase actually read — confirmed by search, not assumed (`docs/workshop-design.md` has only the summary-level domain/weight row). Questions are cited by each domain's own named objective instead (e.g., "Domain 3: connection-protocol selection"), grouped from the objectives listed in that same design doc.

**Coverage note:** the hands-on exercise's artifacts (`doc_qa.py`'s `refresh_index` fix, `evaluation.py`'s `evaluate`/`compare_top_k`) directly verify RAG pipeline design, evaluation metric design, A/B testing, and diagnosing a stale-retrieval failure — against exactly one scenario (the Platform Docs team). This checkpoint carries the remaining objectives (connection-protocol selection, auth/security-gap analysis, tool/agent capability-bloat evaluation, accuracy-latency trade-offs, cost/latency optimization, observability at scale), plus re-tests RAG/evaluation-metric judgment against scenarios the hands-on work hasn't already walked you through.

**Originality note:** every question is written originally against the objective it tests — none are copied or reworded from Anthropic's real exam, any leaked item bank, or Anthropic's own official sample questions (the exam guide's own Sample Question 3, about a RAG system returning confident-but-wrong answers after a document refresh, is used only as a style/difficulty anchor for this module's design, per `docs/workshop-design.md` — never copied into a question here).

---

## Scenarios

**Scenario 1 (reused from your hands-on work): the Platform Docs team's documentation Q&A system,** covered in `fixtures/foundry/`.

**Scenario 2: the Payments team** wants to integrate Claude with a third-party fraud-detection API to review flagged transactions, deciding how Claude should actually connect to that external system.

**Scenario 3: the Mobile team** shipped a customer-facing chat feature built on Claude. Two weeks after launch, p95 latency has crept up and a support ticket reports Claude confidently answering a question with information that was true at launch but is now wrong.

---

## Questions

**1. (Domain 3: RAG pipeline design)** For Scenario 1, why does a document's `doc_id` staying the same across a content revision matter specifically for index design, not just for `refresh_index`'s implementation?

A) It doesn't matter — any index design is equally vulnerable to staleness regardless of how it keys documents.
B) An index keyed by `doc_id` needs an explicit signal that content changed (a hash, version, or timestamp) precisely because the key itself gives no such signal — the design must account for "same identity, different content" as a real state, not an edge case to patch in later.
C) `doc_id` staleness is a Domain 5 (governance) concern, not a RAG pipeline design concern at all.
D) The fix is to make every document's `doc_id` change whenever its content changes, eliminating the need for any staleness-detection logic.

**2. (Domain 3: RAG pipeline design)** A contributor proposes fixing Scenario 1's staleness bug by rebuilding the entire index from scratch on every single query, instead of incrementally refreshing only changed documents. What's the real cost of that design choice at Foundry's actual scale (thousands of docs, frequent queries)?

A) There is no real cost; rebuilding on every query is always the safest and cheapest option.
B) It trades a real, recurring computational cost (re-chunking and re-hashing the entire corpus on every single query) for a staleness guarantee that incremental refresh-with-correct-change-detection already provides at a fraction of the cost — the "always rebuild everything" fix oversolves the problem it's responding to.
C) The only cost is a one-time cost paid the first time the index is ever built, with no ongoing cost afterward.
D) Rebuilding on every query is cheaper than incremental refresh in every case, regardless of corpus size or query volume.

**3. (Domain 3: connection-protocol selection)** For Scenario 2, what's the most important factor in choosing how Claude connects to the fraud-detection API?

A) Always prefer the newest available connection technology, regardless of what the fraud-detection API actually supports or requires.
B) Whether the integration needs are met by a direct API/CLI call, an MCP server exposing the API as a structured tool, or a full agent-to-agent handoff — driven by the API's own real shape (auth model, rate limits, whether Claude needs multi-step tool use against it or a single request/response) rather than defaulting to whichever pattern was used last.
C) The choice should be made by the fraud-detection API vendor, not by Foundry.
D) Connection-protocol selection has no real trade-offs; every mechanism is functionally interchangeable for any integration.

**4. (Domain 3: connection-protocol selection)** The Payments team argues Scenario 2 should use the same MCP-server pattern `resolve`'s own tools used in Part 1, "since it worked well there." What's the flaw in that reasoning, applied here specifically?

A) There's no flaw — proven patterns should always be reused regardless of the new integration's actual shape.
B) `resolve`'s tools were internal functions Foundry itself controlled and could scope with least-privilege design from the start; a third-party fraud-detection API has its own external auth model, rate limits, and failure modes Foundry doesn't control — the pattern's mechanics may still fit, but the trust and scoping analysis has to be redone, not assumed to carry over.
C) MCP servers can only ever wrap internal tools, never third-party APIs, so the proposal is technically impossible.
D) The flaw is that Part 1's tools were too capable, and Scenario 2 requires a strictly less capable integration mechanism than MCP allows.

**5. (Domain 3: auth/security-gap analysis)** For Scenario 2, what's a real auth/security gap to check before connecting Claude to the fraud-detection API, beyond "does the connection work"?

A) None — if the API call succeeds and returns fraud data, the integration is secure by definition.
B) Whether the credentials Claude's tool call uses are scoped to only what this specific integration needs (read-only flagged-transaction lookup, say) rather than a broad, shared API key that would let a compromised or misbehaving tool call do far more than the fraud-review task requires — the same least-privilege discipline the exam guide's own Sample Question 1 anchors.
C) Security is only a concern if the fraud-detection API is free; paid APIs are inherently secure.
D) Auth scope only matters for internal tools, never for third-party API integrations.

**6. (Domain 3: auth/security-gap analysis)** A contributor argues Scenario 2's integration is safe because "Claude only reads flagged transactions, it never writes anything." Why is read-only access alone not a complete security analysis?

A) It is complete — read-only access can never expose sensitive information or create risk.
B) Read-only access to sensitive data (transaction details, customer information) still carries real exposure risk (data leaving its intended boundary, appearing in logs or model context beyond where it should) even without any write capability — "read-only" bounds one risk dimension, not all of them.
C) Read-only access is actually more dangerous than write access in every case.
D) This concern only applies to write access, so read-only integrations never need any security review at all.

**7. (Domain 3: tool/agent capability-bloat evaluation)** For Scenario 2, a contributor proposes giving Claude one broad `call_fraud_api` tool that can hit any endpoint on the fraud-detection API, "so we don't have to build a new tool every time we need a new endpoint." What's the concern, consistent with Module 03's own tool-scoping discipline?

A) There's no concern; a single flexible tool is always simpler and therefore always better than several narrow ones.
B) A broad, do-anything tool is harder to reason about, test, and scope permissions for than several narrow, purpose-built tools — the same capability-bloat risk Module 03's tool-design discipline already established, here at the integration layer instead of within a single codebase.
C) The concern only applies if the fraud-detection API has more than ten endpoints.
D) Tool capability has no bearing on security or reasoning difficulty, only on developer convenience.

**8. (Domain 3: tool/agent capability-bloat evaluation)** What's a concrete signal that a Claude-based integration has drifted into capability bloat?

A) The integration uses more than one tool, regardless of what each tool actually does.
B) A single tool's description has grown to cover several unrelated actions (e.g., "look up a transaction OR flag it OR reverse it OR update the customer's risk score") because each new need was bolted onto the existing tool rather than given its own scoped one.
C) The integration has been in production for more than six months.
D) The tool's docstring is longer than one paragraph.

**9. (Domain 4: evaluation metric design)** Scenario 1's `evaluate` function scores a case correct only if the model's answer cites the *specific* expected document, not just any document. Why does this precision matter more than a metric that just checks "did it cite something"?

A) It doesn't matter; any citation at all is sufficient evidence the system is grounded correctly.
B) A metric that accepts any citation would silently pass a system that's confidently grounding answers in the *wrong* document — exactly the kind of failure a real evaluation harness exists to catch, not average away.
C) Citation specificity is a Domain 3 concern, not a Domain 4 evaluation-metric concern.
D) The looser metric is actually more informative because it produces a higher accuracy number.

**10. (Domain 4: evaluation metric design)** For Scenario 3, the Mobile team's only current metric is "% of user messages that got a response" (as opposed to an error). Why is this an incomplete evaluation metric for the actual problem described (confidently answering with outdated information)?

A) It's a complete metric; a response either happens or it doesn't, and that's the only thing worth measuring.
B) It measures whether the system produced *a* response at all, but says nothing about whether that response was *correct* — the reported symptom (confidently wrong, not-a-crash) is invisible to a metric that only tracks response-vs-error.
C) Response-rate metrics are only useful for RAG systems, never for any other kind of Claude-based system.
D) The metric should be removed entirely rather than supplemented, since it provides no value whatsoever.

**11. (Domain 4: A/B testing)** Scenario 1's `compare_top_k` runs the same evaluation dataset against two different `top_k` values. Why is running the *same* dataset against both configurations essential to a valid A/B comparison here, rather than evaluating each configuration against a different sample of queries?

A) It isn't essential; any two samples of similar size produce an equally valid comparison.
B) Holding the dataset constant isolates `top_k` as the only variable that changed between the two runs — if the query sets differed too, a lower accuracy under one configuration could just as easily reflect a harder query mix as a worse `top_k` choice, and the comparison would no longer isolate what it claims to.
C) The dataset must change between runs, or the comparison is invalid by definition.
D) A/B testing only requires that the two configurations use different model tiers, not that anything else be held constant.

**12. (Domain 4: accuracy-latency trade-offs)** For Scenario 3, if raising the retrieved-context size (more chunks, larger `top_k`-equivalent) measurably improves answer accuracy but also increases p95 latency further, what does a sound accuracy-latency trade-off analysis require before shipping that change?

A) Always ship the accuracy improvement immediately; latency is a secondary concern that can be addressed later, if at all.
B) A stated, real threshold for what latency increase is acceptable for the Mobile team's actual product (a customer-facing chat feature already reporting elevated p95), weighed against the actual size of the accuracy gain — not treating either metric as automatically dominant over the other.
C) Never ship an accuracy improvement that has any latency cost whatsoever, regardless of the product's actual latency budget.
D) Accuracy and latency are unrelated metrics that never need to be considered together.

**13. (Domain 4: cost/latency optimization)** For Scenario 3, the Mobile team's rising p95 latency is traced to the system re-fetching and re-scoring the entire document corpus on every single user message, even when the corpus hasn't changed since the last request. What's the most direct cost/latency optimization here, consistent with Domain 3's own RAG pipeline design principles?

A) Switch to a larger, more capable model tier — a bigger model doesn't address a per-request corpus-rescoring cost, so this wouldn't fix the actual bottleneck.
B) Cache or persist the index across requests, only refreshing it when the underlying documents actually change (the same incremental-refresh discipline Scenario 1's own `refresh_index` exists to get right) — rather than paying the full re-scoring cost on every request regardless of whether anything changed.
C) Reduce the number of user messages the Mobile team's product accepts per day, to lower total load.
D) Latency has no relationship to how often the index is rebuilt; the fix must be elsewhere entirely.

**14. (Domain 4: diagnosing system issues)** For Scenario 3, given the two reported symptoms (rising p95 latency AND confidently wrong answers to a question whose real answer changed since launch), what's the most likely single root cause tying both together, versus treating them as two unrelated problems?

A) They must be unrelated issues with unrelated causes, since one is a performance symptom and the other is a correctness symptom.
B) A stale, never-refreshed index that keeps growing or re-scoring against outdated content can plausibly produce both symptoms at once — wrong answers from outdated content, and rising latency if the system is redundantly reprocessing an ever-growing, never-pruned index — worth checking as a single shared cause before assuming two separate investigations are needed.
C) The only possible cause is the model itself has degraded over time, unrelated to anything in the system's own design.
D) Latency and correctness issues can never share a root cause in a RAG system, by definition.

---

## Answer key

**Do not scroll further until you've answered all 14 questions closed-book and recorded your answers.**

1. **B.** An index keyed by `doc_id` needs its own explicit change signal, since identity alone can't distinguish "same doc, new content" from "same doc, unchanged." (A and C both deny this is a real design concern. D proposes an unworkable, over-engineered non-fix.)
2. **B.** Full-rebuild-on-every-query trades a real, ongoing cost for a guarantee incremental refresh already provides more cheaply. (A and D both ignore the real, recurring cost. C wrongly claims the cost is one-time.)
3. **B.** The connection mechanism should be driven by the external system's own real shape and needs, not habit. (A and D both substitute a rule-of-thumb for actual analysis. C offloads Foundry's own design responsibility.)
4. **B.** A pattern's mechanics may transfer, but the trust/scoping analysis for an external, un-controlled system must be redone. (A treats pattern reuse as unconditionally safe. C is factually wrong — MCP can wrap external APIs. D misstates the actual concern.)
5. **B.** Least-privilege credential scoping is a real, necessary check beyond "does it work" — the same principle the exam guide's own Sample Question 1 anchors. (A and C both treat successful function as sufficient for security. D draws an arbitrary, unjustified distinction.)
6. **B.** Read-only access still carries real exposure risk around where sensitive data ends up, a different risk dimension than write access. (A and C both overstate or misstate the actual risk profile. D dismisses a real, distinct risk class.)
7. **B.** A broad, do-everything tool carries the same capability-bloat risk Module 03 established, now at the integration layer. (A asserts broader scope is strictly better, the opposite of the documented risk. C invents an arbitrary threshold. D denies any connection between capability and reasoning difficulty.)
8. **B.** A tool whose description has accumulated several unrelated actions is a concrete, recognizable bloat signal. (A, C, and D each substitute an irrelevant or arbitrary proxy for the real signal.)
9. **B.** A metric accepting any citation would miss a system confidently grounding answers in the wrong document — exactly the failure a real metric should catch. (A and D both treat the looser, less informative metric as acceptable or even preferable. C misassigns the concern to the wrong domain.)
10. **B.** A response-rate metric can't distinguish a correct response from a confidently wrong one, which is precisely the reported symptom. (A and C both overstate the existing metric's completeness or scope. D discards a metric that still has some value instead of supplementing it.)
11. **B.** Holding the dataset constant isolates `top_k` as the only variable, which is what makes the comparison valid. (A and C both deny or invert this core A/B testing principle. D introduces an unrelated, incorrect requirement.)
12. **B.** A sound trade-off analysis weighs a real latency threshold against the actual size of the accuracy gain, given the product's own already-elevated latency. (A and C each treat one metric as automatically dominant, the opposite of a real trade-off analysis. D denies any relationship between the two metrics.)
13. **B.** Caching/persisting the index and refreshing only on real change directly addresses the redundant per-request cost, mirroring Scenario 1's own incremental-refresh discipline. (A misdiagnoses the bottleneck as a model-capability problem. C addresses symptoms rather than the cause. D denies a real, direct relationship between index-rebuild frequency and latency.)
14. **B.** A stale, ever-growing, never-refreshed index is a plausible single cause behind both a correctness symptom and a performance symptom, worth checking before assuming two separate root causes. (A and D both assume the two symptoms must be unrelated without checking. C jumps to an unsupported, unrelated explanation.)

---

*Checkpoint authored 2026-07-17, alongside Module 08's hands-on tier, both built together from the start.*
