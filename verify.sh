#!/bin/bash

# 1. Start DB
echo "Starting Database..."
docker compose up -d
sleep 5 # Wait for DB to start

# 2. Start Backend
echo "Starting Backend..."
# Assuming venv is active or available
export DATABASE_URL="postgresql://user:password@localhost:5432/lexicon"
# export OPENAI_API_KEY="sk-..." # User needs to set this if testing embedding
nohup uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
PID=$!
sleep 5 # Wait for App to start

# 3. Test Ingest
echo "Testing Ingestion..."
curl -X POST -F "file=@test_contract.txt" http://localhost:8000/ingest

echo "\n"

# 4. Test Query
echo "Testing Query..."
curl -X POST -H "Content-Type: application/json" -d '{"query": "termination duration"}' http://localhost:8000/query

echo "\n"

# 5. Cleanup
echo "Stopping Backend (PID: $PID)..."
kill $PID
