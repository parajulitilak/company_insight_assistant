
##### `docs/12-factor-app/build.md`
Build, release, run principle.

# 5. Build, Release, Run

> Strictly separate build and run stages

The project uses Docker to separate build, release, and run stages.

## Implementation
- **Build**: `Dockerfile` installs dependencies and copies code.
- **Release**: `docker-compose.yml` applies environment-specific configuration.
- **Run**: `uvicorn` runs the FastAPI app.
- **GitHub Actions**: Automates testing and deployment (configurable).

## Setup
docker-compose up --build