from app.core.celery_config import celery_app as celery
from app.tasks.stat import run_stat_analysis
celery.autodiscover_tasks(["app.tasks"])
