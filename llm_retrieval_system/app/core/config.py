import os
from typing import Optional
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

class Settings:
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "DocuMind AI"
    VERSION: str = "1.0.0"
    
    # Database Settings
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "hackathon_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "hackathon_password_2024")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "hackathon_db")
    USE_DATABASE: bool = os.getenv("USE_DATABASE", "true").lower() == "true"
    
    # LLM Settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = "gpt-4"
    MAX_TOKENS: int = 1000
    
    # Vector Store Settings
    FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "vector_store")
    EMBEDDING_MODEL: str = "text-embedding-ada-002"
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))
    
    # File Upload Settings
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "52428800"))  # 50MB
    UPLOAD_FOLDER: str = os.getenv("UPLOAD_FOLDER", "documents")
    ALLOWED_EXTENSIONS: set = {".pdf", ".docx", ".eml", ".txt"}
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @property
    def database_url(self) -> Optional[str]:
        if not self.USE_DATABASE:
            return None
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:5432/{self.POSTGRES_DB}"

settings = Settings()
