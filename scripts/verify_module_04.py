#!/usr/bin/env python3
"""Deterministic tier for Module 04 (Agentic Loops and Multi-Agent Orchestration).

Chains Module 03's check (which itself chains Module 02's, which chains
Module 01's), per the cumulative-gate convention in fixtures/resolve/SPEC.md's
compatibility contract, then runs the repo's own canonical tests/test_agent.py
(not the submission's copy -- see verify_module_02.py's module docstring for
why) against run_support_session and verify_before_refund_hook in src/agent.py.

Usage: scripts/verify_module_04.py [path-to-attempt]
  Defaults to fixtures/resolve/ relative to the repo root.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_module_03 import check_module_03  # noqa: E402
from verify_module_01 import CheckResult  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_TEST_FILE = REPO_ROOT / "fixtures" / "resolve" / "tests" / "test_agent.py"


def run_agent_tests(target: Path) -> tuple[bool, str]:
    with tempfile.TemporaryDirectory() as tmp:
        test_copy = Path(tmp) / "test_agent.py"
        shutil.copy(CANONICAL_TEST_FILE, test_copy)
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_copy), "-v"],
            cwd=target,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0, result.stdout + result.stderr


def check_module_04(target: Path) -> CheckResult:
    """Importable by a future Module 05's checker for cumulative-gate chaining."""
    m3 = check_module_03(target)
    if not m3.passed:
        return m3
    passed, output = run_agent_tests(target)
    findings = list(m3.findings)
    findings.append("  Module 04 test suite: PASS" if passed else "  Module 04 test suite: FAIL")
    return CheckResult(passed=passed, findings=findings, output=output)


def main(argv: list[str]) -> int:
    target = Path(argv[1]).resolve() if len(argv) > 1 else REPO_ROOT / "fixtures" / "resolve"

    print(f"=== Module 04 deterministic tier: {target} ===")
    print()
    result = check_module_04(target)
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
