from fastapi import FastAPI

app = FastAPI(
    title="Agentic RAG Backend",
    description="Week 1 scaffold for backend APIs.",
    version="0.1.0",
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
