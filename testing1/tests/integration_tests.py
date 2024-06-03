import unittest
import pika
import json

class TestRabbitMQ(unittest.TestCase):
    def setUp(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

    def tearDown(self):
        self.connection.close()

    def test_data_pushed_to_rabbitmq(self):
        queue = 'my_queue'
        self.channel.queue_declare(queue=queue)

        def callback(ch, method, properties, body):
            self.data = json.loads(body)

        self.channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()

        expected_data = {'key': 'value'}  # Replace with your expected data
        self.assertEqual(self.data, expected_data)

if __name__ == '__main__':
    unittest.main()