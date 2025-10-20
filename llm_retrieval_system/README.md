# LLM Query Retrieval System

This repository contains a FastAPI-based LLM-powered query retrieval system with a PostgreSQL backend using SQLAlchemy and Alembic for migrations.

---

## 🚀 Project Overview

- FastAPI backend with REST API endpoints
- PostgreSQL database for persistence
- SQLAlchemy ORM models and Alembic migrations
- Environment configuration via `.env`
- Supports document upload, text chunking, embedding, and query storage (implementation ongoing)

---

## 🛠️ Complete Environment Setup Guide

This guide provides setup instructions for both **macOS** and **Windows**. Choose your platform:

- [🍎 **macOS Setup**](#-macos-setup)
- [🪟 **Windows Setup**](#-windows-setup)

---

## 🍎 macOS Setup

### Prerequisites
- **Homebrew** (install from [brew.sh](https://brew.sh))
- **Python 3.12+** (will be handled by virtual environment)

### 1. Clone or Extract the Project

Navigate to your desired directory and clone/extract the project:
```bash
cd ~/Desktop/Code/Hackathons  # or your preferred directory
# If cloning: git clone <repository-url>
# If extracted, navigate to the hackrx directory
cd hackrx
```

### 2. Create and Activate Virtual Environment

Create your virtual environment **outside** the project directory:
```bash
# Create virtual environment with Python 3.12
python3 -m venv hackathon_env

# Activate the virtual environment
source hackathon_env/bin/activate
```
You should see `(hackathon_env)` in your terminal prompt.

### 3. Navigate to Project Directory

```bash
cd llm_retrieval_system
```

### 4. Install Dependencies

```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Install all project dependencies
pip install -r requirements.txt
```

### 5. Install and Setup PostgreSQL

**Install PostgreSQL via Homebrew:**
```bash
# Install PostgreSQL 14
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14

# Add PostgreSQL to your PATH (add to ~/.zshrc or ~/.bash_profile)
export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"

# Reload your shell configuration
source ~/.zshrc  # or source ~/.bash_profile
```

**Create Database and User:**
```bash
# Create database
psql postgres -c "CREATE DATABASE hackathon_db;"

# Create user with password
psql postgres -c "CREATE USER hackathon_user WITH ENCRYPTED PASSWORD 'hackathon_password_2024';"

# Grant privileges
psql postgres -c "GRANT ALL PRIVILEGES ON DATABASE hackathon_db TO hackathon_user;"
psql hackathon_db -c "ALTER SCHEMA public OWNER TO hackathon_user;"
psql hackathon_db -c "GRANT ALL ON SCHEMA public TO hackathon_user;"
psql hackathon_db -c "GRANT CREATE ON SCHEMA public TO hackathon_user;"
```

### 6. Configure Environment Variables

The `.env` file should be automatically created. If not, create it in the project root:
```bash
cat > .env << 'EOF'
# Database Configuration
POSTGRES_SERVER=localhost
POSTGRES_USER=hackathon_user
POSTGRES_PASSWORD=hackathon_password_2024
POSTGRES_DB=hackathon_db
DATABASE_URL=postgresql+psycopg2://hackathon_user:hackathon_password_2024@localhost:5432/hackathon_db
USE_DATABASE=true

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Pinecone Configuration (Optional for development)
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=hackathon-document-index
EMBEDDING_DIMENSION=1536

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production

# File Upload Configuration
MAX_FILE_SIZE=52428800
UPLOAD_FOLDER=documents
FAISS_INDEX_PATH=vector_store

# Logging
LOG_LEVEL=INFO
EOF
```

### 7. Run Database Migrations

```bash
# Run Alembic migrations to create tables
alembic upgrade head
```

### 8. Start the Application

```bash
# Make sure virtual environment is activated and PostgreSQL is running
source ../hackathon_env/bin/activate  # if not already activated
export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"  # if not in shell profile

# Start the FastAPI server
python -m app.main
```

### 9. Verify Installation

**Access your API:**
- **Health Check**: http://localhost:8000/health
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

**Test commands:**
```bash
# Test health endpoint
curl http://localhost:8000/health

# Check database connection
python -c "from app.core.config import settings; print('DB URL:', settings.DATABASE_URL)"
```

---

## 🪟 Windows Setup

Follow these exact steps after cloning or downloading the project:

---

### 1. Clone or Extract the Project

Assume you cloned or unzipped the project into:

`
D:\A Source Code\Hackathons\hackrx\llm_retrieval_system
`

After this step, **go one directory up** before setting up your environment:

```
cd "D:\A Source Code\Hackathons\hackrx"
```

---

### 2. Create and Activate Virtual Environment

Create your virtual environment **outside** the project directory (in `hackrx` folder) for better separation:

```
python -m venv hackathon_env
.\hackathon_env\Scripts\activate 
```


You should now see your prompt prefixed with `(hackathon_env)`.

---

### 3. Navigate Into Your Project Folder

Now enter your project folder to install dependencies and run commands:

```
cd llm_retrieval_system
```


---

### 4. Install Project Dependencies

Upgrade pip and install dependencies as specified in `requirements.txt` located inside the project folder:

```
pip install --upgrade pip
pip install -r requirements.txt
```


*If you encounter issues installing `psycopg2-binary` (especially on Python 3.12+), check the alternative driver section below.*

---

### 5. Install and Configure PostgreSQL (v17+)

**PostgreSQL installation steps:**

- Download PostgreSQL from [official site](https://www.postgresql.org/download/windows/)
- Install PostgreSQL 17, accept defaults, remember your superuser password.
- Add PostgreSQL's `bin` folder to your Windows PATH:
`C:\Program Files\PostgreSQL\17\bin\`


- Restart your terminal after modifying PATH.

**Create Project Database and User:**

Open `psql` shell:

```
psql -U postgres -h localhost
```


Run inside `psql` prompt:

```
CREATE DATABASE hackathon_db;
CREATE USER hackathon_user WITH ENCRYPTED PASSWORD 'hackathon_password_2024';
GRANT ALL PRIVILEGES ON DATABASE hackathon_db TO hackathon_user;
ALTER SCHEMA public OWNER TO hackathon_user;
GRANT ALL ON SCHEMA public TO hackathon_user;
GRANT CREATE ON SCHEMA public TO hackathon_user;
\q
```


---

### 6. Setup `.env` File

Create or update the `.env` file inside your project folder (`llm_retrieval_system`) with:

```
POSTGRES_SERVER=localhost
POSTGRES_USER=hackathon_user
POSTGRES_PASSWORD=hackathon_password_2024
POSTGRES_DB=hackathon_db
DATABASE_URL=postgresql+psycopg2://hackathon_user:hackathon_password_2024@localhost:5432/hackathon_db
USE_DATABASE=true

OPENAI_API_KEY=your_openai_api_key_here

SECRET_KEY=your-super-secret-key-change-this-in-production

MAX_FILE_SIZE=52428800
UPLOAD_FOLDER=documents
FAISS_INDEX_PATH=vector_store

LOG_LEVEL=INFO
```


---

### 7. Initialize and Run Database Migrations with Alembic

**Initialize Alembic (Only if not already done):**

```
alembic init alembic
```


**Configure `alembic.ini`:**  
Set the database URL:

```
sqlalchemy.url = postgresql+psycopg2://hackathon_user:hackathon_password_2024@localhost:5432/hackathon_db
```


**Configure `alembic/env.py`:**  
Make sure to import your SQLAlchemy Base to support autogeneration:

```
import sys
from pathlib import Path
sys.path.append(str(Path(file).parent.parent))

from app.core.database import Base
target_metadata = Base.metadata
```


**Create Initial Migration and Apply:**

```
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```


---

### 8. Run the Application

Start the server inside the project directory:

```
python -m app.main
```


Access your API at:

- Health endpoint: [http://localhost:8000/health](http://localhost:8000/health)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### 9. Optional: Use `pg8000` Driver Instead of `psycopg2-binary`

If you experience errors installing `psycopg2-binary` (especially on Python 3.12 or higher), switch to `pg8000`:

1. Uninstall psycopg2-binary:

```
pip uninstall psycopg2-binary
```

2. Install `pg8000`:

```
pip install pg8000
```


3. Update `.env`:

```
DATABASE_URL=postgresql+pg8000://hackathon_user:hackathon_password_2024@localhost:5432/hackathon_db
```


No code changes needed beyond this.

---

---

## 🔧 Troubleshooting

### Common Issues (All Platforms)

#### Database Connection Issues
```bash
# Test PostgreSQL connection
psql -U hackathon_user -d hackathon_db -h localhost -c "SELECT current_database(), current_user;"

# Check if PostgreSQL is running
# macOS: brew services list | grep postgresql
# Windows: net start postgresql-x64-17
```

#### Python/Virtual Environment Issues
```bash
# Check Python version
python --version

# Verify virtual environment is active
which python  # should show path to hackathon_env

# Recreate virtual environment if needed
deactivate
rm -rf hackathon_env  # or rmdir /s hackathon_env on Windows
python -m venv hackathon_env
```

#### Import/Dependency Issues
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Check specific import
python -c "import fastapi; print('FastAPI OK')"
```

### Platform-Specific Troubleshooting

#### macOS Issues
- **Homebrew not found**: Install from [brew.sh](https://brew.sh)
- **PostgreSQL connection refused**: Ensure service is running with `brew services start postgresql@14`
- **PATH issues**: Add PostgreSQL to your shell profile (`.zshrc` or `.bash_profile`)
- **Permission denied**: Use `sudo` only if necessary, prefer user-level installations

#### Windows Issues
- **PostgreSQL service not starting**: Run services.msc and start PostgreSQL service manually
- **PATH not updated**: Restart terminal/command prompt after PATH changes
- **psql command not found**: Ensure PostgreSQL bin directory is in PATH
- **Virtual environment activation**: Use `hackathon_env\Scripts\activate` (not `bin/activate`)

### Environment Variable Issues
```bash
# Verify environment loading
python -c "from app.core.config import settings; print('DB URL:', settings.DATABASE_URL)"

# Check .env file exists and has correct permissions
ls -la .env  # macOS/Linux
dir .env     # Windows
```

---

### 11. Quick Test Commands

After activation and inside project folder
Check Python version
```
python --version
```

Verify DB URL and flag
```
python -c "from app.core.config import settings; print(settings.DATABASE_URL, settings.USE_DATABASE)"
```

Test DB connection
```
python -c "from app.core.database import init_database; print('DB init success' if init_database() else 'DB init fail')"
```

Run migrations (ensure alembic.ini is configured)
```
alembic upgrade head
```

Start the app server
```
python -m app.main
```


---

## 🚀 Quick Start Commands

After completing setup, use these commands to start your development session:

### macOS
```bash
# Activate environment and start application
cd ~/path/to/hackrx
source hackathon_env/bin/activate
export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"
cd llm_retrieval_system
python -m app.main
```

### Windows
```bash
# Activate environment and start application
cd "C:\path\to\hackrx"
hackathon_env\Scripts\activate
cd llm_retrieval_system
python -m app.main
```

---

## 📊 Development Status

### ✅ Completed Features
- ✅ FastAPI backend with REST endpoints
- ✅ PostgreSQL database integration
- ✅ SQLAlchemy ORM with Alembic migrations  
- ✅ Document processing pipeline (PDF, DOCX, email)
- ✅ Text chunking and embedding services
- ✅ OpenAI integration for LLM functionality
- ✅ Pinecone vector database support
- ✅ Environment configuration management
- ✅ Comprehensive logging system
- ✅ API documentation (Swagger/ReDoc)
- ✅ Health monitoring endpoints

### 🔧 API Endpoints
- `GET /health` - System health check
- `POST /hackrx/run` - Main query processing endpoint
- `POST /documents/upload` - Document upload
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation

---

## 📚 Useful Links

- [Python Downloads](https://www.python.org/downloads/)
- [Homebrew (macOS)](https://brew.sh)
- [PostgreSQL Downloads](https://www.postgresql.org/download/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/en/latest/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Pinecone Documentation](https://docs.pinecone.io/)

---

## 🤝 Contributing

1. Ensure your development environment is set up correctly
2. Run tests: `pytest`
3. Format code: `black . && isort .`
4. Lint code: `flake8`
5. Submit pull requests with clear descriptions

---

### Happy Hacking! 🎉
Made with 💗 by Team BajajPaglu

**LLM-Powered Intelligent Query-Retrieval System** - Processing documents and making contextual decisions for insurance, legal, HR, and compliance domains.



