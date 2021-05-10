from config import settings
import pandas as pd
from datetime import datetime


def save_data(data: list) -> None:
    for item in data:
        item["system"] = settings.system
        item["browser"] = settings.browser.value
        item["cookies1"] = settings.cookies1
        item["cookies3"] = settings.cookies3
        item["country"] = settings.country
        item["incognito"] = settings.incognito
        item["user_agent"] = settings.user_agent
        item["search_place"] = settings.search_place.value
        item["search_period"] = settings.search_period
        item["search_people"] = settings.search_people
        item["currency"] = settings.currency

    df = pd.DataFrame(data)
    name = "./files/csv/data_{}.csv".format(datetime.now().strftime("%m-%d_%H-%M-%S"))
    df.to_csv(name)
