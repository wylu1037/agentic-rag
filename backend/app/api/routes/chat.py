from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from app.api.schemas import ChatRequest, ChatResponse, CitationOut
from app.dependencies import get_chat_service
from app.services.chat import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    result = await service.chat(query=request.query, top_k=request.top_k)
    return ChatResponse(
        answer=result.answer,
        citations=[
            CitationOut(
                document_title=c.document_title,
                source=c.source,
                source_section=c.source_section,
                content_snippet=c.content_snippet,
                score=c.score,
            )
            for c in result.citations
        ],
        conversation_id=result.conversation_id,
    )


@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    service: ChatService = Depends(get_chat_service),
) -> StreamingResponse:
    return StreamingResponse(
        service.chat_stream(query=request.query, top_k=request.top_k),
        media_type="text/event-stream",
    )
