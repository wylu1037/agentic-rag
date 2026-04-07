from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.ingest import router as ingest_router
from app.config import Settings
from app.infra.database import dispose_engine, init_engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    settings = Settings()
    init_engine(settings)
    yield
    await dispose_engine()


app = FastAPI(
    title="Agentic RAG Backend",
    description="Agentic RAG backend with Clean Architecture.",
    version="0.2.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(ingest_router)
app.include_router(chat_router)
