"""Module 08 exercise, part 2: a real evaluation harness for the Platform
Docs team's Q&A system (`src/doc_qa.py`) -- a labeled dataset, an accuracy
metric, and an A/B comparison across a real configuration choice (`top_k`).

This is the second of Module 08's two required deliverables. The first
(fixing `refresh_index`'s seeded staleness bug in `doc_qa.py`) is a
diagnose-and-fix exercise; this one is build-from-stub, like Module 07's
`ticket_triage.py`. Together they cover Domain 4's "evaluation metric
design," "A/B testing," and "diagnosing system issues" objectives with real
artifacts, not just checkpoint questions.

Requires Python 3.9+.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from src.doc_qa import DocIndex, DocQAModelClient, answer_question


@dataclass(frozen=True)
class EvalCase:
    query: str
    expected_doc_id: str  # a correct answer must cite this doc_id


@dataclass
class EvalResult:
    total: int
    correct: int
    accuracy: float
    failures: List[str] = field(default_factory=list)  # queries that failed, for debugging


def evaluate(
    index: DocIndex, model_client: DocQAModelClient, dataset: List[EvalCase], top_k: int = 3
) -> EvalResult:
    """Run every case in `dataset` through `answer_question`, and score each
    one correct if and only if `case.expected_doc_id` appears in the
    returned answer's `cited_doc_ids` -- citing SOME doc is not enough; it
    must be the specific doc the case expects. Must return an `EvalResult`
    with `total` equal to `len(dataset)`, `correct` equal to the number of
    matching cases, `accuracy` equal to `correct / total`, and `failures`
    containing the `query` string of every case that did NOT match, in the
    same order they were evaluated.
    """
    correct = 0
    failures: List[str] = []
    for case in dataset:
        answer = answer_question(case.query, index, model_client, top_k=top_k)
        if case.expected_doc_id in answer.cited_doc_ids:
            correct += 1
        else:
            failures.append(case.query)
    total = len(dataset)
    accuracy = correct / total if total else 0.0
    return EvalResult(total=total, correct=correct, accuracy=accuracy, failures=failures)


def compare_top_k(
    index: DocIndex, model_client: DocQAModelClient, dataset: List[EvalCase], k_values: List[int]
) -> Dict[int, EvalResult]:
    """Run `evaluate` once per value in `k_values` (same index, same
    model_client, same dataset -- only `top_k` varies), and return a dict
    mapping each `k` to its own `EvalResult`. This is the module's A/B
    testing artifact: the same evaluation harness run under two or more
    real configurations, so their accuracy can be directly compared.
    """
    return {k: evaluate(index, model_client, dataset, top_k=k) for k in k_values}
