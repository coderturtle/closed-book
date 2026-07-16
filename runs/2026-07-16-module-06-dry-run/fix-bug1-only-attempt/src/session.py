"""Module 06 (Foundations Capstone) exercise: a full integration of
Modules 02, 04, and 05 into one support session, standing in for the real
CCA-F skill of diagnosing a production defect that spans domains rather
than living in one isolated function.

`run_full_support_session` is NOT a stub -- it's fully written and runs.
It also contains two real, seeded defects, each spanning a different pair
of this project's prior modules. Nothing here raises NotImplementedError;
`scripts/verify_module_06.py`'s provided test suite already fails against
this file exactly as shipped. The exercise is to diagnose each failure's
actual root cause and fix it -- not to rewrite the function from scratch,
and not to make the tests pass by weakening what they check (see the
module README's rubric on that distinction).

This file intentionally does not say which lines are the bugs. Reasoning
about *why* a test fails, from the fixture project's own prior-module
docstrings and this file's structure, is Domain 1/4/5 diagnostic work in
miniature -- not a fact to be told upfront.

A third, real gap (found via review, not one of the two pedagogical
defects above) is already fixed here: a hook rejection on its own used to
`continue` straight to the next turn without ever consulting
`should_escalate`, so a model stuck repeatedly attempting a blocked
`process_refund` made no real progress yet never escalated -- silently
running to `max_iterations` instead. That contradicts this project's own
fail-closed default (a blocked/ambiguous action should escalate, not run
out the clock in silence), so it's corrected in the loop below rather
than left as a third thing for a learner to diagnose.
"""
from __future__ import annotations

from typing import Callable, List, Optional

from src.agent import SessionState, verify_before_refund_hook
from src.context import CaseFacts, should_escalate, update_case_facts
from src.extraction import ExtractionFailed, ModelClient as ExtractionModelClient, extract_refund_request

AgentModelClient = Callable[[List[dict]], dict]
ToolRegistry = dict


def run_full_support_session(
    customer_message: str,
    agent_model_client: AgentModelClient,
    extraction_model_client: ExtractionModelClient,
    tools: ToolRegistry,
    backend,
    max_iterations: int = 10,
) -> dict:
    """Run one full support session: extract structured intent from the
    customer's opening message (Module 02), then run the agentic loop
    (Module 04) with case-fact tracking and escalation (Module 05)
    threaded through every turn.

    Two separate model clients are injected deliberately, not merged into
    one -- `extraction_model_client` is Module 02's `(prompt, prior_attempts)
    -> dict` shape; `agent_model_client` is Module 04's `(conversation_history)
    -> dict` shape. They are not interchangeable, and a correct fix does not
    collapse them into one.
    """
    facts = CaseFacts()
    session = SessionState()

    try:
        extraction = extract_refund_request(customer_message, extraction_model_client)
    except ExtractionFailed:
        extraction = None

    history: List[dict] = [{"role": "user", "content": customer_message}]

    for i in range(max_iterations):
        response = agent_model_client(history)
        stop_reason = response.get("stop_reason")

        if stop_reason == "end_turn":
            return {"stop_reason": "end_turn", "text": response.get("text", ""), "facts": facts}

        if stop_reason != "tool_use":
            raise ValueError(f"unrecognized stop_reason: {stop_reason!r}")

        tool_name = response["tool_name"]
        tool_args = response["tool_args"]
        history.append({"role": "assistant", "tool_use": {"tool_name": tool_name, "tool_args": tool_args}})

        rejection = verify_before_refund_hook(tool_name, tool_args, session)
        if rejection is not None:
            history.append({"role": "tool_result", "tool_name": tool_name, "content": rejection})
            escalation_reason = should_escalate(facts, iterations_used=i, max_iterations=max_iterations)
            if escalation_reason is not None:
                return {"escalated": True, "reason": escalation_reason, "facts": facts, "extraction": extraction}
            continue

        result = tools[tool_name](**tool_args, backend=backend)
        if not result.get("error"):
            session.tool_calls_made.append(tool_name)
            if tool_name == "get_customer":
                session.verified_customer_id = result.get("customer_id")
        history.append({"role": "tool_result", "tool_name": tool_name, "content": result})

        reason = should_escalate(facts, iterations_used=i, max_iterations=max_iterations)
        facts = update_case_facts(facts, tool_name, tool_args, result)
        if reason is not None:
            return {"escalated": True, "reason": reason, "facts": facts}

    return {"stop_reason": "max_iterations", "text": "", "facts": facts}
