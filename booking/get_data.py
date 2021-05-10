from config import settings
from config.enums import EBrowser
from config.types import TDriver

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import logging
import time
import re
import sys


logger = logging.getLogger(__name__)


def scrape_card(card: WebElement) -> dict:
    name = card.find_element_by_class_name("sr-hotel__name").text
    try:
        rating = float(card.find_element_by_class_name("bui-review-score__badge").text.replace(",", "."))
    except:
        rating = None
    try:
        reviews = int(card.find_element_by_class_name("bui-review-score__text").text.split()[0])
    except:
        reviews = None
    try:
        stars = int(card.find_element_by_class_name("bui-rating").get_attribute("aria-label")[0])
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
    prices = [
        int(n) for n in re.findall(r"\d+", card.find_elements_by_class_name("bui-u-sr-only")[1].text.replace(" ", ""))
    ]
    price = prices[-1]
    discount = len(prices) > 1
    previous_price = prices[0] if discount else None
    return dict(
        name=name,
        rating=rating,
        reviews=reviews,
        stars=stars,
        occupancy=occupancy,
        persuasion=persuasion,
        persuasion_left=persuasion_left,
        promo=promo,
        price=price,
        discount=discount,
        previous_price=previous_price,
    )


def next_page(driver: TDriver) -> None:
    button = driver.find_element_by_css_selector('svg[class="bk-icon -iconset-navarrow_right bui-pagination__icon"]')
    driver.execute_script("arguments[0].scrollIntoView();", button)
    time.sleep(1.5)
    if settings.browser == EBrowser.CHROME:
        driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(0.8)
    button.click()
    time.sleep(4.2)

    hover = driver.find_element_by_id("onetrust-banner-sdk")
    driver.execute_script("arguments[0].style.display = 'none'", hover)


def run_scrap(driver: TDriver, pages=4) -> list:
    logger.info("Scraping page: {}".format(1))

    hover = driver.find_element_by_id("onetrust-banner-sdk")
    driver.execute_script("arguments[0].style.display = 'none'", hover)

    overlay = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CLASS_NAME, "map_full_overlay__close"))
    )
    try:
        overlay.click()
    except:
        pass

    cards = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "sr_item_default")))
    time.sleep(0.7)

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
        cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "sr_item_default"))
        )
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
