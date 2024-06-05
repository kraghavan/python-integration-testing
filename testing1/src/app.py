import time
import json
import traceback
from rabbitmq_helper import RabbitMQPublisher
from kafka_helper import KafkaProducer

data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "id": 1234,
    "timestamp": time.time()
}

# Convert the Python dictionary to a JSON string
DATA_PAYLOAD = json.dumps(data)

def publish_rabbitmq():
    try:
        rabbit_publisher = RabbitMQPublisher()
        rabbit_publisher.connect()
        rabbit_publisher.send_message(DATA_PAYLOAD)
        rabbit_publisher.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def publish_kafka():
    try:
        kafka_producer = KafkaProducer()
        kafka_producer.produce_message(message=DATA_PAYLOAD)
        kafka_producer.close()
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def main():
    publish_rabbitmq()
    publish_kafka()

if __name__ == '__main__':
    time.sleep(10)
    main()

