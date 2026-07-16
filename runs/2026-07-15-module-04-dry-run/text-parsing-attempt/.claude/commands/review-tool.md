---
argument-hint: [tool-file]
---

Review $1 against `.claude/rules/tools.md`'s conventions. Check specifically: does it return a structured error (`errorCategory`, `isRetryable`) on every failure path, not a bare exception? If this is `process_refund.py`, does it require a verified customer ID before proceeding? Report findings as a short checklist, not prose.
