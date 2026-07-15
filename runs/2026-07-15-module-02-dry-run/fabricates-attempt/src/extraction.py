"""Structured extraction from freeform customer messages. Authored for real in
Module 02 (Prompts and Structured Output That Survive Production).

resolve's agent (Module 04) needs to turn a customer's freeform message into a
structured request before any tool call can happen: how much refund are they
asking for, and why. This module is where that extraction gets built --
before there's an agentic loop to feed it, and before the real MCP tools
(Module 03) exist to act on it.

The model call itself is injected as `model_client` so the deterministic test
suite can supply canned responses without a live API call -- same shape as
Module 01's checker never actually running Claude Code, just checking the
configuration a learner would produce.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional

REASON_CATEGORIES = ["defective_item", "wrong_item", "late_delivery", "changed_mind", "other"]

ModelClient = Callable[[str, List[dict]], dict]

FEW_SHOT_EXAMPLES: List[dict] = [
    {
        "message": "The lamp I bought for $45.99 arrived broken.",
        "expected": {
            "refund_amount_cents": 4599,
            "reason_category": "defective_item",
            "reason_detail": None,
            "confidence": "high",
        },
    },
    {
        "message": "This isn't what I ordered, just take it back.",
        "expected": {
            "refund_amount_cents": None,
            "reason_category": "wrong_item",
            "reason_detail": None,
            "confidence": "low",
        },
    },
]


def build_extraction_prompt(message: str, prior_attempts: List[dict]) -> str:
    lines = [
        "Extract: refund_amount_cents, reason_category "
        f"(one of {REASON_CATEGORIES}), reason_detail, confidence.",
    ]
    for ex in FEW_SHOT_EXAMPLES:
        lines.append(f"- {ex['message']!r} -> {ex['expected']}")
    lines.append(f"Message: {message!r}")
    if prior_attempts:
        lines.append(f"Previous error: {prior_attempts[-1]['error']}")
    return "\n".join(lines)


@dataclass
class ExtractionResult:
    refund_amount_cents: Optional[int]
    reason_category: str
    reason_detail: Optional[str]
    confidence: str  # "high" or "low"


class ExtractionFailed(Exception):
    """Raised when the model client never produces a schema-valid response
    within max_retries -- never silently returned as a best-effort guess."""


def _validate(raw: dict) -> str | None:
    if "reason_category" not in raw:
        return "missing reason_category"
    if raw["reason_category"] not in REASON_CATEGORIES:
        return f"invalid reason_category: {raw['reason_category']}"
    if "refund_amount_cents" not in raw:
        return "missing refund_amount_cents"
    amount = raw["refund_amount_cents"]
    if amount is not None and not isinstance(amount, int):
        return f"refund_amount_cents must be an int or null, got {type(amount).__name__}"
    if "confidence" not in raw or raw["confidence"] not in ("high", "low"):
        return "missing or invalid confidence"
    if raw["reason_category"] == "other" and not raw.get("reason_detail"):
        return "reason_category is 'other' but reason_detail is missing or empty"
    return None


def extract_refund_request(
    message: str, model_client: ModelClient, max_retries: int = 2
) -> ExtractionResult:
    prior_attempts: list[dict] = []
    for _ in range(max_retries + 1):
        prompt = build_extraction_prompt(message, prior_attempts)
        raw = model_client(prompt, prior_attempts)
        error = _validate(raw)
        if error is None:
            return ExtractionResult(
                # `or 0` treats an explicit, honest null the same as a missing
                # key -- collapsing "the model said there's no amount" into
                # "assume zero," which isn't the same claim.
                refund_amount_cents=raw.get("refund_amount_cents") or 0,
                reason_category=raw["reason_category"],
                reason_detail=raw.get("reason_detail"),
                confidence=raw["confidence"],
            )
        prior_attempts.append({"response": raw, "error": error})
    raise ExtractionFailed(f"failed after {max_retries + 1} attempts")
