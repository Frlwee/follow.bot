import json

from pydantic import BaseModel


class RedisUtils:
    def __init__(self, redis):
        self.redis = redis

    async def get_as(self, key: str, model: type[BaseModel]):
        if value := (await self.redis.get(key)):
            return model.parse_obj(json.loads(value))
        return None
