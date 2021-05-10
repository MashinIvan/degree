from config import settings
from config.enums import EBrowser
from config.types import TDriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

import logging
import time
import re
import sys


logger = logging.getLogger(__name__)


def scrape_card(card: WebElement) -> dict:
    name = card.find_element_by_class_name("sr-card__name").text
    try:
        rating = float(card.find_element_by_class_name("bui-review-score__badge").text.replace(",", "."))
    except:
        rating = None
    try:
        reviews = int(card.find_element_by_class_name("bui-review-score__text").text.split()[0])
    except:
        reviews = None
    try:
        stars = int(card.find_element_by_class_name("bui-rating").get_attribute("aria-label").split()[0])
    except:
        stars = None
    try:
        occupancy = [int(s) for s in card.find_elements_by_class_name("bui-u-sr-only")[0].text.split() if s.isdigit()][
            -1
        ]
    except:
        occupancy = None
    try:
        persuasion = bool(card.find_element_by_class_name("js_sr_persuation_msg").text)
    except:
        persuasion = None
    if persuasion:
        persuasion_left = [
            int(s) for s in card.find_element_by_class_name("js_sr_persuation_msg").text.split() if s.isdigit()
        ][-1]
    else:
        persuasion_left = None
    promo = bool(card.find_elements_by_class_name("ranking_vb_tag"))
    price = card.find_element_by_class_name("bui-price-display__value").text
    price_float = _get_price_float(price)

    return dict(
        name=name,
        rating=rating,
        reviews=reviews,
        stars=stars,
        occupancy=occupancy,
        persuasion=persuasion,
        persuasion_left=persuasion_left,
        promo=promo,
        price=price_float,
        discount=None,
        previous_price=None,
    )


def next_page(driver: TDriver) -> None:
    button = driver.find_element_by_class_name("js-pagination-next-link")
    _scroll_into_view(driver, button)

    button.click()
    time.sleep(4.2)

    hover = driver.find_element_by_class_name("ot-sdk-row")
    driver.execute_script("arguments[0].style.display = 'none'", hover)


def run_scrap(driver: TDriver, pages=4) -> list:
    logger.info("Scraping page: {}".format(1))

    hover = driver.find_element_by_class_name("ot-sdk-row")
    driver.execute_script("arguments[0].style.display = 'none'", hover)

    cards_list: WebElement = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sr-card-list"))
    )
    time.sleep(0.7)
    cards = cards_list.find_elements_by_tag_name("li")

    errors = 0
    data = []
    for card in cards:
        try:
            data.append(scrape_card(card))
        except Exception as e:
            errors += 1
            continue

    logger.info("total cards: {}".format(len(data)))
    logger.warning("total errors: {}".format(errors))

    for i in range(pages - 1):
        logger.info("Scraping page: {}".format(i + 2))

        next_page(driver)
        cards_list: WebElement = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sr-card-list"))
        )
        time.sleep(0.7)
        cards = cards_list.find_elements_by_tag_name("li")

        time.sleep(0.7)
        for card in cards:
            try:
                data.append(scrape_card(card))
            except Exception as e:
                errors += 1
                continue

        logger.info("total cards: {}".format(len(data)))
        logger.warning("total errors: {}".format(errors))

    logger.info("Finished, saving...")

    return data


def _get_price_float(value: str) -> float:
    value = re.sub(r"\D", "", value)
    return float(value)


def _scroll_into_view(driver: TDriver, element: WebElement) -> None:
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(0.07)
