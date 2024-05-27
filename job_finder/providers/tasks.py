from celery import shared_task

from providers.controllers import IndeedScrapperController
from providers.models import Provider


@shared_task()
def get_provider_results(provider_id: int | None = None) -> str:
    providers: list[int] = (
        [provider_id]
        if provider_id
        else list(Provider.objects.all().values_list(Provider.Keys.id, flat=True))
    )
    for provider_id in providers:
        IndeedScrapperController().get_results(provider_id)
    return f"New results gathered for Provider ID: {provider_id}"


@shared_task()
def get_provider_results_in_bulk():
    # Fires multiple tasks at once - one task per provider
    providers: list[int] = list(
        Provider.objects.all().values_list(Provider.Keys.id, flat=True)
    )
    for provider_id in providers:
        get_provider_results.delay(provider_id)
    return "Scheduled multiple providers scrapping!"
