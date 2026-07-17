#!/usr/bin/env python3
"""Deterministic tier for Module 07 (Designing the Solution: Architecture,
Models & Context Strategy).

First checker for Part 2 (`fixtures/foundry/`, CCAR-P Architect Professional).
Per `fixtures/foundry/SPEC.md`'s compatibility contract, this does NOT chain
back through Part 1's `check_module_06`/`resolve` gate -- Module 06's own
hard-prerequisite framing already establishes a learner reached here having
cleared all of Part 1, and `foundry` is a structurally separate codebase.

Two real deliverables are checked: (1) `tests/test_ticket_triage.py`, run
against the repo's own canonical copy (never the submission's -- see
verify_module_02.py's module docstring for why); (2) a real architecture
decision record at `docs/adr-0001-ticket-triage-architecture.md`, checked
for required section presence, non-trivial content per section, and that
the Alternatives section actually names and addresses the specific
alternative the Helpdesk team proposed ("something like resolve").

Usage: scripts/verify_module_07.py [path-to-attempt]
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

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_TEST_FILE = REPO_ROOT / "fixtures" / "foundry" / "tests" / "test_ticket_triage.py"
ADR_RELATIVE_PATH = Path("docs") / "adr-0001-ticket-triage-architecture.md"
REQUIRED_ADR_SECTIONS = ["Context", "Decision", "Alternatives Considered", "Consequences"]
MIN_SECTION_CHARS = 40


@dataclass
class CheckResult:
    passed: bool
    findings: list[str] = field(default_factory=list)
    output: str = ""


def _expected_test_count() -> int:
    return len(re.findall(r"(?m)^def test_", CANONICAL_TEST_FILE.read_text()))


def run_triage_tests(target: Path) -> tuple[bool, str]:
    """Copies both the canonical test file AND the submission's src/ into a
    fresh, neutral temp dir, and runs pytest with cwd set to THAT dir -- never
    cwd=target. Running with cwd=target would put the submission's own
    top-level directory at the front of sys.path for a `python -m pytest`
    invocation; a submission could then ship a same-named shadow module (e.g.
    a 2-line `pytest.py` that does `raise SystemExit(0)`) that resolves ahead
    of the real installed pytest package and skips the canonical test file
    entirely without ever executing it.

    A zero exit code alone is NOT sufficient evidence the suite actually ran:
    submission code executes during pytest's own collection (importing
    src/ticket_triage.py is exactly that), so a submission calling
    `os._exit(0)` at module import time kills the whole pytest subprocess
    with return code 0 before a single test runs, and returncode==0 alone
    would read that as a clean pass. Fixed by additionally requiring the
    pytest summary line itself report the full expected test count actually
    passed (`os._exit` truncates output before that line is ever printed).
    See docs/decisions.md's 2026-07-17 entry -- found via doubt-driven-
    development (the shadow-module bypass), then the os._exit variant found
    by a Fable-model critique of that same remediation. Fixed in all six
    checkers at once."""
    submission_src = target / "src"
    if not submission_src.is_dir():
        return False, f"FAIL: no src/ directory found in the submission at {target}"
    expected = _expected_test_count()
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        test_copy = tmp_path / "test_ticket_triage.py"
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


def check_adr(target: Path) -> tuple[bool, list[str]]:
    findings: list[str] = []
    adr_path = target / ADR_RELATIVE_PATH
    if not adr_path.is_file():
        return False, [f"FAIL: no ADR found at {ADR_RELATIVE_PATH} (exercise requirement: a real architecture decision record)"]

    text = adr_path.read_text()
    findings.append(f"OK:   {ADR_RELATIVE_PATH} exists and is non-empty" if text.strip() else f"FAIL: {ADR_RELATIVE_PATH} is empty")
    if not text.strip():
        return False, findings

    # Strip fenced code blocks before section matching -- otherwise a heading
    # that only appears inside a ```code``` illustration (e.g. a markdown
    # syntax example) would count as a real section. Found via doubt-driven-
    # development (both the Claude subagent and Codex reviews independently
    # flagged this); see docs/decisions.md's 2026-07-17 entry. Only strip when
    # fences are balanced (an even number of ``` markers) -- an unclosed
    # fence in an otherwise-valid ADR would make this regex pair the wrong
    # fences and delete real section content, a false-fail worse than the
    # gap it's closing (found by a Fable-model critique of this same fix).
    # A coarse proxy either way: a fake heading inside a non-``` fence (e.g.
    # ~~~ or an indented code block) still isn't caught -- disclosed, not
    # silently assumed solved, per this checker's own "necessary, not
    # sufficient" framing (see the module README's rubric section).
    if text.count("```") % 2 == 0:
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    passed = True
    section_bodies: dict[str, str] = {}
    for section in REQUIRED_ADR_SECTIONS:
        # Match a markdown heading (any level) containing this section name,
        # capturing everything up to the next heading of the same or higher
        # level, or end of file.
        pattern = re.compile(
            rf"^#+\s*{re.escape(section)}\s*$(.*?)(?=^#+\s|\Z)",
            re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )
        m = pattern.search(text)
        if not m:
            findings.append(f"FAIL: no '{section}' section found in the ADR")
            passed = False
            continue
        body = m.group(1).strip()
        section_bodies[section] = body
        if len(body) < MIN_SECTION_CHARS:
            findings.append(f"FAIL: '{section}' section exists but has too little real content ({len(body)} chars, need {MIN_SECTION_CHARS}+)")
            passed = False
        else:
            findings.append(f"OK:   '{section}' section present with real content")

    alternatives = section_bodies.get("Alternatives Considered", "")
    if alternatives:
        mentions_agentic_alternative = bool(
            re.search(r"\bresolve\b", alternatives, re.IGNORECASE)
            or re.search(r"\bagentic\b|\bagent\b", alternatives, re.IGNORECASE)
        )
        if mentions_agentic_alternative:
            findings.append("OK:   Alternatives Considered names the Helpdesk team's own proposed alternative (an agentic/resolve-like approach)")
        else:
            findings.append("FAIL: Alternatives Considered does not name the specific alternative the Helpdesk team actually proposed (an agentic loop / something like resolve)")
            passed = False

    return passed, findings


def check_module_07(target: Path) -> CheckResult:
    """Importable by a future Module 08's checker for cumulative-gate chaining."""
    test_passed, test_output = run_triage_tests(target)
    adr_passed, adr_findings = check_adr(target)

    findings = list(adr_findings)
    findings.append("  Module 07 test suite: PASS" if test_passed else "  Module 07 test suite: FAIL")

    return CheckResult(passed=test_passed and adr_passed, findings=findings, output=test_output)


def main(argv: list[str]) -> int:
    target = Path(argv[1]).resolve() if len(argv) > 1 else REPO_ROOT / "fixtures" / "foundry"

    print(f"=== Module 07 deterministic tier: {target} ===")
    print()
    result = check_module_07(target)
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
