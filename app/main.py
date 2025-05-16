from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas, database, rag_model
from .logging_config import logger
from contextlib import asynccontextmanager

app = FastAPI(title="Fusemachines RAG Job Assistant")

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy"}

models.Base.metadata.create_all(bind=database.engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    logger.info("Starting up FastAPI application")
    yield
    logger.info("Shutting down FastAPI application")

app = FastAPI(title="Fusemachines RAG Job Assistant", lifespan=lifespan)

@app.post("/scrape/", response_model=List[schemas.JobResponse])
async def scrape_jobs(db: Session = Depends(database.get_db)):
    """Scrape and index job listings from Fusemachines."""
    logger.info("Received scrape request")
    try:
        jobs = rag_model.scrape_fusemachines_jobs()
        for job in jobs:
            job_create = schemas.JobCreate(title=job["title"], location=job["location"])
            db_job = crud.create_job(db, job_create)
            chunk = f"{job['title']} in {job['location']}"
            embedding_vector = rag_model.generate_embedding(chunk)
            embedding_create = schemas.EmbeddingCreate(job_id=db_job.id, embedding_vector=embedding_vector)
            crud.create_embedding(db, embedding_create)
        return crud.get_jobs(db)
    except Exception as e:
        logger.error(f"Scrape error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query/", response_model=schemas.QueryResponse)
async def query_jobs(query: schemas.QueryRequest, db: Session = Depends(database.get_db)):
    """Query job listings and generate a response."""
    logger.info(f"Received query: {query.query}")
    try:
        retrieved = rag_model.retrieve_jobs(query.query, db)
        response = rag_model.generate_response(query.query, retrieved)
        return schemas.QueryResponse(query=query.query, retrieved_jobs=retrieved, response=response)
    except Exception as e:
        logger.error(f"Query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs/", response_model=List[schemas.JobResponse])
async def get_jobs(db: Session = Depends(database.get_db)):
    """Retrieve all job listings."""
    logger.info("Fetching all jobs")
    try:
        return crud.get_jobs(db)
    except Exception as e:
        logger.error(f"Get jobs error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))