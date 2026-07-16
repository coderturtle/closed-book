"""MCP tool module: lookup_order."""
from __future__ import annotations

from src.backend import Backend


def lookup_order(customer_id: str, order_id: str, backend: Backend) -> dict:
    """Look up an order by order_id, scoped to a customer_id already obtained
    from get_customer -- never call this with a bare order_id and no
    customer_id. If order_id exists but belongs to a *different* customer,
    this returns "not found," not an error naming the mismatch -- never
    confirm to a caller that an order_id is valid for someone else's account.

    Boundary vs. get_customer: get_customer resolves a *person* from an
    email/phone/account-ID; lookup_order resolves an *order* the caller
    already knows belongs to that person.
    """
    from src.tool_errors import tool_error

    record = backend.find_order(customer_id, order_id)
    if record is None:
        # Same message whether order_id doesn't exist at all or belongs to a
        # different customer -- never confirm which case it was.
        return tool_error("business", f"no order {order_id!r} found for this customer", False)
    return {**record}
