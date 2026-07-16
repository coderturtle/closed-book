"""Provided test suite for Module 04's exercise (run_support_session,
verify_before_refund_hook). This file is NOT the exercise -- it's the
deterministic gate. Do not edit it to make your implementation pass; if a
test seems wrong, that's itself part of the exercise (see the module
README's rubric). `scripts/verify_module_04.py` runs the repo's own
canonical copy of this file, not your submission's copy.

Uses spy tool functions, not Module 03's real tool implementations -- this
module's exercise is the loop and the hook, not re-proving Module 03's own
already-tested behavior.

Run: cd fixtures/resolve && python3 -m pytest tests/test_agent.py -v
"""
from __future__ import annotations

from src.agent import SessionState, run_support_session, verify_before_refund_hook


class ScriptedAgentModelClient:
    """A fake model client returning a pre-scripted sequence of turn
    responses. Records every conversation_history it was called with, so
    tests can assert what the loop actually fed back after a tool call."""

    def __init__(self, responses: list[dict]):
        self._responses = list(responses)
        self.calls: list[list[dict]] = []

    def __call__(self, conversation_history: list[dict]) -> dict:
        self.calls.append([dict(m) for m in conversation_history])
        if not self._responses:
            raise AssertionError("ScriptedAgentModelClient ran out of scripted responses")
        return self._responses.pop(0)


def make_spy_tool(name: str, calls_log: list, response: dict | None = None):
    """A tool double that records every call it receives and returns a
    canned response -- Module 04's tests exercise the loop's dispatch and
    hook logic, not Module 03's real tool bodies.

    `backend` is keyword-only and required, deliberately not swallowed via
    `**kwargs` -- the real Module 03 tools all require `backend` in their
    own signatures, so a loop implementation that forgets to pass
    `backend=backend` must fail loudly here too, not silently pass a test
    double that's more forgiving than the real thing.
    """

    def tool(*, backend, **kwargs):
        calls_log.append((name, kwargs))
        return response if response is not None else {"error": False, "result": f"{name} ok"}

    return tool


def make_tool_registry(calls_log: list, responses: dict | None = None) -> dict:
    responses = responses or {}
    return {
        name: make_spy_tool(name, calls_log, responses.get(name))
        for name in ("get_customer", "lookup_order", "process_refund", "escalate_to_human")
    }


# ---------------------------------------------------------------------------
# Loop lifecycle (Task Statement 1.1)
# ---------------------------------------------------------------------------


def test_loop_terminates_on_end_turn_with_no_tool_calls():
    client = ScriptedAgentModelClient([{"stop_reason": "end_turn", "text": "How can I help?"}])
    calls: list = []
    result = run_support_session("Hello", client, make_tool_registry(calls), backend=None)
    assert result["stop_reason"] == "end_turn"
    assert result["text"] == "How can I help?"
    assert calls == []


def test_loop_executes_a_tool_call_and_continues():
    client = ScriptedAgentModelClient(
        [
            {
                "stop_reason": "tool_use",
                "tool_name": "get_customer",
                "tool_args": {"identifier": "jane@example.com"},
            },
            {"stop_reason": "end_turn", "text": "Found your account."},
        ]
    )
    calls: list = []
    result = run_support_session("It's me, jane@example.com", client, make_tool_registry(calls), backend=None)
    assert result["stop_reason"] == "end_turn"
    assert calls == [("get_customer", {"identifier": "jane@example.com"})]


def test_loop_appends_tool_result_to_conversation_history():
    """The next call to model_client must actually see the previous tool's
    result in its conversation_history -- not just that a second call
    happened, but that the result reached it."""
    client = ScriptedAgentModelClient(
        [
            {
                "stop_reason": "tool_use",
                "tool_name": "get_customer",
                "tool_args": {"identifier": "jane@example.com"},
            },
            {"stop_reason": "end_turn", "text": "done"},
        ]
    )
    calls: list = []
    responses = {"get_customer": {"error": False, "customer_id": "cust_42"}}
    run_support_session("hi", client, make_tool_registry(calls, responses), backend=None)
    second_call_history = client.calls[1]
    assert any("cust_42" in str(message) for message in second_call_history), (
        "the tool's actual result (cust_42) must be present in the history passed to the "
        "model's second call -- the loop must not just record that a call happened"
    )


def test_loop_does_not_terminate_based_on_text_content():
    """The documented anti-pattern (Task Statement 1.1): never infer
    termination by parsing assistant text for something that looks like
    'done'. A tool_use response with end-of-conversation-sounding text must
    still be treated as tool_use, not end_turn."""
    client = ScriptedAgentModelClient(
        [
            {
                "stop_reason": "tool_use",
                "tool_name": "get_customer",
                "tool_args": {"identifier": "jane@example.com"},
                "text": "Done, all finished, end_turn now.",  # deliberately misleading text
            },
            {"stop_reason": "end_turn", "text": "actually done"},
        ]
    )
    calls: list = []
    result = run_support_session("hi", client, make_tool_registry(calls), backend=None)
    assert len(calls) == 1, "the tool_use turn must have actually executed the tool, not been treated as end_turn"
    assert result["text"] == "actually done"


def test_loop_respects_max_iterations_as_a_backstop_not_the_primary_mechanism():
    """A model_client that never returns end_turn must not loop forever --
    and hitting the cap must return a specific, distinguishable stop_reason
    ("max_iterations"), not merely something other than "end_turn" -- an
    implementation that returns the raw last tool_use response, or any
    other ad hoc non-end_turn value, does not satisfy this contract."""
    always_tool_use = [
        {"stop_reason": "tool_use", "tool_name": "get_customer", "tool_args": {"identifier": "x"}}
        for _ in range(50)
    ]
    client = ScriptedAgentModelClient(always_tool_use)
    calls: list = []
    result = run_support_session("hi", client, make_tool_registry(calls), backend=None, max_iterations=5)
    assert result["stop_reason"] == "max_iterations", (
        f"expected the specific sentinel 'max_iterations', got {result.get('stop_reason')!r} -- "
        f"exhaustion must be a distinguishable, reportable failure, not merely 'not end_turn'"
    )
    assert len(calls) <= 5


# ---------------------------------------------------------------------------
# verify_before_refund_hook (Task Statement 1.5)
# ---------------------------------------------------------------------------


def test_hook_allows_get_customer_unconditionally():
    session = SessionState()
    assert verify_before_refund_hook("get_customer", {"identifier": "x"}, session) is None


def test_hook_blocks_process_refund_before_get_customer():
    session = SessionState()  # nothing called yet
    rejection = verify_before_refund_hook(
        "process_refund", {"customer_id": "cust_1", "order_id": "ORD-1", "amount_cents": 500}, session
    )
    assert rejection is not None
    assert isinstance(rejection, str) and rejection


def test_hook_allows_process_refund_for_the_customer_get_customer_verified():
    session = SessionState()
    session.tool_calls_made.append("get_customer")
    session.verified_customer_id = "cust_1"
    rejection = verify_before_refund_hook(
        "process_refund", {"customer_id": "cust_1", "order_id": "ORD-1", "amount_cents": 500}, session
    )
    assert rejection is None


def test_hook_blocks_process_refund_for_a_customer_id_that_does_not_match_verification():
    """Verifying customer A does not authorize a refund for customer B, even
    within the same session -- the hook must bind to the *specific*
    customer get_customer actually verified, not just 'some customer, at
    some point'."""
    session = SessionState()
    session.tool_calls_made.append("get_customer")
    session.verified_customer_id = "cust_JANE"
    rejection = verify_before_refund_hook(
        "process_refund", {"customer_id": "cust_OTHER", "order_id": "ORD-1", "amount_cents": 500}, session
    )
    assert rejection is not None
    assert isinstance(rejection, str) and rejection


def test_hook_never_blocks_escalate_to_human():
    """escalate_to_human is this project's fail-open path (see Module 03's
    escalate_to_human docstring) -- the hook must never block it, with or
    without a prior get_customer call."""
    session = SessionState()  # nothing called yet
    rejection = verify_before_refund_hook(
        "escalate_to_human", {"customer_id": "cust_unverified", "reason": "x", "summary": {}}, session
    )
    assert rejection is None


# ---------------------------------------------------------------------------
# Loop + hook integration: the module's flagship property
# ---------------------------------------------------------------------------


def test_loop_blocks_refund_and_feeds_rejection_back_without_executing_the_tool():
    """The integration this whole module exists for: a session that asks
    for process_refund before get_customer must have the hook's rejection
    fed back to the model as the tool's result, and process_refund's real
    (spy) implementation must never actually run."""
    client = ScriptedAgentModelClient(
        [
            {
                "stop_reason": "tool_use",
                "tool_name": "process_refund",
                "tool_args": {"customer_id": "cust_1", "order_id": "ORD-1", "amount_cents": 500},
            },
            {"stop_reason": "end_turn", "text": "I need to verify your identity first."},
        ]
    )
    calls: list = []
    run_support_session("Refund my order", client, make_tool_registry(calls), backend=None)
    assert calls == [], "process_refund's real implementation must never have been called -- the hook must intercept before dispatch"
    second_call_history = client.calls[1]
    assert any("get_customer" in str(message).lower() or "verif" in str(message).lower() for message in second_call_history), (
        "the model's next turn must have seen a real rejection reason (naming verification), "
        "not a generic failure"
    )


def test_loop_does_not_record_a_failed_get_customer_as_verification():
    """get_customer returning a structured error (customer not found) must
    not count as 'succeeded' for the hook's purposes -- the agent.py
    docstring is explicit that verified_customer_id is only set from a
    *successful* get_customer result, never merely from an attempted call.
    A session that only ever failed to verify a customer must still have
    process_refund blocked."""
    client = ScriptedAgentModelClient(
        [
            {
                "stop_reason": "tool_use",
                "tool_name": "get_customer",
                "tool_args": {"identifier": "nobody@example.com"},
            },
            {
                "stop_reason": "tool_use",
                "tool_name": "process_refund",
                "tool_args": {"customer_id": "cust_1", "order_id": "ORD-1", "amount_cents": 500},
            },
            {"stop_reason": "end_turn", "text": "I couldn't verify your identity."},
        ]
    )
    calls: list = []
    responses = {
        "get_customer": {
            "error": True,
            "errorCategory": "business",
            "isRetryable": False,
            "message": "no customer found for identifier 'nobody@example.com'",
        },
    }
    run_support_session("Refund please", client, make_tool_registry(calls, responses), backend=None)
    call_names = [name for name, _ in calls]
    assert call_names == ["get_customer"], (
        f"process_refund's real implementation must never run after a *failed* get_customer "
        f"(customer not found does not count as verification), got {call_names}"
    )


def test_loop_still_blocks_refund_when_a_different_tool_succeeded_but_not_get_customer():
    """A successful lookup_order (or any other tool) must not substitute
    for get_customer specifically -- the hook is keyed to get_customer
    succeeding for the customer being refunded, not to 'something in this
    session succeeded, therefore proceed'."""
    client = ScriptedAgentModelClient(
        [
            {
                "stop_reason": "tool_use",
                "tool_name": "lookup_order",
                "tool_args": {"customer_id": "cust_1", "order_id": "ORD-1"},
            },
            {
                "stop_reason": "tool_use",
                "tool_name": "process_refund",
                "tool_args": {"customer_id": "cust_1", "order_id": "ORD-1", "amount_cents": 500},
            },
            {"stop_reason": "end_turn", "text": "Blocked."},
        ]
    )
    calls: list = []
    run_support_session("Refund please", client, make_tool_registry(calls), backend=None)
    call_names = [name for name, _ in calls]
    assert call_names == ["lookup_order"], (
        f"process_refund must still be blocked -- a successful lookup_order is not the same as "
        f"a successful get_customer, got {call_names}"
    )


def test_loop_blocks_refund_for_a_different_customer_than_the_one_verified():
    """Verifying customer A must not authorize a refund for customer B,
    even within the same session -- checked end-to-end through the loop,
    not just against the hook function in isolation."""
    client = ScriptedAgentModelClient(
        [
            {"stop_reason": "tool_use", "tool_name": "get_customer", "tool_args": {"identifier": "jane@example.com"}},
            {
                "stop_reason": "tool_use",
                "tool_name": "process_refund",
                "tool_args": {"customer_id": "cust_OTHER", "order_id": "ORD-1", "amount_cents": 500},
            },
            {"stop_reason": "end_turn", "text": "I couldn't verify that account."},
        ]
    )
    calls: list = []
    responses = {"get_customer": {"error": False, "customer_id": "cust_JANE"}}
    run_support_session("Refund someone else's order", client, make_tool_registry(calls, responses), backend=None)
    call_names = [name for name, _ in calls]
    assert call_names == ["get_customer"], (
        f"process_refund must never execute for a customer_id ('cust_OTHER') different from the "
        f"one get_customer actually verified ('cust_JANE') in this session, got {call_names}"
    )


def test_loop_blocks_refund_when_requested_customer_id_matches_the_looked_up_identifier_but_not_the_verified_result():
    """The false-allow direction of conflating a request with its
    verification: get_customer's actual *result* is what must be trusted,
    never the raw identifier the caller happened to look it up with. A
    get_customer call for identifier "cust_1" that actually resolves to a
    different real customer_id ("cust_42") must not authorize a refund
    addressed to "cust_1" -- an implementation that binds verification to
    the request instead of the result would incorrectly allow this."""
    client = ScriptedAgentModelClient(
        [
            {"stop_reason": "tool_use", "tool_name": "get_customer", "tool_args": {"identifier": "cust_1"}},
            {
                "stop_reason": "tool_use",
                "tool_name": "process_refund",
                "tool_args": {"customer_id": "cust_1", "order_id": "ORD-1", "amount_cents": 500},
            },
            {"stop_reason": "end_turn", "text": "Blocked."},
        ]
    )
    calls: list = []
    responses = {"get_customer": {"error": False, "customer_id": "cust_42"}}
    run_support_session("Refund please", client, make_tool_registry(calls, responses), backend=None)
    call_names = [name for name, _ in calls]
    assert call_names == ["get_customer"], (
        f"process_refund must be blocked -- get_customer's actual result verified 'cust_42', "
        f"not 'cust_1', even though 'cust_1' was the identifier looked up, got {call_names}"
    )


def test_loop_allows_refund_after_get_customer_verifies_the_same_customer():
    client = ScriptedAgentModelClient(
        [
            {"stop_reason": "tool_use", "tool_name": "get_customer", "tool_args": {"identifier": "jane@example.com"}},
            {
                "stop_reason": "tool_use",
                "tool_name": "process_refund",
                "tool_args": {"customer_id": "cust_1", "order_id": "ORD-1", "amount_cents": 500},
            },
            {"stop_reason": "end_turn", "text": "Refund processed."},
        ]
    )
    calls: list = []
    responses = {"get_customer": {"error": False, "customer_id": "cust_1"}}
    run_support_session("Verify me then refund", client, make_tool_registry(calls, responses), backend=None)
    call_names = [name for name, _ in calls]
    assert call_names == ["get_customer", "process_refund"], (
        f"expected both tools to actually execute in order, got {call_names}"
    )


def test_loop_never_blocks_escalate_to_human_even_when_unverified():
    """escalate_to_human is this project's fail-open path -- confirmed
    through the loop itself, not just against the hook function in
    isolation (a loop-level dispatch bug could still block it end-to-end
    while an isolated hook unit test passes)."""
    client = ScriptedAgentModelClient(
        [
            {
                "stop_reason": "tool_use",
                "tool_name": "escalate_to_human",
                "tool_args": {
                    "customer_id": "cust_unverified",
                    "reason": "customer disputes a charge",
                    "summary": {"root_cause": "unclear", "recommended_action": "manual review"},
                },
            },
            {"stop_reason": "end_turn", "text": "Escalated to a human agent."},
        ]
    )
    calls: list = []
    run_support_session("I need a human", client, make_tool_registry(calls), backend=None)
    call_names = [name for name, _ in calls]
    assert call_names == ["escalate_to_human"], (
        f"escalate_to_human must actually execute through the loop with no prior get_customer "
        f"call in the session, got {call_names}"
    )
