"""MCP tool module: get_customer."""
from __future__ import annotations

from src.backend import Backend


def get_customer(identifier: str, backend: Backend) -> dict:
    """Gets a customer. Takes an identifier which could be an email, phone,
    or account thing. Not for orders, use lookup_order for that."""
    from src.tool_errors import tool_error

    record = backend.find_customer(identifier)
    if record is None:
        return tool_error("business", f"no customer found for identifier {identifier!r}", False)
    return {"customer_id": record["customer_id"], **record}
