from fastapi.testclient import TestClient
from moto import mock_s3
import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models import Base

BUCKET = "jobs-bucket"


@mock_s3
def test_create_job(tmp_path, monkeypatch):
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket=BUCKET)

    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    token = "test"
    data = {"file": ("test.pdf", b"content", "application/pdf")}
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/v1/jobs", files=data, headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "queued"
    assert "job_id" in body
