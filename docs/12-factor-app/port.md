# 7. Port Binding

> Export services via port binding

The app exports HTTP services via port binding using FastAPI and `uvicorn`.

## Implementation
- **Port**: Configured via `PORT` in `.env` (default 9000).
- **Host**: `HOST=0.0.0.0` for external access.
- **Uvicorn**: Runs the app with `uvicorn app.main:app --host ${HOST} --port ${PORT}`.

## Setup
> uvicorn app.main:app --host 0.0.0.0 --port 9000