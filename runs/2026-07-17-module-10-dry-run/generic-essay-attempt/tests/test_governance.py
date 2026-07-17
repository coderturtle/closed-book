"""Provided test suite for Module 09's exercise (src/governance.py's
`answer_question_with_governance`/`approve_and_release`). This file is NOT
the exercise -- it's the deterministic gate. Do not edit it to make your
implementation pass. `scripts/verify_module_09.py` runs the repo's own
canonical copy of this file, not your submission's copy.

Run: cd fixtures/foundry && python3 -m pytest tests/test_governance.py -v
"""
from __future__ import annotations

from src.doc_qa import AnswerFailed, build_index
from src.governance import (
    approve_and_release,
    answer_question_with_governance,
    contains_sensitive_content,
)


class ScriptedModelClient:
    """A fake model client keyed by the QUERY text (extracted from the turn
    content answer_question builds), not call order. Records every
    (system_prompt, turn_content) pair it received."""

    def __init__(self, responses_by_query: dict):
        self._responses_by_query = dict(responses_by_query)
        self.calls: list[tuple[str, str]] = []

    def __call__(self, system_prompt: str, turn_content: str) -> dict:
        self.calls.append((system_prompt, turn_content))
        query = turn_content.rsplit("Question: ", 1)[-1]
        if query not in self._responses_by_query:
            raise AssertionError(f"ScriptedModelClient has no scripted response for query {query!r}")
        return self._responses_by_query[query]


def valid_response(answer="Here is the answer.", cited_doc_ids=None):
    return {"answer": answer, "cited_doc_ids": cited_doc_ids or []}


# ---------------------------------------------------------------------------
# contains_sensitive_content
# ---------------------------------------------------------------------------


def test_contains_sensitive_content_detects_password_marker():
    assert contains_sensitive_content("the temporary password is hunter2") is True


def test_contains_sensitive_content_detects_ssn_marker():
    """Symmetric coverage: a submission that only checks for 'password'
    (the first, easiest marker to think of) would pass a test suite that
    only ever exercised 'password' -- this checks a structurally different
    marker to catch that class of gap."""
    assert contains_sensitive_content("customer SSN on file: 000-00-0000") is True


def test_contains_sensitive_content_detects_credential_marker():
    assert contains_sensitive_content("rotate the database credential immediately") is True


def test_contains_sensitive_content_is_case_insensitive():
    assert contains_sensitive_content("New PASSWORD policy for all engineers") is True


def test_contains_sensitive_content_returns_false_for_clean_text():
    assert contains_sensitive_content("restart the deploy pipeline and check logs") is False


# ---------------------------------------------------------------------------
# answer_question_with_governance -- the human-in-the-loop gate
# ---------------------------------------------------------------------------


def test_governance_withholds_when_retrieved_content_is_sensitive():
    index = build_index(
        {"runbook": "to rotate the on call password follow these exact steps carefully today"}, chunk_size=12
    )
    client = ScriptedModelClient({})  # deliberately empty -- must never be called
    result = answer_question_with_governance("how do I rotate the on call password", index, client, top_k=2)
    assert result.requires_human_review is True
    assert result.answer is None
    assert result.review_reason is not None and result.review_reason.strip() != ""
    assert len(client.calls) == 0, "model_client must never be called when retrieved content is sensitive"


def test_governance_withholds_with_a_structurally_different_sensitive_marker():
    """Uses 'credential' instead of the 'password' example above -- the same
    symmetric-coverage discipline as the contains_sensitive_content tests,
    applied at the governance-gate level too."""
    index = build_index(
        {"runbook": "the automated system stores each rotated database credential in the vault"}, chunk_size=12
    )
    client = ScriptedModelClient({})
    result = answer_question_with_governance("where are rotated credentials stored", index, client, top_k=2)
    assert result.requires_human_review is True
    assert result.answer is None
    assert len(client.calls) == 0


def test_governance_withholds_based_on_chunk_content_even_when_the_query_itself_is_clean():
    """The query itself must never be treated as a proxy for what the
    retrieved chunk actually contains. A submission that checks
    contains_sensitive_content(query) instead of each retrieved chunk's own
    text would incorrectly ALLOW this query through: none of its own words
    are sensitive markers, even though the chunk it retrieves is flagged."""
    index = build_index(
        {"runbook": "database emergency response requires checking the credential rotation logs immediately"},
        chunk_size=12,
    )
    client = ScriptedModelClient({})  # deliberately empty -- must never be called
    result = answer_question_with_governance("database emergency response steps", index, client, top_k=2)
    assert result.requires_human_review is True
    assert result.answer is None
    assert len(client.calls) == 0, "model_client must never be called -- the retrieved chunk, not the query, is what's flagged"


def test_governance_review_reason_never_leaks_the_actual_sensitive_chunk_text():
    """A withheld review_reason exists so a human reviewer knows WHICH
    document to look at -- it must never itself carry the flagged content
    back to the original caller, or withholding the answer accomplishes
    nothing. Only doc_id-level references belong in review_reason."""
    sensitive_text = "the emergency override password for this system is hunter2-supersecret"
    index = build_index({"runbook": sensitive_text}, chunk_size=12)
    client = ScriptedModelClient({})
    result = answer_question_with_governance("emergency override password", index, client, top_k=2)
    assert result.requires_human_review is True
    assert "hunter2-supersecret" not in (result.review_reason or ""), (
        "review_reason must not leak the actual sensitive chunk content back to the caller"
    )


def test_governance_allows_a_clean_query_through_to_the_real_answer():
    index = build_index({"runbook": "restart the deploy pipeline and check the logs afterward"}, chunk_size=12)
    client = ScriptedModelClient(
        {"how do I restart the deploy pipeline": valid_response("Restart it and check logs.", ["runbook"])}
    )
    result = answer_question_with_governance("how do I restart the deploy pipeline", index, client, top_k=2)
    assert result.requires_human_review is False
    assert result.review_reason is None
    assert result.answer is not None
    assert result.answer.text == "Restart it and check logs."
    assert len(client.calls) == 1, "model_client must be called normally for a clean query"


def test_governance_withholds_when_only_one_of_several_retrieved_chunks_is_sensitive():
    """A submission that only checks the single highest-scoring chunk (or
    requires ALL retrieved chunks to be sensitive before withholding) would
    miss this -- any one flagged chunk among several retrieved must trigger
    withholding."""
    index = build_index(
        {
            "runbook-a": "restart the deploy pipeline and check the logs today",
            "runbook-b": "the emergency override password is stored in the vault",
        },
        chunk_size=12,
    )
    client = ScriptedModelClient({})
    result = answer_question_with_governance("restart deploy pipeline password override", index, client, top_k=3)
    assert result.requires_human_review is True
    assert result.answer is None
    assert len(client.calls) == 0


def test_governance_lets_answerfailed_propagate_for_a_query_that_retrieves_nothing():
    index = build_index({"runbook": "restart the deploy pipeline and check logs"}, chunk_size=12)
    client = ScriptedModelClient({})
    try:
        answer_question_with_governance("xyzzy zorbnak quuxplex", index, client, top_k=2)
        assert False, "expected AnswerFailed to propagate"
    except AnswerFailed:
        pass


def test_governance_default_top_k_is_three():
    """Mirrors doc_qa.py's own evaluate() default-top_k test: this index
    needs top_k >= 2 for the second document to even be retrieved, so a
    hardcoded top_k=1 internally would silently miss the sensitive chunk
    and wrongly allow the query through."""
    index = build_index(
        {
            "faq": "deploy pipeline restart questions and answers frequently asked",
            "runbook": "deploy deploy deploy password rotation buried at the end here",
        },
        chunk_size=12,
    )
    client = ScriptedModelClient({})
    result = answer_question_with_governance("deploy pipeline password", index, client)  # top_k omitted
    assert result.requires_human_review is True, "the default top_k must actually retrieve the sensitive chunk"
    assert result.answer is None


# ---------------------------------------------------------------------------
# approve_and_release -- the attributed human-approval path
# ---------------------------------------------------------------------------


def test_approve_and_release_requires_a_non_empty_approver_id():
    index = build_index({"runbook": "the emergency override password is in the vault"}, chunk_size=12)
    client = ScriptedModelClient({})
    try:
        approve_and_release("emergency override password", index, client, "", top_k=2)
        assert False, "expected ValueError for an empty approver_id"
    except ValueError:
        pass
    assert len(client.calls) == 0, "model_client must never be called without a valid approver_id"


def test_approve_and_release_rejects_a_whitespace_only_approver_id():
    index = build_index({"runbook": "the emergency override password is in the vault"}, chunk_size=12)
    client = ScriptedModelClient({})
    try:
        approve_and_release("emergency override password", index, client, "   ", top_k=2)
        assert False, "expected ValueError for a whitespace-only approver_id"
    except ValueError:
        pass
    assert len(client.calls) == 0


def test_approve_and_release_returns_the_real_answer_with_a_valid_approver_id():
    index = build_index({"runbook": "the emergency override password is in the vault"}, chunk_size=12)
    client = ScriptedModelClient(
        {"emergency override password": valid_response("It's in the vault.", ["runbook"])}
    )
    answer = approve_and_release("emergency override password", index, client, "sre-lead-morgan", top_k=2)
    assert answer.text == "It's in the vault."
    assert len(client.calls) == 1


def test_approve_and_release_default_top_k_is_three():
    """Every other approve_and_release test above passes top_k=2 explicitly
    -- a wrong default here would pass all of them undetected."""
    index = build_index(
        {
            "faq": "deploy pipeline restart questions and answers frequently asked",
            "runbook": "deploy deploy deploy password rotation buried at the end here",
        },
        chunk_size=12,
    )
    client = ScriptedModelClient(
        {"deploy pipeline password": valid_response("Rotate it.", ["runbook"])}
    )
    answer = approve_and_release("deploy pipeline password", index, client, "sre-lead-morgan")  # top_k omitted
    assert answer.text == "Rotate it."
