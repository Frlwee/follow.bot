from redis import asyncio as aioredis

from src.redis.utils import RedisUtils

redis: aioredis = aioredis.from_url("redis://redis")

redis_utils: RedisUtils = RedisUtils(redis)
