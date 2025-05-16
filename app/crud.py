from sqlalchemy.orm import Session
from . import models, schemas
from .logging_config import logger
import json

def create_job(db: Session, job: schemas.JobCreate):
    """Create a job listing in the database."""
    try:
        db_job = models.Job(title=job.title, location=job.location)
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        logger.info(f"Created job: {job.title} in {job.location}")
        return db_job
    except Exception as e:
        logger.error(f"Error creating job: {e}")
        raise

def create_embedding(db: Session, embedding: schemas.EmbeddingCreate):
    """Create an embedding for a job in the database."""
    try:
        embedding_vector = json.dumps(embedding.embedding_vector)
        db_embedding = models.Embedding(job_id=embedding.job_id, embedding_vector=embedding_vector)
        db.add(db_embedding)
        db.commit()
        db.refresh(db_embedding)
        logger.info(f"Created embedding for job_id: {embedding.job_id}")
        return db_embedding
    except Exception as e:
        logger.error(f"Error creating embedding: {e}")
        raise

def get_jobs(db: Session):
    """Retrieve all job listings."""
    try:
        jobs = db.query(models.Job).all()
        logger.info(f"Retrieved {len(jobs)} jobs")
        return jobs
    except Exception as e:
        logger.error(f"Error retrieving jobs: {e}")
        raise

def get_embedding(db: Session, job_id: int):
    """Retrieve embedding for a job by job_id."""
    try:
        embedding = db.query(models.Embedding).filter(models.Embedding.job_id == job_id).first()
        if embedding:
            logger.info(f"Retrieved embedding for job_id: {job_id}")
            return embedding
        logger.warning(f"No embedding found for job_id: {job_id}")
        return None
    except Exception as e:
        logger.error(f"Error retrieving embedding for job_id {job_id}: {e}")
        raise