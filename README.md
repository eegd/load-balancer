# load-balancer

There is one part of this project -> api.

## Framework
 - [fastapi](https://fastapi.tiangolo.com/) -> api using this asgi framework.

## Local Develop Setting

```bash
# setup containers
$ docker-compose up
```

## Installation

* Python version - 3.10

```
$ python3 -m pip install -r requirements.txt
or
$ pip3 install -r requirements.txt
```

## Running the app

```
$ python3 -m uvicorn api.main:app --reload --port 8000
or
$ uvicorn api.main:app --reload --port 8000
```