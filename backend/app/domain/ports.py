from collections.abc import AsyncIterator
from typing import Protocol
from uuid import UUID

from app.domain.models import Chunk, Document


class DocumentRepository(Protocol):
    async def save(self, doc: Document) -> Document: ...
    async def get(self, doc_id: UUID) -> Document | None: ...
    async def delete(self, doc_id: UUID) -> bool: ...


class VectorRepository(Protocol):
    async def store_chunks(self, chunks: list[Chunk]) -> None: ...
    async def search_similar(
        self, query_embedding: list[float], top_k: int = 5
    ) -> list[tuple[Chunk, float]]: ...


class Embedder(Protocol):
    async def embed_texts(self, texts: list[str]) -> list[list[float]]: ...
    async def embed_query(self, query: str) -> list[float]: ...


class LLMClient(Protocol):
    async def generate(self, messages: list[dict], system_prompt: str = "") -> str: ...
    async def generate_stream(
        self, messages: list[dict], system_prompt: str = ""
    ) -> AsyncIterator[str]: ...


class DocumentParser(Protocol):
    def parse(self, content: bytes | str, filename: str) -> str: ...


class TextChunker(Protocol):
    def chunk(self, text: str, source: str, doc_id: UUID) -> list[Chunk]: ...
