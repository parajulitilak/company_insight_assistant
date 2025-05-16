#!/bin/bash
# ollama_setup.sh

# Verify Ollama binary
if ! command -v ollama >/dev/null 2>&1; then
  echo "Error: Ollama binary not found"
  exit 1
fi

# Check Ollama version
echo "Checking Ollama version..."
if ! ollama --version; then
  echo "Error: Ollama binary is not executable or corrupted"
  exit 1
fi

# Start Ollama server
echo "Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama server to be ready (max 120 seconds)
timeout 120 bash -c 'until curl -f http://127.0.0.1:11434 > /dev/null 2>&1 || curl -f http://127.0.0.1:11434/api/version > /dev/null 2>&1; do
  echo "Waiting for Ollama server to start..."
  sleep 2
done'
if [ $? -eq 0 ]; then
  echo "Ollama server is up, pulling models..."
  ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf || { echo "Failed to pull bge-base-en-v1.5-gguf, trying fallback..."; ollama pull bge-small-en-v1.5 || exit 1; }
  ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF || { echo "Failed to pull Llama-3.2-1B-Instruct-GGUF, trying fallback..."; ollama pull llama3 || exit 1; }
else
  echo "Error: Ollama server failed to start within 120 seconds"
  kill $OLLAMA_PID
  exit 1
fi

# Start FastAPI
exec uvicorn app.main:app --host 0.0.0.0 --port 9000