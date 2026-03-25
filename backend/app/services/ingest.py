from app.domain.models import Document
from app.domain.ports import (
    DocumentParser,
    DocumentRepository,
    Embedder,
    TextChunker,
    VectorRepository,
)


class IngestService:
    def __init__(
        self,
        parser: DocumentParser,
        chunker: TextChunker,
        embedder: Embedder,
        doc_repo: DocumentRepository,
        vector_repo: VectorRepository,
    ) -> None:
        self._parser = parser
        self._chunker = chunker
        self._embedder = embedder
        self._doc_repo = doc_repo
        self._vector_repo = vector_repo

    async def ingest(self, content: str | bytes, filename: str, source: str = "") -> Document:
        text = self._parser.parse(content, filename)

        doc = Document(
            title=filename,
            source=source or filename,
            content=text,
            content_type=self._detect_type(filename),
        )
        doc = await self._doc_repo.save(doc)

        chunks = self._chunker.chunk(text, doc.source, doc.id)

        if chunks:
            texts = [c.content for c in chunks]
            embeddings = await self._embedder.embed_texts(texts)
            for chunk, emb in zip(chunks, embeddings, strict=True):
                chunk.embedding = emb

            await self._vector_repo.store_chunks(chunks)

        doc.chunk_count = len(chunks)
        return doc

    @staticmethod
    def _detect_type(filename: str) -> str:
        lower = filename.lower()
        if lower.endswith(".md"):
            return "markdown"
        if lower.endswith(".txt"):
            return "text"
        if lower.endswith(".pdf"):
            return "pdf"
        return "text"
