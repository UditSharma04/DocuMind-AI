import logging
from pathlib import Path
from typing import Optional, List
import PyPDF2
from docx import Document as DocxDocument

logger = logging.getLogger(__name__)

class TextExtractor:
    """Service for extracting text from various document formats"""
    
    @staticmethod
    def extract_text(file_path: str, file_type: str) -> Optional[str]:
        """
        Extract text from uploaded document
        
        Args:
            file_path: Path to the uploaded file
            file_type: Type of file (pdf, docx, txt)
            
        Returns:
            Extracted text content or None if extraction fails
        """
        try:
            if file_type.lower() == 'pdf':
                return TextExtractor._extract_from_pdf(file_path)
            elif file_type.lower() in ['docx', 'doc']:
                return TextExtractor._extract_from_docx(file_path)
            elif file_type.lower() == 'txt':
                return TextExtractor._extract_from_txt(file_path)
            else:
                logger.error(f"Unsupported file type: {file_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            return None
    
    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            logger.error(f"Error reading PDF {file_path}: {e}")
            return ""
        return text.strip()
    
    @staticmethod
    def _extract_from_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = DocxDocument(file_path)
            for paragraph in doc.paragraphs:
                if paragraph.text:
                    text += paragraph.text + "\n"
        except Exception as e:
            logger.error(f"Error reading DOCX {file_path}: {e}")
            return ""
        return text.strip()
    
    @staticmethod
    def _extract_from_txt(file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            try:
                with open(file_path, 'r', encoding='cp1252') as file:
                    return file.read().strip()
            except Exception as e:
                logger.error(f"Error reading TXT {file_path}: {e}")
                return ""
        except Exception as e:
            logger.error(f"Error reading TXT {file_path}: {e}")
            return ""
