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

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_module_01 import CheckResult, check_module_01  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_TEST_FILE = REPO_ROOT / "fixtures" / "resolve" / "tests" / "test_extraction.py"


def _expected_test_count() -> int:
    return len(re.findall(r"(?m)^def test_", CANONICAL_TEST_FILE.read_text()))


def run_extraction_tests(target: Path) -> tuple[bool, str]:
    """Run the repo's own canonical test_extraction.py (not the submission's
    copy) against the submission's src/, so a learner can't weaken the gate
    by editing the test file in their own attempt directory. Copies src/ into
    a fresh, neutral temp dir and runs pytest with cwd set to THAT dir --
    never cwd=target, which would put the submission's own top-level
    directory at the front of sys.path and let a shadow `pytest.py` bypass
    the real pytest package entirely.

    A zero exit code alone isn't sufficient evidence the suite actually ran:
    submission code executes during pytest's own collection, so a submission
    calling `os._exit(0)` at import time kills the subprocess with return
    code 0 before a single test runs. Fixed by additionally requiring the
    pytest summary itself report the full expected test count passed. See
    docs/decisions.md's 2026-07-17 entry (found via Module 07's doubt-driven-
    development and a Fable-model critique of that remediation, fixed in all
    six checkers at once)."""
    submission_src = target / "src"
    if not submission_src.is_dir():
        return False, f"FAIL: no src/ directory found in the submission at {target}"
    expected = _expected_test_count()
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        test_copy = tmp_path / "test_extraction.py"
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
