"""MCP tool module: process_refund."""
from __future__ import annotations

from src.backend import Backend


def process_refund(customer_id: str, order_id: str, amount_cents: int, backend: Backend) -> dict:
    """Issue a refund against a specific order. This is the tool this whole
    project's canonical safety rule exists for (see fixtures/resolve/SPEC.md):
    never refund without a verified customer.

    Two separate layers enforce this, deliberately not one:
    - Module 04 (later) adds a session-level hook that blocks calling this
      tool at all unless its own customer_id matches the specific customer
      a get_customer call already succeeded for earlier in the same
      session -- enforcing not just *that* verification happened, but that
      it happened *for this customer*.
    - THIS tool's own job is different and narrower: it must independently
      re-verify customer_id against the backend before doing anything else
      -- defense in depth, so this tool is safe to call even if some future
      caller (or a bug in Module 04's hook) skips the session-level check.
      A customer_id that doesn't resolve via backend.find_customer must fail
      closed with a structured error, never proceed on a caller's word alone.

    Also validates: order_id belongs to customer_id, and amount_cents does
    not exceed the order's refundable_cents.
    """
    raise NotImplementedError("Module 03's exercise: implement this as a real MCP tool.")
