from tortoise import Tortoise


from src.config import logger
from src.database.config import db_config


async def init_database() -> None:
    logger.info('Run init database...')

    await Tortoise.init(config=db_config)
    await Tortoise.generate_schemas()
