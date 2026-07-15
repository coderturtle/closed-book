#!/usr/bin/env python3
"""Deterministic tier for Module 01 (Configuring Claude Code for Real Work).

Mechanical checks only: does the required structure exist, and does each
path-scoped rule's glob actually match real content in the project -- not
whether the configuration is *good* (that's the conceptual tier, Coachgremlin's
job, scored against CCA-F Task Statement 3.1-3.6's own "Skills in:" bullets).

Rewritten in Python 2026-07-15, replacing the original bash version, after a
doubt-driven-development review (a fresh Claude subagent + Codex, both run
against the bash version) found several bugs that share one root cause --
reimplementing YAML frontmatter parsing and recursive globbing in shell that
has to run on macOS's bash 3.2 (no `globstar`, quoted-only pattern matching,
no path-escape rejection). See docs/decisions.md's 2026-07-15 entries and
runs/2026-07-14-module-01-dry-run/grading.md for the full history.

Importable as a module (`check_module_01`) so later modules' checkers can
chain it -- the cumulative-gate convention in fixtures/resolve/SPEC.md.

Usage: scripts/verify_module_01.py [path-to-attempt]
  Defaults to fixtures/resolve/ relative to the repo root.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CheckResult:
    passed: bool
    findings: list[str] = field(default_factory=list)

    def ok(self, msg: str) -> None:
        self.findings.append(f"  OK:   {msg}")

    def fail(self, msg: str) -> None:
        self.findings.append(f"  FAIL: {msg}")
        self.passed = False


def _extract_frontmatter(path: Path) -> dict | None:
    """Parse a minimal YAML frontmatter subset: `key: value` scalars and
    `key: [\"a\", \"b\"]` / block-list (`key:\n  - a\n  - b`) arrays only --
    the subset this checker actually needs, not a general YAML parser.
    Anchored: frontmatter must start at line 1 and have a real closing `---`.
    Returns None if the file has no valid frontmatter block.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    try:
        close_idx = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None  # no closing delimiter -- not valid frontmatter

    body = lines[1:close_idx]
    result: dict[str, list[str] | str] = {}
    key = None
    i = 0
    while i < len(body):
        line = body[i]
        block_list_match = re.match(r"^(\w[\w-]*):\s*$", line)
        inline_match = re.match(r"^(\w[\w-]*):\s*(.+)$", line)
        if block_list_match:
            key = block_list_match.group(1)
            items: list[str] = []
            j = i + 1
            while j < len(body) and re.match(r"^\s*-\s+", body[j]):
                items.append(re.sub(r"^\s*-\s+", "", body[j]).strip().strip("\"'"))
                j += 1
            result[key] = items
            i = j
            continue
        if inline_match:
            key, raw_value = inline_match.group(1), inline_match.group(2).strip()
            if raw_value.startswith("["):
                # Inline array: ["a", "b"] or [a, b]
                inner = raw_value.strip("[]")
                result[key] = [v.strip().strip("\"'") for v in inner.split(",") if v.strip()]
            else:
                result[key] = raw_value.strip("\"'")
            i += 1
            continue
        i += 1
    return result


def _is_safe_pattern(pattern: str) -> bool:
    """Reject patterns that could escape the target project directory."""
    if pattern.startswith("/") or pattern.startswith("~"):
        return False
    if ".." in Path(pattern).parts:
        return False
    return True


def check_module_01(target: Path) -> CheckResult:
    result = CheckResult(passed=True)

    # 1. Project-root CLAUDE.md exists and is non-empty.
    claude_md = target / "CLAUDE.md"
    if claude_md.is_file() and claude_md.stat().st_size > 0:
        result.ok("CLAUDE.md exists and is non-empty")
    else:
        result.fail(f"CLAUDE.md missing or empty at {claude_md}")

    # 2. At least one .claude/rules/*.md file exists.
    rules_dir = target / ".claude" / "rules"
    rules_files = sorted(rules_dir.glob("*.md")) if rules_dir.is_dir() else []
    if rules_files:
        result.ok(f"{len(rules_files)} file(s) found under .claude/rules/")
    else:
        result.fail(
            "no .claude/rules/*.md file found -- a monolithic root CLAUDE.md alone "
            "does not satisfy this project's path-scoping requirement (Task Statement 3.3)"
        )

    # 3. At least one rule scopes real files under src/tools/**, and at least one
    #    (possibly the same or a different file) scopes real files under tests/** --
    #    the exercise explicitly asks for conventions "distinct from whatever
    #    applies to tests/**", so both scopes are required, not just any scope.
    tools_scoped = False
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
            matches = list(target.glob(pattern))
            if not matches:
                continue
            if any(target / "src" / "tools" in m.parents or m == target / "src" / "tools" for m in matches):
                tools_scoped = True
            if any(target / "tests" in m.parents or m == target / "tests" for m in matches):
                tests_scoped = True
            result.ok(f"rules file {f.name}'s pattern '{pattern}' matches {len(matches)} real file(s)")

    if unsafe_patterns:
        result.fail(
            "rejected pattern(s) that could escape the project directory "
            f"(absolute path, '~', or '..' component): {', '.join(unsafe_patterns)}"
        )
    if tools_scoped:
        result.ok("at least one rule scopes real files under src/tools/**")
    else:
        result.fail(
            "no rule scopes real files specifically under src/tools/** -- a rule scoped "
            "elsewhere (e.g. only tests/**, or a typo'd path) does not satisfy this"
        )
    if tests_scoped:
        result.ok("at least one rule scopes real files under tests/**")
    else:
        result.fail("no rule scopes real files specifically under tests/**")

    # 4. At least one project-scoped slash command exists (recursively --
    #    subdirectory-namespaced commands like .claude/commands/resolve/foo.md
    #    are a real, documented convention and must not be rejected).
    cmd_dir = target / ".claude" / "commands"
    cmd_files = sorted(cmd_dir.rglob("*.md")) if cmd_dir.is_dir() else []
    if cmd_files:
        result.ok(f"{len(cmd_files)} project-scoped slash command(s) found under .claude/commands/")
    else:
        result.fail("no .claude/commands/**/*.md file found")

    # 5. CI-readiness: some doc in the project documents a non-interactive
    #    `claude -p`/`--print` invocation. This is a textual heuristic, not a
    #    real CI run -- it cannot verify the documented command actually works,
    #    only that CI-mode usage is documented somewhere. The conceptual tier
    #    and this module's closed-book checkpoint (questions 11-12) carry the
    #    real verification of understanding.
    ci_documented = False
    # Excludes SPEC.md: it ships with the fixture and *describes* this
    # requirement in prose (which itself contains the string "claude -p"),
    # so including it would make this check a permanent, silent no-op --
    # found by re-running the dry run against this exact bug, 2026-07-15.
    for doc in list(target.rglob("*.md")):
        if ".claude" in doc.parts or doc.name == "SPEC.md":
            continue
        text = doc.read_text(encoding="utf-8", errors="replace")
        if re.search(r"claude\s+(-p\b|--print\b)", text):
            ci_documented = True
            break
    if ci_documented:
        result.ok("a non-interactive `claude -p`/`--print` invocation is documented somewhere in the project")
    else:
        result.fail(
            "no project doc documents a `claude -p`/`--print` invocation pattern "
            "(exercise requirement 4: CI-readiness)"
        )

    return result


def main(argv: list[str]) -> int:
    root = Path(__file__).resolve().parent.parent
    target = Path(argv[1]).resolve() if len(argv) > 1 else root / "fixtures" / "resolve"

    print(f"=== Module 01 deterministic tier: {target} ===")
    result = check_module_01(target)
    for line in result.findings:
        print(line)
    print()
    if result.passed:
        print("=== Deterministic tier: PASS ===")
        return 0
    print("=== Deterministic tier: FAIL ===")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
