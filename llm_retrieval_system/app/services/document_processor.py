import logging
import os
from pathlib import Path
from typing import List, Optional
import traceback

from app.core.config import settings
from app.models import Document, DocumentChunk
from app.services.text_extractor import TextExtractor
from app.services.chunking_service import ChunkingService

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Service for processing uploaded documents"""
    
    def __init__(self):
        logger.info("Initializing DocumentProcessor...")
        
        try:
            self.text_extractor = TextExtractor()
            logger.info("TextExtractor initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize TextExtractor: {e}")
            self.text_extractor = None
            
        try:
            self.chunking_service = ChunkingService(
                chunk_size=settings.CHUNK_SIZE,
                chunk_overlap=settings.CHUNK_OVERLAP
            )
            logger.info("ChunkingService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChunkingService: {e}")
            self.chunking_service = None
    
    async def process_document(self, file_path: str, filename: str, file_type: str) -> Optional[dict]:
        """
        Process uploaded document: extract text, chunk, and store in database
        
        Args:
            file_path: Path to uploaded file
            filename: Original filename
            file_type: File extension
            
        Returns:
            Document data dict if successful, None otherwise
        """
        try:
            logger.info(f"Processing document: {filename}")
            
            # Check if services are available
            if self.text_extractor is None:
                logger.error("TextExtractor is not initialized")
                return None
                
            if self.chunking_service is None:
                logger.error("ChunkingService is not initialized") 
                return None
            
            # Extract text from document
            logger.info(f"Extracting text from {filename}")
            text_content = self.text_extractor.extract_text(file_path, file_type)
            
            if not text_content:
                logger.error(f"No text extracted from {filename}")
                return None
            
            logger.info(f"Text extracted successfully: {len(text_content)} characters")
            
            # Import SessionLocal fresh to ensure it's initialized
            from app.core.database import get_session_local
            SessionLocal = get_session_local()
            
            if SessionLocal is None:
                logger.error("SessionLocal is None - database not initialized")
                return None
            
            # Create document record
            db = SessionLocal()
            try:
                document = Document(
                    filename=filename,
                    file_type=file_type,
                    content=text_content[:10000]  # Store first 10k chars for preview
                )
                db.add(document)
                db.commit()
                db.refresh(document)
                
                # Extract data while session is active
                document_data = {
                    "id": document.id,
                    "filename": document.filename,
                    "file_type": document.file_type,
                    "upload_date": document.upload_date
                }
                
                logger.info(f"Document saved to database with ID: {document.id}")
                
                # Chunk the text
                logger.info(f"Chunking text from {filename}")
                chunks = self.chunking_service.chunk_text(text_content)
                
                logger.info(f"Text chunked into {len(chunks)} chunks")
                
                # Store chunks
                chunk_objects = []
                for i, chunk_text in enumerate(chunks):
                    chunk = DocumentChunk(
                        document_id=document.id,
                        chunk_index=i,
                        chunk_text=chunk_text
                    )
                    chunk_objects.append(chunk)
                
                if chunk_objects:
                    db.add_all(chunk_objects)
                    db.commit()
                    logger.info(f"{len(chunk_objects)} chunks saved to database")
                
                # Add chunk count to document data
                document_data["chunks_created"] = len(chunks)
                
                logger.info(f"Successfully processed {filename}: {len(chunks)} chunks created")
                return document_data
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"Error processing document {filename}: {e}")
            logger.error(f"Error type: {type(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None

    
    def get_supported_file_types(self) -> List[str]:
        """Get list of supported file extensions"""
        return ['.pdf', '.docx', '.doc', '.txt']
    
    def is_file_supported(self, filename: str) -> bool:
        """Check if file type is supported"""
        file_ext = Path(filename).suffix.lower()
        return file_ext in self.get_supported_file_types()
