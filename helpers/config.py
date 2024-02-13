import os
import json
import logging
import logging.config
from dotenv import load_dotenv


load_dotenv()

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_Loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard": {"format": "%(levelname)-10s - %(name)-15s : %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "logs/infos.log",
            "mode": "w",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "client": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "discord": {
            "handlers": ["console2", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)

logger.info("Loading Discord token")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN_ENV")


def read_channels() -> list[int]:
    with open("config/channels.json", "r") as channels_json:
        channels = json.load(channels_json)
    return channels


def write_channels(channels: list[int]) -> None:
    with open("config/channels.json", "w") as channels_json:
        channels = json.dump(channels, channels_json)
