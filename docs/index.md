# RAG Fusemachines Job Assistant

This project implements a Retrieval-Augmented Generation (RAG) system as a FastAPI application to scrape and query job listings from the Fusemachines careers page. It uses Selenium for web scraping, `ollama` for embeddings and response generation, and SQLite for storing job data and embeddings.

## Features
- Scrape job listings from '[Fusemachines](https://fusemachines.com/)'.
- Index jobs with embeddings using the `bge-base-en-v1.5-gguf` model.
- Retrieve relevant jobs using cosine similarity.
- Generate responses to user queries with the `Llama-3.2-1B-Instruct-GGUF` model.
- RESTful API with endpoints for scraping, querying, and retrieving jobs.
- Adheres to the [Twelve-Factor App](https://12factor.net/) methodology for scalable, maintainable deployment.

## Architecture
- **Backend**: FastAPI with SQLAlchemy for database operations.
- **Database**: SQLite for storing job listings and embeddings.
- **Scraping**: Selenium with Firefox for dynamic web content.
- **RAG Components**: Embedding model, vector search, and language model via `ollama`.
- **Logging**: `loguru` for event streams.
- **Deployment**: Dockerized with `docker-compose`.

## Getting Started
See the [Project Setup](rag_project.md) for detailed instructions and API usage.