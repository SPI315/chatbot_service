import os
import sys
import pika
from dotenv import load_dotenv

env_path = os.path.join(sys.path[0], ".env")
load_dotenv(env_path)
user = os.getenv("RM_USER")
pswrd = os.getenv("RM_PASSWORD")

# Параметры подключения
connection_params = pika.ConnectionParameters(
    host="rabbitmq",  # Замените на адрес вашего RabbitMQ сервера
    port=5672,  # Порт по умолчанию для RabbitMQ
    virtual_host="/",  # Виртуальный хост (обычно '/')
    credentials=pika.PlainCredentials(
        username=user,  # Имя пользователя по умолчанию
        password=pswrd,  # Пароль по умолчанию
    ),
    heartbeat=30,
    blocked_connection_timeout=2,
)

# Имя очереди
queue_name = "prediction_queue"
