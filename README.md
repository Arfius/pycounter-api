# requests-counter


### fast-api example

```
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
from requests_counter.reqcounter import ReqCounter
import asyncio

app = FastAPI()
cl = ReqCounter("redis://localhost")
asyncio.create_task(cl.setup([("my-key-test",10)]))

async def check_key(key:str):
    res = await cl.decrease(key)
    if res == False:
        raise HTTPException(429, "Too Many Requests", headers={"Retry-After": "renew subscription"})
    return key

@app.get("/consume/{key}")
async def consume_key(key: dict = Depends(check_key)):
    return {"job": "done"}
```