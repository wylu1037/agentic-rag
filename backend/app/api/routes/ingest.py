from fastapi import APIRouter

from app.api.schemas import IngestRequest, IngestResponse
from app.dependencies import IngestServiceDep

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("", response_model=IngestResponse)
async def ingest_document(
    request: IngestRequest,
    service: IngestServiceDep,
) -> IngestResponse:


    doc = await service.ingest(
        content=request.content,
        filename=request.filename,
        source=request.source or request.filename,
    )
    return IngestResponse(
        document_id=doc.id,
        title=doc.title,
        chunk_count=doc.chunk_count,
    )
