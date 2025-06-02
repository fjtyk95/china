import os
from fastapi.testclient import TestClient
from moto import mock_s3
import boto3
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from api.main import app
from api.db import Base, get_db
from api.models import Job

@pytest.fixture(autouse=True)
def override_db():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def _get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_db
    yield TestingSessionLocal
    app.dependency_overrides.clear()

@mock_s3
def test_create_job(override_db):
    os.environ["S3_BUCKET"] = "test-bucket"
    s3 = boto3.client("s3", region_name="us-east-1")
    s3.create_bucket(Bucket="test-bucket")

    client = TestClient(app)
    token = jwt.encode({"sub": "user123"}, "secret", algorithm="HS256")
    pdf = b"hello"
    resp = client.post(
        "/v1/jobs",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("sample.pdf", pdf, "application/pdf")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "queued"

    objects = s3.list_objects_v2(Bucket="test-bucket")
    assert any(o["Key"] == f"uploads/{data['job_id']}/sample.pdf" for o in objects.get("Contents", []))

    Session = override_db
    db = Session()
    job = db.query(Job).filter_by(id=data["job_id"]).first()
    assert job is not None
    assert job.status == "queued"
    db.close()
