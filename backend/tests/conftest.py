from collections.abc import AsyncIterator
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.domain.models import Chunk


@pytest.fixture
def sample_markdown() -> str:
    return """# 项目概述

这是一个 Agentic RAG 项目。

## 技术选型

### 路线 A（推荐）

使用 FastAPI + LangGraph + PostgreSQL/pgvector。

### 路线 B

使用 FastAPI + LangChain + Qdrant。

## 实施计划

第 1 周：初始化工程骨架。
第 2 周：完成基线 RAG。
"""


@pytest.fixture
def mock_embedder() -> AsyncMock:
    embedder = AsyncMock()
    embedder.embed_texts = AsyncMock(
        side_effect=lambda texts: [[0.1] * 1536 for _ in texts]
    )
    embedder.embed_query = AsyncMock(return_value=[0.1] * 1536)
    return embedder


@pytest.fixture
def mock_llm() -> AsyncMock:
    llm = AsyncMock()
    llm.generate = AsyncMock(return_value="这是一个测试回答。")

    async def mock_stream(*_args, **_kwargs) -> AsyncIterator[str]:
        for token in ["这是", "一个", "测试", "回答", "。"]:
            yield token

    llm.generate_stream = mock_stream
    return llm


@pytest.fixture
def mock_doc_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.save = AsyncMock(side_effect=lambda doc: doc)
    repo.get = AsyncMock(return_value=None)
    repo.delete = AsyncMock(return_value=True)
    return repo


@pytest.fixture
def mock_vector_repo() -> AsyncMock:
    repo = AsyncMock()
    repo.store_chunks = AsyncMock()
    repo.search_similar = AsyncMock(
        return_value=[
            (
                Chunk(
                    id=uuid4(),
                    document_id=uuid4(),
                    content="使用 FastAPI + LangGraph + PostgreSQL/pgvector。",
                    chunk_index=0,
                    token_count=20,
                    metadata={
                        "heading_path": "技术选型 > 路线 A（推荐）",
                        "source_section": "路线-a推荐",
                        "source": "README.md",
                    },
                ),
                0.92,
            ),
        ]
    )
    return repo
