
##### `docs/12-factor-app/backing.md`
Backing services principle.

# 4. Backing Services

> Treat backing services as attached resources

The project uses SQLite as a backing service for storing job listings and embeddings. `ollama` is treated as an external service for embeddings and generation.

## Implementation
- **SQLite**: Configured via `DATABASE_URL` in `.env`.
- **ollama**: Configured via `OLLAMA_HOST`, running locally or remotely.
- **SQLAlchemy**: Manages database connections.

## Setup
# Ensure ollama is running
ollama serve
# Database is created automatically by SQLAlchemy