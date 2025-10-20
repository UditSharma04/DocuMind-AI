# tests/test_models.py

import sys
from pathlib import Path

# Ensure the parent directory (with "app") is in sys.path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import init_database
from app.models import Document, DocumentChunk, Embedding, Query

def run_model_test():
    assert init_database(), 'DB init failed'
    from app.core.database import SessionLocal
    db = SessionLocal()

    # Create document
    doc = Document(filename="test.pdf", file_type="pdf", content="Hello world!")
    db.add(doc); db.commit(); db.refresh(doc)
    print("Document:", doc)

    # Add chunk
    chunk = DocumentChunk(document_id=doc.id, chunk_index=0, chunk_text="Hello world!")
    db.add(chunk); db.commit(); db.refresh(chunk)
    print("Chunk:", chunk)

    # Add embedding (simulate bytes)
    vector = bytes([1, 2, 3, 4])  # Replace with real data in your app
    emb = Embedding(chunk_id=chunk.id, vector_data=vector)
    db.add(emb); db.commit(); db.refresh(emb)
    print("Embedding:", emb)

    # Add query
    qry = Query(query_text="What is test?", response="This is a test.")
    db.add(qry); db.commit(); db.refresh(qry)
    print("Query:", qry)

    db.close()

if __name__ == "__main__":
    run_model_test()
