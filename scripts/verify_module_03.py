#!/usr/bin/env python3
"""Deterministic tier for Module 03 (Designing Tools and MCP Interfaces).

Chains Module 02's check (which itself chains Module 01's), per the
cumulative-gate convention in fixtures/resolve/SPEC.md's compatibility
contract, then runs the real pytest suite against the four MCP tools in
src/tools/.

Usage: scripts/verify_module_03.py [path-to-attempt]
  Defaults to fixtures/resolve/ relative to the repo root.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_module_02 import check_module_02  # noqa: E402


def run_tool_tests(target: Path) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_tools.py", "-v"],
        cwd=target,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0, result.stdout + result.stderr


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parent.parent
    target = Path(argv[1]).resolve() if len(argv) > 1 else root / "fixtures" / "resolve"

    print(f"=== Module 03 deterministic tier: {target} ===")
    print()
    print("-- Cumulative gate: Module 02's check (chains Module 01's) --")
    m2_result, m2_output = check_module_02(target)
    for line in m2_result.findings:
        print(line)
    if m2_output:
        print(m2_output)
    if not m2_result.passed:
        print()
        print("=== Deterministic tier: FAIL (Module 02's gate did not pass -- ")
        print("    fix that before this submission can be evaluated for Module 03) ===")
        return 1
    print("  Module 02's gate: PASS")

    print()
    print("-- Module 03: MCP tool test suite (tests/test_tools.py) --")
    passed, output = run_tool_tests(target)
    print(output)

    print()
    if passed:
        print("=== Deterministic tier: PASS ===")
        return 0
    print("=== Deterministic tier: FAIL ===")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
