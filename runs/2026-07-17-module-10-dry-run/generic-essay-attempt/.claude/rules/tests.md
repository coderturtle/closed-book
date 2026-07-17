---
paths: ["tests/**"]
---

# Foundry test conventions

Every `tests/test_*.py` file here is a canonical gate, not a learner
scratch file — `scripts/verify_module_NN.py` always runs the repo's own
copy in an isolated temp directory, never the submission's copy, so editing
these files to make a submission pass does nothing against the real gate.

- Test doubles are keyed by call content (query text, or full context), not
  call order, so tests can assert real behavior regardless of internal
  call sequencing.
- Every test that checks a default parameter value omits that parameter
  explicitly, rather than passing it — a default that's never actually
  exercised is not verified.
