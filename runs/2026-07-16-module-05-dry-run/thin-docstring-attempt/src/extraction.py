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
        # Ambiguous: no explicit category word, no dollar amount stated.
        "message": "This isn't what I ordered, I don't even know what to do with it, just take it back.",
        "expected": {
            "refund_amount_cents": None,
            "reason_category": "wrong_item",
            "reason_detail": None,
            "confidence": "low",
        },
    },
    {
        "message": "The box had something printed on it I found offensive, I don't want it in my house.",
        "expected": {
            "refund_amount_cents": None,
            "reason_category": "other",
            "reason_detail": "customer objects to packaging content, unrelated to product quality",
            "confidence": "low",
        },
    },
]


def build_extraction_prompt(message: str, prior_attempts: List[dict]) -> str:
    lines = [
        "Extract a structured refund request from the customer message below.",
        "Required fields: refund_amount_cents (int or null), reason_category "
        f"(one of {REASON_CATEGORIES}), reason_detail (string, required and non-empty "
        "if reason_category is 'other', otherwise null), confidence ('high' or 'low').",
        "",
        "Examples:",
    ]
    for ex in FEW_SHOT_EXAMPLES:
        lines.append(f"- Message: {ex['message']!r} -> {ex['expected']}")
    lines.append("")
    lines.append(f"Customer message: {message!r}")
    if prior_attempts:
        last_error = prior_attempts[-1]["error"]
        lines.append("")
        lines.append(f"Your previous attempt was invalid: {last_error}. Correct this and try again.")
    return "\n".join(lines)


@dataclass
class ExtractionResult:
    refund_amount_cents: Optional[int]
    reason_category: str
    reason_detail: Optional[str]
    confidence: str


class ExtractionFailed(Exception):
    pass


def _validate(raw: dict) -> str | None:
    if "reason_category" not in raw:
        return "missing required field: reason_category"
    if raw["reason_category"] not in REASON_CATEGORIES:
        return f"reason_category '{raw['reason_category']}' is not one of {REASON_CATEGORIES}"
    if "refund_amount_cents" not in raw:
        return "missing required field: refund_amount_cents (use null if not stated in the message)"
    amount = raw["refund_amount_cents"]
    if amount is not None and not isinstance(amount, int):
        return f"refund_amount_cents must be an int or null, got {type(amount).__name__}: {amount!r}"
    if "confidence" not in raw or raw["confidence"] not in ("high", "low"):
        return "missing or invalid confidence (must be 'high' or 'low')"
    if raw["reason_category"] == "other" and not raw.get("reason_detail"):
        return "reason_category is 'other' but reason_detail is missing or empty"
    return None


def extract_refund_request(
    message: str, model_client: ModelClient, max_retries: int = 2
) -> ExtractionResult:
    if max_retries < 0:
        raise ValueError("max_retries must be >= 0")
    prior_attempts: list[dict] = []
    for _ in range(max_retries + 1):
        prompt = build_extraction_prompt(message, prior_attempts)
        raw = model_client(prompt, prior_attempts)
        error = _validate(raw)
        if error is None:
            return ExtractionResult(
                refund_amount_cents=raw["refund_amount_cents"],
                reason_category=raw["reason_category"],
                reason_detail=raw.get("reason_detail"),
                confidence=raw["confidence"],
            )
        prior_attempts.append({"response": raw, "error": error})
    raise ExtractionFailed(
        f"could not extract a valid structured request after {max_retries + 1} attempts: "
        f"{prior_attempts[-1]['error']}"
    )
