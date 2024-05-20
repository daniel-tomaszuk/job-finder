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
        max_length=16, choices=SeniorityName, default=SeniorityName.OTHER
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


class ProviderConfig(models.Model):

    class Keys:
        id = "id"
        config_name = "config_name"
        seniority = "seniority"
        key_word = "key_word"

        # relations
        seniority = "seniority"
        key_word = "key_word"

    config_name = models.CharField(max_length=128)
    seniority = models.ManyToManyField(Seniority, related_name="provider_configs")
    key_word = models.ManyToManyField(KeyWord, related_name="provider_configs")

    def __str__(self) -> str:
        return f"Provider Config - {self.config_name}"


class Provider(models.Model):

    class Key:
        id = "id"
        name = "name"
        base_link = "base_link"

        # relations
        job_offers = "job_offers"
        config = "config"

    name = models.CharField(max_length=128)
    base_link = models.CharField(max_length=512)
    config = models.ForeignKey(
        ProviderConfig, related_name="providers", on_delete=models.PROTECT
    )

    def __str__(self) -> str:
        return f"Provider {self.name.title()}"
