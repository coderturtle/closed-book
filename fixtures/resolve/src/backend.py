"""The backend every Module 03 tool is injected with, mirroring Module 02's
`model_client` injection (see src/extraction.py) -- so the deterministic test
suite can supply fake backend data without a real database, and so the same
tool code will work unchanged once Module 04 wires a real backend in.

Real implementations query resolve's actual customer/order systems. The test
suite supplies a FakeBackend with scripted records.

**Scope, stated explicitly:** this protocol is read-only (lookups only, no
mutation), and stays that way for the rest of this project. Module 03's
tools verify a refund *decision* -- is this customer real, does this order
belong to them, is the amount within what's refundable. `process_refund`'s
"success" response means "this refund decision was verified valid," not
"money has moved."

Module 04 does not extend this into a stateful, mutating backend. Its
exercise is orchestration -- the agentic loop and the session-level hook
that decides *whether* `process_refund` may be called at all -- not
refund persistence or idempotency against a double-submitted request.
Those are real production concerns, but they belong to Domain 2 (tool
design) territory this project already resolved in Module 03, not to
Domain 1 (agentic orchestration), which is what Module 04 teaches. See
`docs/decisions.md` for the record of this scope call.
"""
from __future__ import annotations

from typing import Optional, Protocol


class Backend(Protocol):
    def find_customer(self, identifier: str) -> Optional[dict]:
        """Return a customer record ({"customer_id": ..., "email": ...} or
        similar) if `identifier` matches a real customer, else None. Never
        raises for "not found" -- that's a valid, expected outcome, not an
        error condition.

        `identifier` is deliberately typed broadly: `get_customer` calls
        this with a raw email/phone/account-ID string (a customer not yet
        resolved), while `process_refund` calls it with an already-resolved
        `customer_id` (re-verifying a customer it's been told is real). A
        real implementation must accept both shapes -- `find_customer` is a
        general "does this identify a real customer" check, not specifically
        the first-contact lookup `get_customer` happens to use it for.
        """
        ...

    def find_order(self, customer_id: str, order_id: str) -> Optional[dict]:
        """Return an order record ({"order_id": ..., "refundable_cents": ...}
        or similar) if `order_id` belongs to `customer_id`, else None --
        including when the order exists but belongs to a *different*
        customer (never leak that distinction; both cases return None)."""
        ...
