from vkbottle import BaseMiddleware
from vkbottle.bot import Message


class UserInfoMiddleware(BaseMiddleware[Message]):
    async def pre(self):
        user = (await self.event.ctx_api.users.get(self.event.from_id))[0]

        self.send({"user_info": user})
