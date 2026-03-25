from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://agentic:agentic@localhost:5432/agentic_rag"
    database_url_sync: str = "postgresql://agentic:agentic@localhost:5432/agentic_rag"

    openai_api_key: str = ""
    openai_embedding_model: str = "text-embedding-3-small"
    openai_chat_model: str = "gpt-4o-mini"
    embedding_dimension: int = 1536

    chunk_size: int = 512
    chunk_overlap: int = 64

    default_top_k: int = 5

    model_config = {"env_file": ".env", "env_prefix": "RAG_"}
