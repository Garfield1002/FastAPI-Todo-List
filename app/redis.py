from redis import Redis
import redis.asyncio as redis


async def init_redis_pool() -> redis.Redis:
    redis_c: Redis = await redis.Redis(host="redis", port=6379, db=0)

    # Does the redis server exist?
    if not (await redis_c.exists("todoId")):
        await redis_c.set("todoId", "0")

    return redis_c
