from fastapi import FastAPI, Request
from .router import task
import logging, sys

app = FastAPI()

# logging config
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    client = request.client
    method = request.method
    url = request.url
    logger.info(f"client: {client}, method: {method}, url: {url}")
    response = await call_next(request)
    return response


app.include_router(prefix="/task", tags=["task"], router=task.router)
