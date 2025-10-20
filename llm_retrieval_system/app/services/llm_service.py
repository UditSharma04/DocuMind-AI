import os, logging
from typing import List, Dict
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
    genai.configure(api_key=GEMINI_API_KEY)

class LLMService:
    def __init__(self):
        # Use available Gemini models (from list_models output)
        model_names = [
            "models/gemini-2.5-flash",
            "models/gemini-flash-latest", 
            "models/gemini-pro-latest",
            "models/gemini-2.0-flash"
        ]
        self.model = None
        self.model_name = None
        
        if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
            for model_name in model_names:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    self.model_name = model_name
                    logger.info(f"Successfully initialized Gemini model: {self.model_name}")
                    break
                except Exception as e:
                    logger.warning(f"Failed to initialize model {model_name}: {e}")
                    continue
            
            if not self.model:
                logger.error("Failed to initialize any Gemini model - using fallback responses")
        else:
            logger.warning("Gemini API key not configured - using fallback responses")

    def generate_answer(self, query: str, context_chunks: List[Dict]) -> Dict:
        """Generate answer using Gemini model"""
        
        # If no model available, return fallback response
        if not self.model:
            return {
                "answer": "I'm currently unable to process your question due to API configuration. Please check the Gemini API key setup.",
                "model": "fallback",
                "tokens_used": 0
            }
        
        # Build context from chunks
        context = "\n\n".join([
            f"Document: {chunk.get('document_filename', 'Unknown')}\n{chunk.get('chunk_text', str(chunk))}"
            for chunk in context_chunks[:5]  # Use top 5 chunks
        ])
        
        prompt = f"""You are an expert assistant that answers questions based on provided documents. 
Use only the information from the documents below to answer the question.

Question: {query}

Context Documents:
{context}

Instructions:
1. Answer the question using only information from the provided context
2. If the answer isn't in the context, say so clearly
3. Cite which document(s) you're referencing
4. Provide reasoning for your answer

Answer:"""
        
        try:
            response = self.model.generate_content(prompt)
            
            # Handle usage metadata properly
            tokens_used = 0
            try:
                if hasattr(response, 'usage_metadata') and response.usage_metadata:
                    tokens_used = getattr(response.usage_metadata, 'total_token_count', 0)
            except:
                tokens_used = 0
                
            return {
                "answer": response.text.strip(),
                "model": self.model_name,
                "tokens_used": tokens_used
            }
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return {
                "answer": f"I encountered an error while processing your question: {str(e)}",
                "model": self.model_name,
                "tokens_used": 0
            }