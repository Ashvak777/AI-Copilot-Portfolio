"""
Reference Implementation — RAG retrieve-and-ground sketch.

Illustrates authorization-aware retrieval and prompt assembly.
This is not proprietary production code and does not connect to live systems.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence


@dataclass
class Chunk:
    chunk_id: str
    text: str
    source_uri: str
    score: float
    acl_groups: Sequence[str]


@dataclass
class GroundedAnswer:
    answer: str
    citations: List[str]
    refused: bool


def filter_by_acl(chunks: Iterable[Chunk], user_groups: Sequence[str]) -> List[Chunk]:
    allowed = set(user_groups)
    return [c for c in chunks if allowed.intersection(c.acl_groups)]


def retrieve(
    query_vector: Sequence[float],
    index_search,
    user_groups: Sequence[str],
    top_k: int = 5,
    min_score: float = 0.35,
    product: str | None = None,
) -> List[Chunk]:
    """Semantic retrieve + metadata/ACL filter + score threshold."""
    raw = index_search(query_vector, top_k=top_k * 3, product=product)
    authorized = filter_by_acl(raw, user_groups)
    ranked = sorted(authorized, key=lambda c: c.score, reverse=True)
    return [c for c in ranked if c.score >= min_score][:top_k]


def build_context(chunks: Sequence[Chunk]) -> str:
    blocks = []
    for i, chunk in enumerate(chunks, start=1):
        blocks.append(
            f"[S{i}] id={chunk.chunk_id} source={chunk.source_uri}\n{chunk.text}"
        )
    return "\n\n".join(blocks)


def answer_from_context(user_question: str, chunks: Sequence[Chunk], llm_complete) -> GroundedAnswer:
    if not chunks:
        return GroundedAnswer(
            answer="I could not find an approved source for that question.",
            citations=[],
            refused=True,
        )

    context = build_context(chunks)
    prompt = {
        "system": "Answer only from CONTEXT. Cite [S#]. Refuse if insufficient.",
        "context": context,
        "user": user_question,
    }
    text = llm_complete(prompt)
    citations = [c.source_uri for c in chunks]
    return GroundedAnswer(answer=text, citations=citations, refused=False)
