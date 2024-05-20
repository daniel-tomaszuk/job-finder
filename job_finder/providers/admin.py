from django.contrib import admin

from providers.models import Provider


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    pass
