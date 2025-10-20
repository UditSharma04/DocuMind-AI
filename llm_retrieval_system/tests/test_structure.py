import pytest
import sys
import os
from pathlib import Path

# Add app to path for Windows
current_dir = Path(__file__).parent.parent
sys.path.append(str(current_dir))

def test_app_imports():
    """Test that all app modules can be imported"""
    from app.main import app
    from app.core.config import settings
    from app.core.database import get_db
    
    assert app is not None
    assert settings is not None
    assert get_db is not None

def test_project_structure():
    """Test that all required directories exist"""
    base_path = Path(__file__).parent.parent
    
    required_dirs = [
        "app",
        "app\\core",
        "app\\models", 
        "app\\schemas",
        "app\\services",
        "app\\api",
        "app\\utils",
        "tests",
        "documents",
        "logs"
    ]
    
    for dir_path in required_dirs:
        dir_path_normalized = dir_path.replace("\\", os.sep)
        assert (base_path / dir_path_normalized).exists(), f"Directory {dir_path} does not exist"

def test_config_loading():
    """Test that configuration loads correctly"""
    from app.core.config import settings
    
    assert settings.PROJECT_NAME == "LLM Query Retrieval System"
    assert settings.VERSION == "1.0.0"
    assert settings.API_V1_STR == "/api/v1"

if __name__ == "__main__":
    pytest.main([__file__])
