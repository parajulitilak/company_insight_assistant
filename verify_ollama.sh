#!/bin/bash
# verify_ollama.sh
echo "Checking Ollama server..."
curl -f http://localhost:11434 || { echo "Ollama server not running"; exit 1; }
echo "Ollama server is running"

echo "Listing available models..."
docker exec rag_fusemachines ollama list || { echo "Failed to list models"; exit 1; }

echo "Testing embedding model..."
docker exec rag_fusemachines ollama run hf.co/CompendiumLabs/bge-base-en-v1.5-gguf "Test embedding" || \
  docker exec rag_fusemachines ollama run bge-small-en-v1.5 "Test embedding" || \
  { echo "Embedding model test failed"; exit 1; }

echo "Testing chat model..."
docker exec rag_fusemachines ollama run hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF "Hello" || \
  docker exec rag_fusemachines ollama run llama3 "Hello" || \
  { echo "Chat model test failed"; exit 1; }

echo "Ollama verification completed successfully"