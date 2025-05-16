
##### `docs/12-factor-app/config.md`
Configuration principle.

# 3. Config

> Store config in the environment

Configuration is stored in a `.env` file and loaded using `python-dotenv`.

## Implementation
- **.env**:

  DATABASE_URL=sqlite:///./data/jobs.db

  LOG_LEVEL=DEBUG

  ENVIRONMENT=development

  PORT=9000

  HOST=0.0.0.0
  
  OLLAMA_HOST=http://localhost:11434