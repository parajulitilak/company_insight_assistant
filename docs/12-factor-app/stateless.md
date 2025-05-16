
##### `docs/12-factor-app/stateless.md`
Stateless processes principle.

# 6. Processes

> Execute the app as one or more stateless processes

The FastAPI app is stateless, with all persistent data stored in SQLite.

## Implementation
- **Stateless**: No in-memory state; jobs and embeddings are in the database.
- **SQLAlchemy**: Manages database sessions per request.
- **Avoid Sticky Sessions**: No reliance on session caching.

## Notes
- Use a vector database (e.g., Qdrant) for scalability in production.