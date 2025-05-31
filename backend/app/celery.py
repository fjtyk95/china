from __future__ import annotations

from celery import Celery


def create_celery() -> Celery:
    celery_app = Celery(
        "worker",
        broker="redis://redis:6379/0",
        backend="redis://redis:6379/0",
    )
    celery_app.conf.task_routes = {"app.tasks.add": {"queue": "default"}}
    return celery_app

celery_app = create_celery()
