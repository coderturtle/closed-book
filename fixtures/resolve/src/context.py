"""Case-fact persistence and escalation decisions. Authored for real in
Module 05 (Context and Reliability at Scale) -- CCA-F Domain 5, Task
Statements 5.1 (conversation context preservation), 5.2 (escalation/
ambiguity resolution), 5.5 (human review/confidence calibration), and 5.6
(provenance/multi-source synthesis).

The problem this module exists for: a long support session accumulates
facts (which customer, which order, how much to refund) inside a growing,
unstructured conversation history. Nothing about Module 04's loop keeps
those facts from decaying -- a fact established at turn 2 is just one more
message buried under fifteen more by turn 17, indistinguishable to a
naive re-read from something the model half-remembers or paraphrases
wrong. This module's fix is a *persistent, structured* case-facts record,
updated from tool results as the session progresses, so a fact's presence
doesn't depend on the model successfully re-deriving it from raw history
every turn.

This is a *reliability* layer on top of Module 04's *safety* layer, not a
replacement for it -- deliberately separate concerns, not accidental
duplication: Module 04's `SessionState.verified_customer_id` exists so
`verify_before_refund_hook` can make a real-time authorization decision
(last-verified-wins is correct there -- a session enforces one active
verified customer at a time). This module's `CaseFacts` exists so a human
reviewing the case afterward -- or an escalation decision made *during*
the case -- has an accurate, sourced record of what happened, including
when two tool results disagreed. Overwriting silently would be exactly
wrong here, even though it's exactly right in Module 04's hook.

Requires Python 3.9+ (see fixtures/resolve/src/extraction.py's note on why).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CaseFact:
    """One fact, with its provenance. `source_tool` is which tool call
    established this value -- not just "we know this," but "here's how we
    know it," so a human reviewing the case later isn't asked to trust an
    unsourced claim."""

    value: object
    source_tool: str


@dataclass
class CaseFacts:
    """The persistent record for one support session. Deliberately not the
    conversation history itself -- a structured projection of it, so a fact's
    presence doesn't depend on successfully re-deriving it from a growing
    transcript every turn (Task Statement 5.1).

    `conflicts` -- facts where two different tool results disagreed on the
    same field. Task Statement 5.6's own "conflicting-source annotation"
    requirement: a conflict must be recorded, not silently resolved by
    whichever result happened to arrive second. Each entry is
    `(field_name, CaseFact_that_lost, CaseFact_that_won)` -- both sourced,
    so a human can judge which one was actually right.
    """

    customer_id: Optional[CaseFact] = None
    order_id: Optional[CaseFact] = None
    refund_amount_cents: Optional[CaseFact] = None
    error_count: int = 0
    conflicts: list = field(default_factory=list)


# Fields update_case_facts knows how to extract from a tool result, keyed by
# the tool name that can establish them and the result key that carries the
# value. Not every tool result updates every field -- get_customer never
# reports an order_id, lookup_order never reports a customer_id it didn't
# already receive as an argument, and so on.
FACT_SOURCES = {
    "get_customer": {"customer_id": "customer_id"},
    "lookup_order": {"order_id": "order_id"},
    "process_refund": {"refund_amount_cents": "refunded_cents"},
}


def update_case_facts(case_facts: CaseFacts, tool_name: str, tool_args: dict, tool_result: dict) -> CaseFacts:
    """Fold one tool call's result into the persistent case-facts record.

    A tool result carrying `{"error": True, ...}` must increment
    `error_count` and update nothing else -- a failed call establishes no
    fact (the same "success, not attempt, is what counts" discipline
    Module 04's `verified_customer_id` already applies, here extended to
    every fact this module tracks, not just customer verification).

    A successful result updates each field `FACT_SOURCES[tool_name]` maps
    for that tool, reading the value from `tool_result` (never from
    `tool_args` -- the actual result is what's trustworthy, not what was
    asked for; this is the same request-vs-result distinction Module 04's
    own doubt-driven-development review had to add a test for). This
    applies to *every* mapped field alike, not just the one the provided
    test suite happens to exercise most thoroughly -- `get_customer`'s
    `customer_id`, `lookup_order`'s `order_id`, and `process_refund`'s
    `refund_amount_cents` are all equally request-vs-result-sensitive; a
    real backend can return a *different* order or a *capped* refund
    amount than what was asked for, for any of the three. If a field
    already has a *different* recorded value, this is a conflict (Task
    Statement 5.6): append `(field_name, old_fact, new_fact)` to
    `case_facts.conflicts`, and keep the *new* value as the field's current
    value (most-recent-wins for the active value, but the disagreement
    itself must survive in `conflicts`, not vanish) -- surfacing the
    disagreement is the point; silently keeping only the old value would
    hide a real signal just as much as silently keeping only the new one
    would.

    Must not mutate the `case_facts` argument in place -- including its
    *nested* mutable state. `conflicts` is a list; a shallow copy that
    reuses the original's list object still mutates the caller's `CaseFacts`
    the moment a conflict is appended, even though every scalar field looks
    untouched. Return a new `CaseFacts` (and a new, independent `conflicts`
    list) reflecting the update, leaving the caller's original -- every
    field, including its nested list -- untouched. This applies on the
    error path too: a failed call must not mutate the original object's
    `error_count`, `conflicts`, or any already-recorded fact either.
    """
    raise NotImplementedError("Module 05's exercise: implement case-fact extraction and conflict detection.")


def should_escalate(case_facts: CaseFacts, iterations_used: int, max_iterations: int) -> Optional[str]:
    """Decide whether this session should escalate to a human right now.
    Returns a specific, human-readable reason string if it should, or None
    if the session should continue normally.

    Task Statement 5.5's own core lesson: escalation criteria must be based
    on *structured signals this function can actually see* -- unresolved
    conflicts in `case_facts.conflicts`, a real error-rate threshold, or
    the loop running out of room -- never on a model's own self-reported
    confidence or sentiment, which this function has no access to in the
    first place (by design: `case_facts` and the two int arguments are the
    *entire* signature -- not a `model_confidence` or similarly-purposed
    parameter someone could wire up later. Do not add one, even as an
    unused or defaulted-to-`None` parameter; the guarantee this function
    makes is about what it *can* see, and an unused parameter that could
    be populated later is a structural door left open, not a closed one).

    Exactly the three conditions below, and no others -- do not add a
    fourth trigger from any other field or piece of state, even one that
    seems reasonable. Check them in order (return on the first that
    applies):
    1. `case_facts.conflicts` is non-empty -- an unresolved factual
       conflict is exactly the kind of ambiguity a human should resolve,
       not the loop guessing which source was right.
    2. `case_facts.error_count >= 3` -- three failed tool calls in one
       session is a real reliability signal, not a fluke worth one more
       silent retry. Below 3, do not escalate on error count alone.
    3. `iterations_used >= max_iterations - 1` -- escalate *before*
       `run_support_session`'s own `max_iterations` backstop fires, so the
       session ends with a human handoff instead of Module 04's own
       generic `"max_iterations"` failure state. Strictly below that
       boundary, do not escalate on iteration count alone.
    If none apply, return None.
    """
    raise NotImplementedError("Module 05's exercise: implement the escalation decision.")
