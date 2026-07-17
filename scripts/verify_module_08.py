#!/usr/bin/env python3
"""Deterministic tier for Module 08 (Building and Proving It: Integration,
Evaluation & Optimization).

Chains `check_module_07` (Foundry's own first gate), per the Part 2
compatibility contract stated in `fixtures/foundry/SPEC.md` -- Part 2
checkers chain within Part 2 only, never back into Part 1's `check_module_06`.

One canonical test file, `tests/test_doc_qa.py`, run against the repo's own
canonical copy (never the submission's), covering two real deliverables in
one gate: (1) a diagnose-and-fix defect in `src/doc_qa.py`'s
`refresh_index` (a seeded stale-retrieval bug, matching the exam guide's own
Sample 3 anchor); (2) a build-from-stub evaluation harness in
`src/evaluation.py` (`evaluate`/`compare_top_k`).

Test execution isolates the submission's `src/` into a fresh, neutral temp
directory (never `cwd=target`) and requires the pytest summary itself report
the full expected test count passed, not just a zero exit code -- both
mitigations applied here from the start, not discovered via review, per the
project-wide checker-bypass finding from Module 07's own doubt-driven-
development. See docs/decisions.md's 2026-07-17 entries.

Usage: scripts/verify_module_08.py [path-to-attempt]
  Defaults to fixtures/foundry/ relative to the repo root.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_module_07 import check_module_07  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_TEST_FILE = REPO_ROOT / "fixtures" / "foundry" / "tests" / "test_doc_qa.py"


@dataclass
class CheckResult:
    passed: bool
    findings: list[str] = field(default_factory=list)
    output: str = ""


def _expected_test_count() -> int:
    return len(re.findall(r"(?m)^def test_", CANONICAL_TEST_FILE.read_text()))


def run_doc_qa_tests(target: Path) -> tuple[bool, str]:
    """Copies the submission's src/ into a fresh, neutral temp dir alongside
    the canonical test file, and runs pytest with cwd set to THAT dir --
    never cwd=target (would let a submission's own top-level file shadow the
    real pytest package). Also requires the pytest summary itself report the
    full expected test count passed, not just a zero exit code (guards
    against submission code force-exiting the subprocess during collection,
    e.g. `os._exit(0)`)."""
    submission_src = target / "src"
    if not submission_src.is_dir():
        return False, f"FAIL: no src/ directory found in the submission at {target}"
    expected = _expected_test_count()
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        test_copy = tmp_path / "test_doc_qa.py"
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


def check_module_08(target: Path) -> CheckResult:
    """Importable by Module 09's checker for cumulative-gate chaining."""
    m7 = check_module_07(target)
    test_passed, test_output = run_doc_qa_tests(target)

    findings = list(m7.findings)
    findings.append("  Module 07's gate: PASS" if m7.passed else "  Module 07's gate: FAIL")
    findings.append("  Module 08 test suite: PASS" if test_passed else "  Module 08 test suite: FAIL")

    return CheckResult(passed=m7.passed and test_passed, findings=findings, output=test_output)


def main(argv: list[str]) -> int:
    target = Path(argv[1]).resolve() if len(argv) > 1 else REPO_ROOT / "fixtures" / "foundry"

    print(f"=== Module 08 deterministic tier: {target} ===")
    print()
    result = check_module_08(target)
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
