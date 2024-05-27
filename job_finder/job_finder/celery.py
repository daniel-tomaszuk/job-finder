import os

from celery import Celery
from celery.schedules import crontab
from django.apps import apps
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_finder.settings")

celery_app = Celery("job_finder", broker=settings.CELERY_BROKER_URL)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.


celery_app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
celery_app.conf.beat_schedule = {
    "get_provider_results": {
        "task": "providers.tasks.get_provider_results_in_bulk",
        "schedule": crontab(hour="*", minute="0"),
    },
}
