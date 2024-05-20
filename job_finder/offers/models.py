from django.db import models
from scrapping_process.models import Seniority

from providers.models import Provider


class JobOffer(models.Model):

    class Keys:
        id = "id"
        link = "link"
        seniority = "seniority"
        short_description = "short_description"

        # relations
        provider = "provider"

    link = models.CharField(max_length=512)
    seniority = models.CharField(
        max_length=16,
        choices=Seniority.SeniorityName,
        default=Seniority.SeniorityName.OTHER,
    )
    short_description = models.CharField(max_length=1024, null=True, blank=True)
    provider = models.ForeignKey(
        Provider,
        related_name="job_offers",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self) -> str:
        return f"{self.provider} | {self.seniority} | {self.short_description}"
