"""Provided test suite for Module 05's exercise (update_case_facts,
should_escalate). This file is NOT the exercise -- it's the deterministic
gate. Do not edit it to make your implementation pass; if a test seems
wrong, that's itself part of the exercise (see the module README's
rubric). `scripts/verify_module_05.py` runs the repo's own canonical copy
of this file, not your submission's copy.

Run: cd fixtures/resolve && python3 -m pytest tests/test_context.py -v
"""
from __future__ import annotations

import inspect

from src.context import CaseFacts, should_escalate, update_case_facts


# ---------------------------------------------------------------------------
# update_case_facts (Task Statements 5.1, 5.6)
# ---------------------------------------------------------------------------


def test_update_case_facts_records_customer_id_from_get_customer_success():
    facts = update_case_facts(
        CaseFacts(), "get_customer", {"identifier": "jane@example.com"}, {"customer_id": "cust_1"}
    )
    assert facts.customer_id is not None
    assert facts.customer_id.value == "cust_1"
    assert facts.customer_id.source_tool == "get_customer"


def test_update_case_facts_does_not_record_customer_id_on_get_customer_failure():
    facts = update_case_facts(
        CaseFacts(),
        "get_customer",
        {"identifier": "nobody@example.com"},
        {"error": True, "errorCategory": "business", "isRetryable": False, "message": "not found"},
    )
    assert facts.customer_id is None
    assert facts.error_count == 1


def test_update_case_facts_records_order_id_from_lookup_order_success():
    facts = update_case_facts(
        CaseFacts(), "lookup_order", {"customer_id": "cust_1", "order_id": "ORD-1"}, {"order_id": "ORD-1", "refundable_cents": 5000}
    )
    assert facts.order_id is not None
    assert facts.order_id.value == "ORD-1"
    assert facts.order_id.source_tool == "lookup_order"


def test_update_case_facts_records_refund_amount_from_process_refund_success():
    facts = update_case_facts(
        CaseFacts(),
        "process_refund",
        {"customer_id": "cust_1", "order_id": "ORD-1", "amount_cents": 3000},
        {"refunded_cents": 3000, "order_id": "ORD-1"},
    )
    assert facts.refund_amount_cents is not None
    assert facts.refund_amount_cents.value == 3000
    assert facts.refund_amount_cents.source_tool == "process_refund"


def test_update_case_facts_reads_the_actual_refund_result_not_the_requested_amount():
    """A backend might only partially honor a request (e.g. cap a refund at
    what's actually refundable). The recorded fact must reflect what the
    result actually says happened, not what was asked for."""
    facts = update_case_facts(
        CaseFacts(),
        "process_refund",
        {"customer_id": "cust_1", "order_id": "ORD-1", "amount_cents": 5000},
        {"refunded_cents": 3000, "order_id": "ORD-1"},
    )
    assert facts.refund_amount_cents.value == 3000, (
        "must record the result's actual refunded_cents (3000), not the requested amount_cents (5000)"
    )


def test_update_case_facts_reads_the_actual_order_result_not_the_requested_order_id():
    """The same result-vs-request discipline applies to lookup_order: its
    tool_args and tool_result both happen to use the key "order_id", which
    makes it easy for an implementation to accidentally read the request
    instead of the result without any test noticing -- unless a test uses
    two different values for the two, as this one does."""
    facts = update_case_facts(
        CaseFacts(),
        "lookup_order",
        {"customer_id": "cust_1", "order_id": "ORD-REQUESTED"},
        {"order_id": "ORD-ACTUAL", "refundable_cents": 5000},
    )
    assert facts.order_id.value == "ORD-ACTUAL", (
        "must record the result's actual order_id (ORD-ACTUAL), not the requested order_id (ORD-REQUESTED)"
    )


def test_update_case_facts_increments_error_count_on_any_tool_error():
    facts = CaseFacts()
    facts = update_case_facts(facts, "process_refund", {}, {"error": True, "errorCategory": "validation", "isRetryable": False, "message": "x"})
    assert facts.error_count == 1
    facts = update_case_facts(facts, "lookup_order", {}, {"error": True, "errorCategory": "business", "isRetryable": False, "message": "y"})
    assert facts.error_count == 2


def test_update_case_facts_error_does_not_extract_a_fact_from_the_request_args():
    """lookup_order's tool_args happens to carry a real "order_id" key --
    an implementation that reads facts from tool_args instead of gating on
    the error at all would record a fact from a *failed* call, using
    exactly the key-name coincidence test_update_case_facts_reads_the_actual_order_result_not_the_requested_order_id
    exists to catch on the success path. This checks the same coincidence
    can't be exploited on the error path instead."""
    facts = update_case_facts(
        CaseFacts(),
        "lookup_order",
        {"customer_id": "cust_1", "order_id": "ORD-9"},
        {"error": True, "errorCategory": "business", "isRetryable": False, "message": "no such order"},
    )
    assert facts.order_id is None, "a failed lookup_order must record no order_id fact, even though tool_args happens to carry one"
    assert facts.error_count == 1


def test_update_case_facts_does_not_mutate_the_original():
    original = CaseFacts()
    updated = update_case_facts(original, "get_customer", {"identifier": "x"}, {"customer_id": "cust_1"})
    assert original.customer_id is None, "the original CaseFacts passed in must not be mutated"
    assert updated.customer_id is not None


def test_update_case_facts_conflicts_list_is_independent_of_the_original():
    """A shallow copy that reuses the original's `conflicts` list object
    would pass every other test here, since every scalar field looks
    untouched -- only appending to `conflicts` on one and checking the
    other actually catches it."""
    original = update_case_facts(CaseFacts(), "get_customer", {"identifier": "a@example.com"}, {"customer_id": "cust_A"})
    assert original.conflicts == []
    updated = update_case_facts(original, "get_customer", {"identifier": "b@example.com"}, {"customer_id": "cust_B"})
    assert len(updated.conflicts) == 1
    assert original.conflicts == [], (
        "recording a conflict on the returned CaseFacts must not also mutate the original's conflicts list"
    )


def test_update_case_facts_error_path_preserves_existing_facts_and_does_not_mutate_original():
    """The no-mutation and error-path rules apply together: an error on one
    tool must not discard facts a *different*, earlier, successful call
    already established, and the object passed in must come out unchanged
    either way."""
    facts = update_case_facts(CaseFacts(), "get_customer", {"identifier": "a@example.com"}, {"customer_id": "cust_A"})
    updated = update_case_facts(
        facts, "process_refund", {"customer_id": "cust_A", "order_id": "ORD-1", "amount_cents": 500},
        {"error": True, "errorCategory": "business", "isRetryable": False, "message": "no such order"},
    )
    assert updated.customer_id is not None and updated.customer_id.value == "cust_A", (
        "an unrelated tool's error must not discard an already-established fact"
    )
    assert updated.error_count == 1
    assert facts.error_count == 0, "the object passed in must not have its error_count mutated"
    assert facts.customer_id.value == "cust_A", "the object passed in must still have its own fact intact"


def test_update_case_facts_records_a_conflict_when_a_fact_changes():
    facts = update_case_facts(CaseFacts(), "get_customer", {"identifier": "a@example.com"}, {"customer_id": "cust_A"})
    facts = update_case_facts(facts, "get_customer", {"identifier": "b@example.com"}, {"customer_id": "cust_B"})
    assert len(facts.conflicts) == 1
    assert facts.customer_id.value == "cust_B", "the current value should reflect the most recent result"


def test_update_case_facts_conflict_entries_preserve_both_sourced_values():
    facts = update_case_facts(CaseFacts(), "get_customer", {"identifier": "a@example.com"}, {"customer_id": "cust_A"})
    facts = update_case_facts(facts, "get_customer", {"identifier": "b@example.com"}, {"customer_id": "cust_B"})
    field_name, old_fact, new_fact = facts.conflicts[0]
    assert field_name == "customer_id"
    assert old_fact.value == "cust_A"
    assert new_fact.value == "cust_B"
    assert old_fact.source_tool == "get_customer"
    assert new_fact.source_tool == "get_customer"


def test_update_case_facts_order_id_conflict_preserves_both_sourced_values():
    """The same conflict-preservation guarantee, checked for order_id --
    an implementation that gets customer_id's conflict handling right
    could still record order_id conflicts as (field, None, None) or
    similarly hollow entries without this test."""
    facts = update_case_facts(CaseFacts(), "lookup_order", {"customer_id": "cust_1", "order_id": "ORD-1"}, {"order_id": "ORD-A"})
    facts = update_case_facts(facts, "lookup_order", {"customer_id": "cust_1", "order_id": "ORD-1"}, {"order_id": "ORD-B"})
    assert len(facts.conflicts) == 1
    field_name, old_fact, new_fact = facts.conflicts[0]
    assert field_name == "order_id"
    assert old_fact.value == "ORD-A"
    assert new_fact.value == "ORD-B"
    assert old_fact.source_tool == "lookup_order"
    assert new_fact.source_tool == "lookup_order"
    assert facts.order_id.value == "ORD-B"


def test_update_case_facts_no_conflict_when_second_result_matches_first():
    facts = update_case_facts(CaseFacts(), "get_customer", {"identifier": "a@example.com"}, {"customer_id": "cust_A"})
    facts = update_case_facts(facts, "get_customer", {"identifier": "a@example.com"}, {"customer_id": "cust_A"})
    assert facts.conflicts == [], "reporting the same value twice is confirmation, not a conflict"


def test_update_case_facts_no_conflict_when_second_order_id_result_matches_first():
    facts = update_case_facts(CaseFacts(), "lookup_order", {"customer_id": "cust_1", "order_id": "ORD-1"}, {"order_id": "ORD-A"})
    facts = update_case_facts(facts, "lookup_order", {"customer_id": "cust_1", "order_id": "ORD-1"}, {"order_id": "ORD-A"})
    assert facts.conflicts == [], "reporting the same order_id twice is confirmation, not a conflict"


def test_update_case_facts_records_a_conflict_for_refund_amount_cents():
    """Two successful process_refund results disagreeing on the actual
    amount refunded (e.g. a retried call against a partially-updated
    backend) must be recorded as a conflict, the same as any other field."""
    facts = update_case_facts(
        CaseFacts(), "process_refund", {"customer_id": "cust_1", "order_id": "ORD-1", "amount_cents": 3000},
        {"refunded_cents": 3000, "order_id": "ORD-1"},
    )
    facts = update_case_facts(
        facts, "process_refund", {"customer_id": "cust_1", "order_id": "ORD-1", "amount_cents": 3000},
        {"refunded_cents": 1500, "order_id": "ORD-1"},
    )
    assert len(facts.conflicts) == 1
    field_name, old_fact, new_fact = facts.conflicts[0]
    assert field_name == "refund_amount_cents"
    assert old_fact.value == 3000
    assert new_fact.value == 1500
    assert old_fact.source_tool == "process_refund"
    assert new_fact.source_tool == "process_refund"
    assert facts.refund_amount_cents.value == 1500, "the current value should reflect the most recent result"


def test_update_case_facts_no_conflict_when_second_refund_result_matches_first():
    facts = update_case_facts(
        CaseFacts(), "process_refund", {"customer_id": "cust_1", "order_id": "ORD-1", "amount_cents": 3000},
        {"refunded_cents": 3000, "order_id": "ORD-1"},
    )
    facts = update_case_facts(
        facts, "process_refund", {"customer_id": "cust_1", "order_id": "ORD-1", "amount_cents": 3000},
        {"refunded_cents": 3000, "order_id": "ORD-1"},
    )
    assert facts.conflicts == [], (
        "reporting the same refunded_cents twice is confirmation, not a conflict -- and a spurious "
        "conflict here would wrongly trigger should_escalate's conflicts-first rule"
    )


def test_update_case_facts_accumulates_independent_conflicts_across_different_fields():
    """Two unrelated conflicts (one on customer_id, one on order_id, from
    separate tool calls) must both survive in `conflicts` -- accumulating,
    not overwriting each other just because they're stored in the same
    list."""
    facts = update_case_facts(CaseFacts(), "get_customer", {"identifier": "a@example.com"}, {"customer_id": "cust_A"})
    facts = update_case_facts(facts, "get_customer", {"identifier": "b@example.com"}, {"customer_id": "cust_B"})
    facts = update_case_facts(facts, "lookup_order", {"customer_id": "cust_B", "order_id": "ORD-1"}, {"order_id": "ORD-1"})
    facts = update_case_facts(facts, "lookup_order", {"customer_id": "cust_B", "order_id": "ORD-2"}, {"order_id": "ORD-2"})
    assert len(facts.conflicts) == 2, f"expected 2 independent conflicts (customer_id, order_id), got {len(facts.conflicts)}"
    conflict_fields = {field_name for field_name, _, _ in facts.conflicts}
    assert conflict_fields == {"customer_id", "order_id"}


def test_update_case_facts_ignores_a_tool_with_no_known_fact_mapping():
    facts = update_case_facts(
        CaseFacts(),
        "escalate_to_human",
        {"customer_id": "cust_1", "reason": "x", "summary": {"root_cause": "a", "recommended_action": "b"}},
        {"escalated": True, "customer_id": "cust_1", "reason": "x"},
    )
    assert facts.customer_id is None
    assert facts.error_count == 0
    assert facts.conflicts == []


# ---------------------------------------------------------------------------
# should_escalate (Task Statements 5.2, 5.5)
# ---------------------------------------------------------------------------


def test_should_escalate_signature_has_no_confidence_or_extra_parameters():
    """Task Statement 5.5's core lesson only holds if the function is
    structurally unable to see a confidence/sentiment-style signal -- an
    unused or defaulted-to-None extra parameter would reopen exactly the
    door this design is supposed to keep closed, even if nothing currently
    calls it with a value."""
    params = list(inspect.signature(should_escalate).parameters)
    assert params == ["case_facts", "iterations_used", "max_iterations"], (
        f"should_escalate must take exactly these three parameters, no more, got {params}"
    )


def test_should_escalate_returns_none_when_nothing_is_wrong():
    assert should_escalate(CaseFacts(), iterations_used=1, max_iterations=10) is None


def test_should_escalate_flags_unresolved_conflicts_first():
    """Conflicts must be checked before the error-count or iteration
    thresholds -- an unresolved factual disagreement is ambiguity a human
    should resolve regardless of what else is also true about the session."""
    facts = CaseFacts(error_count=5)
    facts.conflicts.append(("customer_id", object(), object()))
    reason = should_escalate(facts, iterations_used=9, max_iterations=10)
    assert reason is not None
    assert "conflict" in reason.lower()
    assert "failure" not in reason.lower() and "iteration" not in reason.lower()


def test_should_escalate_flags_error_threshold():
    facts = CaseFacts(error_count=3)
    reason = should_escalate(facts, iterations_used=1, max_iterations=10)
    assert reason is not None
    assert "fail" in reason.lower() or "error" in reason.lower()


def test_should_escalate_does_not_flag_below_error_threshold():
    facts = CaseFacts(error_count=2)
    assert should_escalate(facts, iterations_used=1, max_iterations=10) is None


def test_should_escalate_checks_error_threshold_before_iteration_threshold():
    facts = CaseFacts(error_count=3)
    reason = should_escalate(facts, iterations_used=9, max_iterations=10)
    assert reason is not None
    assert ("fail" in reason.lower() or "error" in reason.lower())
    assert "iteration" not in reason.lower()


def test_should_escalate_flags_near_max_iterations():
    reason = should_escalate(CaseFacts(), iterations_used=9, max_iterations=10)
    assert reason is not None
    assert "iteration" in reason.lower()


def test_should_escalate_does_not_flag_well_before_max_iterations():
    assert should_escalate(CaseFacts(), iterations_used=2, max_iterations=10) is None


def test_should_escalate_iteration_boundary_is_exact():
    """The boundary itself, not just "near" vs. "well before" -- one
    iteration short of the threshold must not escalate, and the threshold
    itself must."""
    assert should_escalate(CaseFacts(), iterations_used=8, max_iterations=10) is None, (
        "iterations_used == max_iterations - 2 must not escalate yet"
    )
    assert should_escalate(CaseFacts(), iterations_used=9, max_iterations=10) is not None, (
        "iterations_used == max_iterations - 1 must escalate"
    )


def test_should_escalate_reasons_are_specific_not_generic():
    conflict_facts = CaseFacts()
    conflict_facts.conflicts.append(("order_id", object(), object()))
    conflict_reason = should_escalate(conflict_facts, iterations_used=0, max_iterations=10)
    error_reason = should_escalate(CaseFacts(error_count=3), iterations_used=0, max_iterations=10)
    iteration_reason = should_escalate(CaseFacts(), iterations_used=9, max_iterations=10)
    assert len({conflict_reason, error_reason, iteration_reason}) == 3, (
        "each escalation condition must produce its own distinguishable reason, "
        "not one generic 'escalate' string"
    )
