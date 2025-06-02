import os
from celery import Celery

celery_app = Celery(
    'worker',
    broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1'),
)

celery_app.autodiscover_tasks(['worker.tasks'])

__all__ = ('celery_app',)
