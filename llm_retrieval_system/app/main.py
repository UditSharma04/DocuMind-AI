from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import os
from pathlib import Path

# Configure logging first (without emojis to avoid encoding issues)
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Import config first
from app.core.config import settings
from app.api.document_routes import router as document_router
from app.api.embedding_routes import router as embedding_router
from app.api.query_routes import router as query_router
from app.api.hackrx_routes import router as hackrx_router
from app.api.demo_routes import router as demo_router

# Create FastAPI instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="LLM-powered query retrieval system for hackathon",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    # Disable syntax highlighting to prevent Swagger UI loading issues
    swagger_ui_parameters={"syntaxHighlight.activated": False}
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(
    document_router,
    prefix=settings.API_V1_STR
)

app.include_router(embedding_router)
app.include_router(query_router)
app.include_router(hackrx_router)
app.include_router(demo_router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("Starting up DocuMind AI...")
    
    # Create directories
    Path(settings.UPLOAD_FOLDER).mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)
    Path(settings.FAISS_INDEX_PATH).mkdir(exist_ok=True)
    
    # Database initialization with detailed logging
    if settings.USE_DATABASE:
        logger.info("Database is enabled, attempting initialization...")
        try:
            from app.core.database import init_database, get_session_local
            
            # Initialize database
            db_init_success = init_database()
            logger.info(f"Database initialization result: {db_init_success}")
            
            if not db_init_success:
                logger.error("❌ Database initialization failed!")
                raise Exception("Database initialization returned False")
            
            # Verify SessionLocal is available
            SessionLocal = get_session_local()
            logger.info(f"SessionLocal factory: {SessionLocal}")
            
            if SessionLocal is None:
                logger.error("❌ SessionLocal is None after initialization!")
                raise Exception("SessionLocal is None")
            
            # Test creating a session
            test_db = SessionLocal()
            test_db.close()
            logger.info("✅ Database test session created and closed successfully")
            
            logger.info("✅ Database setup completed successfully")
            
        except ImportError as e:
            logger.error(f"❌ Database modules not available: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Database setup failed: {e}")
            logger.error(f"❌ Error type: {type(e)}")
            raise
    else:
        logger.info("Database disabled in configuration")
    
    logger.info("Startup completed successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Shutting down DocuMind AI...")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database_enabled": settings.USE_DATABASE
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "DocuMind AI - Intelligent Document Query System",
        "version": settings.VERSION,
        "docs": "/docs",
        "database_status": "enabled" if settings.USE_DATABASE else "disabled"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
