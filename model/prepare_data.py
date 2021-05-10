from config import settings

import pandas as pd
import numpy as np

from datetime import datetime
from hashlib import sha1
import os


def prepare():
    storage_path = os.path.join(settings.root, "files", "csv")
    files = [f for f in os.listdir(storage_path) if f[-4:] == ".csv"]

    data = []
    for csv in files:
        df = pd.read_csv(os.path.join(storage_path, csv))
        data.append(df)

    df: pd.DataFrame = pd.concat(data, axis=0, ignore_index=True)
    df.drop("Unnamed: 0", axis="columns", inplace=True)

    df.dropna(axis="index", how="all", inplace=True)

    df["hash"] = df.apply(
        lambda row: sha1(
            "|".join(
                [
                    str(row["name"]),
                    str(row["stars"]),
                    str(row["reviews"]),
                    str(row["occupancy"]),
                    str(row["search_place"]),
                    str(row["search_period"]),
                    str(row["search_people"]),
                ]
            ).encode()
        ).hexdigest(),
        axis=1,
    )

    df["price0"] = df.apply(
        lambda row: _find_base_price(df, row),
        axis=1,
    )

    print(df["hash"].value_counts())

    print(df[df["hash"] == "b7deeff7968b82b99fb04c99f284f96276cbb169"][["price", "incognito"]])

    df.drop(df[~df.incognito].index, inplace=True, axis="index")

    name = "./model/dataset/data_{}.csv".format(datetime.now().strftime("%m-%d_%H-%M-%S"))
    df.to_csv(name, index=False, sep=";")
    name = "./model/dataset/preview_latest.csv"
    df.to_csv(name, index=False, sep=",")


def _find_base_price(df: pd.DataFrame, row: pd.Series) -> int:
    same_hash = df[df["incognito"] & df["hash"] == row["hash"]]["price"]
    if len(same_hash):
        print("iiiihaaa")
        print(row["hash"])
        return max(same_hash - row["price"])
    return np.nan
