import os
import uuid
import logging
from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models import Document
from app.services import DocumentProcessor

# Configure logger
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["documents"])

# Initialize document processor
document_processor = DocumentProcessor()

@router.post("/upload", response_model=dict)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and process a document
    
    Supported formats: PDF, DOCX, DOC, TXT
    """
    logger.info(f"Received file upload: {file.filename}, content_type: {file.content_type}")
    
    # Validate file type
    if not document_processor.is_file_supported(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Supported: {document_processor.get_supported_file_types()}"
        )
    
    # Create unique filename
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = Path(settings.UPLOAD_FOLDER) / unique_filename
    
    try:
        # Save uploaded file
        logger.info(f"Saving file to: {file_path}")
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"File saved successfully, size: {len(content)} bytes")
        
        # Process document
        logger.info("Starting document processing...")
        document_data = await document_processor.process_document(
        str(file_path), 
        file.filename, 
        file_ext[1:]  # Remove the dot
        )

        if not document_data:
            # Clean up file if processing failed
            if file_path.exists():
                os.unlink(file_path)
            raise HTTPException(status_code=500, detail="Failed to process document")

        logger.info(f"Document processed successfully: ID {document_data['id']}")

        return {
            "message": "Document uploaded and processed successfully",
            "document_id": document_data["id"],
            "filename": document_data["filename"],
            "file_type": document_data["file_type"],
            "chunks_created": document_data.get("chunks_created", 0)
        }

        
    except Exception as e:
        # Enhanced error logging
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Clean up file if something went wrong
        if file_path.exists():
            os.unlink(file_path)
        
        # Return more detailed error
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing file: {str(e)} (Type: {type(e).__name__})"
        )

@router.get("/", response_model=List[dict])
async def list_documents(db: Session = Depends(get_db)):
    """Get list of all uploaded documents"""
    documents = db.query(Document).all()
    return [
        {
            "id": doc.id,
            "filename": doc.filename,
            "file_type": doc.file_type,
            "upload_date": doc.upload_date,
            "chunks_count": len(doc.chunks) if hasattr(doc, 'chunks') else 0
        }
        for doc in documents
    ]

@router.get("/{document_id}", response_model=dict)
async def get_document(document_id: int, db: Session = Depends(get_db)):
    """Get specific document details"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {
        "id": document.id,
        "filename": document.filename,
        "file_type": document.file_type,
        "upload_date": document.upload_date,
        "content_preview": document.content[:500] if document.content else "",
        "chunks": [
            {
                "id": chunk.id,
                "chunk_index": chunk.chunk_index,
                "text_preview": chunk.chunk_text[:100] + "..." if len(chunk.chunk_text) > 100 else chunk.chunk_text
            }
            for chunk in document.chunks
        ] if hasattr(document, 'chunks') else []
    }

@router.delete("/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete a document and its chunks"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}
