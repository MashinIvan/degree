from config.enums import ERivals


def visit_rivals(driver):
    for item in ERivals:
        url = item.value
        driver.get(url)

        if item == ERivals.TRIPADVISOR:
            search_tripadvisor(driver)

        elif item == ERivals.HOTELS:
            search_hotels(driver)

        elif item == ERivals.EXPEDIA:
            search_expedia(driver)


def search_tripadvisor(driver):
    ...


def search_hotels(driver):
    ...


def search_expedia(driver):
    ...
