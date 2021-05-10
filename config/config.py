from .enums import EBrowser, ECountry, EUserAgentChrome, EUserAgentFirefox, ESearchPlace, EOS
from pydantic import BaseSettings, Field
import logging
import typing
import random
import os


logger = logging.getLogger("config")


class Settings(BaseSettings):
    browser: EBrowser
    incognito: bool
    user_agent: typing.Union[EUserAgentChrome, EUserAgentFirefox]
    cookies1: bool
    cookies3: bool

    search_place: ESearchPlace
    search_period: int
    search_people: int

    root: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    system: EOS = Field(description="set in .env")
    cookies_path: str = Field(description="set in .env")
    country: ECountry = Field(description="set in .env")

    currency: str = Field(None, description="is set while scraping")
    is_mobile: bool = Field(None, description="is set while scraping")
    rivals: bool = Field(None, description="is set while scraping")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def set_default_config():
    browser = random.choice(list(EBrowser))
    logger.info("Chosen browser: {}".format(browser))

    incognito = random.randint(0, 1)
    logger.info("Chosen incognito: {}".format(incognito))

    if browser == EBrowser.CHROME:
        user_agent = random.choice(list(EUserAgentChrome))
    else:
        user_agent = random.choice(list(EUserAgentFirefox))
    logger.info("Chosen user_agent: {}".format(user_agent))

    search_place = random.choice(list(ESearchPlace))
    logger.info("Chosen search_place: {}".format(search_place))

    search_period = random.randint(5, 12)
    logger.info("Chosen search_period: {}".format(search_period))

    search_people = random.randint(1, 2)
    logger.info("Chosen search_people: {}".format(search_people))

    if not incognito:
        cookies1 = random.randint(0, 1)
        logger.info("Chosen cookies1: {}".format(cookies1))

        cookies3 = random.randint(0, 1)
        logger.info("Chosen cookies3: {}".format(cookies3))

        rivals = random.randint(0, 1)
        logger.info("Chosen rivals: {}".format(rivals))
    else:
        cookies1 = False
        logger.info("Chosen cookies1: {}".format(cookies1))

        cookies3 = False
        logger.info("Chosen cookies3: {}".format(cookies3))

        rivals = False
        logger.info("Chosen rivals: {}".format(rivals))

    ret = Settings(
        browser=browser,
        incognito=incognito,
        user_agent=user_agent,
        cookies1=cookies1,
        cookies3=cookies3,
        search_place=search_place,
        search_period=search_period,
        search_people=search_people,
        rivals=rivals,
    )

    if user_agent == EUserAgentFirefox.MOBILE or user_agent == EUserAgentChrome.MOBILE:
        ret.is_mobile = True
    else:
        ret.is_mobile = False

    logger.info("config set")
    return ret


def update_settings(config: Settings) -> None:
    new_config = set_default_config()

    config.browser = new_config.browser
    config.incognito = new_config.incognito
    config.user_agent = new_config.user_agent
    config.cookies1 = new_config.cookies1
    config.cookies3 = new_config.cookies3
    config.search_place = new_config.search_place
    config.search_period = new_config.search_period
    config.search_people = new_config.search_people
    config.rivals = new_config.rivals

    if config.user_agent == EUserAgentFirefox.MOBILE or config.user_agent == EUserAgentChrome.MOBILE:
        config.is_mobile = True
    else:
        config.is_mobile = False
