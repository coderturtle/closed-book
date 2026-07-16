"""Provided test suite for Module 06's capstone exercise
(run_full_support_session). This file is NOT the exercise -- it's the
deterministic gate. Do not edit it to make your implementation pass; if a
test seems wrong, that's itself part of the exercise (see the module
README's rubric). `scripts/verify_module_06.py` runs the repo's own
canonical copy of this file, not your submission's copy.

Unlike every earlier module's suite, this one is written to FAIL against
`src/session.py` exactly as shipped -- that file is not a stub, it's a
fully-written integration with two real, seeded defects. Your job is to
diagnose and fix them, not implement anything from scratch.

Run: cd fixtures/resolve && python3 -m pytest tests/test_session.py -v
"""
from __future__ import annotations

from src.session import run_full_support_session


class ScriptedExtractionModelClient:
    """Module 02's model client shape: (prompt, prior_attempts) -> raw dict.
    Records every call so tests can confirm extraction actually ran."""

    def __init__(self, responses: list[dict]):
        self._responses = list(responses)
        self.calls: list[tuple[str, list[dict]]] = []

    def __call__(self, prompt: str, prior_attempts: list[dict]) -> dict:
        self.calls.append((prompt, list(prior_attempts)))
        if not self._responses:
            raise AssertionError("ScriptedExtractionModelClient ran out of scripted responses")
        return self._responses.pop(0)


class ScriptedAgentModelClient:
    """Module 04's model client shape: (conversation_history) -> response dict."""

    def __init__(self, responses: list[dict]):
        self._responses = list(responses)
        self.calls: list[list[dict]] = []

    def __call__(self, conversation_history: list[dict]) -> dict:
        self.calls.append([dict(m) for m in conversation_history])
        if not self._responses:
            raise AssertionError(
                "ScriptedAgentModelClient ran out of scripted responses -- if this fired "
                "unexpectedly, the loop called the model more times than a correct "
                "implementation should have needed to"
            )
        return self._responses.pop(0)


def make_spy_tool(name: str, calls_log: list, response: dict | None = None):
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


def high_confidence_extraction(refund_amount_cents=None, reason_category="defective_item"):
    return {
        "refund_amount_cents": refund_amount_cents,
        "reason_category": reason_category,
        "reason_detail": None,
        "confidence": "high",
    }


# ---------------------------------------------------------------------------
# Baseline: the integration must actually work for a clean session
# ---------------------------------------------------------------------------


def test_extraction_actually_runs_before_the_loop():
    extraction_client = ScriptedExtractionModelClient([high_confidence_extraction()])
    agent_client = ScriptedAgentModelClient([{"stop_reason": "end_turn", "text": "How can I help?"}])
    calls: list = []
    run_full_support_session(
        "My lamp broke", agent_client, extraction_client, make_tool_registry(calls), backend=None
    )
    assert len(extraction_client.calls) == 1, "extract_refund_request must actually be called with the customer's message"


def test_clean_session_completes_via_end_turn():
    extraction_client = ScriptedExtractionModelClient([high_confidence_extraction()])
    agent_client = ScriptedAgentModelClient(
        [
            {"stop_reason": "tool_use", "tool_name": "get_customer", "tool_args": {"identifier": "jane@example.com"}},
            {"stop_reason": "end_turn", "text": "Found your account."},
        ]
    )
    calls: list = []
    responses = {"get_customer": {"error": False, "customer_id": "cust_1"}}
    result = run_full_support_session(
        "My lamp broke", agent_client, extraction_client, make_tool_registry(calls, responses), backend=None
    )
    assert result.get("stop_reason") == "end_turn"
    assert not result.get("escalated")
    assert calls == [("get_customer", {"identifier": "jane@example.com"})]


def test_hook_still_blocks_unverified_refund_through_the_full_integration():
    """Module 04's verify_before_refund_hook must still be wired in and
    enforced -- the capstone integration must not have silently dropped it
    while wiring everything else together."""
    extraction_client = ScriptedExtractionModelClient([high_confidence_extraction()])
    agent_client = ScriptedAgentModelClient(
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
    result = run_full_support_session(
        "Refund my order", agent_client, extraction_client, make_tool_registry(calls), backend=None
    )
    assert calls == [], "process_refund must still be blocked without a prior verified get_customer call"
    assert result.get("stop_reason") == "end_turn" and not result.get("escalated"), (
        f"a single blocked rejection with plenty of iteration budget remaining must let the session "
        f"continue to a normal end_turn, not escalate on the rejection alone; got {result}"
    )


def test_repeated_hook_rejections_eventually_escalate():
    """A model stuck repeatedly attempting a blocked process_refund makes no
    real progress. This project's own stated fail-closed design principle
    is that a blocked/ambiguous action escalates rather than silently
    running out the clock -- should_escalate's iteration-proximity signal
    must still fire on the rejection path, not only after an actual tool
    result. (Found via review, not one of this module's two seeded
    pedagogical defects -- a real gap that applies uniformly regardless of
    which of those two you've fixed.)"""
    extraction_client = ScriptedExtractionModelClient([high_confidence_extraction()])
    always_blocked_refund = {
        "stop_reason": "tool_use",
        "tool_name": "process_refund",
        "tool_args": {"customer_id": "cust_1", "order_id": "ORD-1", "amount_cents": 500},
    }
    agent_client = ScriptedAgentModelClient([always_blocked_refund, always_blocked_refund])
    calls: list = []
    result = run_full_support_session(
        "Refund my order", agent_client, extraction_client, make_tool_registry(calls), backend=None, max_iterations=2
    )
    assert calls == [], "process_refund must never actually execute -- it's blocked every time"
    assert len(agent_client.calls) == 2, (
        f"the first rejection alone (iterations_used=0 of max_iterations=2) must NOT escalate -- "
        f"escalating on the very first rejection regardless of iteration budget is a different, "
        f"over-eager bug, not the fix this test exists to check; expected the loop to consult the "
        f"model a 2nd time before escalating, got {len(agent_client.calls)} call(s)"
    )
    assert result.get("escalated") is True, (
        f"expected escalation once the iteration budget for repeated rejections runs out, got {result}"
    )


# ---------------------------------------------------------------------------
# Seeded defect 1: a low-confidence extraction must not, by itself, bypass
# the agentic loop and should_escalate's own contract (spans Modules 02 & 05)
# ---------------------------------------------------------------------------


def test_low_confidence_extraction_does_not_bypass_the_agent_loop():
    """extraction.confidence describes how confident the EXTRACTION step was
    in parsing the customer's message -- it is not, and must not become, an
    escalation signal in its own right. should_escalate (Module 05) is the
    *only* authority on escalation, and its own signature deliberately has
    no confidence parameter. A correct integration must let the agentic
    loop actually run even when extraction confidence is low."""
    extraction_client = ScriptedExtractionModelClient(
        [
            {
                "refund_amount_cents": None,
                "reason_category": "other",
                "reason_detail": "ambiguous message",
                "confidence": "low",
            }
        ]
    )
    agent_client = ScriptedAgentModelClient([{"stop_reason": "end_turn", "text": "Resolved directly."}])
    calls: list = []
    result = run_full_support_session(
        "uh, something's wrong with the thing I got", agent_client, extraction_client, make_tool_registry(calls), backend=None
    )
    assert len(agent_client.calls) >= 1, (
        "the agentic loop must actually run even when extraction confidence is low -- "
        "low extraction confidence is not itself grounds to skip the loop and escalate"
    )
    assert not result.get("escalated"), (
        f"a low-confidence extraction must not, on its own, escalate the session; got {result}"
    )
    assert result.get("stop_reason") == "end_turn"


# ---------------------------------------------------------------------------
# Seeded defect 2: should_escalate must see the CURRENT turn's tool result,
# not a stale pre-update CaseFacts (spans Modules 04 & 05)
# ---------------------------------------------------------------------------


def test_should_escalate_sees_the_current_turns_result_immediately():
    """A session whose third tool call fails (crossing should_escalate's
    error_count >= 3 threshold) must escalate on that same turn -- not one
    turn later, after a fourth model call that a correct implementation
    should never have needed to make."""
    extraction_client = ScriptedExtractionModelClient([high_confidence_extraction()])
    agent_client = ScriptedAgentModelClient(
        [
            {"stop_reason": "tool_use", "tool_name": "lookup_order", "tool_args": {"customer_id": "cust_1", "order_id": "ORD-1"}},
            {"stop_reason": "tool_use", "tool_name": "lookup_order", "tool_args": {"customer_id": "cust_1", "order_id": "ORD-2"}},
            {"stop_reason": "tool_use", "tool_name": "lookup_order", "tool_args": {"customer_id": "cust_1", "order_id": "ORD-3"}},
            # Deliberately no 4th scripted response: a correct implementation
            # must escalate immediately after the 3rd failed call and never
            # ask the model for a 4th turn.
        ]
    )
    calls: list = []
    error_result = {"error": True, "errorCategory": "business", "isRetryable": False, "message": "no such order"}
    responses = {"lookup_order": error_result}
    result = run_full_support_session(
        "Where are my orders?", agent_client, extraction_client, make_tool_registry(calls, responses), backend=None
    )
    assert result.get("escalated") is True, (
        f"expected escalation immediately after the 3rd failed tool call in the same turn, got {result}"
    )
    assert result["facts"].error_count == 3, (
        "the escalation decision and the returned facts must agree that all 3 errors were counted "
        "by the time escalation happened"
    )
    assert len(agent_client.calls) == 3, (
        f"a correct implementation escalates on the same turn as the 3rd failure and must not need "
        f"a 4th call to the model, got {len(agent_client.calls)} calls"
    )
