from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.infra.chunker import HeadingAwareChunker
from app.infra.database import get_session
from app.infra.document_store import PgDocumentStore
from app.infra.embedder import OpenAIEmbedder
from app.infra.llm import OpenAILLM
from app.infra.parser import DoclingParser
from app.infra.reranker import HeuristicReranker, NoopReranker
from app.infra.vector_store import PgVectorStore
from app.services.chat import ChatService
from app.services.ingest import IngestService
from app.services.retrieval import RetrievalService


@lru_cache
def get_settings() -> Settings:
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]


SessionDep = Annotated[AsyncSession, Depends(get_session)]



def get_parser() -> DoclingParser:
    return DoclingParser()


ParserDep = Annotated[DoclingParser, Depends(get_parser)]


def get_chunker(settings: SettingsDep) -> HeadingAwareChunker:
    return HeadingAwareChunker(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )


ChunkerDep = Annotated[HeadingAwareChunker, Depends(get_chunker)]


def get_embedder(settings: SettingsDep) -> OpenAIEmbedder:
    return OpenAIEmbedder(settings)


EmbedderDep = Annotated[OpenAIEmbedder, Depends(get_embedder)]


def get_document_store(session: SessionDep) -> PgDocumentStore:
    return PgDocumentStore(session)


DocumentStoreDep = Annotated[PgDocumentStore, Depends(get_document_store)]


def get_vector_store(session: SessionDep) -> PgVectorStore:
    return PgVectorStore(session)


VectorStoreDep = Annotated[PgVectorStore, Depends(get_vector_store)]


def get_reranker(settings: SettingsDep) -> NoopReranker | HeuristicReranker:
    if not settings.enable_reranker:
        return NoopReranker()
    return HeuristicReranker()


RerankerDep = Annotated[NoopReranker | HeuristicReranker, Depends(get_reranker)]


def get_ingest_service(
    parser: ParserDep,
    chunker: ChunkerDep,
    embedder: EmbedderDep,
    doc_store: DocumentStoreDep,
    vector_store: VectorStoreDep,
) -> IngestService:
    return IngestService(
        parser=parser,
        chunker=chunker,
        embedder=embedder,
        doc_repo=doc_store,
        vector_repo=vector_store,
    )


IngestServiceDep = Annotated[IngestService, Depends(get_ingest_service)]


def get_retrieval_service(
    settings: SettingsDep,
    embedder: EmbedderDep,
    vector_store: VectorStoreDep,
    reranker: RerankerDep,
) -> RetrievalService:
    return RetrievalService(
        embedder=embedder,
        vector_repo=vector_store,
        reranker=reranker,
        reranker_fetch_k=settings.reranker_fetch_k,
    )


RetrievalServiceDep = Annotated[RetrievalService, Depends(get_retrieval_service)]


def get_llm(settings: SettingsDep) -> OpenAILLM:
    return OpenAILLM(settings)


LLMDep = Annotated[OpenAILLM, Depends(get_llm)]


def get_chat_service(
    retrieval: RetrievalServiceDep,
    llm: LLMDep,
) -> ChatService:
    return ChatService(retrieval=retrieval, llm=llm)


ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
