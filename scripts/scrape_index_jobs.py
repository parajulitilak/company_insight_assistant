from pathlib import Path
from app import crud, database, rag_model
from sqlalchemy.orm import Session
from app.logging_config import logger

def scrape_and_index_jobs():
    """Scrape Fusemachines jobs and index them in the database. Admin script to scrape and index jobs"""
    logger.info("Starting scrape and index process")
    try:
        jobs = rag_model.scrape_fusemachines_jobs()
        db = next(database.get_db())
        for job in jobs:
            job_create = crud.schemas.JobCreate(title=job["title"], location=job["location"])
            db_job = crud.create_job(db, job_create)
            chunk = f"{job['title']} in {job['location']}"
            embedding_vector = rag_model.generate_embedding(chunk)
            embedding_create = crud.schemas.EmbeddingCreate(job_id=db_job.id, embedding_vector=embedding_vector)
            crud.create_embedding(db, embedding_create)
        logger.info(f"Indexed {len(jobs)} jobs")
    except Exception as e:
        logger.error(f"Error in scrape and index: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    scrape_and_index_jobs()