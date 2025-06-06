from celery import Celery

BROKER_URL = "redis://redis:6379/0"


def create_celery() -> Celery:
    app = Celery("worker", broker=BROKER_URL)
    app.autodiscover_tasks(['worker.tasks'])
    return app


celery_app = create_celery()
