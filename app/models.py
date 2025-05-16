from sqlalchemy import Column, Integer, String, Text, ForeignKey
from .database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    location = Column(String, nullable=False)

class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    embedding_vector = Column(Text, nullable=False)  # Store as JSON string