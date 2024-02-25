import gettext

import loguru
from vkbottle import run_multibot, API

from src.definitions import LOCALES_DOMAIN, LOCALES_DIR
from src.utils.loop import loop_wrapper, loop
from src.middlewares import middlewares
from src.database import init_database
from src.settings import settings
from src.handlers import labelers
from src.bot import Bot


bot = Bot(loop_wrapper=loop_wrapper)
bot.labeler.message_view.replace_mention = True

for labeler in labelers:
    bot.labeler.load(labeler)

for middleware in middlewares:
    bot.labeler.message_view.register_middleware(middleware)


def __main__():
    loop_wrapper.add_task(init_database())
    loop_wrapper.add_task(
        run_multibot(
            bot,
            apis=([API(token) for token in settings.VK_TOKENS])
        )
    )

    loop_wrapper.run_forever(loop=loop)
