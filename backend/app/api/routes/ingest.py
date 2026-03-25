from fastapi import APIRouter, Depends

from app.api.schemas import IngestRequest, IngestResponse
from app.dependencies import get_ingest_service
from app.services.ingest import IngestService

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("", response_model=IngestResponse)
async def ingest_document(
    request: IngestRequest,
    service: IngestService = Depends(get_ingest_service),
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
