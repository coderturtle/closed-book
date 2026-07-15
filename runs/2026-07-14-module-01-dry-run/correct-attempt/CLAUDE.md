# resolve

A customer support resolution agent. Handles returns, billing disputes, and account issues via Claude, backed by MCP tools against backend systems.

## Safety rule

Never call `process_refund` before `get_customer` has returned a verified customer ID.

See `.claude/rules/tools.md` for tool-specific conventions and `.claude/rules/tests.md` for testing conventions — split out because they apply to files spread across this project, not one directory, and only when a matching file is actually being edited.
