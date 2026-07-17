#!/usr/bin/env python3
"""Deterministic tier for Module 09 (Shipping Responsibly: Governance,
Stakeholders & Team Enablement).

Chains `check_module_08` (which chains `check_module_07`), per the Part 2
compatibility contract in `fixtures/foundry/SPEC.md`.

Three real deliverables, one gate:
1. `tests/test_governance.py` (canonical, neutral-temp-dir + expected-pass-
   count execution): `src/governance.py`'s human-in-the-loop gate wrapped
   around Module 08's `doc_qa.answer_question`.
2. `docs/shipping-readiness-review.md`: a real, structurally-checked
   stakeholder-facing document (4 required sections), reusing Module 07's
   `check_adr`-style regex section extraction.
3. `.claude/` team tooling configuration for `fixtures/foundry/` itself
   (Domain 7, Developer Productivity & Operational Enablement) -- rules
   scoping real `src/**` and `tests/**` content, plus a slash command --
   reusing Module 01's frontmatter-parsing and safe-pattern helpers rather
   than reimplementing them.

Usage: scripts/verify_module_09.py [path-to-attempt]
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
from verify_module_01 import _extract_frontmatter, _is_safe_pattern  # noqa: E402
from verify_module_08 import check_module_08  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_TEST_FILE = REPO_ROOT / "fixtures" / "foundry" / "tests" / "test_governance.py"
REVIEW_RELATIVE_PATH = Path("docs") / "shipping-readiness-review.md"
REQUIRED_REVIEW_SECTIONS = [
    "Failure Modes",
    "Compliance Requirement and Architectural Consequence",
    "Human-in-the-Loop Checkpoint",
    "Stakeholder Summary",
]
MIN_SECTION_CHARS = 40


@dataclass
class CheckResult:
    passed: bool
    findings: list[str] = field(default_factory=list)
    output: str = ""


def _expected_test_count() -> int:
    return len(re.findall(r"(?m)^def test_", CANONICAL_TEST_FILE.read_text()))


def run_governance_tests(target: Path) -> tuple[bool, str]:
    """Same two-layer hardening as every checker since Module 07's doubt-
    driven-development: a neutral temp dir (never cwd=target) plus an
    expected-pass-count check on the pytest summary, applied here from the
    start."""
    submission_src = target / "src"
    if not submission_src.is_dir():
        return False, f"FAIL: no src/ directory found in the submission at {target}"
    expected = _expected_test_count()
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        test_copy = tmp_path / "test_governance.py"
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


def check_readiness_review(target: Path) -> tuple[bool, list[str]]:
    findings: list[str] = []
    review_path = target / REVIEW_RELATIVE_PATH
    if not review_path.is_file():
        return False, [f"FAIL: no shipping-readiness review found at {REVIEW_RELATIVE_PATH}"]

    text = review_path.read_text()
    findings.append(
        f"OK:   {REVIEW_RELATIVE_PATH} exists and is non-empty" if text.strip() else f"FAIL: {REVIEW_RELATIVE_PATH} is empty"
    )
    if not text.strip():
        return False, findings

    # Strip fenced code blocks before section matching, only when balanced --
    # see scripts/verify_module_07.py's check_adr for why (found via Module
    # 07's own doubt-driven-development).
    if text.count("```") % 2 == 0:
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    passed = True
    section_bodies: dict[str, str] = {}
    for section in REQUIRED_REVIEW_SECTIONS:
        pattern = re.compile(
            rf"^#+\s*{re.escape(section)}\s*$(.*?)(?=^#+\s|\Z)",
            re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )
        m = pattern.search(text)
        if not m:
            findings.append(f"FAIL: no '{section}' section found in the review")
            passed = False
            continue
        body = m.group(1).strip()
        section_bodies[section] = body
        if len(body) < MIN_SECTION_CHARS:
            findings.append(f"FAIL: '{section}' section exists but has too little real content ({len(body)} chars, need {MIN_SECTION_CHARS}+)")
            passed = False
        else:
            findings.append(f"OK:   '{section}' section present with real content")

    compliance_body = section_bodies.get("Compliance Requirement and Architectural Consequence", "")
    if compliance_body:
        names_a_real_consequence = bool(re.search(r"\bsensitive\b|\bcompliance\b|\bredact", compliance_body, re.IGNORECASE))
        if names_a_real_consequence:
            findings.append("OK:   Compliance Requirement and Architectural Consequence names a real, specific consequence")
        else:
            findings.append("FAIL: Compliance Requirement and Architectural Consequence doesn't name a specific compliance-driven design consequence")
            passed = False

    return passed, findings


def check_team_tooling(target: Path) -> tuple[bool, list[str]]:
    """Domain 7 (Developer Productivity & Operational Enablement): real
    `.claude/` configuration for `fixtures/foundry/` itself, scoping real
    `src/**` and `tests/**` content, plus a project-scoped slash command --
    Module 01's own exercise shape, reused in a new project."""
    findings: list[str] = []
    passed = True

    rules_dir = target / ".claude" / "rules"
    rules_files = sorted(rules_dir.glob("*.md")) if rules_dir.is_dir() else []
    if rules_files:
        findings.append(f"OK:   {len(rules_files)} file(s) found under .claude/rules/")
    else:
        findings.append("FAIL: no .claude/rules/*.md file found for fixtures/foundry/ team tooling")
        passed = False

    src_scoped = False
    tests_scoped = False
    unsafe_patterns: list[str] = []
    for f in rules_files:
        frontmatter = _extract_frontmatter(f)
        if not frontmatter or "paths" not in frontmatter:
            continue
        patterns = frontmatter["paths"]
        if isinstance(patterns, str):
            patterns = [patterns]
        for pattern in patterns:
            if not _is_safe_pattern(pattern):
                unsafe_patterns.append(f"{f.name}: '{pattern}'")
                continue
            # Files only -- a pattern like `paths: ["src"]` (no glob) would
            # otherwise match the bare directory node itself and count as
            # "scoping real files" without matching anything inside it.
            # Found via doubt-driven-development (Codex confirmed the same
            # root cause in verify_module_01.py's own check, fixed there too).
            matches = [m for m in target.glob(pattern) if m.is_file()]
            if not matches:
                continue
            if any(target / "src" in m.parents for m in matches):
                src_scoped = True
            if any(target / "tests" in m.parents for m in matches):
                tests_scoped = True
            findings.append(f"OK:   rules file {f.name}'s pattern '{pattern}' matches {len(matches)} real file(s)")

    if unsafe_patterns:
        findings.append(
            "FAIL: rejected pattern(s) that could escape the project directory: " + ", ".join(unsafe_patterns)
        )
        passed = False
    if src_scoped:
        findings.append("OK:   at least one rule scopes real files under src/**")
    else:
        findings.append("FAIL: no rule scopes real files under src/**")
        passed = False
    if tests_scoped:
        findings.append("OK:   at least one rule scopes real files under tests/**")
    else:
        findings.append("FAIL: no rule scopes real files under tests/**")
        passed = False

    cmd_dir = target / ".claude" / "commands"
    cmd_files = sorted(cmd_dir.rglob("*.md")) if cmd_dir.is_dir() else []
    if cmd_files:
        findings.append(f"OK:   {len(cmd_files)} project-scoped slash command(s) found under .claude/commands/")
    else:
        findings.append("FAIL: no .claude/commands/**/*.md file found")
        passed = False

    return passed, findings


def check_module_09(target: Path) -> CheckResult:
    """Importable by Module 10's checker for cumulative-gate chaining."""
    m8 = check_module_08(target)
    test_passed, test_output = run_governance_tests(target)
    review_passed, review_findings = check_readiness_review(target)
    tooling_passed, tooling_findings = check_team_tooling(target)

    findings = list(m8.findings)
    findings.append("  Module 08's gate: PASS" if m8.passed else "  Module 08's gate: FAIL")
    findings.append("  Module 09 test suite: PASS" if test_passed else "  Module 09 test suite: FAIL")
    findings.extend(review_findings)
    findings.extend(tooling_findings)

    passed = m8.passed and test_passed and review_passed and tooling_passed
    return CheckResult(passed=passed, findings=findings, output=test_output)


def main(argv: list[str]) -> int:
    target = Path(argv[1]).resolve() if len(argv) > 1 else REPO_ROOT / "fixtures" / "foundry"

    print(f"=== Module 09 deterministic tier: {target} ===")
    print()
    result = check_module_09(target)
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
