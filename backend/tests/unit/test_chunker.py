from uuid import uuid4

from app.infra.chunker import HeadingAwareChunker


class TestHeadingAwareChunker:
    def test_splits_by_heading(self, sample_markdown: str) -> None:
        chunker = HeadingAwareChunker(chunk_size=512, chunk_overlap=64)
        chunks = chunker.chunk(sample_markdown, "README.md", uuid4())

        assert len(chunks) > 0
        headings = [c.metadata.get("heading_path", "") for c in chunks]
        assert any("路线 A" in h for h in headings)
        assert any("路线 B" in h for h in headings)

    def test_chunk_metadata_has_source_section(self, sample_markdown: str) -> None:
        chunker = HeadingAwareChunker(chunk_size=512, chunk_overlap=64)
        chunks = chunker.chunk(sample_markdown, "README.md", uuid4())

        for chunk in chunks:
            assert "source_section" in chunk.metadata
            assert "heading_path" in chunk.metadata
            assert chunk.metadata["source"] == "README.md"

    def test_chunk_indexes_are_sequential(self, sample_markdown: str) -> None:
        chunker = HeadingAwareChunker(chunk_size=512, chunk_overlap=64)
        chunks = chunker.chunk(sample_markdown, "test.md", uuid4())

        indexes = [c.chunk_index for c in chunks]
        assert indexes == list(range(len(chunks)))

    def test_small_chunk_size_splits_further(self) -> None:
        text = "# Title\n\n" + "word " * 200
        chunker = HeadingAwareChunker(chunk_size=50, chunk_overlap=10)
        chunks = chunker.chunk(text, "test.md", uuid4())

        assert len(chunks) > 1
        for chunk in chunks:
            assert chunk.token_count > 0

    def test_plain_text_without_headings(self) -> None:
        text = "这是一段没有标题的纯文本内容。"
        chunker = HeadingAwareChunker(chunk_size=512, chunk_overlap=64)
        chunks = chunker.chunk(text, "plain.txt", uuid4())

        assert len(chunks) == 1
        assert chunks[0].metadata["heading_path"] == ""
