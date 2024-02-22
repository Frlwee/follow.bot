import asyncio

from sys import platform

from src.config import logger

from vkbottle.tools.dev.loop_wrapper import LoopWrapper

if platform == "linux" or platform == "linux2":
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    logger.info("uvloop \"EventLoopPolicy\" configured")

loop = asyncio.get_event_loop()
loop_wrapper = LoopWrapper()

__all__ = (
    "loop",
    "loop_wrapper",
)