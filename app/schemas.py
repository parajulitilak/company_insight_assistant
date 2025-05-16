from pydantic import BaseModel
from typing import List

class JobCreate(BaseModel):
    title: str
    location: str

class JobResponse(JobCreate):
    id: int

    class Config:
        from_attributes = True

class EmbeddingCreate(BaseModel):
    job_id: int
    embedding_vector: List[float]

class QueryRequest(BaseModel):
    query: str

    class Config:
        schema_extra = {
            "example": {
                "query": "What data scientist jobs are available?"
            }
        }

class QueryResponse(BaseModel):
    query: str
    retrieved_jobs: List[dict]  # List of (chunk, similarity) dicts
    response: str