from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
from app.counterlimit import CounterLimit
import asyncio

app = FastAPI()
cl = CounterLimit("redis://localhost")
asyncio.create_task(cl.setup([("my-key-cardiff",10)]))

async def check_key(key:str):
    res = await cl.decrease(key)
    if res == False:
        raise HTTPException(429, "Too Many Requests", headers={"Retry-After": "renew subscription"})
    return key


@app.get("/consume/{key}")
async def consume_key(key:str):
    res = await cl.decrease(key)
    return {"key": key, "alive":res}

@app.get("/destroy/{key}")
async def destroy(key:str):
    res = await cl.destroy(key)
    res = "not found" if res is False else "ok"
    return {"destroy":res}

@app.get("/reset/{key}/{value}")
async def reset(key:str,value:int):
    res = await cl.reset(key, value)
    res = "not found" if res is None else "ok"
    return {"reset":res}

@app.get("/status")
async def status():
    values = await cl.status()
    return values

@app.get("/depends/{key}")
async def consume_key(key: dict = Depends(check_key)):
    res = await cl.decrease(key)
    return {"key": key, "alive":res}
