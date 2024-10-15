import os
import logging
from logging.config import dictConfig
import pathlib

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

BASE_DIR = pathlib.Path(__file__).parent

CMDS_DIR = BASE_DIR / "src/cmds"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(levelname)s : %(message)s - %(asctime)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard"
        }
    },
    "loggers": {
        "bot": {
            "level": "INFO",
            "propagate": False,
            "handlers": ['console']
        }
    },
}

dictConfig(LOGGING_CONFIG)
