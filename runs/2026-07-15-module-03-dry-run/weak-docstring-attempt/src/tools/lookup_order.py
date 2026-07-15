"""MCP tool module: lookup_order."""
from __future__ import annotations

from src.backend import Backend


def lookup_order(customer_id: str, order_id: str, backend: Backend) -> dict:
    """Gets an order. Needs a customer_id and an order id. See get_customer
    for customer lookups."""
    from src.tool_errors import tool_error

    record = backend.find_order(customer_id, order_id)
    if record is None:
        # Same message whether order_id doesn't exist at all or belongs to a
        # different customer -- never confirm which case it was.
        return tool_error("business", f"no order {order_id!r} found for this customer", False)
    return {**record}
