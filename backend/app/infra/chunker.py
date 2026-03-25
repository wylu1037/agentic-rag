import re
import unicodedata
from uuid import UUID

import tiktoken

from app.domain.models import Chunk


def _slugify(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[^\w\s\u4e00-\u9fff-]", "", text)
    text = re.sub(r"[\s]+", "-", text.strip())
    return text.lower()


class HeadingAwareChunker:
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 64) -> None:
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        self._enc = tiktoken.get_encoding("cl100k_base")

    def _token_count(self, text: str) -> int:
        return len(self._enc.encode(text))

    def chunk(self, text: str, source: str, doc_id: UUID) -> list[Chunk]:
        sections = self._split_by_headings(text)
        chunks: list[Chunk] = []
        idx = 0

        for heading_path, section_slug, section_text in sections:
            sub_chunks = self._split_section(section_text)
            for sub in sub_chunks:
                token_count = self._token_count(sub)
                chunks.append(
                    Chunk(
                        document_id=doc_id,
                        content=sub,
                        chunk_index=idx,
                        token_count=token_count,
                        metadata={
                            "heading_path": heading_path,
                            "source_section": section_slug,
                            "source": source,
                        },
                    )
                )
                idx += 1

        return chunks

    def _split_by_headings(self, text: str) -> list[tuple[str, str, str]]:
        heading_re = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
        sections: list[tuple[str, str, str]] = []
        heading_stack: list[tuple[int, str]] = []
        last_pos = 0
        last_heading_path = ""
        last_slug = ""

        for match in heading_re.finditer(text):
            if last_pos < match.start():
                section_text = text[last_pos : match.start()].strip()
                if section_text:
                    sections.append((last_heading_path, last_slug, section_text))

            level = len(match.group(1))
            title = match.group(2).strip()

            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()
            heading_stack.append((level, title))

            last_heading_path = " > ".join(h[1] for h in heading_stack)
            last_slug = _slugify(title)
            last_pos = match.end()

        trailing = text[last_pos:].strip()
        if trailing:
            sections.append((last_heading_path, last_slug, trailing))

        if not sections and text.strip():
            sections.append(("", "", text.strip()))

        return sections

    def _split_section(self, text: str) -> list[str]:
        tokens = self._enc.encode(text)
        if len(tokens) <= self._chunk_size:
            return [text]

        chunks: list[str] = []
        start = 0
        while start < len(tokens):
            end = min(start + self._chunk_size, len(tokens))
            chunk_text = self._enc.decode(tokens[start:end])
            chunks.append(chunk_text)
            start = end - self._chunk_overlap
            if start >= len(tokens):
                break

        return chunks
