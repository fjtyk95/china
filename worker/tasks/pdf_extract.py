import io
import json
import os
from typing import List

import boto3
import pandas as pd
import pdfplumber
from celery import shared_task
from sqlalchemy import create_engine, text

S3_BUCKET = os.environ['S3_BUCKET']
DATABASE_URL = os.environ.get('DATABASE_URL')

s3 = boto3.client('s3')
engine = create_engine(DATABASE_URL) if DATABASE_URL else None


def _extract_tables_from_pdf(data: bytes) -> List[pd.DataFrame]:
    tables: List[pd.DataFrame] = []
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                df = pd.DataFrame(table)
                tables.append(df)
    return tables


@shared_task
def extract_tables(job_id: str, s3_key: str) -> str:
    obj = s3.get_object(Bucket=S3_BUCKET, Key=s3_key)
    pdf_bytes = obj['Body'].read()

    tables = _extract_tables_from_pdf(pdf_bytes)
    json_data = [df.to_dict(orient='records') for df in tables]
    json_body = json.dumps(json_data).encode('utf-8')

    output_key = f"processed/{job_id}/tables.json"
    s3.put_object(Bucket=S3_BUCKET, Key=output_key, Body=json_body, ContentType='application/json')

    if engine is not None:
        with engine.begin() as conn:
            conn.execute(
                text("UPDATE jobs SET status='extracted', output_key=:key WHERE id=:id"),
                {"key": output_key, "id": job_id},
            )

    return output_key
