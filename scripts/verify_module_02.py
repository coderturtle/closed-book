#!/usr/bin/env python3
"""Deterministic tier for Module 02 (Prompts and Structured Output That
Survive Production).

Two things, chained: (1) Module 01's own checker, per the cumulative-gate
convention in fixtures/resolve/SPEC.md's compatibility contract -- a Module 02
submission that broke Module 01's already-passed configuration should fail
here, not slip through silently. (2) the real, provided pytest suite
(test_extraction.py) against the learner's own src/extraction.py.

Runs the *repo's own canonical copy* of test_extraction.py, not whatever
copy sits in the submitted target -- a doubt-driven-development review of
Module 03 found that running a submission's own test file lets a learner
weaken or delete it and pass trivially, since the "don't edit this" notice
at the top of the file is prose, not enforcement. Applies here too, found
and fixed the same day. See docs/decisions.md's 2026-07-15 entries.

Requires pytest. See fixtures/resolve/requirements.txt.

Usage: scripts/verify_module_02.py [path-to-attempt]
  Defaults to fixtures/resolve/ relative to the repo root.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_module_01 import CheckResult, check_module_01  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_TEST_FILE = REPO_ROOT / "fixtures" / "resolve" / "tests" / "test_extraction.py"


def run_extraction_tests(target: Path) -> tuple[bool, str]:
    """Run the repo's own canonical test_extraction.py (not the submission's
    copy) against the submission's src/, so a learner can't weaken the gate
    by editing the test file in their own attempt directory."""
    with tempfile.TemporaryDirectory() as tmp:
        test_copy = Path(tmp) / "test_extraction.py"
        shutil.copy(CANONICAL_TEST_FILE, test_copy)
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_copy), "-v"],
            cwd=target,  # so `from src.extraction import ...` resolves against the submission
            capture_output=True,
            text=True,
        )
        return result.returncode == 0, result.stdout + result.stderr


def check_module_02(target: Path) -> CheckResult:
    """Importable by later modules' checkers for cumulative-gate chaining
    (fixtures/resolve/SPEC.md's compatibility contract). Returns a single
    CheckResult: Module 01's findings (chained) plus this module's own
    pass/fail, with raw pytest text in `.output`.
    """
    m1 = check_module_01(target)
    if not m1.passed:
        return m1
    passed, output = run_extraction_tests(target)
    findings = list(m1.findings) + ["  Module 01's gate: PASS"]
    findings.append("  Module 02 test suite: PASS" if passed else "  Module 02 test suite: FAIL")
    return CheckResult(passed=passed, findings=findings, output=output)


def main(argv: list[str]) -> int:
    target = Path(argv[1]).resolve() if len(argv) > 1 else REPO_ROOT / "fixtures" / "resolve"

    print(f"=== Module 02 deterministic tier: {target} ===")
    print()
    result = check_module_02(target)
    for line in result.findings:
        print(line)
    if result.output:
        print()
        print(result.output)

    print()
    if result.passed:
        print("=== Deterministic tier: PASS ===")
        return 0
    print("=== Deterministic tier: FAIL ===")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
