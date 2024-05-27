import contextlib
import logging
import os
from time import sleep

from django.db.models import QuerySet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.remote.webelement import WebElement

from offers.models import JobOffer
from providers.models import Provider
from scrapping_process.models import ScrappingProcess
from scrapping_process.models import ScrappingStep
from scrapping_process.models import Selector

loggerr = logging.getLogger()

SLEEP_SECONDS = 3


class BrowserManager:
    WEBDRIVER = None
    ENGINE_PATH: str = ""
    BINARY_LOCATION: str = ""

    def __init__(self):
        self.browser = None
        if not self.WEBDRIVER or not self.ENGINE_PATH or not self.BINARY_LOCATION:
            raise NotImplementedError

    def __enter__(self):
        loggerr.info(f"Opening new browser - {self.browser}")
        return self.browser

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()
        loggerr.info(f"Browser closed - {self.browser}")


class FirefoxBrowserManager(BrowserManager):
    WEBDRIVER = webdriver.Firefox
    ENGINE_PATH = "~/geckodriver"
    BINARY_LOCATION = "/usr/bin/firefox-esr"

    def __init__(self):
        super().__init__()

        # Path to the manually downloaded geckodriver
        geckodriver_path = os.path.expanduser(self.ENGINE_PATH)
        service = Service(executable_path=geckodriver_path)
        options = Options()
        options.add_argument("--headless")
        options.binary_location = self.BINARY_LOCATION

        self.browser: webdriver.Firefox = self.WEBDRIVER(
            service=service, options=options
        )
        sleep(SLEEP_SECONDS)  # wait for new browser window to fully load
        loggerr.info(f"New browser initialized - {self.browser}")


class IndeedScrapperController:
    __SELECTORS_MAPPING = {
        Selector.SelectorType.selector_id: By.ID,
        Selector.SelectorType.selector_class: By.CLASS_NAME,
        Selector.SelectorType.selector_link: By.PARTIAL_LINK_TEXT,
        Selector.SelectorType.selector_css: By.CSS_SELECTOR,
        Selector.SelectorType.selector_none: None,
    }

    def get_results(self, provider_id: int):
        provider = (
            Provider.objects.filter(id=provider_id)
            .select_related(
                Provider.Keys.scrapping_process,
            )
            .prefetch_related(
                f"{Provider.Keys.scrapping_process}__{ScrappingProcess.Keys.steps}",
                f"{Provider.Keys.scrapping_process}__{ScrappingProcess.Keys.steps}__{ScrappingStep.Keys.selector}",
            )
            .first()
        )
        with FirefoxBrowserManager() as browser:
            browser.get(provider.base_link)
            self.__process_steps(browser=browser, provider=provider)

    def __process_steps(self, browser, provider: Provider):
        scrapping_process_steps: QuerySet[ScrappingStep] = (
            provider.scrapping_process.steps.all().order_by(ScrappingStep.Keys.order)
        )
        element: WebElement | None = None
        for step in scrapping_process_steps:
            found_jobs: list[WebElement] = []
            sleep(SLEEP_SECONDS)  # give page time to load
            selector: Selector = step.selector
            selector_type: Selector.SelectorType = selector.selector_type
            browser_selector: By | None = self.__SELECTORS_MAPPING.get(selector_type)

            if step.is_input_step and element:
                # send keys into search bar
                element.send_keys(step.key_words + Keys.RETURN)
                continue

            elif step.get_many_elements:
                # find multiple required elements
                found_jobs = browser.find_elements(
                    browser_selector, step.selector.selector_value
                )
            else:
                # find required element
                element: WebElement = browser.find_element(
                    browser_selector, step.selector.selector_value
                )
                if step.is_next_page_step:
                    # click the element even if it's obscured by something else
                    browser.execute_script("arguments[0].click();", element)

            if found_jobs:
                self.__save_jobs_from_page(found_jobs=found_jobs, provider=provider)

    def __save_jobs_from_page(self, found_jobs: list[WebElement], provider: Provider):
        job_offers: list[JobOffer] = []
        for job in found_jobs:
            link: str = self.__get_final_job_url(job)
            if not link:
                continue
            job_offers.append(
                JobOffer(
                    link=link,
                    short_description=job.text,
                    provider=provider,
                )
            )

        JobOffer.objects.bulk_create(job_offers, batch_size=20, ignore_conflicts=True)
        loggerr.info(f"Saved {len(job_offers)} job offers")

    @staticmethod
    def __get_final_job_url(job) -> str:
        """
        Open new browser, access the link (follow redirections etc), return final link.
        """

        with FirefoxBrowserManager() as new_browser, contextlib.suppress(Exception):
            link: str = job.get_attribute("href")
            new_browser.get(link)
            loggerr.info(f"Accessing the link: {link}")
            sleep(SLEEP_SECONDS)
            final_link: str = new_browser.current_url
            return final_link
        return ""
