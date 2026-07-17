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

Requires Python 3.9+ (see fixtures/resolve/src/extraction.py's note on why
`from __future__ import annotations` alone doesn't cover PEP 585 generic
subscripting outside annotation position, if this module ever needs it).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

TICKET_CATEGORIES = ("password_reset", "vpn_access", "software_request", "hardware_request", "other")

# Model client shape: (system_prompt, ticket_message) -> raw dict. Deliberately
# two separate arguments, not one concatenated string -- the static system
# prompt and the per-ticket message are structurally distinct inputs, mirroring
# how the real Claude API separates a `system` prompt from turn content. A
# model_client that receives them pre-concatenated has already lost the
# information needed to cache the static portion.
TicketModelClient = Callable[[str, str], dict]


@dataclass
class TicketClassification:
    category: str
    confidence: str  # "high" or "low"
    detail: Optional[str]  # required and non-empty if category == "other"


class TriageFailed(Exception):
    pass


def build_triage_prompt() -> str:
    """Returns the static, cache-friendly system prompt: IT policy text and
    the category definitions every ticket is classified against. Takes NO
    arguments -- this is deliberate, not an oversight. The entire
    cache-friendliness property this module's tests check is that this
    prompt is byte-identical across every call to `classify_ticket`,
    regardless of which ticket is being classified. A function that could
    take a ticket-specific argument would make it possible (even if
    unintentional) to let per-ticket content leak into the supposedly-static
    portion; a zero-argument function makes that mistake structurally
    harder to make, though `classify_ticket` itself is still what the tests
    actually check the real behavior against.

    Must return the same non-empty string on every call. What it says is
    yours to write (real IT policy framing, the five categories above,
    and the classification instructions) -- the property under test is
    that it doesn't change, not its specific wording.
    """
    raise NotImplementedError("Module 07's exercise: write the static, cache-friendly system prompt.")


def classify_ticket(
    ticket_message: str, model_client: TicketModelClient, max_retries: int = 2
) -> TicketClassification:
    """Classify one Helpdesk ticket. Must call `model_client(system_prompt,
    ticket_message)` with `system_prompt` set to `build_triage_prompt()`'s
    own output, unmodified, on every call -- the static prompt and the
    per-ticket message are passed as two separate arguments, never merged
    into one string before the call. Validates the raw response against
    the category schema (`category` must be one of `TICKET_CATEGORIES`;
    `confidence` must be "high" or "low"; `detail` is required and
    non-empty -- whitespace-only doesn't count -- when `category == "other"`,
    otherwise it may be absent or `None`), retrying with the specific
    validation error fed back to the model on failure -- the same
    validate-and-retry discipline `fixtures/resolve/src/extraction.py`'s
    `extract_refund_request` established in Module 02. A malformed response
    (not even a dict) must be treated as a validation failure and retried,
    not allowed to crash the function. Raises `TriageFailed` rather than
    fabricate a result after exhausting `max_retries`. `max_retries < 0` is a
    caller error: raise `ValueError` immediately, before ever calling
    `model_client`.
    """
    raise NotImplementedError("Module 07's exercise: implement the triage classifier.")
