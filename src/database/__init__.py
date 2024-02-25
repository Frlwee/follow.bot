from tortoise import Tortoise

from src.database.config import config


async def init_database():
    await Tortoise.init(config=config)
    await Tortoise.generate_schemas()
