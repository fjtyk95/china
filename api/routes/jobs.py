import os
import urllib.request
from uuid import uuid4
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Header
from sqlalchemy.orm import Session
import boto3
from jose import jwt, JWTError

from ..db import get_db
from ..models import Job

router = APIRouter()

@router.post("/jobs")
async def create_job(
    file: UploadFile = File(...),
    authorization: str | None = Header(None),
    db: Session = Depends(get_db),
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split()[1]
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET", "secret"), algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid token")

    job_id = str(uuid4())
    s3_key = f"uploads/{job_id}/{file.filename}"
    bucket = os.environ["S3_BUCKET"]
    s3 = boto3.client("s3")
    presigned_url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": bucket, "Key": s3_key},
        ExpiresIn=3600,
        HttpMethod="PUT",
    )
    file_content = await file.read()
    request = urllib.request.Request(presigned_url, data=file_content, method="PUT")
    with urllib.request.urlopen(request) as _:
        pass

    job = Job(id=job_id, user_id=user_id, s3_key=s3_key, status="queued")
    db.add(job)
    db.commit()
    return {"job_id": job_id, "status": "queued"}
