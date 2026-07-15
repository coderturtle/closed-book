# resolve

A customer support resolution agent. Handles returns, billing disputes, and account issues via Claude, backed by MCP tools against backend systems.

## Safety rule

Never call `process_refund` before `get_customer` has returned a verified customer ID.

## Tool conventions (src/tools/)

Every tool in `src/tools/` should return a structured result, not raise a bare exception. Include an `errorCategory` field (`transient`/`validation`/`business`/`permission`) and an `isRetryable` boolean on any failure.

## Testing conventions (tests/)

Every tool needs a corresponding test file in `tests/`. Use pytest. Cover at least one success case and one structured-error case per tool.
