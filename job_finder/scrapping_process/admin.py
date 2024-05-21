from django.contrib import admin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.utils.html import format_html
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
    readonly_fields = ("related_scrapping_steps",)

    def related_scrapping_steps(self, obj: ScrappingProcess) -> str:
        related_steps: QuerySet[ScrappingStep] = ScrappingStep.objects.filter(
            process_id=obj.id
        ).order_by(ScrappingStep.Keys.order)
        if not related_steps:
            return "Process has no steps!"

        related_steps_html: str = ""
        for step in related_steps:
            related_steps_html += (
                f'<br><a href={self.__get_reverse_url(step)} target="_blank">{step}</a>'
            )

        return format_html(related_steps_html)

    @staticmethod
    def __get_reverse_url(obj: ScrappingStep) -> str:
        return reverse_lazy(
            f"admin:{obj._meta.app_label}_{obj._meta.model_name}_change", args=(obj.id,)
        )
