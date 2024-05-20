from django.contrib import admin

from providers.models import KeyWord
from providers.models import Provider
from providers.models import ProviderConfig
from providers.models import Seniority


@admin.register(Seniority)
class SeniorityAdmin(admin.ModelAdmin):
    pass


@admin.register(KeyWord)
class KeyWordAdmin(admin.ModelAdmin):
    pass


@admin.register(ProviderConfig)
class ProviderConfigAdmin(admin.ModelAdmin):
    pass


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    pass
