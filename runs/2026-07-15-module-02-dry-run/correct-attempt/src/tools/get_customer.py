"""MCP tool: get_customer. Authored for real in Module 03 (Tool & MCP Design).

Looks up a customer by an identifier the caller provides (email, phone, or
account ID). Returns a verified customer record or a structured "not found"
result — never a bare exception a calling agent has to guess about.
"""


def get_customer(identifier: str) -> dict:
    raise NotImplementedError("Module 03's exercise: implement this as a real MCP tool.")
