from celery import shared_task

from providers.controllers import IndeedScrapperController


@shared_task
def get_provider_results(provider_id: int) -> str:
    IndeedScrapperController().get_results(provider_id)
    return f"New results gathered for Provider ID: {provider_id}"
