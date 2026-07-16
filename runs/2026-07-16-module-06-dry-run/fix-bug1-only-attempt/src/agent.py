"""The coordinator agent. Authored for real in Module 04 (Agentic Loops and
Multi-Agent Orchestration). This is the module every earlier module in this
project's arc was building toward: a real agentic loop that calls
get_customer, lookup_order, process_refund, and escalate_to_human, with a
programmatic hook enforcing verify-before-refund at the *session* level --
distinct from, and layered on top of, Module 03's own tool-level defense in
depth (see process_refund's own docstring for why both layers exist).

Requires Python 3.9+ (see fixtures/resolve/src/extraction.py's note on why).
"""
from __future__ import annotations

from typing import Callable, List, Optional

AgentModelClient = Callable[[List[dict]], dict]
ToolRegistry = dict


class SessionState:
    """Tracks what's happened in this session so a hook can make a real
    decision instead of trusting the model's own claim about what it
    already did. Deliberately minimal -- this is not conversation memory,
    it's just enough state for the one hook this module implements.

    `verified_customer_id` -- not just *whether* `get_customer` succeeded,
    but *which* customer it verified. A session that verifies customer A
    must not be treated as having verified customer B. A second successful
    `get_customer` call for a different customer overwrites this value
    (last-verified-wins) -- a session holds at most one verified customer
    at a time.
    """

    def __init__(self) -> None:
        self.tool_calls_made: List[str] = []
        self.verified_customer_id: Optional[str] = None


def verify_before_refund_hook(tool_name: str, tool_args: dict, session: SessionState) -> Optional[str]:
    """A programmatic hook (Task Statement 1.5), not a prompt instruction:
    intercepts every tool call before it executes and returns a rejection
    message if the call should be blocked, or None to let it proceed.

    The rule this hook enforces: `process_refund`'s `customer_id` argument
    must match `session.verified_customer_id` -- the customer a `get_customer`
    call already succeeded for, earlier in this same session. This is the
    *session-level* enforcement Module 03's own `process_refund` docstring
    names as the layer above its own tool-level re-verification -- two
    layers, deliberately not one (see that docstring for why neither
    replaces the other). `escalate_to_human` is never blocked by this hook
    -- it's this project's fail-open path (see its own docstring).
    """
    if tool_name != "process_refund":
        return None
    if session.verified_customer_id is None:
        return (
            "process_refund blocked: this session has no successful get_customer call yet. "
            "Call get_customer to verify the customer's identity before requesting a refund."
        )
    if tool_args.get("customer_id") != session.verified_customer_id:
        return (
            "process_refund blocked: customer_id does not match the customer this session "
            "verified via get_customer. Call get_customer for this specific customer before "
            "requesting a refund on their behalf."
        )
    return None


def run_support_session(
    customer_message: str,
    model_client: AgentModelClient,
    tools: ToolRegistry,
    backend,
    max_iterations: int = 10,
) -> dict:
    """The agentic loop. Send the growing conversation to `model_client`;
    while the response's `stop_reason` is "tool_use", run
    `verify_before_refund_hook` first -- if it returns a rejection, feed
    that rejection back to the model as the tool's result (never execute
    the tool), otherwise execute the real tool via `tools` and feed back
    its actual result; append every tool call and result to the
    conversation history so the next turn has full context. Stop when
    `stop_reason` is "end_turn", returning the final text. `max_iterations`
    is a safety backstop, not the primary stopping mechanism -- hitting it
    returns `{"stop_reason": "max_iterations", ...}`, a distinguishable,
    reportable failure, not a value that could be mistaken for a normal
    `end_turn` completion.

    Dispatch every tool call as `tools[tool_name](**tool_args,
    backend=backend)` -- always pass `backend` explicitly by keyword.
    """
    history: List[dict] = [{"role": "user", "content": customer_message}]
    session = SessionState()

    for _ in range(max_iterations):
        response = model_client(history)
        stop_reason = response.get("stop_reason")

        if stop_reason == "end_turn":
            return {"stop_reason": "end_turn", "text": response.get("text", "")}

        if stop_reason != "tool_use":
            raise ValueError(f"unrecognized stop_reason: {stop_reason!r}")

        tool_name = response["tool_name"]
        tool_args = response["tool_args"]
        history.append({"role": "assistant", "tool_use": {"tool_name": tool_name, "tool_args": tool_args}})

        rejection = verify_before_refund_hook(tool_name, tool_args, session)
        if rejection is not None:
            history.append({"role": "tool_result", "tool_name": tool_name, "content": rejection})
            continue

        result = tools[tool_name](**tool_args, backend=backend)
        if not result.get("error"):
            session.tool_calls_made.append(tool_name)
            if tool_name == "get_customer":
                session.verified_customer_id = result.get("customer_id")
        history.append({"role": "tool_result", "tool_name": tool_name, "content": result})

    return {"stop_reason": "max_iterations", "text": "", "history": history}
