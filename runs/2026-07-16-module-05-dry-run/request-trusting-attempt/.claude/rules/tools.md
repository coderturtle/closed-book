---
paths: ["src/tools/**/*"]
---

# Tool conventions

Every tool in this directory returns a structured result, not a bare exception. Include an `errorCategory` field (`transient`/`validation`/`business`/`permission`) and an `isRetryable` boolean on any failure. `process_refund` must not be callable without a verified customer ID already in hand — enforce this with a hook, not a comment.
