---
paths: ["src/**"]
---

# Foundry source conventions

Every module's exercise files live directly under `src/` (no subdirectories,
unlike `resolve`'s `src/tools/`) — `ticket_triage.py`, `doc_qa.py`,
`evaluation.py`, `governance.py`, one file per module's own deliverable.

- Deterministic test doubles only (scripted/spy model clients) — never call
  a real model API from source code in this project.
- Every public function's docstring states its contract precisely enough
  that a learner could write the canonical test suite from the docstring
  alone, since that is effectively what happened during authoring.
- New modules chain the prior module's `check_module_NN` function for
  cumulative-gate validation — see `SPEC.md`'s compatibility contract.
