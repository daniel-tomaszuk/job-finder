import json
from typing import Callable

from providers.models import Provider
from scrapping_process.data_migrations.fixtures.key_words import KEY_WORD_FIXTURES
from scrapping_process.data_migrations.fixtures.providers import PROVIDER_FIXTURES
from scrapping_process.data_migrations.fixtures.scrapping_process import SCRAPPING_PROCESS_FIXTURES
from scrapping_process.data_migrations.fixtures.scrapping_steps import SCRAPPING_STEP_FIXTURES
from scrapping_process.data_migrations.fixtures.selectors import SELECTOR_FIXTURES
from scrapping_process.models import KeyWord
from scrapping_process.models import ScrappingProcess
from scrapping_process.models import ScrappingStep
from scrapping_process.models import Selector


class DataMigrationBase:

    @classmethod
    def apply(cls, *args, **kwargs) -> str:
        raise NotImplementedError

    @classmethod
    def downgrade(cls, *args, **kwargs) -> str:
        raise NotImplementedError


class LoadInitialDataMigration:
    FIXTURES = [
        (SELECTOR_FIXTURES, Selector),
        (KEY_WORD_FIXTURES, KeyWord),
        (SCRAPPING_PROCESS_FIXTURES, ScrappingProcess),
        (PROVIDER_FIXTURES, Provider),
        (SCRAPPING_STEP_FIXTURES, ScrappingStep),
    ]

    @classmethod
    def apply(cls, *args, **kwargs):
        for fixture, model in cls.FIXTURES:
            data: list[dict] = json.loads(fixture)
            cls.__save_data(data, model)
        return f"{cls} data migrations applied!"

    @classmethod
    def __save_data(cls, data: list[dict], model: Callable):
        for data_row in data:
            instance_kwargs = {key: value for key, value in data_row["fields"].items()}

            # if object already exists, do not create it
            model.objects.get_or_create(
                id=data_row["pk"],
                defaults=instance_kwargs,
            )

    @classmethod
    def downgrade(cls, *args, **kwargs) -> str:
        return f"{cls} downgrade not implemented!"
