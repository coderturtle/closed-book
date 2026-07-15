# Module 02 closed-book checkpoint

**Format:** 12 questions, 15 minutes, 80% (10/12) to pass. Multiple choice, one correct answer, three distractors.

**Before you start:** close or minimize your Claude Code session. No notes, no AI assistance, no searching. See [`docs/design-tension.md`](../../docs/design-tension.md).

**Coverage note:** this checkpoint carries full coverage of CCA-F Domain 4's Task Statements 4.1–4.6. The hands-on exercise's test suite verifies 4.3 (structured output/schema enforcement) and 4.4 (validation-retry) directly, since those produce checkable behavior; 4.1 (explicit criteria), 4.2 (few-shot), 4.5 (batch processing), and 4.6 (multi-instance review) are architectural/prompt-design judgment calls with no artifact the test suite can inspect, so they're tested here instead. Two questions per task statement, in order.

**Originality note:** every question is written originally against the published task statement it tests — none are copied or reworded from Anthropic's real exam, any leaked item bank, or Anthropic's own official sample questions.

---

## Questions

**1. (Task Statement 4.1)** A `resolve` contributor's first prompt for the extraction tool tells the model to "only extract the refund amount if you're confident about it." In practice, the model applies this inconsistently — sometimes extracting a clearly-stated amount, sometimes not. What's the most effective fix?

A) Replace the vague confidence instruction with an explicit, checkable rule: "extract `refund_amount_cents` only when a specific dollar figure is stated in the message; otherwise return `null`."
B) Add the word "please" and rephrase the instruction more politely, since the model may be interpreting the tone as a soft suggestion.
C) Lower the model's temperature setting, since confidence issues are a randomness problem.
D) Instruct the model to always extract an amount, then flag low-confidence extractions separately.

**2. (Task Statement 4.1)** `resolve`'s extraction tool occasionally miscategorizes a `late_delivery` complaint as `other`, frustrating the team building the routing logic downstream. What's the most direct way to reduce this specific false-positive rate without affecting the tool's other categories?

A) Write an explicit, specific criterion for what counts as `late_delivery` (e.g. "the message states or implies the order has not arrived by an expected or promised date"), rather than relying on the category name alone to convey the distinction.
B) Remove the `other` category entirely, forcing the model to always pick one of the four specific categories.
C) Instruct the model to "be more careful" when a message could plausibly be about a late order.
D) Increase `max_retries` so the model gets more chances to reconsider its categorization.

**3. (Task Statement 4.2)** The extraction tool consistently mishandles messages where a customer states a refund reason without naming a category explicitly (e.g. "this isn't what I ordered" — which should map to `wrong_item`). Plain instructions describing each category haven't fixed this. What's the most effective next step?

A) Add 2-4 few-shot examples showing exactly this kind of implicit-category message mapped to the correct category, demonstrating the reasoning rather than just stating a rule.
B) Rewrite the category names to be more descriptive, e.g. renaming `wrong_item` to `received_incorrect_item_not_as_ordered`.
C) Split `wrong_item` into two narrower categories to reduce ambiguity.
D) Add a `confidence: "low"` default whenever the message doesn't state a category explicitly.

**4. (Task Statement 4.2)** A `resolve` contributor's few-shot examples for the extraction tool are all clean, textbook-clear messages ("My lamp arrived broken, please refund $45.99"). The tool performs well on messages like these but poorly on messages with multiple issues bundled together, or genuinely ambiguous phrasing. What does this suggest about the few-shot set?

A) The examples don't demonstrate the actually-hard, ambiguous cases — few-shot examples are most valuable for showing how to handle exactly the situations that are hard to describe in a general rule, not the situations that are already easy.
B) There are too few examples; simply adding more clean examples of the same shape should improve ambiguous-case handling too.
C) Few-shot examples are the wrong technique here; only explicit criteria (Task Statement 4.1) can handle ambiguity.
D) The examples should be removed, since they may be teaching the model to expect only clean messages.

**5. (Task Statement 4.3)** A `resolve` contributor is deciding how to guarantee the extraction tool's output is always valid, parseable JSON matching the expected schema, even under model variance. Which approach provides that guarantee most reliably?

A) Use `tool_use` with a JSON schema as the extraction mechanism — the model's structured tool-call output is constrained to the schema, eliminating JSON syntax errors as a category.
B) Ask the model in the system prompt to "always respond with valid JSON only, no other text."
C) Post-process the model's free-text response with a regular expression to extract JSON-looking substrings.
D) Lower the model's temperature to reduce output variance in formatting.

**6. (Task Statement 4.3)** The extraction schema defines `refund_amount_cents` as a required integer field. On messages that never mention a dollar amount, the model is forced to invent a plausible-sounding number to satisfy the schema. What's the correct schema-design fix?

A) Make `refund_amount_cents` a nullable field, so the model can honestly represent "not stated in the message" instead of being forced to fabricate a value to satisfy a required field.
B) Change the field's type from integer to string, so the model can write "unknown" instead of a number.
C) Remove the field from the schema entirely, since it can't always be extracted reliably.
D) Add a second field, `amount_is_guessed: bool`, so fabricated values can at least be flagged after the fact.

**7. (Task Statement 4.4)** The extraction tool's first attempt at a message returns a `reason_category` value that isn't one of the five valid categories. The retry logic re-sends the same message with no additional context. What's missing from this retry design?

A) The specific validation error (which field failed, and why) should be appended to the retry request, so the model can correct the actual mistake rather than guessing what went wrong from an identical prompt.
B) Nothing — retrying with the identical prompt is sufficient, since the model's response is non-deterministic and a second attempt is likely to differ anyway.
C) The retry should lower `max_retries` to 0, since a first-attempt failure indicates the schema itself is wrong.
D) The retry should switch to a different, larger model, since retries exist specifically to escalate to more capable models.

**8. (Task Statement 4.4)** A customer's message is genuinely garbled and contains no interpretable refund information at all. The extraction tool retries three times, and every attempt fails schema validation for the same underlying reason. What should happen?

A) The function should raise a clear failure after `max_retries` is exhausted, rather than retrying indefinitely or returning a fabricated best-effort result — retries are ineffective when the required information is simply absent from the source, not just malformed.
B) `max_retries` should be increased until the model eventually produces something schema-valid, since persistence is the correct response to any validation failure.
C) The function should return a default `ExtractionResult` with all fields set to placeholder values, so downstream code never has to handle a failure case.
D) The message should be silently dropped from processing with no error raised, since a garbled message is not `resolve`'s fault.

**9. (Task Statement 4.5)** `resolve`'s team wants to run the extraction tool overnight against a backlog of 10,000 archived support messages to build a historical reasons-for-refund report. Which API approach fits this workload?

A) The Message Batches API — a non-blocking, latency-tolerant workload (an overnight report) is exactly what it's designed for, at roughly half the per-request cost of the synchronous API.
B) The synchronous API, run in a tight loop, since 10,000 requests will complete quickly enough not to matter.
C) The Message Batches API is inappropriate here because extraction requires the retry loop's multi-turn tool calling, which the Batch API doesn't support within a single request — a real, correct constraint, but not one that rules out batch processing for messages that succeed on the first attempt.
D) Neither API is appropriate; this workload should use a fine-tuned model instead.

**10. (Task Statement 4.5)** Of the 10,000 archived messages submitted as a single batch overnight, 200 come back as failures (malformed input on `resolve`'s side, not model errors). What's the correct way to handle this?

A) Resubmit only the 200 failed messages, identified by their `custom_id`, after fixing whatever caused the malformed input — not the full 10,000 again.
B) Resubmit the entire batch of 10,000 from scratch, since partial resubmission risks losing track of which messages were already processed successfully.
C) Treat the 200 failures as acceptable loss and exclude them from the report permanently.
D) Switch the 200 failed messages to the synchronous API only, and leave the successful 9,800 as they are, then merge the two result sets by array position.

**11. (Task Statement 4.6)** A `resolve` contributor wants to double-check the extraction tool's outputs on a sample of real messages before trusting it in production. They consider reviewing each extraction within the same conversation that produced it, right after the original call. What's the concern with that approach?

A) A review conducted within the same conversation carries forward the reasoning context that produced the original extraction, making it less likely to question that extraction's own prior decision than an independent request with no prior context would be.
B) There's no meaningful concern — same-conversation review and an independent fresh request produce statistically identical error-catching rates.
C) Same-conversation review is strictly better, since it already has full context on the message and doesn't need it re-explained.
D) The concern only applies to code review, not structured-data extraction, since extraction has no "reasoning" to be biased by.

**12. (Task Statement 4.6)** `resolve`'s team wants to audit extraction accuracy across all 10,000 archived messages from the batch run, but a single review pass produces inconsistent depth: detailed scrutiny on the first few hundred, increasingly superficial checks toward the end. What's the most effective restructuring?

A) Split the audit into multiple focused passes over smaller batches, rather than one continuous pass over the full 10,000 — this is the same attention-dilution problem large multi-file code reviews have, and the same fix applies.
B) Reduce the sample size to 100 messages and treat that as representative of the full 10,000.
C) Run the same single continuous pass twice and average the two sets of findings.
D) Skip auditing entirely for extractions where the tool itself reported `"confidence": "high"`, since high-confidence outputs don't need review.

---

## Answer key

**Do not scroll further until you've answered all 12 questions closed-book and recorded your answers.**

1. **A.** Explicit, checkable criteria are the documented fix for vague instructions producing inconsistent results. (B is not a real mechanism. C misdiagnoses a precision problem as a randomness problem. D adds a workaround instead of fixing the actual instruction.)
2. **A.** A specific criterion distinguishing the target category is the direct fix; vague category names alone don't convey the distinction reliably. (B is destructive and doesn't fix the root cause. C is the same vague-instruction failure mode the question describes. D conflates a retry mechanism with a precision fix — they solve different problems.)
3. **A.** Few-shot examples demonstrating the specific implicit-mapping pattern are exactly the fix for this ambiguous-case failure mode. (B doesn't address the underlying pattern-matching gap. C over-corrects by adding schema complexity. D masks the problem with a confidence flag instead of fixing the categorization.)
4. **A.** Few-shot examples are most valuable exactly where a general rule struggles — ambiguous, hard-to-describe cases — and a set of only clean examples doesn't teach that. (B misunderstands why few-shot works; more of the same shape doesn't add new signal. C is false — few-shot and explicit criteria are complementary, not substitutes. D throws away a working technique rather than fixing its composition.)
5. **A.** `tool_use` with a JSON schema is the right mechanism, and the most reliable approach available for schema-compliant structured output — this is the exam guide's own framing. Worth being precise beyond the exam guide's shorthand, though: the hard guarantee that a response's shape strictly matches the schema comes specifically from setting `strict: true` on the tool definition; `tool_use` without it is still far more reliable than free-text parsing, but "constrains the output format" is closer to "strongly biases" than "mechanically guarantees" unless strict mode is on. (B relies on probabilistic instruction-following, which is unreliable by construction. C is a fragile workaround for a problem `tool_use` solves directly. D reduces variance but doesn't guarantee schema compliance.)
6. **A.** A nullable field lets the model honestly represent absence instead of being forced to fabricate a value to satisfy a required field — exactly the fabrication-prevention principle this module's own test suite (`test_no_amount_mentioned_is_none_not_fabricated`) checks. (B changes the type without addressing the forced-fabrication problem. C removes useful information entirely. D adds a workaround rather than fixing the schema.)
7. **A.** Specific validation-error feedback in the retry request is what lets the model actually correct the mistake, rather than guess blindly. (B ignores that retrying identically doesn't reliably fix a structural misunderstanding. C reverses the correct response to a first-attempt failure. D misunderstands what retries are for — they're not primarily a model-upgrade mechanism.)
8. **A.** Raising a clear failure after retries are exhausted, rather than looping forever or fabricating a result, is the correct response when the underlying information is genuinely absent, not just malformed. (B assumes persistence fixes a problem that isn't about persistence. C silently discards a real result and hides the failure from downstream code. D silently drops data with no visibility into what happened.)
9. **A.** An overnight backlog report is exactly the latency-tolerant, non-blocking shape the Batch API is designed for. (B works but ignores the real cost savings available for a workload with no latency requirement. C correctly identifies a real Batch API limitation but draws the wrong conclusion from it — the retry loop's *first* attempt at each message can still go through the batch; only cross-request retries would need separate handling. D is an over-engineered, unnecessary escalation.)
10. **A.** Resubmitting only the failed subset, tracked by `custom_id`, is the documented way to handle partial batch failures without redoing successful work. (B wastes the 9,800 successful results unnecessarily. C silently degrades the report's completeness without addressing the fixable cause. D risks misaligning results if `custom_id` correlation isn't used, exactly the failure mode `custom_id` exists to prevent.)
11. **A.** A review conducted within the same conversation retains reasoning momentum from that generation, making it structurally less likely to catch a mistake than an independent request with no prior context would. (B is false — this is a well-documented, real effect. C reverses the actual finding. D incorrectly scopes the concern to code review only; it applies to any generation-then-self-review pattern.)
12. **A.** Splitting into smaller, focused passes is the documented fix for attention dilution across a large review workload — the same problem and the same fix as large multi-file code reviews. (B discards most of the audit's coverage. C doesn't address the underlying attention-dilution cause, just repeats it. D skips exactly the cases most likely to need checking, since high self-reported confidence is not the same claim as high actual accuracy.)

---

*Checkpoint authored 2026-07-15, alongside Module 02's hands-on tier, both built together this time per the explicit lesson from Module 01's remediation.*
