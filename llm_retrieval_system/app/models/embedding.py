from sqlalchemy import Column, Integer, ForeignKey, String, LargeBinary, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(Integer, ForeignKey("document_chunks.id", ondelete="CASCADE"), nullable=False)
    pinecone_id = Column(String(64), unique=True, nullable=False)
    vector_data = Column(LargeBinary, nullable=True)  # Make this nullable
    model_name = Column(String(100), default="text-embedding-ada-002")
    status = Column(String(20), default="completed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    chunk = relationship("DocumentChunk", back_populates="embedding")
