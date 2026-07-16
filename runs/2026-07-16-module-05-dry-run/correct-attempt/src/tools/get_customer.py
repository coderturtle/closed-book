"""MCP tool module: get_customer."""
from __future__ import annotations

from src.backend import Backend


def get_customer(identifier: str, backend: Backend) -> dict:
    """Look up a customer by identifier. Accepted formats: email address,
    phone number, or account ID (a string starting with "acct_") -- never
    an order ID. Returns a verified customer record, or a structured
    "not found" result -- never a bare exception a calling agent has to
    guess about.

    Boundary vs. lookup_order: get_customer's identifier is about the
    *person* (email/phone/account ID); lookup_order's identifiers are about
    the person's *order* (customer_id + a separate order_id). An agent with
    a bare order-looking string ("ORD-4821") should call lookup_order, not
    this tool.
    """
    from src.tool_errors import tool_error

    record = backend.find_customer(identifier)
    if record is None:
        return tool_error("business", f"no customer found for identifier {identifier!r}", False)
    return {"customer_id": record["customer_id"], **record}
