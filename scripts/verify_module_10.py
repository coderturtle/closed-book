#!/usr/bin/env python3
"""Deterministic tier for Module 10 (Professional Capstone: Sit-Ready for
CCAR-P).

Chains `check_module_09` (which chains `check_module_08`, which chains
`check_module_07`), per the Part 2 compatibility contract in
`fixtures/foundry/SPEC.md`. This is the final link in Part 2's cumulative
gate.

One real deliverable, purely written: `docs/capstone-architecture-defense.md`,
a structurally-checked document synthesizing Foundry's full Part 2 system
(Modules 07-09: ticket triage, doc Q&A/evaluation, governance) and defending
it in writing against a real, seeded stakeholder objection -- reusing the
same regex-section-extraction discipline as Module 07's `check_adr` and
Module 09's `check_readiness_review`.

Usage: scripts/verify_module_10.py [path-to-attempt]
  Defaults to fixtures/foundry/ relative to the repo root.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_module_09 import check_module_09  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFENSE_RELATIVE_PATH = Path("docs") / "capstone-architecture-defense.md"
REQUIRED_DEFENSE_SECTIONS = [
    "The Objection",
    "Why It's a Reasonable Challenge",
    "The Defense",
    "What Would Change Our Mind",
]
MIN_SECTION_CHARS = 60  # higher bar than Modules 07/09 -- a capstone synthesis needs more than a paragraph
# "The Defense" specifically has to carry real reasoning about three distinct
# systems, not just name-drop them in one throwaway sentence -- a doubt-driven-
# development review constructed a ~150-char bypass of the generic length
# floor above, so this section gets its own, higher one.
DEFENSE_MIN_CHARS = 400
# A "falsifiable condition" is not falsifiable if the text explicitly
# refuses to ever change its conclusion. Rather than match a fixed set of
# phrases (trivially dodged by a paraphrase -- a review found "never
# reconsider" -> "would never revisit" slips past an exact-phrase list), this
# looks for co-occurrence, in the same sentence, of a refusal marker and a
# reconsider-class verb -- still a coarse proxy, not real semantics; the
# conceptual rubric's own criterion 3 ("the falsifiability condition is
# genuinely falsifiable") is what actually judges this.
REFUSAL_MARKERS = re.compile(
    r"\bnever\b|\bwon'?t\b|\bwill not\b|\bwould not\b|\bdo(?:es)? not\b"
    r"|\bregardless\b|\bno matter\b|\birrespective\b",
    re.IGNORECASE,
)
RECONSIDER_VERBS = re.compile(
    r"\breconsider\w*|\brevisit\w*|\brethink\w*|\bre-?evaluat\w*|\brevis\w*|\bchange\b|\banticipat\w*",
    re.IGNORECASE,
)
# Naming the three systems and clearing a length floor is satisfiable by
# generic architecture platitudes ("separate things should be separate")
# with zero real content -- a doubt-driven-development review constructed
# exactly this bypass. This is a coarse proxy for "does the text actually
# engage the systems' real, distinct risk profiles Modules 07-09
# established," not a semantic check -- the conceptual rubric's own
# criterion 2 is what actually judges whether the reasoning is good.
# NOTE (disclosed, not fixed): a submission that merely quotes or lists these
# words affirmatively ("the VP's memo mentions risk, compliance, and audit")
# without any real reasoning about them can still slip past this -- no
# lexical check can distinguish real engagement from name-dropping in every
# case. This is the class of gap the conceptual rubric exists to catch.
DEFENSE_RISK_VOCABULARY = re.compile(
    r"\brisks?\b|\bfailure modes?\b|\bclassif\w*|\bretriev\w*|\bstale\w*|\bcomplian\w*"
    r"|\bcorrectness\b|\baudits?\b|\btest(?:s|ed|ing)?\b|\bblast radius(?:es)?\b",
    re.IGNORECASE,
)
DEFENSE_MIN_DISTINCT_RISK_TERMS = 3
# A sentence that self-referentially denies discussing these terms ("this
# paragraph does not compare risks, tests, compliance...") shouldn't count --
# a constructed doubt-driven-development bypass did exactly this. Deliberately
# narrow (specific self-denial verbs, not any negation word in the sentence):
# an earlier, broader "any negation word excludes the whole sentence" version
# produced false positives against honest writing that describes a system's
# real guarantees in negation-shaped language ("sensitive content never
# reaches a model call", "must not answer from stale content") -- that
# language should still count.
SELF_DENIAL_MARKERS = re.compile(
    r"\bdoes not\b|\bdoesn'?t\b|\bwill not\b|\bwon'?t\b|\bdeclines? to\b|\bavoids?\b"
    r"|\brather than compar\w*|\brather than discuss\w*|\brather than weigh\w*"
    r"|\bwithout (?:discussing|comparing|addressing|weighing)\b",
    re.IGNORECASE,
)
SELF_DENIAL_WINDOW_CHARS = 80  # how far back from a risk-term match to look for a self-denial trigger

_CANONICAL_PREFIXES = [
    "risk", "failure mode", "classif", "retriev", "stale", "complian",
    "correctness", "audit", "test", "blast radius",
]


def _canonicalize_risk_term(raw: str) -> str:
    lowered = raw.lower()
    for prefix in _CANONICAL_PREFIXES:
        if lowered.startswith(prefix):
            return prefix
    return lowered


@dataclass
class CheckResult:
    passed: bool
    findings: list[str] = field(default_factory=list)
    output: str = ""


def check_architecture_defense(target: Path) -> tuple[bool, list[str]]:
    findings: list[str] = []
    defense_path = target / DEFENSE_RELATIVE_PATH
    if not defense_path.is_file():
        return False, [f"FAIL: no capstone architecture defense found at {DEFENSE_RELATIVE_PATH}"]

    text = defense_path.read_text()
    findings.append(
        f"OK:   {DEFENSE_RELATIVE_PATH} exists and is non-empty" if text.strip() else f"FAIL: {DEFENSE_RELATIVE_PATH} is empty"
    )
    if not text.strip():
        return False, findings

    # Strip fenced code blocks before section matching, only when balanced --
    # see scripts/verify_module_07.py's check_adr for why.
    if text.count("```") % 2 == 0:
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    passed = True
    section_bodies: dict[str, str] = {}
    for section in REQUIRED_DEFENSE_SECTIONS:
        pattern = re.compile(
            rf"^#+\s*{re.escape(section)}\s*$(.*?)(?=^#+\s|\Z)",
            re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )
        m = pattern.search(text)
        if not m:
            findings.append(f"FAIL: no '{section}' section found in the architecture defense")
            passed = False
            continue
        body = m.group(1).strip()
        section_bodies[section] = body
        if len(body) < MIN_SECTION_CHARS:
            findings.append(f"FAIL: '{section}' section exists but has too little real content ({len(body)} chars, need {MIN_SECTION_CHARS}+)")
            passed = False
        else:
            findings.append(f"OK:   '{section}' section present with real content")

    # The defense must actually name the specific systems being defended --
    # a generic essay about architecture in general, with none of Foundry's
    # own real modules named, would pass the section-presence check alone.
    defense_body = section_bodies.get("The Defense", "")
    if defense_body:
        names_real_systems = bool(
            re.search(r"\bticket_triage\b|\bticket.triage\b", defense_body, re.IGNORECASE)
            and re.search(r"\bdoc_qa\b|\bdoc.qa\b", defense_body, re.IGNORECASE)
            and re.search(r"\bgovernance\b", defense_body, re.IGNORECASE)
        )
        if names_real_systems:
            findings.append("OK:   The Defense names all three of Foundry's real Part 2 systems (ticket_triage, doc_qa, governance)")
        else:
            findings.append("FAIL: The Defense doesn't name all three of Foundry's real systems (ticket_triage, doc_qa, governance) -- a generic architecture essay isn't sufficient")
            passed = False

        if len(defense_body) < DEFENSE_MIN_CHARS:
            findings.append(f"FAIL: The Defense is too short to be real reasoning about three systems ({len(defense_body)} chars, need {DEFENSE_MIN_CHARS}+) -- a single sentence naming all three isn't a defense")
            passed = False
        else:
            findings.append("OK:   The Defense is long enough to plausibly carry real reasoning, not just name-drop the three systems")

        distinct_risk_terms = set()
        for match in DEFENSE_RISK_VOCABULARY.finditer(defense_body):
            preceding = defense_body[max(0, match.start() - SELF_DENIAL_WINDOW_CHARS):match.start()]
            if SELF_DENIAL_MARKERS.search(preceding):
                continue
            distinct_risk_terms.add(_canonicalize_risk_term(match.group(0)))
        if len(distinct_risk_terms) < DEFENSE_MIN_DISTINCT_RISK_TERMS:
            findings.append(f"FAIL: The Defense doesn't engage enough of the systems' real risk vocabulary ({len(distinct_risk_terms)} distinct term(s) found, need {DEFENSE_MIN_DISTINCT_RISK_TERMS}+) -- naming systems and hitting a length floor isn't the same as reasoning about their actual failure modes")
            passed = False
        else:
            findings.append(f"OK:   The Defense engages real risk vocabulary ({len(distinct_risk_terms)} distinct term(s)), not just architecture platitudes")

    # "What Would Change Our Mind" must state a real, checkable condition,
    # not just restate that the design is correct -- a coarse proxy for
    # "is this actually falsifiable," same discipline as Module 07/09's own
    # keyword checks on their respective sections.
    falsifiability_body = section_bodies.get("What Would Change Our Mind", "")
    if falsifiability_body:
        states_a_condition = bool(re.search(r"\bif\b|\bwhen\b|\bonce\b|\bshould\b", falsifiability_body, re.IGNORECASE))
        refuses_to_be_false = any(
            REFUSAL_MARKERS.search(sentence) and RECONSIDER_VERBS.search(sentence)
            for sentence in re.split(r"(?<=[.!?])\s+", falsifiability_body)
        )
        if states_a_condition and not refuses_to_be_false:
            findings.append("OK:   What Would Change Our Mind states a conditional, checkable criterion")
        elif refuses_to_be_false:
            findings.append("FAIL: What Would Change Our Mind contains a trigger word but also an explicit refuse-to-reconsider disclaimer -- that's not falsifiable")
            passed = False
        else:
            findings.append("FAIL: What Would Change Our Mind doesn't read as a real conditional criterion")
            passed = False

    return passed, findings


def check_module_10(target: Path) -> CheckResult:
    """The final link in Part 2's cumulative gate."""
    m9 = check_module_09(target)
    defense_passed, defense_findings = check_architecture_defense(target)

    findings = list(m9.findings)
    findings.append("  Module 09's gate: PASS" if m9.passed else "  Module 09's gate: FAIL")
    findings.extend(defense_findings)

    passed = m9.passed and defense_passed
    return CheckResult(passed=passed, findings=findings, output="")


def main(argv: list[str]) -> int:
    target = Path(argv[1]).resolve() if len(argv) > 1 else REPO_ROOT / "fixtures" / "foundry"

    print(f"=== Module 10 deterministic tier: {target} ===")
    print()
    result = check_module_10(target)
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
