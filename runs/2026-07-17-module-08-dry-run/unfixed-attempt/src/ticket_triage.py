"""Module 07 exercise: a real, working ticket-triage classifier for the
Helpdesk team's problem (see SPEC.md), built around the specific design
tension this module exists to teach -- recognizing when a well-designed
prompt beats an agentic loop, not just how to build the agentic loop.

The Helpdesk team's first instinct was "we want something like resolve"
(Part 1's multi-tool agentic coordinator). This module's exercise is the
alternative: most of their ~4,000 tickets/month are single-turn structured
classification decisions with no real need for multi-step tool use or
agentic autonomy. `classify_ticket` is a single-turn workflow, deliberately
not an agentic loop -- and its prompt structure is deliberately
cache-friendly, since the exam guide's own Sample Question 2 (a large,
repeatedly-sent static system prompt) is exactly this shape.

Requires Python 3.9+.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional

TICKET_CATEGORIES = ("password_reset", "vpn_access", "software_request", "hardware_request", "other")

TicketModelClient = Callable[[str, str], dict]


@dataclass
class TicketClassification:
    category: str
    confidence: str
    detail: Optional[str]


class TriageFailed(Exception):
    pass


_STATIC_TRIAGE_PROMPT = """You are the Foundry Helpdesk ticket-triage classifier.

Classify each incoming IT ticket into exactly one category:
- password_reset: the employee is locked out or needs a password reset.
- vpn_access: VPN connectivity, network access, or remote-access issues.
- software_request: requests for new software installs or license grants.
- hardware_request: requests for new or replacement hardware.
- other: anything that does not clearly fit the above four categories.

Respond with a JSON object: {"category": <one of the five categories above>,
"confidence": "high" or "low", "detail": a short string if category is
"other" (required and non-empty in that case), otherwise null.

Rules:
- If the ticket is ambiguous between two categories, prefer "other" with
  confidence "low" and a detail explaining the ambiguity, rather than
  guessing between the two.
- Never fabricate a category outside the five listed above.
"""


def build_triage_prompt() -> str:
    """Returns the static, cache-friendly system prompt: IT policy text and
    the category definitions every ticket is classified against."""
    return _STATIC_TRIAGE_PROMPT


def _validate(raw: dict) -> Optional[str]:
    if not isinstance(raw, dict):
        return f"expected a JSON object, got {type(raw).__name__}"
    if "category" not in raw:
        return "missing required field: category"
    if raw["category"] not in TICKET_CATEGORIES:
        return f"category {raw['category']!r} is not one of {TICKET_CATEGORIES}"
    if "confidence" not in raw or raw["confidence"] not in ("high", "low"):
        return "missing or invalid confidence (must be 'high' or 'low')"
    if raw["category"] == "other" and not (raw.get("detail") or "").strip():
        return "category is 'other' but detail is missing or empty"
    return None


def classify_ticket(
    ticket_message: str, model_client: TicketModelClient, max_retries: int = 2
) -> TicketClassification:
    """Classify one Helpdesk ticket."""
    if max_retries < 0:
        raise ValueError(f"max_retries must be >= 0, got {max_retries}")
    system_prompt = build_triage_prompt()
    prior_attempts: List[dict] = []

    for _ in range(max_retries + 1):
        turn_content = ticket_message
        if prior_attempts:
            last_error = prior_attempts[-1]["error"]
            turn_content = (
                f"{ticket_message}\n\nYour previous attempt was invalid: {last_error}. "
                "Correct this and try again."
            )
        raw = model_client(system_prompt, turn_content)
        error = _validate(raw)
        if error is None:
            return TicketClassification(
                category=raw["category"], confidence=raw["confidence"], detail=raw.get("detail")
            )
        prior_attempts.append({"response": raw, "error": error})

    raise TriageFailed(
        f"could not classify ticket after {max_retries + 1} attempts: {prior_attempts[-1]['error']}"
    )
