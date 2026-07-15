"""Shared structured-error shape for every Module 03 tool (Task Statement 2.2).

One consistent taxonomy across all four tools, not an ad hoc shape per tool --
an agent handling a tool failure needs to make the same category of decision
(retry? explain to the customer? escalate?) regardless of which tool failed.
"""
from __future__ import annotations

ERROR_CATEGORIES = ["transient", "validation", "business", "permission"]


def tool_error(category: str, message: str, is_retryable: bool) -> dict:
    if category not in ERROR_CATEGORIES:
        raise ValueError(f"category must be one of {ERROR_CATEGORIES}, got {category!r}")
    return {
        "error": True,
        "errorCategory": category,
        "isRetryable": is_retryable,
        "message": message,
    }
