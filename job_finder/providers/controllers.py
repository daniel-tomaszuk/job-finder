from time import sleep

from django.db.models import QuerySet
from scrapping_process.models import ScrappingProcess
from scrapping_process.models import ScrappingStep
from scrapping_process.models import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from offers.models import JobOffer
from providers.models import Provider


class BrowserManager:
    BROWSER = webdriver.Firefox

    def __init__(self):
        self.browser = self.BROWSER()

    def __enter__(self):
        return self.browser

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()


class IndeedScrapperController:
    __SELECTORS_MAPPING = {
        Selector.SelectorType.selector_id: By.ID,
        Selector.SelectorType.selector_class: By.CLASS_NAME,
        Selector.SelectorType.selector_link: By.PARTIAL_LINK_TEXT,
        Selector.SelectorType.selector_css: By.CSS_SELECTOR,
        Selector.SelectorType.selector_none: None,
    }

    def get_results(self):
        provider: Provider = (
            Provider.objects.select_related(
                Provider.Keys.scrapping_process,
            )
            .prefetch_related(
                f"{Provider.Keys.scrapping_process}__{ScrappingProcess.Keys.steps}",
                f"{Provider.Keys.scrapping_process}__{ScrappingProcess.Keys.steps}__{ScrappingStep.Keys.selector}",
            )
            .first()
        )

        with BrowserManager() as browser:
            browser.get(provider.base_link)

            self.__process_steps(browser=browser, provider=provider)

    def __process_steps(self, browser, provider: Provider):
        scrapping_process_steps: QuerySet[ScrappingStep] = (
            provider.scrapping_process.steps.all().order_by(ScrappingStep.Keys.order)
        )
        element = None
        found_jobs = []
        for step in scrapping_process_steps:
            sleep(1)  # give page time to load
            selector: Selector = step.selector
            selector_type: Selector.SelectorType = selector.selector_type
            browser_selector: By | None = self.__SELECTORS_MAPPING.get(selector_type)

            if step.is_input_step and element:
                element.send_keys(step.key_words + Keys.RETURN)
                continue

            if step.get_many_elements:
                found_jobs = browser.find_elements(
                    browser_selector, step.selector.selector_value
                )
            else:
                element = browser.find_element(
                    browser_selector, step.selector.selector_value
                )

        job_offers: list[JobOffer] = []
        for job in found_jobs:
            job_offers.append(
                JobOffer(
                    link=job.get_attribute("href"),
                    short_description=job.text,
                    provider=provider,
                )
            )

        JobOffer.objects.bulk_create(job_offers, batch_size=20)
