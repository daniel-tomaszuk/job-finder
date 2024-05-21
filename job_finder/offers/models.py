from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from providers.models import Provider


class JobOffer(models.Model):

    class Keys:
        id = "id"
        link = "link"
        short_description = "short_description"
        created_at = "created_at"
        updated_at = "updated_at"

        # admin panel
        external_link = "external_link"

        # relations
        provider = "provider"

    link = models.CharField(max_length=512, unique=True)
    short_description = models.CharField(max_length=1024, null=True, blank=True)
    provider = models.ForeignKey(
        Provider,
        related_name="job_offers",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.provider} | {self.short_description}"

    @admin.display
    def external_link(self):
        return format_html('<a href={url} target="_blank">Link</a>', url=self.link)
