from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.search_service import SearchService
from app.services.llm_service import LLMService

router = APIRouter(prefix="/api/v1/query", tags=["Query"])

class QueryRequest(BaseModel):
    question: str
    top_k: int = 10

@router.post("/ask")
def ask_question(request: QueryRequest, db: Session = Depends(get_db)):
    """
    End-to-end question answering with semantic search + LLM
    """
    try:
        # Search for relevant chunks
        search_service = SearchService(db)
        relevant_chunks = search_service.semantic_search(
            query=request.question,
            top_k=request.top_k
        )
        
        if not relevant_chunks:
            raise HTTPException(
                status_code=404, 
                detail="No relevant documents found for your question"
            )
        
        # Generate answer using LLM
        llm_service = LLMService()
        result = llm_service.generate_answer(
            query=request.question,
            context_chunks=relevant_chunks
        )
        
        return {
            "question": request.question,
            "answer": result["answer"],
            "sources": list(set(result["sources"])),  # Remove duplicates
            "confidence": result["confidence"],
            "relevant_chunks": len(relevant_chunks)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@router.post("/search")
def semantic_search(request: QueryRequest, db: Session = Depends(get_db)):
    """
    Semantic search only (without LLM answer generation)
    """
    search_service = SearchService(db)
    results = search_service.semantic_search(
        query=request.question,
        top_k=request.top_k
    )
    
    return {
        "query": request.question,
        "results": results,
        "total_results": len(results)
    }
