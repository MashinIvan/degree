from config import settings
from config.types import TDriver
from config.enums import ECountry

from helpers.sleep import sleeper

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

import logging
import time


logger = logging.getLogger(__name__)


def pre_scrap(driver: TDriver) -> None:
    if settings.rivals:
        # try:
        #     search_expedia(driver)
        # except Exception as e:
        #     logger.warning(e)

        try:
            search_trip(driver)
        except Exception as e:
            logger.warning(e)

    if settings.incognito:
        driver.delete_all_cookies()


def search_expedia(driver: TDriver) -> None:
    driver.get("https://www.expedia.com/")
    sleeper.medium()

    search: WebElement = WebDriverWait(driver, 7).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button[data-stid='location-field-destination-menu-trigger']")
        )
    )
    sleeper.short()
    search.click()
    sleeper.short()

    search_input: WebElement = driver.find_element_by_id("location-field-destination")
    _fill_search_place_input(driver, search_input)

    results: WebElement = driver.find_element_by_css_selector("ul[data-stid='location-field-destination-results']")
    results.find_elements_by_tag_name("li")[0].click()
    sleeper.short()

    submit: WebElement = driver.find_element_by_css_selector("button[type='submit']").click()


def search_trip(driver: TDriver) -> None:
    country = settings.country
    if settings.country == ECountry.ENGLAND:
        country = "com"

    driver.get("https://www.tripadvisor.{}/".format(settings.country))
    sleeper.short()

    _hide_hover_trip(driver)

    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']")))
    sleeper.short()

    driver.find_element_by_css_selector("div[data-test-attribute='typeahead-SINGLE_SEARCH_HERO']").click()
    sleeper.short()

    search_input: WebElement = driver.find_elements_by_css_selector("input[type='search']")[1]
    _fill_search_place_input(driver, search_input)

    results: WebElement = driver.find_element_by_id("typeahead_results")
    results.find_elements_by_tag_name("a")[0].click()


def _fill_search_place_input(driver: TDriver, inp: WebElement) -> None:
    inp.click()
    inp.send_keys(Keys.CONTROL + "a")
    inp.send_keys(Keys.DELETE)
    sleeper.short()
    inp.send_keys(settings.search_place.value)
    sleeper.medium()


def _hide_hover_trip(driver: TDriver) -> None:
    accept = driver.find_element_by_id("_evidon-accept-button")
    accept.click()
