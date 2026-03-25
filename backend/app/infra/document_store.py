from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Document
from app.infra.db_models import DocumentRow


class PgDocumentStore:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, doc: Document) -> Document:
        row = DocumentRow(
            id=doc.id,
            title=doc.title,
            source=doc.source,
            content=doc.content,
            content_type=doc.content_type,
            metadata_=doc.metadata,
        )
        self._session.add(row)
        await self._session.flush()
        return doc

    async def get(self, doc_id: UUID) -> Document | None:
        row = await self._session.get(DocumentRow, doc_id)
        if row is None:
            return None
        return Document(
            id=row.id,
            title=row.title,
            source=row.source,
            content=row.content,
            content_type=row.content_type,
            metadata=row.metadata_,
            created_at=row.created_at,
        )

    async def delete(self, doc_id: UUID) -> bool:
        row = await self._session.get(DocumentRow, doc_id)
        if row is None:
            return False
        await self._session.delete(row)
        await self._session.flush()
        return True
