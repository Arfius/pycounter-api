import aioredis
import asyncio

class RedisDB:
    def __init__(self, url, key_threshold):
        self.url = url
        self.key_threshold = key_threshold

    async def init(self):
        self.redis = await aioredis.create_redis_pool(self.url)
        value = await self.status(self.key)
        if value is None:
            await self.__set_key_value(self.key, self.max_value)
        return int(value)
            
    async def __set_key_value(self, key, value):
         return await self.redis.set(key, value)

    async def descrese(self):
        value = int(await self.status(self.key))
        value -=1
        return await self.__set_key_value(self.key,value)

    async def status(self):
        return await self.redis.get(self.key)

    async def destroy(self, key):
        return await self.redis.delete(self.key)

    async def close(self):
        self.redis.close()
        await self.redis.wait_closed()