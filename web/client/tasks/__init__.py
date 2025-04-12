from celery import Celery
from celery.schedules import crontab

celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['src.tasks.scan_tasks']
)

celery.conf.beat_schedule = {}
celery.conf.timezone = 'UTC'
