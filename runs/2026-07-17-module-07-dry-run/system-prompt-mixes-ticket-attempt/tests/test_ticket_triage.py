"""Provided test suite for Module 07's exercise (build_triage_prompt,
classify_ticket). This file is NOT the exercise -- it's the deterministic
gate. Do not edit it to make your implementation pass; if a test seems
wrong, that's itself part of the exercise (see the module README's
rubric). `scripts/verify_module_07.py` runs the repo's own canonical copy
of this file, not your submission's copy.

Run: cd fixtures/foundry && python3 -m pytest tests/test_ticket_triage.py -v
"""
from __future__ import annotations

import inspect

from src.ticket_triage import TriageFailed, build_triage_prompt, classify_ticket


class ScriptedTicketModelClient:
    """A fake model client returning a pre-scripted sequence of raw dicts,
    one per call. Records every (system_prompt, turn_content) pair it
    received so tests can assert what classify_ticket actually sent."""

    def __init__(self, responses: list[dict]):
        self._responses = list(responses)
        self.calls: list[tuple[str, str]] = []

    def __call__(self, system_prompt: str, turn_content: str) -> dict:
        self.calls.append((system_prompt, turn_content))
        if not self._responses:
            raise AssertionError("ScriptedTicketModelClient ran out of scripted responses")
        return self._responses.pop(0)


def valid_response(category="password_reset", confidence="high", detail=None):
    return {"category": category, "confidence": confidence, "detail": detail}


# ---------------------------------------------------------------------------
# build_triage_prompt -- the static, cache-friendly system prompt
# ---------------------------------------------------------------------------


def test_build_triage_prompt_returns_a_non_empty_string():
    prompt = build_triage_prompt()
    assert isinstance(prompt, str) and prompt.strip()


def test_build_triage_prompt_takes_no_arguments():
    """A zero-argument function structurally can't accept ticket-specific
    content -- part of what makes the cache-friendliness property here a
    property of the design, not just of the test suite's current inputs."""
    params = list(inspect.signature(build_triage_prompt).parameters)
    assert params == [], f"build_triage_prompt must take no arguments, got {params}"


def test_build_triage_prompt_is_stable_across_calls():
    assert build_triage_prompt() == build_triage_prompt()


# ---------------------------------------------------------------------------
# classify_ticket -- correctness
# ---------------------------------------------------------------------------


def test_classify_ticket_returns_valid_classification_on_first_try():
    client = ScriptedTicketModelClient([valid_response(category="vpn_access", confidence="high")])
    result = classify_ticket("I can't connect to the VPN from home", client)
    assert result.category == "vpn_access"
    assert result.confidence == "high"


def test_classify_ticket_calls_model_with_the_static_prompt_and_the_ticket_message():
    client = ScriptedTicketModelClient([valid_response()])
    classify_ticket("My password expired and I can't log in", client)
    assert len(client.calls) == 1
    system_prompt, turn_content = client.calls[0]
    assert system_prompt == build_triage_prompt()
    assert "My password expired and I can't log in" in turn_content


def test_classify_ticket_system_prompt_is_identical_across_different_tickets():
    """The cache-friendliness property this module exists to teach: the
    static system prompt must not vary with the ticket being classified."""
    client_a = ScriptedTicketModelClient([valid_response(category="password_reset")])
    client_b = ScriptedTicketModelClient([valid_response(category="hardware_request")])
    classify_ticket("I forgot my password", client_a)
    classify_ticket("My laptop screen is cracked, I need a replacement", client_b)
    assert client_a.calls[0][0] == client_b.calls[0][0], (
        "the system_prompt sent for two completely different tickets must be byte-identical"
    )


def test_classify_ticket_system_prompt_stays_identical_across_a_retry():
    """The harder version of the same property: even when a retry needs to
    feed back a specific validation error, that error must travel in the
    per-call turn content, never by mutating the static system prompt --
    otherwise every retry would silently break cacheability, the opposite
    of Module 02's own retry design (which regenerated its whole prompt
    each attempt, a pattern that was fine there but would defeat the point
    here)."""
    client = ScriptedTicketModelClient(
        [
            {"category": "not_a_real_category", "confidence": "high", "detail": None},
            valid_response(category="software_request"),
        ]
    )
    classify_ticket("I need a license for design software", client)
    assert len(client.calls) == 2
    first_system_prompt, _ = client.calls[0]
    second_system_prompt, second_turn_content = client.calls[1]
    assert first_system_prompt == second_system_prompt, (
        "the system_prompt must be identical on the retry -- only the turn content may change"
    )
    assert "not_a_real_category" in second_turn_content or "invalid" in second_turn_content.lower(), (
        "the retry's turn content must actually carry the specific validation error forward"
    )


def test_classify_ticket_rejects_invalid_category_and_retries():
    client = ScriptedTicketModelClient(
        [
            {"category": "not_a_real_category", "confidence": "high", "detail": None},
            valid_response(category="password_reset"),
        ]
    )
    result = classify_ticket("locked out of my account", client, max_retries=2)
    assert result.category == "password_reset"
    assert len(client.calls) == 2


def test_classify_ticket_requires_detail_for_other_category():
    client = ScriptedTicketModelClient(
        [
            {"category": "other", "confidence": "low", "detail": None},
            {"category": "other", "confidence": "low", "detail": "printer toner delivery question"},
        ]
    )
    result = classify_ticket("Where's my toner delivery?", client, max_retries=2)
    assert result.category == "other"
    assert result.detail == "printer toner delivery question"
    assert len(client.calls) == 2


def test_classify_ticket_does_not_require_detail_for_non_other_categories():
    client = ScriptedTicketModelClient([valid_response(category="vpn_access", detail=None)])
    result = classify_ticket("VPN keeps disconnecting", client)
    assert result.category == "vpn_access"
    assert result.detail is None


def test_classify_ticket_validates_confidence_enum():
    client = ScriptedTicketModelClient(
        [
            {"category": "password_reset", "confidence": "maybe", "detail": None},
            valid_response(category="password_reset", confidence="low"),
        ]
    )
    result = classify_ticket("might have the wrong password?", client, max_retries=2)
    assert result.confidence == "low"
    assert len(client.calls) == 2


def test_classify_ticket_raises_triage_failed_after_exhausting_retries():
    always_invalid = {"category": "not_real", "confidence": "high", "detail": None}
    client = ScriptedTicketModelClient([always_invalid, always_invalid, always_invalid])
    try:
        classify_ticket("garbled ticket text", client, max_retries=2)
        assert False, "expected TriageFailed to be raised"
    except TriageFailed:
        pass
    assert len(client.calls) == 3, "max_retries=2 means 3 total attempts (1 initial + 2 retries)"
