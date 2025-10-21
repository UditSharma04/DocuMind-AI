import os, logging
import numpy as np
from typing import List, Dict
from sqlalchemy.orm import Session
from app.services.embedding_service import EmbeddingService
from app.services.pinecone_service import query_vector as search_pinecone  # Rename import
from app.models import DocumentChunk, Document, Embedding

logger = logging.getLogger(__name__)

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    vec1_np = np.array(vec1)
    vec2_np = np.array(vec2)
    
    dot_product = np.dot(vec1_np, vec2_np)
    norm1 = np.linalg.norm(vec1_np)
    norm2 = np.linalg.norm(vec2_np)
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return float(dot_product / (norm1 * norm2))

class SearchService:
    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = EmbeddingService(db)

    def semantic_search(self, query: str, top_k: int = 10, document_ids: List[int] = None) -> List[Dict]:
        """
        Perform semantic search for a query
        
        Args:
            query: Search query string
            top_k: Maximum number of results to return
            document_ids: Optional list of document IDs to restrict search to
        
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
        
        # If no Pinecone matches, fallback to semantic search using local embeddings
        if not matches:
            logger.info("No Pinecone matches found, using semantic search with local embeddings")
            
            # Build base query to get chunks with embeddings
            base_query = (
                self.db.query(DocumentChunk, Document, Embedding)
                .join(Document, DocumentChunk.document_id == Document.id)
                .outerjoin(Embedding, DocumentChunk.id == Embedding.chunk_id)
            )
            
            # Apply document ID filter if provided
            if document_ids:
                base_query = base_query.filter(Document.id.in_(document_ids))
                logger.info(f"Filtering search to documents: {document_ids}")
            
            # Get all chunks (we'll score them semantically)
            db_chunks = base_query.all()
            
            if db_chunks:
                logger.info(f"Found {len(db_chunks)} chunks to score semantically")
                
                # Score chunks using semantic similarity with embeddings
                scored_chunks = []
                chunks_without_embeddings = 0
                
                for chunk, doc, embedding in db_chunks:
                    # Try to get embedding vector from database
                    chunk_embedding = None
                    
                    # If embedding exists in DB, try to use it
                    if embedding and hasattr(embedding, 'vector_data') and embedding.vector_data:
                        chunk_embedding = embedding.vector_data
                    else:
                        # Generate embedding on-the-fly for this chunk
                        try:
                            chunk_embedding = self.embedding_service._embed_batch([chunk.chunk_text])[0]
                            chunks_without_embeddings += 1
                        except Exception as e:
                            logger.warning(f"Could not generate embedding for chunk {chunk.id}: {e}")
                            continue
                    
                    # Calculate semantic similarity
                    if chunk_embedding:
                        similarity_score = cosine_similarity(query_embedding, chunk_embedding)
                        
                        # Also add keyword bonus for exact matches
                        query_lower = query.lower()
                        chunk_text_lower = chunk.chunk_text.lower()
                        keyword_bonus = 0.0
                        
                        # Check for exact phrase match
                        if query_lower in chunk_text_lower:
                            keyword_bonus = 0.15
                        else:
                            # Check for individual important words (filter stopwords)
                            stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'under'}
                            query_words = [w for w in query_lower.split() if w not in stopwords and len(w) > 2]
                            
                            if query_words:
                                word_matches = sum(1 for word in query_words if word in chunk_text_lower)
                                keyword_bonus = (word_matches / len(query_words)) * 0.1
                        
                        final_score = similarity_score + keyword_bonus
                        
                        scored_chunks.append({
                            "chunk_id": chunk.id,
                            "chunk_text": chunk.chunk_text,
                            "document_id": chunk.document_id,
                            "score": float(final_score),
                            "document_filename": doc.filename,
                            "semantic_score": float(similarity_score),
                            "keyword_bonus": float(keyword_bonus)
                        })
                
                if chunks_without_embeddings > 0:
                    logger.info(f"Generated {chunks_without_embeddings} embeddings on-the-fly")
                
                # Sort by final score (semantic + keyword bonus)
                scored_chunks.sort(key=lambda x: x["score"], reverse=True)
                
                top_results = scored_chunks[:top_k]
                logger.info(f"Returning top {len(top_results)} results with scores: {[f'{r['score']:.3f}' for r in top_results[:3]]}")
                
                return top_results
            
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
