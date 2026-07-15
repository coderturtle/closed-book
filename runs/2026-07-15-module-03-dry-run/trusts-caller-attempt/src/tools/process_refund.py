"""MCP tool module: process_refund."""
from __future__ import annotations

from src.backend import Backend


def process_refund(customer_id: str, order_id: str, amount_cents: int, backend: Backend) -> dict:
    """Issue a refund against a specific order. This is the tool this whole
    project's canonical safety rule exists for (see fixtures/resolve/SPEC.md):
    never refund without a verified customer.

    Two separate layers enforce this, deliberately not one:
    - Module 04 (later) adds a conversation-level hook that blocks calling
      this tool at all until get_customer has actually run earlier in the
      same session -- enforcing the *order* tool calls happen in.
    - THIS tool's own job is different and narrower: it must independently
      re-verify customer_id against the backend before doing anything else
      -- defense in depth, so this tool is safe to call even if some future
      caller (or a bug in Module 04's hook) skips the session-level check.
      A customer_id that doesn't resolve via backend.find_customer must fail
      closed with a structured error, never proceed on a caller's word alone.

    Also validates: order_id belongs to customer_id, and amount_cents does
    not exceed the order's refundable_cents.
    """
    from src.tool_errors import tool_error

    # Trusts the caller-supplied customer_id without re-verifying it against
    # the backend -- reasoning "Module 04's hook already checks this before
    # the tool is even called, so checking again here is redundant." A real,
    # plausible mistake: it's true for the *intended* call path, but this
    # tool has no way to know it was actually reached through that path.
    order = backend.find_order(customer_id, order_id)
    if order is None:
        return tool_error("business", f"no order {order_id!r} found for this customer", False)
    if amount_cents <= 0:
        return tool_error("validation", "amount_cents must be positive", False)
    if amount_cents > order["refundable_cents"]:
        return tool_error(
            "validation",
            f"amount_cents {amount_cents} exceeds refundable {order['refundable_cents']}",
            False,
        )
    return {"refunded_cents": amount_cents, "order_id": order_id}
