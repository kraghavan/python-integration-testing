import unittest
from confluent_kafka import Consumer, KafkaException
import json
import time

KAFKA_CONTAINER_NAME = "my_kafka_container"
KAFKA_HOST = "kafka"
KAFKA_PORT = 9092
KAFKA_TOPIC = 'test'
KAFKA_BOOSTRAP_SERVERS = f"{KAFKA_HOST}:{KAFKA_PORT}"

time.sleep(120)

class KafkaConsumerTest(unittest.TestCase):
    def setUp(self):
        self.consumer = Consumer({
            'bootstrap.servers': KAFKA_BOOSTRAP_SERVERS,
            'group.id': KAFKA_TOPIC +'_' +str(time.time()),
            'auto.offset.reset': 'earliest',
        })

    def tearDown(self):
        self.consumer.close()

    def test_data_pushed_to_kafka(self):
        self.consumer.subscribe([KAFKA_TOPIC])

        try:
            msg = self.consumer.poll(5.0)
            if msg is None:
                print("No messages found")
            else:
                data = json.loads(msg.value().decode('utf-8'))
                self.assertEqual(data["name"], "John Doe")
                self.assertEqual(data["email"], "john.doe@example.com")
                self.assertEqual(data["id"], 1234)
        except Exception as e:
            print(f"An error occurred: {e}")
if __name__ == '__main__':
    unittest.main()