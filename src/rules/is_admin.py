from vkbottle.bot import Message
from vkbottle.dispatch.rules import ABCRule

from src.settings import settings


class IsAdminRule(ABCRule[Message]):
    async def check(self, message: Message) -> bool:
        return message.from_id in settings.ADMINS
