FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./worker

CMD ["celery", "-A", "worker.celery_app", "worker", "--loglevel=info"]
