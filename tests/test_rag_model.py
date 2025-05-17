from unittest.mock import patch
import pytest
from app.rag_model import generate_embedding, generate_response

@patch("ollama.Client")
def test_generate_embedding(mock_client):
  mock_client.return_value.embed.return_value = {"embeddings": [[0.1, 0.2, 0.3]]}
  result = generate_embedding("test chunk")
  assert result == [0.1, 0.2, 0.3]
  mock_client.return_value.embed.assert_called_with(model="hf.co/CompendiumLabs/bge-base-en-v1.5-gguf", input="test chunk")

@patch("ollama.Client")
def test_generate_response(mock_client):
  mock_client.return_value.chat.return_value = [
    {"message": {"content": "Mocked response"}},
  ]
  retrieved_jobs = [{"chunk": "Job: Data Scientist"}]
  result = generate_response("What jobs?", retrieved_jobs)
  assert "Mocked response" in result
  mock_client.return_value.chat.assert_called()