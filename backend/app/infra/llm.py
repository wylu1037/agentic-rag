from collections.abc import AsyncIterator

import openai

from app.config import Settings


class OpenAILLM:
    def __init__(self, settings: Settings) -> None:
        self._client = openai.AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )
        self._model = settings.openai_chat_model

    async def generate(self, messages: list[dict], system_prompt: str = "") -> str:
        api_messages: list[dict] = []
        if system_prompt:
            api_messages.append({"role": "system", "content": system_prompt})
        api_messages.extend(messages)

        resp = await self._client.chat.completions.create(
            model=self._model,
            messages=api_messages,
        )
        return resp.choices[0].message.content or ""

    async def generate_stream(
        self, messages: list[dict], system_prompt: str = ""
    ) -> AsyncIterator[str]:
        api_messages: list[dict] = []
        if system_prompt:
            api_messages.append({"role": "system", "content": system_prompt})
        api_messages.extend(messages)

        stream = await self._client.chat.completions.create(
            model=self._model,
            messages=api_messages,
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                yield delta.content
