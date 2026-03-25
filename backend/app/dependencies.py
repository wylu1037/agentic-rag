from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.infra.chunker import HeadingAwareChunker
from app.infra.database import get_session
from app.infra.document_store import PgDocumentStore
from app.infra.embedder import OpenAIEmbedder
from app.infra.llm import OpenAILLM
from app.infra.parser import MarkdownParser
from app.infra.vector_store import PgVectorStore
from app.services.chat import ChatService
from app.services.ingest import IngestService
from app.services.retrieval import RetrievalService


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_parser() -> MarkdownParser:
    return MarkdownParser()


def get_chunker(settings: Settings = Depends(get_settings)) -> HeadingAwareChunker:
    return HeadingAwareChunker(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )


def get_embedder(settings: Settings = Depends(get_settings)) -> OpenAIEmbedder:
    return OpenAIEmbedder(settings)


def get_document_store(session: AsyncSession = Depends(get_session)) -> PgDocumentStore:
    return PgDocumentStore(session)


def get_vector_store(session: AsyncSession = Depends(get_session)) -> PgVectorStore:
    return PgVectorStore(session)


def get_ingest_service(
    parser: MarkdownParser = Depends(get_parser),
    chunker: HeadingAwareChunker = Depends(get_chunker),
    embedder: OpenAIEmbedder = Depends(get_embedder),
    doc_store: PgDocumentStore = Depends(get_document_store),
    vector_store: PgVectorStore = Depends(get_vector_store),
) -> IngestService:
    return IngestService(
        parser=parser,
        chunker=chunker,
        embedder=embedder,
        doc_repo=doc_store,
        vector_repo=vector_store,
    )


def get_retrieval_service(
    embedder: OpenAIEmbedder = Depends(get_embedder),
    vector_store: PgVectorStore = Depends(get_vector_store),
) -> RetrievalService:
    return RetrievalService(embedder=embedder, vector_repo=vector_store)


def get_llm(settings: Settings = Depends(get_settings)) -> OpenAILLM:
    return OpenAILLM(settings)


def get_chat_service(
    retrieval: RetrievalService = Depends(get_retrieval_service),
    llm: OpenAILLM = Depends(get_llm),
) -> ChatService:
    return ChatService(retrieval=retrieval, llm=llm)
