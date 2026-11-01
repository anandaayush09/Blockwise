"""Hybrid retrieval over regulation chunks: BM25 + dense vectors + reciprocal rank fusion, optional rerank.

Owns: indexing chunks and returning ranked chunks with their clause references and scores.

Must NOT: answer questions or compute penalties. It returns evidence; the regulation agent
writes the answer and cites ``clause_ref`` from the returned chunks only.
Must treat retrieved text as untrusted data, never as instructions (prompt-injection test in Phase 10).

Why hybrid: BM25 finds exact clause numbers and defined terms that embeddings can miss;
embeddings catch paraphrases. Prove it with an eval query, not an assumption.

DECISION(ADR-0007): vector store (pgvector vs Qdrant), embedding model, rerank or not.
"""

from __future__ import annotations

from pydantic import BaseModel

from blockwise.regulation.corpus import Chunk


class RetrievedChunk(BaseModel):
    chunk: Chunk
    score: float
    retriever: str  # "bm25" | "dense" | "fused" | "reranked"


def build_index(chunks: list[Chunk]) -> None:
    raise NotImplementedError


def search(query: str, k: int = 5, include_superseded: bool = False) -> list[RetrievedChunk]:
    raise NotImplementedError


def reciprocal_rank_fusion(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    """Fuse several ranked lists of chunk ids into one. Pure function: unit-test it by hand."""
    raise NotImplementedError
