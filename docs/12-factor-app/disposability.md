
##### `docs/12-factor-app/disposability.md`
Disposability principle.

# 9. Disposability

> Maximize robustness with fast startup and graceful shutdown

The app starts quickly and shuts down gracefully.

## Implementation
- **Lifespan Events**: FastAPI’s `lifespan` handles startup/shutdown.
- **Docker**: Ensures fast container startup.
- **SIGTERM**: Graceful shutdown via `uvicorn`.

## Setup
- Handled automatically by `docker-compose`.