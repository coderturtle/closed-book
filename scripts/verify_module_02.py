#!/usr/bin/env python3
"""Deterministic tier for Module 02 (Prompts and Structured Output That
Survive Production).

Two things, chained: (1) Module 01's own checker, per the cumulative-gate
convention in fixtures/resolve/SPEC.md's compatibility contract -- a Module 02
submission that broke Module 01's already-passed configuration should fail
here, not slip through silently. (2) the real, provided pytest suite
(tests/test_extraction.py) against the learner's own src/extraction.py.

Requires pytest. See fixtures/resolve/requirements.txt.

Usage: scripts/verify_module_02.py [path-to-attempt]
  Defaults to fixtures/resolve/ relative to the repo root.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_module_01 import CheckResult, check_module_01  # noqa: E402


def run_extraction_tests(target: Path) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_extraction.py", "-v"],
        cwd=target,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0, result.stdout + result.stderr


def check_module_02(target: Path) -> tuple[CheckResult, str]:
    """Importable by later modules' checkers for cumulative-gate chaining
    (fixtures/resolve/SPEC.md's compatibility contract). Returns Module 01's
    CheckResult (chained) and the raw pytest output for tests/test_extraction.py
    -- callers that only need pass/fail should check `result.passed and
    "passed" appears via the returned pytest output`, but the simplest
    correct check is calling this module's own `main()` exit code; this
    function exists so a later module can chain the *result*, not just the
    process exit code.
    """
    m1 = check_module_01(target)
    if not m1.passed:
        return m1, ""
    passed, output = run_extraction_tests(target)
    result = CheckResult(passed=passed, findings=list(m1.findings))
    return result, output


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parent.parent
    target = Path(argv[1]).resolve() if len(argv) > 1 else root / "fixtures" / "resolve"

    print(f"=== Module 02 deterministic tier: {target} ===")
    print()
    print("-- Cumulative gate: Module 01's checker --")
    m1 = check_module_01(target)
    for line in m1.findings:
        print(line)
    if not m1.passed:
        print()
        print("=== Deterministic tier: FAIL (Module 01's gate did not pass -- ")
        print("    fix that before this submission can be evaluated for Module 02) ===")
        return 1
    print("  Module 01's gate: PASS")

    print()
    print("-- Module 02: extraction test suite (tests/test_extraction.py) --")
    passed, output = run_extraction_tests(target)
    print(output)

    print()
    if passed:
        print("=== Deterministic tier: PASS ===")
        return 0
    print("=== Deterministic tier: FAIL ===")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
