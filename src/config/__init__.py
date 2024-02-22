import sys
import json

from loguru import logger

from src.config.model import ConfigModel


with open("properties.json", mode="r", encoding="UTF-8") as file:
    raw_config = json.load(file)
    config: ConfigModel = ConfigModel(**raw_config)


LOG_FORMAT = (
    "<magenta>AF CM</magenta> | "
    "<level>{level: <8}</level> | "
    "<italic><green>{time:YYYY-MM-DD HH:mm:ss}</green></italic> | "
    "{name}:{function}:{line} > <level>{message}</level>"
)


logger.remove()
logger.add(sys.stderr, format=LOG_FORMAT, level="INFO", enqueue=True, colorize=True)


__all__ = (
    config,
    logger,
)
