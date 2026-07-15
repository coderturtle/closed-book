"""The backend every Module 03 tool is injected with, mirroring Module 02's
`model_client` injection (see src/extraction.py) -- so the deterministic test
suite can supply fake backend data without a real database, and so the same
tool code will work unchanged once Module 04 wires a real backend in.

Real implementations query resolve's actual customer/order systems. The test
suite supplies a FakeBackend with scripted records.
"""
from __future__ import annotations

from typing import Optional, Protocol


class Backend(Protocol):
    def find_customer(self, identifier: str) -> Optional[dict]:
        """Return a customer record ({"customer_id": ..., "email": ...} or
        similar) if `identifier` matches a real customer, else None. Never
        raises for "not found" -- that's a valid, expected outcome, not an
        error condition."""
        ...

    def find_order(self, customer_id: str, order_id: str) -> Optional[dict]:
        """Return an order record ({"order_id": ..., "refundable_cents": ...}
        or similar) if `order_id` belongs to `customer_id`, else None --
        including when the order exists but belongs to a *different*
        customer (never leak that distinction; both cases return None)."""
        ...
