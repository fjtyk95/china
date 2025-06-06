from celery import Celery
import os

broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
backend_url = os.getenv("CELERY_RESULT_BACKEND", broker_url)

celery_app = Celery("worker", broker=broker_url, backend=backend_url)
celery_app.autodiscover_tasks(['worker.tasks'])
