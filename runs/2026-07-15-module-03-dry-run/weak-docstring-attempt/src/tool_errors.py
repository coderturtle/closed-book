"""Shared structured-error shape for every Module 03 tool (Task Statement 2.2).

One consistent taxonomy across all four tools, not an ad hoc shape per tool --
an agent handling a tool failure needs to make the same category of decision
(retry? explain to the customer? escalate?) regardless of which tool failed.

Category semantics, so a category choice is derivable from the definition
rather than reverse-engineered from a hidden test:

- **transient** -- the request might succeed if retried unchanged (a network
  timeout, a momentary backend outage). isRetryable is normally True.
- **validation** -- the request as given cannot be honored *as stated*: a
  malformed or out-of-range input (a non-positive amount, an amount that
  exceeds what's actually refundable on this order, a required field
  missing). The caller would need to change *what it's asking for*, not just
  retry the same request. isRetryable is normally False.
- **business** -- the request is well-formed but the thing it refers to
  doesn't exist or doesn't relate the way the caller assumed (no customer
  matches this identifier, no order matches this order_id for this
  customer). isRetryable is normally False.
- **permission** -- the request is well-formed and refers to something real,
  but the caller hasn't established the right to act on it (a customer_id
  that was never verified via get_customer). isRetryable is normally False.
"""
from __future__ import annotations

ERROR_CATEGORIES = ("transient", "validation", "business", "permission")


def tool_error(category: str, message: str, is_retryable: bool) -> dict:
    if category not in ERROR_CATEGORIES:
        raise ValueError(f"category must be one of {ERROR_CATEGORIES}, got {category!r}")
    return {
        "error": True,
        "errorCategory": category,
        "isRetryable": is_retryable,
        "message": message,
    }
