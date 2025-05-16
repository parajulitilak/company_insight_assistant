
##### `docs/12-factor-app/dependency.md`
Dependencies principle.

# 2. Dependencies

> Explicitly declare and isolate dependencies

Dependencies are declared in `requirements.txt` and isolated using a virtual environment or Docker.

## Implementation
- **Pip**: Installs dependencies via `pip install -r requirements.txt`.
- **Virtualenv**: Created with `python -m venv venv`.
- **Docker**: Installs dependencies in a containerized environment.
- **Key Dependencies**:
  - `fastapi`, `uvicorn`: Web framework and server.
  - `selenium`, `ollama`: Scraping and RAG components.
  - `sqlalchemy`, `loguru`: Database and logging.

## Setup
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt