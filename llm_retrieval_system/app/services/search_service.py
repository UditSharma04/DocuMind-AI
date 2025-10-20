import os, logging
from typing import List, Dict
from sqlalchemy.orm import Session
from app.services.embedding_service import EmbeddingService
from app.services.pinecone_service import query_vector as search_pinecone  # Rename import
from app.models import DocumentChunk, Document

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = EmbeddingService(db)

    def semantic_search(self, query: str, top_k: int = 10) -> List[Dict]:
        """
        Perform semantic search for a query
        
        Returns:
            List of relevant chunks with metadata
        """
        # Generate embedding for query
        query_embedding = self.embedding_service._embed_batch([query])[0]  # Renamed variable
        
        # Search Pinecone
        results = search_pinecone(query_embedding, top_k=top_k)  # Use renamed function
        
        # Handle both Pinecone object and dict format
        if hasattr(results, 'matches'):
            matches = results.matches
        else:
            matches = results.get('matches', [])
        
        # If no Pinecone matches, fallback to database search with text similarity
        if not matches:
            logger.info("No Pinecone matches found, searching database with text similarity")
            
            # Search by text similarity - prioritize recent documents and look for keywords
            query_lower = query.lower()
            query_words = query_lower.split()
            
            # Get chunks from most recent documents first, with text matching
            db_chunks = (
                self.db.query(DocumentChunk, Document)
                .join(Document)
                .order_by(Document.upload_date.desc(), DocumentChunk.chunk_index)
                .limit(top_k * 3)  # Get more to filter
                .all()
            )
            
            if db_chunks:
                # Score chunks based on keyword matches
                scored_chunks = []
                for chunk, doc in db_chunks:
                    chunk_text_lower = chunk.chunk_text.lower()
                    
                    # Calculate basic text similarity score
                    score = 0.5  # Base score
                    word_matches = sum(1 for word in query_words if word in chunk_text_lower)
                    if word_matches > 0:
                        score = 0.7 + (word_matches / len(query_words)) * 0.3
                    
                    scored_chunks.append({
                        "chunk_id": chunk.id,
                        "chunk_text": chunk.chunk_text,
                        "document_id": chunk.document_id,
                        "score": score,
                        "document_filename": doc.filename,
                        "word_matches": word_matches
                    })
                
                # Sort by score and word matches, return top results
                scored_chunks.sort(key=lambda x: (x["word_matches"], x["score"]), reverse=True)
                return scored_chunks[:top_k]
            
            # Only return demo content if NO documents exist in database
            logger.info("No documents found in database, returning demo content")
            return [{
                "chunk_id": 1,
                "chunk_text": f"Sample document content related to: {query}. This is a demonstration of the RAG system working with Gemini AI. In a real scenario, this would be actual document content retrieved from the vector database.",
                "document_id": 1,
                "score": 0.8,
                "document_filename": "demo_policy_document.pdf"
            }]
        
        # Enrich with database info (for when we have real indexed documents)
        enriched_results = []
        for match in matches:
            try:
                chunk_id = int(match.id.replace('chunk-', ''))
                chunk = self.db.query(DocumentChunk).filter(DocumentChunk.id == chunk_id).first()
                
                if chunk:
                    enriched_results.append({
                        "chunk_id": chunk.id,
                        "chunk_text": chunk.chunk_text,
                        "document_id": chunk.document_id,
                        "score": match.score,
                        "document_filename": chunk.document.filename
                    })
            except (ValueError, AttributeError) as e:
                logger.warning(f"Error processing match: {e}")
                continue
        
        return enriched_results
