import logging
from typing import List
import re

logger = logging.getLogger(__name__)

class ChunkingService:
    """Service for splitting text into chunks for embedding"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of text chunks
        """
        if not text or len(text.strip()) == 0:
            return []
        
        # Clean and normalize text
        text = self._clean_text(text)
        
        # Try sentence-based chunking first
        chunks = self._sentence_based_chunking(text)
        
        # If chunks are too large, use character-based chunking
        final_chunks = []
        for chunk in chunks:
            if len(chunk) <= self.chunk_size:
                final_chunks.append(chunk)
            else:
                final_chunks.extend(self._character_based_chunking(chunk))
        
        return [chunk.strip() for chunk in final_chunks if chunk.strip()]
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove excessive newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()
    
    def _sentence_based_chunking(self, text: str) -> List[str]:
        """Split text by sentences, respecting chunk size"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                chunks.append(current_chunk)
                # Start new chunk with overlap
                current_chunk = self._get_overlap_text(current_chunk) + sentence
            else:
                current_chunk += (" " if current_chunk else "") + sentence
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def _character_based_chunking(self, text: str) -> List[str]:
        """Split text by character count with overlap"""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            if chunk.strip():
                chunks.append(chunk)
            start = end - self.chunk_overlap
            
            # Prevent infinite loop
            if start >= end:
                break
        
        return chunks
    
    def _get_overlap_text(self, text: str) -> str:
        """Get the last part of text for overlap"""
        if len(text) <= self.chunk_overlap:
            return text
        return text[-self.chunk_overlap:]
