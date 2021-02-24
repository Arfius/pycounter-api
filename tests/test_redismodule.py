from couter_limit.redismodule import RedisDB
import pytest

    
@pytest.mark.asyncio
async def test_decrease_db():
    dbredis = RedisDB('redis://localhost')
    await dbredis.init(("mykey",100))
    res = await dbredis.decrease("mykey")
    await dbredis.close()
    assert res == 99

@pytest.mark.asyncio
async def test_status_db():
    dbredis = RedisDB('redis://localhost')
    await dbredis.init(("mykey",100))
    res = await dbredis.status("mykey")
    await dbredis.close()
    assert res == 99

@pytest.mark.asyncio
async def test_destroy_db():
    dbredis = RedisDB('redis://localhost')
    await dbredis.init(("mykey",100))
    await dbredis.destroy("mykey")
    res = await dbredis.status("mykey")
    await dbredis.close()
    assert res == None