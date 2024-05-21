from django.contrib import admin

from offers.models import JobOffer


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = (
        JobOffer.Keys.provider,
        JobOffer.Keys.short_description,
        JobOffer.Keys.external_link,
        JobOffer.Keys.created_at,
        JobOffer.Keys.updated_at,
    )
    ordering = (f"-{JobOffer.Keys.created_at}",)
