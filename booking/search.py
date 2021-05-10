from config import settings
from config.types import TDriver
from config.enums import EBrowser

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

import time
import logging


logger = logging.getLogger(__name__)


def search(driver: TDriver, city: str, dates: list, guests: list) -> None:
    # place
    _hide_hover(driver)

    search_place = driver.find_elements_by_class_name("sb-searchbox__input")[0]
    search_place.click()
    search_place.send_keys(Keys.CONTROL + "a")
    search_place.send_keys(Keys.DELETE)
    time.sleep(0.25)
    search_place.send_keys(city)
    time.sleep(1.5)
    driver.find_elements_by_class_name("c-autocomplete__item")[0].click()

    # dates
    _hide_hover(driver)

    driver.execute_script("window.scrollBy(0, 150);")
    time.sleep(1.7)
    driver.find_element_by_css_selector('td[data-date="{}"]'.format(dates[0])).click()
    time.sleep(1.7)
    driver.find_element_by_css_selector('td[data-date="{}"]'.format(dates[1])).click()

    # guests and rooms
    _hide_hover(driver)

    driver.find_elements_by_class_name("xp__input-group")[3].click()

    adults = int(driver.find_elements_by_class_name("bui-stepper__display")[0].text)
    while adults != guests[0]:
        if adults < guests[0]:
            try:
                driver.find_element_by_css_selector('button[aria-label="Взрослых: увеличить количество"]').click()
            except NoSuchElementException:
                try:
                    driver.find_element_by_css_selector('button[aria-label="Increase number of Adults"]').click()
                except NoSuchElementException:
                    driver.find_elements_by_css_selector('button[aria-describedby="group_adults_desc"]')[1].click()
        if adults > guests[0]:
            try:
                driver.find_element_by_css_selector('button[aria-label="Взрослых: уменьшить количество"]').click()
            except NoSuchElementException:
                try:
                    driver.find_element_by_css_selector('button[aria-label="Decrease number of Adults"]').click()
                except NoSuchElementException:
                    driver.find_elements_by_css_selector('button[aria-describedby="group_adults_desc"]')[0].click()
        time.sleep(1.1)
        adults = int(driver.find_elements_by_class_name("bui-stepper__display")[0].text)

    children = int(driver.find_elements_by_class_name("bui-stepper__display")[1].text)
    while children != guests[1]:
        if children < guests[1]:
            try:
                driver.find_element_by_css_selector('button[aria-label="Детей: увеличить количество"]').click()
            except NoSuchElementException:
                driver.find_element_by_css_selector('button[aria-label="Increase number of Children"]').click()
        if children > guests[1]:
            try:
                driver.find_element_by_css_selector('button[aria-label="Детей: уменьшить количество"]').click()
            except NoSuchElementException:
                driver.find_element_by_css_selector('button[aria-label="Decrease number of Children"]').click()
        time.sleep(1.1)
        children = int(driver.find_elements_by_class_name("bui-stepper__display")[1].text)

    rooms = int(driver.find_elements_by_class_name("bui-stepper__display")[2].text)
    while rooms != guests[2]:
        if rooms < guests[2]:
            try:
                driver.find_element_by_css_selector('button[aria-label="Номера: увеличить количество"]').click()
            except NoSuchElementException:
                driver.find_element_by_css_selector('button[aria-label="Increase number of Rooms"]').click()
        if rooms > guests[2]:
            try:
                driver.find_element_by_css_selector('button[aria-label="Номера: уменьшить количество"]').click()
            except NoSuchElementException:
                driver.find_element_by_css_selector('button[aria-label="Decrease number of Rooms"]').click()
        time.sleep(1.1)
        rooms = int(driver.find_elements_by_class_name("bui-stepper__display")[2].text)

    driver.find_element_by_class_name("sb-searchbox__button").click()
    time.sleep(3.2)

    _hide_hover(driver)


def search_mobile(driver: TDriver, city: str, dates: list, guests: list) -> None:
    hover = driver.find_element_by_class_name("ot-sdk-row")
    driver.execute_script("arguments[0].style.display = 'none'", hover)

    search_place: WebElement = driver.find_element_by_id("input_destination_wrap")
    _scroll_into_view(driver, search_place)
    search_place.click()
    search_input: WebElement = driver.find_element_by_id("input_destination")
    time.sleep(0.12)
    search_input.send_keys(Keys.CONTROL + "a")
    search_input.send_keys(Keys.DELETE)
    time.sleep(0.25)
    search_input.send_keys(city)
    time.sleep(1.5)
    driver.find_elements_by_class_name("autocomplete_option")[0].click()
    time.sleep(0.17)

    driver.find_element_by_css_selector('td[data-date="{}"]'.format(dates[0])).click()
    time.sleep(1.7)
    driver.find_element_by_css_selector('td[data-date="{}"]'.format(dates[1])).click()
    driver.find_elements_by_class_name("searchbox_cross_product__overlay-close")[1].click()
    time.sleep(0.19)

    driver.find_element_by_css_selector("div[data-component='searchbox/groups/config']").click()
    time.sleep(0.17)

    adults = int(driver.find_elements_by_class_name("bui-stepper__display")[0].text)
    decrease = lambda: driver.find_elements_by_css_selector("button[data-bui-ref='input-stepper-subtract-button']")[
        0
    ].click()
    increase = lambda: driver.find_elements_by_css_selector("button[data-bui-ref='input-stepper-add-button']")[
        0
    ].click()

    while adults != guests[0]:
        if adults < guests[0]:
            increase()
            adults += 1
        if adults > guests[0]:
            decrease()
            adults -= 1
        time.sleep(0.11)
    driver.find_elements_by_class_name("searchbox_cross_product__overlay-close")[2].click()
    time.sleep(0.17)

    driver.find_element_by_id("submit_search").click()
    time.sleep(3.2)


def set_currency(driver: TDriver, currency: str) -> None:
    time.sleep(1.66)
    button = driver.find_element_by_css_selector('button[data-modal-header-async-type="currencyDesktop"]')
    button.click()

    time.sleep(1.42)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "bui-traveller-header__currency"))
    )

    rub = driver.find_element_by_partial_link_text(currency)
    if rub:
        href = rub.get_attribute("href")
        driver.get(href)

        logger.info("set currency to RUB")

        settings.currency = "RUB"
    else:
        settings.currency = button.text.strip()
    time.sleep(1.77)


def set_currency_mobile(driver: TDriver, currency: str) -> None:
    hover = driver.find_element_by_class_name("ot-sdk-row")
    driver.execute_script("arguments[0].style.display = 'none'", hover)

    time.sleep(1.66)
    hamburger = driver.find_element_by_css_selector('button[data-bui-component="Modal.HeaderAsync"]')
    hamburger.click()
    time.sleep(0.87)

    currency_selection: WebElement = driver.find_element_by_class_name(
        "bui-traveller-header__mobile-content"
    ).find_element_by_tag_name("ul")
    currency_selection.find_elements_by_tag_name("li")[0].click()

    time.sleep(0.42)
    rub = driver.find_element_by_partial_link_text(currency)
    if rub:
        href = rub.get_attribute("href")
        driver.get(href)

        logger.info("set currency to RUB")

        settings.currency = "RUB"
    else:
        settings.currency = currency_selection.find_element_by_class_name("bui-inline-container__start").text.strip()
    time.sleep(1.77)


def _scroll_into_view(driver: TDriver, element: WebElement) -> None:
    driver.execute_script("arguments[0].scrollIntoView();", element)


def _scroll_by(driver: TDriver, px: int) -> None:
    driver.execute_script("window.scrollBy(0, {});".format(px))


def _hide_hover(driver: TDriver) -> None:
    hover = driver.find_element_by_id("onetrust-banner-sdk")
    driver.execute_script("arguments[0].style.display = 'none'", hover)
