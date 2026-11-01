"""Regulation corpus: load source documents and split them into clause-aware chunks.

Owns: parsing the PDFs under data/regulations/, keeping clause number, heading path,
amendment/version and effective date on every chunk.

Must NOT: split a clause from its table or its proviso, or mix superseded and current text
without marking which is which. A chunk without a citable clause reference is useless here.

DECISION(ADR-0007): chunking unit (clause vs fixed size), enrichment of each chunk with its
heading path (contextual retrieval), and how superseded text is handled.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from pydantic import BaseModel


class Chunk(BaseModel):
    chunk_id: str
    text: str
    document: str
    clause_ref: str  # e.g. "Reg. X(3)(b)": whatever form the source uses
    heading_path: list[str]
    effective_from: date | None
    superseded: bool


def load_documents(directory: Path) -> list[Path]:
    raise NotImplementedError


def chunk_document(path: Path) -> list[Chunk]:
    raise NotImplementedError
