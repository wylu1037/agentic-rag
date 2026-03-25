from app.domain.models import Chunk
from app.domain.ports import Embedder, VectorRepository


class RetrievalService:
    def __init__(self, embedder: Embedder, vector_repo: VectorRepository) -> None:
        self._embedder = embedder
        self._vector_repo = vector_repo

    async def retrieve(self, query: str, top_k: int = 5) -> list[tuple[Chunk, float]]:
        query_embedding = await self._embedder.embed_query(query)
        return await self._vector_repo.search_similar(query_embedding, top_k=top_k)
