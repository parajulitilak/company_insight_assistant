import pytest
import sys
import os
from fastapi.testclient import TestClient
from app.main import app
from app import database, models, schemas, crud
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

SQLALCHEMY_DATABASE_URL = "sqlite:///./data/test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    models.Base.metadata.create_all(bind=engine)
    yield
    models.Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_db):
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[database.get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def seed_test_data(db_session):
    sample_jobs = [
        schemas.JobCreate(title="Data Scientist", location="Argentina"),
        schemas.JobCreate(title="Software Engineer", location="Canada"),
    ]
    for job in sample_jobs:
        db_job = crud.create_job(db_session, job)
        chunk = f"{job.title} in {job.location}"
        embedding_vector = [0.1] * 768  # Mock embedding
        embedding_create = schemas.EmbeddingCreate(job_id=db_job.id, embedding_vector=embedding_vector)
        crud.create_embedding(db_session, embedding_create)
    return sample_jobs

@pytest.mark.asyncio
async def test_query_jobs(client, seed_test_data):
    response = client.post("/query/", json={"query": "Data Scientist jobs"})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["query"] == "Data Scientist jobs"
    assert isinstance(response_data["retrieved_jobs"], list)
    assert len(response_data["retrieved_jobs"]) > 0
    assert "Data Scientist in Argentina" in [job["chunk"] for job in response_data["retrieved_jobs"]]
    assert isinstance(response_data["response"], str)

@pytest.mark.asyncio
async def test_get_jobs(client, seed_test_data):
    response = client.get("/jobs/")
    assert response.status_code == 200
    jobs = response.json()
    assert isinstance(jobs, list)
    assert len(jobs) >= 2
    assert jobs[0]["title"] == "Data Scientist"
    assert jobs[0]["location"] == "Argentina"