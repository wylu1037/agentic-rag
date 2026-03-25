import pytest

from app.infra.chunker import HeadingAwareChunker
from app.infra.parser import MarkdownParser
from app.services.ingest import IngestService


@pytest.mark.asyncio
async def test_ingest_service(
    sample_markdown, mock_embedder, mock_doc_repo, mock_vector_repo
) -> None:
    service = IngestService(
        parser=MarkdownParser(),
        chunker=HeadingAwareChunker(chunk_size=512, chunk_overlap=64),
        embedder=mock_embedder,
        doc_repo=mock_doc_repo,
        vector_repo=mock_vector_repo,
    )

    doc = await service.ingest(sample_markdown, "README.md")

    assert doc.title == "README.md"
    assert doc.chunk_count > 0
    mock_doc_repo.save.assert_called_once()
    mock_embedder.embed_texts.assert_called_once()
    mock_vector_repo.store_chunks.assert_called_once()
