
##### `docs/12-factor-app/concurrency.md`
Concurrency principle.

# 8. Concurrency

> Scale out via the process model

The app supports concurrency through multiple `uvicorn` workers.

## Implementation
- **Uvicorn Workers**: Configurable via `gunicorn` or `uvicorn --workers`.
- **Asyncio**: FastAPI uses async endpoints for concurrent requests.
- **Process Model**: Docker allows scaling via multiple containers.

## Setup

# Example with multiple workers
> gunicorn -k uvicorn.workers.UvicornWorker -w 4 app.main:app