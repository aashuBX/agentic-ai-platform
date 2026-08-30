"""POST /documents/upload — ingest a document through the real RAG pipeline (parse -> hash ->
dedup -> chunk -> embed -> store). Accepts `.txt`/`.md` always, `.pdf` when the `rag` extra's
`pypdf` is installed.
"""

import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.deps import get_rag_pipeline
from app.models.rag import IngestResult
from app.rag.ingestion.parser import UnsupportedDocumentTypeError
from app.rag.pipeline import RAGPipeline

router = APIRouter(tags=["documents"])


@router.post("/documents/upload", response_model=IngestResult)
async def upload_document(
    file: UploadFile = File(...),
    pipeline: RAGPipeline = Depends(get_rag_pipeline),
) -> IngestResult:
    original_name = file.filename or "uploaded-document.txt"
    suffix = Path(original_name).suffix.lower()
    contents = await file.read()

    with tempfile.NamedTemporaryFile(suffix=suffix) as tmp:
        tmp.write(contents)
        tmp.flush()
        try:
            return pipeline.ingest_file(
                tmp.name,
                source=original_name,
                title=Path(original_name).stem,
                extra_metadata={"original_filename": original_name},
            )
        except UnsupportedDocumentTypeError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc
