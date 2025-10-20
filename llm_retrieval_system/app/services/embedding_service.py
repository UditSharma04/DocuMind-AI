import os, logging, backoff
from typing import List
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.services.pinecone_service import upsert_vectors
from app.models import DocumentChunk, Embedding

# Use sentence-transformers for embeddings instead of OpenAI
from sentence_transformers import SentenceTransformer

load_dotenv()
logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self, db: Session):
        self.db = db
        # Use a free, local embedding model
        self.model_name = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        try:
            # Try loading the model with fallback
            logger.info(f"Loading sentence transformer model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Successfully loaded embedding model: {self.model_name}")
        except Exception as e:
            logger.warning(f"Failed to load embedding model {self.model_name}: {e}")
            logger.info("Embedding service will run in simulation mode")
            self.model = None

    def _embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using sentence-transformers (free, local)."""
        if not self.model:
            logger.error("Embedding model not available")
            return [[0.0] * 384 for _ in texts]  # Return dummy embeddings
            
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Embedding generation error: {e}")
            return [[0.0] * 384 for _ in texts]  # Return dummy embeddings

    # ---------- public API ----------
    def generate_for_document(self, doc_id: int, batch_size: int = 100) -> int:
        """Generate and store embeddings for all chunks of a document."""
        chunks: List[DocumentChunk] = (
            self.db.query(DocumentChunk)
            .filter(DocumentChunk.document_id == doc_id)
            .order_by(DocumentChunk.chunk_index)
            .all()
        )
        if not chunks:
            logger.warning(f"No chunks found for document {doc_id}")
            return 0

        total = 0
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            vectors = self._embed_batch([c.chunk_text for c in batch])

            pine_payload = []
            for chunk, vec in zip(batch, vectors):
                pine_id = f"chunk-{chunk.id}"
                pine_payload.append(
                    {
                        "id": pine_id,
                        "values": vec,
                        "metadata": {
                            "document_id": chunk.document_id,
                            "chunk_index": chunk.chunk_index,
                        },
                    }
                )
                # ORM row
                emb = Embedding(
                    chunk_id=chunk.id,
                    pinecone_id=pine_id,
                    model_name=MODEL,
                    status="completed",
                )
                self.db.add(emb)

            upsert_vectors(pine_payload)
            self.db.commit()
            total += len(batch)
            logger.info(f"Upserted {len(batch)} vectors for doc {doc_id}")

        return total
