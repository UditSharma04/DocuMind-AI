# DocuMind AI - Backend API

**FastAPI Backend for Intelligent Document Query System**

This is the backend API for DocuMind AI, providing document processing, semantic search, and AI-powered answer generation capabilities.

## 🚀 Tech Stack

- **FastAPI**: Modern, high-performance Python web framework
- **PostgreSQL**: Reliable relational database
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Alembic**: Database migration management
- **Sentence Transformers**: Local embedding generation (`all-MiniLM-L6-v2`)
- **Google Gemini AI**: LLM for intelligent answer generation
- **NumPy**: Vector operations and cosine similarity calculations
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX file processing

## 📋 Prerequisites

### macOS
- **Homebrew** (install from [brew.sh](https://brew.sh))
- **Python 3.12+**
- **PostgreSQL 14+**
- **Google Gemini API Key**

### Windows
- **Python 3.12+**
- **PostgreSQL 14+**
- **Google Gemini API Key**

## 🛠️ Setup Instructions

### 1. Navigate to Backend Directory

```bash
cd llm_retrieval_system
```

### 2. Create and Activate Virtual Environment

#### macOS/Linux
```bash
# Create virtual environment
python3 -m venv ../hackathon_env

# Activate virtual environment
source ../hackathon_env/bin/activate
```

#### Windows
```bash
# Create virtual environment
python -m venv ..\hackathon_env

# Activate virtual environment
..\hackathon_env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install and Configure PostgreSQL

#### macOS
```bash
# Install PostgreSQL
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14

# Add PostgreSQL to PATH
export PATH="/opt/homebrew/opt/postgresql@14/bin:$PATH"

# Create database and user
createdb hackathon_db
psql hackathon_db -c "CREATE USER hackathon_user WITH PASSWORD 'your_secure_password';"
psql hackathon_db -c "GRANT ALL PRIVILEGES ON DATABASE hackathon_db TO hackathon_user;"
psql hackathon_db -c "GRANT ALL ON SCHEMA public TO hackathon_user;"
```

#### Windows
1. Download and install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. During installation, remember your postgres superuser password
3. Open pgAdmin or Command Prompt and create database:

```sql
CREATE DATABASE hackathon_db;
CREATE USER hackathon_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE hackathon_db TO hackathon_user;
```

### 5. Configure Environment Variables

Create a `.env` file in the `llm_retrieval_system` directory:

```bash
# Database Configuration
DATABASE_ENABLED=true
DATABASE_URL=postgresql+psycopg2://hackathon_user:your_secure_password@localhost:5432/hackathon_db

# Google Gemini AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=models/gemini-2.0-flash

# Pinecone Configuration (Optional - system works without it)
PINECONE_API_KEY=your_pinecone_api_key_here
EMBEDDING_DIMENSION=384

# File Upload Configuration
UPLOAD_FOLDER=documents
MAX_UPLOAD_SIZE=10485760  # 10MB in bytes
```

**Note**: Get your free Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### 6. Run Database Migrations

```bash
# Run Alembic migrations to create database tables
alembic upgrade head
```

### 7. Start the Development Server

```bash
# Start FastAPI server
python -m app.main
```

The API will be available at [http://localhost:8000](http://localhost:8000)

## 📁 Project Structure

```
llm_retrieval_system/
├── alembic/                    # Database migrations
│   ├── versions/              # Migration scripts
│   └── env.py                 # Alembic configuration
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI application entry point
│   ├── api/                   # API route handlers
│   │   ├── document_routes.py    # Document upload/management
│   │   ├── query_routes.py       # Search and query endpoints
│   │   ├── hackrx_routes.py      # Main Q&A endpoint
│   │   └── demo_routes.py        # Demo/testing endpoints
│   ├── core/                  # Core configuration
│   │   ├── config.py             # Settings management
│   │   └── database.py           # Database connection
│   ├── models/                # SQLAlchemy ORM models
│   │   ├── document.py           # Document model
│   │   ├── document_chunk.py     # Document chunk model
│   │   ├── embedding.py          # Embedding model
│   │   └── query.py              # Query model
│   ├── services/              # Business logic
│   │   ├── document_processor.py  # Document processing
│   │   ├── text_extractor.py      # Text extraction (PDF/DOCX)
│   │   ├── chunking_service.py    # Text chunking
│   │   ├── embedding_service.py   # Embedding generation
│   │   ├── search_service.py      # Semantic search
│   │   ├── llm_service.py         # Gemini AI integration
│   │   └── pinecone_service.py    # Vector database (optional)
│   └── utils/                 # Utility functions
├── documents/                 # Uploaded documents storage
├── logs/                      # Application logs
├── static/                    # Static files
├── .env                       # Environment variables (create this)
├── alembic.ini               # Alembic configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔌 API Endpoints

### Health Check
- `GET /health` - Check API status and version

### Document Management
- `POST /api/v1/documents/upload` - Upload a document (PDF, DOCX, TXT)
- `GET /api/v1/documents/` - List all documents
- `GET /api/v1/documents/{id}` - Get document details
- `DELETE /api/v1/documents/{id}` - Delete a document

### Query Processing
- `POST /hackrx/run` - Submit questions and get AI-generated answers
  - **Headers**: `Authorization: Bearer {token}`
  - **Body**: 
    ```json
    {
      "documents": ["document-1", "document-2"],
      "questions": ["Question 1", "Question 2"]
    }
    ```
  - **Response**:
    ```json
    {
      "answers": ["Answer 1", "Answer 2"]
    }
    ```

### Search
- `POST /api/v1/query/semantic-search` - Perform semantic search
- `POST /api/v1/query/ask` - Ask a question and get an answer

### Interactive API Documentation
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🔧 Key Features

### Document Processing
- **Multi-Format Support**: PDF, DOCX, DOC, TXT
- **Intelligent Chunking**: 1000 characters with 200-character overlap
- **Metadata Extraction**: File type, upload date, size
- **Automatic Storage**: Database + file system

### Semantic Search
- **Cosine Similarity**: Real vector similarity scoring
- **Hybrid Scoring**: Semantic (70%) + Keyword (30%)
- **Stopword Filtering**: Ignores common words
- **Exact Phrase Matching**: +15% bonus for exact matches
- **Document Filtering**: Search specific documents only

### AI Integration
- **Google Gemini**: Free tier with generous quota
- **Context-Aware**: Uses only retrieved document chunks
- **Citation Tracking**: References specific documents
- **No Hallucination**: Limited to provided context
- **Reasoning Included**: Explains conclusions

### Performance Optimization
- **On-the-Fly Embeddings**: Generates embeddings as needed
- **Batch Processing**: Efficient bulk operations
- **Async Operations**: FastAPI async/await support
- **Connection Pooling**: Efficient database connections

## 🔒 Security Features

- **Bearer Token Authentication**: API endpoint protection
- **SQL Injection Prevention**: SQLAlchemy parameterized queries
- **File Upload Validation**: Type and size restrictions
- **CORS Configuration**: Configurable cross-origin access
- **Environment Variables**: Sensitive data protection

## 🐛 Troubleshooting

### PostgreSQL Connection Issues
```bash
# Check if PostgreSQL is running
brew services list  # macOS
# or
pg_ctl status       # Windows

# Restart PostgreSQL
brew services restart postgresql@14  # macOS
```

### Module Import Errors
```bash
# Ensure virtual environment is activated
which python  # Should show path to venv

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Database Migration Errors
```bash
# Check current migration status
alembic current

# Reset to head
alembic downgrade base
alembic upgrade head
```

### Gemini API Errors
- Verify your API key in `.env`
- Check quota limits at [Google AI Studio](https://makersuite.google.com/)
- Try different model: `GEMINI_MODEL=models/gemini-pro`

## 📊 Performance Metrics

- **Document Processing**: ~100 chunks/second
- **Embedding Generation**: ~50 embeddings/second (local)
- **Semantic Search**: <1 second for 1000+ chunks
- **AI Answer Generation**: 5-15 seconds (depends on Gemini API)

## 🧪 Testing

```bash
# Run basic health check
curl http://localhost:8000/health

# Test document upload
curl -X POST http://localhost:8000/api/v1/documents/upload \
  -F "file=@test.pdf"

# Test query endpoint
curl -X POST http://localhost:8000/hackrx/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_token" \
  -d '{
    "documents": ["document-1"],
    "questions": ["What is this document about?"]
  }'
```

## 🔄 Database Schema

### Documents Table
- `id`: Primary key
- `filename`: Original filename
- `file_type`: File extension
- `upload_date`: Timestamp
- `content`: Full text content

### Document Chunks Table
- `id`: Primary key
- `document_id`: Foreign key to documents
- `chunk_index`: Sequence number
- `chunk_text`: Text content
- `vector_data`: 384-dim embedding vector

### Embeddings Table
- `id`: Primary key
- `chunk_id`: Foreign key to chunks
- `model_name`: Embedding model used
- `status`: Processing status

## 🚀 Deployment

### Docker (Recommended)
```bash
# Build image
docker build -t documind-backend .

# Run container
docker run -p 8000:8000 --env-file .env documind-backend
```

### Production Considerations
- Use production-grade WSGI server (Gunicorn + Uvicorn workers)
- Enable HTTPS with SSL certificates
- Configure proper CORS settings
- Set up database backups
- Implement rate limiting
- Add monitoring and logging

## 📚 Dependencies

Key packages:
- `fastapi>=0.104.0` - Web framework
- `uvicorn>=0.24.0` - ASGI server
- `sqlalchemy>=2.0.0` - ORM
- `alembic>=1.12.0` - Migrations
- `psycopg2-binary>=2.9.9` - PostgreSQL adapter
- `sentence-transformers>=2.2.0` - Local embeddings
- `google-generativeai>=0.3.0` - Gemini AI
- `numpy>=1.24.0` - Vector operations
- `PyPDF2>=3.0.1` - PDF processing
- `python-docx>=0.8.11` - DOCX processing

## 🔄 Updates and Maintenance

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head

# Check logs
tail -f logs/app.log
```

## 📝 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_ENABLED` | No | `true` | Enable database functionality |
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `GEMINI_API_KEY` | Yes | - | Google Gemini API key |
| `GEMINI_MODEL` | No | `models/gemini-2.0-flash` | Gemini model name |
| `PINECONE_API_KEY` | No | - | Pinecone API key (optional) |
| `EMBEDDING_DIMENSION` | No | `384` | Embedding vector dimension |
| `UPLOAD_FOLDER` | No | `documents` | Document storage directory |
| `MAX_UPLOAD_SIZE` | No | `10485760` | Max file size (10MB) |

## 🎓 Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Sentence Transformers](https://www.sbert.net/)

---

**Made with ❤️ by Udit Sharma**
