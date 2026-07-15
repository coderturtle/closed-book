"""Provided test suite for Module 02's exercise (extract_refund_request,
build_extraction_prompt, FEW_SHOT_EXAMPLES).

This file is NOT the exercise -- it's the deterministic gate, same role
tests/test_tools.py's real content will play once Module 03 lands. Do not
edit it to make your implementation pass; if a test seems wrong, that's
itself part of the exercise (see the module README's rubric).

Run: cd fixtures/resolve && python3 -m pytest tests/test_extraction.py -v
"""
from __future__ import annotations

import pytest

from src.extraction import (
    FEW_SHOT_EXAMPLES,
    REASON_CATEGORIES,
    ExtractionFailed,
    ExtractionResult,
    build_extraction_prompt,
    extract_refund_request,
)


class ScriptedModelClient:
    """A fake model client returning a pre-scripted sequence of raw dicts, one
    per call. Records every call it received (the constructed prompt,
    prior_attempts) so tests can assert what the retry loop actually
    constructed and sent to the model.
    """

    def __init__(self, responses: list[dict]):
        self._responses = list(responses)
        self.calls: list[tuple[str, list[dict]]] = []

    def __call__(self, prompt: str, prior_attempts: list[dict]) -> dict:
        # Snapshot prior_attempts (shallow copy of the list, not its dict
        # contents) so a later mutation of the *same* list object by a buggy
        # implementation can't silently rewrite what we recorded here.
        self.calls.append((prompt, list(prior_attempts)))
        if not self._responses:
            raise AssertionError("ScriptedModelClient ran out of scripted responses")
        return self._responses.pop(0)


# ---------------------------------------------------------------------------
# Core extraction behavior (correctness, honesty, retry)
# ---------------------------------------------------------------------------


def test_clean_message_extracts_correctly():
    client = ScriptedModelClient(
        [
            {
                "refund_amount_cents": 4599,
                "reason_category": "defective_item",
                "reason_detail": None,
                "confidence": "high",
            }
        ]
    )
    result = extract_refund_request("The lamp I bought for $45.99 arrived broken.", client)
    assert result == ExtractionResult(4599, "defective_item", None, "high")
    assert len(client.calls) == 1


def test_no_amount_mentioned_is_none_not_fabricated():
    """The message never states a dollar figure -- the result must say so
    honestly (None), not guess a plausible-looking number."""
    client = ScriptedModelClient(
        [
            {
                "refund_amount_cents": None,
                "reason_category": "late_delivery",
                "reason_detail": None,
                "confidence": "high",
            }
        ]
    )
    result = extract_refund_request("My order still hasn't arrived, it's been two weeks.", client)
    assert result.refund_amount_cents is None
    assert result.reason_category == "late_delivery"


def test_ambiguous_reason_maps_to_other_with_detail():
    """A reason that doesn't fit any explicit category must land in 'other'
    with a real, non-empty reason_detail -- not silently dropped or forced
    into the nearest wrong category."""
    client = ScriptedModelClient(
        [
            {
                "refund_amount_cents": 1200,
                "reason_category": "other",
                "reason_detail": "customer says the packaging was offensive, unrelated to the product itself",
                "confidence": "low",
            }
        ]
    )
    result = extract_refund_request(
        "I want a refund, the box had something printed on it I found offensive.", client
    )
    assert result.reason_category == "other"
    assert result.reason_detail
    assert result.reason_detail.strip() != ""


def test_other_without_detail_is_rejected_and_retried():
    """'other' with a missing or empty reason_detail is a schema violation,
    not a valid extraction -- 'other' means the model has something specific
    to say that doesn't fit the fixed categories; saying nothing defeats the
    category's whole purpose."""
    client = ScriptedModelClient(
        [
            {
                "refund_amount_cents": 800,
                "reason_category": "other",
                "reason_detail": "",  # empty -- invalid
                "confidence": "low",
            },
            {
                "refund_amount_cents": 800,
                "reason_category": "other",
                "reason_detail": "customer wants a refund for reasons unrelated to the product",
                "confidence": "low",
            },
        ]
    )
    result = extract_refund_request("Some unusual complaint.", client)
    assert result.reason_detail
    assert len(client.calls) == 2


def test_invalid_confidence_value_is_rejected_and_retried():
    """confidence must be exactly 'high' or 'low' -- any other value
    (including a plausible-looking one like 'medium') is a schema violation."""
    client = ScriptedModelClient(
        [
            {
                "refund_amount_cents": 300,
                "reason_category": "wrong_item",
                "reason_detail": None,
                "confidence": "medium",  # not a valid value
            },
            {
                "refund_amount_cents": 300,
                "reason_category": "wrong_item",
                "reason_detail": None,
                "confidence": "low",
            },
        ]
    )
    result = extract_refund_request("Wrong item, not sure how much though.", client)
    assert result.confidence == "low"
    assert len(client.calls) == 2


def test_wrong_type_amount_is_rejected_and_retried():
    """refund_amount_cents must be an int or None -- a string that merely
    looks numeric is a schema violation, not an acceptable value."""
    client = ScriptedModelClient(
        [
            {
                "refund_amount_cents": "twenty dollars",  # wrong type
                "reason_category": "wrong_item",
                "reason_detail": None,
                "confidence": "high",
            },
            {
                "refund_amount_cents": 2000,
                "reason_category": "wrong_item",
                "reason_detail": None,
                "confidence": "high",
            },
        ]
    )
    result = extract_refund_request("Wrong item, refund $20.", client)
    assert result.refund_amount_cents == 2000
    assert len(client.calls) == 2


def test_invalid_first_response_retries_with_error_fed_back():
    """First response is missing a required field. The implementation must
    retry, and the retry's prior_attempts must actually carry the earlier
    failure forward -- not just blindly re-ask the same question."""
    client = ScriptedModelClient(
        [
            {"refund_amount_cents": 2000, "confidence": "high"},  # missing reason_category
            {
                "refund_amount_cents": 2000,
                "reason_category": "wrong_item",
                "reason_detail": None,
                "confidence": "high",
            },
        ]
    )
    result = extract_refund_request("Wrong item, refund the $20.", client)
    assert result.reason_category == "wrong_item"
    assert len(client.calls) == 2
    # The second call must have been told about the first failure.
    _, prior_attempts_on_retry = client.calls[1]
    assert len(prior_attempts_on_retry) == 1
    assert "error" in prior_attempts_on_retry[0]
    assert prior_attempts_on_retry[0]["error"]  # non-empty, names something real
    assert "response" in prior_attempts_on_retry[0]  # the raw failed response, not just the error string
    # The first call must have seen an empty history -- if the implementation
    # shares and mutates the same list object across calls instead of a fresh
    # snapshot per attempt, this would now (wrongly) show the retry's entry.
    _, prior_attempts_on_first_call = client.calls[0]
    assert prior_attempts_on_first_call == []


def test_invalid_category_value_is_rejected_and_retried():
    """The model returns a reason_category outside REASON_CATEGORIES. This is
    a schema violation, not a valid 'other' -- must retry, not silently
    accept an invented category."""
    client = ScriptedModelClient(
        [
            {
                "refund_amount_cents": 500,
                "reason_category": "customer_is_annoyed",  # not a real category
                "reason_detail": None,
                "confidence": "high",
            },
            {
                "refund_amount_cents": 500,
                "reason_category": "changed_mind",
                "reason_detail": None,
                "confidence": "high",
            },
        ]
    )
    result = extract_refund_request("Never mind, I don't want it anymore, refund my $5.", client)
    assert result.reason_category == "changed_mind"
    assert len(client.calls) == 2


def test_exhausting_retries_raises_not_silently_returns_garbage():
    """Every attempt is invalid. The function must raise, not return a
    best-effort guess built from garbage, and must actually use all the
    retries it's given -- not give up early."""
    client = ScriptedModelClient(
        [
            {"reason_category": "other"},  # missing required fields
            {"reason_category": "other"},
            {"reason_category": "other"},
        ]
    )
    with pytest.raises(ExtractionFailed):
        extract_refund_request("garbled message", client, max_retries=2)
    # max_retries=2 means exactly 1 initial attempt + 2 retries = 3 calls total
    # -- not fewer (giving up early) and not more (ignoring the limit).
    assert len(client.calls) == 3


def test_max_retries_zero_makes_exactly_one_attempt_then_raises():
    """max_retries=0 means no retries at all: one attempt, and if it fails,
    raise immediately."""
    client = ScriptedModelClient([{"reason_category": "other"}])  # invalid, no retry available
    with pytest.raises(ExtractionFailed):
        extract_refund_request("garbled", client, max_retries=0)
    assert len(client.calls) == 1


def test_extra_unexpected_fields_are_tolerated():
    """A response with unrelated extra keys shouldn't crash the parser --
    only the required schema fields matter."""
    client = ScriptedModelClient(
        [
            {
                "refund_amount_cents": 999,
                "reason_category": "defective_item",
                "reason_detail": None,
                "confidence": "high",
                "internal_debug_note": "model thinking trace, ignore this",
            }
        ]
    )
    result = extract_refund_request("Broken item, $9.99 refund please.", client)
    assert result.refund_amount_cents == 999


# ---------------------------------------------------------------------------
# Prompt construction (Task Statements 4.1, 4.2, 4.4 -- the actual prompt-
# engineering artifact this module is about, not just the retry wrapper)
# ---------------------------------------------------------------------------


def test_prompt_names_schema_fields_and_categories():
    """The prompt must state the schema explicitly (Task Statement 4.1:
    explicit criteria beat vague instructions) -- every required field name
    and every valid category should appear somewhere in it."""
    prompt = build_extraction_prompt("My lamp arrived broken, refund $45.99.", [])
    for field in ("refund_amount_cents", "reason_category", "reason_detail", "confidence"):
        assert field in prompt
    for category in REASON_CATEGORIES:
        assert category in prompt


def test_few_shot_examples_are_present_and_well_formed():
    """At least 2 few-shot examples exist, each with a message and an
    expected structured output -- presence and shape are deterministic;
    whether they demonstrate a genuinely ambiguous case (not just clean
    textbook messages) is the conceptual tier's job, see the module rubric."""
    assert len(FEW_SHOT_EXAMPLES) >= 2
    for example in FEW_SHOT_EXAMPLES:
        assert "message" in example and isinstance(example["message"], str) and example["message"]
        assert "expected" in example and isinstance(example["expected"], dict)
        for field in ("refund_amount_cents", "reason_category", "reason_detail", "confidence"):
            assert field in example["expected"]


def test_retry_prompt_embeds_the_specific_prior_error():
    """On retry, the constructed prompt must actually embed the specific
    validation error from the failed attempt -- not just carry it in
    prior_attempts unused. A model can't correct a mistake it was never told
    about, even if the data was technically passed along somewhere."""
    client = ScriptedModelClient(
        [
            {"refund_amount_cents": 2000, "confidence": "high"},  # missing reason_category
            {
                "refund_amount_cents": 2000,
                "reason_category": "wrong_item",
                "reason_detail": None,
                "confidence": "high",
            },
        ]
    )
    extract_refund_request("Wrong item, refund the $20.", client)
    retry_prompt, prior_attempts_on_retry = client.calls[1]
    error_text = prior_attempts_on_retry[0]["error"]
    assert error_text in retry_prompt
