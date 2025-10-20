from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator, Optional
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.core.config import settings

logger = logging.getLogger(__name__)

# Initialize database components
engine: Optional[object] = None
SessionLocal: Optional[object] = None

# Create Base class for models
Base = declarative_base()

# Metadata for migrations
metadata = MetaData()

def init_database():
    """Initialize database connection"""
    global engine, SessionLocal
    
    if not settings.USE_DATABASE or not settings.database_url:
        logger.info("Database disabled - running without database")
        return False
    
    try:
        # Create SQLAlchemy engine
        engine = create_engine(
            settings.database_url,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=10,
            max_overflow=20,
            echo=False  # Set to True for SQL debugging
        )
        
        # Test connection - FIXED: Wrap SQL string with text()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            logger.info("Database connection test successful")
        
        # Create SessionLocal class
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        logger.info("Database initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        logger.error(f"Database URL: {settings.database_url}")
        engine = None
        SessionLocal = None
        return False

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    """
    global SessionLocal
    
    # If SessionLocal is None, try to initialize it
    if not SessionLocal:
        logger.warning("SessionLocal is None, attempting to initialize database...")
        if init_database():
            logger.info("Database initialized successfully in get_db()")
        else:
            logger.error("Database initialization failed in get_db()")
            raise RuntimeError("Database not available")
    
    # Double-check SessionLocal is still available
    if not SessionLocal:
        logger.error("SessionLocal is still None after initialization attempt")
        raise RuntimeError("Database not available")
        
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_tables():
    """
    Create all tables
    """
    if not engine:
        logger.warning("Cannot create tables - database not initialized")
        return False
        
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        return False

def drop_tables():
    """
    Drop all tables (use with caution)
    """
    if not engine:
        logger.warning("Cannot drop tables - database not initialized")
        return False
        
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Database tables dropped successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to drop tables: {e}")
        return False

def check_database_connection():
    """
    Check if database is accessible
    """
    if not engine:
        return False
        
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False

def get_session_local():
    """
    Get the SessionLocal factory
    """
    return SessionLocal
