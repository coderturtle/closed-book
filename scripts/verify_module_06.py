#!/usr/bin/env python3
"""Deterministic tier for Module 06 (Foundations Capstone).

Chains Module 05's check (which itself chains Module 04's, Module 03's,
Module 02's, Module 01's), per the cumulative-gate convention in
fixtures/resolve/SPEC.md's compatibility contract, then runs the repo's own
canonical tests/test_session.py (not the submission's copy -- see
verify_module_02.py's module docstring for why) against
run_full_support_session in src/session.py.

Unlike every earlier module's checker, a passing Module 01-05 gate does NOT
imply this file starts green: src/session.py ships with two real, seeded
defects, and this suite is written to fail against it exactly as shipped.

Usage: scripts/verify_module_06.py [path-to-attempt]
  Defaults to fixtures/resolve/ relative to the repo root.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_module_05 import check_module_05  # noqa: E402
from verify_module_01 import CheckResult  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_TEST_FILE = REPO_ROOT / "fixtures" / "resolve" / "tests" / "test_session.py"


def _expected_test_count() -> int:
    return len(re.findall(r"(?m)^def test_", CANONICAL_TEST_FILE.read_text()))


def run_session_tests(target: Path) -> tuple[bool, str]:
    """Copies src/ into a fresh, neutral temp dir and runs pytest with cwd set
    to THAT dir -- never cwd=target, which would put the submission's own
    top-level directory at the front of sys.path and let a shadow `pytest.py`
    bypass the real pytest package entirely. A zero exit code alone isn't
    sufficient evidence the suite actually ran (submission code executes
    during pytest's own collection, so `os._exit(0)` at import time kills the
    subprocess with return code 0 before any test runs) -- also requires the
    pytest summary itself report the full expected test count passed. See
    docs/decisions.md's 2026-07-17 entry (found via Module 07's doubt-driven-
    development and a Fable-model critique of that remediation, fixed across
    all six checkers at once)."""
    submission_src = target / "src"
    if not submission_src.is_dir():
        return False, f"FAIL: no src/ directory found in the submission at {target}"
    expected = _expected_test_count()
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        test_copy = tmp_path / "test_session.py"
        shutil.copy(CANONICAL_TEST_FILE, test_copy)
        shutil.copytree(submission_src, tmp_path / "src")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_copy), "-v"],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )
        output = result.stdout + result.stderr
        passed = result.returncode == 0 and f"{expected} passed" in output
        return passed, output


def check_module_06(target: Path) -> CheckResult:
    """Importable by a future module's checker for cumulative-gate chaining."""
    m5 = check_module_05(target)
    if not m5.passed:
        return m5
    passed, output = run_session_tests(target)
    findings = list(m5.findings)
    findings.append("  Module 06 test suite: PASS" if passed else "  Module 06 test suite: FAIL")
    return CheckResult(passed=passed, findings=findings, output=output)


def main(argv: list[str]) -> int:
    target = Path(argv[1]).resolve() if len(argv) > 1 else REPO_ROOT / "fixtures" / "resolve"

    print(f"=== Module 06 deterministic tier: {target} ===")
    print()
    result = check_module_06(target)
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
