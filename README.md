# Company Insight Assistant

A **FastAPI** microservice implementing a **Retrieval-Augmented Generation (RAG)** system to scrape, store, and intelligently query job listings from [Fusemachines](https://fusemachines.com/). Built with a modern, modular architecture, powered by **Ollama** for embeddings and text generation, and adhering to the [Twelve-Factor App](https://12factor.net/) methodology. Containerized with Docker and integrated with GitHub Actions for CI/CD.

![CCDS Template](https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter)

## Features

- **RAG Pipeline**: Scrapes job listings, indexes them with semantic embeddings, and answers queries using generative AI.
- **FastAPI Backend**: RESTful API for scraping, querying, and retrieving jobs.
- **Ollama Integration**: Uses `bge-base-en-v1.5-gguf` for embeddings and `Llama-3.2-1B-Instruct-GGUF` for responses, served via a dedicated `ollama` container.
- **Selenium**: Scrapes dynamic content from the Fusemachines careers page in headless mode.
- **SQLite**: Stores job listings and embeddings in `data/jobs.db`.
- **Dockerized**: Multi-service setup with `web`, `ollama`, and `mkdocs` containers.
- **Logging**: Configured with `loguru` for detailed event streams.
- **Testing**: Unit tests in `tests/` using `pytest`.
- **CI/CD**: GitHub Actions workflow for automated testing.
- **Documentation**: MkDocs with 12-Factor App principles and project details.
- Follows **Twelve-Factor App** principles for scalability and maintainability.

## Project Structure

```bash
company_insight_assistant/
├── app/                            # FastAPI application code
│   ├── crud.py
│   ├── database.py
│   ├── logging_config.py
│   ├── main.py
│   ├── models.py
│   ├── rag_model.py
│   ├── schemas.py
│   └── __pycache__/
├── company_insight_assistant/      # Data science utilities
│   ├── config.py
│   ├── dataset.py
│   ├── features.py
│   ├── plots.py
│   └── modeling/
│       ├── predict.py
│       └── train.py
├── data/                           # Data storage
│   ├── external/
│   ├── interim/
│   ├── processed/
│   ├── raw/
│   └── jobs.db
├── docs/                           # MkDocs documentation
│   ├── 12-factor-app/
│   │   ├── admin.md
│   │   ├── backing.md
│   │   ├── build.md
│   │   ├── codebase.md
│   │   ├── concurrency.md
│   │   ├── config.md
│   │   ├── dependency.md
│   │   ├── disposability.md
│   │   ├── index.md
│   │   ├── logging.md
│   │   ├── overview.md
│   │   ├── parity.md
│   │   ├── port.md
│   │   └── stateless.md
│   ├── css/
│   │   └── extra.css
│   ├── index.md
│   ├── mkdocs.yml
│   └── rag_project.md
├── logs/                           # Log files
│   └── info.log
├── models/                         # Model artifacts
├── notebooks/                      # Jupyter notebooks
│   └── rag_scraper_prototype.ipynb
├── references/                     # Reference materials
├── reports/                        # Reports and figures
│   └── figures/
├── scripts/                        # Utility scripts
│   └── scrape_index_jobs.py
├── tests/                          # Unit tests
│   ├── test.py
│   └── test_data.py
├── site/                           # MkDocs generated site
├── .gitignore                      # Git ignore rules
├── .pre-commit-config.yaml         # Pre-commit hooks
├── docker-compose.yml              # Docker Compose configuration
├── Dockerfile                      # Web service Docker image
├── Dockerfile.mkdocs               # MkDocs service Docker image
├── install-extensions.sh            # VS Code extensions
├── LICENSE                         # MIT License
├── Makefile                        # Build automation
├── mkdocs.yml                      # MkDocs configuration
├── ollama_setup.sh                 # FastAPI startup script
├── pyproject.toml                  # Project metadata
├── pytest.ini                      # Pytest configuration
├── README.md                       # Project overview
├── requirements.txt                # Dependencies
├── verify_ollama.sh                # Ollama verification script
```

## Setup & Installation

### Prerequisites

- **Python 3.13**
- **Docker**: For containerized deployment.
- **Git**: For version control.

### 1. Clone the Repository

```bash
git clone https://github.com/parajulitilak/company_insight_assistant.git
cd company_insight_assistant
```

### 2. Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:

```env
DATABASE_URL=sqlite:///./data/jobs.db
LOG_LEVEL=DEBUG
ENVIRONMENT=development
PORT=9000
HOST=0.0.0.0
OLLAMA_HOST=http://localhost:11434
```

### 3. Install Dependencies (Local)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Install Pre-commit Hooks

```bash
pre-commit install
```

### 5. Run with Docker

Build and start services (`ollama`, `web`, `mkdocs`):

```bash
docker compose up --build
```

- **Ollama**: Runs on `http://localhost:11434`.
- **FastAPI**: Runs on `http://localhost:9000`.
- **MkDocs**: Runs on `http://localhost:9090`.

Manually pull Ollama models (if not already pulled):

```bash
docker exec ollama ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
docker exec ollama ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
```

Verify Ollama:

```bash
./verify_ollama.sh
```

## Running the Application

### Locally

```bash
uvicorn app.main:app --host 0.0.0.0 --port 9000
```

### With Docker

```bash
docker compose up -d
```

Run the scraping script:

```bash
docker exec -it rag_fusemachines python scripts/scrape_index_jobs.py
```

## API Endpoints

| Method | Endpoint   | Description                           | Example Request Body                     |
| ------ | ---------- | ------------------------------------- | ----------------------------------------- |
| POST   | `/scrape/` | Scrapes and indexes job listings      | None                                     |
| POST   | `/query/`  | Queries jobs using RAG pipeline       | `{"query": "Data Scientist jobs"}`       |
| GET    | `/jobs/`   | Returns all stored job listings       | None                                     |
| GET    | `/health/` | Checks API health                     | None                                     |

### Example Queries

#### Scrape Jobs

```bash
curl -X POST http://localhost:9000/scrape/
```

#### Query Jobs

```bash
curl -X POST http://localhost:9000/query/ \
  -H "Content-Type: application/json" \
  -d '{"query": "What data scientist jobs are available?"}'
```

#### List Jobs

```bash
curl http://localhost:9000/jobs/
```

#### Health Check

```bash
curl http://localhost:9000/health/
```

## Scripts

- **`scripts/scrape_index_jobs.py`**: Scrapes and indexes job listings.

```bash
python scripts/scrape_index_jobs.py
```

## Testing

Run unit tests:

```bash
pytest tests/ -v
```

In Docker:

```bash
docker exec rag_fusemachines pytest tests/ -v
```

## Documentation

Serve MkDocs locally:

```bash
mkdocs serve
```

Or use Docker:

```bash
docker compose up mkdocs
```

Access at `http://localhost:9090`. Includes:
- Project overview (`docs/index.md`, `docs/rag_project.md`).
- 12-Factor App principles (`docs/12-factor-app/`).

## Development Workflow

- **Branching**: Uses `main` (production) and `develop` (integration). Create `feature/*` or `fix/*` branches from `develop`.
- **Commits**: Use descriptive messages (e.g., `Add GitHub Actions CI workflow`).
- **CI/CD**: GitHub Actions (`ci.yml`) runs tests on push/PR to `main` or `develop`.
- **PRs**: Create pull requests from `develop` to `main` after tests pass.

## Contributing

1. Fork the repository.
2. Create a `feature/*` or `fix/*` branch.
3. Commit changes and run tests.
4. Push and open a PR to `develop`.

## License

MIT License. See `LICENSE` for details.

## Credits

- Inspired by [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/).
- Based on [Hugging Face RAG tutorial](https://huggingface.co/blog/ngxson/make-your-own-rag).
- Built for the Fusemachines AI Fellowship 2025.


