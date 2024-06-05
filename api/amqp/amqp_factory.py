from pika.adapters.blocking_connection import BlockingChannel
from ..utility.config import GlobalConfig
import logging, pika, sys


class AmqpFactory:
    logger = logging.Logger(__name__)
    _cfg = GlobalConfig()

    def __init__(self) -> None:
        self.host = self._cfg.AMQP_HOST
        self.port = self._cfg.AMQP_PORT
        self.username = self._cfg.AMQP_USERNAME
        self.password = self._cfg.AMQP_PASSWORD
        self.exchange_name = self._cfg.EXCHANGE_NAME
        self.queue_name = self._cfg.QUEUE_NAME
        self.connection = None
        self.logger.warning(
            f"[amqp_factory] 'host': '{self.host}', 'port': '{self.port}'"
        )

    def create_connection(self) -> None:
        try:
            self.logger.warning(f"[amqp_factory] rabbitmq is connected")
            credentials = pika.PlainCredentials(self.username, self.password)
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host, credentials=credentials, heartbeat=0
                )
            )
        except Exception as err:
            self.logger.error(f"[amqp_factory] {err}")

    def create_channel(self) -> BlockingChannel:
        if not self._is_connected():
            self.create_connection()
        try:
            self.logger.warning(
                f"[amqp_factory] create channel 'exchange_name': '{self.exchange_name}', 'queue_name': '{self.queue_name}'"
            )
            channel = self.connection.channel()
            channel.queue_declare(queue=self._cfg.QUEUE_NAME, durable=True)
            return channel
        except Exception as err:
            self.logger.error(f"[amqp_factory] {err}")

    def _is_connected(self):
        return self.connection is not None
