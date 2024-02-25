import asyncio

from sys import platform

from vkbottle.tools.loop_wrapper import LoopWrapper

if platform == "linux" or platform == "linux2":
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


loop = asyncio.get_event_loop()
loop_wrapper = LoopWrapper()
