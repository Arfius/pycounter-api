import aioredis


class RedisDB:
    def __init__(self, url):
        self.url = url
        self.redis = None

    async def __create_entry(self, key: str, max_value: int) -> None:
        if await self.redis.exists(key) == 0:
            await self.redis.set(key, max_value)

    async def __setup(self):
        if self.redis is None : 
                    self.redis = await aioredis.create_redis_pool(self.url)

    async def init_api_key(self, tuple_key_threshold: tuple) -> None:
        self. __setup()
        [await self.__create_entry(key_value[0], key_value[1]) for key_value in tuple_key_threshold]

    async def init_origin(self, origin_internal_key, list_of_origin:list) -> None :
        self. __setup()
        await self.__create_entry(origin_internal_key, list_of_origin)

    async def set_key_value(self, key: str, value: int) -> int:
        if await self.redis.exists(key) != 0:
            await self.redis.set(key, value)
            return await self.status(key)
        else:
            None

    async def decrease(self, key: str) -> int:
        await self.redis.decr(key)
        return await self.status(key)

    async def status(self, key: str) -> int:
        res = await self.redis.get(key)
        return int(res) if res is not None else res

    async def destroy(self, key: str) -> bool:
        if await self.redis.exists(key) != 0:
            await self.redis.delete(key)
            return True
        else:
            return False

    async def close(self) -> None:
        self.redis.close()
        await self.redis.wait_closed()

    async def all_keys(self) -> list:
        return await self.redis.keys("*")
