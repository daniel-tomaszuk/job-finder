from celery import shared_task
from celery.schedules import crontab

from job_finder import celery_app
from providers.controllers import IndeedScrapperController


@shared_task
def get_provider_results(provider_id: int) -> str:
    IndeedScrapperController().get_results(provider_id)
    return f"New results gathered for Provider ID: {provider_id}"


celery_app.conf.beat_schedule = {
    "get_provider_results": {
        "task": "tasks.get_provider_results",
        "schedule": crontab(hour="12", minute="0"),
    },
}
