import logging
import os
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

LOGGING_CONFIG = {
    'version': 1,
    'disabled_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)-s - %(asctime)s - %(module)-s : %(message)s'
        },
        'standard': {
            'format': '%(levelname)-s - %(module)-s : %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'bot': {
            'level': 'INFO',
            'propagate': False,
            'handlers': ['console']
        }
    }
}

dictConfig(LOGGING_CONFIG)