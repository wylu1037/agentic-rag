from fastapi import APIRouter
from starlette.responses import StreamingResponse

from app.api.schemas import ChatRequest, ChatResponse, CitationOut
from app.dependencies import ChatServiceDep

router = APIRouter(prefix="/chat", tags=["chat"])



@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    service: ChatServiceDep,
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
    service: ChatServiceDep,
) -> StreamingResponse:


    return StreamingResponse(
        service.chat_stream(query=request.query, top_k=request.top_k),
        media_type="text/event-stream",
    )
