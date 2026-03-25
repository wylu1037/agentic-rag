from uuid import UUID

from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    content: str
    filename: str
    source: str | None = None


class IngestResponse(BaseModel):
    document_id: UUID
    title: str
    chunk_count: int


class ChatRequest(BaseModel):
    query: str
    conversation_id: str | None = None
    top_k: int = Field(default=5, ge=1, le=20)


class CitationOut(BaseModel):
    document_title: str
    source: str
    source_section: str
    content_snippet: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    citations: list[CitationOut]
    conversation_id: str
