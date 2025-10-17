from celery import Celery
from app.config import REDIS_URL
celery_app = Celery("app", broker=REDIS_URL, backend=REDIS_URL)
celery_app.conf.task_track_started = True
celery_app.conf.worker_prefetch_multiplier = 1
