"""Module 08 exercise, part 1: a real, mostly-working documentation Q&A
system for the Platform Docs team's problem (see SPEC.md) -- retrieval-
augmented answering over internal engineering docs.

Unlike Module 07's ticket-triage classifier (a single-turn decision with no
real need for retrieval), this IS a genuine RAG use case: the corpus is
large, changes over time, and answers must be grounded in whichever version
of a document is CURRENT, not memorized. Domain 3's "RAG pipeline design"
objective has no natural artifact anywhere else in Foundry -- this module is
where it lives.

This file ships mostly working, matching Module 06's diagnose-and-fix shape:
chunking, indexing, retrieval, and grounded answer generation are all
correct as shipped. `refresh_index` has ONE real, seeded defect -- find and
fix it. It is not documented in this docstring; that's the point.

Requires Python 3.9+.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass(frozen=True)
class Chunk:
    doc_id: str
    chunk_index: int
    text: str


@dataclass
class DocIndex:
    chunks: Dict[str, List[Chunk]] = field(default_factory=dict)
    content_hashes: Dict[str, str] = field(default_factory=dict)


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def chunk_document(doc_id: str, text: str, chunk_size: int = 12) -> List[Chunk]:
    """Split a document's text into fixed-size word chunks. Deterministic:
    same doc_id + text + chunk_size always produces the same chunks, in the
    same order."""
    words = text.split()
    if not words:
        return []
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk_text = " ".join(words[i : i + chunk_size])
        chunks.append(Chunk(doc_id=doc_id, chunk_index=i // chunk_size, text=chunk_text))
    return chunks


def build_index(documents: Dict[str, str], chunk_size: int = 12) -> DocIndex:
    """Build a fresh index from scratch. Always correct by construction --
    the bug (see `refresh_index`) is specifically about INCREMENTAL updates,
    not the initial build."""
    chunks: Dict[str, List[Chunk]] = {}
    hashes: Dict[str, str] = {}
    for doc_id, text in documents.items():
        chunks[doc_id] = chunk_document(doc_id, text, chunk_size)
        hashes[doc_id] = _content_hash(text)
    return DocIndex(chunks=chunks, content_hashes=hashes)


def refresh_index(index: DocIndex, documents: Dict[str, str], chunk_size: int = 12) -> DocIndex:
    """Incrementally update an existing index against the current state of
    `documents` -- called periodically as the Platform Docs team's corpus
    changes, without paying the cost of a full rebuild every time. Must not
    mutate `index` in place, and must not re-chunk a document whose content
    is genuinely unchanged (the whole reason this exists instead of just
    calling `build_index` again). Two assumptions this function relies on,
    stated rather than silently assumed: `chunk_size` is stable across an
    index's lifecycle (it is not itself part of what `refresh_index` detects
    changing); and the `index` passed in was itself produced by `build_index`
    or a prior `refresh_index` call, not hand-constructed with inconsistent
    `chunks`/`content_hashes`."""
    new_chunks = dict(index.chunks)
    new_hashes = dict(index.content_hashes)
    for doc_id, text in documents.items():
        if doc_id not in new_chunks:
            new_chunks[doc_id] = chunk_document(doc_id, text, chunk_size)
            new_hashes[doc_id] = _content_hash(text)
    return DocIndex(chunks=new_chunks, content_hashes=new_hashes)


def score_chunk(chunk_text: str, query: str) -> float:
    """Deterministic keyword-overlap relevance score: fraction of the
    chunk's words that appear in the query (case-insensitive). No embedding
    model involved -- this exercise's own retrieval quality isn't the point
    under test; what happens when the index goes stale is."""
    query_words = set(query.lower().split())
    chunk_words = chunk_text.lower().split()
    if not query_words or not chunk_words:
        return 0.0
    overlap = sum(1 for w in chunk_words if w in query_words)
    return overlap / len(chunk_words)


@dataclass
class RetrievedChunk:
    doc_id: str
    text: str
    score: float


def retrieve(index: DocIndex, query: str, top_k: int = 3) -> List[RetrievedChunk]:
    """Return the top_k highest-scoring chunks across the whole index,
    deterministically tie-broken (doc_id, then text) so results are
    reproducible across runs."""
    scored: List[RetrievedChunk] = []
    for doc_id, chunks in index.chunks.items():
        for chunk in chunks:
            s = score_chunk(chunk.text, query)
            if s > 0:
                scored.append(RetrievedChunk(doc_id=doc_id, text=chunk.text, score=s))
    scored.sort(key=lambda c: (-c.score, c.doc_id, c.text))
    return scored[:top_k]


# Model client shape: (system_prompt, turn_content) -> raw dict with the
# model's grounded answer and which doc_ids it actually cited.
DocQAModelClient = Callable[[str, str], dict]


@dataclass
class Answer:
    text: str
    cited_doc_ids: List[str]


class AnswerFailed(Exception):
    pass


_SYSTEM_PROMPT = (
    "You are the Platform Docs team's internal documentation assistant. "
    "Answer ONLY using the provided context chunks -- never from memory or "
    "general knowledge. Cite every doc_id whose content you actually used. "
    "If the context doesn't contain enough information to answer, say so "
    "rather than guessing."
)


def answer_question(query: str, index: DocIndex, model_client: DocQAModelClient, top_k: int = 3) -> Answer:
    """Retrieve the top_k most relevant chunks, then ask the model to answer
    grounded in exactly that context. Raises AnswerFailed if retrieval finds
    nothing relevant, or if the model's response is malformed -- this
    function never fabricates an answer or a citation."""
    retrieved = retrieve(index, query, top_k=top_k)
    if not retrieved:
        raise AnswerFailed(f"no relevant documents found for query: {query!r}")
    context = "\n\n".join(f"[{c.doc_id}] {c.text}" for c in retrieved)
    turn_content = f"Context:\n{context}\n\nQuestion: {query}"
    raw = model_client(_SYSTEM_PROMPT, turn_content)
    if not isinstance(raw, dict) or "answer" not in raw or "cited_doc_ids" not in raw:
        raise AnswerFailed(f"malformed model response: {raw!r}")
    if not isinstance(raw["answer"], str) or not isinstance(raw["cited_doc_ids"], list):
        raise AnswerFailed(f"malformed model response (wrong field types): {raw!r}")
    return Answer(text=raw["answer"], cited_doc_ids=list(raw["cited_doc_ids"]))
