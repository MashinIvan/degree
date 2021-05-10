from .config import set_default_config, Settings
import logging
import sys


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs.log", mode="w"),
    ],
)

settings: Settings = set_default_config()
