import unittest
import pika
import json
import time

RABBITMQ_HOST = "rabbitmq"
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE = 'test'
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
BLOCKED_CONNECTION_TIMEOUT = 300

class TestRabbitMQ(unittest.TestCase):
    def setUp(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()

    def tearDown(self):
        self.connection.close()

    def test_data_pushed_to_rabbitmq(self):
        queue = RABBITMQ_QUEUE
        self.channel.queue_declare(queue=queue)

        def callback(ch, method, properties, body):
            self.data = json.loads(body)

        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

        self.assertEqual(self.data["name"], "John Doe")
        self.assertEqual(self.data["email"], "john.doe@example.com")
        self.assertEqual(self.data["id"], 1234)

if __name__ == '__main__':
    unittest.main()