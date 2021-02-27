from requests_counter._redismodule import RedisDB


class ReqCounter:
    def __init__(self, url):
        self.rds = RedisDB(url)
        self.__origin_internal_key = "rc_list_origin"

    async def setup_api_key(self, values):
        await self.rds.init_api_key(values)
    
    async def setup_origin(self, values):
        await self.rds.init_origin(self.__origin_internal_key, values)

    async def check_origin(self, origin):
        return origin in await self.status(self.__origin_internal_key)

    async def decrease(self, key):
        value = await self.rds.decrease(key)
        return True if value > 0 else False

    async def reset(self, key, value):
        return await self.rds.set_key_value(key, value)

    async def destroy(self, key):
        return await self.rds.destroy(key)

    async def destroy_all(self):
        return [await self.rds.destroy(key) for key in await self.rds.all_keys()]

    async def status(self):
        return [{"key": key, "value": await self.rds.status(key)} for key in await self.rds.all_keys()]

    async def close(self):
        return await self.rds.close()
