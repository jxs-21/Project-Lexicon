# Technical Architecture: Project Lexicon (PostgreSQL Edition)

**Date:** 2025-12-23
**Status:** Approved

## 1. Architectural Strategy
We are choosing **PostgreSQL with `pgvector`** as the unified data backbone.
**Why this shows expertise:** Instead of naively adding more tools (complexity), we are leveraging a robust, ACID-compliant relational database to handle both structured data (users, logs, permissions) and unstructured data (vectors). This eliminates synchronization issues and creates a "single source of truth" for compliance.

## 2. Infrastructure Components
- **Orchestration:** n8n (Dockerized) - *The "Traffic Controller"*
- **API Gateway & Logic:** FastAPI (Python 3.11+) - *The "Brain"*
- **Database:** PostgreSQL 16+ (with `pgvector` extension) - *The "Vault"*
- **LLM Provider:** Azure OpenAI (GPT-4o) - *The "Engine"*

## 3. Data Schema (The "Legal-Grade" Foundation)

We will use three primary tables to ensure strict referential integrity.

### A. `documents`
*The raw source files.*
- `id` (UUID, PK)
- `filename` (String)
- `uploaded_at` (Timestamp)
- `ingestion_status` (Enum: PENDING, PROCESSED, ERROR)
- `owner_id` (String - for RBAC)

### B. `document_chunks`
*The searchable vectors. Linked to documents with CASCADE delete.*
- `id` (UUID, PK)
- `document_id` (UUID, FK -> documents.id)
- `content` (Text - the actual 500-token chunk)
- `page_number` (Int)
- `embedding` (VECTOR[1536]) - *Indexed with HNSW for speed*

### C. `audit_logs`
*The immutable compliance record.*
- `id` (UUID, PK)
- `timestamp` (Timestamp)
- `user_id` (String)
- `query_text` (Text)
- `retrieved_chunk_ids` (Array[UUID]) - *Which specific text did the AI see?*
- `generated_response` (Text)

## 4. API Specification (FastAPI)

### POST `/ingest/`
- **Input:** File (PDF/DOCX), Metadata (JSON)
- **Process:**
  1. Save file to temp storage.
  2. Haystack Pipeline: Clean -> Split -> Embed.
  3. **Transaction:** Insert into `documents` AND `document_chunks`.
- **Output:** `{"document_id": "...", "chunks_created": 42}`

### POST `/query/`
- **Input:** `{"query": "...", "user_id": "..."}`
- **Process:**
  1. Embed query (using local or Azure embedding).
  2. **Security Filter:** Select top 5 chunks FROM `document_chunks` WHERE `embedding` <=> query AND `document_id` IN (allowed_docs).
  3. Construct Prompt with User Query + Chunks.
  4. Call GPT-4o.
  5. **Transaction:** Save record to `audit_logs` then return response.
- **Output:** `{"answer": "...", "citations": [{"doc_id": "...", "text": "..."}]}`

## 5. Development Plan (Vertical Slices)

1.  **Foundation:** Spin up Docker Compose (Postgres + pgvector).
2.  **The API Skeleton:** Create FastAPI app with SQLAlchemy models.
3.  **Ingestion:** Implement the /ingest endpoint with Haystack components.
4.  **Retrieval:** Implement the /query endpoint with vector search.
5.  **Orchestration:** Create the n8n Workflow to talk to the API.
