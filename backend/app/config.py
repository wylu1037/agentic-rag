from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://agentic:agentic@localhost:5432/agentic_rag"
    database_url_sync: str = "postgresql://agentic:agentic@localhost:5432/agentic_rag"

    openai_api_key: str = ""
    openai_base_url: str | None = None
    openai_embedding_model: str = "Qwen/Qwen3-Embedding-0.6B"
    openai_chat_model: str = "gpt-4o-mini"
    embedding_dimension: int = 1024

    chunk_size: int = 512
    chunk_overlap: int = 64

    default_top_k: int = 5
    enable_reranker: bool = False
    reranker_fetch_k: int = 20

    model_config = {"env_file": ".env", "env_prefix": "RAG_"}
