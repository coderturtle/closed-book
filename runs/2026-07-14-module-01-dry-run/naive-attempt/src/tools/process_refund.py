"""MCP tool: process_refund. Authored for real in Module 03 (Tool & MCP Design).

Issues a refund against a verified order. This is the tool this whole
project's safe-design default (docs/workshop-design.md) exists for: it must
never be callable before get_customer has returned a verified customer ID —
the exam guide's own Sample Question 1 is this exact scenario.
"""


def process_refund(customer_id: str, order_id: str, amount_cents: int) -> dict:
    raise NotImplementedError("Module 03's exercise: implement this as a real MCP tool.")
