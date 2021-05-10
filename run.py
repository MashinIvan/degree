from config import settings, Settings, set_default_config
from config.config import update_settings
from config.enums import EUserAgentChrome, EUserAgentFirefox
from config.get_browser import get_browser
from config.pre_scrap import pre_scrap

from booking.open import open_booking
from booking.get_data import run_scrap
from booking.get_data_mobile import run_scrap as run_scrap_mobile

from save_data import save_data
from model.prepare_data import prepare

import logging
import time
import fire


logger = logging.getLogger(__name__)


class Runner:
    def main(self) -> None:
        driver = get_browser()
        time.sleep(1.1)

        pre_scrap(driver)

        open_booking(driver)

        if settings.is_mobile:
            data = run_scrap_mobile(driver, pages=6)
        else:
            data = run_scrap(driver, pages=6)

        save_data(data)

        driver.close()

    def main_loop(self, iterations: int) -> None:
        for i in range(iterations):
            logger.info(
                """
            #-----------------------------------------------#
            STARTING ITERATION:  {}
            """.format(
                    i + 1
                )
            )
            try:
                self.main()
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(e)
                continue
            finally:
                update_settings(settings)

    def prepare_data(self) -> None:
        prepare()


if __name__ == "__main__":
    fire.Fire(Runner)
