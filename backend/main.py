from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import uvicorn
import shutil
import os

from .database import engine, get_db, Base
from .models import Document, DocumentChunk, AuditLog
from .rag_service import RAGService

# Create Tables (for MVP simplification)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Lexicon RAG API")
rag_service = RAGService()

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Save File Temporarily or Read content
    # For text/pdf, simplified to reading text for MVP
    # Ideally should handle PDF parsing.
    # Assuming text file for MVP as per plan "test_contract.txt"
    
    content = (await file.read()).decode("utf-8")
    
    # 2. Store Document Record
    db_doc = Document(filename=file.filename, content=content)
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    
    # 3. Process & Splitting
    processed_docs = rag_service.process_file(content, file.filename)
    
    # 4. Store Chunks
    for chunk in processed_docs:
        # Check if embedding exists (might be mock or None)
        embedding_val = chunk.embedding if hasattr(chunk, "embedding") and chunk.embedding is not None else None
        
        db_chunk = DocumentChunk(
            document_id=db_doc.id,
            content=chunk.content,
            embedding=embedding_val
        )
        db.add(db_chunk)
    
    db.commit()
    
    return {"status": "success", "document_id": db_doc.id, "chunks_count": len(processed_docs)}

@app.post("/query")
async def query_documents(query: dict, db: Session = Depends(get_db)):
    query_text = query.get("query")
    if not query_text:
        raise HTTPException(status_code=400, detail="Query text required")
    
    # 1. Embed Query
    query_embedding = rag_service.embed_query(query_text)
    
    # 2. Search (using pgvector L2 distance)
    # Note: <-> is L2 distance operator in pgvector
    results = db.query(DocumentChunk).order_by(
        DocumentChunk.embedding.l2_distance(query_embedding)
    ).limit(3).all()
    
    response_text = "Found relevant chunks:\n" + "\n---\n".join([r.content for r in results])
    
    # 3. Audit Log
    audit = AuditLog(
        query_text=query_text,
        response_text=response_text
    )
    db.add(audit)
    db.commit()
    
    return {
        "query": query_text,
        "results": [{"content": r.content, "id": r.id} for r in results],
        "answer": "This is a retrieval-only MVP response. LLM generation to be added."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
