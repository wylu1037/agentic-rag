import json
from collections.abc import AsyncIterator
from uuid import uuid4

from app.domain.models import ChatResult, Chunk, Citation
from app.domain.ports import LLMClient
from app.services.retrieval import RetrievalService

SYSTEM_PROMPT = (
    "你是一个基于 RAG（检索增强生成）的知识问答助手。"
    "请根据以下检索到的上下文回答用户的问题。\n\n"
    "规则：\n"
    "1. 只根据提供的上下文回答，不要编造信息。\n"
    "2. 如果上下文不足以回答问题，请明确说明。\n"
    "3. 回答末尾请列出引用来源，格式为 [来源: 文件名#章节]。\n"
    "4. 使用中文回答。"
)


def _build_context(chunks_with_scores: list[tuple[Chunk, float]]) -> str:
    parts: list[str] = []
    for i, (chunk, score) in enumerate(chunks_with_scores, 1):
        source = chunk.metadata.get("source", "unknown")
        section = chunk.metadata.get("heading_path", "")
        page_numbers = chunk.metadata.get("page_numbers", [])
        header = f"[片段 {i}] 来源: {source}"
        if section:
            header += f" | 章节: {section}"
        elif page_numbers:
            header += f" | 页码: {','.join(str(page) for page in page_numbers)}"
        header += f" | 相关度: {score:.2f}"
        parts.append(f"{header}\n{chunk.content}")
    return "\n\n---\n\n".join(parts)


def _build_citations(chunks_with_scores: list[tuple[Chunk, float]]) -> list[Citation]:
    return [
        Citation(
            chunk_id=chunk.id,
            document_title=chunk.metadata.get("source", "unknown"),
            source=chunk.metadata.get("source", ""),
            source_section=chunk.metadata.get("source_section", "")
            or chunk.metadata.get("heading_path", "")
            or _format_pages(chunk.metadata.get("page_numbers", [])),
            content_snippet=chunk.content[:200],
            score=score,
        )
        for chunk, score in chunks_with_scores
    ]


def _format_pages(page_numbers: list[int]) -> str:
    if not page_numbers:
        return ""
    if len(page_numbers) == 1:
        return f"page-{page_numbers[0]}"
    return f"pages-{page_numbers[0]}-{page_numbers[-1]}"


class ChatService:
    def __init__(self, retrieval: RetrievalService, llm: LLMClient) -> None:
        self._retrieval = retrieval
        self._llm = llm

    async def chat(self, query: str, top_k: int = 5) -> ChatResult:
        chunks_with_scores = await self._retrieval.retrieve(query, top_k=top_k)

        context = _build_context(chunks_with_scores)
        user_message = f"上下文：\n{context}\n\n问题：{query}"

        answer = await self._llm.generate(
            messages=[{"role": "user", "content": user_message}],
            system_prompt=SYSTEM_PROMPT,
        )

        citations = _build_citations(chunks_with_scores)
        return ChatResult(
            answer=answer,
            citations=citations,
            conversation_id=str(uuid4()),
        )

    async def chat_stream(self, query: str, top_k: int = 5) -> AsyncIterator[str]:
        chunks_with_scores = await self._retrieval.retrieve(query, top_k=top_k)

        context = _build_context(chunks_with_scores)
        user_message = f"上下文：\n{context}\n\n问题：{query}"

        citations = _build_citations(chunks_with_scores)

        async for token in self._llm.generate_stream(
            messages=[{"role": "user", "content": user_message}],
            system_prompt=SYSTEM_PROMPT,
        ):
            yield f"event: chunk\ndata: {json.dumps({'token': token}, ensure_ascii=False)}\n\n"

        citations_data = [
            {
                "document_title": c.document_title,
                "source": c.source,
                "source_section": c.source_section,
                "content_snippet": c.content_snippet,
                "score": c.score,
            }
            for c in citations
        ]
        yield (
            f"event: citations\n"
            f"data: {json.dumps({'citations': citations_data}, ensure_ascii=False)}\n\n"
        )

        yield f"event: done\ndata: {json.dumps({'conversation_id': str(uuid4())})}\n\n"
