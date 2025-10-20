from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.embedding_service import EmbeddingService

router = APIRouter(prefix="/api/v1/embeddings", tags=["Embeddings"])

@router.post("/generate/{document_id}")
def generate_embeddings(document_id: int, db: Session = Depends(get_db)):
    svc = EmbeddingService(db)
    count = svc.generate_for_document(document_id)
    if count == 0:
        raise HTTPException(status_code=404, detail="No chunks found")
    return {"message": "embeddings generated", "vectors": count}
