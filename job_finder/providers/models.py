from django.db import models


class Seniority(models.Model):
    class Keys:
        id = "id"
        name = "name"

        # relations
        provider_configs = "provider_configs"

    class SeniorityName(models.TextChoices):
        JUNIOR = "junior", "junior"
        MID = "mid", "mid"
        REGULAR = "regular", "regular"
        SENIOR = "senior", "senior"
        OTHER = "other", "other"

    name = models.CharField(
        max_length=16, choices=SeniorityName, default=SeniorityName.OTHER
    )


class KeyWord(models.Model):
    class Keys:
        id = "id"
        key_word = "key_word"

        # relations
        provider_configs = "provider_configs"

    key_word = models.CharField(max_length=64)


class ProviderConfig(models.Model):
    seniority = models.ManyToManyField(Seniority, related_name="provider_configs")
    key_word = models.ManyToManyField(KeyWord, related_name="provider_configs")


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
