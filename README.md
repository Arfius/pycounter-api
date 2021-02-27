# requests-counter

A tool to monitor the number of HTTP requests.

It uses a key as extra parameter in the HTTP header, and optionally can filter the HTTP request per _source_ (like origin).


![ci/cd](https://github.com/Arfius/requests-counter/actions/workflows/request-counter.yml/badge.svg)

#### Use cases

Scenario: A Company that sell a Service that is limited by a max amount of requests and/or filtered by source HTTP request parameter.

- As a Company, I want to set a request limit for an _apiKey_and/or by source.
- As a Company, I want to update/destroy/inspect the status of subscription via api.

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
from fastapi import Depends, FastAPI, HTTPException, Header

# 1. Import the library
from requests_counter.reqcounter import ReqCounter

import asyncio
app = FastAPI()

# 2. Create an ReqCounter object with the url to redis instance as parameter
cl = ReqCounter("redis://localhost")

# 3. populate the Object with a list of tuple (key, max_value)
asyncio.create_task(cl.setup_api_key([("my-api-key-test", 100)]))
asyncio.create_task(cl.setup_source(["source1", "source2"]))


# 4. Declare a function to be injected into Depends module. 
# It will decrease the max_value for each request. It will raise a 429 HTTPException when max_value is 0.
# It will raise a 403 HTTPException when source is not in the list.
async def check_key(apiKey: str = Header(None), source: str = Header(None)):
    res = await cl.decrease(apiKey)
    if res is False:
        raise HTTPException(400, "User Requests Limit Exceeded")
    if await cl.check_source(source) is False:
        raise HTTPException(403, "Forbidden")
    return apiKey


# 5. Inject the check_key function to endpoint
@app.get("/consume")
async def consume_key(apiKey=Depends(check_key)):
    return {"job": "done", "apiKey": apiKey}
```
To run this example
```bash
$> uvicorn requests_counter.example:app --reload --port 8080
```

### As endpoint 

Command below run the server to interact with your redis instance for

- Destroy a key
- Update the value (i.e. renewal)
- Get the status of all keys


```bash
$> uvicorn requests_counter.api:app --reload --port 8080
```

Run `http://locahost:8080/docs` for documentation.
