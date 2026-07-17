"""Provided test suite for Module 08's exercise (src/doc_qa.py's
`refresh_index` fix, and src/evaluation.py's `evaluate`/`compare_top_k`).
This file is NOT the exercise -- it's the deterministic gate. Do not edit it
to make your implementation pass. `scripts/verify_module_08.py` runs the
repo's own canonical copy of this file, not your submission's copy.

Run: cd fixtures/foundry && python3 -m pytest tests/test_doc_qa.py -v
"""
from __future__ import annotations

from unittest.mock import patch

from src.doc_qa import (
    AnswerFailed,
    Chunk,
    DocIndex,
    answer_question,
    build_index,
    chunk_document,
    refresh_index,
    retrieve,
    score_chunk,
)
from src.evaluation import EvalCase, compare_top_k, evaluate


class ScriptedDocQAModelClient:
    """A fake model client keyed by the QUERY text (extracted from the turn
    content `answer_question` builds), not call order -- so the evaluation
    harness can call it for several different queries in any order and each
    still gets its own scripted response. Records every (system_prompt,
    turn_content) pair it received."""

    def __init__(self, responses_by_query: dict):
        self._responses_by_query = dict(responses_by_query)
        self.calls: list[tuple[str, str]] = []

    def __call__(self, system_prompt: str, turn_content: str) -> dict:
        self.calls.append((system_prompt, turn_content))
        query = turn_content.rsplit("Question: ", 1)[-1]
        if query not in self._responses_by_query:
            raise AssertionError(f"ScriptedDocQAModelClient has no scripted response for query {query!r}")
        return self._responses_by_query[query]


class GroundedScriptedModelClient:
    """A model client that always 'sees' its full context and cites every
    doc_id that actually appears in it -- simulating an honest model that
    can only cite what it was actually shown. Unlike
    ScriptedDocQAModelClient (keyed by query text alone, ignoring context),
    this one's answer genuinely depends on what retrieval put in front of
    it, which is what makes a top_k A/B comparison meaningful rather than
    a structural pass-through check."""

    def __init__(self):
        self.calls: list[tuple[str, str]] = []

    def __call__(self, system_prompt: str, turn_content: str) -> dict:
        self.calls.append((system_prompt, turn_content))
        cited = []
        for line in turn_content.split("\n"):
            if line.startswith("[") and "]" in line:
                doc_id = line[1 : line.index("]")]
                if doc_id not in cited:
                    cited.append(doc_id)
        return {"answer": "grounded answer", "cited_doc_ids": cited}


# ---------------------------------------------------------------------------
# chunk_document / build_index / score_chunk / retrieve -- shipped, correct
# ---------------------------------------------------------------------------


def test_chunk_document_splits_into_fixed_size_word_chunks():
    text = "one two three four five six seven eight nine ten eleven twelve thirteen"
    chunks = chunk_document("doc-a", text, chunk_size=12)
    assert len(chunks) == 2
    assert chunks[0].text == "one two three four five six seven eight nine ten eleven twelve"
    assert chunks[1].text == "thirteen"
    assert chunks[0].doc_id == "doc-a" and chunks[1].doc_id == "doc-a"
    assert chunks[0].chunk_index == 0 and chunks[1].chunk_index == 1


def test_chunk_document_on_empty_text_returns_no_chunks():
    assert chunk_document("doc-a", "", chunk_size=12) == []


def test_chunk_document_default_chunk_size_is_twelve():
    """Every other chunk_document/build_index/refresh_index test passes
    chunk_size=12 explicitly -- a submission with a wrong default would
    pass all of them undetected."""
    text = "one two three four five six seven eight nine ten eleven twelve thirteen"
    chunks = chunk_document("doc-a", text)  # chunk_size omitted -- must default to 12
    assert len(chunks) == 2
    assert chunks[0].text == "one two three four five six seven eight nine ten eleven twelve"
    assert chunks[1].text == "thirteen"


def test_build_index_indexes_every_document():
    index = build_index({"doc-a": "alpha beta gamma", "doc-b": "delta epsilon"}, chunk_size=12)
    assert set(index.chunks.keys()) == {"doc-a", "doc-b"}
    assert index.chunks["doc-a"][0].text == "alpha beta gamma"
    assert "doc-a" in index.content_hashes and "doc-b" in index.content_hashes


def test_score_chunk_counts_keyword_overlap():
    assert score_chunk("rollback the deploy now", "how do I rollback a deploy") > 0
    assert score_chunk("completely unrelated text here", "rollback a deploy") == 0.0


def test_retrieve_returns_highest_scoring_chunks_first():
    index = build_index(
        {
            "runbook": "to roll back a deploy run the rollback command",
            "onboarding": "new engineers request vpn access during week one",
        },
        chunk_size=12,
    )
    results = retrieve(index, "how do I roll back a deploy", top_k=1)
    assert len(results) == 1
    assert results[0].doc_id == "runbook"


def test_retrieve_respects_top_k():
    index = build_index(
        {
            "a": "rollback deploy procedure one",
            "b": "rollback deploy procedure two",
            "c": "rollback deploy procedure three",
        },
        chunk_size=12,
    )
    assert len(retrieve(index, "rollback deploy procedure", top_k=2)) == 2


# ---------------------------------------------------------------------------
# answer_question -- shipped, correct
# ---------------------------------------------------------------------------


def test_answer_question_grounds_the_call_in_retrieved_context_and_cites_it():
    index = build_index({"runbook": "to roll back a deploy run the rollback command now"}, chunk_size=12)
    client = ScriptedDocQAModelClient(
        {"how do I roll back a deploy": {"answer": "Run the rollback command.", "cited_doc_ids": ["runbook"]}}
    )
    result = answer_question("how do I roll back a deploy", index, client)
    assert result.text == "Run the rollback command."
    assert result.cited_doc_ids == ["runbook"]
    assert len(client.calls) == 1
    system_prompt, turn_content = client.calls[0]
    assert "runbook" in turn_content and "roll back a deploy" in turn_content
    assert "ONLY using the provided context" in system_prompt


def test_answer_question_raises_when_nothing_relevant_is_retrieved():
    index = build_index({"runbook": "to roll back a deploy run the rollback command"}, chunk_size=12)
    client = ScriptedDocQAModelClient({})
    try:
        answer_question("xyzzy zorbnak quuxplex", index, client)  # zero keyword overlap, deliberately
        assert False, "expected AnswerFailed to be raised"
    except AnswerFailed:
        pass
    assert len(client.calls) == 0, "model_client must never be called when retrieval finds nothing"


def test_answer_question_raises_on_malformed_model_response():
    index = build_index({"runbook": "to roll back a deploy run the rollback command"}, chunk_size=12)
    client = ScriptedDocQAModelClient({"how do I roll back a deploy": {"answer": "Run it."}})  # missing cited_doc_ids
    try:
        answer_question("how do I roll back a deploy", index, client)
        assert False, "expected AnswerFailed to be raised"
    except AnswerFailed:
        pass


def test_answer_question_raises_when_cited_doc_ids_is_not_a_list():
    """A response with cited_doc_ids as a bare string (e.g. "runbook"
    instead of ["runbook"]) is still technically iterable -- without a real
    type check, list("runbook") silently becomes character-by-character
    citations (['r', 'u', 'n', ...]) instead of raising."""
    index = build_index({"runbook": "to roll back a deploy run the rollback command"}, chunk_size=12)
    client = ScriptedDocQAModelClient({"how do I roll back a deploy": {"answer": "Run it.", "cited_doc_ids": "runbook"}})
    try:
        answer_question("how do I roll back a deploy", index, client)
        assert False, "expected AnswerFailed for a non-list cited_doc_ids"
    except AnswerFailed:
        pass


# ---------------------------------------------------------------------------
# refresh_index -- diagnose and fix: one seeded defect
# ---------------------------------------------------------------------------


def test_refresh_index_adds_a_brand_new_document():
    index = build_index({"runbook": "old rollback procedure text here"}, chunk_size=12)
    updated = refresh_index(index, {"runbook": "old rollback procedure text here", "onboarding": "new hire vpn setup guide"}, chunk_size=12)
    assert "onboarding" in updated.chunks
    assert updated.chunks["onboarding"][0].text == "new hire vpn setup guide"


def test_refresh_index_updates_changed_document_content():
    """The core diagnose-and-fix test: a document whose doc_id already
    exists in the index, but whose CONTENT has changed, must have its
    chunks (and content hash) actually updated -- otherwise the system
    keeps answering from a stale, superseded version of the doc forever."""
    index = build_index({"runbook": "old rollback procedure run command alpha"}, chunk_size=12)
    updated = refresh_index(index, {"runbook": "new rollback procedure run command beta"}, chunk_size=12)
    assert updated.chunks["runbook"][0].text == "new rollback procedure run command beta", (
        "refresh_index must re-chunk a document whose content changed, not just "
        "check whether its doc_id is already present in the index"
    )


def test_refresh_index_updates_the_content_hash_on_change():
    index = build_index({"runbook": "old rollback procedure run command alpha"}, chunk_size=12)
    original_hash = index.content_hashes["runbook"]
    updated = refresh_index(index, {"runbook": "new rollback procedure run command beta"}, chunk_size=12)
    assert updated.content_hashes["runbook"] != original_hash


def test_refresh_index_leaves_a_genuinely_unchanged_document_untouched():
    index = build_index({"runbook": "rollback procedure run command alpha"}, chunk_size=12)
    updated = refresh_index(index, {"runbook": "rollback procedure run command alpha"}, chunk_size=12)
    assert updated.chunks["runbook"] == index.chunks["runbook"]


def test_refresh_index_preserves_a_document_absent_from_the_incoming_dict():
    index = build_index({"runbook": "rollback text", "onboarding": "vpn setup text"}, chunk_size=12)
    updated = refresh_index(index, {"runbook": "rollback text updated now"}, chunk_size=12)
    assert "onboarding" in updated.chunks
    assert updated.chunks["onboarding"] == index.chunks["onboarding"]


def test_refresh_index_does_not_recompute_chunks_for_a_genuinely_unchanged_document():
    """A full-rebuild-every-call implementation (re-chunking every document
    on every refresh, regardless of whether its content changed) would pass
    every other refresh_index test above -- a frozen Chunk re-derived to an
    identical value is still value-equal to the original. This is the only
    test that actually distinguishes 'skipped the unnecessary work' from
    'redid the unnecessary work and got the same answer', which matters
    because refresh_index exists specifically as a cheaper alternative to
    calling build_index again (see its own docstring)."""
    index = build_index({"runbook": "rollback procedure alpha", "onboarding": "vpn setup guide beta"}, chunk_size=12)
    with patch("src.doc_qa.chunk_document", wraps=chunk_document) as spy:
        refresh_index(
            index,
            {"runbook": "rollback procedure alpha", "onboarding": "vpn setup guide UPDATED now"},
            chunk_size=12,
        )
        # Robust to a correct implementation calling chunk_document with keyword
        # args (chunk_document(doc_id=..., text=..., chunk_size=...)) instead of
        # positionally -- call.args[0] alone would IndexError on that, a false
        # failure against correct code, not just a missed detection of buggy code.
        called_doc_ids = []
        for call in spy.call_args_list:
            args, kwargs = call
            called_doc_ids.append(args[0] if args else kwargs.get("doc_id"))
    assert "onboarding" in called_doc_ids, "the changed document must be re-chunked"
    assert "runbook" not in called_doc_ids, "a genuinely unchanged document must NOT be re-chunked"


def test_refresh_index_does_not_mutate_the_original_index_object():
    """A refresh_index that mutates its input `index` in place and returns
    that same object would pass every other refresh_index test above too --
    they all compare the RETURNED index against the original, which is
    tautological if they're literally the same object. This test keeps its
    own snapshot of the original values taken BEFORE the call."""
    index = build_index({"runbook": "old rollback procedure alpha"}, chunk_size=12)
    original_text = index.chunks["runbook"][0].text
    original_hash = index.content_hashes["runbook"]
    refresh_index(index, {"runbook": "new rollback procedure beta"}, chunk_size=12)
    assert index.chunks["runbook"][0].text == original_text, "refresh_index must not mutate its input index in place"
    assert index.content_hashes["runbook"] == original_hash


def test_refresh_index_returned_chunk_lists_are_independent_of_the_original():
    """Even a refresh_index that correctly returns a NEW DocIndex object can
    still share the underlying List[Chunk] objects for unchanged documents
    with the original index (a shallow dict copy alone does this). Mutating
    the returned index's list must not be visible through the original."""
    index = build_index({"runbook": "rollback procedure alpha"}, chunk_size=12)
    updated = refresh_index(index, {"runbook": "rollback procedure alpha"}, chunk_size=12)  # unchanged
    poison = Chunk(doc_id="runbook", chunk_index=99, text="poison")
    updated.chunks["runbook"].append(poison)
    assert poison not in index.chunks["runbook"], (
        "mutating the returned index's chunk list must not affect the original index's list"
    )


def test_refresh_index_stale_content_is_no_longer_retrievable_after_a_fix():
    """End-to-end version of the same property, through retrieve() rather
    than inspecting DocIndex internals directly -- the actual user-facing
    symptom of the seeded bug."""
    index = build_index({"runbook": "step one restart the legacy service manually"}, chunk_size=12)
    updated = refresh_index(index, {"runbook": "step one run the automated rollback script"}, chunk_size=12)
    results = retrieve(updated, "automated rollback script", top_k=1)
    assert results and "automated rollback script" in results[0].text
    stale_results = retrieve(updated, "restart the legacy service manually", top_k=1)
    assert not stale_results or "legacy service" not in stale_results[0].text


# ---------------------------------------------------------------------------
# evaluate -- build from stub
# ---------------------------------------------------------------------------


def _small_index():
    return build_index(
        {
            "runbook": "to roll back a deploy run the rollback command now",
            "onboarding": "new engineers request vpn access during their first week",
        },
        chunk_size=12,
    )


def test_evaluate_counts_correct_and_incorrect_cases():
    index = _small_index()
    client = ScriptedDocQAModelClient(
        {
            "how do I roll back a deploy": {"answer": "Run the rollback command.", "cited_doc_ids": ["runbook"]},
            "how do I get vpn access": {"answer": "Run the rollback command.", "cited_doc_ids": ["runbook"]},  # wrong
        }
    )
    dataset = [
        EvalCase(query="how do I roll back a deploy", expected_doc_id="runbook"),
        EvalCase(query="how do I get vpn access", expected_doc_id="onboarding"),
    ]
    result = evaluate(index, client, dataset, top_k=2)
    assert result.total == 2
    assert result.correct == 1
    assert result.accuracy == 0.5
    assert result.failures == ["how do I get vpn access"]


def test_evaluate_requires_the_specific_expected_doc_not_just_any_citation():
    """Guards against a too-lenient metric ('cited anything -> correct')
    that would silently overstate real accuracy."""
    index = _small_index()
    client = ScriptedDocQAModelClient(
        {"how do I roll back a deploy": {"answer": "See onboarding.", "cited_doc_ids": ["onboarding"]}}
    )
    dataset = [EvalCase(query="how do I roll back a deploy", expected_doc_id="runbook")]
    result = evaluate(index, client, dataset, top_k=2)
    assert result.correct == 0
    assert result.accuracy == 0.0
    assert result.failures == ["how do I roll back a deploy"]


def test_evaluate_all_correct_gives_accuracy_one_and_no_failures():
    index = _small_index()
    client = ScriptedDocQAModelClient(
        {"how do I roll back a deploy": {"answer": "Run it.", "cited_doc_ids": ["runbook"]}}
    )
    dataset = [EvalCase(query="how do I roll back a deploy", expected_doc_id="runbook")]
    result = evaluate(index, client, dataset, top_k=2)
    assert result.accuracy == 1.0
    assert result.failures == []


def test_evaluate_a_citation_list_with_the_expected_doc_plus_extras_still_counts_correct():
    index = _small_index()
    client = ScriptedDocQAModelClient(
        {"how do I roll back a deploy": {"answer": "See both.", "cited_doc_ids": ["onboarding", "runbook"]}}
    )
    dataset = [EvalCase(query="how do I roll back a deploy", expected_doc_id="runbook")]
    result = evaluate(index, client, dataset, top_k=2)
    assert result.correct == 1


def test_evaluate_on_an_empty_dataset_returns_zero_total_with_no_division_error():
    index = _small_index()
    client = ScriptedDocQAModelClient({})
    result = evaluate(index, client, [], top_k=2)
    assert result.total == 0
    assert result.correct == 0
    assert result.accuracy == 0.0
    assert result.failures == []
    assert len(client.calls) == 0


def test_evaluate_failures_preserve_dataset_order_not_sorted_or_deduplicated():
    """The only other multi-case test has exactly one failure, so a
    submission that silently sorts or deduplicates `failures` would still
    pass it. This dataset has two failures in an order that differs from
    alphabetical, to catch exactly that."""
    index = _small_index()
    client = ScriptedDocQAModelClient(
        {
            # both queries deliberately retrieve something real (so evaluate calls
            # model_client and gets a wrong-but-present citation back, rather than
            # AnswerFailed propagating for an unrelated reason)
            "zzz roll back a deploy": {"answer": "wrong", "cited_doc_ids": ["onboarding"]},
            "aaa vpn access request": {"answer": "wrong", "cited_doc_ids": ["runbook"]},
        }
    )
    dataset = [
        EvalCase(query="zzz roll back a deploy", expected_doc_id="runbook"),
        EvalCase(query="aaa vpn access request", expected_doc_id="onboarding"),
    ]
    result = evaluate(index, client, dataset, top_k=2)
    assert result.failures == ["zzz roll back a deploy", "aaa vpn access request"], (
        "failures must preserve dataset order, not be sorted or deduplicated"
    )


def test_evaluate_default_top_k_is_three():
    """Every other evaluate test above passes top_k explicitly -- a
    submission with a wrong default (e.g. top_k: int = 1) would pass all of
    them undetected. This index needs top_k >= 2 for the expected chunk to
    even be retrieved, so a wrong default of 1 would fail this case."""
    index = build_index(
        {
            "runbook": "deploy deploy deploy rollback procedure buried at the end here",
            "faq": "rollback questions and answers frequently asked",
        },
        chunk_size=12,
    )
    client = GroundedScriptedModelClient()
    dataset = [EvalCase(query="rollback", expected_doc_id="runbook")]
    result = evaluate(index, client, dataset)  # top_k omitted -- must default to 3
    assert result.accuracy == 1.0


def test_evaluate_respects_a_non_default_top_k_directly():
    """`test_evaluate_default_top_k_is_three` only proves the DEFAULT is 3 --
    it doesn't prove `evaluate` actually reads its own `top_k` parameter
    rather than hardcoding 3 internally (which would look identical for
    every other test above, including compare_top_k's own tests, if
    compare_top_k were implemented as an independent reimplementation
    rather than a genuine delegation to evaluate). This calls evaluate
    directly with an explicit non-default top_k=1, where retrieval
    genuinely only returns the wrong document -- a hardcoded-top_k=3
    evaluate would wrongly report accuracy=1.0 here."""
    index = build_index(
        {
            "runbook": "deploy deploy deploy rollback procedure buried at the end here",
            "faq": "rollback questions and answers frequently asked",
        },
        chunk_size=12,
    )
    client = GroundedScriptedModelClient()
    dataset = [EvalCase(query="rollback", expected_doc_id="runbook")]
    result = evaluate(index, client, dataset, top_k=1)
    assert result.accuracy == 0.0, "evaluate must actually use its own top_k parameter, not a hardcoded default"


def test_evaluate_failures_includes_every_failing_case_even_duplicate_queries():
    """No other dataset above has two cases sharing the identical query
    string, so a submission that deduplicates `failures` (e.g. via
    dict.fromkeys) would pass every other test undetected."""
    index = _small_index()
    client = ScriptedDocQAModelClient(
        {"how do I roll back a deploy": {"answer": "wrong", "cited_doc_ids": ["onboarding"]}}
    )
    dataset = [
        EvalCase(query="how do I roll back a deploy", expected_doc_id="runbook"),
        EvalCase(query="how do I roll back a deploy", expected_doc_id="runbook"),
    ]
    result = evaluate(index, client, dataset, top_k=2)
    assert result.total == 2
    assert result.failures == ["how do I roll back a deploy", "how do I roll back a deploy"], (
        "failures must include every failing case, not deduplicate identical queries"
    )


def test_evaluate_lets_answerfailed_propagate_rather_than_silently_marking_incorrect():
    """If a case's query retrieves nothing at all, that's a different,
    louder signal than a wrong citation -- it should surface as a crash,
    not get silently averaged into the accuracy number as just another
    incorrect case."""
    index = _small_index()
    client = ScriptedDocQAModelClient({})
    dataset = [EvalCase(query="xyzzy zorbnak quuxplex", expected_doc_id="runbook")]  # zero keyword overlap
    try:
        evaluate(index, client, dataset, top_k=2)
        assert False, "expected AnswerFailed to propagate out of evaluate"
    except AnswerFailed:
        pass


def test_evaluate_uses_real_retrieved_context_not_just_the_raw_query():
    """A broken evaluate that talks to model_client directly with just the
    query (bypassing answer_question's real retrieval/context-construction
    path) would pass every test above that uses ScriptedDocQAModelClient,
    since that double ignores context entirely. GroundedScriptedModelClient
    only cites doc_ids that actually appear in the context it was shown, so
    this only passes if evaluate genuinely routes through real retrieval."""
    index = build_index({"runbook": "how to roll back a deploy safely"}, chunk_size=12)
    client = GroundedScriptedModelClient()
    dataset = [EvalCase(query="roll back a deploy", expected_doc_id="runbook")]
    result = evaluate(index, client, dataset, top_k=2)
    assert result.correct == 1


# ---------------------------------------------------------------------------
# compare_top_k -- the module's A/B testing artifact
# ---------------------------------------------------------------------------


def test_compare_top_k_returns_one_result_keyed_by_each_k_value():
    index = _small_index()
    client = ScriptedDocQAModelClient(
        {"how do I roll back a deploy": {"answer": "Run it.", "cited_doc_ids": ["runbook"]}}
    )
    dataset = [EvalCase(query="how do I roll back a deploy", expected_doc_id="runbook")]
    results = compare_top_k(index, client, dataset, k_values=[1, 2])
    assert set(results.keys()) == {1, 2}
    assert results[1].total == 1 and results[2].total == 1


def test_compare_top_k_evaluates_the_full_dataset_for_every_k_not_a_subset():
    """Every other compare_top_k test above uses a single-case dataset --
    an implementation that quietly evaluates only dataset[:1] regardless of
    k would still pass them. This dataset has two cases, so a subset-only
    implementation reports the wrong total/correct count."""
    index = _small_index()
    client = ScriptedDocQAModelClient(
        {
            "how do I roll back a deploy": {"answer": "a", "cited_doc_ids": ["runbook"]},
            "how do I get vpn access": {"answer": "b", "cited_doc_ids": ["onboarding"]},
        }
    )
    dataset = [
        EvalCase(query="how do I roll back a deploy", expected_doc_id="runbook"),
        EvalCase(query="how do I get vpn access", expected_doc_id="onboarding"),
    ]
    results = compare_top_k(index, client, dataset, k_values=[2])
    assert results[2].total == 2, "compare_top_k must evaluate the full dataset for each k, not a subset"
    assert results[2].correct == 2


def test_compare_top_k_a_lower_k_can_genuinely_score_worse():
    """Real behavioral A/B difference, not just a structural check: with
    top_k=1, retrieval for this query returns only the single
    highest-scoring chunk, which belongs to the WRONG document -- the
    correct document only enters the top results once top_k is raised.
    Uses GroundedScriptedModelClient specifically because its answer
    genuinely depends on what retrieval put in context, unlike the flat
    query-keyed double used above."""
    index = build_index(
        {
            "runbook": "deploy deploy deploy rollback procedure buried at the end here",
            "faq": "rollback questions and answers frequently asked",
        },
        chunk_size=12,
    )
    client = GroundedScriptedModelClient()
    dataset = [EvalCase(query="rollback", expected_doc_id="runbook")]
    results = compare_top_k(index, client, dataset, k_values=[1, 2])
    assert results[1].accuracy <= results[2].accuracy
    assert results[1].accuracy == 0.0
    assert results[2].accuracy == 1.0
