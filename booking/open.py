from config import settings
from config.types import TDriver
from selenium import webdriver

import time
from booking.search import set_currency, set_currency_mobile, search, search_mobile


def open_booking(driver: TDriver) -> None:
    driver.get("https://booking.{}".format(settings.country))
    time.sleep(4.2)

    if settings.is_mobile:
        set_currency_mobile(driver, "RUB")

        search_mobile(
            driver,
            settings.search_place.value,
            ["2021-05-03", "2021-05-{:02d}".format(3 + settings.search_period)],
            [settings.search_people, 0, 1],
        )
    else:
        set_currency(driver, "RUB")

        search(
            driver,
            settings.search_place.value,
            ["2021-05-03", "2021-05-{:02d}".format(3 + settings.search_period)],
            [settings.search_people, 0, 1],
        )
