from django.db import models
from scrapping_process.models import ScrappingProcess


class Provider(models.Model):

    class Keys:
        id = "id"
        name = "name"

        # relations
        job_offers = "job_offers"
        scrapping_process = "scrapping_process"

    name = models.CharField(max_length=128)
    base_link = models.CharField(max_length=512)
    scrapping_process = models.ForeignKey(
        ScrappingProcess,
        related_name="providers",
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self) -> str:
        return self.name.title()
