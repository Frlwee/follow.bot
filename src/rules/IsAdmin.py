from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

from src.config import config


class IsAdminRule(ABCRule[Message]):
    async def check(self, message: Message) -> bool:
        return message.from_id in config.vk.bot.admins
