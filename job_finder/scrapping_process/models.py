from django.db import models


class Seniority(models.Model):
    class Keys:
        id = "id"
        name = "name"

        # relations
        provider_configs = "provider_configs"

    class Meta:
        verbose_name_plural = "seniorities"

    class SeniorityName(models.TextChoices):
        JUNIOR = "junior", "junior"
        MID = "mid", "mid"
        REGULAR = "regular", "regular"
        SENIOR = "senior", "senior"
        OTHER = "other", "other"

    name = models.CharField(
        max_length=16,
        choices=SeniorityName,
        default=SeniorityName.OTHER,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name.title()


class KeyWord(models.Model):
    class Keys:
        id = "id"
        key_word = "key_word"

        # relations
        provider_configs = "provider_configs"

    key_word = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"Key Word: {self.key_word.upper()}"


class Selector(models.Model):
    class Keys:
        id = "id"
        selector_type = "selector_type"
        selector_value = "selector_value"

    class SelectorType(models.TextChoices):
        selector_id = "element_id", "element_id"
        selector_class = "class_name", "class_name"
        selector_link = "partial_link_text", "partial_link_text"
        selector_css = "css_selector", "css_selector"
        selector_none = "selector_none", "selector_none"

    selector_type = models.CharField(max_length=32, choices=SelectorType)
    selector_value = models.CharField(max_length=256)

    def __str__(self) -> str:
        return f"{self.selector_type} | {self.selector_value}"


class ScrappingProcess(models.Model):
    class Keys:
        id = "id"
        name = "name"

        # relations
        steps = "steps"
        provider_configs = "provider_configs"

    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f"Scrapping Process {self.name}"


class ScrappingStep(models.Model):
    class Keys:
        id = "id"
        name = "name"
        is_input_step = "is_input_step"
        get_many_elements = "get_many_elements"
        order = "order"

        # relations
        selector = "selector"
        key_words = "key_words"
        process = "process"

    class Meta:
        ordering = ["order"]

    name = models.CharField(max_length=128)
    key_words = models.CharField(max_length=512, null=True, blank=True)
    is_input_step = models.BooleanField(default=False)
    get_many_elements = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    selector = models.ForeignKey(
        Selector, related_name="scrapping_steps", on_delete=models.CASCADE
    )
    process = models.ForeignKey(
        ScrappingProcess, related_name="steps", null=True, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"Scrapping step - {self.process.name} | {self.order}"
