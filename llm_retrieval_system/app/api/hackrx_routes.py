from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.search_service import SearchService
from app.services.llm_service import LLMService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["HackRx"])

# Expected token from problem statement
HACKRX_TOKEN = "4b9c2f5eeb9e2cfda8184e3a5f70bfb81840b097ed346bf655cf75b95b47910f"

class HackRxRequest(BaseModel):
    documents: List[str]  # URLs to documents
    questions: List[str]  # List of questions to answer

class HackRxResponse(BaseModel):
    answers: List[str]    # Answers corresponding to each question

@router.post("/hackrx/run", response_model=HackRxResponse)
async def hackrx_run(
    request: HackRxRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    HackRx submission endpoint - processes documents and answers questions
    Expected format matches hackathon requirements
    """
    
    # Validate authorization token
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    token = authorization.replace("Bearer ", "")
    if token != HACKRX_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authorization token")
    
    try:
        # Initialize services
        search_service = SearchService(db)
        llm_service = LLMService()
        
        answers = []
        
        # Parse document IDs from request.documents if they use document-ID format
        selected_document_ids = []
        for doc_ref in request.documents:
            if doc_ref.startswith("document-"):
                # Extract document ID
                try:
                    doc_id = int(doc_ref.replace("document-", ""))
                    selected_document_ids.append(doc_id)
                except ValueError:
                    logger.warning(f"Invalid document reference: {doc_ref}")
        
        logger.info(f"Selected document IDs: {selected_document_ids}")
        
        # Process each question
        for question in request.questions:
            # Perform semantic search with document filtering
            relevant_chunks = search_service.semantic_search(
                query=question,
                top_k=5,
                document_ids=selected_document_ids if selected_document_ids else None
            )
            
            if not relevant_chunks:
                answers.append("I could not find relevant information to answer this question.")
                continue
            
            # Generate answer using LLM
            result = llm_service.generate_answer(
                query=question,
                context_chunks=relevant_chunks
            )
            
            answers.append(result["answer"])
        
        return HackRxResponse(answers=answers)
        
    except Exception as e:
        logger.error(f"HackRx processing error: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error processing request: {str(e)}"
        )
