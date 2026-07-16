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

# The model client for the agent loop: (conversation_history) -> a response
# dict shaped like a real Claude API turn. Two possible shapes, distinguished
# by `stop_reason` -- never by inspecting `text` content, which is the
# documented anti-pattern (Task Statement 1.1's own "Skills in" bullet):
#   {"stop_reason": "tool_use", "tool_name": str, "tool_args": dict}
#   {"stop_reason": "end_turn", "text": str}
AgentModelClient = Callable[[List[dict]], dict]

# tools: {"get_customer": get_customer, "lookup_order": lookup_order,
#         "process_refund": process_refund, "escalate_to_human": escalate_to_human}
# -- each already-implemented from Module 03, called here as
# tools[tool_name](**tool_args, backend=backend).
ToolRegistry = dict


class SessionState:
    """Tracks what's happened in this session so a hook can make a real
    decision instead of trusting the model's own claim about what it
    already did. Deliberately minimal -- this is not conversation memory,
    it's just enough state for the one hook this module implements.

    `verified_customer_id` -- not just *whether* `get_customer` succeeded,
    but *which* customer it verified. A session that verifies customer A
    must not be treated as having verified customer B: the hook's job is
    to bind a specific successful `get_customer` result to the specific
    `customer_id` a later `process_refund` call names, not merely to check
    that *some* `get_customer` call succeeded at some point. A second
    successful `get_customer` call for a different customer overwrites
    this value (last-verified-wins) -- a session holds at most one verified
    customer at a time, deliberately, not a set of every customer ever
    verified in it.
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
    call already succeeded for, earlier in this same session. Blocking on
    "some get_customer call succeeded" without checking *which* customer it
    verified is not sufficient: a session that verifies customer A must not
    be treated as license to refund customer B. This is the *session-level*
    enforcement Module 03's own `process_refund` docstring names as the
    layer above its own tool-level re-verification -- two layers,
    deliberately not one (see that docstring for why neither replaces the
    other). `escalate_to_human` is never blocked by this hook -- it's this
    project's fail-open path (see its own docstring).
    """
    raise NotImplementedError("Module 04's exercise: implement the hook's decision logic.")


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
    is a safety backstop, not the primary stopping mechanism -- the loop is
    expected to terminate via `stop_reason` well before that limit in every
    real scenario; hitting it must return `{"stop_reason": "max_iterations",
    ...}` -- a distinguishable, reportable failure, not a value that could
    be mistaken for a normal `end_turn` completion or a silent truncation.

    Dispatch every tool call as `tools[tool_name](**tool_args,
    backend=backend)` -- always pass `backend` explicitly by keyword, since
    the real Module 03 tools require it (a call missing it would fail
    against the real tools even if a test double happens to tolerate it).
    """
    raise NotImplementedError("Module 04's exercise: implement the agentic loop.")
