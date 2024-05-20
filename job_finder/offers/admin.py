from django.contrib import admin

from offers.models import JobOffer


@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = (
        JobOffer.Keys.provider,
        JobOffer.Keys.seniority,
        JobOffer.Keys.short_description,
        JobOffer.Keys.link,
    )
