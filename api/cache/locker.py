from fastapi import status
from fastapi.responses import JSONResponse
from .cache_factory import CacheFactory
from ..utility.config import GlobalConfig
import logging


class LockerService:
    logger = logging.Logger(__name__)
    cache_factory = CacheFactory()

    def __init__(self) -> None:
        self.cfg = GlobalConfig()
        self.redis_client = self.cache_factory.redis_client()

    def lock(self, key: str) -> JSONResponse | None:
        try:
            request_key = self._request_key(key)
            num_queue = self._num_queue(request_key)
            if num_queue == self.cfg.MAX_KEY_REQUEST:
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content="key requests has reached the limit",
                )
            self.redis_client.incr(request_key)
            return
        except Exception as err:
            self.logger.error(f"[locker]: {err}")

    def unlock(self, key: str) -> JSONResponse | None:
        try:
            request_key = self._request_key(key)
            num_queue = self._num_queue(request_key)
            if num_queue == 0:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content="key not found",
                )
            self.redis_client.decr(request_key)
            return
        except Exception as err:
            self.logger.error(f"[locker] {err}")

    def _request_key(self, key: str) -> str:
        return f"requests:task_{key}"

    def _num_queue(self, key: str):
        current_num = self.redis_client.get(key)
        return int(current_num) if current_num else 0  # type: ignore
