# LLM-Powered Query Retrieval System - Complete Development Workflow

This document outlines a step-by-step workflow for building the hackathon project described in the problem statement. Each phase contains discrete tasks, setup instructions, and explicit test points to ensure quality at every stage.

---

## Phase 1: Project Setup & Foundation

### Task 1.1 – Environment Setup
* **Setup**  
  ```bash
  python -m venv hackathon_env
  source hackathon_env/bin/activate  # on Unix/macOS
  # or .\hackathon_env\Scripts\activate on Windows
  pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
  pip install langchain openai pinecone-client faiss-cpu python-docx PyPDF2
  pip install pytest requests httpx
  ```
* **Test** – Run `python - <<<'import fastapi, uvicorn, sqlalchemy, openai'` – no import errors.

### Task 1.2 – Project Structure Setup
* **Setup**  
  ```text
  llm_retrieval_system/
  ├── app/
  │   ├── __init__.py
  │   ├── main.py
  │   ├── core/
  │   │   ├── config.py
  │   │   └── database.py
  │   ├── models/
  │   ├── schemas/
  │   ├── services/
  │   └── utils/
  ├── tests/
  ├── documents/
  ├── .env
  ├── requirements.txt
  └── README.md
  ```
* **Test** – `uvicorn app.main:app --reload` starts and `/docs` loads.

### Task 1.3 – Basic FastAPI Application
* **Setup** – Create minimal FastAPI app with `/health` endpoint.
* **Test** – `curl http://localhost:8000/health` returns `{"status":"ok"}`.

**🔍 Milestone 1 Check** – Basic FastAPI server up and healthy.

---

## Phase 2: Database & Data Models

### Task 2.1 – PostgreSQL Setup
* **Setup** – Spin up PostgreSQL (Docker or local), add connection string in `.env`.
* **Test** – `psql` connects; Alembic creates initial tables.

### Task 2.2 – Data Models Design
* **Setup** – Create SQLAlchemy models:
  * `Document` – id, filename, content, file_type, upload_date
  * `DocumentChunk` – id, document_id, chunk_text, chunk_index
  * `Embedding` – id, chunk_id, vector_data, embedding_model
  * `Query` – id, query_text, response, timestamp
* **Test** – CRUD operations in unit tests succeed.

### Task 2.3 – Migration System
* **Setup** – Configure Alembic autogeneration.
* **Test** – `alembic upgrade head` and `alembic downgrade -1` work.

**🔍 Milestone 2 Check** – Database schema stable and operational.


---

## Phase 3: Document Processing Pipeline

### Task 3.1 – Document Upload Handler
* **Setup** – `POST /documents/upload` endpoint; accept PDF, DOCX, EML.
* **Test** – Upload sample files and verify persistence.

### Task 3.2 – Text Extraction Services
* **Setup** – Implement:
  * PDF → PyPDF2
  * DOCX → python-docx
  * E-mail (.eml) → email.parser
* **Test** – Content extracted matches source files.

### Task 3.3 – Chunking Strategy
* **Setup** – Sentence-based chunking with 20–30 % overlap, token budget awareness.
* **Test** – All chunks ≤ LLM context window and maintain coherence.

**🔍 Milestone 3 Check** – Documents upload, extract, and chunk correctly.

---

## Phase 4: Embedding & Vector Search

### Task 4.1 – Embedding Generation
* **Setup** – Integrate OpenAI `text-embedding-3*` or Sentence-Transformers.
* **Test** – Embeddings length matches model dimensionality.

### Task 4.2 – FAISS Vector Store
* **Setup** – Create FAISS index, persist to disk, reload on startup.
* **Test** – Similarity search on indexed corpus returns expected neighbors.

### Task 4.3 – Vector Search API
* **Setup** – `POST /search` embedding query → k-NN search → ranked chunks.
* **Test** – Search for known phrases returns correct chunks.

**🔍 Milestone 4 Check** – Semantic search fully functional.

---

## Phase 5: LLM Integration & Query Processing

### Task 5.1 – LLM Client Setup
* **Setup** – OpenAI GPT-4 client with exponential back-off and token-usage logging.
* **Test** – Simple prompt/response round-trip succeeds.

### Task 5.2 – Query Processing Pipeline
1. Embed user query
2. Retrieve top-k chunks via FAISS
3. Construct system + context prompt
4. Call GPT-4
5. Stream or return answer
* **Test** – End-to-end QA on sample docs produces accurate answers.

### Task 5.3 – Response Formatting
* **Setup** – Return JSON `{answer, sources, confidence}`.
* **Test** – Schema validated by Pydantic.

**🔍 Milestone 5 Check** – Full query-to-answer path stable.

---

## Phase 6: API Development & Validation

### Task 6.1 – Core Endpoints
* `/hackrx/run` – main QA route  
* Document CRUD  
* Health endpoints
* **Test** – All routes return expected status codes.

### Task 6.2 – Validation
* **Setup** – Pydantic models for all inputs/outputs.
* **Test** – Invalid payloads → 422 with clear message.

### Task 6.3 – Auth & AuthZ
* **Setup** – Bearer/ JWT token-based auth.
* **Test** – Protected endpoints require valid token.

**🔍 Milestone 6 Check** – API meets spec and validates data.

---

## Phase 7: Performance Optimization

### Task 7.1 – Token Optimization
* Prompt compression, message pruning, partial context recall.
* **Test** – Measure token reduction ≥ 20 % vs baseline.

### Task 7.2 – Latency Optimization
* Async I/O, database indexes, HTTP keep-alive.
* **Test** – 95-th percentile latency ≤ desired SLA.

### Task 7.3 – Batch Processing
* **Setup** – Batch embeddings & FAISS adds.
* **Test** – Throughput meets multi-document ingestion needs.

**🔍 Milestone 7 Check** – Performance KPIs achieved.

---

## Phase 8: Testing & Quality Assurance

### Task 8.1 – Unit Tests
* Focus on utils, services, and core logic.
* **Goal** – ≥ 90 % coverage.

### Task 8.2 – Integration Tests
* End-to-end document → query pipeline.
* Fault injection & error-handling paths.

### Task 8.3 – API Tests
* Use sample policy doc; verify clause matching accuracy.

**🔍 Milestone 8 Check** – All tests green; quality gate passed.

---

## Phase 9: Deployment & Containerization

### Task 9.1 – Dockerization
* **Setup** – Multi-stage `Dockerfile`; `docker-compose.yml` with Postgres.
* **Test** – `docker compose up` exposes app on `localhost:8000`.

### Task 9.2 – Production Config
* Logging, metrics, environment vars, graceful shutdown.

### Task 9.3 – Deployment Docs
* README sections: prerequisites, env setup, quick-start commands.

**🔍 Milestone 9 Check** – Containers run in prod parity env.

---

## Phase 10: Final Integration & Submission

### Task 10.1 – System Testing
* Load + stress testing, memory profiling, chaos engineering basics.

### Task 10.2 – Documentation & Review
* Architecture diagram, API reference, ADRs, inline docstrings.

### Task 10.3 – Submission Package
* Clean repo, sample `.env.example`, screencast demo, slide deck.

**🔍 Final Milestone** – Hackathon-ready system delivered.

---

### Evaluation Criteria Alignment
| Criterion      | Where Addressed (Phase) |
|----------------|-------------------------|
| Accuracy       | 5, 8                    |
| Token Efficiency | 7                      |
| Latency        | 7, 8                    |
| Reusability    | 1, 2                    |
| Explainability | 5                       |

---

*Happy hacking!*