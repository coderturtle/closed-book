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

from src.ticket_triage import (
    TICKET_CATEGORIES,
    TriageFailed,
    build_triage_prompt,
    classify_ticket,
)


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


def test_build_triage_prompt_mentions_all_five_categories():
    """A prompt that's technically non-empty, stable, and zero-argument but
    says nothing about the actual categories (e.g. `return "classify"`) would
    satisfy every other test above -- this closes that gap with a real,
    if coarse, content floor."""
    prompt = build_triage_prompt().lower()
    for category in TICKET_CATEGORIES:
        assert category in prompt, f"the triage prompt must mention the {category!r} category"


def test_ticket_categories_is_immutable():
    """TICKET_CATEGORIES must be a tuple, not a list -- the same defensive
    convention `fixtures/resolve/src/tool_errors.py`'s ERROR_CATEGORIES
    already established, so the allowed-category contract can't be silently
    mutated by any importer."""
    assert isinstance(TICKET_CATEGORIES, tuple), "TICKET_CATEGORIES must be a tuple, not a mutable list"


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
    assert client_a.calls[0][0] == build_triage_prompt(), (
        "the system_prompt sent must actually BE build_triage_prompt()'s own output, not just "
        "some other value that happens to be identical across the two calls in this test"
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
    first_system_prompt, first_turn_content = client.calls[0]
    second_system_prompt, second_turn_content = client.calls[1]
    assert first_system_prompt == second_system_prompt == build_triage_prompt(), (
        "the system_prompt must be identical on the retry, and must actually BE "
        "build_triage_prompt()'s own output -- only the turn content may change"
    )
    assert "not_a_real_category" in second_turn_content, (
        "the retry's turn content must carry the SPECIFIC validation error forward (the actual "
        "invalid category value), not a generic 'that was invalid, try again' placeholder -- a "
        "generic retry message would leave the model no better informed than before"
    )
    assert "I need a license for design software" in second_turn_content, (
        "the retry's turn content must still carry the original ticket text, not just the error"
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


def test_classify_ticket_respects_a_non_default_max_retries():
    """Every other retry-count test above uses either the default (2) or the
    literal value 2 explicitly -- a hardcoded `for _ in range(3):` that
    ignores the max_retries argument entirely (as long as it still guards
    negative values) would pass every one of them undetected. This uses a
    different value (4) to confirm the argument is actually read, not just
    present in the signature."""
    always_invalid = {"category": "not_real", "confidence": "high", "detail": None}
    client = ScriptedTicketModelClient([always_invalid] * 5)
    try:
        classify_ticket("garbled ticket text", client, max_retries=4)
        assert False, "expected TriageFailed to be raised"
    except TriageFailed:
        pass
    assert len(client.calls) == 5, "max_retries=4 means 5 total attempts (1 initial + 4 retries)"


def test_classify_ticket_default_max_retries_is_two():
    """The signature's documented default (`max_retries: int = 2`) must
    actually be exercised somewhere -- every other exhaustion/retry-count
    test above passes max_retries explicitly, so a submission changing the
    real default (e.g. to 999) would pass every one of them undetected."""
    always_invalid = {"category": "not_real", "confidence": "high", "detail": None}
    client = ScriptedTicketModelClient([always_invalid, always_invalid, always_invalid])
    try:
        classify_ticket("garbled ticket text", client)  # max_retries omitted -- must default to 2
        assert False, "expected TriageFailed to be raised"
    except TriageFailed:
        pass
    assert len(client.calls) == 3, "the default max_retries=2 means 3 total attempts"


def test_classify_ticket_calls_model_client_again_for_a_repeated_identical_ticket():
    """No test above ever classifies the same ticket text twice -- an
    implementation that memoizes on ticket_message and skips calling
    model_client on a repeat would pass every other test while silently
    never re-classifying a retried webhook or duplicate submission."""
    client = ScriptedTicketModelClient([valid_response(category="vpn_access"), valid_response(category="vpn_access")])
    classify_ticket("VPN drops every few minutes", client)
    classify_ticket("VPN drops every few minutes", client)
    assert len(client.calls) == 2, "model_client must be called again even for an identical ticket_message"


def test_classify_ticket_retries_past_a_non_dict_model_response():
    """A model_client is only a Callable[[str, str], dict] by type hint, not
    by runtime enforcement -- a malformed response (e.g. a parse failure
    upstream returning None) must be treated as a validation failure and
    retried, not crash classify_ticket outright."""
    client = ScriptedTicketModelClient([None, valid_response(category="hardware_request")])
    result = classify_ticket("need a new monitor", client, max_retries=2)
    assert result.category == "hardware_request"
    assert len(client.calls) == 2


def test_classify_ticket_rejects_whitespace_only_detail_for_other_category():
    """A whitespace-only detail (e.g. " ") is falsy-adjacent but not actually
    `None`/empty by a naive `not raw.get("detail")` check -- it carries no
    real information and must be rejected the same way a missing detail is."""
    client = ScriptedTicketModelClient(
        [
            {"category": "other", "confidence": "low", "detail": "   "},
            {"category": "other", "confidence": "low", "detail": "vending machine is out of order"},
        ]
    )
    result = classify_ticket("the vending machine ate my money", client, max_retries=2)
    assert result.detail == "vending machine is out of order"
    assert len(client.calls) == 2


def test_classify_ticket_raises_value_error_for_negative_max_retries():
    """max_retries=-1 must fail clearly and immediately (before ever calling
    model_client), not fall through the retry loop into an implementation
    detail like an IndexError on an empty prior-attempts list."""
    client = ScriptedTicketModelClient([])
    try:
        classify_ticket("locked out again", client, max_retries=-1)
        assert False, "expected ValueError to be raised"
    except ValueError:
        pass
    assert len(client.calls) == 0, "model_client must never be called when max_retries is invalid"
