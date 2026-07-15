#!/usr/bin/env bash
# verify-module-01.sh — deterministic tier for Module 01 (Configuring Claude Code
# for Real Work). Mechanical checks only: does the required structure exist, and
# does a path-scoped rule's glob actually match real content in the project — not
# whether the configuration is *good* (that's the conceptual tier, Coachgremlin's
# job, scored against Task Statement 3.1-3.6's own "Skills in:" bullets).
#
# Usage: scripts/verify-module-01.sh [path-to-attempt]
#   Defaults to fixtures/resolve/ relative to the repo root.
set -uo pipefail
shopt -s globstar  # required for `**` glob patterns (e.g. "src/tools/**/*") to match recursively

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-$ROOT/fixtures/resolve}"

PASS=true
fail() { echo "  FAIL: $1"; PASS=false; }
ok()   { echo "  OK:   $1"; }

echo "=== Module 01 deterministic tier: $TARGET ==="

# 1. Project-root CLAUDE.md exists and is non-empty.
if [[ -s "$TARGET/CLAUDE.md" ]]; then
  ok "CLAUDE.md exists and is non-empty"
else
  fail "CLAUDE.md missing or empty at $TARGET/CLAUDE.md"
fi

# 2. At least one .claude/rules/*.md file exists.
RULES_DIR="$TARGET/.claude/rules"
RULES_FILES=()
if [[ -d "$RULES_DIR" ]]; then
  while IFS= read -r -d '' f; do RULES_FILES+=("$f"); done < <(find "$RULES_DIR" -maxdepth 1 -name "*.md" -print0 2>/dev/null)
fi
if [[ ${#RULES_FILES[@]} -gt 0 ]]; then
  ok "${#RULES_FILES[@]} file(s) found under .claude/rules/"
else
  fail "no .claude/rules/*.md file found — a monolithic root CLAUDE.md alone does not satisfy this project's path-scoping requirement (Task Statement 3.3)"
fi

# 3. At least one rules file has YAML frontmatter with a `paths:` key whose
#    glob pattern actually matches a real file under the project (not just
#    present syntactically — the naive-attempt failure mode this check targets
#    is a rules file that exists but scopes to nothing real).
SCOPED_MATCH=false
for f in "${RULES_FILES[@]:-}"; do
  [[ -z "$f" ]] && continue
  # Extract the paths: line's glob value(s) from frontmatter (between the first two --- lines).
  FRONTMATTER=$(awk '/^---$/{c++; next} c==1' "$f")
  PATTERNS=$(echo "$FRONTMATTER" | grep -A5 '^paths:' | grep -oE '"[^"]+"|\x27[^\x27]+\x27' | tr -d '"'"'"'' || true)
  if [[ -z "$PATTERNS" ]]; then
    # Single-line form: paths: ["a/**/*", "b/**/*"]
    PATTERNS=$(echo "$FRONTMATTER" | grep '^paths:' | grep -oE '"[^"]+"' | tr -d '"' || true)
  fi
  while IFS= read -r pattern; do
    [[ -z "$pattern" ]] && continue
    if (cd "$TARGET" && compgen -G "$pattern" > /dev/null 2>&1); then
      ok "rules file $(basename "$f")'s pattern '$pattern' matches real file(s) under the project"
      SCOPED_MATCH=true
    fi
  done <<< "$PATTERNS"
done
if [[ "$SCOPED_MATCH" != "true" ]]; then
  fail "no .claude/rules/ file's paths: glob matched any real file under $TARGET — a rules file that scopes to nothing is equivalent to having none"
fi

# 4. At least one project-scoped slash command exists.
CMD_DIR="$TARGET/.claude/commands"
CMD_COUNT=0
if [[ -d "$CMD_DIR" ]]; then
  CMD_COUNT=$(find "$CMD_DIR" -maxdepth 1 -name "*.md" | wc -l | tr -d ' ')
fi
if [[ "$CMD_COUNT" -gt 0 ]]; then
  ok "$CMD_COUNT project-scoped slash command(s) found under .claude/commands/"
else
  fail "no .claude/commands/*.md file found"
fi

echo ""
if [[ "$PASS" == "true" ]]; then
  echo "=== Deterministic tier: PASS ==="
  exit 0
else
  echo "=== Deterministic tier: FAIL ==="
  exit 1
fi
