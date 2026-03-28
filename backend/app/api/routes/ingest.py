from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.api.schemas import IngestRequest, IngestResponse
from app.dependencies import IngestServiceDep

router = APIRouter(prefix="/ingest", tags=["ingest"])


@router.post("", response_model=IngestResponse)
async def ingest_document(
    request: IngestRequest,
    service: IngestServiceDep,
) -> IngestResponse:
    try:
        doc = await service.ingest(
            content=request.content,
            filename=request.filename,
            source=request.source or request.filename,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return IngestResponse(
        document_id=doc.id,
        title=doc.title,
        chunk_count=doc.chunk_count,
    )


@router.post("/file", response_model=IngestResponse)
async def ingest_file(
    service: IngestServiceDep,
    file: UploadFile = File(...),
    source: str | None = Form(default=None),
) -> IngestResponse:
    filename = file.filename or "upload.bin"

    try:
        doc = await service.ingest(
            content=await file.read(),
            filename=filename,
            source=source or filename,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return IngestResponse(
        document_id=doc.id,
        title=doc.title,
        chunk_count=doc.chunk_count,
    )
