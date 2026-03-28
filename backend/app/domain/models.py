from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass
class Document:
    id: UUID = field(default_factory=uuid4)
    title: str = ""
    source: str = ""
    content: str = ""
    content_type: str = "markdown"
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    chunk_count: int = 0


@dataclass
class Chunk:
    id: UUID = field(default_factory=uuid4)
    document_id: UUID = field(default_factory=uuid4)
    content: str = ""
    embedding: list[float] | None = None
    chunk_index: int = 0
    token_count: int = 0
    metadata: dict = field(default_factory=dict)


@dataclass
class ParsedSection:
    text: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class ParsedContent:
    text: str = ""
    content_type: str = "text"
    metadata: dict = field(default_factory=dict)
    sections: list[ParsedSection] = field(default_factory=list)


@dataclass
class Citation:
    chunk_id: UUID = field(default_factory=uuid4)
    document_title: str = ""
    source: str = ""
    source_section: str = ""
    content_snippet: str = ""
    score: float = 0.0


@dataclass
class ChatResult:
    answer: str = ""
    citations: list[Citation] = field(default_factory=list)
    conversation_id: str = ""
