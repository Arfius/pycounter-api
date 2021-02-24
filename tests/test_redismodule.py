from couter_limit.redismodule import RedisDB
import pytest


@pytest.mark.asyncio
async def test_init_db():
    dbredis = RedisDB('redis://localhost',"mykey",100)
    res = await dbredis.init()
    await dbredis.close()
    
@pytest.mark.asyncio
async def test_decrease_db():
    dbredis = RedisDB('redis://localhost',"mykey",100)
    await dbredis.init()
    res = await dbredis.descrese("mykey")
    await dbredis.close()
    assert res == True


@pytest.mark.asyncio
async def test_status_db():
    dbredis = RedisDB('redis://localhost',"mykey",100)
    await dbredis.init()
    res = await dbredis.status("mykey")
    print("res-----------",res)
    await dbredis.close()