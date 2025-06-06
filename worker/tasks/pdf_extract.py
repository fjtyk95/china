import os
import json
import io
import uuid
import boto3
import pandas as pd
import pdfplumber

from worker.celery_app import celery_app
from worker.database import SessionLocal
from worker.models import Job

@celery_app.task
def extract_tables(job_id: str, s3_key: str):
    bucket = os.environ['S3_BUCKET']
    s3 = boto3.client('s3')

    obj = s3.get_object(Bucket=bucket, Key=s3_key)
    pdf_data = obj['Body'].read()

    tables = []
    with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables() or []:
                if not table:
                    continue
                df = pd.DataFrame(table[1:], columns=table[0])
                tables.append(df.to_dict(orient='records'))

    out_key = f"processed/{job_id}_tables.json"
    s3.put_object(Bucket=bucket, Key=out_key, Body=json.dumps(tables))

    session = SessionLocal()
    try:
        job = session.query(Job).filter_by(id=job_id).first()
        if job:
            job.status = 'extracted'
            session.commit()
    finally:
        session.close()

    return {'output_key': out_key, 'table_count': len(tables)}
