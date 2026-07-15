"""Provided test suite for Module 03's exercise (the four MCP tools in
src/tools/). This file is NOT the exercise -- it's the deterministic gate.
Do not edit it to make your implementation pass; if a test seems wrong,
that's itself part of the exercise (see the module README's rubric).

Run: cd fixtures/resolve && python3 -m pytest tests/test_tools.py -v
"""
from __future__ import annotations

from src.tool_errors import ERROR_CATEGORIES
from src.tools.escalate_to_human import escalate_to_human
from src.tools.get_customer import get_customer
from src.tools.lookup_order import lookup_order
from src.tools.process_refund import process_refund


class FakeBackend:
    """A fake backend with scripted customer/order records, no real database."""

    def __init__(self, customers: dict | None = None, orders: dict | None = None):
        # customers: {identifier: customer_record}
        # orders: {(customer_id, order_id): order_record}
        self._customers = customers or {}
        self._orders = orders or {}

    def find_customer(self, identifier):
        return self._customers.get(identifier)

    def find_order(self, customer_id, order_id):
        return self._orders.get((customer_id, order_id))


def _assert_valid_error_shape(result: dict):
    """Every tool's error response must use the shared, consistent shape --
    not an ad hoc structure that varies per tool."""
    assert result.get("error") is True
    assert result.get("errorCategory") in ERROR_CATEGORIES
    assert isinstance(result.get("isRetryable"), bool)
    assert result.get("message")


# ---------------------------------------------------------------------------
# get_customer
# ---------------------------------------------------------------------------


def test_get_customer_found():
    backend = FakeBackend(customers={"jane@example.com": {"customer_id": "cust_1", "email": "jane@example.com"}})
    result = get_customer("jane@example.com", backend)
    assert result.get("error") is not True
    assert result["customer_id"] == "cust_1"


def test_get_customer_not_found_is_structured_not_an_exception():
    backend = FakeBackend(customers={})
    result = get_customer("nobody@example.com", backend)
    _assert_valid_error_shape(result)


def test_get_customer_docstring_disambiguates_identifier_formats():
    """The docstring must state which identifier formats get_customer
    accepts (Task Statement 2.1: precise boundaries, not just a name) --
    this is what lets an agent choose correctly between get_customer and
    lookup_order without trial and error."""
    doc = (get_customer.__doc__ or "").lower()
    for keyword in ("email", "phone", "account"):
        assert keyword in doc


# ---------------------------------------------------------------------------
# lookup_order
# ---------------------------------------------------------------------------


def test_lookup_order_found():
    backend = FakeBackend(orders={("cust_1", "ORD-1"): {"order_id": "ORD-1", "refundable_cents": 5000}})
    result = lookup_order("cust_1", "ORD-1", backend)
    assert result.get("error") is not True
    assert result["order_id"] == "ORD-1"


def test_lookup_order_not_found_is_structured():
    backend = FakeBackend(orders={})
    result = lookup_order("cust_1", "ORD-does-not-exist", backend)
    _assert_valid_error_shape(result)


def test_lookup_order_does_not_leak_other_customers_orders():
    """An order that exists but belongs to a different customer must return
    the same 'not found' result as a genuinely nonexistent order -- never a
    response that confirms the order_id is valid for someone else."""
    backend = FakeBackend(orders={("cust_OTHER", "ORD-1"): {"order_id": "ORD-1", "refundable_cents": 5000}})
    result = lookup_order("cust_1", "ORD-1", backend)  # wrong customer_id for this order
    _assert_valid_error_shape(result)
    assert "cust_OTHER" not in str(result)


def test_lookup_order_docstring_disambiguates_from_get_customer():
    doc = (lookup_order.__doc__ or "").lower()
    assert "customer_id" in doc
    assert "order" in doc


# ---------------------------------------------------------------------------
# process_refund -- the safety-critical tool
# ---------------------------------------------------------------------------


def test_process_refund_happy_path():
    backend = FakeBackend(
        customers={"cust_1": {"customer_id": "cust_1"}},
        orders={("cust_1", "ORD-1"): {"order_id": "ORD-1", "refundable_cents": 5000}},
    )
    result = process_refund("cust_1", "ORD-1", 5000, backend)
    assert result.get("error") is not True
    assert result["refunded_cents"] == 5000


def test_process_refund_fails_closed_on_unverified_customer():
    """The tool's own defense-in-depth check: a customer_id that doesn't
    resolve via backend.find_customer must be rejected here, even if some
    caller skipped verification -- never process a refund on a caller's
    word alone."""
    backend = FakeBackend(
        customers={},  # "cust_fake" was never verified by get_customer
        orders={("cust_fake", "ORD-1"): {"order_id": "ORD-1", "refundable_cents": 5000}},
    )
    result = process_refund("cust_fake", "ORD-1", 5000, backend)
    _assert_valid_error_shape(result)
    assert result["errorCategory"] == "permission"
    assert result["isRetryable"] is False


def test_process_refund_rejects_order_not_belonging_to_customer():
    backend = FakeBackend(
        customers={"cust_1": {"customer_id": "cust_1"}},
        orders={("cust_OTHER", "ORD-1"): {"order_id": "ORD-1", "refundable_cents": 5000}},
    )
    result = process_refund("cust_1", "ORD-1", 5000, backend)
    _assert_valid_error_shape(result)


def test_process_refund_rejects_amount_exceeding_refundable():
    backend = FakeBackend(
        customers={"cust_1": {"customer_id": "cust_1"}},
        orders={("cust_1", "ORD-1"): {"order_id": "ORD-1", "refundable_cents": 5000}},
    )
    result = process_refund("cust_1", "ORD-1", 999999, backend)
    _assert_valid_error_shape(result)
    assert result["errorCategory"] == "validation"


def test_process_refund_rejects_non_positive_amount():
    backend = FakeBackend(
        customers={"cust_1": {"customer_id": "cust_1"}},
        orders={("cust_1", "ORD-1"): {"order_id": "ORD-1", "refundable_cents": 5000}},
    )
    result = process_refund("cust_1", "ORD-1", 0, backend)
    _assert_valid_error_shape(result)


# ---------------------------------------------------------------------------
# escalate_to_human
# ---------------------------------------------------------------------------


def test_escalate_to_human_happy_path():
    backend = FakeBackend()
    result = escalate_to_human(
        "cust_1",
        "policy exception requested",
        {"root_cause": "customer requests exception to 30-day policy", "recommended_action": "manager review"},
        backend,
    )
    assert result.get("error") is not True


def test_escalate_to_human_rejects_missing_root_cause():
    backend = FakeBackend()
    result = escalate_to_human("cust_1", "unclear", {"recommended_action": "review"}, backend)
    _assert_valid_error_shape(result)


def test_escalate_to_human_rejects_empty_recommended_action():
    backend = FakeBackend()
    result = escalate_to_human(
        "cust_1", "unclear", {"root_cause": "customer is upset", "recommended_action": ""}, backend
    )
    _assert_valid_error_shape(result)


# ---------------------------------------------------------------------------
# Cross-tool: consistent error taxonomy (Task Statement 2.2)
# ---------------------------------------------------------------------------


def test_all_four_tools_use_the_same_error_shape():
    """Every tool's error path returns the same shape (error/errorCategory/
    isRetryable/message) -- an agent handling a failure shouldn't need
    per-tool special-casing to know what went wrong."""
    backend = FakeBackend()
    results = [
        get_customer("nobody@example.com", backend),
        lookup_order("cust_1", "ORD-none", backend),
        process_refund("cust_fake", "ORD-none", 100, backend),
        escalate_to_human("cust_1", "x", {}, backend),
    ]
    for result in results:
        _assert_valid_error_shape(result)
