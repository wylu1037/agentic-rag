import openai

from app.config import Settings


class OpenAIEmbedder:
    def __init__(self, settings: Settings) -> None:
        self._client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
        self._model = settings.openai_embedding_model

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        resp = await self._client.embeddings.create(input=texts, model=self._model)
        return [item.embedding for item in resp.data]

    async def embed_query(self, query: str) -> list[float]:
        result = await self.embed_texts([query])
        return result[0]
