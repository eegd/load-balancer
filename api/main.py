from fastapi import FastAPI
from .router import task
import logging


logging.basicConfig(level=logging.WARN, format="%(asctime)s %(levelname)s: %(message)s")

app = FastAPI()
app.include_router(prefix="/task", tags=["task"], router=task.router)
