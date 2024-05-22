import pika
import uuid
from rmworker.connection_params import connection_params, queue_name


class RpcClient:
    def __init__(self) -> None:
        self.connection = pika.BlockingConnection(connection_params)
        self.queue_name = queue_name
        self.channel = self.connection.channel()

        # создаем верменную очередь
        result = self.channel.queue_declare(queue="", exclusive=True)
        self.response_queue = result.method.queue

        # подписываемся на временную очередь
        self.channel.basic_consume(
            queue=self.response_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

        self.response = None
        self.corr_id = str(uuid.uuid4())

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = body

    def send_message(self, message=str):
        # Отправка сообщения
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            properties=pika.BasicProperties(
                reply_to=self.response_queue,
                correlation_id=self.corr_id,
            ),
            body=message,
        )

        while self.response is None:

            # Проверка ответа на сообщение
            self.connection.process_data_events(time_limit=600)

        return self.response
