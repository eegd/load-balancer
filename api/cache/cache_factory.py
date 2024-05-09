from ..utility.config import GlobalConfig
import logging, redis, sys


class CacheFactory:
    logger = logging.Logger(__name__)
    cfg = GlobalConfig()

    def __init__(self) -> None:
        self.host = self.cfg.REDIS_HOST
        self.port = self.cfg.REDIS_PORT
        self.logger.warning(
            f"[cache_factory] 'host': '{self.host}', 'port': '{self.port}'"
        )

    def redis_client(self):
        try:
            self.logger.warning(f"[cache_factory] redis is connected")
            return redis.Redis(host=self.host)
        except Exception as err:
            self.logger.error(f"[redis client] {err}")
            sys.exit(0)
