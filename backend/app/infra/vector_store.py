from uuid import UUID

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Chunk
from app.infra.db_models import ChunkRow


class PgVectorStore:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def store_chunks(self, chunks: list[Chunk]) -> None:
        rows = [
            ChunkRow(
                id=c.id,
                document_id=c.document_id,
                content=c.content,
                embedding=c.embedding,
                chunk_index=c.chunk_index,
                token_count=c.token_count,
                metadata_=c.metadata,
            )
            for c in chunks
        ]
        self._session.add_all(rows)
        await self._session.flush()

    async def search_similar(
        self, query_embedding: list[float], top_k: int = 5
    ) -> list[tuple[Chunk, float]]:
        embedding_str = "[" + ",".join(str(v) for v in query_embedding) + "]"
        stmt = (
            select(
                ChunkRow,
                (1 - ChunkRow.embedding.cosine_distance(embedding_str)).label("score"),
            )
            .order_by(text("score DESC"))
            .limit(top_k)
        )
        result = await self._session.execute(stmt)
        rows = result.all()

        return [
            (
                Chunk(
                    id=row.ChunkRow.id,
                    document_id=row.ChunkRow.document_id,
                    content=row.ChunkRow.content,
                    chunk_index=row.ChunkRow.chunk_index,
                    token_count=row.ChunkRow.token_count,
                    metadata=row.ChunkRow.metadata_,
                ),
                float(row.score),
            )
            for row in rows
        ]

    async def delete_by_document(self, document_id: UUID) -> int:
        from sqlalchemy import delete as sa_delete

        stmt = sa_delete(ChunkRow).where(ChunkRow.document_id == document_id)
        result = await self._session.execute(stmt)
        return result.rowcount
