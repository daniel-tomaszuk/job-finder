from django.contrib import admin
from scrapping_process.models import ScrappingProcess
from scrapping_process.models import ScrappingStep
from scrapping_process.models import Selector
from scrapping_process.models import Seniority


@admin.register(Seniority)
class SeniorityAdmin(admin.ModelAdmin):
    pass


@admin.register(Selector)
class SelectorAdmin(admin.ModelAdmin):
    pass


@admin.register(ScrappingStep)
class SelectorAdmin(admin.ModelAdmin):
    pass


@admin.register(ScrappingProcess)
class SelectorAdmin(admin.ModelAdmin):
    pass
