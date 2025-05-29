from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from uuid import uuid4
import boto3
import urllib.request
from sqlalchemy.orm import Session
from .database import get_db
from .models import Job
from .jwt import verify_token

app = FastAPI()

security = HTTPBearer()


class JobResponse(BaseModel):
    job_id: str
    status: str


@app.post("/v1/jobs", response_model=JobResponse)
async def create_job(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    if not verify_token(credentials.credentials):
        raise HTTPException(status_code=401, detail="Invalid token")

    job_id = str(uuid4())
    s3 = boto3.client("s3")
    bucket = "jobs-bucket"
    url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket, "Key": job_id},
        ExpiresIn=300,
    )
    content = await file.read()
    req = urllib.request.Request(url, data=content, method="PUT")
    with urllib.request.urlopen(req) as resp:
        if resp.status not in (200, 204):
            raise HTTPException(status_code=500, detail="Upload failed")

    job = Job(id=job_id, filename=file.filename, status="queued")
    db.add(job)
    db.commit()

    return JobResponse(job_id=job_id, status="queued")
