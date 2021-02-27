from requests_counter._redismodule import RedisDB
import pytest


@pytest.mark.asyncio
async def test_create_entry_db():
    dbredis = RedisDB('redis://localhost')
    await dbredis.setup()
    await dbredis.create_entry("mykey", 100)
    res = await dbredis.status("mykey")
    await dbredis.close()
    assert int(res) == 100


@pytest.mark.asyncio
async def test_decrease_db():
    dbredis = RedisDB('redis://localhost')
    await dbredis.setup()
    res = await dbredis.decrease("mykey")
    await dbredis.close()
    assert int(res) == 99


@pytest.mark.asyncio
async def test_destroy_db():
    dbredis = RedisDB('redis://localhost')
    await dbredis.setup()
    await dbredis.destroy("mykey")
    res1 = await dbredis.status("mykey")
    await dbredis.close()
    assert res1 is None
