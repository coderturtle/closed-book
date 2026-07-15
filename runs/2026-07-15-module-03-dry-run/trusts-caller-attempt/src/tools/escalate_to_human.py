"""MCP tool module: escalate_to_human."""
from __future__ import annotations

from src.backend import Backend


def escalate_to_human(customer_id: str, reason: str, summary: dict, backend: Backend) -> dict:
    """Hand a case to a human agent with a structured summary. A human
    picking this up has no access to the conversation transcript, so
    `summary` must carry everything: it's required to include "root_cause"
    and "recommended_action" keys (both non-empty strings) -- a summary
    missing either is a validation error, not a best-effort handoff, since a
    human with half the picture makes a worse decision than one who was
    never assigned the case at all.
    """
    from src.tool_errors import tool_error

    if not summary.get("root_cause"):
        return tool_error("validation", "summary.root_cause is required and must be non-empty", False)
    if not summary.get("recommended_action"):
        return tool_error(
            "validation", "summary.recommended_action is required and must be non-empty", False
        )
    return {"escalated": True, "customer_id": customer_id, "reason": reason}
