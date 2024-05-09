import json, logging, sys, time, os
from fastapi.responses import JSONResponse
from .amqp_factory import AmqpFactory
from ..cache.locker import LockerService
from ..utility.config import GlobalConfig


class WorkerService:
    logger = logging.Logger(__name__)
    amqp = AmqpFactory()
    locker = LockerService()
    _cfg = GlobalConfig()

    def __init__(self) -> None:
        self.queue_name = self._cfg.QUEUE_NAME
        self.channel = self.amqp.create_channel()

    def receive_publish(self):
        try:
            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(
                queue=self.queue_name,
                on_message_callback=self._callback,
            )
            self.channel.start_consuming()
        except Exception as err:
            self.logger.error(f"[receive_publish]: {err}")

    def _callback(self, ch, method, properties, msg) -> None | JSONResponse:
        self.logger.warning(f"[receive_publish]: start to execute task: {msg}")

        # pretend time sleep as task
        json_body = json.loads(msg)
        time.sleep(len(json_body["msg"]))
        ch.basic_ack(delivery_tag=method.delivery_tag)

        unlock_response = self.locker.unlock(json_body["key"])
        if isinstance(unlock_response, JSONResponse):
            return unlock_response

        self.logger.warning(f"[receive_publish]: {unlock_response}")


if __name__ == "__main__":
    try:
        worker = WorkerService()
        worker.receive_publish()
    except KeyboardInterrupt:
        worker.logger.error("worker is interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
