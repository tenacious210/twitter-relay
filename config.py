import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN_ENV')

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_Loggers": False,
    "formatters" :{
        "verbose":{
            'format': "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard":{
            'format': "%(levelname)-10s - %(name)-15s : %(message)s"
        }
    },
    "handlers":{
        "console":{
            'level': "DEBUG",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "console2":{
            'level': "WARNING",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "file":{
            'level': "INFO",
            'class': "logging.FileHandler",
            'filename': "logs/infos.log",
            'mode': "w",
            'formatter': "verbose"
        }
    },
    "loggers":{
        "client":{
            'handlers': ["console"],
            'level': "INFO",
            'propagate': False
        },
        "discord":{
            'handlers': ["console2", "file"],
            'level': "INFO",
            'propagate': False
        }
    }
}
dictConfig(LOGGING_CONFIG)