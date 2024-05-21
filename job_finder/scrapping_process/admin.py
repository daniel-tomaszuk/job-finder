from django.contrib import admin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.utils.html import format_html

from providers.models import Provider
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
    list_display = (
        ScrappingStep.Keys.name,
        ScrappingStep.Keys.order,
        ScrappingStep.Keys.process,
    )
    ordering = (
        ScrappingStep.Keys.process,
        ScrappingStep.Keys.order,
    )


@admin.register(ScrappingProcess)
class SelectorAdmin(admin.ModelAdmin):
    list_display = (ScrappingProcess.Keys.name,)
    readonly_fields = ("related_providers", "related_scrapping_steps")

    def related_scrapping_steps(self, obj: ScrappingProcess) -> str:
        related_steps: QuerySet[ScrappingStep] = ScrappingStep.objects.filter(
            process_id=obj.id
        ).order_by(ScrappingStep.Keys.order)
        return self.__get_related_object_html(related_steps)

    def related_providers(self, obj: ScrappingProcess) -> str:
        related_providers: QuerySet[Provider] = Provider.objects.filter(
            scrapping_process_id=obj.id
        )
        return self.__get_related_object_html(related_providers)

    def __get_related_object_html(self, objects_list: QuerySet) -> str:
        if not objects_list:
            return "No related objects!"

        related_objects_html: str = ""
        for obj in objects_list:
            related_objects_html += (
                f'<br><a href={self.__get_reverse_url(obj)} target="_blank">{obj}</a>'
            )

        return format_html(related_objects_html)

    @staticmethod
    def __get_reverse_url(obj: ScrappingStep | Provider) -> str:
        return reverse_lazy(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change", args=(obj.id,)
        )
