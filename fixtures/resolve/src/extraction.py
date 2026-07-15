"""Structured extraction from freeform customer messages. Authored for real in
Module 02 (Prompts and Structured Output That Survive Production).

resolve's agent (Module 04) needs to turn a customer's freeform message into a
structured request before any tool call can happen: how much refund are they
asking for, and why. This module is where that extraction gets built --
before there's an agentic loop to feed it, and before the real MCP tools
(Module 03) exist to act on it.

Requires Python 3.9+ (uses PEP 585 generic subscripting, e.g. list[dict], in
non-annotation position -- `from __future__ import annotations` only defers
evaluation of annotations, not the direct ModelClient assignment below).

The model call itself is injected as `model_client` so the deterministic test
suite can supply canned responses without a live API call -- same shape as
Module 01's checker never actually running Claude Code, just checking the
configuration a learner would produce. What IS real, and graded, is the
prompt construction: `build_extraction_prompt` and `FEW_SHOT_EXAMPLES` are the
actual prompt-engineering artifact this module is about -- `model_client`
receives the constructed prompt, not the raw message, so there's something
real for the conceptual-tier rubric to grade (see the module README).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional

REASON_CATEGORIES = ["defective_item", "wrong_item", "late_delivery", "changed_mind", "other"]

# A model client is a callable: (prompt, prior_attempts) -> raw dict, where
# prompt is what build_extraction_prompt constructed (not the raw customer
# message -- see below) and prior_attempts is a list of {"response": dict,
# "error": str} from earlier retries in this same call (empty on the first
# attempt). Real implementations call the Claude API with tool_use and a JSON
# schema; the test suite supplies a fake one that returns canned dicts, so the
# retry-loop logic is testable without a live API call.
ModelClient = Callable[[str, List[dict]], dict]

# The few-shot examples your prompt should embed. At least one MUST demonstrate
# a genuinely ambiguous case (a message that doesn't name its category
# explicitly, or bundles multiple issues) -- not only clean, textbook messages.
# See the module README's rubric criterion 3 and CCA-F Task Statement 4.2.
FEW_SHOT_EXAMPLES: List[dict] = []


def build_extraction_prompt(message: str, prior_attempts: List[dict]) -> str:
    """Construct the prompt sent to the model: the schema fields and valid
    categories (explicit criteria, Task Statement 4.1), the few-shot examples
    above, the customer's message, and -- on a retry -- the specific prior
    validation error, so the model can actually correct the mistake instead
    of guessing what went wrong (Task Statement 4.4).
    """
    raise NotImplementedError("Module 02's exercise: implement the prompt construction.")


@dataclass
class ExtractionResult:
    refund_amount_cents: Optional[int]
    reason_category: str
    reason_detail: Optional[str]
    confidence: str  # "high" or "low"


class ExtractionFailed(Exception):
    """Raised when the model client never produces a schema-valid response
    within max_retries -- never silently returned as a best-effort guess."""


def extract_refund_request(
    message: str, model_client: ModelClient, max_retries: int = 2
) -> ExtractionResult:
    raise NotImplementedError("Module 02's exercise: implement the extraction + retry loop.")
