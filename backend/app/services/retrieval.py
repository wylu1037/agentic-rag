from app.domain.models import Chunk
from app.domain.ports import Embedder, Reranker, VectorRepository


class RetrievalService:
    def __init__(
        self,
        embedder: Embedder,
        vector_repo: VectorRepository,
        reranker: Reranker,
        reranker_fetch_k: int = 20,
    ) -> None:
        self._embedder = embedder
        self._vector_repo = vector_repo
        self._reranker = reranker
        self._reranker_fetch_k = max(reranker_fetch_k, 1)

    async def retrieve(self, query: str, top_k: int = 5) -> list[tuple[Chunk, float]]:
        query_embedding = await self._embedder.embed_query(query)
        fetch_k = max(top_k, self._reranker_fetch_k)
        candidates = await self._vector_repo.search_similar(query_embedding, top_k=fetch_k)
        return await self._reranker.rerank(query=query, candidates=candidates, top_k=top_k)
