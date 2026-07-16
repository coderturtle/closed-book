"""Coordinator agent for resolve."""
from __future__ import annotations

from typing import Callable, List, Optional

AgentModelClient = Callable[[List[dict]], dict]
ToolRegistry = dict


class SessionState:
    """Session state."""

    def __init__(self) -> None:
        self.tool_calls_made: List[str] = []
        self.verified_customer_id: Optional[str] = None


def verify_before_refund_hook(tool_name: str, tool_args: dict, session: SessionState) -> Optional[str]:
    """Blocks process_refund if the right customer hasn't been verified."""
    if tool_name != "process_refund":
        return None
    if session.verified_customer_id is None:
        return "Error: call get_customer first."
    if tool_args.get("customer_id") != session.verified_customer_id:
        return "Error: customer_id does not match get_customer's result."
    return None


def run_support_session(
    customer_message: str,
    model_client: AgentModelClient,
    tools: ToolRegistry,
    backend,
    max_iterations: int = 10,
) -> dict:
    """Runs the loop."""
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
