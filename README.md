<<<<<<< HEAD
# company_insight_assistant
Retrieval-Augmented Generation (RAG) prototype using FastAPI, Selenium, and Ollama — built with 12-Factor App principles, containerized with Docker, and powered by LLMs for querying real-time company data.
=======
# RAG Fusemachines Job Assistant

A **FastAPI** microservice implementing a **Retrieval-Augmented Generation (RAG)** system to scrape, store, and intelligently query job listings from [Fusemachines](https://fusemachines.com/). Built with a modern, modular architecture, powered by **Ollama** for embeddings and text generation, and adhering to the [Twelve-Factor App](https://12factor.net/) methodology.

![CCDS Template](https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter)

## Features

- **RAG Pipeline**: Scrapes job listings, indexes them with semantic embeddings, and answers queries using generative AI.
- **FastAPI Backend**: RESTful API with endpoints for scraping, querying, and retrieving jobs.
- **Ollama Integration**: Uses `bge-base-en-v1.5-gguf` for embeddings and `Llama-3.2-1B-Instruct-GGUF` for response generation.
- **Selenium**: Scrapes dynamic content from the Fusemachines careers page.
- **SQLite**: Lightweight storage for job listings and embeddings.
- **Dockerized**: Ensures portability and consistent deployment.
- **Logging**: Uses `loguru` for event streams.
- **Testing**: Unit tests with `pytest` for reliability.
- **CI/CD Ready**: Configured with pre-commit hooks and GitHub Actions support.
- Follows **Twelve-Factor App** principles for scalability and maintainability.

## Project Structure

```bash
rag_fusemachines/
├── app/                    # FastAPI application code
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── logging_config.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── rag_model.py
├── data/                   # SQLite database
│   └── jobs.db
├── docs/                   # MkDocs documentation
│   ├── 12-factor-app/
│   │   ├── admin.md
│   │   ├── backing.md
│   │   ├── build.md
│   │   ├── codebase.md
│   │   ├── concurrency.md
│   │   ├── config.md
│   │   ├── dependency.md
│   │   ├── disposability.md
│   │   ├── logging.md
│   │   ├── overview.md
│   │   ├── parity.md
│   │   ├── port.md
│   │   └── stateless.md
│   ├── index.md
│   └── rag_project.md
├── scripts/                # Admin scripts
│   └── scrape_index_jobs.py
├── tests/                  # Unit tests
│   └── test.py
├── css/                    # Custom CSS for MkDocs
│   └── extra.css
├── .env                    # Environment variables
├── .gitignore              # Git ignore rules
├── .pre-commit-config.yaml # Pre-commit hooks
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker image definition
├── install-extensions.sh    # VS Code extensions
├── mkdocs.yml              # MkDocs configuration
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Dependencies
└── README.md               # Project overview
```

## Setup & Installation

### 1. Install Ollama and Models

Install [Ollama](https://ollama.com) and pull the required models:

```bash
ollama pull hf.co/CompendiumLabs/bge-base-en-v1.5-gguf
ollama pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
```

Start the Ollama server:

```bash
ollama serve
```

### 2. System Requirements

- **Python 3.10**
- **Geckodriver**: Install for Firefox automation and add to your `PATH` ([instructions](https://firefox-source-docs.mozilla.org/testing/geckodriver/)).
- **Docker**: Optional, for containerized deployment.

### 3. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment

Copy the example environment file and edit as needed:

```bash
cp .env.example .env
```

Ensure your `.env` includes:

```env
DATABASE_URL=sqlite:///./data/jobs.db
LOG_LEVEL=DEBUG
ENVIRONMENT=development
PORT=9000
HOST=0.0.0.0
OLLAMA_HOST=http://localhost:11434
```

### 6. Install Pre-commit Hooks

```bash
pre-commit install
```

## Running the Application

### Locally

```bash
uvicorn app.main:app --host 0.0.0.0 --port 9000
```

### With Docker

```bash
docker-compose up --build
```

To run the admin script in Docker:

```bash
docker exec -it rag_fusemachines python scripts/scrape_index_jobs.py
```

## API Endpoints

| Method | Endpoint   | Description                           | Example Request Body                     |
| ------ | ---------- | ------------------------------------- | ----------------------------------------- |
| POST   | `/scrape/` | Scrapes and indexes job listings      | None                                     |
| POST   | `/query/`  | Queries jobs using RAG pipeline       | `{"query": "Data Scientist jobs"}`       |
| GET    | `/jobs/`   | Returns all stored job listings       | None                                     |

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

#### List All Jobs

```bash
curl http://localhost:9000/jobs/
```

## Scripts

- **`scripts/scrape_index_jobs.py`**: Manually scrape and index job listings.

```bash
python scripts/scrape_index_jobs.py
```

## Running Tests

Run unit tests to verify functionality:

```bash
pytest
```

## Documentation

View project documentation using MkDocs:

1. Install MkDocs:

```bash
pip install mkdocs
```

2. Serve documentation:

```bash
mkdocs serve
```

3. Access at `http://localhost:9090`.

Alternatively, use the `mkdocs` service in `docker-compose.yml`:

```bash
docker-compose up mkdocs
```

Documentation includes:
- Project overview and setup (`docs/index.md`, `docs/rag_project.md`).
- Twelve-Factor App principles (`docs/12-factor-app/`).

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Credits

- Inspired by the [Cookiecutter Data Science](https://drivendata.github.io/cookiecutter-data-science/) template.
- Based on the Hugging Face article [Code a simple RAG from scratch](https://huggingface.co/blog/ngxson/make-your-own-rag).
- Built for the Fusemachines AI Fellowship 2025.
>>>>>>> 8841274 (Initial commit with FastAPI, Ollama, and MkDocs setup)
