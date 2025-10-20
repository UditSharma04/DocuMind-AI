from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import time
import asyncio

router = APIRouter(tags=["Demo"])

class DemoRequest(BaseModel):
    documents: List[str]
    questions: List[str]

class DemoResponse(BaseModel):
    answers: List[str]

@router.post("/demo/hackrx/run", response_model=DemoResponse)
async def demo_hackrx_run(request: DemoRequest):
    """
    Demo endpoint that works without OpenAI API key
    Returns sample responses for demonstration purposes
    """
    
    # Simulate processing time
    await asyncio.sleep(1)
    
    # Generate demo responses based on questions
    demo_answers = []
    
    for question in request.questions:
        if "grace period" in question.lower():
            answer = "Based on the policy document, the grace period for premium payment is 30 days from the due date. During this period, you can renew your policy without losing continuity benefits."
        elif "waiting period" in question.lower() and "pre-existing" in question.lower():
            answer = "The waiting period for pre-existing diseases (PED) is 36 months of continuous coverage from the first policy inception date."
        elif "maternity" in question.lower():
            answer = "Yes, this policy covers maternity expenses including childbirth and lawful medical termination. You need 24 months of continuous coverage to be eligible, limited to two deliveries per policy period."
        elif "cataract" in question.lower():
            answer = "The policy has a specific waiting period of 2 years for cataract surgery coverage."
        elif "organ donor" in question.lower():
            answer = "Yes, medical expenses for organ donors are covered when the organ is for an insured person and complies with the Transplantation of Human Organs Act, 1994."
        elif "discount" in question.lower() or "ncd" in question.lower():
            answer = "The No Claim Discount (NCD) is 5% on the base premium for renewal after a claim-free year. The maximum NCD is capped at 5% of total base premium."
        elif "health check" in question.lower():
            answer = "Yes, the policy reimburses health check-up expenses at the end of every two continuous policy years, subject to limits in the Table of Benefits."
        elif "hospital" in question.lower() and "define" in question.lower():
            answer = "A hospital is defined as an institution with at least 10-15 inpatient beds (depending on location), qualified 24/7 nursing staff, medical practitioners, fully equipped operation theatre, and daily patient records."
        elif "ayush" in question.lower():
            answer = "The policy covers inpatient AYUSH treatments (Ayurveda, Yoga, Naturopathy, Unani, Siddha, Homeopathy) up to Sum Insured limit when taken in an AYUSH Hospital."
        elif "room rent" in question.lower() or "icu" in question.lower():
            answer = "For Plan A, daily room rent is capped at 1% of Sum Insured and ICU charges at 2% of Sum Insured. These limits don't apply for treatments in Preferred Provider Network (PPN)."
        else:
            answer = f"Based on the document analysis, here's what I found regarding '{question}': This is a comprehensive insurance policy with various coverage options and specific terms. For detailed information about this specific query, please refer to the complete policy document or contact customer service."
        
        demo_answers.append(answer)
    
    return DemoResponse(answers=demo_answers)
