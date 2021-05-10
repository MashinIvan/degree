from config import settings
from config.enums import EBrowser, EUserAgentChrome, EUserAgentFirefox, EOS
from config.types import TDriver

from selenium import webdriver

from typing import Union
import logging
import os


logger = logging.getLogger(__name__)


def get_browser() -> TDriver:
    if settings.browser == EBrowser.CHROME:
        if settings.system == EOS.UBUNTU:
            driver_name = "chromedriver"
        else:
            driver_name = "chromedriver.exe"
        path = os.path.join(settings.root, "files", "browsers", driver_name)

        options = webdriver.ChromeOptions()
        if settings.user_agent == EUserAgentChrome.MOBILE:
            options.add_argument("window-size=375,812")
        else:
            options.add_argument("window-size=1280,800")

        options.add_argument("user-agent={}".format(settings.user_agent.value))

        if settings.incognito:
            options.add_argument("--incognito")
        caps = options.to_capabilities()

        if not settings.incognito:  # and not (settings.cookies1 or settings.cookies3):
            options.add_argument("user-data-dir={}".format(settings.cookies_path))

        # options.headless = True

        driver = webdriver.Chrome(
            executable_path=path,
            chrome_options=options,
            desired_capabilities=caps,
        )

    else:
        if settings.system == EOS.UBUNTU:
            driver_name = "geckodriver"
        else:
            driver_name = "geckodriver.exe"

        path = os.path.join(settings.root, "files", "browsers", driver_name)

        options = webdriver.FirefoxOptions()
        if settings.user_agent == EUserAgentFirefox.MOBILE:
            options.add_argument("--width=375")
            options.add_argument("--height=812")
        else:
            options.add_argument("--width=1280")
            options.add_argument("--height=800")

        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", settings.user_agent.value)

        if settings.incognito:
            profile.set_preference("browser.privatebrowsing.autostart", True)
            options.add_argument("-private")

        # options.headless = True

        driver = webdriver.Firefox(
            executable_path=path,
            firefox_options=options,
            firefox_profile=profile,
        )

    driver.delete_all_cookies()

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    logger.info("Driver set")
    return driver
