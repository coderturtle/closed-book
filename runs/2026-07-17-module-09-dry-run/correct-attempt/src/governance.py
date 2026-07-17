"""Module 09 exercise, deliverable 1: a real human-in-the-loop governance
gate wrapped around the Platform Docs team's Q&A system (`src/doc_qa.py`).

Shipping `answer_question` to real internal users raises a real compliance
question this module's exercise is built around: some of the Platform Docs
team's own internal documents (security runbooks, credential-rotation
procedures) reference genuinely sensitive content -- API keys, passwords,
SSNs referenced in old incident writeups. `doc_qa.py` itself has no opinion
about this; it retrieves whatever scores highest and answers from it. That's
fine for Module 08's own exercise (RAG pipeline design and evaluation), but
shipping it as-is would mean any employee's question could surface sensitive
content straight into a model call and a returned answer, with no review of
any kind.

This module's governance layer sits in front of `answer_question` and
withholds an answer -- WITHOUT ever calling `model_client` -- whenever the
chunks retrieval would have surfaced contain sensitive content, requiring an
explicit, attributed human approval before the real answer is released. This
is the same "don't call the tool until verified" discipline as `resolve`'s
own `verify_before_refund_hook` from Module 04 (Part 1), here applied to
content sensitivity instead of customer identity.

Requires Python 3.9+.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from src.doc_qa import Answer, AnswerFailed, DocIndex, DocQAModelClient, answer_question, retrieve

# Deterministic keyword-based sensitive-content detector -- the same coarse,
# disclosed-as-coarse proxy discipline as doc_qa.py's own score_chunk (no
# real PII/security classifier is available in this environment). Case-
# insensitive substring match against retrieved chunk text.
SENSITIVE_MARKERS = (
    "ssn",
    "social security",
    "password",
    "api key",
    "api_key",
    "credential",
    "secret key",
)


def contains_sensitive_content(text: str) -> bool:
    """True if `text` contains any of SENSITIVE_MARKERS, case-insensitive."""
    lowered = text.lower()
    return any(marker in lowered for marker in SENSITIVE_MARKERS)


@dataclass
class GovernedAnswer:
    answer: Optional[Answer]  # None while withheld pending human review
    requires_human_review: bool
    review_reason: Optional[str]  # human-readable reason, set iff requires_human_review


def answer_question_with_governance(
    query: str, index: DocIndex, model_client: DocQAModelClient, top_k: int = 3
) -> GovernedAnswer:
    """Retrieve first (via `retrieve`, not `answer_question`) so retrieved
    context can be inspected for sensitive content BEFORE a model ever sees
    it. If any retrieved chunk contains sensitive content, `model_client`
    must NEVER be called -- return a `GovernedAnswer` with `answer=None`,
    `requires_human_review=True`, and a `review_reason` naming which
    document triggered it. Sensitive internal content should never leave
    this function ungoverned, not even to ask the model to summarize it.

    If nothing retrieved is flagged, proceed to the real
    `doc_qa.answer_question(query, index, model_client, top_k=top_k)` and
    wrap its result: `GovernedAnswer(answer=<real answer>,
    requires_human_review=False, review_reason=None)`.
    """
    retrieved = retrieve(index, query, top_k=top_k)
    if not retrieved:
        raise AnswerFailed(f"no relevant documents found for query: {query!r}")
    flagged = [c for c in retrieved if contains_sensitive_content(c.text)]
    if flagged:
        doc_ids = sorted({c.doc_id for c in flagged})
        reason = f"retrieved content from {', '.join(doc_ids)} contains sensitive markers"
        return GovernedAnswer(answer=None, requires_human_review=True, review_reason=reason)
    answer = answer_question(query, index, model_client, top_k=top_k)
    return GovernedAnswer(answer=answer, requires_human_review=False, review_reason=None)


def approve_and_release(
    query: str, index: DocIndex, model_client: DocQAModelClient, approver_id: str, top_k: int = 3
) -> Answer:
    """A human reviewer, having seen the flagged context out-of-band,
    approves release. Requires a real, non-empty `approver_id` -- raise
    `ValueError` immediately, before calling `model_client`, if it's empty
    or whitespace-only. This is the audit trail: WHO approved release of
    sensitive content, not just that someone did. On a valid `approver_id`,
    actually calls through to the real `doc_qa.answer_question` and returns
    its `Answer` -- this is the only path that ever returns the real answer
    for a query that governance flagged.
    """
    if not approver_id or not approver_id.strip():
        raise ValueError("approver_id must be a real, non-empty identifier")
    return answer_question(query, index, model_client, top_k=top_k)
