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

import copy
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CaseFact:
    """One fact, with its provenance."""

    value: object
    source_tool: str


@dataclass
class CaseFacts:
    """The persistent record for one support session."""

    customer_id: Optional[CaseFact] = None
    order_id: Optional[CaseFact] = None
    refund_amount_cents: Optional[CaseFact] = None
    error_count: int = 0
    conflicts: list = field(default_factory=list)


FACT_SOURCES = {
    "get_customer": {"customer_id": "customer_id"},
    "lookup_order": {"order_id": "order_id"},
    "process_refund": {"refund_amount_cents": "refunded_cents"},
}


def update_case_facts(case_facts: CaseFacts, tool_name: str, tool_args: dict, tool_result: dict) -> CaseFacts:
    """Fold one tool call's result into the persistent case-facts record."""
    new_facts = copy.deepcopy(case_facts)

    if tool_result.get("error"):
        new_facts.error_count += 1
        return new_facts

    field_map = FACT_SOURCES.get(tool_name)
    if not field_map:
        return new_facts

    for field_name, result_key in field_map.items():
        if result_key not in tool_result:
            continue
        new_value = tool_result[result_key]
        new_fact = CaseFact(value=new_value, source_tool=tool_name)
        # BUG: overwrites silently, never records that the two results
        # actually disagreed.
        setattr(new_facts, field_name, new_fact)

    return new_facts


def should_escalate(case_facts: CaseFacts, iterations_used: int, max_iterations: int) -> Optional[str]:
    """Decide whether this session should escalate to a human right now."""
    if case_facts.conflicts:
        return "Unresolved conflicting facts require human review before proceeding."
    if case_facts.error_count >= 3:
        return "Repeated tool failures (3+) in this session require human review."
    if iterations_used >= max_iterations - 1:
        return "Session is near its iteration limit; escalate before it runs out."
    return None
