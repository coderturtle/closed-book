"""MCP tool: escalate_to_human. Authored for real in Module 03 (Tool & MCP Design).

Hands a case to a human agent with a structured summary (customer ID, root
cause, recommended action) — a human picking this up has no access to the
conversation transcript, so the summary has to carry everything.
"""


def escalate_to_human(customer_id: str, reason: str, summary: dict) -> dict:
    raise NotImplementedError("Module 03's exercise: implement this as a real MCP tool.")
