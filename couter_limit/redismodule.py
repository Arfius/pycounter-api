import aioredis
import asyncio

class RedisDB:
    def __init__(self, url):
        self.url = url

    async def __create_entry(self, key, max_value):
        if await self.redis.exists(key) == 0:
            await self.__set_key_value(key, int(max_value))

    async def init(self, tuple_key_threshold):
        self.redis = await aioredis.create_redis_pool(self.url)
        # [await self.__create_entry( key_value[0], key_value[1]) for key_value in tuple_key_threshold]
        await self.__create_entry(tuple_key_threshold[0], tuple_key_threshold[1])
    
    async def __set_key_value(self, key, value):
         return await self.redis.set(key, value)

    async def decrease(self, key):
        await self.redis.decr(key)
        return await self.status(key)

    async def status(self, key):
        res = await self.redis.get(key)
        return int(res) if res is not None else res

    async def destroy(self, key):
        return await self.redis.delete(key)

    async def close(self):
        self.redis.close()
        await self.redis.wait_closed()