import redis.asyncio as redis


class TodoStore:
    """
    Stores and retrieves todo items from redis.
    """

    def __init__(self, redis: redis.Redis):
        self._redis = redis

    async def get_all(self) -> set:
        """
        Get all the fields and values stored in the
        """
        return await self._redis.smembers("todoIdsSet")

    async def get_item(self, id: str) -> dict:
        """
        Get the item with the given id.
        """
        return await self._redis.hgetall(id)

    async def add_item(self, item: dict) -> str:
        """
        Add the given item to the store.
        """
        id = await self._redis.incr("todoId")
        id = f"todo{id}"
        await self._redis.hmset(id, item)
        await self._redis.sadd("todoIdsSet", id)
        return id

    async def update_item(self, id: str, item: dict) -> None:
        """
        Update the item with the given id.
        """
        await self._redis.hmset(id, item)

    async def does_item_exist(self, id: str) -> bool:
        """
        Does the item with the given id exist?
        """
        return await self._redis.exists(id)

    async def delete_item(self, id: str) -> None:
        """
        Delete the item with the given id.
        """
        await self._redis.srem("todoIdsSet", id)
        await self._redis.delete(id)
