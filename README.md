# Project Lexicon ⚖️

> **Legal-Grade RAG (Retrieval-Augmented Generation) Engine**
> *Secure, private, and precise AI for legal workflows.*

## Overview
Project Lexicon is a specialized RAG architecture designed for the legal domain. It allows law firms to securely ingest contracts and legal documents, index them using local, privacy-preserving embeddings, and query them using high-intelligence LLMs (Claude 3.5 Sonnet) to get precise, cited answers.

This MVP demonstrates a "Legal-Grade" approach where **data privacy** and **retrieval accuracy** are paramount.

## MVP Features (Current Status)
*   **Local Embeddings**: Uses `BAAI/bge-small-en-v1.5` running locally on CPU/Silicon. No client data is sent to OpenAI/3rd-parties for vectorization.
*   **Vector Database**: PostgreSQL 16 with `pgvector` for scalable, relational+vector storage.
*   **Intelligence Layer**: Integrated with **Anthropic Claude 3.5 Sonnet** for top-tier legal reasoning and drafting.
*   **Audit Logging**: Every query and response is logged to the database for compliance and review.
*   **Infrastructure**: Fully Dockerized backbone.

## Tech Stack
*   **Backend**: Python, FastAPI, SQLAlchemy
*   **Database**: PostgreSQL + pgvector
*   **AI/ML**: 
    *   *Retrieval*: `sentence-transformers` (HuggingFace)
    *   *Generation*: Anthropic API (Claude)
    *   *Orchestration*: Haystack 2.0 components

## Getting Started

### Prerequisites
*   Docker Desktop
*   Python 3.10+
*   Anthropic API Key

### Installation

1.  **Clone the repo**
    ```bash
    git clone https://github.com/jxs-21/Project-Lexicon.git
    cd Project-Lexicon
    ```

2.  **Environment Setup**
    ```bash
    cp .env.example .env
    # Edit .env and add your ANTHROPIC_API_KEY
    ```

3.  **Start Database**
    ```bash
    docker compose up -d
    ```

4.  **Run Backend**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r backend/requirements.txt
    uvicorn backend.main:app --reload
    ```

## Usage

**Ingest a Document:**
```bash
curl -X POST -F "file=@your_contract.txt" http://localhost:8000/ingest
```

**Ask a Question:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"query": "What is the termination notice period?"}' http://localhost:8000/query
```

## Upgrade Paths (Roadmap)
*   [ ] **PDF & OCR Support**: Integrate `pymupdf` or `unstructured` to handle complex PDFs and scanned documents.
*   [ ] **Frontend**: Next.js dashboard for lawyers to upload files and chat.
*   [ ] **Citations**: UI overlay showing the exact paragraph source for every claim.
*   [ ] **Multi-Tenancy**: Workspace isolation for different clients/matters.
