import unittest
import pika
import json
import traceback
import time

import sys

RABBITMQ_HOST = "rabbitmq"
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE = 'test'
RABBITMQ_USERNAME = 'guest'
RABBITMQ_PASSWORD = 'guest'
BLOCKED_CONNECTION_TIMEOUT = 300

MINN = 0
MAXX = 1
time.sleep(20)

class TestRabbitMQ(unittest.TestCase):
    def setUp(self):
        try:
            self.port = RABBITMQ_PORT
            self.host = RABBITMQ_HOST
            self.message_count = MINN
            self.max_messages = MAXX # max expected msgs
            credentials=pika.PlainCredentials(username=RABBITMQ_USERNAME, 
                                            password=RABBITMQ_PASSWORD)
            # Define connection parameters
            parameters = pika.ConnectionParameters(credentials=credentials, 
                                                host=self.host, 
                                                port=self.port, 
                                                blocked_connection_timeout=BLOCKED_CONNECTION_TIMEOUT)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()

    def tearDown(self):
        self.connection.close()

    def callback(self, ch, method, properties, body):
        self.message_count += 1
        self.data = json.loads(body.decode())  # assuming the body is a JSON string
        print(f"Received message {self.message_count}: {self.data}")
        if self.message_count >= self.max_messages:
            ch.stop_consuming()

    def test_data_pushed_to_rabbitmq(self):
        try:
            self.queue = RABBITMQ_QUEUE

            self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=True)
            self.channel.start_consuming()

            self.assertEqual(self.data["name"], "John Doe")
            self.assertEqual(self.data["email"], "john.doe@example.com")
            self.assertEqual(self.data["id"], 1234)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()

if __name__ == '__main__':
    unittest.main()