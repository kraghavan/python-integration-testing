import unittest
from confluent_kafka import Consumer, KafkaException
import json

class KafkaConsumerTest(unittest.TestCase):
    def setUp(self):
        self.consumer = Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'test',
            'auto.offset.reset': 'earliest',
        })

    def tearDown(self):
        self.consumer.close()

    def test_data_pushed_to_kafka(self):
        self.consumer.subscribe(['test'])

        try:
            msg = self.consumer.poll(1.0)
            if msg is None:
                pass
            if msg.error():
                raise KafkaException(msg.error())
            else:
                data = json.loads(msg.value().decode('utf-8'))
                self.assertEqual(data["name"], "John Doe")
                self.assertEqual(data["email"], "john.doe@example.com")
                self.assertEqual(data["id"], 1234)
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    unittest.main()