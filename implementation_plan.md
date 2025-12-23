# Implementation Plan - Project Lexicon (MVP)

# Goal
Build a "Legal-Grade" RAG system using FastAPI and PostgreSQL (pgvector) to securely ingest documents and answer legal queries with audit trails.

## User Review Required
> [!IMPORTANT]
> **API Keys**: I will need your `OPENAI_API_KEY` (or Azure equivalent) to configure the embedding and generation models. I will assume standard OpenAI for now for simplicity unless you provide Azure details.
> **Docker**: Ensure Docker Desktop is running.

## Proposed Changes

### Infrastructure
#### [NEW] [docker-compose.yml](file:///Users/jasdeep.bhangal/.gemini/antigravity/playground/RAG-agent/docker-compose.yml)
- PostgreSQL 16 image with `pgvector/pgvector:pg16`
- n8n image (optional, can be added later if needed, focusing on core stack first)
- Environment variables configuration

### Backend (Python/FastAPI)
#### [NEW] [backend/requirements.txt](file:///Users/jasdeep.bhangal/.gemini/antigravity/playground/RAG-agent/backend/requirements.txt)
- `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2-binary`, `pgvector`, `haystack-ai`, `python-multipart`

#### [NEW] [backend/database.py](file:///Users/jasdeep.bhangal/.gemini/antigravity/playground/RAG-agent/backend/database.py)
- SQLAlchemy engine setup and session management.

#### [NEW] [backend/models.py](file:///Users/jasdeep.bhangal/.gemini/antigravity/playground/RAG-agent/backend/models.py)
- `Document` model
- `DocumentChunk` model (with Vector column)
- `AuditLog` model

#### [NEW] [backend/main.py](file:///Users/jasdeep.bhangal/.gemini/antigravity/playground/RAG-agent/backend/main.py)
- `/ingest` endpoint
- `/query` endpoint

#### [NEW] [backend/rag_service.py](file:///Users/jasdeep.bhangal/.gemini/antigravity/playground/RAG-agent/backend/rag_service.py)
- Haystack 2.0 pipeline logic for cleaning/splitting.
- Embedding generation logic.

## Verification Plan

### Automated Tests
- **Ingestion Test**:
    - `curl -X POST -F "file=@test_contract.pdf" http://localhost:8000/ingest`
    - Verify `SELECT count(*) FROM document_chunks` > 0
- **Retrieval Test**:
    - `curl -X POST -d '{"query": "termination clause"}' http://localhost:8000/query`
    - Verify response contains answer and citations.
    - Verify `SELECT count(*) FROM audit_logs` increased.

### Manual Verification
- I will create a `test_contract.txt` dummy file to run the tests against.
