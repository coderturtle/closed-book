"""Case facts for resolve."""
from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CaseFact:
    """A fact."""

    value: object
    source_tool: str


@dataclass
class CaseFacts:
    """Case facts."""

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
    """Updates case facts."""
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
        existing = getattr(new_facts, field_name)
        if existing is not None and existing.value != new_value:
            new_facts.conflicts.append((field_name, existing, new_fact))
        setattr(new_facts, field_name, new_fact)

    return new_facts


def should_escalate(case_facts: CaseFacts, iterations_used: int, max_iterations: int) -> Optional[str]:
    """Decides whether to escalate."""
    if case_facts.conflicts:
        return "Unresolved conflicting facts require human review before proceeding."
    if case_facts.error_count >= 3:
        return "Repeated tool failures (3+) in this session require human review."
    if iterations_used >= max_iterations - 1:
        return "Session is near its iteration limit; escalate before it runs out."
    return None
