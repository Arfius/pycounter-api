# pycounter-api


### fast-api example
```
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
from pycounter_api.counterlimit import CounterLimit
import asyncio

app = FastAPI()
cl = CounterLimit("redis://localhost")
asyncio.create_task(cl.setup([("my-key-test",10)]))

async def check_key(key:str):
    res = await cl.decrease(key)
    if res == False:
        raise HTTPException(429, "Too Many Requests", headers={"Retry-After": "renew subscription"})
    return key


@app.get("/consume/{key}")
async def consume_key(key: dict = Depends(check_key)):
    res = await cl.decrease(key)
    return {"key": key, "alive":res}
```