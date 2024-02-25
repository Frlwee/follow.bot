from vkbottle import BaseMiddleware
from vkbottle.bot import Message
from vkbottle_types.codegen.objects import UsersUserFull

from src.redis import redis, redis_utils


class UserInformationMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        key = f"user:{self.event.from_id}"
        user = await redis_utils.get_as(key, UsersUserFull)

        if not user:
            user = await self.event.get_user()
            await redis.set(key, user.json(), nx=True)
            await redis.expire(key, 60 * 5)

        self.send({"user_information": user})
