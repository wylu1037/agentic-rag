import re

from app.domain.models import Chunk
from app.domain.ports import Reranker


class NoopReranker:
    async def rerank(
        self, query: str, candidates: list[tuple[Chunk, float]], top_k: int
    ) -> list[tuple[Chunk, float]]:
        del query
        return candidates[:top_k]


class HeuristicReranker(Reranker):
    def __init__(self, lexical_weight: float = 0.25) -> None:
        self._lexical_weight = lexical_weight

    async def rerank(
        self, query: str, candidates: list[tuple[Chunk, float]], top_k: int
    ) -> list[tuple[Chunk, float]]:
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return candidates[:top_k]

        scored: list[tuple[Chunk, float]] = []
        for chunk, dense_score in candidates:
            chunk_tokens = self._tokenize(chunk.content)
            overlap = 0.0
            if chunk_tokens:
                overlap = len(query_tokens & chunk_tokens) / len(query_tokens)
            final_score = (1 - self._lexical_weight) * dense_score + self._lexical_weight * overlap
            scored.append((chunk, final_score))

        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        return {token.lower() for token in re.findall(r"\w+", text)}
