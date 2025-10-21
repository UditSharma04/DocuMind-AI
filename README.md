# DocuMind AI

**Intelligent Document Query System powered by AI & Vector Search**

DocuMind AI is a full-stack RAG (Retrieval-Augmented Generation) system that allows users to upload documents and ask intelligent questions about their content. The system uses advanced semantic search with embeddings and Google Gemini AI to provide accurate, contextual answers.

## 🌟 Overview

DocuMind AI bridges the gap between unstructured documents and intelligent information retrieval. Whether you're working with insurance policies, research papers, resumes, or legal documents, DocuMind AI helps you find answers instantly without reading through hundreds of pages.

### Key Features

- **📤 Multi-Format Document Upload**: Support for PDF, DOCX, DOC, and TXT files
- **📊 Smart Document Management**: Visual interface to view, select, and manage uploaded documents
- **🔍 Semantic Search**: Advanced embedding-based search using sentence transformers
- **🤖 AI-Powered Answers**: Contextual responses powered by Google Gemini AI
- **🎯 Selective Context**: Choose specific documents for targeted queries
- **⚡ Real-Time Processing**: Fast document chunking and embedding generation
- **💾 Persistent Storage**: PostgreSQL database for reliable data management
- **🎨 Modern UI**: Beautiful, responsive Next.js interface with TypeScript

## 🏗️ Architecture

### Technology Stack

#### Backend
- **FastAPI**: High-performance Python web framework
- **PostgreSQL**: Relational database for document storage
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migration management
- **Sentence Transformers**: Local embedding generation (`all-MiniLM-L6-v2`)
- **Google Gemini AI**: LLM for answer generation
- **NumPy**: Vector operations and cosine similarity

#### Frontend
- **Next.js 15**: React framework with Turbopack
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Shadcn/ui**: Beautiful UI components
- **Axios**: HTTP client for API communication
- **React Query**: Server state management

### System Flow

```
1. Document Upload
   ↓
2. Text Extraction (PDF/DOCX/TXT)
   ↓
3. Intelligent Chunking (1000 chars with 200 overlap)
   ↓
4. Embedding Generation (384-dim vectors)
   ↓
5. Storage (PostgreSQL + Vector embeddings)
   ↓
6. User Query → Semantic Search (Cosine Similarity)
   ↓
7. Context Retrieval (Top-K relevant chunks)
   ↓
8. AI Answer Generation (Google Gemini)
   ↓
9. Structured Response with Citations
```

## 🎯 How It Works

### 1. Document Processing
When you upload a document, DocuMind AI:
- Extracts text content from various formats
- Splits content into semantically meaningful chunks (1000 characters with 200-character overlap)
- Generates 384-dimensional vector embeddings for each chunk
- Stores chunks and embeddings in PostgreSQL for fast retrieval

### 2. Semantic Search
When you ask a question:
- Your question is converted into a 384-dimensional vector embedding
- The system calculates cosine similarity between your question and all document chunks
- Applies stopword filtering to focus on meaningful keywords
- Adds keyword bonuses for exact phrase matches (+15%) and word matches (+10%)
- Returns the top-K most relevant chunks with confidence scores

### 3. AI Answer Generation
With relevant context retrieved:
- Top 5 most relevant chunks are sent to Google Gemini AI
- AI generates a comprehensive answer based only on the provided context
- Response includes reasoning and document citations
- Prevents hallucination by limiting AI to retrieved information

### 4. Document Selection
Users have full control:
- View all uploaded documents with metadata (file type, upload date, chunk count)
- Select specific documents for targeted queries
- Use "Select All" for comprehensive searches across all documents
- Delete unwanted or outdated documents

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL 14+
- Google Gemini API Key

### Quick Start

#### Backend Setup
```bash
cd llm_retrieval_system
# Follow setup instructions in llm_retrieval_system/README.md
```

#### Frontend Setup
```bash
cd hackrx-frontend
# Follow setup instructions in hackrx-frontend/README.md
```

**Note**: Detailed setup instructions for each component are available in their respective README files.

## 📊 Features in Detail

### Document Management
- **Upload**: Drag-and-drop or click to upload PDF, DOCX, or TXT files
- **View**: See all uploaded documents with file type badges and metadata
- **Select**: Choose specific documents for context-aware queries
- **Delete**: Remove documents with cascade deletion (chunks + embeddings)

### Intelligent Search
- **Semantic Understanding**: Understands meaning, not just keywords
- **Stopword Filtering**: Ignores filler words like "and", "the", "under"
- **Phrase Matching**: Prioritizes exact phrase matches
- **Multi-Document**: Search across selected documents simultaneously
- **Confidence Scoring**: Each result includes relevance score

### AI Integration
- **Context-Aware**: Answers based only on your documents
- **Citation Tracking**: References specific documents and sections
- **No Hallucination**: AI limited to retrieved information
- **Reasoning Included**: Explains how conclusions were reached

## 🎨 User Interface

### Three-Tab Design
1. **Upload Tab**: Beautiful drag-and-drop document upload interface
2. **Manage Tab**: Document library with search and deletion capabilities
3. **Query Tab**: Document selector and intelligent Q&A interface

### Real-Time Updates
- Live health monitoring
- Instant document list refresh
- Progress indicators for long-running operations
- Success/error notifications

## 🔒 Security & Privacy

- **Local Processing**: All embeddings generated locally (no external API calls)
- **Secure Storage**: PostgreSQL with proper authentication
- **API Authentication**: Bearer token validation
- **Data Isolation**: Each document's chunks are properly isolated
- **Cascade Deletion**: Complete data removal when documents are deleted

## 💰 Cost Efficiency

- **$0/month for embeddings**: Uses local sentence-transformers model
- **Google Gemini Free Tier**: Generous free quota for answer generation
- **No Pinecone**: Avoids $70+/month vector database costs
- **PostgreSQL**: Free, reliable, battle-tested storage

## 📈 Performance

- **Fast Embedding**: ~100 chunks/second on M1/M2 MacBook
- **Quick Search**: Cosine similarity on 1000+ chunks in <1 second
- **Efficient Chunking**: Optimal 1000-character chunks with overlap
- **Cached Models**: Sentence transformer loaded once, reused

## 🛠️ Technical Highlights

### Advanced Features
- ✅ Cosine similarity-based semantic search
- ✅ Hybrid scoring (semantic + keyword)
- ✅ On-the-fly embedding generation
- ✅ Document-specific context filtering
- ✅ Stopword-aware keyword extraction
- ✅ Exact phrase matching bonuses
- ✅ Batch embedding generation
- ✅ Cascade delete relationships
- ✅ Real-time health monitoring
- ✅ Comprehensive error handling

### Code Quality
- ✅ TypeScript for type safety
- ✅ SQLAlchemy ORM with proper models
- ✅ Alembic migrations for schema versioning
- ✅ FastAPI async operations
- ✅ Comprehensive logging
- ✅ Structured error responses
- ✅ Component-based React architecture
- ✅ Responsive Tailwind CSS design

## 📝 Use Cases

### Insurance & Legal
- Query policy terms and conditions
- Find specific exclusions and coverage details
- Compare clauses across multiple documents

### Research & Academia
- Search through research papers
- Find methodology sections
- Extract specific findings and citations

### HR & Recruitment
- Search resumes for specific skills
- Find project experience details
- Match candidates to job requirements

### Business Documents
- Query contracts and agreements
- Find specific terms and conditions
- Extract financial data and metrics

## 🎯 Future Enhancements

- [ ] Support for more file formats (Excel, PowerPoint)
- [ ] Multi-language support
- [ ] Document comparison features
- [ ] Export answers to PDF/Word
- [ ] User authentication and multi-tenancy
- [ ] Cloud deployment with Docker
- [ ] Real-time collaborative queries
- [ ] Advanced analytics dashboard

## 📄 License

© 2024 Udit Sharma. All rights reserved.

This project is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

## 👨‍💻 Author

**Made with ❤️ by Udit Sharma**

---

*DocuMind AI - Making documents intelligent, one query at a time.*

