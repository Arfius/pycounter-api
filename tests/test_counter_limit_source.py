from requests_counter.reqcounter import ReqCounter
import pytest

origin_allowed = ["origin_1", "origin_2"]


@pytest.mark.asyncio
async def test_check_origin_in():
    cl = ReqCounter('redis://localhost')
    await cl.setup_source(origin_allowed)
    res = await cl.check_source("origin_1")
    await cl.destroy_all()
    await cl.close()
    assert res is True


@pytest.mark.asyncio
async def test_check_origin_not_in():
    cl = ReqCounter('redis://localhost')
    await cl.setup_source(origin_allowed)
    res = await cl.check_source("origin_12")
    await cl.destroy_all()
    await cl.close()
    assert res is False
