# requests-counter

A tool to monitoring the number of requests from an or multiple _api_key_.

![ci/cd](https://github.com/Arfius/requests-counter/actions/workflows/request-counter.yml/badge.svg)

#### Use cases

Scenario: A Company that sell a Service that is limited by a max amount of requests.

- As a Company, I would set a request limit for an _api_key_.
- As a Company, I would update/destroy/inspect the status of subscription via api.

### Installation

#### Requirement

 Install *redis* or run a docker container as below

```bash
$> docker run --name test-redis -p6379:6379 -ti redis redis-server --appendonly yes
```

### Package Installation

```bash
$> pip install requests-counter
```



## Usage

### As request counter for fastapi

```python
from fastapi import Depends, FastAPI, HTTPException

#1. Import the library
from requests_counter.reqcounter import ReqCounter

import asyncio
app = FastAPI()

#2. Create an ReqCounter object with the url to redis instance as parameter
cl = ReqCounter("redis://localhost")

#3. populate the Object with a list of tuple (key, max_value)
asyncio.create_task(cl.setup([("my-api-key-test",10)]))

#4. Declare a function to inject to Depends module. It will decrease the max_value for each request. It will raise a 429 HTTPException when max_value is 0.
async def check_key(key:str):
    res = await cl.decrease(key)
    if res == False:
        raise HTTPException(429, "Too Many Requests", headers={"Retry-After": "renew subscription"})
    return key

#5. Inject the check_key function to endpoint
@app.get("/consume/{key}")
async def consume_key(key: dict = Depends(check_key)):
    return {"job": "done"}
```

### As endpoint 

Command below run the server to interact with your redis instance for

- Destroy a key
- Update the value (i.e. renewal)
- Get the status of all keys


```bash
$> uvicorn requests_counter.api:app --reload --port 8080
```

Run `http://locahost:8080/dosc` for documentation.
